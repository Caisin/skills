---
name: kx-sea-orm
description: |
  Use when 任务明确聚焦 SeaORM 与 `#[derive(Sea)]` 的模型定义、迁移、通用增删改查、事务、多数据源和多表操作示例，且明确禁止用 SeaORM relation 做外键。

  触发场景：
  - 需要给 `ents/` 或下游业务仓库补一套 SeaORM 示例代码
  - 需要解释 `qry()/sel()/m()/get()/auto_migrate()` 应该怎么配合使用
  - 需要示范不依赖 `belongs_to/has_many/find_with_related` 的手工外键与多表读写
  - 需要把 `derives/codegen/src/table/sea` 的生成能力翻译成可直接照抄的业务模板
  - 需要明确数据库字段设计、软删除设计、主键与索引命名规范

  触发词：SeaORM、derive(Sea)、模型定义、迁移、CRUD、事务、多数据源、多表、外键、relation、auto_migrate、qry、sel、ModifyModel、字段设计、索引设计、主键设计、is_del
---

# kx-sea-orm

`kx-sea-orm` 是当前仓库里专门给 SeaORM + `#[derive(Sea)]` 写示例代码的 skill。
它聚焦**实体定义、迁移、CRUD、事务、多数据源、多表操作**六类场景，并且默认坚持：**不要用 SeaORM relation 做外键建模**。

如果仓库里的 SeaORM 生成能力、实践约定或目录规范发生变化，必须同步更新本 skill、相关 repo-local skills 与 `AGENTS.md`，避免示例与真实能力漂移。

## 适用边界

### 适用

- 需要写 `#[derive(Sea)]` 模型定义示例
- 需要写 `prelude::migrate()` / `auto_migrate()` 风格迁移示例
- 需要写标准新增、查询、分页、更新、软删除示例
- 需要写 `SeaTrans` 单库或多库事务示例
- 需要写多数据源联动示例
- 需要写**不使用 relation** 的多表读写示例
- 需要制定字段长度、类型、软删除、主键、索引命名等数据库设计规范

### 不适用

- 纯 Rust 编译器 / trait / 生命周期 / Send / Sync 问题
  - 交给 `rust-router`
- 重点是 `svc/ctl/router/install` 或完整实践层分层落地
  - 交给 `kx-rs`
- 重点是 `sdks/` 第三方接入
  - 交给 `kx-sdk` / `kx-sdk-aigc`

## Reference Selection

按任务类型优先读取：

- 模型定义 / 迁移 / CRUD / 事务 / 多数据源 / 多表操作模板
  - 读 `references/patterns.md`
- 想确认 `#[derive(Sea)]` 到底生成了哪些能力
  - 读 `references/codegen-map.md`
- 还需要回看仓库原始参考
  - 对照 `.agents/skills/kx-rs/references/sea-usage.md`
  - 对照 `.agents/skills/kx-rs/references/crud-workflow.md`
  - 对照 `derives/codegen/src/table/sea/`

## 核心规则

1. **禁止用 SeaORM relation 做外键**
   - 不要依赖 `belongs_to`、`has_many`、`find_with_related`、`find_also_related` 这类 relation 流程。
   - 外键语义统一使用普通字段（如 `dept_id`、`user_id`）+ 业务层校验 + 事务保证一致性。
2. **模型默认保留空 `Relation`**
   - 示例里的 `Relation` 维持空枚举：`pub enum Relation {}`。
3. **优先走生成能力，不回退到大段手写 SeaORM 样板**
   - 主键查询优先 `<T>::get(c, pk)`
   - 简单筛选优先 `<T>::sel()`
   - 复杂条件 / 排序 / 分页 / 批量更新优先 `<T>::qry()`
   - 更新构造优先 `<T>::m()` 或 `update_set(...)`
4. **软删表默认过滤 `is_del_eq(false)`**
   - 分页默认补稳定排序；如果没有显式排序，优先 `desc_id()`。
5. **迁移优先使用模型自带 `auto_migrate()` / `create_index()` 能力**
   - 这些能力来自 `derives/codegen/src/table/sea` 的生成代码，不需要每次手写 `MigrationTrait`。
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
10. **多表读取优先两段式 / 显式查询**
   - 先查主表，再批量查从表，然后在 service 层组装返回值。
11. **涉及 `bins/` / `bizs/` / `ents/` 的目录表达时，要明确这是下游业务仓库约定**
   - 当前工作区本身没有 `bizs/` 或 `bins/`。

## 推荐回答顺序

1. 先判断用户要的是六类示例中的哪几类
2. 再从 `references/patterns.md` 只摘对应章节
3. 如果用户问“为什么能这么写”，再补 `references/codegen-map.md`
4. 若问题已经扩展到完整业务分层或路由，再 handoff 到 `kx-rs`

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 看到外键就去写 belongs_to / has_many relation
❌ 忽略 derive 生成的 qry/sel/m/get，退回 Entity::find() / ActiveModel 大段手写
❌ 把多表读取全塞进 relation，而不是显式两段查询
❌ 迁移时只会手写 SeaORM MigrationTrait，不知道当前仓库模型自带 auto_migrate()
❌ 说“这是当前仓库的 bizs/bins 结构”，把下游业务仓库约定和当前工作区事实混在一起
```

### 正确做法

```text
✅ 用普通字段表达外键，如 dept_id / user_id / order_id
✅ 通过 service 层先校验关联记录存在，再执行写入
✅ 查询优先用 <T>::get / <T>::sel / <T>::qry / <T>::m()
✅ 迁移优先展示 prelude::migrate() + Model::auto_migrate() + Model::create_index()
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
给我一套 kx 里能用的 SeaORM 示例：用户表和部门表，包含模型定义、迁移、CRUD、事务、多数据源和多表查询，而且不要用 relation。
```

**Output direction**

```text
- 先明确这是 kx-sea-orm 命中的六段式示例场景。
- 先给模型定义与迁移，再给 CRUD 与事务，最后给多数据源和多表两段查询。
- 明确 dept_id 只是普通字段，关联一致性靠业务层校验与事务保证，不使用 SeaORM relation。
- 如果用户后续还想继续扩成完整 biz/svc/ctl/router 落地，再 handoff 到 kx-rs。
```
