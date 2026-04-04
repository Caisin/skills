---
name: kx-biz-auth
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-auth` 这个认证鉴权封装包，统一提供认证、登录、权限、菜单、角色、用户、OAuth2 与社交登录相关路由和安装能力。

  触发场景：
  - 在业务项目里接入统一认证鉴权路由
  - 需要复用 `AuthRouter::apis()`
  - 需要执行认证库与操作日志的初始化 `AuthInstall::migrate()`
  - 需要扩展 app/social/per/system/user 等认证子域

  触发词：kx-biz-auth、认证、鉴权、AuthRouter、AuthInstall、oauth2、角色、菜单、权限、用户管理、钉钉登录
---

# kx-biz-auth

`kx-biz-auth` 是当前仓库里专门面向 `kx-biz-auth` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-auth` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 接入统一认证路由
- 扩展权限/用户/菜单/登录能力
- 排查 auth 与 log 数据源初始化

### 不适用

- 参数配置封装
- 资源内容路由
- 通用 SDK 封装实现

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-auth`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-auth` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-auth = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: AuthRouter::apis()
- Install: AuthInstall::migrate()
```

## 回答时优先强调的事实

- 该 crate 同时涉及 `auth` 数据源和 `log` 数据源。
- 对外统一入口是 `AuthRouter::apis()`。
- 路由按 app / dt / user / per / system / api_per / tz 分域。

## 最常用的落地套路

```text
- 先复用统一 auth 路由，再决定是否扩展某个认证子域。
- 安装时不要只迁移 auth，`OpLog` 也在这个 crate 里一起初始化。
- 用户/角色/菜单/权限属于不同子域，回答时不要混成一个大而全说明。
```

## 钉钉登录接入步骤

### 1. 前端发起钉钉授权

前端应跳转到 **钉钉登录实际路由地址**，而不是自己拼钉钉开放平台地址。

示例：

```ts
/**
 * 打开钉钉登录
 */
export async function openDingTalkLogin() {
  const url = window.location.href;
  const sp = url.split('?');
  window.location.href = `${requestClient.getBaseUrl()}/auth/dt/login?redirect_url=${sp[0]}`;
}
```

关键说明：

```text
- 如果只有默认钉钉应用，走 `/auth/dt/login`
- 如果有多个钉钉应用可选，走带应用 id 的地址 `/auth/dt/login/{app_id}`
- `redirect_url` 应传“登录成功后要跳回的源地址”
```

### 2. 服务端登录回调语义

`kx-biz-auth` 内部已经提供钉钉登录回调处理：

```text
- 登录入口：`/auth/dt/login` 或 `/auth/dt/login/{app_id}`
- 回调入口：`/auth/dt/callback/{app_id}`
- 回调成功后，会把登录结果追加到最初请求时传入的 `redirect_url`
- 未绑定场景下，会把 `access_token` 等登录信息带回源地址
```

### 3. 前端源地址处理回跳结果

登录回调跳回源地址后，前端要主动监听 URI 中是否存在登录信息，并完成本地登录态构建。

示例：

```ts
// vue项目示例,在app.vue添加这个代码,然后将登陆信息存入
// 其他项目需要根据具体项目的框架和使用具体分析,这个代码只是给个原理性操作
// 钉钉登录跳转
onMounted(() => {
  const url = window.location.href;
  const sp = url.split('?');
  const qry = qs.parse(sp[1] || {});
  if (qry?.access_token) {
    const accessStore = useAccessStore();
    accessStore.setAccessToken(qry?.access_token as string);
    const router = useRouter();
    router.push(preferences.app.defaultHomePath);
  }
});
```

关键说明：

```text
- 回跳后的源地址必须能读取 query 中的 `access_token`
- 读取成功后要立刻落本地登录态，再跳转到业务首页或目标页
- 具体监听位置随前端框架变化，但原理都是“页面初始化时检查 URI 是否带登录结果”
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只接了用户登录接口，却忘了统一 auth router 里还有权限和系统管理子域。
❌ 只迁移了 auth 数据源，漏掉日志表。
❌ 把参数、SDK 或资源类问题混进 auth skill。
❌ 前端直接拼钉钉开放平台地址，而不是走 `kx-biz-auth` 提供的登录路由。
❌ 登录回调后没有在源地址监听页面参数，导致已经回跳却没建立本地登录态。
```

### 正确做法

```text
✅ 优先复用 `AuthRouter::apis()` 与 `AuthInstall::migrate()`。
✅ 按 app/social/per/system/user 子域拆回答案。
✅ 涉及参数或 SDK 时分别 handoff 到 kx-biz-param 或 sdk-mgr。
✅ 钉钉登录优先走 `/auth/dt/login` 或 `/auth/dt/login/{app_id}`，并传 `redirect_url`
✅ 前端在回跳源地址统一处理 `access_token` 等登录结果
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
我在一个项目里想直接接用户登录、菜单角色、权限管理这些接口，不想自己散着挂，应该怎么接？
```

**Output direction**

```text
应命中 kx-biz-auth，并优先建议复用 `AuthRouter::apis()`。
```
