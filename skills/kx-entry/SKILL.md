---
name: kx-entry
description: |
  Use when 判断任务应落在哪层、哪个目录或使用哪个 repo-local skill。
  触发词：放哪里、改哪里、从哪开始、哪个目录、哪个模块、哪个 skill
---

# kx-entry

只做定位和分流，不重复实现手册。

## 仓库地图

| 目录 | 职责 |
| --- | --- |
| `core/` | 共享类型与基础抽象 |
| `crates/` | 通用框架能力 |
| `derives/` | derive 与代码生成 |
| `ents/` | 框架共享或独立发布实体 |
| `bizs/` | 可复用业务 crate，默认共置 entity/svc/ctl/install |
| `bins/` | 独立产品入口与聚合运行入口 |
| `sdks/` | 第三方 provider 接入 |
| `tools/` | CLI 与开发工具 |
| `docs/` | 用户文档、设计与长期记忆 |

## 路由规则

- Schema/entity/迁移：`write-entity`
- 查询/写入/事务：`write-svc`
- DTO/handler/router：`write-ctl`
- 数据库测试：`database-tests`；一般测试：`write-tests`
- SDK：`kx-sdk`、`google-sdk` 或 `kx-sdk-aigc`
- 公共 API、跨 crate、Schema 或安全设计：`kx-design`
- 文档、提交、PR：`prose`、`commit`、`pr`
- 后台操作体验：`admin-operator-ux`

跨层业务按 `write-entity -> write-svc -> write-ctl` 落地。框架事实优先回溯 `derives/codegen`、`crates/sea-orm` 和 `crates/axum`。
