---
name: kx-sdk-aigc
description: |
  Use when 任务明确落在 kx 仓库的 sdks/aigc，包括 AigcAuth、AigcSdk、平台级单 API trait、streaming 与同协议原始透传 proxy。

  触发场景：
  - 修改 src/sdk、src/auth、src/api/<platform>/{non_stream,stream}/
  - 新增或调整 OpenAI / Gemini / Anthropic / DeepSeek / Vertex / Ollama provider 能力
  - 调整 AigcStream(meta + raw)、SSE decode、proxy/observe、protocol + model 路由
  - 需要补 request_id / usage / attempt_no / provider_hint 等链路字段

  触发词：AigcAuth、AigcSdk、OpenAI、Gemini、Anthropic、DeepSeek、Vertex、Ollama、stream、SSE、proxy、observe、usage、request_id
---

# kx-sdk-aigc

`kx-sdk-aigc` 是 `sdks/aigc` 的专用 skill。
它只负责这个 crate 的认证抽象、平台级 API trait、trait 邻近 DTO、streaming 与第一阶段 proxy 子系统，不覆盖其它 `sdks/` crate。

如果 `sdks/aigc` 的结构、约定或测试布局变化了，必须同步更新本 skill、`kx-entry`、`kx-sdk` 和 `AGENTS.md`。

## 适用边界

### 适用

- `AigcAuth`、`AigcSdk`、`BaseAigcSdk` 改动
- `src/api/<platform>/{non_stream,stream}/<single-http-api>.rs` 改动
- `OpenAiSdk`、`GeminiSdk`、`AnthropicSdk`、`DeepSeekSdk`、`VertexSdk`、`OllamaSdk` 改动
- `src/streaming/` 下的 SSE decode / 事件映射改动
- `src/proxy/` 下的路由、rewrite、usage/request-id 抽取、熔断与可观测性改动

### 不适用

- 纯 Rust 编译器 / 所有权 / 生命周期 / Send / Sync 问题
  - 交给 `rust-router`
- 还在讨论是否扩 scope 或总体 SDK 设计
  - 先交给 `brainstorming` 或 `writing-plans`
- 其它 `sdks/<provider>` crate，而不是 `sdks/aigc`
  - 交给 `kx-sdk`

## Reference Selection

按任务类型优先读取：

- 平台级单 API trait / DTO
  - 读 `references/patterns.md`
- streaming / SSE decode / AigcStream
  - 先读 `references/patterns.md`，再定位 `src/streaming/`
- proxy / observe / 链路字段
  - 先读 `references/patterns.md`，再定位 `src/proxy/`

## 快速定位表

| 需求 | 优先目录 / 文件 | 先确认什么 |
| --- | --- | --- |
| 认证与 SDK 宿主 | `src/auth/`、`src/sdk/` | 是否应落 `AigcAuth + AigcSdk` |
| 平台非流式 API | `src/api/<platform>/non_stream/` | 是否一个 HTTP API 一个 trait 文件 |
| 平台流式 API | `src/api/<platform>/stream/`、`src/streaming/` | 发送层是否仍返回原始 `AigcStream` |
| proxy 路由 / request 重写 | `src/proxy/types.rs`、`src/proxy/runtime.rs` | 是否仍保持同协议原始透传 |
| 观测与链路字段 | `src/proxy/observe/` | 事件、builder、observer 是否按职责分层 |

## 推荐实现模板

### 1. 平台级单 API trait 模板

优先保持“单 HTTP API 一个 trait 文件，DTO 与 trait 邻近”的结构。
下面是当前仓库已存在的真实模式：

```rust
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct OpenAiChatCompletionsReq {
    pub model: String,
    #[serde(default)]
    pub messages: Vec<OpenAiChatMessage>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub temperature: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub stream: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct OpenAiChatMessage {
    pub role: String,
    pub content: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct OpenAiChatCompletionsResp {
    pub id: Option<String>,
    pub model: Option<String>,
}

pub trait OpenAiChatCompletionsApi: AigcSdkExt {
    fn chat_completions(
        &self,
        req: &OpenAiChatCompletionsReq,
    ) -> impl std::future::Future<Output = anyhow::Result<OpenAiChatCompletionsResp>> + Send {
        self.post_json_ret("chat/completions", req)
    }
}

impl<A> OpenAiChatCompletionsApi for OpenAiSdk<A> where Self: AigcSdkExt {}
impl<A> OpenAiChatCompletionsApi for OllamaSdk<A> where Self: AigcSdkExt {}
```

### 2. proxy / observe 检查清单

改 proxy 时，默认先检查这几条：

1. 仍然是**同协议原始透传**，不要做跨协议翻译
2. `ProxyHttpRequest` 是否保留 `protocol + model`
3. provider 差异是否继续收敛在 `AigcSdk` hook 上
4. proxy 是否继续复用 `before_send()` 处理鉴权与固定协议头
5. `ProxyEvent` 是否保持 `RequestStart / ResponseFinish / Usage / UsageSummary / Breaker / StreamFrame / StreamFinish`
6. 链路字段是否优先补齐 `trace_id / provider_key / canonical_model / upstream_model`，按需带 `attempt_no / provider_hint / request_id`

## 核心规则

1. **基础能力先看 `AigcAuth + AigcSdk`**
   - 不要把 provider 特例上推到通用层
2. **API 目录按平台 + 单 HTTP API 拆分**
   - 不回退到统一大 trait，也不回到 `src/provider/*.rs` DTO 聚合层
3. **stream 发送层保持原始 `AigcStream`**
   - SSE decode / provider mapper 放到 `src/streaming/`
4. **proxy 第一阶段只做同协议原始透传**
   - 不做统一 DTO 网关，不做跨协议翻译
5. **observer 默认 raw-only**
   - 请求体、响应体、stream frame 不在 SDK 侧提前生成 preview / summary / truncated
6. **最小验证优先**
   - 默认先跑 `cargo test -p kx-sdk-aigc`

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把多个平台 DTO 重新集中回 src/provider/*.rs
❌ 在 proxy 层手写 Bearer / x-api-key，而不是复用 before_send()
❌ 把 stream 发送层直接耦合成 provider 事件对象，而不是原始 AigcStream
❌ 在 proxy 第一阶段就做跨协议翻译或统一 DTO 网关
❌ 观测事件里提前塞 preview/summary/truncated，导致 SDK 侧承担展示职责
```

### 正确做法

```text
✅ 一个 HTTP API 一个 trait 文件，DTO 紧邻 trait
✅ provider 差异尽量收敛到 AigcSdk hook
✅ streaming 保持 meta + raw，再在后续步骤 decode
✅ proxy 继续只做同协议原始透传
✅ observer 事件默认保留原始载荷，脱敏/截断/摘要交给订阅端
```

## 输出模板

默认按这个结构输出：

```text
问题归类
- auth/sdk、平台 API、streaming，还是 proxy/observe

改动落点
- 优先目录与文件

关键约定
- 当前任务必须遵守的 3~6 条规则

验证方式
- 最小必要 cargo 命令

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
我要给 OpenAI 风格 provider 新增一个非流式 API，并保持 proxy 后续可复用，应该怎么组织？
```

**Output direction**

```text
- 先在 src/api/openai/non_stream/ 下按“单 HTTP API 一个 trait 文件”落位。
- 请求/响应 DTO 直接写在该 trait 文件附近，不回退到 provider DTO 聚合层。
- trait 默认实现优先复用 AigcSdkExt::get_ret/post_json_ret。
- 如果后续 proxy 也需要模型提取、request-id 或 usage 抽取，再看是否补 AigcSdk hook，而不是把逻辑散写到 proxy/runtime。
- 最后先跑 cargo test -p kx-sdk-aigc。
```
