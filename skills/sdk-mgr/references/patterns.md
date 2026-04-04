# sdk-mgr Patterns

用于 `sdk-mgr` 的模块级 reference，聚焦 `sdk_mgr` 作为“SDK 管理封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 按 app_id 获取 SDK
- 理解 param 配置到 SDK 实例的映射
- 扩展 SDK 管理封装

## 先记住这几条

1. 其他项目依赖写法：`sdk_mgr = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`无统一 router，核心入口是 `DtSdkMgr` / `WxSdkMgr``。
3. 安装或初始化入口：`无 install；依赖 `kx-biz-param` 中的配置表`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
sdk_mgr = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: 无统一 router，核心入口是 `DtSdkMgr` / `WxSdkMgr`
- Install: 无 install；依赖 `kx-biz-param` 中的配置表
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
- 先看是否已经能通过参数库配置直接拿到 SDK，不要手工重复初始化。
- feature 关闭时不要误以为对应 manager 一定存在。
- WxSdkMgr 会尝试初始化消息加解密 `Crypto`。
```

## 常见错误

```text
❌ 把 sdk_mgr 当成 HTTP 接口包。
❌ 绕过 manager 层在业务代码里重复 new SDK。
❌ 忽略 feature 开关和参数库配置来源。
```

## 正确做法

```text
✅ 优先复用 `DtSdkMgr` / `WxSdkMgr`。
✅ 回答时强调依赖 `kx-biz-param` 中的配置表。
✅ 协议实现问题 handoff 到对应 SDK skill。
```
