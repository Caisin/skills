# kx-biz-auth Patterns

用于 `kx-biz-auth` 的模块级 reference，聚焦 `kx-biz-auth` 作为“认证鉴权封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 接入统一认证路由
- 扩展权限/用户/菜单/登录能力
- 排查 auth 与 log 数据源初始化

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-auth = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`AuthRouter::apis()`。
3. 安装或初始化入口：`AuthInstall::migrate()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-auth = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: AuthRouter::apis()
- Install: AuthInstall::migrate()
```

### 接入顺序

```text
1. 先引入依赖
2. 再复用 install / migrate 入口
3. 再复用 router 或 manager 入口
4. 最后按需扩展内部实现
```

---

## 回答策略

```text
- 先复用统一 auth 路由，再决定是否扩展某个认证子域。
- 安装时不要只迁移 auth，`OpLog` 也在这个 crate 里一起初始化。
- 用户/角色/菜单/权限属于不同子域，回答时不要混成一个大而全说明。
```

## 钉钉登录接入模板

### 前端发起登录

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

说明：

```text
- 单应用默认走 `/auth/dt/login`
- 多应用场景走 `/auth/dt/login/{app_id}`
- `redirect_url` 应传发起登录时的源地址
```

### 服务端路由语义

基于当前 crate 现有实现：

```text
- 登录入口：`/auth/dt/login`
- 多应用登录入口：`/auth/dt/login/{app_id}`
- 回调入口：`/auth/dt/callback/{app_id}`
- 回调成功后，会把登录结果追加到最初的 `redirect_url` 再跳回去
```

### 前端处理回跳结果

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

说明：

```text
- 源地址页面初始化时要检查是否存在 `access_token`
- 一旦发现登录结果，就要建立本地登录态
- 之后再跳业务首页或目标页
```

## 常见错误

```text
❌ 只接了用户登录接口，却忘了统一 auth router 里还有权限和系统管理子域。
❌ 只迁移了 auth 数据源，漏掉日志表。
❌ 把参数、SDK 或资源类问题混进 auth skill。
❌ 前端绕开 `/auth/dt/login`，直接拼外部钉钉地址
❌ 回调后不监听源地址参数，导致 token 丢失
```

## 正确做法

```text
✅ 优先复用 `AuthRouter::apis()` 与 `AuthInstall::migrate()`。
✅ 按 app/social/per/system/user 子域拆回答案。
✅ 涉及参数或 SDK 时分别 handoff 到 kx-biz-param 或 sdk-mgr。
✅ 钉钉登录统一通过 auth 路由发起，并由源地址统一消费回跳参数
```
