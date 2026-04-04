---
name: kx-biz-app
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-app` 这个应用端聚合封装包，统一聚合 app 端登录、用户、资源、订单、礼物、资产支付模板等路由与安装流程。

  触发场景：
  - 在业务项目里接入统一 app 端路由
  - 需要复用 `AppRouter::apis()`
  - 需要执行 app 端聚合安装流程 `AppInstall::install()`
  - 需要判断 app 端需求该落聚合层还是 auth/res/asset/gift 子 crate

  触发词：kx-biz-app、AppRouter、AppInstall、应用端聚合、app router、登录、订单、用户、pay_tmp
---

# kx-biz-app

`kx-biz-app` 是当前仓库里专门面向 `kx-biz-app` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-app` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 接应用端统一路由
- 运行 app 端安装流程
- 扩展 app 聚合层

### 不适用

- 资源内容内部实现
- auth 内部实现
- 后台管理聚合

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-app`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-app` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-app = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: AppRouter::apis()
- Install: AppInstall::install()
```

## 回答时优先强调的事实

- 这是 app 端聚合 crate，不是单一业务实现 crate。
- 当前统一聚合 auth、user、res、order、gift、asset/pay_tmp。
- 安装流程会联动 asset、res、mktg、gift。

## 最常用的落地套路

```text
- 优先把它看成 app 端网关层。
- 聚合层负责 nest 现有子路由，不应复制子业务实现。
- 如果只是要加 app 端一条聚合路由，先判断该路由是否已在子 crate 中存在。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把具体 res/auth/asset 逻辑塞到 app 聚合层。
❌ 自己在项目里重复挂一堆 app 子路由，而不复用 `AppRouter`。
❌ 把后台管理入口和 app 端聚合混在一起。
```

### 正确做法

```text
✅ 优先复用 `AppRouter` 与 `AppInstall`。
✅ 聚合层只做 app 端路由与安装编排。
✅ 具体子域问题 handoff 到对应 crate。
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
我想在一个 app 项目里统一接登录、用户、资源、订单和礼物接口，不想每个模块自己挂，应该用什么？
```

**Output direction**

```text
应命中 kx-biz-app，并指向 `AppRouter::apis()`。
```
