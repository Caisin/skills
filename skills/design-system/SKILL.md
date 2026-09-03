---
name: design-system
description: |
  Use when 设计 token 架构、组件规范，或用统一 token 生成 HTML slides。
  触发词：design token、设计系统、组件规范、主题、slides、演示文稿
---

# Design System

## Reference Selection

- token 分层：`references/token-architecture.md`
- primitive/semantic/component：对应 `references/*-tokens.md`
- 组件状态：`references/component-specs.md`、`references/states-and-variants.md`
- Tailwind：`references/tailwind-integration.md`

## 核心规则

1. 使用 `primitive -> semantic -> component` 三层；组件不直接依赖任意色值或间距。
2. 语义 token 覆盖前景、背景、边框、状态、焦点和禁用态，并同时验证明暗主题。
3. 组件规范包含 anatomy、尺寸、状态、交互、键盘、ARIA 和内容边界。
4. 先扩展现有 token，再新增 primitive；禁止为单个页面复制一套近似变量。
5. Slides 使用 `data/*.csv` 和 `scripts/search-slides.py` 选择布局/图表，所有页面共享 token 源。

## 常用命令

```bash
node scripts/generate-tokens.cjs
node scripts/validate-tokens.cjs
python3 scripts/search-slides.py "query"
node scripts/slide-token-validator.py <html>
```

## 验证

检查 token 引用、对比度、响应式文本、组件状态和最终渲染；slides 还需逐页截图检查溢出和图表可读性。
