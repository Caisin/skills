# kx-biz-adm Module Map

这是 `kx-biz-adm` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `kx-biz-adm/src/install.rs`
  - 统一调用 Base/Auth/Param/Storage/Res/Asset/Mktg/Gift 的安装或迁移入口
- `kx-biz-adm/src/router.rs`
  - 统一聚合后台基础路由、业务路由与 app 端资源路由
- `kx-biz-adm/src/ctl/oplog.rs`
  - 管理端操作日志接口
- `kx-biz-adm/src/dto/mod.rs`
  - 聚合层 DTO 入口

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 要统一接后台路由 | `router.rs` + `AdmRouter::apis()` |
| 只想接基础后台能力 | `AdmRouter::basic_apis()` |
| 要跑管理端整体安装 | `install.rs` + `AdmInstall::migrate()` |
| 问题落到 auth/param/storage/res 具体实现 | handoff 到对应 crate skill |

## 回答时优先强调的事实

```text
- 这是管理端聚合 crate，不是单一业务子域实现 crate。
- 核心价值是统一挂载子业务路由与统一安装顺序。
- 具体业务逻辑应继续下钻到对应子 crate skill。
```

## 常见错误

```text
❌ 在业务项目里重复手工 nest 多个后台子模块，而不复用 `AdmRouter`。
❌ 把具体业务逻辑塞进聚合层，而不是放回子 crate。
❌ 安装时漏掉子模块 install/migrate 顺序。
```

## 正确做法

```text
✅ 优先复用 `AdmRouter` 与 `AdmInstall`。
✅ 聚合层只做路由与安装编排，业务实现继续下沉。
✅ 遇到子域问题时直接 handoff 到对应 crate skill。
```
