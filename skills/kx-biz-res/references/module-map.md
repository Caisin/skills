# kx-biz-res Module Map

这是 `kx-biz-res` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `kx-biz-res/src/install.rs`
  - 初始化 res 数据源
- `kx-biz-res/src/router.rs`
  - 统一聚合 adm/app/notify 路由
- `kx-biz-res/src/ctl/adm/*`
  - 管理端资源、分类、标签、页面配置、短链等接口
- `kx-biz-res/src/ctl/app/*`
  - 应用端资源、配置、日志、文档接口
- `kx-biz-res/src/ctl/notify/*`
  - 通知接口
- `kx-biz-res/src/svc/*`
  - 资源、页面、短链、解锁、打分、点赞等业务逻辑

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 接管理端资源接口 | `ResRouter::apis()` |
| 接 app 端资源接口 | `ResRouter::app_apis()` |
| 接通知接口 | `ResRouter::notify_apis()` |
| 初始化资源库 | `ResInstall::install()` |

## 回答时优先强调的事实

```text
- 这个 crate 同时有 adm / app / notify 三类路由入口。
- 管理端除了资源本体，还包含 page cfg、short link、sync type 等子域。
- 资源业务依赖 storage、asset、sdk_mgr 等其他 crate。
```

## 常见错误

```text
❌ 把管理端、应用端、通知接口混成一个入口说明。
❌ 把存储上传或文件 URL 逻辑说成 res 自己实现。
❌ 忽略页面配置与资源内容是两个不同子域。
```

## 正确做法

```text
✅ 按 adm/app/notify 三类入口回答。
✅ 先复用 `ResRouter` 与 `ResInstall`，再下钻到具体子域。
✅ 文件存储问题 handoff 到 kx-biz-storage。
```
