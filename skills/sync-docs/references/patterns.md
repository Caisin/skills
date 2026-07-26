# Documentation Sync Patterns

用于把代码或 commit 范围映射到正确的文档表面。

## 变更映射

| 变更 | 优先检查 |
|---|---|
| 新增/修改公共 API | 源码 rustdoc、对应 `docs/src/crates/**` |
| crate/feature/目录变化 | `Cargo.toml`、`README.md`、`docs/src/SUMMARY.md`、crate inventory |
| Schema/迁移/一致性变化 | rustdoc、设计文档、长期记忆 |
| 新的稳定排障结论 | `docs/long-term-memory.md` |
| 协作规范变化 | `AGENTS.md`、`docs/dev/`、相关 skills |

## 推荐流程

```text
选范围 -> 筛用户可观察变化 -> 搜旧结论 -> 更新规范源 -> 构建/测试 -> 记录缺口
```

## 常见错误

```text
❌ 修改 docs/book/ 生成物
❌ 只追加新段落，不删除错误旧结论
❌ 同步文档时顺带重写无关章节
```

## 正确做法

```text
✅ 每个文档改动可追溯到代码或规范变化
✅ mdBook、rustdoc、设计和长期记忆职责分开
✅ 用对应工具验证对应文档表面
```
