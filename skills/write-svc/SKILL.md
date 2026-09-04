---
name: write-svc
description: |
  Use when 编写业务查询、写入、事务、幂等、CAS、多表或多数据源一致性。
  触发词：service、svc、事务、查询、CRUD、upsert、update_set、幂等、CAS、outbox
---

# Write Svc

service 负责业务规则与一致性；entity/Schema 交给 `write-entity`，HTTP 协议交给 `write-ctl`。

## Reference Selection

- 查询、写入、事务和并发模式：读 `references/patterns.md`。
- 数据库并发测试：同时使用 `database-tests` 与 `write-tests`。

## 核心规则

1. 静态单表查询优先生成 alias 的 `get/get_opt/qry/sel`；动态 JOIN、聚合、后端专属条件和 CAS 可使用 SeaORM builder。
2. 分页和批处理必须稳定排序；多表列表采用“主表分页、从表批量查询、内存组装”，避免 N+1。
3. 新建且拒绝重复、流水、审计、账本用 `insert`；完整 Model 允许主键覆盖用 `upsert`；局部条件更新用 `update_set`。
4. 已加载 `ActiveModel::update` 可用于 SeaORM 原生局部更新；不得机械改成可能插入缺失记录的 `upsert`。
5. version、lease、claim、fencing 和状态前置条件必须进入更新条件并检查 `rows_affected == 1`。
6. 单数据源使用 SeaORM `transaction` helper；通过数据源 alias 取事务或跨库 best-effort 协调时使用 `SeaTrans`。跨库不承诺原子性。
7. 外部调用不占用长事务，使用 outbox、持久化任务或可重试状态机衔接。
8. `sort/sort_or` 适用于实体字段与回退语义一致的列表；需要字段别名或稳定 `invalid_sort` 错误时保留显式白名单。
9. 状态、时间、版本和权限字段显式赋值；仅稳定的 `None/0/false` 用 `..Default::default()`。
10. 单个业务实现文件不超过 1000 行；按子域拆到 `svc/<domain>.rs`，`mod.rs` 只声明和重导出，禁止用 `include!` 拼接超长实现。

## 验证

先跑目标回归测试，再跑目标 crate Clippy；涉及事务时验证中途失败回滚、幂等和并发冲突。
