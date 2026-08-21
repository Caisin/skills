# KX Sea ORM Codegen Map

用于把 `derives/codegen/src/table/sea` 的生成代码，映射成业务侧可直接使用的能力清单。

## 1. `mod.rs`

关键点：

```text
- 生成 #[sea_orm::model] dense entity 模板。
- 通过 model_attrs(derive(Sea)) 只给持久化 Model 注入 KX 扩展。
- Relation、ModelEx、ActiveModelEx 等类型由 SeaORM 2 生成，不手写空 Relation。
- codegen 没有业务关系元数据时不猜测 relation；下游可在 dense entity 中显式声明关系，`belongs_to` 必须带 `skip_fk`。
- 生成 get_pk_val() / unset_pks() 这类主键辅助能力。
```

对应文件：`derives/codegen/src/table/sea/mod.rs`

## 2. `sea_model.rs`

业务侧最常直接用到的入口几乎都在这里：

```text
- Model::qry() -> Query
- Model::sel() -> EntitySelect
- Model::m() -> ModifyModel
- Model::get() / get_opt() / exists()
- Model::upsert() / upsert_many() / insert()
- Model::auto_migrate()
- Model::create_index()
- 自动注册表备注和字段备注，供 SchemaCommentSyncExt 按 entity prefix 批量同步
```

这就是为什么当前仓库推荐：

```rust
let user = SysUser::get(c, id).await?;
let page = SysUser::qry().is_del_eq(false).page(c, paging).await?;
let saved = user.upsert(c).await?;
SysUser::auto_migrate(c).await?;
```

对应文件：`derives/codegen/src/table/sea/sea_model.rs`

## 3. `sea_query.rs`

这里生成每个字段的查询 builder：

```text
- xxx_eq / ne / ge / le / bt
- xxx_like / contains / start_with / end_with
- xxx_is_in / not_in
- asc_xxx / desc_xxx
- one() / one_opt() / all() / page()
- update_set()
- exists()
- 静态条件使用 SeaORM 2 `COLUMN.<field>`；运行时字符串排序继续使用 `Column::from_str`
```

所以多表场景里，批量查询常见写法是：

```rust
SysDept::qry().id_is_in(dept_ids).all(c).await?
```

对应文件：`derives/codegen/src/table/sea/sea_query.rs`

`sea_entity_select.rs` 生成 `sel()` 后的过滤与多字段排序，同样使用强类型
`COLUMN.<field>`。通用 `Cond` 通过 `IntoSimpleExpr` 接受 SeaORM 2 typed column wrapper，
不再要求旧 `ColumnTrait`。

## 4. `sea_modify_model.rs`

这里负责“构造待保存/待更新对象”的写法：

```text
- set_xxx() / unset_xxx() / get_xxx()
- set_default()
- get_pk_val()
- upsert() / insert() / update()
- 显式 IntoActiveModel：Some(value) 转 Set，未设置字段转 NotSet
- cols()
```

创建 DTO 使用 `insert`，缺少主键的字段保持 `NotSet`；只有主键已经设置且业务允许
覆盖时才使用 `upsert`：

```rust
let mut m = SysUser::m();
m.set_name(name)
 .set_mobile(mobile)
 .set_dept_id(dept_id);
let created = m.insert(c).await?;
```

对应文件：`derives/codegen/src/table/sea/sea_modify_model.rs`

## 5. `sea_entity.rs`

这里补了实体级 schema sync 入口：

```text
- Entity::upsert() / upsert_many() / upsert_many_statement()
- upsert 冲突目标为 PrimaryKey::iter()，更新非主键列
- Entity::auto_migrate()
- SchemaBuilder::sync 创建缺失表、列和索引
- SchemaSyncConnection 约束 schema sync 可接受的连接
- create_table() 暂时作为 deprecated 转发
```

`auto_migrate()` 不修改或删除已有对象；破坏性结构变更仍需显式 migration。
generated upsert 不会自动选择自然唯一键；这类冲突目标必须由业务显式构造
`OnConflict`。

crate 级迁移优先调用
`SchemaCommentSyncExt::sync_schema_with_comments("my_crate::entity::*")`。该 trait 复用
SeaORM 官方 entity registry sync，再读取 `derive(Sea)` 自动注册的备注元数据；业务
`install.rs` 不需要逐表维护 `add_col_comment()` 调用，也不要再创建重复迁移职责的
`entity/prelude.rs`。

对应文件：`derives/codegen/src/table/sea/sea_entity.rs`

## 6. 这份 codegen map 怎么用

### 当用户只想“要一套示例”

优先贴 `references/patterns.md`，不要先上源码细节。

### 当用户追问“为什么有 qry()/m()/auto_migrate() 这些能力”

再补这份 map，并指出对应源码文件。

### 当用户遇到生成行为不符合预期

优先回看：

- `derives/codegen/src/table/sea/mod.rs`
- `derives/codegen/src/table/sea/sea_model.rs`
- `derives/codegen/src/table/sea/sea_query.rs`
- `derives/codegen/src/table/sea/sea_modify_model.rs`
- `derives/codegen/src/table/sea/sea_entity.rs`

## 常见错误

```text
❌ 只记住 qry()/m()/auto_migrate() 能用，却不知道它们来自哪里
❌ 以为 derive 只生成 Entity/Model，没有 Query 和 ModifyModel
❌ 手写空 Relation，或让 Sea derive 同时落到 ModelEx
❌ 期待 codegen 根据普通 ID 字段自动猜测 relation
❌ `belongs_to` 遗漏 `skip_fk`，让实体 Schema DDL 创建数据库外键
❌ 把 upsert 与 SeaORM 原生 ActiveModelTrait::save 混为一谈
❌ 业务代码退回 module::Entity::find() + module::Column::Field，绕过生成的 alias API
❌ 把索引、动态字段解析和 ActiveModel 状态也机械替换成 typed COLUMN
❌ 生成行为不符合预期时，只在业务代码里猜，不回看 derives/codegen
```

## 正确做法

```text
✅ 先用 patterns.md 回答业务模板，再用这份 map 解释生成来源
✅ 需要确认 API 边界时，直接按文件回看 sea_model.rs / sea_query.rs / sea_modify_model.rs
✅ dense entity 使用 model_attrs(derive(Sea))，冲突更新显式使用 upsert
✅ 显式 relation 使用 BelongsTo / HasOne / HasMany，关系拥有侧声明 skip_fk
✅ 迁移、查询、更新模板都优先和 codegen 真实生成能力保持一致
✅ 业务静态查询使用 Alias::get/qry/sel，生成器内部使用 COLUMN.<field>
✅ 索引、动态字符串字段解析、ActiveModel 状态和必要的底层更新继续使用 Column 枚举
```
