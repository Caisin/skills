---
name: write-entity
description: |
  Use when 编写或修改 SeaORM 2 dense entity、字段类型、relation、Schema、索引、备注和业务 crate 的 install 迁移入口。

  触发场景：
  - 新增或调整 `src/entity/<subdomain>/*.rs`
  - 使用 `#[sea_orm::model]`、`model_attrs(derive(Sea))`、`comment`、`unique_key`
  - 设计主键、软删、JSON、枚举、索引和无数据库外键 relation
  - 编写 `XxxInstall::migrate()/migrate_with()` 与 schema sync

  触发词：entity、实体、SeaORM、sea_orm::model、derive(Sea)、Schema、迁移、install、索引、unique_key、comment、relation、skip_fk、auto_migrate
---

# Write Entity

负责业务 crate 的持久化模型和 Schema 契约。它不编写业务事务，也不编写 HTTP handler。

## 适用边界

### 适用

- dense entity、枚举、字段类型、主键、软删和 relation
- 表/字段备注、单列索引、联合唯一索引和显式联合普通索引
- `install.rs` 中的 schema registry sync 和备注同步
- `#[derive(Sea)]` 生成能力的模型侧约定

### 不适用

- 查询编排、事务、幂等、CAS、多表写入：使用 `write-svc`
- DTO、handler、`ApiRouter`、接口权限策略：使用 `write-ctl`
- 数据库行为测试与外部数据库环境：使用 `database-tests`

## Reference Selection

- 写实体、relation、索引或迁移时读 `references/patterns.md`
- 新增数据库行为测试时同时使用 `database-tests` 和 `write-tests`

## 核心规则

1. 使用 `#[sea_orm::model]` 和 `model_attrs(derive(Sea))`，不手写空 `Relation`。
2. 每张表和持久化字段都写 SeaORM `comment`；已有 `comment` 时不保留重复 `///`。
3. relation 只表达查询关系。拥有关系字段的 `belongs_to` 必须 `skip_fk`，数据库不创建外键。
4. 普通业务表优先 `i64` 自增主键；兼容 SQLite 的持久化数字不用无符号类型。
5. JSON 使用 `Json`；时间戳统一调用 `kx_tools::times::sys_timestamp()`。
6. `indexed`、`unique`、同名 `unique_key` 分别表达单列普通、单列唯一和联合唯一索引。
7. 联合普通索引和同一字段参与第二个联合唯一分组时，在 `install.rs` 显式创建。
8. 业务迁移只由 `XxxInstall::migrate()/migrate_with()` 暴露，不创建 `entity/prelude.rs`。
9. `sync_schema_with_comments()` 只补缺失对象；类型修改、删除和已有约束调整使用显式 migration。

## 常见错误 vs 正确做法

```text
❌ 用重复 rustdoc 代替表和字段 comment
❌ 在 relation 上创建数据库外键，或把联合普通索引误写成 unique_key
❌ 在 entity/prelude.rs 和 install.rs 维护两套迁移入口
✅ entity 声明模型契约，install.rs 统一补充同步和显式索引
```

## 输出模板

```text
模型与字段
关系与一致性边界
索引与迁移
目录落点
验证方式
```

## 完整示例

**Input**

```text
新增一张 outbox entity，需要联合唯一幂等键、普通消费索引和表字段备注。
```

**Output direction**

- entity 用同名 `unique_key` 表达联合唯一幂等键。
- 联合普通消费索引放 `install.rs`。
- `XxxInstall::migrate_with()` 先执行 registry sync，再补显式索引。
- SQLite 测试验证重复迁移、唯一约束和索引列顺序。
