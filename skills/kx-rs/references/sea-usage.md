# Sea Usage Handoff

用于“用户在 kx-rs 语境下问到了 SeaORM / `#[derive(Sea)]`，但问题其实已经进入 `kx-sea-orm` 边界”的场景。

## 什么时候直接切去 `kx-sea-orm`

出现这些问题时，不要继续在 `kx-rs` 里展开：

- 要一套模型定义示例
- 要迁移 / `auto_migrate()` 示例
- 要通用 CRUD 示例
- 要事务、多数据源或多表操作示例
- 要解释 `get()/sel()/qry()/m()/update_set()` 怎么写
- 明确要求**不要使用 SeaORM relation 做外键**

## 推荐说法

```text
这部分已经属于 kx-sea-orm 的职责边界。
如果你要的是 SeaORM / #[derive(Sea)] 的代码模板，我会直接按 kx-sea-orm 给你示例。
```

## 为什么不再在 kx-rs 里重复展开

```text
- kx-rs 现在聚焦 practice 层目录、svc/ctl/router/install 分层与源码回溯。
- kx-sea-orm 专门负责模型、迁移、CRUD、事务、多数据源、多表操作示例。
- 把两类内容拆开后，命中更准，也能避免在 kx-rs 里重复维护 SeaORM 模板。
```

## 常见错误

```text
❌ 用户已经明确要 SeaORM 模型/迁移/事务示例，还继续在 kx-rs 里给零散片段
❌ 明明需要 explain derive 生成能力，却只给 practice 层目录建议
❌ 同一套 SeaORM 模板在 kx-rs 和 kx-sea-orm 两边重复维护
```

## 正确做法

```text
✅ 先判断用户是在问 practice 层分层，还是在问 SeaORM 代码模板
✅ 一旦进入 SeaORM 模板边界，直接切到 kx-sea-orm
✅ kx-rs 只保留路由和分层上的 handoff 说明，不重复维护 SeaORM 示例
```
