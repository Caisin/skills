---
name: kx-project-init
description: |
  Use when 从 `cargo new` 创建新的 kx-rs 项目并补齐目录、依赖、文档和可运行 CRUD 骨架。
  触发词：创建 kx-rs 项目、初始化项目、cargo new、项目模板、CRUD 骨架
---

# kx-project-init

## Reference Selection

- 目录与依赖模板：`references/patterns.md`
- README：`references/readme-template.md`
- AGENTS：`references/agents-template.md`

## 核心流程

1. 从 `cargo new <name>` 开始，确认包名、binary/library、数据库和规模。
2. 小项目保留最少层次；复杂项目再拆 `entity/svc/ctl/dto/tasks`，不预建空目录。
3. 通过 workspace/registry 方式加入 kx-rs 依赖，固定 Rust 2024，不复制框架源码。
4. 初始化 `AGENTS.md`、`docs/long-term-memory.md` 和 `.agents` 子模块。
5. 首个持表功能按 `write-entity -> write-svc -> write-ctl` 建立最小 CRUD、安装入口和测试。
6. README 只写真实运行前置、配置、安装、启动和验证命令，不放密钥。

## 约束

- 业务 entity 默认与同域 service/router/install 共置；共享发布实体才放 `ents/`。
- 异步批量操作从一开始接入 `kx-biz-task`，不使用裸 `tokio::spawn`。
- 初始化完成前必须能构建、运行目标测试，并执行一次 install/serve 冒烟检查。
