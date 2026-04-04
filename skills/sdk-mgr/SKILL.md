---
name: sdk-mgr
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `sdk_mgr` 这个SDK 管理封装包，基于参数库配置统一管理钉钉与微信小程序 SDK 实例，提供全局缓存与按 app_id 获取能力。

  触发场景：
  - 在业务项目里按配置直接获取钉钉或微信小程序 SDK 客户端
  - 需要复用 `DtSdkMgr` / `WxSdkMgr`
  - 需要理解 feature `dingtalk` / `wxapp` 的启停边界
  - 需要排查 SDK 为什么从参数库读取配置或为什么命中全局缓存

  触发词：sdk_mgr、sdk-mgr、DtSdkMgr、WxSdkMgr、微信小程序 sdk、钉钉 sdk、app 配置缓存
---

# sdk-mgr

`sdk-mgr` 是当前仓库里专门面向 `sdk_mgr` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `sdk_mgr` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 按 app_id 获取 SDK
- 理解 param 配置到 SDK 实例的映射
- 扩展 SDK 管理封装

### 不适用

- 第三方 SDK HTTP/协议实现细节
- 业务路由/ctl 层设计
- 参数库实体模板

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `sdk_mgr`
  - 先读 `references/patterns.md`
- 想知道 `sdk_mgr` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
sdk_mgr = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: 无统一 router，核心入口是 `DtSdkMgr` / `WxSdkMgr`
- Install: 无 install；依赖 `kx-biz-param` 中的配置表
```

## 回答时优先强调的事实

- 当前 crate 是轻量 manager 层，不提供 HTTP 路由。
- 钉钉与微信小程序能力都从参数库配置表读取。
- 实例使用 `SwapGlobalMap` 做进程内缓存。

## 最常用的落地套路

```text
- 先看是否已经能通过参数库配置直接拿到 SDK，不要手工重复初始化。
- feature 关闭时不要误以为对应 manager 一定存在。
- WxSdkMgr 会尝试初始化消息加解密 `Crypto`。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把 sdk_mgr 当成 HTTP 接口包。
❌ 绕过 manager 层在业务代码里重复 new SDK。
❌ 忽略 feature 开关和参数库配置来源。
```

### 正确做法

```text
✅ 优先复用 `DtSdkMgr` / `WxSdkMgr`。
✅ 回答时强调依赖 `kx-biz-param` 中的配置表。
✅ 协议实现问题 handoff 到对应 SDK skill。
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
我在业务代码里想按 app_id 直接拿到微信小程序 SDK，并自动复用缓存，应该用哪个 crate？
```

**Output direction**

```text
应命中 sdk-mgr，并指向 `WxSdkMgr::get()`。
```
