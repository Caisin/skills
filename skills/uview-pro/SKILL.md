---
name: uview-pro
description: Comprehensive knowledge of uView-Pro UI framework for Vue3 + TypeScript + uni-app
---

# uView-Pro Skill

uView Pro 是基于 Vue3 和 TypeScript 的高质量 uni-app 组件库，提供 80+ 精选 UI 组件、便捷工具和常用模板，全面支持多端开发（微信小程序、H5、支付宝小程序、百度小程序、头条小程序、QQ 小程序等）。

## When to Use This Skill

触发此技能的场景：

- **组件开发**: 使用 uView-Pro 组件（ActionSheet、AlertTips、Avatar、Badge、Button、Calendar、Card、Cell、Checkbox、Collapse、Waterfall 等）
- **工具函数**: 调用 uView-Pro 工具库（trim、deepClone、deepMerge、color、colorSwitch 等）
- **样式配置**: 使用 ConfigProvider 全局配置、Color 色彩系统
- **表单处理**: 实现表单组件（Checkbox、Slider、Calendar 等）
- **布局组件**: 使用 Card、Cell、Collapse 等布局组件
- **反馈组件**: 使用 LoadingPopup、AlertTips 等反馈组件
- **导航组件**: 使用 BackTop 等导航组件
- **数据展示**: 使用 Waterfall 瀑布流、Badge 徽标、Avatar 头像等
- **问题排查**: 调试 uView-Pro 相关代码
- **最佳实践**: 学习 uView-Pro 推荐的开发模式

## Key Concepts

### 框架特性

- **Vue3 + TypeScript**: 完整的类型支持，提供类型定义文件
- **多端兼容**: 支持 App、H5、微信/支付宝/百度/头条/QQ 小程序
- **组件化**: 80+ 高质量组件，开箱即用
- **工具库**: 挂载在 `$u` 对象下的实用工具函数
- **安全区适配**: 针对 iPhone X 等全面屏机型的底部安全区适配

### 工具库调用方式

uView-Pro 的工具函数挂载在 `$u` 对象下，有两种调用方式：

1. **在 script 中**: 使用 `uni.$u.xxx` 或导入 `$u`
2. **在 template 中**: 直接使用 `$u.xxx`（需先导入）

## Quick Reference

### 1. 工具函数基础用法（官方文档）

```js
// 方式1: 通过 uni.$u 调用
console.log(uni.$u.trim(' abc '));  // 去除两端空格

// 方式2: 导入 $u 后调用
import { $u } from 'uview-pro'
console.log($u.trim(' abc '));  // 去除两端空格
```

### 2. 在模板中使用工具函数（官方文档）

```html
<template>
  <view>
    去除所有空格：{{$u.trim(str, 'all')}}
  </view>
</template>

<script setup lang="ts">
  import { $u } from 'uview-pro'
</script>
```

### 3. ActionSheet 操作菜单基础用法（官方文档）

```html
<template>
  <view>
    <u-action-sheet :list="list" v-model="show"></u-action-sheet>
    <u-button @click="show = true">打开ActionSheet</u-button>
  </view>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { ActionSheetItem } from 'uview-pro/types/global'

  const list = ref<ActionSheetItem[]>([
    {
      text: '点赞',
      color: 'blue',
      fontSize: '28rpx',
      subText: '感谢您的点赞'
    },
    {
      text: '分享'
    },
    {
      text: '评论'
    }
  ])

  const show = ref(false)
</script>
```

### 4. ActionSheet 带提示信息和取消按钮（官方文档）

```html
<template>
  <u-action-sheet
    :list="list"
    v-model="show"
    :tips="tips"
    :cancel-btn="true"
  ></u-action-sheet>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { ActionSheetTips, ActionSheetItem } from 'uview-pro/types/global'

  const tips = ref<ActionSheetTips>({
    text: '在水一方',
    color: '#909399',
    fontSize: '24rpx'
  })

  const list = ref<ActionSheetItem[]>([
    {
      text: '点赞',
      color: 'blue',
      fontSize: '28rpx'
    }
  ])

  const show = ref(true)
</script>
```

### 5. ActionSheet 点击事件处理（官方文档）

```html
<template>
  <u-action-sheet
    :list="list"
    @click="handleClick"
    v-model="show"
  ></u-action-sheet>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { ActionSheetItem } from 'uview-pro/types/global'

  const list = ref<ActionSheetItem[]>([
    { text: '点赞', color: 'blue', fontSize: '28rpx' },
    { text: '分享' },
    { text: '评论' }
  ])

  const show = ref(true)

  const handleClick = (index: number) => {
    console.log(`点击了第${index + 1}项，内容为：${list.value[index].text}`)
  }
</script>
```

### 6. Collapse 折叠面板基础用法（官方文档）

```html
<template>
  <u-collapse>
    <u-collapse-item :title="item.head" v-for="(item, index) in itemList" :key="index">
      {{item.body}}
    </u-collapse-item>
  </u-collapse>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

interface CollapseItem {
  head: string
  body: string
  open?: boolean
  disabled?: boolean
}

const itemList = reactive<CollapseItem[]>([{
  head: "赏识在于角度的转换",
  body: "只要我们正确择取一个合适的参照物乃至稍降一格去看待他人，值得赏识的东西便会扑面而来",
  open: true,
  disabled: true
}, {
  head: "生活中不是缺少美，而是缺少发现美的眼睛",
  body: "学会欣赏，实际是一种积极生活的态度，是生活的调味品，会在欣赏中发现生活的美",
  open: false,
}, {
  head: "周围一些不起眼的人、事、物，或许都隐藏着不同凡响的智慧",
  body: "但是据说雕刻大卫像所用的这块大理石，曾被多位雕刻家批评得一无是处",
  open: false,
}])
</script>
```

### 7. Collapse 控制初始状态和禁用（官方文档）

```html
<template>
  <u-collapse>
    <u-collapse-item
      :title="item.head"
      v-for="(item, index) in itemList"
      :key="index"
      :open="item.open"
      :disabled="item.disabled"
    >
      {{item.body}}
    </u-collapse-item>
  </u-collapse>
</template>
```

**说明**:
- `open` 参数控制面板初始是否打开
- `disabled` 参数为 `true` 时，面板保持初始状态，无法操作
- 默认为手风琴模式（打开一个，其他关闭），可通过 `accordion="false"` 允许多个面板同时打开

### 8. Waterfall 瀑布流基础用法（官方文档）

瀑布流组件利用 Vue 作用域插槽，将数据分为左右两列展示：

```html
<template>
  <u-waterfall v-model="flowList" :add-time="200" idKey="id">
    <template v-slot:left="{ leftList }">
      <view v-for="item in leftList" :key="item.id">
        <u-lazy-load :image="item.image">
          <view>{{ item.title }}</view>
        </u-lazy-load>
      </view>
    </template>

    <template v-slot:right="{ rightList }">
      <view v-for="item in rightList" :key="item.id">
        <u-lazy-load :image="item.image">
          <view>{{ item.title }}</view>
        </u-lazy-load>
      </view>
    </template>
  </u-waterfall>
</template>
```

**重要参数**:
- `v-model`: 双向绑定数据数组
- `add-time`: 单条数据添加到队列的时间间隔（ms），默认 200
- `idKey`: 数据唯一值的键名，默认 `id`

**组件方法**（通过 ref 调用）:
- `clear()`: 清空列表数据
- `remove(id)`: 移除指定 id 的数据

### 9. TypeScript 类型支持（官方文档）

uView-Pro 提供完整的 TypeScript 类型定义：

```typescript
import type {
  ActionSheetItem,
  ActionSheetTips
} from 'uview-pro/types/global'

// 使用类型定义
const list = ref<ActionSheetItem[]>([...])
const tips = ref<ActionSheetTips>({...})
```

### 10. 安全区适配（官方文档）

针对 iPhone X 等全面屏机型的底部安全区适配：

```html
<u-action-sheet
  :list="list"
  v-model="show"
  :safe-area-inset-bottom="true"
></u-action-sheet>
```

`safe-area-inset-bottom` 参数开启底部安全区适配，避免与指示条重合。

## Reference Files

此技能包含来自官方文档的综合参考资料（位于 `references/` 目录）：

### zh.md
**来源**: 官方中文文档
**置信度**: 中等
**页面数**: 140 页
**内容**:
- 完整的组件文档（ActionSheet、AlertTips、Avatar、AvatarCropper、BackTop、Badge、Button、Calendar、Card、Cell、Checkbox、CircleProgress、Collapse、ConfigProvider、CountDown、CountTo 等）
- 工具函数文档（color、colorSwitch、deepClone、deepMerge、trim 等）
- 使用指南（CustomIcon 扩展自定义图标库等）
- 平台差异说明
- API 参数详解
- 事件回调说明
- 完整代码示例

### llms.md
**来源**: 官方文档摘要
**置信度**: 中等
**内容**:
- 组件目录索引
- 快速导航链接
- 组件概览

### llms-full.md
**来源**: 官方文档完整版
**置信度**: 中等
**内容**:
- ActionSheet 操作菜单完整文档
- AlertTips 警告提示完整文档
- 包含详细的 API 说明、Props、Events、Slots
- 完整的使用示例和代码

### index.md
**来源**: 文档索引
**置信度**: 中等
**内容**:
- 文档分类导航
- 快速查找入口

## Working with This Skill

### 初学者入门

1. **从基础组件开始**: 先熟悉 Button、Cell、Badge 等简单组件
2. **学习工具函数**: 掌握 `$u` 工具库的调用方式（`uni.$u.xxx` 或导入 `$u`）
3. **理解 TypeScript 类型**: 使用 `uview-pro/types/global` 中的类型定义
4. **查看完整示例**: 参考 `references/zh.md` 中的代码示例

### 组件开发

1. **查找组件文档**: 在 `references/zh.md` 或 `llms.md` 中查找目标组件
2. **理解 Props 和 Events**: 查看组件的参数配置和事件回调
3. **参考代码示例**: 复制并修改官方示例代码
4. **注意平台差异**: 查看"平台差异说明"表格，确认目标平台支持情况
5. **TypeScript 支持**: 导入对应的类型定义，获得完整的类型提示

### 高级用法

1. **自定义插槽**: 使用组件的 slot 自定义内容（如 ActionSheet-item 的 default 插槽）
2. **作用域插槽**: 理解 Waterfall 等组件的作用域插槽用法
3. **组件方法调用**: 通过 ref 调用组件内部方法（如 Waterfall 的 `clear()` 和 `remove(id)`）
4. **全局配置**: 使用 ConfigProvider 进行全局主题配置
5. **安全区适配**: 在需要的组件上启用 `safe-area-inset-bottom`

### 问题排查

1. **检查平台兼容性**: 确认组件在目标平台是否支持
2. **查看 API 文档**: 确认参数名称、类型和默认值
3. **参考完整示例**: 对比官方示例代码，检查是否遗漏配置
4. **TypeScript 类型错误**: 确认导入了正确的类型定义
5. **事件回调**: 确认事件名称和回调参数格式

## Component Categories

### 操作反馈
- **ActionSheet**: 操作菜单，从底部弹出供用户选择
- **AlertTips**: 警告提示，展现需要关注的信息
- **LoadingPopup**: 加载弹窗，用于异步加载等待场景

### 数据展示
- **Avatar**: 头像展示
- **Badge**: 徽标数，用于消息提示
- **Card**: 卡片容器
- **Waterfall**: 瀑布流布局，左右两列展示

### 导航组件
- **BackTop**: 返回顶部按钮
- **Cell**: 单元格，常用于列表

### 表单组件
- **Button**: 按钮
- **Calendar**: 日历选择器
- **Checkbox**: 复选框
- **Slider**: 滑动选择器

### 布局组件
- **Collapse**: 折叠面板，手风琴效果
- **ConfigProvider**: 全局配置

### 进度指示
- **CircleProgress**: 圆形进度条
- **CountDown**: 倒计时
- **CountTo**: 数字滚动

### 工具函数
- **color**: 颜色值处理
- **colorSwitch**: 颜色转换
- **deepClone**: 对象深度克隆
- **deepMerge**: 对象深度合并
- **trim**: 字符串去空格

## Best Practices

### 1. TypeScript 类型安全

始终导入并使用 uView-Pro 提供的类型定义：

```typescript
import type { ActionSheetItem, ActionSheetTips } from 'uview-pro/types/global'
```

### 2. 工具函数调用

优先使用导入方式，避免全局依赖：

```typescript
import { $u } from 'uview-pro'
// 推荐
console.log($u.trim(' abc '))
// 而不是
console.log(uni.$u.trim(' abc '))
```

### 3. 组件 v-model 绑定

对于需要控制显示/隐藏的组件，使用 `v-model` 双向绑定：

```html
<u-action-sheet :list="list" v-model="show"></u-action-sheet>
```

### 4. 事件监听位置

注意事件监听的正确位置：
- Collapse 的 `change` 事件监听在 `<u-collapse>` 上
- Collapse-item 的 `change` 事件监听在 `<u-collapse-item>` 上

### 5. 安全区适配

在底部固定的组件上启用安全区适配：

```html
<u-action-sheet :safe-area-inset-bottom="true"></u-action-sheet>
```

### 6. 瀑布流性能优化

- 合理设置 `add-time` 参数（推荐 200ms）
- 结合 LazyLoad 懒加载组件使用
- 使用 LoadMore 组件实现分页加载

### 7. 异步关闭

对于需要异步操作的场景，使用 `async-close` 参数：

```html
<u-action-sheet :async-close="true"></u-action-sheet>
```

## Platform Support

uView-Pro 支持以下平台：

| 平台 | 支持情况 |
|------|---------|
| App | ✓ |
| H5 | ✓ |
| 微信小程序 | ✓ |
| 支付宝小程序 | ✓ |
| 百度小程序 | ✓ |
| 头条小程序 | ✓ |
| QQ小程序 | ✓ |

**注意事项**:
- 微信小程序中使用 LazyLoad 需要 HBuilderX 2.8.11+
- 支付宝小程序需要 HBuilderX 2.8.2+

## Resources

### 官方文档
- 官网: https://uviewpro.cn
- 组件文档: https://uviewpro.cn/zh/components/
- 工具函数: https://uviewpro.cn/zh/tools/

### 本地参考文件
- `references/zh.md`: 完整的中文文档（140 页）
- `references/llms.md`: 组件目录索引
- `references/llms-full.md`: 详细组件文档
- `references/index.md`: 文档导航索引

### 使用建议
1. 快速查找组件时，先查看 `llms.md` 获取组件列表
2. 需要详细 API 说明时，查看 `zh.md` 对应章节
3. 需要完整示例代码时，查看 `llms-full.md`

## Notes

- **文档来源**: 此技能从 uView-Pro 官方文档自动生成
- **类型支持**: 完整的 TypeScript 类型定义，位于 `uview-pro/types/global`
- **多端兼容**: 所有组件均支持 App、H5 和主流小程序平台
- **Vue3 生态**: 基于 Vue3 Composition API，使用 `<script setup>` 语法
- **代码示例**: 所有示例均包含语言标注，支持语法高亮
- **实时更新**: 参考文件保留了官方文档的结构和示例

## Updating

更新此技能的步骤：

1. 使用相同配置重新运行文档抓取工具
2. 技能将使用最新信息重新构建
3. 检查 `references/` 目录中的更新内容
4. 验证新增组件和 API 的文档完整性

## Common Issues

### 1. 组件不显示

**可能原因**:
- 未正确导入组件
- v-model 绑定的变量初始值不正确
- 平台不支持该组件

**解决方案**:
- 检查组件导入语句
- 确认 v-model 绑定的变量为布尔值
- 查看"平台差异说明"确认兼容性

### 2. TypeScript 类型错误

**可能原因**:
- 未导入类型定义
- 使用了错误的类型名称

**解决方案**:
```typescript
import type { ActionSheetItem } from 'uview-pro/types/global'
```

### 3. 工具函数调用失败

**可能原因**:
- 未正确导入 `$u`
- 在 script 中使用了 template 语法

**解决方案**:
```typescript
// 正确方式
import { $u } from 'uview-pro'
console.log($u.trim(' abc '))
```

### 4. 事件回调不触发

**可能原因**:
- 事件监听位置错误
- 事件名称拼写错误

**解决方案**:
- 确认事件监听在正确的组件上
- 参考文档确认事件名称（如 `@click` 而非 `@onClick`）

### 5. 瀑布流高度计算不准确

**可能原因**:
- 图片加载时机不确定
- `add-time` 参数设置过小

**解决方案**:
- 增大 `add-time` 值（推荐 200ms 以上）
- 结合 LazyLoad 组件使用
- 异步获取内容后调用 `init()` 方法重新计算高度

## Quick Command Reference

### 查看组件列表
```bash
# 查看所有可用组件
cat references/llms.md
```

### 搜索特定组件
```bash
# 搜索 ActionSheet 相关文档
grep -n "ActionSheet" references/zh.md
```

### 查看完整文档
```bash
# 查看完整的中文文档
cat references/zh.md
```

---

**版本**: 基于 uView-Pro 官方文档生成
**最后更新**: 2026-01-17
**文档来源**: https://uviewpro.cn
**技能类型**: UI 组件库 + 工具函数库
**支持框架**: Vue3 + TypeScript + uni-app
