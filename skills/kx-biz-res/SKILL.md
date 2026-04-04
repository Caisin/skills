---
name: kx-biz-res
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-res` 这个资源内容封装包，统一提供资源内容、页面配置、短链、小说/文档、应用端资源接口与通知接口。

  触发场景：
  - 在业务项目里接入统一资源内容路由
  - 需要复用 `ResRouter::apis()` / `app_apis()` / `notify_apis()`
  - 需要执行资源库初始化 `ResInstall::install()`
  - 需要扩展资源、分类、标签、页面配置、短链、文档、通知等子域

  触发词：kx-biz-res、ResRouter、ResInstall、资源内容、页面配置、短链、小说、文档、notify、wx msg
---

# kx-biz-res

`kx-biz-res` 是当前仓库里专门面向 `kx-biz-res` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-res` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 接管理端资源路由
- 接应用端资源/文档/配置路由
- 扩展资源内容子域

### 不适用

- 文件存储底层逻辑
- 统一 app 聚合网关
- auth/param 业务本体

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-res`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-res` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-res = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: ResRouter::apis(), ResRouter::app_apis(), ResRouter::notify_apis()
- Install: ResInstall::install()
```

## 回答时优先强调的事实

- 这个 crate 同时有 adm / app / notify 三类路由入口。
- 管理端除了资源本体，还包含 page cfg、short link、sync type 等子域。
- 资源业务依赖 storage、asset、sdk_mgr 等其他 crate。

## 最常用的落地套路

```text
- 先判断需求属于 adm、app 还是 notify，再继续细分到 res/category/tag/item/page/sl/doc。
- 如果只是要统一挂路由，优先复用 ResRouter，不要在业务项目里散着 merge。
- 存储 URL、文件读取等问题应回到 storage crate。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把管理端、应用端、通知接口混成一个入口说明。
❌ 把存储上传或文件 URL 逻辑说成 res 自己实现。
❌ 忽略页面配置与资源内容是两个不同子域。
```

### 正确做法

```text
✅ 按 adm/app/notify 三类入口回答。
✅ 先复用 `ResRouter` 与 `ResInstall`，再下钻到具体子域。
✅ 文件存储问题 handoff 到 kx-biz-storage。
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
我想在一个项目里同时接后台资源管理接口和 app 端资源/文档接口，有没有统一 crate 可以直接挂？
```

**Output direction**

```text
应命中 kx-biz-res，并说明可分别复用 `ResRouter::apis()` 与 `ResRouter::app_apis()`。
```
