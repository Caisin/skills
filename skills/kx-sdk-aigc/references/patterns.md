# AIGC SDK Patterns

用于 `sdks/aigc` 的平台 API、streaming 与 proxy/observe 场景。

## 先判断什么

1. 这是 auth/sdk、平台 API、streaming，还是 proxy/observe？
2. 是否应该继续复用 `AigcAuth + AigcSdk`？
3. 是否仍在“同协议原始透传”边界内？

## 平台 API 模板

```rust
pub trait OpenAiFooApi: AigcSdkExt {
    fn foo(
        &self,
        req: &OpenAiFooReq,
    ) -> impl std::future::Future<Output = anyhow::Result<OpenAiFooResp>> + Send {
        self.post_json_ret("foo", req)
    }
}
```

## proxy 检查清单

```text
- 保留 protocol + model
- provider 差异优先收敛到 AigcSdk hook
- before_send() 统一处理鉴权和固定协议头
- streaming 发送层保持 AigcStream(meta + raw)
- 不做跨协议翻译，不做统一 DTO 网关
```

## 常见错误

```text
❌ DTO 回退到 provider 聚合层
❌ 在 proxy 层重复手写鉴权
❌ streaming 发送层直接返回 provider 事件对象
❌ 在 observer 里提前生成 preview/summary/truncated
```

## 正确做法

```text
✅ 单 HTTP API 一个 trait 文件，DTO 邻近 trait
✅ provider 特例优先挂在 AigcSdk hook 或 provider SDK 本身
✅ observer 默认 raw-only
✅ 最小验证优先 cargo test -p kx-sdk-aigc
```
