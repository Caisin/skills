# kx-biz-app Module Map

这是 `kx-biz-app` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `kx-biz-app/src/install.rs`
  - 统一安装 asset/res/mktg/gift
- `kx-biz-app/src/router.rs`
  - 统一聚合 app 登录、用户、资源、订单、礼物、资产支付模板路由
- `kx-biz-app/src/ctl/auth/*`
  - app 登录相关接口
- `kx-biz-app/src/ctl/user/*`
  - app 用户接口
- `kx-biz-app/src/ctl/asset/*`
  - 订单与支付模板接口

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 接统一 app 路由 | `AppRouter::apis()` |
| 初始化 app 端相关业务表 | `AppInstall::install()` |
| 问题落到 res/auth/asset/gift 具体实现 | handoff 到对应 crate skill |

## 回答时优先强调的事实

```text
- 这是 app 端聚合 crate，不是单一业务实现 crate。
- 当前统一聚合 auth、user、res、order、gift、asset/pay_tmp。
- 安装流程会联动 asset、res、mktg、gift。
```

## 常见错误

```text
❌ 把具体 res/auth/asset 逻辑塞到 app 聚合层。
❌ 自己在项目里重复挂一堆 app 子路由，而不复用 `AppRouter`。
❌ 把后台管理入口和 app 端聚合混在一起。
```

## 正确做法

```text
✅ 优先复用 `AppRouter` 与 `AppInstall`。
✅ 聚合层只做 app 端路由与安装编排。
✅ 具体子域问题 handoff 到对应 crate。
```
