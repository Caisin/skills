---
name: kx-biz-storage
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-storage` 这个存储封装包，统一提供存储配置、文件上传/访问、Vditor 接入、id2url 转换、存储操作器管理与缓存能力。

  触发场景：
  - 在业务项目里接入统一存储路由
  - 需要复用 `StorageRouter::apis()` 与 `StorageInstall::migrate()`
  - 需要通过 `StgOpMgr` 获取存储 operator 或文件 URL
  - 需要把 JSON 里的文件 id 统一转成 URL

  触发词：kx-biz-storage、StorageRouter、StorageInstall、StgOpMgr、id2url、文件上传、Vditor、storage cfg
---

# kx-biz-storage

`kx-biz-storage` 是当前仓库里专门面向 `kx-biz-storage` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-storage` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 接统一文件/存储接口
- 扩展存储配置与文件服务
- 使用 id2url 与 URL 缓存

### 不适用

- 资源内容业务编排
- 参数配置表定义
- 底层 opendal/provider 实现细节

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-storage`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-storage` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-storage = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: StorageRouter::apis()
- Install: StorageInstall::migrate()
```

## 回答时优先强调的事实

- 统一路由分成 cfg / file / vd 三块。
- `StgOpMgr` 是核心存储操作管理入口。
- 本 crate 依赖参数库中的 `local_storage_host` 等配置。

## 最常用的落地套路

```text
- 优先复用 StgOpMgr 和 id2url，不要在业务层重复写 URL 拼装和 presign 逻辑。
- 本地存储 URL 依赖参数配置 `local_storage_host`。
- 文件 URL 带缓存，不要忽略 UrlCache 语义。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 业务代码里重复拼文件访问地址或手工 presign。
❌ 只改数据库或 operator 初始化，忘了 URL 缓存与参数依赖。
❌ 把资源内容或页面配置问题误归到 storage。
```

### 正确做法

```text
✅ 优先复用 `StorageRouter` / `StorageInstall` / `StgOpMgr` / `Id2Url`。
✅ 回答时明确 cfg/file/vd 三块与 URL 缓存边界。
✅ 资源内容类问题 handoff 到 kx-biz-res。
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
我想在项目里统一接文件上传、存储配置和 Vditor 上传接口，最短入口是什么？
```

**Output direction**

```text
应命中 kx-biz-storage，并指向 `StorageRouter::apis()` 与 `StorageInstall::migrate()`。
```
