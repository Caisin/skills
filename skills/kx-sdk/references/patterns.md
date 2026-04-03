# SDK Patterns

用于 `sdks/` 通用第三方接入开发场景。

## 先判断什么

1. 这是 provider 适配层，还是纯基础能力？
2. 是否已有 `GetClient`、`GetAccessToken`、`TokenStore`、`ToRet` 可复用？
3. 这是普通 `sdks/<provider>`，还是已经进入 `sdks/aigc`？

## 推荐模板

```rust
pub trait FooApi: GetClient + GetAccessToken {
    fn foo(&self) -> impl Future<Output = anyhow::Result<FooRet>> {
        async move {
            let token = self.access_token().await?;
            self.cli()
                .post("https://example.com/foo")
                .query(&json!({"access_token": token}))
                .to_ret()
                .await
        }
    }
}

impl<T: GetClient + GetAccessToken> FooApi for T {}
```

## 常见错误

```text
❌ 直接在 trait 上引入 async_trait
❌ 每个接口都重新手写 token / header / JSON 解包样板
❌ DTO 与 trait 分散在无关模块
❌ 明明是 aigc 场景，却继续沿用通用 sdk 指南
```

## 正确做法

```text
✅ trait 返回 impl Future
✅ 公共请求样板下沉到基础 trait
✅ DTO 与能力 trait 邻近组织
✅ 命中 sdks/aigc 时立刻 handoff 到 kx-sdk-aigc
```
