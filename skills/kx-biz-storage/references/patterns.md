# kx-biz-storage Patterns

用于 `kx-biz-storage` 的模块级 reference，聚焦 `kx-biz-storage` 作为“存储封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 接统一文件/存储接口
- 扩展存储配置与文件服务
- 使用 id2url 与 URL 缓存

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-storage = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`StorageRouter::apis()`。
3. 安装或初始化入口：`StorageInstall::migrate()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-storage = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: StorageRouter::apis()
- Install: StorageInstall::migrate()
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
- 优先复用 StgOpMgr 和 id2url，不要在业务层重复写 URL 拼装和 presign 逻辑。
- 本地存储 URL 依赖参数配置 `local_storage_host`。
- 文件 URL 带缓存，不要忽略 UrlCache 语义。
```

## 常见错误

```text
❌ 业务代码里重复拼文件访问地址或手工 presign。
❌ 只改数据库或 operator 初始化，忘了 URL 缓存与参数依赖。
❌ 把资源内容或页面配置问题误归到 storage。
```

## 正确做法

```text
✅ 优先复用 `StorageRouter` / `StorageInstall` / `StgOpMgr` / `Id2Url`。
✅ 回答时明确 cfg/file/vd 三块与 URL 缓存边界。
✅ 资源内容类问题 handoff 到 kx-biz-res。
```
