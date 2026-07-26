---
name: prose
description: |
  Use when 编写或修改当前仓库的中文文档、README、rustdoc、设计文档、issue、PR 或提交正文。

  触发场景：
  - 新增或改写 Markdown / README
  - 编写公共 API rustdoc 或 doc test 说明
  - 润色 issue、PR、commit body 等人类可读文本

  触发词：文档、README、rustdoc、写作、润色、说明、prose、Markdown
---

# kx-rs Prose

仓库文本应直接、具体、可核实，默认使用中文描述当前行为。

## 适用边界

### 适用

- `docs/`、README 与贡献规范
- rustdoc、设计文档、issue、PR 和 commit body
- 修改代码时新增的用户可见说明

### 不适用

- 纯代码实现且不新增文本
- 翻译外部材料但不写入仓库

## Reference Selection

- 完整写作规则与例子
  - 读 `../../../docs/dev/WRITING.md`
- Rustdoc/doc test 专项规则
  - 读 `../../../docs/src/rustdoc-guidelines.md`
- 快速替换模式
  - 读 `references/patterns.md`

## 核心规则

1. 先写对象、行为和边界，不用评价词代替事实。
2. 使用主动语态与现在时；只记录当前行为。
3. 默认中文，公共标识符、协议字段和命令保持原文。
4. 无法在仓库核实的内容明确标为假设或“下游业务仓库约定”。
5. 代码示例按文档表面选择可执行 doctest、`no_run`、`ignore` 或明确的示意代码。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ “这个关键组件提供了强大且无缝的能力”
❌ “系统现在新增了……”并叙述无关历史
❌ 用本机绝对路径或真实凭据做示例
```

### 正确做法

```text
✅ 写清类型、方法、输入输出和失败语义
✅ 用仓库相对路径与可执行命令支撑说明
✅ 将未知、推断与已验证事实分开
```

## 输出模板

```text
对象与用途
当前行为
边界/限制
使用示例
验证方式
```

## 完整示例

**Input**

```text
给这个公共 trait 补一段 rustdoc。
```

**Output direction**

```text
- 说明 trait 解决的问题和调用边界
- 对不直观的状态/错误语义补充说明
- 能稳定运行时加入可执行 doc test
```
