# kx-biz-adm Patterns

用于 `kx-biz-adm` 的模块级 reference，聚焦 `kx-biz-adm` 作为“管理端聚合封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 接入统一后台路由
- 扩展后台聚合层 install/router
- 判断某个后台接口应该落聚合层还是子模块

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-adm = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`AdmRouter::apis()`, `AdmRouter::basic_apis()`, `AdmRouter::app_apis()`。
3. 安装或初始化入口：`AdmInstall::migrate()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-adm = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: AdmRouter::apis(), AdmRouter::basic_apis(), AdmRouter::app_apis()
- Install: AdmInstall::migrate()
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
- 优先把它当成后台网关层，而不是功能实现层。
- 路由聚合优先复用现成子 crate router，不要在聚合层复制业务 handler。
- 新增后台能力时先判断是“新挂一个子路由”还是“扩展现有子 crate”。
```

## 常见错误

```text
❌ 在业务项目里重复手工 nest 多个后台子模块，而不复用 `AdmRouter`。
❌ 把具体业务逻辑塞进聚合层，而不是放回子 crate。
❌ 安装时漏掉子模块 install/migrate 顺序。
```

## 正确做法

```text
✅ 优先复用 `AdmRouter` 与 `AdmInstall`。
✅ 聚合层只做路由与安装编排，业务实现继续下沉。
✅ 遇到子域问题时直接 handoff 到对应 crate skill。
```
