# sdk-mgr Module Map

这是 `sdk_mgr` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `sdk_mgr/src/lib.rs`
  - feature 开关与导出入口
- `sdk_mgr/src/dt_sdk_mgr.rs`
  - 钉钉 SDK 获取、默认 SDK 获取与缓存
- `sdk_mgr/src/wxapp.rs`
  - 微信小程序 SDK 获取、配置获取与消息加解密初始化

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 要拿钉钉 SDK | `DtSdkMgr::get()` / `DtSdkMgr::def_sdk()` |
| 要拿微信小程序 SDK | `WxSdkMgr::get()` / `WxSdkMgr::get_cfg()` |
| 问题落在 SDK 协议实现 | handoff 到 kx-sdk 或对应 provider crate |

## 回答时优先强调的事实

```text
- 当前 crate 是轻量 manager 层，不提供 HTTP 路由。
- 钉钉与微信小程序能力都从参数库配置表读取。
- 实例使用 `SwapGlobalMap` 做进程内缓存。
```

## 常见错误

```text
❌ 把 sdk_mgr 当成 HTTP 接口包。
❌ 绕过 manager 层在业务代码里重复 new SDK。
❌ 忽略 feature 开关和参数库配置来源。
```

## 正确做法

```text
✅ 优先复用 `DtSdkMgr` / `WxSdkMgr`。
✅ 回答时强调依赖 `kx-biz-param` 中的配置表。
✅ 协议实现问题 handoff 到对应 SDK skill。
```
