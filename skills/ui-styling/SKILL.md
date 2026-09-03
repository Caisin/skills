---
name: ui-styling
description: |
  Use when 使用 shadcn/ui、Radix 与 Tailwind 构建可访问、响应式的产品界面或视觉工具。
  触发词：UI、shadcn、Radix、Tailwind、responsive、dark mode、canvas
argument-hint: "[component or layout]"
license: MIT
---

# UI Styling

## Reference Selection

- 组件/可访问性：`references/shadcn-components.md`、`shadcn-accessibility.md`
- 主题：`references/shadcn-theming.md`
- Tailwind：`references/tailwind-utilities.md`、`tailwind-responsive.md`、`tailwind-customization.md`
- Canvas：`references/canvas-design-system.md`

## 核心规则

1. 优先使用项目已有组件和 token；缺失时再用 shadcn CLI 或 `scripts/shadcn_add.py` 添加。
2. Radix 负责语义、键盘与焦点，Tailwind 负责布局和样式；不要破坏组件可访问状态。
3. 移动优先，稳定定义容器、网格、固定比例元素和溢出行为；不按视口宽度缩放字体。
4. 明暗主题使用语义 CSS variables，验证文本、边框、focus ring、disabled 和 error 对比度。
5. 图标按钮提供名称/tooltip；表单有 label、错误与 loading；弹层保持焦点圈闭和 Esc 行为。
6. Canvas 适合自定义可视化，不替代可访问的普通控件和文本内容。

## 工具

```bash
python3 scripts/shadcn_add.py <component>
python3 scripts/tailwind_config_gen.py
```

## 验证

在目标桌面/移动视口检查溢出、遮挡、键盘、焦点、对比度和真实交互；运行项目 typecheck、lint 和视觉截图。
