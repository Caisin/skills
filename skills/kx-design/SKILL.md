---
name: kx-design
description: |
  Use when 需要为 KX 仓库的非平凡工程变更编写或评审设计，覆盖公共 API、跨 crate 边界、SeaORM 2 Schema、
  数据源、事务、安全、兼容性、分阶段实施和验证计划。
---

# 设计 KX 工程变更

设计文档统一放在 `docs/dev/design/`。单一、可独立评审的功能从
`docs/dev/design/_template.md` 创建 `docs/dev/design/<feature-name>.md`；先写用户可观察行为和
运行约束，再写会影响正确性的模块边界。

设计文档默认使用中文。协议字段、代码符号、CLI 命令、API path、数据库对象名和稳定错误码保持
原文，不为中文表达改名。UI、品牌、Logo、Banner 和视觉资产设计使用 UIRO 的 `design`，不使用
本 skill。

触发场景包括公共 API 或 derive/codegen 契约变化、Schema 与事务调整、安全或第三方协议边界、
跨 crate 架构调整，以及需要分阶段交付的业务迁移。局部 bug 修复、纯测试补充、文字纠错和无
可观察行为变化的内部重构通常不需要设计文档。

触发词：KX 工程设计、设计文档、架构设计、API 设计、Schema 设计、迁移方案、事务设计、兼容性方案。

## 大型功能设计

当变更跨越多个业务流程、crate 或数据源，同时包含后端和多个前端，联动修改 Schema、启动组合
或安全边界，或者无法在一个可评审迭代中实现并验收时，不把所有内容塞进单个文档。使用独立目录
保存总览和有顺序的阶段文档：

```text
docs/dev/design/<feature-name>/index.md
docs/dev/design/<feature-name>/01-<stage>.md
docs/dev/design/<feature-name>/02-<stage>.md
...
```

同一功能不能同时存在 `<feature-name>.md` 和 `<feature-name>/index.md`。`index.md` 是用户范围、
架构、全局不变量、兼容性、安全边界、阶段顺序和阶段链接的唯一决策入口。表、字段和 API 的完整
规格移入阶段文档后，总览只保留跨阶段约束，不重复整份明细。

### 执行进度

大型设计的 `index.md` 必须包含可在会话中断后继续使用的执行进度：

- 链接所有编号阶段，并标明 `待开始`、`进行中`、`已完成` 或 `阻塞`；
- 同一时间最多一个阶段为 `进行中`；
- 记录最近通过验收的阶段及其具体验证证据；
- 记录当前恢复点，包括下一动作、已知阻塞和必要的文件或命令；
- 用简短日期日志记录阶段开始、验收、重开和范围变化。

只有阶段退出条件和必需验证全部通过后，才使用 `- [x]`。`待开始`、`进行中` 和 `阻塞` 都使用
`- [ ]` 并显式写出文字状态。设计文档写完不等于实现完成。开始实现、完成重要里程碑、准备中断
和阶段验收时都要更新进度。

### 阶段文档

每个阶段文档必须说明：

- 目标、前置条件、纳入范围和明确延后的行为；
- 本阶段负责的 crate、模块和共享文件；
- 公共 API、DTO、entity、Schema、索引和数据兼容变化；
- `ctl -> svc -> entity/alias` 调用路径，以及单库或多数据源事务边界；
- 安全、初始化、迁移、前端和失败行为中与本阶段有关的变化；
- 聚焦测试、workspace 检查、必要的 DDL 审查和可观察退出条件；
- 本阶段验收后解除阻塞的下一阶段。

### 实现泳道

阶段足够大且适合并行实现时，增加“实现泳道”章节。先列前置门禁，再拆分相互独立的后端、前端、
测试、迁移和文档泳道。每个泳道必须写明：

- 独占修改的文件或模块；
- 只读依赖和已接受契约；
- 预期产物；
- 合并与验证门禁。

crate 根、聚合 router、安装入口、workspace manifest、生成 API 类型和总览进度表等共享文件只交给
一个集成负责人。只有能从同一已接受契约开始，且不依赖其它泳道尚未提交的 API 或 Schema 时，
才标记为并行。

大型前后端功能必须单列最终联合验证泳道，写明后端启动命令、前端 build/dev 命令、测试数据或
初始化前置条件、API 契约检查和可观察端到端流程。各泳道单独编译通过不能替代联合验证。

### 阶段顺序和后续扩展

除非总览明确证明阶段相互独立，否则实现按编号串行推进。前一阶段的退出条件、测试、Schema 审查
或文档同步未完成时，不能开始后一阶段；每个阶段结束时保持 workspace 可构建。

评审可以拆分、合并、插入或删除尚未开始的阶段，但必须同时更新链接、依赖、进度表和恢复点。
阶段一旦进入 `进行中`、`阻塞` 或 `已完成`，不得重编号或改写已接受历史。后续扩展在原目录追加
新的编号阶段；如果改变已完成行为，新增明确说明取代关系和回归覆盖的阶段。

## 必需分析

设计前根据实际改动逐项判断，不适用时明确说明原因：

- 定位拥有该能力的 crate，以及消费它的聚合 crate、binary、SDK 和前端；不把业务能力放回无关
  的框架 crate。
- 定义用户能调用的 API、默认值、错误语义、状态变化和兼容迁移方式。
- HTTP 变更说明 DTO、`ctl -> svc` 调用、`ApiRouter + ApiMeta`、稳定 API code、权限和明文/加密
  策略；分页分别使用 `QsQuery<条件>` 与 `QsQuery<Paging>`。
- SeaORM 2 变更说明 entity 所属功能子目录、表名、字段、类型、主键、relation、JSON、软删、表/字段
  `comment`、唯一约束和联合索引。
- 业务 entity 使用 `#[sea_orm::model]` 和 `model_attrs(derive(Sea))`；查询、局部更新和 upsert 优先
  使用生成的实体 alias，不设计冗长全路径调用。
- 每个业务数据源在所属 crate 通过 `ext_db_trait!` 声明；说明 alias 对应的数据源和安装顺序，不要求
  注册到 `crates/sea-orm/src/lib.rs`。
- Schema 安装统一由 `XxxInstall::migrate()/migrate_with()` 暴露。缺失对象和备注同步使用
  `sync_schema_with_comments()`；联合普通索引、类型修改、删除和已有约束调整使用明确的安装或迁移
  步骤，不在 `prelude.rs` 重复入口。
- 单数据源多表写入使用 `SeaTrans` 定义原子边界；多数据源只承诺显式顺序和 best-effort 补偿，
  不宣称跨库原子事务。
- 并发写入说明幂等键、CAS、version、lease、fencing、outbox 和影响行数检查；不可变流水、审计、
  安全事件和账本使用 insert，不用 upsert 覆盖。
- 涉及启动组合时说明 binary 子命令、配置、install、serve、route catalog、task registry 和 provider
  注入顺序；不受影响时不强制展开整套启动流程。
- 涉及前端时分别列出 PC、H5、小程序的页面、API、权限、资源、上传和构建验证；框架升级优先修改
  业务页面适配公开 API，不新增旧页面兼容层。
- 验证优先从目标 crate 和 SQLite 集成测试开始，再按影响面扩展到 workspace、doc test、mdBook、
  前端 typecheck/test/build 和必要的真实数据库或外部 provider 验证。
- 列出需要同步的 rustdoc、mdBook、README、skill、设计状态和 `docs/long-term-memory.md`。

## Schema 与发布边界

Schema Registry 同步只承担声明式能力已覆盖的安全变更，不能把它当成任意生产数据迁移工具。设计
涉及类型变更、删表删列、重命名、约束替换或存量数据回填时，必须给出显式步骤、DDL 审查、备份、
失败恢复和多数据库差异。SQLite 可以作为集成验收基线，但不能替代目标 MySQL/PostgreSQL 环境中
特有 DDL 与并发语义的部署前验证。

SeaORM 业务设计不得重新引入 Toasty、`TcMgr` 或 baseline。密钥、token、证书和环境专用配置始终
放在版本库外。

## 设计与实现边界

只调用 `$kx-design` 时，工作在设计文档、独立评审和用户明确要求的设计提交完成后停止，不因设计
存在而自动修改业务代码。用户在同一请求中明确要求“设计并实现”时，先接受设计和阶段门禁，再按
总览顺序进入实现；实现发现全局决策变化时，先更新总览和受影响阶段。

## 常见错误与正确做法

```text
❌ 用文件清单代替用户行为、错误语义和兼容契约
❌ 把大型迁移写成一个没有阶段状态和恢复点的长文档
❌ 把 Schema Registry sync 当作任意生产数据迁移工具
❌ 把 SeaTrans 描述成跨数据源原子事务
❌ 只验证各端独立 build，不设计前后端联合验收
✅ 总览维护全局不变量和阶段进度，阶段文档维护可验收规格
✅ 明确业务 crate、entity alias、install、事务和 API catalog 的所有权
✅ 每个阶段结束保持 workspace 可构建，并记录真实验证证据
```

## 输出

完成后报告：

```text
设计文档路径
用户可观察变化
关键不变量与兼容边界
阶段顺序与当前恢复点
开放问题
验证与验收计划
```

## 完整示例

**输入**

```text
为一个同时修改 auth、asset、PC 管理端和小程序的会员迁移写设计，要求分阶段实施并支持中断恢复。
```

**设计方向**

```text
docs/dev/design/membership-migration/index.md
docs/dev/design/membership-migration/01-contract-and-inventory.md
docs/dev/design/membership-migration/02-entities-and-install.md
docs/dev/design/membership-migration/03-services-and-transactions.md
docs/dev/design/membership-migration/04-http-and-frontends.md
docs/dev/design/membership-migration/05-integration-verification.md
```

总览固定用户契约、全局不变量、阶段状态、最近验收证据和恢复点。entity 阶段说明业务 crate alias、
表字段备注、联合索引、`install.rs` 与存量数据迁移；service 阶段说明 `SeaTrans`、幂等和跨数据源
补偿；HTTP 与前端阶段说明 `ApiRouter`、权限以及 PC/小程序契约；最终阶段使用 SQLite 集成测试、
目标 crate 检查、前端 typecheck/test/build 和登录后核心流程完成联合验收。
