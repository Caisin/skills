---
name: ui-ux-pro-max
description: |
  Use when 设计、实现或评审 Web、移动端和桌面 UI，需要查询本地风格、配色、字体、图表与 UX 数据。
  触发词：UI、UX、界面设计、配色、字体、图表、无障碍、响应式、交互评审
---

# ui-ux-pro-max

本 skill 的价值是按需搜索本地数据，不把完整设计百科加载进上下文。

## Prerequisites

脚本只需 Python 3 标准库。缺失时说明限制，不自行安装系统软件。

## 查询流程

1. 识别产品类型、用户、平台、主任务、密度和品牌约束。
2. 新页面先生成 design system；局部问题只查对应 domain。
3. 根据技术栈补一次 stack 查询，再把结果映射到项目已有组件/token。

```bash
python3 scripts/design_system.py "<product keywords>" --format markdown
python3 scripts/search.py "<query>" --domain ux
python3 scripts/search.py "<query>" --stack vue
python3 scripts/validate_data.py
```

可查询 domain 和 stack 以脚本 `--help` 为准，不在主 skill 重复维护列表。

## 核心规则

- 工具型后台优先密度、扫描、比较和重复操作效率；内容/品牌页再强调叙事与视觉。
- 使用现有图标库；熟悉动作优先图标，陌生图标带 tooltip，不手绘替代已有图标。
- 控件类型匹配语义：布尔用开关/复选框，模式用 segmented，选项用 select/menu，数值用 input/slider。
- 不嵌套卡片，不用装饰性渐变球；主体内容和真实资产必须清晰可见。
- 文本不得溢出或遮挡；固定格式元素设置稳定尺寸、网格或 aspect ratio。
- 明暗主题均验证 WCAG 对比度、焦点、键盘、loading、empty、error 和 disabled 状态。
- 动效服务反馈与层级，并尊重 `prefers-reduced-motion`。

## 交付检查

检查主任务路径、响应式、滚动/弹层、真实数据长度、无权限与失败态；可运行时用浏览器截图和交互验证，不只看静态代码。
