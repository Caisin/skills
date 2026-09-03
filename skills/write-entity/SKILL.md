---
name: write-entity
description: |
  Use when 编写或修改 SeaORM 2 entity、字段、relation、索引、Schema 与安装迁移。
  触发词：entity、SeaORM、Schema、迁移、索引、comment、relation、install
---

# Write Entity

只负责持久化模型与 Schema；事务和查询编排交给 `write-svc`，HTTP 交给 `write-ctl`。

## Reference Selection

- 实体、索引、relation、迁移：读 `references/patterns.md`。
- 数据库行为测试：同时使用 `database-tests` 与 `write-tests`。

## 核心规则

1. 业务模型使用 `#[sea_orm::model]`、表/字段 `comment` 和 `model_attrs(derive(Sea))`。
2. `belongs_to` 只表达查询关系，拥有侧必须 `skip_fk`。
3. 单列索引用 `indexed/unique`，联合唯一用同名 `unique_key`，联合普通索引用 `kx(index(...))`；复杂索引写显式 migration。
4. 优先使用表名生成的 alias、Query、setter 和 CRUD。仅已有公共 API 需要兼容时保留语义 alias，不新增无意义包装。
5. 业务 Schema 使用版本化 baseline/显式 migration；每个 migration ID 独立文件，`install.rs` 只注册顺序并暴露 `XxxInstall`。
6. 不创建 `entity/prelude.rs`、`seed.rs` 或第二套安装入口。初始化数据由版本化 data migration 直接插入。
7. 条件方法使用 `_gte/_gt/_lte/_lt/_in/_not_in/_between/_not_between/_starts_with/_ends_with/_is_not_null`，不补旧名兼容层。
8. 时间戳使用 `kx_tools::times::sys_timestamp()`；JSON 使用 `Json`，持久化数值兼容 SQLite。

## 验证

- 运行目标 crate 的迁移/Schema 测试和 Clippy。
- 改动业务 entity 时运行 `rtk cargo test -p kx-rs`，通过全仓 entity 契约门禁。
