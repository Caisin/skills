# KX Sea ORM Codegen Map

用于把 `derives/codegen/src/table/sea` 的生成代码，映射成业务侧可直接使用的能力清单。

## 1. `mod.rs`

关键点：

```text
- 生成 #[sea_orm::model] dense entity 模板。
- 通过 model_attrs(derive(Sea)) 只给持久化 Model 注入 KX 扩展。
- Relation、ModelEx、ActiveModelEx 等类型由 SeaORM 2 生成，不手写空 Relation。
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
- Model::upsert() / insert()
- Model::auto_migrate()
- Model::create_index()
```

这就是为什么当前仓库推荐：

```rust
let user = SysUser::get(c, id).await?;
let page = SysUser::qry().is_del_eq(false).page(c, paging).await?;
let mut m = SysUser::m();
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
```

所以多表场景里，批量查询常见写法是：

```rust
SysDept::qry().id_is_in(dept_ids).all(c).await?
```

对应文件：`derives/codegen/src/table/sea/sea_query.rs`

## 4. `sea_modify_model.rs`

这里负责“构造待保存/待更新对象”的写法：

```text
- set_xxx() / unset_xxx() / get_xxx()
- set_default()
- get_pk_val()
- upsert() / insert() / update()
- DeriveIntoActiveModel：Some(value) 转 Set，未设置字段转 NotSet
- cols()
```

所以新增/更新示例优先写成：

```rust
let mut m = SysUser::m();
m.set_name(name)
 .set_mobile(mobile)
 .set_dept_id(dept_id);
let saved = m.upsert(c).await?;
```

对应文件：`derives/codegen/src/table/sea/sea_modify_model.rs`

## 5. `sea_entity.rs`

这里补了实体级 schema sync 入口：

```text
- Entity::auto_migrate()
- SchemaBuilder::sync 创建缺失表、列和索引
- SchemaSyncConnection 约束 schema sync 可接受的连接
- create_table() 暂时作为 deprecated 转发
```

`auto_migrate()` 不修改或删除已有对象；破坏性结构变更仍需显式 migration。

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
❌ 把 upsert 与 SeaORM 原生 ActiveModelTrait::save 混为一谈
❌ 生成行为不符合预期时，只在业务代码里猜，不回看 derives/codegen
```

## 正确做法

```text
✅ 先用 patterns.md 回答业务模板，再用这份 map 解释生成来源
✅ 需要确认 API 边界时，直接按文件回看 sea_model.rs / sea_query.rs / sea_modify_model.rs
✅ dense entity 使用 model_attrs(derive(Sea))，冲突更新显式使用 upsert
✅ 迁移、查询、更新模板都优先和 codegen 真实生成能力保持一致
```
