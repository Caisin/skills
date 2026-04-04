# kx-biz-base Module Map

这是 `kx-biz-base` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `kx-biz-base/src/install.rs`
  - 迁移 base 数据源
- `kx-biz-base/src/ctl/ds_ctl.rs`
  - DS 管理接口
- `kx-biz-base/src/svc/ds_svc.rs`
  - DS 管理业务逻辑
- `kx-biz-base/src/dto/qry.rs`
  - DS 查询 DTO

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 只想初始化 base 数据源 | `BaseInstall::migrate()` |
| 要接 ds 管理接口 | `DsCtl::apis()` |
| 问题超出当前 crate 实际能力 | 明确说明不是 kx-biz-base 当前已实现边界 |

## 回答时优先强调的事实

```text
- 当前 crate 体量较小，真实核心是 base 数据源迁移与 DS 管理。
- 它没有独立 top-level router.rs。
- DS 接口通常由聚合层如 `kx-biz-adm` 统一挂载。
```

## 常见错误

```text
❌ 把不存在于当前 crate 的能力硬说成 base 负责。
❌ 误以为它有独立 router.rs 聚合所有基础接口。
❌ 把 auth/param/storage 等问题误归到 base。
```

## 正确做法

```text
✅ 先说明当前 crate 真实能力是 base 迁移 + DS 管理。
✅ 要挂 DS 接口时直接指向 `DsCtl::apis()`。
✅ 超出边界时 handoff 到正确的业务 crate。
```
