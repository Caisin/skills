---
name: pr
description: |
  Use when 为当前仓库编写、审查或创建 pull request，需要基于完整分支 diff 说明净改动与验证证据。

  触发场景：
  - 拟定 PR title 和 body
  - 审查 PR 描述是否覆盖真实 diff
  - 用户明确要求执行 gh pr create

  触发词：PR、pull request、合并请求、PR title、PR body、gh pr create
---

# kx-rs Pull Requests

PR 描述目标分支到当前 `HEAD` 的净改动，不描述某一次中间提交。

## 适用边界

### 适用

- 编写或审查 PR title/body
- 根据分支 diff 总结变更与风险
- 用户明确要求创建 PR

### 不适用

- 单个 commit message，应使用 `commit` skill
- 尚未完成或没有验证证据的实现收口

## Reference Selection

- PR 正文结构
  - 读 `../../../.github/pull_request_template.md`
- Title 规则
  - 读 `../../../docs/dev/COMMITS.md`
- 快速检查
  - 读 `references/patterns.md`

## 核心规则

1. 先确定 base branch，再读 `git diff <base>...HEAD` 与 `git log <base>..HEAD`。
2. Title 使用 Conventional Commits；PR title 不添加 Lore trailers。
3. Body 说明净改动、实际验证、公共 API/配置/Schema/安全/文档影响和 review 重点。
4. Markdown 为主的 PR 可在 Summary 顶部链接当前 head branch 的 GitHub 渲染页面。
5. 只有用户明确要求时才执行 `gh pr create`。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只复述最后一个 commit
❌ 将计划中的测试写成已经通过
❌ checklist 全部勾选但正文没有证据
```

### 正确做法

```text
✅ 基于 merge-base 后的完整 diff
✅ 区分已验证、未验证和依赖外部环境的项
✅ 明确 reviewer 应关注的边界与剩余风险
```

## 输出模板

```text
<type>(<scope>): <intent>

## 变更
...
## 验证
...
## 影响
...
## Review 重点
...
```

## 完整示例

**Input**

```text
根据当前分支帮我写 PR。
```

**Output direction**

```text
- 先识别 base branch 并检查完整 diff/log
- 从净改动拟定 title 与正文
- 未经用户明确要求，只输出草稿而不创建远端 PR
```
