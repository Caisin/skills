---
name: design
description: |
  Use when 需要在品牌、Logo、CIP、Banner、Icon、Slides 与社交图片之间选择并执行设计工作流。
  触发词：设计、品牌、Logo、CIP、banner、icon、slides、社交图片
---

# Design

这是设计任务路由器，详细规范按需读取 `references/`，不要一次加载全部资料。

## 路由

| 任务 | 入口 |
| --- | --- |
| 品牌声音、资产和一致性 | `brand` |
| Token 与组件规范 | `design-system` |
| 产品 UI | `ui-styling` / `ui-ux-pro-max` |
| Banner | `banner-design` |
| Slides | `slides` 与 `references/slides*.md` |
| Logo / CIP / Icon / 社交图片 | 对应 `references/*-design.md` |

## 核心规则

1. 先确认交付物、受众、平台、尺寸、品牌约束和参考，再选择工作流。
2. 品牌/产品/人物必须成为首屏主信号；需要观察实物时使用清晰真实或生成位图。
3. Logo/Icon 可使用矢量；照片型主体不以 SVG 插画替代。
4. 提供少量有明确差异的方向，选定后再展开完整套件。
5. 所有交付物都要渲染检查尺寸、文字、对比度、裁切和品牌一致性。

## 安全

不提交密钥，不伪造授权，不使用来源不明的品牌资产；外部生成工具的凭据只从环境读取。
