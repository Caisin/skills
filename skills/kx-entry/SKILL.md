---
name: kx-entry
description: |
  Use when 需要判断 kx 仓库任务该落在哪一层、哪个目录，或应该使用哪个 repo-local skill。

  触发场景：
  - 用户问“放哪里、改哪里、从哪开始、用哪个 skill”
  - 需要区分 core/crates/derives/ents/bizs/sdks/tools
  - 需要在 write-entity、write-svc、write-ctl、kx-sdk 或项目初始化之间路由

  触发词：放哪里、改哪里、从哪开始、哪个目录、哪个模块、哪个 skill、框架层、业务层、entity、svc、ctl
---

# kx-entry

只负责定位和路由，不重复承载各层实现手册。

## 仓库地图

| 目录 | 职责 |
| --- | --- |
| `core/` | 跨框架共享类型和基础抽象 |
| `crates/` | 通用框架能力 |
| `derives/` | derive 与代码生成 |
| `ents/` | 框架共享或需要独立发布的实体 |
| `bizs/` | 可复用业务 crate，entity 与同域 svc/ctl/install 共置 |
| `sdks/` | 第三方 provider 接入 |
| `tools/` | CLI 和开发工具 |
| `docs/` | 用户文档、设计记录和长期记忆 |

当前 workspace 没有 `bins/`；涉及应用入口时明确为下游业务仓库约定。

## 路由表

| 用户意图 | 使用 skill / 入口 |
| --- | --- |
| 新项目初始化 | `kx-project-init` |
| entity、字段、relation、Schema、索引、迁移 | `write-entity` |
| 查询、CRUD、事务、幂等、CAS、多表一致性 | `write-svc` |
| DTO、handler、ApiRouter、接口安全策略 | `write-ctl` |
| 数据库或 Redis 行为测试 | `database-tests` |
| 单元、集成、doc 或编译期测试 | `write-tests` |
| 一般第三方 SDK | `kx-sdk` |
| Google SDK | `google-sdk` |
| AIGC SDK | `kx-sdk-aigc` |
| KX 工程设计、文档、提交、PR | 对应 `kx-design`、`prose`、`commit`、`pr` |
| UI、品牌与视觉设计 | `design` |

跨层功能按 `write-entity -> write-svc -> write-ctl` 顺序落地；不要用一个 skill 同时展开三层细节。

## 源码回溯

- `#[derive(Sea)]` 生成行为：`derives/codegen/src/table/sea/`
- SeaORM 公共封装：`crates/sea-orm/`、`core/sea-common/`
- HTTP 路由与安全元数据：`crates/axum/`
- 当前业务实践：`bizs/*/src/{entity,svc,ctl,dto,install.rs,router.rs}`

## 常见错误 vs 正确做法

```text
❌ 在入口 skill 中重复展开 entity、svc、ctl 的完整实现
❌ 把业务 crate 默认放进 crates/，或把同域 entity 强制拆到 ents/
✅ 先定位职责与目录，再交给对应专用 skill
✅ 跨层需求按 entity -> svc -> ctl 顺序处理
```

## 输出模板

```text
任务层次
推荐目录
建议 skill
第一步
```

## 完整示例

**Input**

```text
资产扣减接口该从 entity、svc 还是 ctl 开始？
```

**Output direction**

- Schema 不变时先用 `write-svc` 固定扣减事务和幂等。
- 再用 `write-ctl` 暴露薄 handler。
- 只有新增字段、索引或迁移时才先使用 `write-entity`。
