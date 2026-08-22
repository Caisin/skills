---
name: issue
description: |
  Use when 为当前仓库编写或审查 bug report、feature proposal 或维护任务 issue。

  触发场景：
  - 报告可复现 bug
  - 提议公共 API 或非平凡功能
  - 把排障结果整理成可跟踪 issue

  触发词：issue、bug report、feature proposal、问题单、缺陷报告、功能提案
---

# kx-rs Issues

Issue 是可长期检索的问题或提案记录，应基于事实、复现和明确边界编写。

## 适用边界

### 适用

- 编写或审查 bug report
- 编写功能提案或维护任务
- 用户明确要求通过 `gh issue create` 创建 issue

### 不适用

- 直接实现已明确的小改动
- PR title/body，应使用 `pr` skill

## Reference Selection

- Bug 模板
  - 读 `../../../.github/ISSUE_TEMPLATE/bug_report.yml`
- 功能提案模板
  - 读 `../../../.github/ISSUE_TEMPLATE/feature_proposal.yml`
- 写作与内容模式
  - 使用 `prose` skill，读 `references/patterns.md`

## 核心规则

1. Bug report 先写操作、预期、实际结果、环境和最小复现，不把根因猜测当事实。
2. Feature proposal 先写问题，再写具体 API/行为方案、替代方案和影响范围。
3. 涉及公共 API、Schema、一致性、安全或跨 crate 调整时，指向 `kx-design` 流程。
4. 只有用户明确要求时才执行创建 issue 的外部副作用。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ “功能坏了，请修复”，没有复现与环境
❌ 先写大段根因推测，不写实际错误
❌ 功能提案只有方案，没有当前问题和替代方案
```

### 正确做法

```text
✅ 附最小失败测试、完整错误和 feature flags
✅ 区分证据、推断与待调查项
✅ 明确影响 crate、下游兼容性和设计文档需求
```

## 输出模板

```text
标题
问题/操作
预期行为
实际行为或建议方案
环境/影响范围
最小复现/替代方案
```

## 完整示例

**Input**

```text
kx-sea-orm 开启 sqlite feature 后测试失败，帮我整理 issue。
```

**Output direction**

```text
- 核实命令、错误输出、平台和 feature 组合
- 只报告可观察行为，根因单列为待调查
- 提供能复现失败的最短 cargo 命令
```
