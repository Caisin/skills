# VbenForm

## Basic Form
```vue
<script lang="ts" setup>
import { Page } from '@vben/common-ui';
import { Card, message } from 'ant-design-vue';
import { useVbenForm, z } from '#/adapter/form';

const [BaseForm, baseFormApi] = useVbenForm({
  commonConfig: {
    colon: true,
    componentProps: { class: 'w-full' },
  },
  handleSubmit: onSubmit,
  layout: 'horizontal',
  schema: [
    {
      component: 'Input',
      componentProps: { placeholder: '请输入' },
      fieldName: 'username',
      label: '用户名',
      rules: 'required',
    },
    {
      component: 'Select',
      componentProps: {
        options: [
          { label: '选项1', value: '1' },
          { label: '选项2', value: '2' },
        ],
      },
      fieldName: 'status',
      label: '状态',
      rules: 'selectRequired',
    },
    {
      component: 'DatePicker',
      fieldName: 'date',
      label: '日期',
    },
    {
      component: 'Switch',
      componentProps: { class: 'w-auto' },
      fieldName: 'enabled',
      label: '启用',
    },
    {
      component: 'Checkbox',
      fieldName: 'agree',
      label: '',
      renderComponentContent: () => ({ default: () => ['我已阅读并同意'] }),
      rules: z.boolean().refine((v) => v, { message: '请勾选同意' }),
    },
  ],
  wrapperClass: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
});

function onSubmit(values: Record<string, any>) {
  message.success(`提交: ${JSON.stringify(values)}`);
}
</script>

<template>
  <Page title="表单示例">
    <Card title="基础表单">
      <BaseForm />
    </Card>
  </Page>
</template>
```

## Form Schema Fields
| Property | Type | Description |
|----------|------|-------------|
| `component` | `ComponentType` | Component name registered in adapter |
| `fieldName` | `string` | Field name for form data binding |
| `label` | `string \| () => VNode` | Field label |
| `rules` | `'required' \| 'selectRequired' \| ZodType` | Validation rules |
| `componentProps` | `object \| () => object` | Props passed to the component |
| `defaultValue` | `any` | Default field value |
| `help` | `string \| () => VNode` | Help text below the field |
| `suffix` | `() => VNode` | Suffix content after the component |
| `dependencies` | `object` | Field dependencies for conditional rendering |
| `renderComponentContent` | `() => Record<string, () => VNode>` | Render component slots |
| `colon` | `boolean` | Show colon after label |
| `valueFormat` | `(value, set) => void` | Custom value transformation on getValues/submit |

## Form API Methods
```typescript
const [Form, formApi] = useVbenForm({ ... });

// Set multiple values
formApi.setValues({ username: 'admin', status: '1' });

// Set single value
formApi.setFieldValue('username', 'admin');

// Get all values
const values = await formApi.getValues();

// Validate
const { valid, values } = await formApi.validate();

// Reset form
formApi.resetForm();

// Update schema dynamically
formApi.updateSchema([{ fieldName: 'username', componentProps: { disabled: true } }]);
```

## valueFormat - Custom Value Transformation
Transform field values when calling `getValues()` or on submit:
```typescript
{
  component: 'RangePicker',
  fieldName: 'dateRange',
  label: '日期范围',
  valueFormat: (value, set) => {
    if (!value) return;
    const [start, end] = value;
    set('dateRange', [dayjs(start).startOf('day').unix(), dayjs(end).endOf('day').unix()]);
  },
}
```

## ApiSelect - Remote Data Select
```typescript
{
  component: 'ApiSelect',
  componentProps: {
    api: getAllMenusApi,
    afterFetch: (data) => data.map(item => ({ label: item.name, value: item.id })),
    autoSelect: 'first',  // Auto-select first option
    // Custom label rendering with labelFn (overrides labelField)
    labelFn: (item) => `${item.name} (${item.code})`,
  },
  fieldName: 'menuId',
  label: '菜单',
}
```

## ApiTreeSelect - Remote Tree Select
```typescript
{
  component: 'ApiTreeSelect',
  componentProps: {
    api: getDeptTreeApi,
    labelField: 'name',
    valueField: 'id',
    childrenField: 'children',
  },
  fieldName: 'deptId',
  label: '部门',
}
```

## Upload Component
```typescript
{
  component: 'Upload',
  componentProps: {
    accept: '.png,.jpg,.jpeg',
    customRequest: upload_file,
    maxCount: 1,
    maxSize: 2,  // MB
    listType: 'picture-card',
    crop: true,           // Enable image cropping
    aspectRatio: '1:1',   // Crop aspect ratio
    handleChange: ({ file }) => {
      if (file.status === 'done') message.success('上传成功');
    },
  },
  fieldName: 'avatar',
  label: '头像',
}
```

## Time Field Mapping
```typescript
const [Form] = useVbenForm({
  // Map rangePicker value to startTime/endTime with format
  fieldMappingTime: [['rangePicker', ['startTime', 'endTime'], 'YYYY-MM-DD']],
  schema: [
    { component: 'RangePicker', fieldName: 'rangePicker', label: '日期范围' },
  ],
});
```
