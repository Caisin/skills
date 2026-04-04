---
name: kx-biz-base
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-base` 这个基础能力封装包，当前实际聚焦基础数据源与 DS 管理能力，提供基础安装入口以及 DS 查询/控制相关接口。

  触发场景：
  - 在业务项目里接入基础库迁移
  - 需要复用 `BaseInstall::migrate()`
  - 需要使用或扩展 DS 管理接口 `DsCtl::apis()` / `DsSvc`
  - 需要判断一个“基础能力”需求是否真的属于当前 crate

  触发词：kx-biz-base、base install、BaseInstall、DsCtl、DsSvc、ds 管理、数据源管理
---

# kx-biz-base

`kx-biz-base` 是当前仓库里专门面向 `kx-biz-base` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-base` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 运行 base 数据源迁移
- 使用或扩展 ds 管理接口
- 说明这个 crate 当前真实边界

### 不适用

- 通用后台聚合
- auth/param/storage 业务细节
- 不存在于当前 crate 的“泛基础能力”臆测

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-base`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-base` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-base = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: DsCtl::apis()（通常由聚合层挂载）
- Install: BaseInstall::migrate()
```

## 回答时优先强调的事实

- 当前 crate 体量较小，真实核心是 base 数据源迁移与 DS 管理。
- 它没有独立 top-level router.rs。
- DS 接口通常由聚合层如 `kx-biz-adm` 统一挂载。

## 最常用的落地套路

```text
- 回答时要尊重当前 crate 真实边界，不要把“基础能力”泛化成仓库里所有公共能力。
- 如果只是要在后台里挂 DS 接口，通常由聚合层去 nest `DsCtl::apis()`。
- base crate 当前更像轻量支撑模块而不是大而全平台层。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把不存在于当前 crate 的能力硬说成 base 负责。
❌ 误以为它有独立 router.rs 聚合所有基础接口。
❌ 把 auth/param/storage 等问题误归到 base。
```

### 正确做法

```text
✅ 先说明当前 crate 真实能力是 base 迁移 + DS 管理。
✅ 要挂 DS 接口时直接指向 `DsCtl::apis()`。
✅ 超出边界时 handoff 到正确的业务 crate。
```

## 输出模板

```text
问题归类
推荐落点
关键约定
实现顺序
验证方式
下一步
```

## 完整示例

**Input**

```text
我想先把 base 数据源跑起来，再接一个 DS 管理接口，当前最短入口是什么？
```

**Output direction**

```text
应命中 kx-biz-base，并指向 `BaseInstall::migrate()` 与 `DsCtl::apis()`。
```
