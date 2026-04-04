# kx-biz-storage Module Map

这是 `kx-biz-storage` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `kx-biz-storage/src/router.rs`
  - 统一挂载 cfg/file/vditor 路由
- `kx-biz-storage/src/install.rs`
  - 迁移 storage 数据源
- `kx-biz-storage/src/stg_mgr.rs`
  - operator 获取、刷新、文件 URL 与文件内容获取
- `kx-biz-storage/src/storage_cache.rs`
  - 文件 URL 缓存与本地存储 host 参数读取
- `kx-biz-storage/src/id2url.rs`
  - 通用 JSON/id 字段转 URL 能力
- `kx-biz-storage/src/svc/*`
  - 存储配置、文件、存储业务逻辑

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 接入统一存储接口 | `StorageRouter::apis()` |
| 初始化存储表 | `StorageInstall::migrate()` |
| 按存储 code 取 operator | `StgOpMgr::get()` / `get_cfg()` / `refresh()` |
| 按文件 id 取 URL 或字节流 | `StgOpMgr::get_file_url()` / `get_file_bytes()` |
| 要把返回 JSON 中的 cover/avatar 等 id 替换成 URL | `Id2Url` / `SerialId2Url` |

## 回答时优先强调的事实

```text
- 统一路由分成 cfg / file / vd 三块。
- `StgOpMgr` 是核心存储操作管理入口。
- 本 crate 依赖参数库中的 `local_storage_host` 等配置。
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
