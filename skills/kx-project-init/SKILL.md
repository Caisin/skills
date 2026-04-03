---
name: kx-project-init
description: |
  Use when 任务明确是创建一个新的 kx-rs 框架项目，需要从 `cargo new <project-name>` 开始，初始化项目结构、kx-rs 必要依赖、默认 `AGENTS.md`、`.agents` 子模块、可跑通的数据库 CRUD 骨架与 `README.md`。

  触发场景：
  - 需要从零创建一个新的 kx-rs 项目模板
  - 需要根据项目规模在“简化模板”和“大型项目模板”之间做选择
  - 需要为新项目初始化 `AGENTS.md`、`docs/long-term-memory.md` 与 `.agents` 子模块
  - 需要给新项目补第一版数据库模块、增删改查模板与运行说明

  触发词：创建 kx-rs 项目、初始化项目、project init、cargo new、项目模板、AGENTS 模板、README 模板、.agents 子模块、数据库模块、CRUD 模板
---

# kx-project-init

`kx-project-init` 是“创建新的 kx-rs 框架项目模板”的专用 skill。
它不只是讲目录结构，而是负责给用户输出一套**可直接落地执行的新项目初始化方案**：从 `cargo new`、依赖补齐、`AGENTS.md` 初始化、`.agents` 子模块接入、数据库模块与 CRUD 骨架，到 `README.md` 的运行文档。

## 适用边界

### 适用

- 从零创建新的 kx-rs 项目
- 设计并初始化项目模板
- 在“单工程简化模板”和“大型项目模板”之间选型
- 初始化 `AGENTS.md`、`docs/long-term-memory.md`、`.agents` 子模块
- 生成第一版数据库模块、`install.rs` 与 CRUD 骨架
- 生成 `README.md` 的使用与运行文档

### 不适用

- 已有项目里补具体 web handler / router / install
  - 交给 `kx-axum-web`
- 已有项目里补实体、迁移、CRUD、事务示例
  - 交给 `kx-sea-orm`
- 已有项目里只讨论 practice 层目录落点
  - 交给 `kx-rs`
- 纯 SDK 接入问题
  - 交给 `kx-sdk` / `kx-sdk-aigc`

## Reference Selection

按任务类型优先读取：

- 项目模板总览
  - 读 `references/patterns.md`
- 默认 `AGENTS.md` 初始化模板
  - 读 `references/agents-template.md`
- 默认 `README.md` 初始化模板
  - 读 `references/readme-template.md`
- 想继续细化 web 层模板
  - 对照 `../kx-axum-web/references/patterns.md`
- 想继续细化实体 / 迁移 / CRUD 模板
  - 对照 `../kx-sea-orm/references/patterns.md`

## 核心规则

1. **必须从 `cargo new <project-name>` 起手**
   - 项目初始化默认先给出 `cargo new` 命令，而不是只停留在目录草图。
2. **必须补 kx-rs 运行所需的必要依赖**
   - 至少要说明如何接入 `kx-axum`、`kx-sea-orm`、`kx-tools`、`anyhow`、`tokio`、`clap` 等基础依赖。
3. **默认初始化 `AGENTS.md` 与 `docs/long-term-memory.md`**
   - `AGENTS.md` 要带通用协作规范，并预留“项目专有规范”空白区。
   - `docs/long-term-memory.md` 要一起创建。
4. **默认初始化 `.agents` 子模块**
   - 使用 `https://github.com/Caisin/skills.git` 作为共享 skill 仓库。
5. **根据项目规模给两套模板**
   - 简化模板：单工程 / 单 crate，适合小项目。
   - 大型模板：`bins/* + bizs/* + ents/*` 多 crate，适合大项目。
6. **初始化时必须给一个可跑通的数据库模块、`install.rs` 与 CRUD 骨架**
   - 至少要有：一个实体模型、一个查询/保存接口入口、一个安装入口和一个启动入口。
7. **bin 模板必须包含 `SubCmd::Install`**
   - `main.rs` 里的 `SubCmd` 至少包含 `Server` 与 `Install`。
   - `Install` 分支要显式调用 `install.rs` 里的初始化/迁移入口。
8. **初始化时必须给 `README.md` 运行说明**
   - 至少说明：如何配置、如何运行、如何迁移、如何启动服务。
8. **只给最小可运行模板，不在第一步塞满业务代码**
   - 保证项目能启动、能扩展、规范清晰即可。

## 推荐回答顺序

1. 先判断用户要的是“简化模板”还是“大型项目模板”
2. 再给 `cargo new` 起手命令
3. 再给目录结构与必要依赖
4. 再给 `AGENTS.md`、`docs/long-term-memory.md`、`.agents` 初始化内容
5. 再给数据库模块、`install.rs` 与 CRUD 骨架
6. 最后给 `README.md` 运行说明模板

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只画目录结构，不给 cargo new 与依赖初始化步骤
❌ 不初始化 AGENTS.md / docs/long-term-memory.md / .agents
❌ 没有 `install.rs` 或 `SubCmd::Install`，导致数据库初始化入口缺失
❌ 没有 README.md，导致新项目跑不起来或不知道怎么启动
❌ 不区分小项目和大项目，统一上重型多 crate 模板
❌ 初始化 skill 里直接展开大量具体业务代码，而不是给可跑通骨架
```

### 正确做法

```text
✅ 从 cargo new 开始，给完整初始化顺序
✅ 同步初始化 AGENTS.md、docs/long-term-memory.md、.agents
✅ 默认先给简化模板，大型工程再拆多 crate
✅ 至少补一个数据库模块、`install.rs` 和 CRUD 骨架，让项目可以完整跑起来
✅ `main.rs` 里要同时支持 `Server` / `Install`
✅ README.md 要写清楚配置、迁移与启动方式
```

## 输出模板

```text
问题归类
- 简化模板 / 大型项目模板

初始化命令
- cargo new
- .agents 子模块命令
- 必要依赖补充

目录结构
- 项目骨架

初始化文件
- AGENTS.md
- docs/long-term-memory.md
- README.md

最小可运行代码
- main.rs
- router.rs / install.rs
- main.rs 的 `SubCmd::Install`
- 数据库模块与 CRUD 骨架

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
帮我创建一个新的 kx-rs 项目模板，要能直接跑起来，包含 cargo new、AGENTS.md、.agents 子模块、数据库模块、CRUD 和 README。
```

**Output direction**

```text
- 先判断默认使用简化模板。
- 从 cargo new 开始给初始化命令。
- 再给项目结构、依赖、AGENTS / long-term-memory / .agents 初始化。
- 最后给可跑通的数据库模块、install.rs、`SubCmd::Install`、CRUD 骨架与 README 运行说明。
```
