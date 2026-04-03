---
name: kx-sdk
description: |
  Use when 任务明确属于 kx 仓库的 sdks/ 第三方接入与 SDK 封装开发。

  触发场景：
  - 新增或修改 sdks/<provider> crate
  - 设计第三方 API trait、请求/响应 DTO、token/cache 复用
  - 判断某项能力该落 sdks 还是 crates
  - 需要让新 SDK 写法与 wx-app / wx-core / sdks/core 保持一致

  触发词：SDK、第三方接入、provider、token、cache、DTO、trait、reqwest、sdks、wx-app、wx-core
---

# kx-sdk

`kx-sdk` 是 `sdks/` 目录下第三方接入 / SDK 开发专用 skill。
目标是让新增或维护的 SDK 与当前仓库既有模式保持一致，而不是每个 provider 都长成一套新风格。

如果任务已经明确落在 `sdks/aigc`，尤其涉及 `AigcAuth`、`AigcSdk`、平台级单 API trait、流式能力或 proxy，请优先切到 `kx-sdk-aigc`。

## 适用边界

### 适用

- 新增 `sdks/<provider>` crate 或在现有 SDK 中加新接口
- 抽象第三方 API 的 trait、请求/响应 DTO、token 刷新和缓存逻辑
- 判断某个第三方能力应落 `sdks/` 还是 `crates/`
- 对齐 `reqwest` 调用、鉴权、缓存、错误返回与已有 SDK 风格

### 不适用

- 纯 Rust 编译器 / trait / lifetime / Send / Sync 问题
  - 交给 `rust-router`
- 明确的 bug、回归、测试失败排查
  - 交给 `systematic-debugging`
- 实践层 `bins/` / `bizs/` / `ents/` 落地
  - 交给 `kx-rs`
- 明确的 `sdks/aigc` provider / proxy / stream 设计
  - 交给 `kx-sdk-aigc`

## Reference Selection

按任务类型优先读取：

- 普通 `sdks/<provider>` 接口扩展
  - 读 `references/patterns.md`
- 判断 `sdks/` 与 `crates/` 边界
  - 先读 `references/patterns.md`，再结合当前仓库实际目录判断
- 如果问题已经明确进入 `sdks/aigc`
  - 立即 handoff 到 `kx-sdk-aigc`，不要继续用本 skill 展开

## 落点判断表

| 需求 | 默认落点 | 原因 |
| --- | --- | --- |
| 第三方平台接口封装 | `sdks/<provider>` | 属于 provider 适配层 |
| 统一 token / store / HTTP 返回抽象 | `sdks/core` 或相关 sdk 基础层 | 供多个 SDK 复用 |
| 多个 provider 共用的纯基础密码学扩展 | `crates/`（如 `crates/kx-rsa`） | 不应在多个 SDK 重复造轮子 |
| 下游业务 CRUD / 控制器 | 不在 `sdks/` | 这不是 SDK 问题 |

## 推荐实现模板

优先使用“能力 trait + 默认实现 + blanket impl”形状，而不是直接把逻辑塞进具体 struct。

### 完整模板

下面这个模板是当前仓库已存在的真实模式，可直接类比扩展：

```rust
pub trait AccessTokenQry: GetAccessToken + GetClient {
    fn access_qry_post<Q, T>(&self, url: &str, data: &Q) -> impl Future<Output = Result<T>>
    where
        Q: Serialize + Sync,
        T: DeserializeOwned + Send + 'static,
    {
        async move { self.access_qry(Method::POST, url, data).await }
    }

    fn access_qry<Q, T>(&self, m: Method, url: &str, data: &Q) -> impl Future<Output = Result<T>>
    where
        Q: Serialize + Sync,
        T: DeserializeOwned + Send + 'static,
    {
        async move {
            let access_token = self.access_token().await?;
            self.cli()
                .request(m, url)
                .query(&json!({"access_token": access_token}))
                .json(data)
                .to_ret()
                .await
        }
    }
}

impl<T: GetAccessToken + GetClient> AccessTokenQry for T {}
```

## 实现规则

1. **一个 trait 表达一组清晰能力**
   - 不要把整个平台所有 API 都堆进单个巨型 impl
2. **异步接口统一返回 `impl Future`**
   - 不要为这类 SDK trait 引入 `#[async_trait]`
3. **默认优先 `&self`**
   - 发请求、读 token、写外部缓存都不自动等于 `&mut self`
4. **优先复用已有能力 trait**
   - 如 `GetClient`、`GetAccessToken`、`TokenStore`、`ToRet`
5. **DTO 与 trait 邻近组织**
   - 请求/响应 DTO 靠近接口 trait，而不是散落到无关模块
6. **验证优先跑最小必要命令**
   - 先 `cargo check -p <crate>`，共享抽象变更再扩大范围

## 常见错误 vs 正确做法

### 常见错误

```rust
// ❌ 错误：直接给 trait 上 async_trait
#[async_trait::async_trait]
pub trait FooApi {
    async fn foo(&self) -> anyhow::Result<FooRet>;
}

// ❌ 错误：把鉴权、组装 URL、解析返回全都散写在每个接口里
pub async fn foo(&self) -> anyhow::Result<FooRet> {
    let token = self.token_store.read().await?;
    let resp = self.client.post(...).send().await?;
    ...
}
```

### 正确做法

```rust
// ✅ 正确：trait 返回 impl Future，并复用公共能力
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

## 首选参考文件

优先回看这些真实文件：

- `sdks/wx-app/src/lib.rs`
- `sdks/wx-app/src/comp/comp_auth_url.rs`
- `sdks/wx-app/src/wx_app_sdk.rs`
- `sdks/wx-core/src/token/component_token.rs`
- `sdks/core/src/token_store.rs`

## 输出模板

默认使用这个结构：

```text
问题归类
- 是新增 SDK 能力，还是沿用现有模式补接口

推荐落点
- crate / 模块 / 文件位置

trait 设计
- 需要哪些能力 trait

公共能力复用
- 复用哪些现有抽象

DTO 与模块组织
- DTO 放哪里，模块怎么拆

验证方式
- 最小必要 cargo 命令

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
我要给 wx-app 加一个新的 access_token 接口，怎么写得跟现有风格一致？
```

**Output direction**

```text
- 先回看 sdks/wx-app/src/lib.rs 的 AccessTokenQry 模式。
- 新接口优先写成能力 trait，默认返回 impl Future。
- 先判断能否复用 GetAccessToken + GetClient + ToRet。
- 请求/响应 DTO 紧邻接口 trait 放置。
- 最后跑 cargo check -p 对应 crate 做最小验证。
```
