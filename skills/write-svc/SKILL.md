---
name: write-svc
description: |
  Use when 编写或修改业务 service，包括校验、查询、事务、幂等、upsert、CAS、多表读写、多数据源和一致性边界。

  触发场景：
  - 编写 `src/svc/<subdomain>/*.rs`
  - 使用实体 alias 的 `get/qry/sel/m/update_set/upsert/upsert_many`
  - 设计单库事务、多库 best-effort、幂等、outbox、lease、fencing 或乐观锁
  - 组装多表结果、避免 N+1、维护缓存失效顺序

  触发词：service、svc、事务、查询、CRUD、update_set、upsert、幂等、CAS、乐观锁、多表、多数据源、SeaTrans、outbox、lease、fencing
---

# Write Svc

负责业务规则和一致性。它消费 entity 提供的类型化能力，对 ctl 暴露稳定业务方法。

## 适用边界

### 适用

- 输入业务校验、权限无关的领域规则和稳定错误语义
- 查询、分页、写入、事务、多表组装、幂等与并发控制
- 数据源 alias、跨库边界和缓存失效顺序
- task/provider 等外部副作用与数据库状态的编排

### 不适用

- 表、字段、relation、索引和 schema sync：使用 `write-entity`
- HTTP extractor、响应包装、API code 和路由策略：使用 `write-ctl`
- SDK 协议实现：使用对应 SDK skill

## Reference Selection

- 编写查询、写入、事务、多表逻辑时读 `references/patterns.md`
- 数据库并发行为测试同时使用 `database-tests` 和 `write-tests`

## 核心规则

1. svc 负责校验、事务、幂等、多表组装和一致性；ctl 不承担这些职责。
2. 静态单表查询优先实体 alias 的 `get/get_opt/qry/sel`，不展开完整模块路径。
3. alias、字段 Query、`COLUMN`、`update_set`、ActiveModel setter、insert/upsert 和索引 helper 已由
   `derive(Sea)` 生成；svc 直接消费这些契约，不重新声明 Model alias 或 CRUD wrapper。
4. 分页和批处理补稳定排序；多表列表使用“主表分页 -> 批量从表 -> 内存组装”。
5. 局部条件更新优先 `Alias::qry().<field>_eq(...).update_set(...)`；新建且必须拒绝重复时用 `insert`；完整 Model 按主键允许覆盖时用 `upsert`。
6. generated upsert 以主键为冲突目标，不隐式使用自然唯一键。
7. `update_set` 返回 SeaORM `UpdateResult`；version、lease、fencing、claim 和状态前置条件必须进入查询条件，并校验 `rows_affected == 1`。
8. 不可变流水、审计、安全事件和账本使用 insert，不做覆盖写。
9. 事务统一使用 `SeaTrans::t`；需要保留领域错误类型时使用 `SeaTrans::sea_trans`。不要在业务示例中手写 `begin/commit/rollback`。单数据源保持数据库原子性，多数据源只提供 best-effort 顺序提交。
10. 时间统一使用 `kx_tools::times::sys_timestamp()`，不在各模块定义 `now_ts()`。
11. 实体已实现 `Default` 且 `None/0/false` 确实是稳定缺省值时，构造使用 `..Default::default()`；状态、时间、版本、权限等业务关键字段仍显式赋值，不为必填 DTO 静默补默认值。

## 常见错误 vs 正确做法

```text
❌ 用 upsert 实现 CAS、lease、fencing 或不可变流水
❌ 在业务 service 中手写 begin/commit/rollback
❌ 在循环里逐条查询关联表，或在远端调用期间持有长事务
❌ 把 SeaTrans 描述成跨库原子事务
❌ 为了少写字段给必填 DTO 实现 Default，掩盖缺失输入
❌ `derive(Sea)` 后又定义业务 Model alias、字段查询器或 update/upsert wrapper
✅ svc 明确写入语义、事务边界、幂等和失败行为
✅ 只对稳定缺省字段使用 `..Default::default()`，关键业务字段保持显式
```

## 输出模板

```text
业务规则
查询与写入语义
事务与并发边界
错误与幂等
验证方式
```

## 完整示例

**Input**

```text
写一个按到期时间扣减资产批次并生成 outbox 的 service。
```

**Output direction**

- 通过 `SeaTrans::t` 获取业务数据源事务并检查幂等键。
- 用 alias query 稳定排序批次。
- 普通局部字段使用 `update_set`；version 扣减使用可校验影响行数的条件更新，同时写不可变流水和 outbox。
- 任一步失败回滚；余额不足返回稳定领域错误。
