---
name: kx-biz-adm
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-adm` 这个管理端聚合封装包，统一聚合管理端路由与安装流程，复用 auth / param / storage / res / asset / mktg / gift 等子业务能力。

  触发场景：
  - 在业务项目里接入统一管理端路由，而不是分别手工挂多套子模块
  - 需要复用 `AdmRouter::apis()` / `AdmRouter::basic_apis()` / `AdmRouter::app_apis()`
  - 需要执行管理端聚合安装流程 `AdmInstall::migrate()`
  - 需要扩展管理端聚合层而不是下钻到具体子业务 crate

  触发词：kx-biz-adm、管理端聚合、adm router、AdmRouter、AdmInstall、basic_apis、app_apis、后台管理路由
---

# kx-biz-adm

`kx-biz-adm` 是当前仓库里专门面向 `kx-biz-adm` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-adm` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 接入统一后台路由
- 扩展后台聚合层 install/router
- 判断某个后台接口应该落聚合层还是子模块

### 不适用

- 具体 auth/param/storage/res/asset 业务实现细节
- 通用 kx-axum handler 模板
- 实体、迁移、derive(Sea) 模板

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-adm`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-adm` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-adm = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: AdmRouter::apis(), AdmRouter::basic_apis(), AdmRouter::app_apis()
- Install: AdmInstall::migrate()
```

## 回答时优先强调的事实

- 这是管理端聚合 crate，不是单一业务子域实现 crate。
- 核心价值是统一挂载子业务路由与统一安装顺序。
- 具体业务逻辑应继续下钻到对应子 crate skill。

## 最常用的落地套路

```text
- 优先把它当成后台网关层，而不是功能实现层。
- 路由聚合优先复用现成子 crate router，不要在聚合层复制业务 handler。
- 新增后台能力时先判断是“新挂一个子路由”还是“扩展现有子 crate”。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 在业务项目里重复手工 nest 多个后台子模块，而不复用 `AdmRouter`。
❌ 把具体业务逻辑塞进聚合层，而不是放回子 crate。
❌ 安装时漏掉子模块 install/migrate 顺序。
```

### 正确做法

```text
✅ 优先复用 `AdmRouter` 与 `AdmInstall`。
✅ 聚合层只做路由与安装编排，业务实现继续下沉。
✅ 遇到子域问题时直接 handoff 到对应 crate skill。
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
我想在一个管理端项目里统一挂 auth/param/storage/res 等后台接口，最好不要自己一条条 nest，应该直接怎么接？
```

**Output direction**

```text
应命中 kx-biz-adm，并优先建议复用 `AdmRouter::apis()` 或 `AdmRouter::basic_apis()`，把它定位成管理端聚合封装包。
```
