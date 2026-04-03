---
name: kx-rs
description: |
  Use when 任务已经明确进入 kx-rs 实践层开发，或需要从实践层问题回溯框架源码入口。

  触发场景：
  - 讨论 bins/bizs/ents 的组织与 CRUD 落地
  - 调整 svc/ctl/router/install 的职责分层与装配顺序
  - 调整 ctl/router 以兼容 openapi-scan
  - 需要判断实践层问题该回看 derives/crates/sdks/tools 的哪里

  触发词：bins、bizs、ents、CRUD、控制器、路由、Service、OpenAPI、openapi-scan、install、实践层
---

# kx-rs

`kx-rs` 是实践层开发专用 skill。
它负责指导**下游业务仓库约定**下的 `bins/` / `bizs/` / `ents/` 分层落地，以及在需要时指出应回看的框架源码目录。

> 注意：当前工作区没有 `bizs/` 或 `bins/`，相关结构应明确标注为“下游业务仓库约定”，不要说成当前仓库事实。

## 适用边界

### 适用

- 新建实践层项目骨架
- 编写 `bizs/`、`bins/` 的模块组织、装配与路由
- 规划 `svc/ctl/router/install/dto` 的职责边界
- 调整 ctl / router / handler 以兼容 `openapi-scan`
- 实践层写法遇到边界，需要回看 `derives/`、`crates/`、`sdks/`、`tools/`

### 不适用

- 纯 Rust 编译器 / trait / lifetime / Send / Sync 问题
  - 交给 `rust-router`
- 纯 bug、回归、测试失败排查
  - 交给 `systematic-debugging`
- 仍在讨论产品方案、任务拆分、重构计划
  - 交给 `brainstorming` 或 `writing-plans`
- 明确要的是 SeaORM / `#[derive(Sea)]` 六段式示例（模型、迁移、CRUD、事务、多数据源、多表）
  - 交给 `kx-sea-orm`
- 明确要的是 `get/sel/qry/m/update_set/auto_migrate` 这类实体/迁移模板
  - 交给 `kx-sea-orm`
- 明确要的是 `kx-axum` 的 ctl/router/install、extractor、`R<T>` / `AxumErr`、`crud_api!` 等 web 层模板
  - 交给 `kx-axum-web`
- 纯 `sdks/` 第三方接入与 SDK 风格问题
  - 交给 `kx-sdk`

## 任务分型与 reference 选择

| 任务类型 | 先读什么 | 结果应该聚焦什么 |
| --- | --- | --- |
| 新建实践层项目 / 模块骨架 | `references/project-skeleton.md` | 目录与安装顺序 |
| 日常 CRUD、控制器、服务、路由 | `references/crud-workflow.md` | svc/ctl/router/install 的落地顺序与职责边界 |
| `openapi-scan` 兼容性 | `references/openapi-scan.md` | 控制器/路由写法约束 |
| 不确定该回看哪个框架目录 | `references/source-navigation.md` | 源码回溯入口 |
| 明确要 SeaORM 模型 / 迁移 / CRUD / 事务模板 | 直接切 `kx-sea-orm` | 不在 `kx-rs` 里重复展开模板 |

必要时可读多份 reference，但只加载当前任务真正需要的部分。

## 最小落地顺序

每次命中后，按这个顺序处理：

1. 先判断是“实践层分层落地”还是“实践层分层落地 + 框架源码回溯”
2. 再选择最相关的 1~2 份 reference
3. 优先回答目录、模块边界、职责分配与装配顺序
4. 如果问题已下钻到 SeaORM 代码模板，明确 handoff 到 `kx-sea-orm`
5. 如果问题已经越过 `kx-rs` 边界，明确 handoff 到更合适的 skill

## 最常强调的边界

### 1. 实践层目录边界

```text
ents/* 负责实体、迁移、索引
bizs/* 负责 svc/ctl/router/install/dto
bins/* 负责装配、配置与运行入口
```

### 2. 控制器边界

```text
ctl/ 保持薄，只负责参数接收、调用 service、返回统一结果
不要把事务、多表组装、复杂业务校验塞进 ctl/
```

### 3. SeaORM 模板边界

```text
如果用户明确要模型定义、迁移、通用 CRUD、事务、多数据源或多表操作示例，直接告诉他使用 kx-sea-orm。
不要在 kx-rs 里重复展开 qry()/sel()/m()/auto_migrate() 的详细模板。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 明明在问实践层模块怎么拆，却直接展开整套 SeaORM 模型/迁移模板
❌ 把控制器、服务、装配顺序混在一起说，不区分 svc/ctl/router/install
❌ 明明是 practice 层问题，却直接钻进 derives/ 或 crates/ 全仓乱找
❌ 用户已经明确要 SeaORM 示例，却还停在 kx-rs 里含混回答
```

### 正确做法

```text
✅ 先回答 bins/bizs/ents、svc/ctl/router/install 该怎么落
✅ 先给最短分层路径，再按需补源码回溯入口
✅ 需要实体/迁移/query/update/事务代码模板时，明确引导去用 kx-sea-orm
✅ 只有实践层边界解释不清时，才回看框架源码目录
```

## 输出模板

默认按这个结构输出：

```text
问题归类
- 实践层问题 / 实践层 + 框架源码回溯

推荐落点
- 优先修改的目录、crate 或文件类型

操作步骤
- 最短落地顺序

关键边界
- 只补当前任务必须知道的 2~4 条分层规则

源码回溯入口
- 仅在需要回看框架源码时给出

下一步
- 一个具体起手动作
```

## 完整示例

**Input**

```text
我要在业务项目里新增一个用户管理模块，按 kx-rs 方式应该先建哪些目录和文件？
```

**Output**

```text
问题归类
- 这是实践层模块落地问题。

推荐落点
- 先看 references/project-skeleton.md 和 references/crud-workflow.md。
- 如果后续还要兼容 swagger/openapi，再补 references/openapi-scan.md。

操作步骤
- 先确定 ents/<ds> 放实体与迁移。
- 再确定 bizs/<biz> 的 svc/ctl/router/install/dto。
- 最后在 bins/<app> 做装配与入口接线。

关键边界
- ents/* 负责实体、迁移、索引。
- bizs/* 负责业务服务、控制器、路由和安装。
- bins/* 只负责装配和运行入口。
- 如果你接下来要我补 SeaORM 模型/迁移/事务代码模板，直接切到 kx-sea-orm。

下一步
- 先把模块目录骨架列出来，再决定要先写 svc 还是先接 router。
```
