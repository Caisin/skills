---
name: commit
description: |
  Use when 编写、审查或执行当前仓库的 Git commit，需要同时满足 Conventional Commits 与 agent Lore trailers。

  触发场景：
  - 用户要求提交当前改动
  - 需要拟定或审查 commit message
  - 需要判断 type、scope、breaking change 或验证 trailers

  触发词：commit、提交、提交信息、commit message、Conventional Commits、Lore trailer
---

# kx-rs Commit

在提交前读取 `docs/dev/COMMITS.md`，以该文件作为格式、type、scope 与 Lore trailers 的规范源。

## 适用边界

### 适用

- 编写或审查 commit message
- 用户明确要求执行 `git commit`
- 判断提交是否需要正文、breaking change 或 `Not-tested`

### 不适用

- PR title/body，应使用 `pr` skill
- 只查看工作区状态而不准备提交

## Reference Selection

- 完整规则与示例
  - 读 `../../../docs/dev/COMMITS.md`
- 快速决策模板
  - 读 `references/patterns.md`

## 核心规则

1. 先读完整 diff 与验证结果，再写 message；不从任务描述猜测实际改动。
2. 首行使用 `<type>(<scope>): <intent>`；scope 不清晰时省略。
3. agent 提交保留有价值的 Lore trailers，至少准确记录 `Tested` / `Not-tested`。
4. 不提交用户未要求纳入的文件，不覆盖已有用户改动。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只看最后一个文件或任务标题就写 commit message
❌ 用 chore 掩盖实际的 fix / feat / docs
❌ 没运行验证却写 Tested: all tests pass
```

### 正确做法

```text
✅ 基于暂存 diff 归纳主意图
✅ scope 优先使用稳定 crate 名或目录名
✅ 对未运行的验证用 Not-tested 明确说明
```

## 输出模板

```text
<type>(<scope>): <intent>

<必要的决策背景>

Constraint: ...
Confidence: high
Scope-risk: narrow
Tested: ...
Not-tested: ...
```

## 完整示例

**Input**

```text
把这次 skills 和文档规范迁移提交掉。
```

**Output direction**

```text
- 先检查 git status、暂存 diff 和实际验证结果
- 使用 docs(skills) 或最能代表净改动的 type/scope
- 在 Tested 中只写真实执行过的 skill 校验与文档构建
```
