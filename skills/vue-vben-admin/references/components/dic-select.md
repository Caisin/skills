# DicSelect & DicRadioGroup (kx-admin)

基于后端字典数据的选择组件，封装了 ApiComponent + 字典 API，自动加载字典选项、支持 i18n label、默认值自动选中。

## Table of Contents
- [DicSelect](#dicselect)
- [DicRadioGroup](#dicradiogroup)
- [字典数据结构](#字典数据结构)

---

## DicSelect

字典下拉选择器。内置 `showSearch`、`filterOption`、`allowClear`、`class: 'w-full'`。

### 在表单 Schema 中使用
```typescript
{
  component: 'DicSelect',
  fieldName: 'storage_type',
  label: '存储类型',
  componentProps: {
    params: { code: 'storage_type' },  // 字典编码
  },
}
```

### 带验证
```typescript
{
  component: 'DicSelect',
  fieldName: 'status',
  label: '状态',
  rules: 'required',
  componentProps: {
    params: { code: 'state' },
    placeholder: '请选择状态',
  },
}
```

### 在搜索表单中使用（带清除）
```typescript
{
  component: 'DicSelect',
  fieldName: 'state',
  label: '状态',
  componentProps: {
    allowClear: true,
    params: { code: 'state' },
  },
}
```

### 在 VxeTable 中作为渲染器
已注册为 VxeTable 渲染器 `CellDicTag`，可在列配置中使用：
```typescript
{
  field: 'storage_type',
  title: '存储类型',
  cellRender: { name: 'CellDicTag', props: { code: 'storage_type' } },
}
```

### 编程式使用（非表单场景）
```vue
<script setup>
import { DicSelect } from '#/adapter/component';
import { ref } from 'vue';

const val = ref();
</script>

<template>
  <DicSelect v-model:value="val" :params="{ code: 'state' }" />
</template>
```

### 默认内置属性
| 属性 | 默认值 | 说明 |
|------|--------|------|
| `api` | `getDic` | 字典数据加载 API |
| `autoSelect` | `dicAutoSelect` | 自动选中 `is_def=1` 的项 |
| `labelFn` | `dicLabelFn` | label 自动 `$t()` 国际化 |
| `showSearch` | `true` | 支持搜索 |
| `filterOption` | `FormFields.filterOption` | label+value 模糊匹配 |
| `allowClear` | `true` | 允许清除 |
| `class` | `'w-full'` | 默认全宽 |

---

## DicRadioGroup

字典单选按钮组。常用于状态切换等少量选项场景。

### 在表单 Schema 中使用
```typescript
{
  component: 'DicRadioGroup',
  fieldName: 'state',
  label: '状态',
  defaultValue: 1,
  componentProps: {
    params: { code: 'state' },
    buttonStyle: 'solid',
    optionType: 'button',
    class: 'w-full',
  },
}
```

### 快捷函数 vbenRadioGroup
`form-use` 中提供了预设的状态单选 schema 生成函数：
```typescript
import { vbenRadioGroup } from '@vben/kx-admin';

// 生成一个 state 字段的 DicRadioGroup schema
const stateSchema = vbenRadioGroup('state');
// 等价于:
// {
//   component: 'DicRadioGroup',
//   fieldName: 'state',
//   label: '参数状态',
//   defaultValue: 1,
//   componentProps: { params: { code: 'state' }, buttonStyle: 'solid', optionType: 'button', class: 'w-full' },
// }
```

### 默认内置属性
| 属性 | 默认值 | 说明 |
|------|--------|------|
| `api` | `getDic` | 字典数据加载 API |
| `autoSelect` | `dicAutoSelect` | 自动选中 `is_def=1` 的项 |
| `labelFn` | `dicLabelFn` | label 自动 `$t()` 国际化 |

---

## 字典数据结构

字典 API `getDic({ code })` 返回的数据格式：
```typescript
interface SystemDicData {
  label: string;   // 显示文本（支持 i18n key）
  value: any;      // 值
  is_def?: number; // 1=默认选中项
  // ...其他字段
}
```

`params.code` 对应后端字典编码，如 `'state'`、`'storage_type'`、`'db_type'` 等。
