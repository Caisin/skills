---
name: database-tests
description: |
  Use when 运行或编写依赖 SeaORM、Toasty、Redis、数据库驱动或其它外部服务的测试，需要选择 feature、隔离环境并准确报告前置条件。

  触发场景：
  - 测试 kx-sea-orm、实体迁移或多数据源行为
  - 测试 Toasty、Redis/cache 或需要本地服务的能力
  - 排查只在 MySQL、PostgreSQL、SQLite 或特定 feature 下出现的问题

  触发词：数据库测试、SeaORM 测试、Toasty 测试、MySQL、PostgreSQL、SQLite、Redis、DATABASE_URL、外部服务测试
---

# Database and External-service Tests

此 skill 替代 Toasty 仓库的 `dynamodb-tests`：kx 没有统一 DynamoDB 驱动测试套件，实际边界是多个 crate、可选数据库 feature 与不同外部服务。

## 适用边界

### 适用

- `kx-sea-orm`、实体、迁移、事务与多数据源测试
- Toasty 或缓存/Redis 等依赖外部服务的测试
- 驱动 feature 组合和环境隔离

### 不适用

- 完全纯内存的普通单元测试
- 上游 Toasty 仓库自己的 DynamoDB integration suite

## Reference Selection

- feature 与命令选择
  - 读目标 crate 的 `Cargo.toml`
- 环境、隔离与结果报告模板
  - 读 `references/patterns.md`
- 测试代码组织
  - 使用 `write-tests` skill

## 核心规则

1. 不假设 workspace 有统一数据库测试命令；先定位目标 crate、feature 和现有测试。
2. SQLite 可用于语义相同的自包含测试；MySQL/PostgreSQL 特有行为必须在对应后端验证，不能用 SQLite 代替。
3. 连接信息来自测试环境变量或临时 fixture，不新增真实凭据、固定开发库地址或共享生产资源。
4. 测试数据使用唯一命名或事务/临时库隔离，不依赖测试执行顺序。
5. 环境不可用时明确报告“未运行及前置条件”，不能把 feature 编译通过当作数据库行为通过。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 直接照搬 Toasty 的 --features dynamodb 命令
❌ 在测试中硬编码开发数据库账号和地址
❌ PostgreSQL 特有语义只在 SQLite 上验证
```

### 正确做法

```text
✅ 从目标 Cargo.toml 核实 mysql/postgres/sqlite feature
✅ 区分 compile/check、连接测试和行为测试证据
✅ 外部服务缺失时记录准确的 Not-tested 条件
```

## 输出模板

```text
目标 crate/行为
所需 feature
环境前置条件
隔离方式
运行命令
验证结果/未验证项
```

## 完整示例

**Input**

```text
运行 kx-sea-orm 的 PostgreSQL 时区测试。
```

**Output direction**

```text
- 先核实 crates/sea-orm/Cargo.toml 的 postgres feature 与测试过滤名
- 使用专用测试数据库连接信息，不写入仓库
- 运行目标测试并区分编译成功、连接成功和时区断言结果
```
