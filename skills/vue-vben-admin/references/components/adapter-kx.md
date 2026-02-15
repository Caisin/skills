# kx-admin Adapter 扩展 (adapter/kx & adapter/form-use)

kx-admin 在上游 vben-admin adapter 基础上的扩展层，包含自定义组件注册、VxeTable 渲染器、表单 Schema 工具函数。

源码目录：
- `packages/kx-admin/src/adapter/kx/` — 组件注册 & VxeTable 渲染器
- `packages/kx-admin/src/adapter/form-use/` — 表单 Schema 工具函数

## Table of Contents
- [初始化流程](#初始化流程)
- [KxComponentType](#kxcomponenttype)
- [覆盖的上游组件](#覆盖的上游组件)
- [VxeTable 自定义渲染器](#vxetable-自定义渲染器)
- [form-use 工具函数](#form-use-工具函数)

---

## 初始化流程

`adapter/kx/init.ts` 导出 `initComponentAdapter()`，先调用上游初始化，再注册 kx 扩展组件：

```typescript
import { initComponentAdapter } from '#/adapter/kx/init';

// 在 app 启动时调用
await initComponentAdapter();
```

导出内容：
- `initComponentAdapter()` — 初始化函数
- `DicSelect` / `DicRadioGroup` — 字典组件（可直接 import 使用）
- `KxComponentType` — 扩展的组件类型

---

## KxComponentType

kx-admin 注册的额外表单组件类型，可在 VbenForm schema 的 `component` 字段中使用：

```typescript
type KxComponentType =
  | 'CodeMirrorEditor'
  | 'CodeMirrorJsonEditor'
  | 'DicRadioGroup'
  | 'DicSelect'
  | 'FileUpload'
  | 'ImgUpload'
  | 'JsonEditor'
  | 'StorageImg';
```

这些组件通过 `registerKxComponents()` 注册到 `globalShareState`，与上游组件合并。

---

## 覆盖的上游组件

kx-admin 覆盖了上游的 `ApiSelect` 和 `ApiTreeSelect`，增加了搜索和过滤能力：

### ApiSelect（增强版）
```typescript
// 相比上游增加了：
{
  filterOption: FormFields.filterOption,  // label+value 模糊匹配
  showSearch: true,
  class: 'w-full',
}
```

### ApiTreeSelect（增强版）
```typescript
// 相比上游增加了：
{
  fieldNames: { label: 'label', value: 'value', children: 'children' },
  filterOption: FormFields.filterOption,
  showSearch: true,
  class: 'w-full',
}
```

使用方式与上游一致，无需额外配置即可搜索过滤。

---

## VxeTable 自定义渲染器

源码：`adapter/kx/vxe-renderers.ts`

### 全局配置
```typescript
// 列最小宽度 100px
VxeUI.setConfig({ grid: { columnConfig: { minWidth: 100 } } });
```

### CellDic — 字典值渲染
根据字典编码将值渲染为对应的字典标签：
```typescript
{
  field: 'storage_type',
  title: '存储类型',
  cellRender: { name: 'CellDic', props: { code: 'storage_type' } },
}
```

### StorageImg — 存储图片渲染
根据文件 ID 渲染存储图片：
```typescript
{
  field: 'cover',
  title: '封面',
  cellRender: { name: 'StorageImg' },
}
```
支持透传 props/attrs 给 StorageImg 组件。

### CellOperation — 操作按钮（kx 增强版）
kx 覆盖了上游 CellOperation，增加了超过 3 个按钮时自动折叠为 Dropdown 的功能：

```typescript
{
  title: '操作',
  width: 200,
  cellRender: {
    name: 'CellOperation',
    options: ['edit', 'delete', 'detail', 'copy'],  // >3 个时后面的折叠
    attrs: {
      nameField: 'name',      // 删除确认弹窗显示的名称字段
      nameTitle: '用户',       // 删除确认弹窗标题
      onClick: onActionClick,
    },
  },
}
```

行为：
- 前 2 个按钮正常显示，第 3 个起折叠到 Dropdown 菜单（省略号图标）
- `delete` 操作自动带 Popconfirm 确认弹窗
- 预设操作码：`edit`（编辑）、`delete`（删除），其它字符串自动尝试 `$t('common.xxx')` 翻译
- 支持对象形式自定义按钮：

```typescript
options: [
  'edit',
  { code: 'copy', text: '复制', icon: 'mdi:content-copy' },
  { code: 'detail', text: '详情', show: (row) => row.status === 1 },
  'delete',
]
```

- `show: false` 或 `show: (row) => boolean` 可控制按钮显隐

---

## form-use 工具函数

源码：`packages/kx-admin/src/adapter/form-use/`

### dicLabelFn / dicAutoSelect

字典组件的辅助函数，已内置到 DicSelect/DicRadioGroup：
```typescript
// label 自动 $t() 国际化
export const dicLabelFn = (item: any) => $t(item.label);

// 自动选中 is_def=1 的默认项
export const dicAutoSelect = (items: any[]) => items.find((item) => item.is_def === 1);
```

### vbenRadioGroup(code) — 状态单选 Schema 生成

快速生成 DicRadioGroup 表单 schema：
```typescript
import { vbenRadioGroup } from '#/adapter/form-use';

const schemas = [
  vbenRadioGroup('state'),
  // 等价于：
  // {
  //   component: 'DicRadioGroup',
  //   fieldName: 'state',
  //   label: '参数状态',
  //   defaultValue: 1,
  //   componentProps: {
  //     params: { code: 'state' },
  //     buttonStyle: 'solid',
  //     optionType: 'button',
  //     class: 'w-full',
  //   },
  // }
];
```

### vbenI8n — 国际化 Key 输入 Schema 生成

生成带 AutoComplete 的国际化 key 输入字段，自动提示已有 i18n key 并实时预览翻译结果：

```typescript
import { vbenI8n } from '#/adapter/form-use';

const schemas = [
  vbenI8n({
    fieldName: 'title',
    label: '标题',
    rules: 'required',
  }),
];
```

功能：
- AutoComplete 下拉列表显示所有可用 i18n key（来自 `I18ns.curOptions()`）
- 支持 label+value 模糊搜索过滤
- label 下方实时显示翻译结果（绿色），无对应翻译时显示红色提示
- `useHelp: true` 时翻译结果显示在 help 位置而非 label 下方

### VxeSchemas.timeSchemas() — 时间列 Schema 生成

快速生成 `created_at` / `updated_at` 时间列配置：
```typescript
import { VxeSchemas } from '#/adapter/form-use';

const gridOptions = {
  columns: [
    { field: 'name', title: '名称' },
    // ...业务列
    ...VxeSchemas.timeSchemas(),
    // 生成：
    // { field: 'created_at', title: '创建时间', formatter: timestampToTime }
    // { field: 'updated_at', title: '更新时间', formatter: timestampToTime }
  ],
};
```
