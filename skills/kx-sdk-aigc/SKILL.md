---
name: kx-sdk-aigc
description: |
  Use when 修改 `sdks/aigc` 的认证、provider API、streaming、proxy、observe 与路由元数据。
  触发词：AigcAuth、AigcSdk、OpenAI、Gemini、Anthropic、stream、SSE、proxy、observe
---

# kx-sdk-aigc

## Reference Selection

目录、trait、stream 和 proxy 模式见 `references/patterns.md`。

## 落点

| 能力 | 位置 |
| --- | --- |
| client/auth/provider host | `src/sdk`、`src/auth` |
| 单个 HTTP API 与 DTO | `src/api/<platform>/{non_stream,stream}` |
| provider 差异 | `AigcSdk` hook |
| 原始代理与观测 | `proxy`、`observe` |

## 核心规则

1. 一个 HTTP API 一个 trait 文件，DTO 与 trait 邻近；公共发送统一复用 SDK hook。
2. 路由由 `protocol + model` 决定，provider hint 只能缩小候选，不绕过能力校验。
3. streaming 保留 `AigcStream { meta, raw }`；发送层不提前翻译为 provider 事件。
4. proxy 默认只做同协议原始透传；跨协议转换必须有独立设计与测试。
5. observe 默认保存 raw 与必要链路字段，不提前制造 preview/summary/truncated 派生语义。
6. request_id、usage、attempt_no、provider_hint 和错误分类贯穿非流式与流式路径。
7. 密钥只由 `AigcAuth` 提供，日志、代理响应和观测数据不得泄露凭据。

## 验证

覆盖请求序列化、SSE 分片/结束/错误、路由选择、原始透传和敏感字段脱敏；真实 provider 测试显式隔离。
