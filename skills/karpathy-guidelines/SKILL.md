---
name: karpathy-guidelines
description: |
  Use when writing, reviewing, or refactoring code and you need behavioral guardrails
  that reduce common LLM coding mistakes: overcomplication, silent assumptions,
  broad unrelated edits, and unverifiable completion claims.

  触发场景：
  - 编写、审查或重构代码时，需要先压住过度设计与猜测
  - 用户要求最小改动、保持现有行为、避免无关重构
  - 需要把任务转成可验证目标，并在完成前明确验证证据

  触发词：Karpathy、karpathy-guidelines、简单优先、最小改动、不要过度设计、surgical change、verification
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 适用边界

### 适用

- 写代码、改代码、review 代码前，需要先约束实现范围
- refactor / cleanup 时，需要避免顺手改无关代码
- bugfix 或功能开发需要转成明确可验证的成功条件
- 需求有多种解释时，需要先暴露假设和取舍

### 不适用

- 用户只要求纯信息查询、翻译或总结，且不涉及实现决策
- 需要完整产品探索或需求澄清时，应交给更强的规划 / interview 工作流

## 核心规则

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State assumptions explicitly. If uncertainty is material, ask.
- If multiple interpretations exist, present them instead of silently picking one.
- If a simpler approach exists, say so and prefer it.
- If something is unclear enough to change the solution, stop and name the ambiguity.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No configurability that was not requested.
- No error handling for impossible scenarios.
- If a 200-line change could be 50 lines, rewrite it smaller.

Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Do not improve adjacent code, comments, or formatting unless required.
- Do not refactor things that are not part of the request.
- Match existing style, even if you would do it differently.
- If you notice unrelated dead code, mention it instead of deleting it.

When your changes create orphans:

- Remove imports, variables, or functions that your change made unused.
- Do not remove pre-existing dead code unless asked.

Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → write tests for invalid inputs, then make them pass.
- "Fix the bug" → reproduce the failure, then make it pass.
- "Refactor X" → ensure behavior is protected before and after.

For multi-step tasks, keep a short plan:

```text
1. Step → verify: check
2. Step → verify: check
3. Step → verify: check
```

Strong success criteria let you loop independently. Weak criteria require clarification.

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 看到一个小 bug，却顺手重构整个模块
❌ 不确认关键假设，直接实现其中一种解释
❌ 为未来可能需求新增抽象、配置项或依赖
❌ 没有运行验证就声称已经完成
```

### 正确做法

```text
✅ 先列出会影响实现的假设和成功条件
✅ 选择能满足当前需求的最小改动
✅ 只清理本次改动制造出来的 unused / orphan
✅ 最后用测试、check、lint 或明确的人工检查证据收口
```

## 输出模板

```text
假设/边界
最小方案
改动范围
验证方式
剩余风险
```

## 完整示例

**Input**

```text
这个函数有个边界 bug，帮我修一下，但不要大改。
```

**Output direction**

```text
- 先说明会做最小复现和最小修复，不做无关重构
- 优先补一个覆盖边界的测试或定位已有测试
- 只修改导致 bug 的分支和本次改动产生的 unused
- 运行目标测试 / check，并报告验证证据与剩余风险
```
