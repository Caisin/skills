---
name: kx-sdk
description: |
  Use when 开发 `sdks/<provider>` 第三方 SDK、DTO、能力 trait、认证和公共请求封装。
  触发词：SDK、第三方接入、provider、token、cache、DTO、trait、reqwest、sdks
---

# kx-sdk

## Reference Selection

普通 provider 模式、错误与测试见 `references/patterns.md`。

## 落点

- 第三方协议、认证、DTO 和 API trait：`sdks/<provider>`。
- 与 provider 无关的框架能力：`crates/`。
- 多 SDK 运行时选择与凭证绑定：业务 crate 或 `bizs/sdk-mgr`。
- Google 与 AIGC 分别交给 `google-sdk`、`kx-sdk-aigc`。

## 核心规则

1. 一个 trait 表达一组清晰 API；DTO 紧邻能力模块，公共 client/auth/response 解包下沉复用。
2. 优先 `fn ... -> impl Future + Send`，除非对象安全或现有接口要求 `async_trait`。
3. URL、method、query/header/body 和响应 envelope 必须对照官方文档；不猜字段和错误码。
4. token 缓存键包含租户/应用/环境，刷新并发需要 single-flight 或锁。
5. 日志和错误不得泄露 token、密钥和完整敏感响应；提供稳定错误上下文。
6. 不在 SDK 内混入业务数据库、权限或 UI 逻辑。

## 验证

DTO 序列化、URL/请求构造和错误解包用离线测试；真实 API 测试必须显式 ignore 并说明凭据与网络前置。
