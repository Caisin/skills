---
name: kx-sea-orm
description: |
  Use when 任务明确聚焦 SeaORM 与 `#[sea_orm::model]` + `#[derive(Sea)]` 的模型定义、迁移、通用增删改查、事务、多数据源和多表操作示例；允许使用 relation，但禁止创建数据库外键。

  触发场景：
  - 需要给 `ents/` 或下游业务仓库补一套 SeaORM 示例代码
  - 需要解释 `qry()/sel()/m()/get()/auto_migrate()` 应该怎么配合使用
  - 需要示范 `belongs_to/has_one/has_many`、`skip_fk` 或两段式多表读写
  - 需要把 `derives/codegen/src/table/sea` 的生成能力翻译成可直接照抄的业务模板
  - 需要明确数据库字段设计、软删除设计、主键与索引命名规范

  触发词：SeaORM、sea_orm::model、derive(Sea)、模型定义、迁移、CRUD、upsert、schema sync、事务、多数据源、多表、外键、relation、auto_migrate、qry、sel、ModifyModel、字段设计、索引设计、主键设计、is_del
---

# kx-sea-orm

`kx-sea-orm` 是当前仓库里专门给 SeaORM 2 dense entity + `#[derive(Sea)]` 写示例代码的 skill。
它聚焦**实体定义、迁移、CRUD、事务、多数据源、多表操作**六类场景，并且默认坚持：**可以使用 SeaORM relation，但不能创建数据库外键**。

如果仓库里的 SeaORM 生成能力、实践约定或目录规范发生变化，必须同步更新本 skill、相关 repo-local skills 与 `AGENTS.md`，避免示例与真实能力漂移。

## 适用边界

### 适用

- 需要写 `#[sea_orm::model]` + `model_attrs(derive(Sea))` 模型定义示例
- 需要写业务 `XxxInstall::migrate()/migrate_with()` 或实体 `auto_migrate()` 迁移示例
- 需要写标准新增、查询、分页、更新、软删除示例
- 需要写 `SeaTrans` 单库或多库事务示例
- 需要写多数据源联动示例
- 需要写 relation、loader 或两段式多表读写示例
- 需要制定字段长度、类型、软删除、主键、索引命名等数据库设计规范

### 不适用

- 纯 Rust 编译器 / trait / 生命周期 / Send / Sync 问题
  - 交给 `rust-router`
- 重点是 `svc/ctl/router/install`、openapi-scan 兼容或完整实践层分层落地
  - 交给 `kx-rs`
- 重点是 `sdks/` 第三方接入
  - 交给 `kx-sdk` / `kx-sdk-aigc`

## Reference Selection

按任务类型优先读取：

- 模型定义 / 迁移 / CRUD / 事务 / 多数据源 / 多表操作模板
  - 读 `references/patterns.md`
- 想确认 `#[derive(Sea)]` 到底生成了哪些能力
  - 读 `references/codegen-map.md`
- 想了解 SeaORM 2.0 正式版新增能力与 KX 采用边界
  - 读 `references/sea-orm-2.md`
- 还需要回看仓库原始参考
  - 对照 `.agents/skills/kx-rs/references/sea-usage.md`
  - 对照 `.agents/skills/kx-rs/references/crud-workflow.md`
  - 对照 `derives/codegen/src/table/sea/`

## 核心规则

1. **允许 relation，但禁止数据库外键**
   - dense entity 可以直接声明 `belongs_to`、`has_one`、`has_many`，并使用 JOIN、loader、`find_with_related` 或 Seaography。
   - 实际持有外键字段的 `belongs_to` 必须声明 `skip_fk`；`has_one` / `has_many` 是反向关系，本身不生成数据库外键。
   - relation 只表达查询关系，不保证引用完整性；普通 ID 字段仍由 service 校验并通过事务维护一致性。
2. **模型使用 SeaORM 2 dense entity 格式**
   - 在 `Model` 前标注 `#[sea_orm::model]`，并把 KX derive 放入 `model_attrs(derive(Sea))`。
   - 不手写空 `Relation`；它与 `ModelEx`、`ActiveModelEx` 等类型由 SeaORM 生成。
3. **优先走生成能力，不回退到大段手写 SeaORM 样板**
   - 主键查询优先 `<T>::get(c, pk)`
   - 简单筛选优先 `<T>::sel()`
   - 复杂条件 / 排序 / 分页 / 批量更新优先 `<T>::qry()`
   - 更新构造优先 `<T>::m()` 或 `update_set(...)`
   - 业务代码通过实体 alias 调用这些方法，不展开为 `module::Entity::find()`；生成器内部的
     静态字段访问使用 SeaORM 2 `COLUMN.<field>`。
   - 聚合投影、运行时字段排序、复合 `Condition`、索引和 CAS 等底层场景可保留直接
     SeaORM builder；不要机械替换动态 `Column` 枚举。
4. **软删表默认过滤 `is_del_eq(false)`**
   - 分页默认补稳定排序；如果没有显式排序，优先 `desc_id()`。
5. **迁移优先使用模型自带 `auto_migrate()` / `create_index()` 能力**
   - `auto_migrate()` 使用实验性的 `SchemaBuilder::sync`，只新增缺失对象，不修改或删除已有对象。
   - crate 级 entity registry 使用 `SchemaCommentSyncExt::sync_schema_with_comments()`，在官方
     `sync()` 后按同一 prefix 补齐 PostgreSQL 表和字段备注，不再逐表调用备注 helper。
   - 业务 crate 的迁移入口只放在 `install.rs`，由 `XxxInstall::migrate()` 获取业务数据源，
     `migrate_with()` 接收既有连接；不要再创建 `entity/prelude.rs` 重复迁移职责。
   - 单列普通索引用 `indexed`，单列唯一索引用 `unique`，联合唯一索引让多列共享同一
     `unique_key`；这些索引由官方 sync 创建。dense entity 当前不能表达联合普通索引，
     这类索引继续在 `install.rs` 显式创建。
   - 迁移连接需满足 `SchemaSyncConnection`；破坏性变更继续使用显式 migration。
6. **字段命名尽量短而稳定**
   - 不要把字段名设计得过长；例如优先 `uid`，不要默认写成 `user_id`。
   - 同类缩写要在全项目保持一致，例如 `uid` / `app_id` / `dept_id` 这类约定字段。
7. **主键默认不要用 UUID**
   - 普通业务表优先使用递增整数主键（如 `i64`）。
   - UUID 主键会带来索引膨胀、写入局部性差和管理不便，不应作为默认选择。
8. **SQLite 兼容时不要用无符号整数**
   - 数字字段统一优先 `i64` / `i32`，不要使用 `u64` / `u32` / `usize` 作为持久化字段类型。
9. **JSON 字段直接使用 `Json` 类型**
   - 需要存 JSON 时，字段类型优先 `Json`，不要退回 `String` 存原始 JSON 文本。
10. **按查询形态选择 relation 或两段式查询**
   - 类型化 JOIN、loader 和 Seaography 可使用 relation；列表分页和复杂组合读取仍优先“主表 -> 批量从表 -> service 组装”，避免 N+1。
11. **涉及 `bins/` / `bizs/` / `ents/` 的目录表达时，要明确这是下游业务仓库约定**
   - 当前工作区本身没有 `bizs/` 或 `bins/`。
12. **当前稳定基线是 SeaORM 2.0.2**
   - 可直接使用 `require_one`、`raw_sql!`、嵌套 partial model、时间默认值 helper 等上游 API。
   - KX 冲突更新使用 `upsert` / `upsert_many`；`ActiveModelTrait::save` 保留 SeaORM 原生 insert/update 语义。
   - `ModifyModel` 由 KX 生成显式 `IntoActiveModel` 转换；未设置字段为 `NotSet`。
   - relation 必须与数据库外键解耦；`belongs_to` 使用 `skip_fk`，关联一致性继续由 service + 事务保证。
13. **按写入语义选择 `insert`、`upsert` 或条件更新**
   - 完整 `Model`、主键已知且业务允许覆盖时优先 `Alias::upsert`；批量覆盖使用
     `Alias::upsert_many`。
   - generated upsert 以主键为冲突目标，不把自然唯一键当作隐式冲突目标。
   - 创建时必须拒绝重复、数据库生成主键、不可变流水、审计/安全事件继续使用 `insert`。
   - version CAS、lease、fencing、claim 和依赖数据库状态前置条件的转换使用
     `update_many` / `update_set`，不能用 upsert 绕过并发约束。

## 推荐回答顺序

1. 先判断用户要的是六类示例中的哪几类
2. 再从 `references/patterns.md` 只摘对应章节
3. 如果用户问“为什么能这么写”，再补 `references/codegen-map.md`
4. 若问题已经扩展到完整业务分层、路由或 OpenAPI，再 handoff 到 `kx-rs`

## 常见错误 vs 正确做法

### 常见错误

```text
❌ `belongs_to` 遗漏 `skip_fk`，让 auto_migrate 生成数据库外键
❌ 把 relation 当作引用完整性或级联写入保证
❌ 手写空 Relation，或把 Sea derive 放进普通 derive 列表导致 ModelEx 重复生成 KX 扩展
❌ 忽略 derive 生成的 qry/sel/m/get，退回 Entity::find() / ActiveModel 大段手写
❌ 列表查询逐行加载 relation，制造 N+1
❌ 迁移时只会手写 SeaORM MigrationTrait，不知道当前仓库模型自带 auto_migrate()
❌ 把 auto_migrate 当成可修改列类型或删除字段的完整迁移系统
❌ 说“这是当前仓库的 bizs/bins 结构”，把下游业务仓库约定和当前工作区事实混在一起
```

### 正确做法

```text
✅ 用普通字段表达外键，如 dept_id / user_id / order_id
✅ 使用 #[sea_orm::model] + model_attrs(derive(Sea))，并在 belongs_to 上声明 skip_fk
✅ 使用 BelongsTo / HasOne / HasMany 直接定义 relation，由 SeaORM 生成 Relation 与 ModelEx
✅ 通过 service 层先校验关联记录存在，再执行写入
✅ 查询优先用 <T>::get / <T>::sel / <T>::qry / <T>::m()
✅ 非破坏性补齐使用 auto_migrate()，类型修改和删除使用显式 migration
✅ 冲突更新使用 upsert；SeaORM 原生 save 只表达 ActiveModel insert/update
✅ 多表读取优先“主表分页 -> 收集 IDs -> 批量查询从表 -> 内存组装”
```

## 输出模板

默认按这个结构输出：

```text
问题归类
- 命中哪几类：模型 / 迁移 / CRUD / 事务 / 多数据源 / 多表

推荐示例章节
- 优先贴哪几段模板

关键约定
- 当前回答必须强调的 3~8 条规则

最小代码骨架
- 可直接抄走的代码片段

验证方式
- 最小必要 cargo check / cargo test

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
给我一套 kx 里能用的 SeaORM 示例：用户表和部门表，包含模型定义、迁移、CRUD、事务、多数据源和多表查询；需要 relation，但不能创建数据库外键。
```

**Output direction**

```text
- 先明确这是 kx-sea-orm 命中的六段式示例场景。
- 先给模型定义与迁移，再给 CRUD 与事务，最后给多数据源和多表两段查询。
- 在用户侧 `belongs_to` 上声明 `skip_fk`，部门侧可声明 `has_many`；说明 relation 只用于查询，关联一致性仍靠业务层校验与事务保证。
- 如果用户后续还想继续扩成完整 biz/svc/ctl/router 落地，再 handoff 到 kx-rs。
```
