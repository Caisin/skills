# KX Sea ORM Patterns

用于 `kx-sea-orm` 的 reference 导航页。

## 适用场景

- 需要先判断当前问题该看哪个 SeaORM 专题
- 需要在模型、迁移、CRUD、事务/多表之间快速切换
- 需要把数据库字段设计规范与示例模板分开阅读

## Reference Selection

| 任务类型 | 优先 reference | 关注点 |
| --- | --- | --- |
| 字段 / 主键 / 索引 / `is_del` 设计 | `schema-design.md` | 字段长度、类型、系统字段、主键、索引命名 |
| relation / loader / 禁用数据库外键 | `schema-design.md`、`sea-orm-2.md` | `BelongsTo`、`HasOne`、`HasMany`、`skip_fk` |
| 非破坏性 schema sync / 显式迁移 / 索引创建 | `migration.md` | `auto_migrate()`、`SchemaSyncConnection`、`create_index()` |
| 标准增删改查 | `crud.md` | `get/sel/qry/m/upsert/update_set` |
| 事务 / 多数据源 / 多表操作 | `transaction-and-multi-table.md` | `SeaTrans`、两段查询、跨库操作 |
| 生成能力来源解释 | `codegen-map.md` | dense entity + `derive(Sea)` 生成入口 |

## 推荐做法

```text
先判断问题是“设计规范”还是“代码模板”
-> 设计规范先看 schema-design.md
-> 代码模板按 migration/crud/transaction-and-multi-table 分流
-> 追问生成来源时再补 codegen-map.md
```

## 常见错误

```text
❌ 把所有主题堆在一个 reference 里，导致定位困难
❌ 一上来就贴完整长文，不先按问题分流
```

## 正确做法

```text
✅ 先按主题分流，再加载最小必要 reference
✅ 设计规范和代码模板分开维护
```
