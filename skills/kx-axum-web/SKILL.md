---
name: kx-axum-web
description: |
  Use when 任务明确聚焦 web 层的 ctl/router/install 写法，使用 `kx-axum` crate 组织接口，并结合 `kx-sea-orm` 生成的 Query / ModifyModel 等结构体。

  触发场景：
  - 需要写 `ctl/` handler、`router.rs` 路由收口、`install.rs` 装配或 `bins/*` 入口
  - 需要使用 `kx_axum::{R, AxumErr, Json, ext::QsQuery}` 组织 web 接口
  - 需要示范基于 `*Qry`、`*ModifyModel` 的列表、分页、保存、删除接口
  - 需要使用 `ApiRouter` / `ApiMeta` 同时声明路由、安全策略和权限 code

触发词：kx-axum、web层、ctl、router、install、bin、main.rs、cfg.toml、handler、AxumErr、QsQuery、Json、Path、ApiRouter、ApiMeta、接口层、路由、分页接口
---

# kx-axum-web

`kx-axum-web` 是当前仓库里专门给 **web 层 / 接口层** 写法提供模板的 skill。
它聚焦 `kx-axum` crate 的 `ctl/`、`router.rs`、`install.rs`、`bins/*` 入口、extractor、统一返回结构，以及如何配合 `kx-sea-orm` 自动生成的 `Query / ModifyModel / Model` 做接口层开发。默认优先给**单工程 / 单 crate 的简单模板**；只有在大型工程里，才进一步拆成 `bins/* + bizs/* + ents/*` 多 crate 结构。

本 skill 的代码风格优先提炼自当前仓库已验证的两类模式：

- **业务模块风格**：`ctl/` 保持薄、`svc/` 收口事务与编排、`router.rs` 用 `nest()` 聚合、`install.rs` 做迁移入口
- **bin 入口风格**：`main.rs` 负责子命令分流、读取配置、完成 `ApiRouter::finish()` 并调用 `run_registered` 启动
- `crates/axum/` 暴露的统一返回、extractor、注册式 Router 与 API catalog 能力
- `kx-sea-orm` 提供的 `Query / ModifyModel / Model` codegen 能力

## 适用边界

### 适用

- 需要写 `ctl/` handler
- 需要写 `router.rs` 路由聚合 / `nest()` 收口
- 需要写 `install.rs` 模块安装或迁移入口
- 需要写 `bins/*/src/main.rs`、`cfg.toml` 的启动与装配示例
- 需要写 `Result<R<T>, AxumErr>` 风格接口
- 需要基于 `*Qry`、`*ModifyModel` 写 page/list/save/get/del
- 需要为默认、公开、仅认证、明文或第三方回调路由声明安全策略

### 不适用

- 重点是实体、迁移、通用 CRUD、事务、多数据源、多表操作模板
  - 交给 `kx-sea-orm`
- 重点是 `bins/` / `bizs/` / `ents/` 项目分层与目录规划
  - 交给 `kx-rs`
- 纯 Rust 编译器 / Send / Sync / lifetime 问题
  - 交给 `rust-router`
- 纯 `sdks/` 第三方接入
  - 交给 `kx-sdk` / `kx-sdk-aigc`

## Reference Selection

按任务类型优先读取：

- web 层常用模板
  - 读 `references/patterns.md`
- 想确认 `kx-axum` 提供了哪些基础能力
  - 读 `references/kx-axum-map.md`
- 想确认 `*Qry` / `*ModifyModel` 这些结构体从哪里来
  - 对照 `../kx-sea-orm/references/codegen-map.md`
- 还需要看实践层完整目录边界
  - 切 `kx-rs`

## 核心规则

1. **控制器保持薄**
   - `ctl/` 负责收参、调用 service、返回 `Result<R<T>, AxumErr>`。
   - 复杂事务、多表组装、关联写入优先下沉到 `svc/`。
2. **优先复用 `kx-axum` 导出的类型**
   - 常见入口：`R`、`AxumErr`、`Json`、`extract::Path`、`ext::QsQuery`、`ApiRouter`、`ApiMeta`。
3. **查询 / 保存优先接 `kx-sea-orm` 自动生成结构体**
   - 列表 / 分页优先 `*Qry`
   - 保存优先 `*ModifyModel`
   - 读取返回优先 `Model`
4. **默认返回统一包装**
   - handler 签名优先 `Result<R<T>, AxumErr>`
   - 不要在业务接口里随意返回裸 `Json<T>` 或裸 `Vec<T>`
5. **router 与 handler 保持同一 `impl XxxCtl` 习惯用法**
   - 这样便于在同一控制器内集中维护路由和 handler。
6. **业务路由默认使用注册式 API**
   - 普通接口只写 `ApiMeta::new(code, summary)`，默认启用 KxEd、JWT 和 API code 权限。
   - 公开、仅认证、明文和第三方回调只通过 `public`、`auth_only`、`plaintext`、`external_callback` 显式降级对应维度。
   - `crud_api!` 已删除；CRUD handler 显式声明，复杂校验、事务和多表拼装继续下沉到 `svc/`。
7. **简单模板优先，复杂模板后置**
   - 默认先给单工程 / 单 crate 模板：`ents/` 放模型，`main.rs` 放启动与路由装配。
   - 只有用户明确是大型工程、需要分层协作或多个独立模块时，再推荐 `bins/* + bizs/* + ents/*` 多 crate 结构。
8. **安装入口与迁移入口分开理解**
   - `router.rs` 负责路由聚合
   - `install.rs` 负责模块迁移 / 初始化
   - 具体实体迁移模板本身交给 `kx-sea-orm`

## 推荐回答顺序

1. 先判断用户要的是单工程简单模板，还是大工程分 crate 模板
2. 再判断用户要的是 `ctl/`、`router.rs`、`install.rs`、`bins/*` 入口，还是整套 web 模块
3. 再从 `references/patterns.md` 摘对应模板
4. 如果用户追问 `R` / `AxumErr` / `ApiRouter` / `QsQuery` 的来源，再补 `references/kx-axum-map.md`
5. 如果问题已经变成实体/迁移模板，直接 handoff 到 `kx-sea-orm`

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把事务、多表写入、复杂组装全部塞进 ctl/
❌ 不复用 *Qry / *ModifyModel，手写一堆重复 DTO
❌ 接口层直接返回裸类型，不走 R<T> / AxumErr
❌ 返回原生 Router，导致 code、备注和安全策略继续分散维护
❌ 明明在问实体/迁移模板，却继续停留在 web 层 skill 里回答
```

### 正确做法

```text
✅ ctl/ 保持薄，复杂逻辑下沉到 svc/
✅ page/list/save 优先接 *Qry / *ModifyModel / Model
✅ 统一返回 Result<R<T>, AxumErr>
✅ CRUD handler 显式声明，路由统一使用 ApiRouter + ApiMeta，复杂逻辑放 ctl + svc
✅ 一旦问题下钻到 SeaORM 模型/迁移/事务模板，直接切到 kx-sea-orm
```

## 输出模板

默认按这个结构输出：

```text
问题归类
- ctl / router / install / web 模块

推荐落点
- 优先修改的文件或目录

关键约定
- 当前回答必须强调的 3~6 条 web 层规则

最小代码骨架
- 可直接照抄的 handler / router / install 模板

验证方式
- 最小必要 cargo check / cargo test

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
给我一个 kx-axum 的 web 层模板：包含 ctl、router、install，列表和保存接口直接复用 Query/ModifyModel。
```

**Output direction**

```text
- 先明确这是 kx-axum-web 命中的 web 层模板场景。
- 默认先给单工程 / 单 crate 模板；如果用户明确是大工程，再补 bins/bizs/ents 分 crate 模板。
- 再给 ctl/page/save 模板、router.rs 聚合、install.rs 迁移入口，以及可选的 bins/main.rs / build.rs / cfg.toml 启动模板。
- 强调 Query/ModifyModel 来自 kx-sea-orm 生成能力。
- 如果用户继续追问实体或迁移本体怎么写，再切到 kx-sea-orm。
```
