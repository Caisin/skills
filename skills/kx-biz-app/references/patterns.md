# kx-biz-app Patterns

用于 `kx-biz-app` 的模块级 reference，聚焦 `kx-biz-app` 作为“应用端聚合封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 接应用端统一路由
- 运行 app 端安装流程
- 扩展 app 聚合层

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-app = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`AppRouter::apis()`。
3. 安装或初始化入口：`AppInstall::install()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-app = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: AppRouter::apis()
- Install: AppInstall::install()
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
- 优先把它看成 app 端网关层。
- 聚合层负责 nest 现有子路由，不应复制子业务实现。
- 如果只是要加 app 端一条聚合路由，先判断该路由是否已在子 crate 中存在。
```

## 常见错误

```text
❌ 把具体 res/auth/asset 逻辑塞到 app 聚合层。
❌ 自己在项目里重复挂一堆 app 子路由，而不复用 `AppRouter`。
❌ 把后台管理入口和 app 端聚合混在一起。
```

## 正确做法

```text
✅ 优先复用 `AppRouter` 与 `AppInstall`。
✅ 聚合层只做 app 端路由与安装编排。
✅ 具体子域问题 handoff 到对应 crate。
```
