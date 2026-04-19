---
name: google-sdk
description: |
  Use when 任务明确聚焦 `sdks/google` / `kx-sdk-google` 的 Google 平台 SDK 开发，包括 OAuth2 client、service account、YouTube / AdMob / Android Publisher / Firebase 能力封装与调试。

  触发场景：
  - 修改 `sdks/google/src/client_sdk.rs`、`src/auth/*`、`src/youtube/*`、`src/admob/*`、`src/androidpublisher/*`、`src/firebase/*`
  - 需要判断某个 Google 能力该走 `GoogleOAuth2Sdk` 还是 `GoogleSdk`
  - 需要补 scope、access token / refresh token、service account token cache 或 Google API 子模块接口
  - 需要给 `sdks/google` 新增 YouTube / AdMob / Android Publisher / Firebase API trait、DTO 或请求样板

  触发词：google sdk、kx-sdk-google、sdks/google、GoogleOAuth2Sdk、GoogleSdk、OAuth2、scope、YouTube、AdMob、Android Publisher、Firebase
---

# Google SDK

`google-sdk` 是 `sdks/google` 的专用 skill。
它负责当前仓库里 Google 平台相关的 OAuth2 client、service account 鉴权、以及 YouTube / AdMob / Android Publisher / Firebase 子模块能力；不替代通用 `kx-sdk`，而是在命中 `sdks/google` 时提供更具体的落点与约束。

如果 `sdks/google` 的结构、约定或测试布局变化了，必须同步更新本 skill、`kx-entry`、`kx-sdk` 和 `AGENTS.md`。

## 适用边界

### 适用

- `GoogleOAuth2Sdk`、`GoogleSdk`、`GoogleOAuth2Token` 改动
- `src/auth/` 下的 `scope/` / `info.rs` / token 相关改动
- `src/youtube/`、`src/admob/`、`src/androidpublisher/`、`src/firebase/` 下的 Google API 接口扩展
- scope 组合、token store key、授权 URL（含 state 透传）、code2token / refresh_token 流程调整
- 判断某个 Google API 该走 OAuth2 用户态鉴权还是 service account

### 不适用

- `sdks/aigc` 相关问题
  - 交给 `kx-sdk-aigc`
- 纯 Rust 编译器 / 生命周期 / Send / Sync 问题
  - 交给 `rust-router`
- 只是在判断一般 `sdks/` 风格，而不是明确进入 `sdks/google`
  - 交给 `kx-sdk`

## Reference Selection

按任务类型优先读取：

- OAuth2 client / scope / refresh token
  - 先看 `sdks/google/src/client_sdk.rs`
  - 再看 `sdks/google/src/auth/scope/`
  - 再读 `references/patterns.md`
- service account token / `GoogleSdk`
  - 先看 `sdks/google/src/lib.rs`
  - 再看 `sdks/google/src/auth/scope/`
  - 再读 `references/patterns.md`
- YouTube Data API
  - 先看 `sdks/google/src/youtube/`
  - 再读 `references/patterns.md`
- AdMob / Android Publisher / Firebase
  - 先看对应 `src/<submodule>/`
  - 再读 `references/patterns.md`

## 快速定位表

| 需求 | 优先文件 / 目录 | 先确认什么 |
| --- | --- | --- |
| OAuth2 client 授权 URL / code2token / refresh token | `sdks/google/src/client_sdk.rs`、`src/auth/scope/` | 是否应走 `GoogleOAuth2Sdk`，以及 scope 是否需要多值 |
| service account token / `scope_token()` | `sdks/google/src/lib.rs`、`src/auth/scope/` | 是否应走 `GoogleSdk` + `Scope` |
| YouTube Data API | `sdks/google/src/youtube/` | 是否需要 OAuth2 用户态 scope |
| AdMob | `sdks/google/src/admob/` | 是否复用 `GoogleOAuth2Token` |
| Android Publisher | `sdks/google/src/androidpublisher/`、`src/purchases/` | 是否复用 service account token |
| Firebase | `sdks/google/src/firebase/` | 是否复用 service account token |

## 核心规则

1. **先分清鉴权宿主**
   - 用户态 OAuth2 走 `GoogleOAuth2Sdk`
   - 服务账号走 `GoogleSdk`
   - 当前不要把两者合并成一个大而全宿主；优先保持两条鉴权链路分离、按场景选择入口
2. **OAuth2 scope 默认要支持多值**
   - 授权 URL 里的 `scope` 应按 Google 文档使用空格分隔的多个 scope
   - 单 scope 构造入口要保留，避免破坏现有调用方
   - `sdks/google` 内部统一使用 `auth::scope::Scope` 命名，不再使用 `usage`
   - 多 scope 聚合能力现在直接收敛在 `Scope` 上，优先复用 `Scope::from_scopes` / `add_scope`
   - `state` 默认可自动生成；若业务需要透传回调状态，优先提供显式 `*_with_state(...)` 入口而不是让调用方自己拼 URL
3. **OAuth2 token key 必须带用户维度**
   - token store key 不要直接拼长 scope 串
   - 应统一走短前缀 + hash
   - hash material 至少包含 `client_id + user_key + scope + token_kind`
4. **一个 Google 能力落一个清晰子模块**
   - YouTube 放 `src/youtube/`
   - AdMob 放 `src/admob/`
   - Android Publisher 放 `src/androidpublisher/` / `src/purchases/`
5. **API trait 优先复用 `GetClient` / token trait / `ToRet`**
   - 不要在每个接口里重复手写 bearer、JSON 解析与错误样板
6. **大响应体先做最小结构化**
   - 顶层分页字段结构化
   - 巨大 `items` 可先保留 raw JSON，避免基础 SDK 过早膨胀
7. **验证优先最小必要**
   - 先跑相关单测
   - 再跑 `cargo check -p kx-sdk-google`

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 所有 Google API 都混到一个大文件里处理
❌ OAuth2 只支持单 scope，把 Google 的多 scope 约束留给调用方自己拼字符串
❌ token key 只按 client + scope 区分，导致不同用户共用一组 refresh/access token key
❌ 明明应该用 GoogleOAuth2Sdk，却错误走 service account
❌ 把 `GoogleOAuth2Sdk` 和 `GoogleSdk` 强行合成一个宿主，导致构造参数、token 流程和调用语义都混在一起
❌ 每个接口都手写 bearer_auth / to_ret 样板
```

### 正确做法

```text
✅ 先判定走 GoogleOAuth2Sdk 还是 GoogleSdk
✅ scope 在 SDK 内部做收敛与校验，支持多 scope 组合
✅ 对 Google 权限枚举统一使用 `auth::scope::Scope`
✅ 多用户场景下显式设置 user_key，让 token key 具备用户隔离能力
✅ 子模块按 YouTube / AdMob / Android Publisher / Firebase 拆分
✅ trait 默认实现优先复用 GetClient / GoogleOAuth2Token / ToRet
```

## 输出模板

```text
问题归类
- OAuth2 client、service account，还是具体 Google API 子模块

改动落点
- crate / 文件 / 子模块位置

关键约定
- 当前任务必须遵守的 3~6 条 Google SDK 规则

验证方式
- 最小必要单测 / cargo 命令

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
我要给 sdks/google 加 YouTube videos.list，并确认 OAuth2 scope 怎么设计才不把多个 scope 写死在业务侧。
```

**Output direction**

```text
- 先确认这是 sdks/google 专门问题，应使用 google-sdk。
- 先判断 videos.list 走 GoogleOAuth2Sdk，而不是 service account。
- scope 组合逻辑优先下沉到 client_sdk.rs，而不是让调用方手工拼接字符串。
- YouTube 接口落到 src/youtube/，请求/响应贴近 trait 放置。
- 最后先跑相关单测，再跑 cargo check -p kx-sdk-google。
```
