# Commit Patterns

用于从实际 diff 与验证结果生成 kx-rs commit message。

## 决策顺序

1. `git status --short` 确认用户改动与本次改动。
2. 查看暂存 diff；没有暂存内容时不要假设提交范围。
3. 选择表达主意图的 type 和可选 scope。
4. 只记录有长期价值的正文与 trailers。

## 推荐模板

```text
fix(axum): preserve custom config during initialization

Constraint: legacy callers still read AppCfg from GlobalIns
Confidence: high
Scope-risk: narrow
Tested: rtk cargo test -p kx-axum
Not-tested: workspace tests; target crate verification was sufficient
```

## 常见错误

```text
❌ feat: update files
❌ Tested: tests pass（实际未运行）
❌ 将无关用户改动一并暂存
```

## 正确做法

```text
✅ 首行表达可维护的意图
✅ Tested/Not-tested 与命令输出一致
✅ Scope-risk 反映影响面而非 diff 行数
```
