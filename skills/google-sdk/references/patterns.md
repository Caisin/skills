# Google SDK Patterns

用于 `google-sdk` 的补充 reference，聚焦 `sdks/google` 的真实结构与长期约定。

## 适用场景

- 扩展 `GoogleOuath2Sdk` 的 scope / token / auth URL 行为
- 判断 Google API 应走 OAuth2 client 还是 service account
- 新增 `src/youtube/`、`src/admob/`、`src/androidpublisher/`、`src/firebase/` 下的接口

## 推荐模板

### 1. OAuth2 client 多 scope 宿主模板

```rust
pub trait GoogleOuath2Token {
    fn access_token(&self) -> impl Future<Output = Result<String>>;
}

pub struct GoogleOuath2Sdk<T: TokenStore> {
    cli: reqwest::Client,
    client_info: ClientInfo,
    store: Option<T>,
    scopes: GoogleOauthScopes,
    user_key: String,
}

impl<T: TokenStore> GoogleOuath2Sdk<T> {
    pub fn new_scopes_with_user_key<I>(
        sa_json: &str,
        usages: I,
        user_key: impl Into<String>,
    ) -> Result<Self>
    where
        I: IntoIterator<Item = Usage>,
    {
        // scope 在 SDK 内部归一化成空格分隔字符串
        // token key = 短前缀 + md5(client_id|user_key|ordered_scope|token_kind)
    }
}
```

### 2. Google API trait 模板

```rust
pub trait YoutubeVideosApi: GetClient + GoogleOuath2Token {
    fn videos_list(&self, req: &VideoListReq) -> impl Future<Output = Result<VideoListResp>> {
        async move {
            self.cli()
                .get("https://www.googleapis.com/youtube/v3/videos")
                .bearer_auth(self.access_token().await?)
                .query(&req.query_pairs()?)
                .to_ret()
                .await
        }
    }
}
```

## 常见错误

```text
❌ 让业务方自己拼接 scope 字符串，而 SDK 内部仍只有单 usage 字段
❌ token key 不带 user_key，导致不同 Google 用户共用一组缓存 key
❌ 把 YouTube / AdMob / Firebase 接口混写在 client_sdk.rs
❌ 大响应体一开始就全量手写超大 DTO，导致基础 SDK 负担过重
```

## 正确做法

```text
✅ scope 组合、user_key、短 hash token key 统一收敛在 GoogleOuath2Sdk 内部
✅ OAuth2 client 与 service account 两条鉴权链路分清楚
✅ 接口按子模块拆分，DTO 与 trait 邻近组织
✅ 先用单测锁住参数序列化 / URL 生成 / cache key 行为，再补实现
```
