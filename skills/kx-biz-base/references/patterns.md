# kx-biz-base Patterns

用于 `kx-biz-base` 的模块级 reference，聚焦 `kx-biz-base` 作为“基础能力封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 运行 base 数据源迁移
- 使用或扩展 ds 管理接口
- 说明这个 crate 当前真实边界

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-base = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`DsCtl::apis()（通常由聚合层挂载）`。
3. 安装或初始化入口：`BaseInstall::migrate()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-base = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: DsCtl::apis()（通常由聚合层挂载）
- Install: BaseInstall::migrate()
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
- 回答时要尊重当前 crate 真实边界，不要把“基础能力”泛化成仓库里所有公共能力。
- 如果只是要在后台里挂 DS 接口，通常由聚合层去 nest `DsCtl::apis()`。
- base crate 当前更像轻量支撑模块而不是大而全平台层。
```

## 常见错误

```text
❌ 把不存在于当前 crate 的能力硬说成 base 负责。
❌ 误以为它有独立 router.rs 聚合所有基础接口。
❌ 把 auth/param/storage 等问题误归到 base。
```

## 正确做法

```text
✅ 先说明当前 crate 真实能力是 base 迁移 + DS 管理。
✅ 要挂 DS 接口时直接指向 `DsCtl::apis()`。
✅ 超出边界时 handoff 到正确的业务 crate。
```
