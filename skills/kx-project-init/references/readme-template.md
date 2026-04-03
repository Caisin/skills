# KX Project Init README Template

用于 `kx-project-init` 的默认 `README.md` 初始化模板。

## 推荐模板

```md
# <project-name>

## 项目简介

这里写项目简介。

## 技术栈

- Rust 2024
- kx-axum
- kx-sea-orm
- SeaORM

## 初始化

```bash
cargo build
```

## 配置

1. 编辑 `cfg.toml`
2. 配置数据库连接
3. 按需调整日志、JWT、安全配置

## 数据库初始化 / 迁移

```bash
cargo run -- install
```

## 运行

```bash
cargo run -- server
```

## 目录说明

- `src/ents/`：实体模型
- `src/ctl/`：控制器
- `src/svc/`：业务服务
- `src/router.rs`：路由聚合
- `AGENTS.md`：协作规范
- `docs/long-term-memory.md`：长期记忆文档
```

## 常见错误

```text
❌ README 只写一句话，没有 install / server 运行方法
❌ 不说明配置与迁移入口
```

## 正确做法

```text
✅ README 至少包含配置、install、server、目录说明
✅ 新项目模板默认就让使用者知道如何初始化数据库并启动
```
