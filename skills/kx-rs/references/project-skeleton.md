# Project Skeleton

用于“新建实践层项目”或“新建实践层模块”的场景。

## 适用场景

- 新建下游业务 workspace
- 新增一个业务模块，需要同时落 `ents/`、`bizs/`、`bins/`
- 回答“这个功能应该先建哪个 crate、先写哪一层”

> 注意：`bins/`、`bizs/`、`ents/` 是**下游业务仓库约定**，不是当前核心框架仓库的既有目录事实。

## 推荐目录模板

```text
<workspace>/
├── Cargo.toml
├── build.rs                  # 可选，若根应用生成 openapi
├── bins/
│   └── app/
│       ├── Cargo.toml
│       ├── cfg.toml
│       └── src/
│           ├── main.rs
│           ├── lib.rs
│           ├── router.rs
│           └── install.rs
├── bizs/
│   └── xxx/
│       ├── Cargo.toml
│       └── src/
│           ├── lib.rs
│           ├── install.rs
│           ├── router.rs
│           ├── ctl/
│           ├── svc/
│           └── dto/
└── ents/
    └── xxx/
        ├── Cargo.toml
        └── src/
            ├── lib.rs
            └── entity/
```

## 最小搭建顺序

1. 先建 `ents/<ds>`，放实体、迁移、索引
2. 再建 `bizs/<biz>`，放 `svc/ctl/router/install/dto`
3. 再建 `bins/<app>`，负责装配和运行入口
4. 最后接 `build.rs` / `openapi-scan` / `cfg.toml`

## 依赖方向

```text
bins/* -> bizs/* -> ents/* -> kx
```

不要反向依赖：

- `ents/*` 不能依赖 `bizs/*`
- `bizs/*` 不应依赖 `bins/*`

## 常见错误

```text
❌ 把实体、业务、应用入口混在一个 crate
❌ 让 bins/* 直接承载业务逻辑
❌ 新项目一开始就把所有依赖都堆到 bins/*
❌ 把下游业务目录描述成当前核心框架仓库事实
```

## 正确做法

```text
✅ ents/* 只负责实体/迁移/索引
✅ bizs/* 负责 svc/ctl/router/install/dto
✅ bins/* 只负责装配、配置与运行入口
✅ 回答时明确“这是下游业务仓库约定”
```

## 完整示例

### 用户问题

```text
我要新建一个 practice 层项目，包含 bins bizs ents，先怎么搭？
```

### 回答方向

```text
- 先说明这属于下游业务仓库约定，不是当前核心框架仓库既有结构。
- 推荐先建 ents/<ds>，再建 bizs/<biz>，最后接 bins/<app>。
- 再补 build.rs / openapi-scan / cfg.toml。
- 最后确认依赖方向保持 bins -> bizs -> ents。
```
