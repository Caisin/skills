# kx-biz-res Patterns

用于 `kx-biz-res` 的模块级 reference，聚焦 `kx-biz-res` 作为“资源内容封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 接管理端资源路由
- 接应用端资源/文档/配置路由
- 扩展资源内容子域

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-res = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`ResRouter::apis()`, `ResRouter::app_apis()`, `ResRouter::notify_apis()`。
3. 安装或初始化入口：`ResInstall::install()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-res = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: ResRouter::apis(), ResRouter::app_apis(), ResRouter::notify_apis()
- Install: ResInstall::install()
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
- 先判断需求属于 adm、app 还是 notify，再继续细分到 res/category/tag/item/page/sl/doc。
- 如果只是要统一挂路由，优先复用 ResRouter，不要在业务项目里散着 merge。
- 存储 URL、文件读取等问题应回到 storage crate。
```

## 常见错误

```text
❌ 把管理端、应用端、通知接口混成一个入口说明。
❌ 把存储上传或文件 URL 逻辑说成 res 自己实现。
❌ 忽略页面配置与资源内容是两个不同子域。
```

## 正确做法

```text
✅ 按 adm/app/notify 三类入口回答。
✅ 先复用 `ResRouter` 与 `ResInstall`，再下钻到具体子域。
✅ 文件存储问题 handoff 到 kx-biz-storage。
```
