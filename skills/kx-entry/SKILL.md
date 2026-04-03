---
name: kx-entry
description: |
  Use when 需要先判断 kx 仓库任务该落在哪一层、哪个目录，或该切到哪个后续 skill。

  触发场景：
  - 用户在问“这事该改哪里 / 放哪里 / 从哪开始”
  - 需要区分 core/crates/derives/sdks/tools 与 bins/bizs/ents
  - 需要判断应交给 kx-project-init、kx-rs、kx-sea-orm、kx-axum-web、kx-sdk、kx-sdk-aigc，还是继续仓库级分析

  触发词：放哪里、改哪里、从哪开始、哪个目录、哪个模块、哪个 skill、sdks 还是 crates、框架层、实践层
---

# kx-entry

`kx-entry` 是 `kx` 仓库的总入口 skill。
它不直接展开实现细节，而是先把任务分到**对的层、对的目录、对的后续 skill**。

## 核心职责

只做这四件事：

1. 给出简短项目上下文
2. 判断任务属于核心框架层还是实践层
3. 定位最可能的目录或模块
4. 路由到更合适的 skill，或在未命中时继续做仓库级分析

如果仓库目录、模块边界、框架约定或最佳实践更新了，必须同步更新本 skill 和相关仓库内 skill，不能只改 `AGENTS.md`。

## 快速判断表

| 用户意图 | 先判断什么 | 下一步 |
| --- | --- | --- |
| “这段代码该放哪” | 是框架层还是实践层 | 给目录 + 理由 |
| “该用哪个 skill” | 是否已有专用 skill 覆盖 | 明确 handoff |
| “sdks 还是 crates” | 是第三方接入还是通用基础抽象 | 默认优先 `sdks/` |
| “新 kx-rs 项目怎么创建” | 是否明确在做项目初始化/脚手架 | 切到 `kx-project-init` |
| “ents/bizs/bins 怎么组织” | 是否在讨论下游业务项目 | 切到 `kx-rs` |
| “SeaORM / derive(Sea) 示例怎么写” | 是否明确在要模型/迁移/CRUD/事务/多源/多表示例 | 切到 `kx-sea-orm` |
| “kx-axum web 层怎么写” | 是否明确在问 ctl/router/install、extractor、R/AxumErr | 切到 `kx-axum-web` |
| “AigcSdk / proxy / observe 怎么改” | 是否明确落在 `sdks/aigc` | 切到 `kx-sdk-aigc` |
| “trait bound / lifetime / Send” | 是否纯 Rust 语言问题 | 切到 `rust-router` |

## 仓库地图

### 当前仓库已核实存在的核心框架层目录

- `core/`: 核心共享抽象与公共模型
- `crates/`: 通用基础库与框架能力
- `derives/`: `#[derive(Sea)]` 等代码生成与宏实现
- `sdks/`: 第三方平台接入与 SDK 适配
- `tools/`: 框架辅助工具
- `kx/`: facade 与统一导出
- `docs/`: 设计文档、实施计划、规范说明

### 下游业务仓库约定（不是当前工作区事实）

以下目录常见于使用 `kx-rs` 的业务仓库，需要明确标注为“下游业务仓库约定”：

- `bins/`: 应用入口
- `bizs/`: 业务模块
- `ents/`: 业务实体与数据域

当前仓库虽然存在 `ents/`，但不要因此把整个仓库误判成实践层项目。

## 路由规则

按下面顺序判断：

### 1. 规划 / 方案类

出现“怎么拆 / 怎么设计 / 先出方案 / 先列计划 / 要不要重构”时，优先建议：

- `brainstorming`
- `writing-plans`

### 2. 纯 Rust 语言与编译问题

出现这些问题时，优先交给 `rust-router`：

- 编译错误
- trait bound
- 生命周期
- async / await
- Send / Sync
- 借用 / 所有权

### 3. bug / 回归 / 测试失败

优先交给 `systematic-debugging`。

### 4. 新项目初始化

当用户明确要创建新的 kx-rs 项目时，优先切到仓库内 `kx-project-init`：

- 初始化单工程 / 单 crate 项目
- 初始化多 crate 项目骨架
- 初始化 `AGENTS.md` 与 `docs/long-term-memory.md`
- 初始化 `.agents` 子模块

### 5. 实践层开发

当用户在问这些内容时，优先切到仓库内 `kx-rs`：

- `bins/`、`bizs/`、`ents/`
- 实体、控制器、服务、路由、DTO
- CRUD 落地
- openapi-scan 与业务控制器兼容

### 6. SeaORM / #[derive(Sea)] 示例专门问题

当用户明确要的是这些内容时，优先切到仓库内 `kx-sea-orm`：

- 模型定义示例
- 迁移 / `auto_migrate()` 示例
- `get/sel/qry/m/update_set` 示例
- `SeaTrans` 事务示例
- 多数据源示例
- 多表操作示例，且明确禁止使用 relation 做外键

### 7. `kx-axum` web 层问题

当用户明确要的是这些内容时，优先切到仓库内 `kx-axum-web`：

- `ctl/` handler 模板
- `router.rs` 的 `nest()` 聚合
- `install.rs` 模块安装入口
- `R<T>` / `AxumErr` / `QsQuery` / `Json` / `Path` 用法
- 基于 `*Qry` / `*ModifyModel` 的 page/list/save/get/del 接口
- 是否适合 `crud_api!` 的判断

### 8. 一般 `sdks/` 开发

当用户在问第三方平台接入、trait 组织、token/cache、请求 DTO、SDK 风格对齐时，优先切到仓库内 `kx-sdk`。

### 9. `sdks/aigc` 专门问题

出现这些内容时，优先切到仓库内 `kx-sdk-aigc`：

- `AigcAuth` / `AigcSdk`
- `src/api/<platform>/{non_stream,stream}/`
- `AigcStream(meta + raw)`
- 原始透传 proxy
- `protocol + model` 路由
- `proxy/observe`
- 链路字段，如 `attempt_no`、`provider_hint`、`request_id`

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 看到仓库里有 ents/，就把整个仓库判成实践层
❌ 用户只是问“该放哪里”，却直接开始写实现代码
❌ 把第三方平台接入默认塞到 crates/
❌ 明明已经命中 kx-sdk-aigc，还继续用通用 kx-sdk 含混处理
```

### 正确做法

```text
✅ 先说明当前仓库主语义是核心框架层
✅ 先判“任务属于哪一层”，再给目录与后续 skill
✅ 第三方接入默认优先看 sdks/，只有纯通用基础能力才考虑 crates/
✅ 命中更专门的 skill 时，明确 handoff，不在入口 skill 里展开实现手册
```

## 标准输出模板

默认使用这个结构：

```text
项目上下文
- 说明 kx 是核心框架层仓库，当前任务更像哪一层

模块定位
- 最可能的目录
- 为什么先看这里

建议 skill
- 命中的 skill 名称
- 为什么切过去

下一步
- 优先查看的 2~4 个目录或文件
- 一个具体起手动作
```

## 完整示例

**Input**

```text
这个支付接入应该放在 sdks 还是 crates？
```

**Output**

```text
项目上下文
- kx 当前是核心框架层仓库，这类问题属于第三方接入/适配层判断。
- 第三方平台接入默认优先看 sdks/，不是先放 crates/。

模块定位
- 优先看 sdks/。
- 因为支付接入本质是 provider 适配，不是纯通用基础抽象。

建议 skill
- 建议切到 kx-sdk。
- 这个 skill 更适合继续约束 trait、DTO、token/cache 与 SDK 风格。

下一步
- 先看 sdks/ 现有 provider crate 的组织方式。
- 再回看 sdks/core、sdks/wx-core 的公共能力抽象。
- 如果最终发现是多个 provider 共用的纯基础能力，再回头评估是否下沉到 crates/。
```
