# Component Usage Patterns

## Table of Contents
- [VbenForm](#vbenform)
- [VxeTable (Grid)](#vxetable-grid)
- [VbenModal](#vbenmodal)
- [VbenDrawer](#vbendrawer)
- [Page Component](#page-component)
- [Alert/Confirm/Prompt](#alertconfirmprompt)
- [Third-Party Login](#third-party-login)

## VbenForm

### Basic Form
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

### Form Schema Fields
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

### Form API Methods
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

### valueFormat - Custom Value Transformation
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

### ApiSelect - Remote Data Select
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

### ApiTreeSelect - Remote Tree Select
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

### Upload Component
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

### Time Field Mapping
```typescript
const [Form] = useVbenForm({
  // Map rangePicker value to startTime/endTime with format
  fieldMappingTime: [['rangePicker', ['startTime', 'endTime'], 'YYYY-MM-DD']],
  schema: [
    { component: 'RangePicker', fieldName: 'rangePicker', label: '日期范围' },
  ],
});
```

## VxeTable (Grid)

### Basic Table
```vue
<script lang="ts" setup>
import type { VxeGridProps } from '#/adapter/vxe-table';
import { Page } from '@vben/common-ui';
import { useVbenVxeGrid } from '#/adapter/vxe-table';

interface RowType {
  id: number;
  name: string;
  age: number;
  status: number;
}

const gridOptions: VxeGridProps<RowType> = {
  columns: [
    { title: '序号', type: 'seq', width: 50 },
    { field: 'name', title: '姓名' },
    { field: 'age', title: '年龄', sortable: true },
    { field: 'status', title: '状态', cellRender: { name: 'CellTag' } },
    {
      title: '操作',
      width: 160,
      cellRender: {
        attrs: { nameField: 'name', onClick: onActionClick },
        name: 'CellOperation',
        options: ['edit', 'delete'],
      },
    },
  ],
  data: [],
  pagerConfig: { enabled: false },
};

const [Grid, gridApi] = useVbenVxeGrid<RowType>({ gridOptions });

function onActionClick({ code, row }: { code: string; row: RowType }) {
  if (code === 'edit') { /* edit logic */ }
  if (code === 'delete') { /* delete logic */ }
}
</script>

<template>
  <Page title="表格示例">
    <Grid table-title="用户列表" />
  </Page>
</template>
```

### Remote Data Table (Proxy Config)
```typescript
const gridOptions: VxeGridProps<RowType> = {
  columns: [...],
  proxyConfig: {
    ajax: {
      query: async ({ page }) => {
        const { items, total } = await getTableListApi({
          pageNo: page.currentPage,
          pageSize: page.pageSize,
        });
        return { items, total };
      },
    },
  },
  pagerConfig: {},  // Enable pagination
};
```

### Table with Search Form
```typescript
const [Grid, gridApi] = useVbenVxeGrid<RowType>({
  formOptions: {
    schema: [
      { component: 'Input', fieldName: 'name', label: '姓名' },
      { component: 'Select', fieldName: 'status', label: '状态',
        componentProps: { options: [...] } },
    ],
  },
  gridOptions: {
    columns: [...],
    proxyConfig: {
      ajax: {
        query: async ({ page }) => {
          const formValues = gridApi.formApi.form.values;
          return await getTableListApi({ ...formValues, pageNo: page.currentPage });
        },
      },
    },
  },
});
```

### Built-in Cell Renderers
| Renderer | Description |
|----------|-------------|
| `CellTag` | Render value as Tag (default: 1=enabled/green, 0=disabled/red) |
| `CellSwitch` | Render value as Switch toggle |
| `CellImage` | Render value as Image |
| `CellLink` | Render value as link Button |
| `CellOperation` | Render action buttons (edit/delete with confirm) |

### Grid API Methods
```typescript
gridApi.setLoading(true);
gridApi.setGridOptions({ border: true, stripe: true });
gridApi.reload();  // Reload data
gridApi.query();   // Query with form values
const state = gridApi.useStore((state) => state.gridOptions?.border);
```

## VbenModal

### Define Modal Component (separate file)
```vue
<!-- modal-demo.vue -->
<script lang="ts" setup>
import { useVbenModal } from '@vben/common-ui';
import { message } from 'ant-design-vue';

const [Modal, modalApi] = useVbenModal({
  onConfirm: handleConfirm,
  onOpenChange(isOpen) {
    if (isOpen) {
      const data = modalApi.getData<{ content: string }>();
      // Use received data
    }
  },
});

async function handleConfirm() {
  modalApi.lock();  // Show loading on confirm button
  try {
    // Do async work
    modalApi.close();
  } finally {
    modalApi.lock(false);
  }
}
</script>

<template>
  <Modal title="弹窗标题">
    <p>弹窗内容</p>
  </Modal>
</template>
```

### Use Modal in Parent
```vue
<script lang="ts" setup>
import { useVbenModal } from '@vben/common-ui';
import ModalDemo from './modal-demo.vue';

const [Modal, modalApi] = useVbenModal({
  connectedComponent: ModalDemo,
});

function openModal() {
  modalApi.setData({ content: '传递的数据' }).open();
}

function openWithTitle() {
  modalApi.setState({ title: '动态标题' }).open();
}
</script>

<template>
  <Modal />
  <Button @click="openModal">打开弹窗</Button>
</template>
```

### Modal with Form
```vue
<script lang="ts" setup>
import { useVbenModal } from '@vben/common-ui';
import { useVbenForm } from '#/adapter/form';

const [Form, formApi] = useVbenForm({
  schema: [
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
  ],
});

const [Modal, modalApi] = useVbenModal({
  async onConfirm() {
    const { valid, values } = await formApi.validate();
    if (valid) {
      // Submit values
      modalApi.close();
    }
  },
  onOpenChange(isOpen) {
    if (isOpen) {
      const data = modalApi.getData<{ values: Record<string, any> }>();
      if (data?.values) formApi.setValues(data.values);
    }
  },
});
</script>

<template>
  <Modal title="表单弹窗"><Form /></Modal>
</template>
```

## VbenDrawer

Usage pattern is identical to VbenModal but uses `useVbenDrawer`:

```vue
<script lang="ts" setup>
import { useVbenDrawer } from '@vben/common-ui';

const [Drawer, drawerApi] = useVbenDrawer({
  onConfirm: handleConfirm,
});
</script>

<template>
  <Drawer title="抽屉标题">
    <p>抽屉内容</p>
  </Drawer>
</template>
```

Parent usage:
```vue
const [Drawer, drawerApi] = useVbenDrawer({ connectedComponent: DrawerDemo });
drawerApi.setData({ ... }).open();
```

## Page Component

Wrap view content with `Page` for consistent layout:

```vue
<template>
  <Page
    title="页面标题"
    description="页面描述"
    content-class="flex flex-col gap-4"
    auto-content-height
  >
    <template #extra>
      <Button type="primary">操作按钮</Button>
    </template>
    <!-- Page content -->
  </Page>
</template>
```

## Alert/Confirm/Prompt

```typescript
import { alert, confirm, prompt, clearAllAlerts } from '@vben/common-ui';

// Alert
alert({ content: '提示内容', icon: 'success' }).then(() => { /* closed */ });

// Confirm
confirm({
  content: '确认操作？',
  icon: 'question',
  beforeClose({ isConfirm }) {
    if (!isConfirm) return;
    return new Promise(resolve => setTimeout(() => resolve(true), 1000));
  },
}).then(() => { /* confirmed */ }).catch(() => { /* cancelled */ });

// Prompt
prompt<string>({
  content: '请输入',
  icon: 'question',
  componentProps: { placeholder: '输入内容...' },
}).then(value => { /* user input */ });
```

## Third-Party Login

The login component supports configurable third-party login providers via `thirdPartyLogins` prop:

```typescript
import type { ThirdPartyLogin } from '@vben/common-ui';
import { SvgGithubIcon } from '@vben/icons';

const thirdPartyLogins: ThirdPartyLogin[] = [
  {
    name: 'github',
    icon: SvgGithubIcon,
    tooltip: 'GitHub 登录',
    onClick: () => { /* handle github login */ },
  },
  {
    name: 'wechat',
    icon: SvgWeChatIcon,
    tooltip: '微信登录',
    onClick: () => { /* handle wechat login */ },
  },
];
```

Usage in login view:
```vue
<AuthenticationLogin
  :third-party-logins="thirdPartyLogins"
  @submit="authLogin"
/>
```

`ThirdPartyLogin` type:
```typescript
interface ThirdPartyLogin {
  name: string;
  icon: Component;
  tooltip?: string;
  onClick?: () => void;
}
```
