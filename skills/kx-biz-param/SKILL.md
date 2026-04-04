---
name: kx-biz-param
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-param` 这个参数业务统一封装包，用它来简化参数相关操作、复用统一通用路由并减少业务侧重复代码。

  触发场景：
  - 在业务项目里想直接复用参数、字典、国际化能力，而不是重复造一套参数模块
  - 需要挂载 `kx-biz-param` 提供的统一通用路由
  - 需要用 `kx-biz-param` 简化参数读取、写入、缓存刷新、字典与国际化相关操作
  - 需要扩展或维护 `kx-biz-param` crate 内的 `ctl/*`、`svc/*`、`cache/*`、`router.rs`、`install.rs`
  - 需要判断需求该落在 `param / dic / i18n / key_i18n` 哪一块

  触发词：kx-biz-param、参数业务包、参数封装包、参数模块、参数配置、系统参数、sys_setting、字典、dic、国际化、i18n、key_i18n、参数缓存、字典缓存、refresh_cache、统一路由、通用路由
---

# kx-biz-param

`kx-biz-param` 是当前仓库里专门面向 `kx-biz-param` crate 的 repo-local skill。
它的首要定位不是“再教你手写一套参数业务”，而是帮助你把 `kx-biz-param` 当成 **kx-rs 下的参数业务统一封装包** 来使用：

- 对外提供统一通用路由：`ParamRouter::apis()`
- 对外提供统一迁移入口：`ParamInstall::migrate()`
- 对内收口参数、字典、国际化、缓存相关公共能力
- 让业务项目优先复用现成封装，减少重复业务代码

它聚焦这个 crate 已经存在的四类能力：

- `param`：系统参数读写与缓存刷新
- `dic`：字典编码 / 字典数据 / 排序 / 批量保存 / 缓存
- `i18n`：按 locale 存整棵 JSON 国际化树
- `key_i18n`：按 `key + lang` 存扁平化国际化数据

回答时优先贴合 `kx-biz-param` crate 的真实结构：`src/{ctl,svc,cache,dto,router,install}.rs` 与 `ents/param/src/entity/*`。
如果用户是在“使用 kx-rs 框架”的上下文里提问，默认先回答**怎么复用这个 crate 简化业务代码**，其次才是**这个 crate 内部该怎么改**。

## 适用边界

### 适用

- 在业务项目里接入 `kx-biz-param`，复用统一参数能力与通用路由
- 判断一个“参数 / 字典 / 国际化”需求是否已经能被这个 crate 直接承接
- 给 `kx-biz-param` 新增或调整接口
- 判断逻辑应放在 `ctl / svc / cache / dto / install / router` 哪一层
- 处理参数缓存、字典缓存、批量保存、拖拽排序、刷新缓存
- 处理 `kx_i18n` 与 `kx_key_i18n` 两套国际化存储形态
- 梳理 `router.rs` 的 `/dic`、`/param`、`/i18n`、`/key_i18n` 路由入口
- 解释这个模块为什么有些读查询直接放在 ctl，有些写操作放在 svc/cache

### 不适用

- 重点在 `ents/param` 的模型设计、迁移、索引、`#[derive(Sea)]` 细节
  - 交给 `kx-sea-orm`
- 重点在通用 `kx-axum` handler / router / `R<T>` / `AxumErr` 模板
  - 交给 `kx-axum-web`
- 重点在整个 practice 层目录规划、`bins/bizs/ents` 分层
  - 交给 `kx-rs`
- 纯 Rust 编译、trait bound、Send/Sync、生命周期问题
  - 交给通用 Rust / debugging 类 skill

## Reference Selection

按任务类型优先读取：

- 想知道怎么把这个 crate 当成统一封装包接入业务项目
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-param` 的模块边界、文件落点、路由入口
  - 读 `references/module-map.md`
- 想写具体接口、缓存刷新、事务或批量逻辑
  - 读 `references/patterns.md`
- 如果问题已经下钻到实体定义或迁移模板
  - 切 `kx-sea-orm`
- 如果问题已经变成通用 web 层写法
  - 切 `kx-axum-web`

## 核心判断规则

1. **优先复用封装，再决定是否扩展**
   - 如果现有 `ParamRouter::apis()`、`ParamInstall::migrate()`、`ParamSvc`、`DicSvc`、缓存能力已经够用，优先直接接入，不要在业务侧重复实现。
2. **先分子域，再落文件**
   - 参数值 / 系统配置 -> `param`
   - 字典编码 / 字典项 / 排序 / 批量保存 -> `dic`
   - locale 对应整棵 JSON 文案 -> `i18n`
   - `key + lang` 扁平翻译数据 -> `key_i18n`
3. **纯读查询可以贴近 ctl，写入 / 失效 / 事务优先放 svc 或 cache**
   - 当前模块现状就是这样，不要为了“绝对分层”把所有简单查询都硬搬走。
4. **涉及缓存失效时，不要只改数据库**
   - `KxParam` 相关改动后要刷新参数缓存
   - `DicData` / `DicCode` 相关改动后要清理字典缓存
5. **涉及排序、批量替换、级联删除时，优先维持事务边界**
   - `DicSvc::drag_data`
   - `DicSvc::del_dic`
   - `DicCache::save_datas`
6. **不要机械套软删约定**
   - `kx-biz-param` 核心表当前主要使用 `state` 过滤启用态，而不是 `is_del` 软删字段；回答时要按模块实际结构来。
7. **默认数据源就是 `SeaOrms::param()`**
   - `install.rs`、ctl、svc、cache 都围绕 `param` 数据源展开。

## 对业务项目的默认建议

当用户是在“某个业务项目里要不要自己写参数模块”这个语境下提问时，优先按下面顺序回答：

1. 先说明：`kx-biz-param` 就是参数业务统一封装包，目标是**简化业务代码**
2. 再说明：优先复用它提供的路由、服务与缓存语义
3. 只有在现有能力不够时，再讨论扩展 `kx-biz-param` 内部实现
4. 如果问题已经变成实体设计 / derive(Sea) 模板 / 通用 web 模板，再 handoff 到对应 skill

## 其他项目接入示例

```toml
[dependencies]
kx-biz-param = { version = "0.1", registry = "hekx" }
```

> 注意：Cargo 字段是 `registry`，不是 `registery`。

最小接入思路：

```text
1. 依赖里引入 kx-biz-param
2. 启动时调用 ParamInstall::migrate() 完成参数模块迁移
3. 路由里挂载 ParamRouter::apis() 复用通用接口
4. 业务侧优先复用现有 param / dic / i18n / key_i18n 能力
```

## 下游项目完整接入模板

### 1. Cargo.toml

```toml
[dependencies]
kx-biz-param = { version = "0.1", registry = "hekx" }
```

### 2. install / 启动初始化

```rust
use anyhow::Result;
use kx_biz_param::install::ParamInstall;

pub async fn install_bizs() -> Result<()> {
    ParamInstall::migrate().await?;
    Ok(())
}
```

### 3. router 挂载

```rust
use kx_axum::axum::Router;
use kx_biz_param::router::ParamRouter;

pub fn apis() -> Router {
    Router::new().nest("/param", ParamRouter::apis())
}
```

### 4. 使用建议

```text
- 先接入统一迁移与统一路由
- 再复用现有参数、字典、国际化能力
- 只有现有封装不能满足需求时，再扩展 kx-biz-param 内部
```

## 当前模块的真实结构心智图

```text
kx-biz-param/
├── src/cache/
│   ├── dic_cache.rs      # 字典缓存、批量保存、缓存清理
│   └── param_cache.rs    # 参数缓存 trait，挂在 KxParam 上
├── src/ctl/
│   ├── dic.rs            # 字典接口
│   ├── i18n.rs           # locale JSON 国际化接口
│   ├── key_i18n.rs       # key + lang 国际化接口
│   └── param.rs          # 系统参数接口
├── src/dto/
│   └── i18n_dto.rs       # 国际化保存请求
├── src/svc/
│   ├── dic_svc.rs        # 字典写入、排序、删除、缓存刷新
│   ├── i18n_svc.rs       # locale JSON 国际化业务
│   ├── key_i18n_svc.rs   # key + lang 国际化聚合
│   └── param_svc.rs      # 参数写入、删除、缓存刷新
├── src/router.rs         # 路由聚合
└── src/install.rs        # param 数据源迁移入口
```

## 最常用的落地套路

### 0. 在业务项目里直接复用这个 crate

优先回答：

```text
- 路由接入：复用 ParamRouter::apis()
- 安装/迁移：复用 ParamInstall::migrate()
- 参数读写：优先复用 ParamSvc / KxParamCache / KxParam 现有能力
- 字典与国际化：优先走 dic / i18n / key_i18n 现有子域，而不是在业务侧散落实现
```

### 1. 新增参数相关接口

优先判断是：

- 读取单个参数值 / 系统设置
- 保存参数值
- 删除参数
- 手工刷新缓存

规则：

```text
- 简单读取：可沿用 ParamCtl + ParamSvc / KxParam::get_param_value 现有模式
- 写入、删除：走 ParamSvc，并在成功后 refresh_cache
- 如果只是读写 JSON 值，不要额外发明新表，优先复用 kx_param.param_value
```

### 2. 新增字典相关接口

优先判断是：

- 查字典缓存
- 分页查编码 / 数据
- 保存单条字典数据
- 批量替换某个字典下的全部数据
- 拖拽排序
- 删除字典编码及其关联数据

规则：

```text
- 单条 / 批量写入都要清理对应 dic_code 的缓存 key
- 批量替换、排序调整、级联删除优先维持事务
- 字典展示顺序按 sort_no，不要漏掉 asc_sort_no()
```

### 3. 新增国际化相关接口

先分清两套存储：

```text
kx_i18n     = locale -> 一整棵 JSON 文案树
kx_key_i18n = (key, lang) -> 单条扁平翻译记录
```

选择建议：

```text
- 面向“某语言完整文案树”的接口，用 i18n
- 面向“按 key / lang 管理翻译键值”的接口，用 key_i18n
- 不要把两套模型混成一个接口层抽象，除非需求真的要做双向同步
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 明明可以直接复用 kx-biz-param，却在业务侧又手写一套参数、字典、国际化接口
❌ 明明已有统一路由入口，却在业务项目里复制粘贴 ctl 逻辑
❌ 改了参数值却忘了 refresh_cache，导致读到旧值
❌ 改了字典数据却没删 Redis key，导致缓存脏读
❌ 拖拽排序或批量替换时不用事务，导致 sort_no 或数据集不一致
❌ 看到仓库总原则里有 soft delete，就在这里机械补 is_del_eq(false)
❌ 把 i18n 与 key_i18n 混成同一套表意，回答时说不清各自适用场景
❌ 明明只是 kx-biz-param 的业务问题，却展开成通用 SeaORM / web 层大而全教程
```

### 正确做法

```text
✅ 先判断现有 kx-biz-param 是否已经能直接复用，从而简化业务代码
✅ 先定位需求属于 param / dic / i18n / key_i18n 哪个子域
✅ 读查询优先复用现有 ctl 风格，写逻辑与失效控制优先下沉到 svc/cache
✅ 涉及缓存就明确写出失效动作
✅ 涉及排序、批量替换、级联删除就优先保持事务边界
✅ 按模块实际字段结构回答：这里常用的是 state 过滤，而不是软删字段
✅ 超出 kx-biz-param 边界时，明确 handoff 到 kx-sea-orm / kx-axum-web / kx-rs
```

## 输出模板

默认按这个结构输出：

```text
问题归类
- param / dic / i18n / key_i18n

推荐落点
- 优先修改的 ctl / svc / cache / dto / router / install 文件

关键约定
- 当前问题必须遵守的 3~6 条模块规则

实现顺序
- 最短落地步骤，尤其说明是否需要事务与缓存失效

验证方式
- 最小必要 cargo check / cargo test 或模块级验证

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
我在一个 kx-rs 业务项目里，不想自己再写参数接口了，能不能直接复用 kx-biz-param 来统一处理参数和路由？
```

**Output direction**

```text
- 识别为“复用参数业务统一封装包”场景，命中 kx-biz-param。
- 先说明 kx-biz-param 的目标就是统一参数相关操作与通用路由，优先复用而不是重写。
- 指向 ParamRouter::apis()、ParamInstall::migrate() 以及 param / dic / i18n / key_i18n 四个子域。
- 只有在现有封装不够时，再继续定位应扩展 ctl / svc / cache 哪一层。
```
