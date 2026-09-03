---
name: kx-design
description: |
  Use when 设计公共 API、跨 crate、Schema/迁移、一致性、安全或分阶段工程变更。
  触发词：工程设计、架构设计、API 设计、Schema、迁移方案、事务、一致性、安全
---

# KX 工程设计

设计文档放 `docs/dev/design/`，从 `_template.md` 创建；先写用户行为和不变量，再写实现边界。

## 何时使用

- 公共 API 或 derive/codegen 契约变化
- Schema、存量数据、事务或安全边界变化
- 跨 crate/前端/数据源的非平凡改动

局部 bug、纯测试和无行为变化的重构不强制写设计。

## 必需内容

1. 目标、非目标、用户可观察行为、错误语义和兼容方式。
2. 负责 crate 与 `ctl -> svc -> entity/alias` 路径；不把业务能力放入框架 crate。
3. Schema 字段、索引、备注、迁移、数据回填与多数据库差异。
4. 单库事务、跨库 best-effort、幂等、CAS/lease/fencing/outbox 和失败恢复。
5. API method/path/code、DTO、权限、加密/明文和第三方 ingress。
6. 启动组合、任务/provider 注入、前端入口和文档影响。
7. 从目标测试到最终联合验证的分层证据。

## 大型设计

跨多个可独立验收里程碑时使用：

```text
docs/dev/design/<name>/index.md
docs/dev/design/<name>/01-<stage>.md
docs/dev/design/<name>/02-<stage>.md
```

`index.md` 是全局不变量、阶段依赖、进度、验证证据和恢复点的唯一入口。阶段按业务闭环拆分，不按 entity/svc/ctl 技术层拆分；共享入口由一个阶段收口。只有依赖已满足、文件与资源不冲突时才标并行。

## Schema 边界

- 业务 entity 用 `#[sea_orm::model] + derive(Sea)`，表/字段写 `comment`，`belongs_to` 使用 `skip_fk`。
- 缺失对象由版本化 baseline 建立；类型变更、删除、约束替换和数据回填使用显式 migration。
- SQLite 是集成基线，不能替代目标 PostgreSQL/MySQL 的 DDL 和并发验证。

## 输出

报告设计路径、行为变化、不变量、兼容边界、阶段/恢复点、开放问题和验证计划。用户只要求设计时不继续实现。
