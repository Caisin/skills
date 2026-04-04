# KX Biz Param Module Map

这是 `kx-biz-param` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

### 顶层

- `kx-biz-param/src/lib.rs`
  - 暴露 `cache / ctl / dto / install / router / svc`
  - `pub use kx_ents_param::entity`
- `kx-biz-param/src/router.rs`
  - 聚合四个子域路由：`/dic`、`/param`、`/i18n`、`/key_i18n`
  - 对外统一入口：`ParamRouter::apis()`
- `kx-biz-param/src/install.rs`
  - 用 `SeaOrms::param()` 跑 `kx_ents_param::entity::prelude::auto_migrate`
  - 对外统一迁移入口：`ParamInstall::migrate()`

### param

- `kx-biz-param/src/ctl/param.rs`
  - 分页、保存、删除、按 code 取值、取 `sys_setting`、手工刷新缓存
- `kx-biz-param/src/svc/param_svc.rs`
  - 保存 / 删除 / 获取参数值 / 获取系统设置 / 刷新缓存
- `kx-biz-param/src/cache/param_cache.rs`
  - `KxParamCache` trait：`get_param / set_param / set_v / get_v / refresh_cache`

### dic

- `kx-biz-param/src/ctl/dic.rs`
  - 字典分页、数据分页、单条保存、批量保存、拖拽排序、删字典、删字典项、查缓存
- `kx-biz-param/src/svc/dic_svc.rs`
  - 排序事务、刷新缓存、删除字典及关联数据、保存字典编码
- `kx-biz-param/src/cache/dic_cache.rs`
  - Redis key：`dic_data:{code}`
  - `get_by_code / save_data / save_datas / fresh_cache`

### i18n

- `kx-biz-param/src/ctl/i18n.rs`
  - 按 locale 取整棵文案、保存文案、通过值查 key、通过 key 查值、检查 key 可用性
- `kx-biz-param/src/svc/i18n_svc.rs`
  - 读写 `KxI18n`，内部操作 JSON 路径
- `kx-biz-param/src/dto/i18n_dto.rs`
  - `I18nSaveData`：支持直接给 data，也支持 key/value 合成局部 JSON

### key_i18n

- `kx-biz-param/src/ctl/key_i18n.rs`
  - 分页、保存、导出完整 i18n 数据
- `kx-biz-param/src/svc/key_i18n_svc.rs`
  - 把多条 `(key, lang, val)` 聚合成多语言 JSON

## 实体对应关系

- `KxParam` -> `ents/param/src/entity/core/kx_param.rs`
- `DicCode` / `DicData` -> `ents/param/src/entity/core/*.rs`
- `KxI18n` -> `ents/param/src/entity/kx_i18n.rs`
- `KxKeyI18n` -> `ents/param/src/entity/kx_key_i18n.rs`

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 其他项目引入依赖 | `kx-biz-param = { version = "0.1", registry = "hekx" }` |
| 业务项目想直接接参数通用路由 | `router.rs` |
| 业务项目想统一执行参数模块迁移 | `install.rs` |
| 新增系统参数接口 | `ctl/param.rs` + `svc/param_svc.rs` |
| 参数改完立即失效缓存 | `svc/param_svc.rs` + `cache/param_cache.rs` |
| 查字典缓存 / 刷新字典缓存 | `cache/dic_cache.rs` + `svc/dic_svc.rs` |
| 字典批量替换 / 排序 | `cache/dic_cache.rs` 或 `svc/dic_svc.rs` |
| locale 维度国际化 | `ctl/i18n.rs` + `svc/i18n_svc.rs` |
| key/lang 维度翻译管理 | `ctl/key_i18n.rs` + `svc/key_i18n_svc.rs` |
| 路由新增挂载 | `router.rs` |
| 模块安装或迁移 | `install.rs` |

## 回答时优先强调的事实

```text
- 这是一个真实存在于当前仓库的业务模块，不是“下游业务仓库约定”。
- 这个 crate 的定位是参数业务统一封装包，优先用于简化业务侧参数代码。
- 其他项目依赖写法是 `kx-biz-param = { version = "0.1", registry = "hekx" }`。
- 默认数据源就是 param。
- 这个模块的核心业务重点不是 soft delete，而是缓存失效、state 过滤、事务一致性与两套国际化模型。
```


## 常见错误

```text
❌ 只看 router，不继续下钻到对应 ctl / svc / cache，导致落点判断过粗
❌ 把 i18n 与 key_i18n 混用，接口层落错文件
❌ 忽略缓存层文件，只改 ctl 或 svc
❌ 忽略这个 crate 已有的统一入口，转而在业务项目里散着写参数逻辑
❌ 在依赖配置里写成 `registery`，导致 Cargo 配置错误
```

## 正确做法

```text
✅ 先用本文件锁定子域与目标文件，再去 patterns.md 拿实现套路
✅ 优先判断能否直接复用 ParamRouter::apis() / ParamInstall::migrate()
✅ 其他项目引入时使用 `kx-biz-param = { version = "0.1", registry = "hekx" }`
✅ 回答时把路由入口、业务文件和实体文件串起来说明
✅ 涉及缓存或事务时，明确提醒继续查看对应 cache / svc 文件
```
