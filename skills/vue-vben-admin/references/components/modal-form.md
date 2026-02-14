# useModalForm & useModalTable (kx-admin)

## Table of Contents
- [useModalForm](#usemodalform)
- [useModalTable](#usemodaltable)

---

## useModalForm

Encapsulates VbenModal + VbenForm into a single composable for CRUD modal forms. Import from `#/components` or `@vben/kx-admin`.

### ModalFormData Interface
```typescript
interface ModalFormData<T, TValues> {
  /** Submit API function */
  api?: (values: TValues) => Promise<unknown> | void;
  /** Row data for edit mode (auto-fills form) */
  row?: Partial<TValues>;
  /** Form schema definition */
  schema?: VbenFormSchema<T>[];
  /** Modal title (supports i18n key) */
  title?: string;
  /** Custom form config (layout, wrapperClass, etc.) */
  form?: Partial<VbenFormProps<T>>;
  /** Custom modal config (width, fullscreen, centered, etc.) */
  modal?: Record<string, any>;
  /** Pre-submit hook: transform data or return false to cancel */
  beforeSubmit?: (values: TValues) => Promise<false | TValues> | false | TValues;
  /** Callback after successful submission */
  onSuccess?: () => void;
}
```

### Basic Usage
```vue
<script lang="ts" setup>
import { useModalForm } from '#/components';
import { saveUser } from '#/api/user';

const { FormModal, openModal } = useModalForm({
  schema: [
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'Input', fieldName: 'email', label: '邮箱' },
  ],
  api: saveUser,
});

// Create
function onCreate() {
  openModal({ title: '新建用户' });
}

// Edit (row data auto-fills form)
function onEdit(row: Record<string, any>) {
  openModal({ row, title: '编辑用户' });
}
</script>

<template>
  <FormModal @success="refreshGrid" />
</template>
```

### Custom wrapperClass
```typescript
// Override default grid layout (default: lg:grid-cols-3 2xl:grid-cols-4)
openModal({
  title: '创建',
  form: {
    wrapperClass: 'gap-x-4 sm:grid-cols-1 md:grid-cols-2',
  },
});
```

### Custom Modal Props
```typescript
openModal({
  title: '详情',
  modal: { fullscreen: true },  // or { centered: true }, etc.
});
```

### beforeSubmit Hook
```typescript
const { FormModal, openModal } = useModalForm({
  schema: useSchema(),
  api: saveItem,
  beforeSubmit: (values) => {
    // Transform data before submit
    return { ...values, updated_at: Date.now() };
    // Or return false to cancel submission
  },
});
```

### onSuccess Callback
```typescript
openModal({
  title: '创建',
  onSuccess: () => {
    message.success('操作成功');
    refreshGrid();
  },
});
```

### Extra Footer Slot
```vue
<FormModal @success="refreshGrid">
  <template #extra-footer="{ formApi }">
    <Button @click="formApi.resetForm()">自定义按钮</Button>
  </template>
</FormModal>
```

### Default Slot (Custom Content Below Form)
```vue
<FormModal @success="refreshGrid">
  <template #default="{ formApi }">
    <div class="mx-4 text-gray-500">额外提示信息</div>
  </template>
</FormModal>
```

### Access formModalApi
```typescript
const { FormModal, formModalApi, openModal } = useModalForm({ ... });

// Programmatically close
formModalApi.close();
// Update modal state
formModalApi.setState({ title: '新标题' });
```

### Full CRUD Page Pattern
```vue
<script lang="ts" setup>
import { Page } from '@vben/common-ui';
import { Plus } from '@vben/icons';
import { Msgs } from '@vben/kx';
import { Button } from 'ant-design-vue';
import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { useModalForm } from '#/components';
import { $t } from '#/locales';
import { delItem, getPage, saveItem } from '#/api/item';
import { useColumns, useGridFormSchema, useSchema } from './data';

const { FormModal, openModal } = useModalForm({
  schema: useSchema(),
  api: saveItem,
});

function onCreate() {
  openModal({ title: $t('common.create', '项目') });
}

function onEdit(row: any) {
  openModal({ row, title: $t('common.edit', '项目') });
}

function onDelete(row: any) {
  Msgs.del({ name: row.name, del_fn: () => delItem(row.id), succ_fn: refreshGrid });
}

function onActionClick({ code, row }: { code: string; row: any }) {
  switch (code) {
    case 'edit': { onEdit(row); break; }
    case 'delete': { onDelete(row); break; }
  }
}

const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: { schema: useGridFormSchema(), submitOnChange: true },
  gridOptions: {
    columns: useColumns(onActionClick),
    height: 'auto',
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) =>
          await getPage({ page: page.currentPage, pageSize: page.pageSize, ...formValues }),
      },
    },
    toolbarConfig: { custom: true, refresh: true, zoom: true },
  },
});

function refreshGrid() { gridApi.query(); }
</script>

<template>
  <Page auto-content-height>
    <FormModal @success="refreshGrid" />
    <Grid :table-title="$t('item.list')">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" /> {{ $t('ui.actionTitle.create') }}
        </Button>
      </template>
    </Grid>
  </Page>
</template>
```

---

## useModalTable

Simplified variant of `useModalForm` without generics, custom form props, or extra-footer slot. Suitable for simple modal forms.

### ModalTableData Interface
```typescript
interface ModalTableData {
  api?: (values: Record<string, any>) => Promise<void> | void;
  row?: Record<string, any>;
  schema?: VbenFormSchema[];
  title?: string;
  modal?: Record<string, any>;
  beforeSubmit?: (values: Record<string, any>) => Promise<false | Record<string, any>> | false | Record<string, any>;
  onSuccess?: () => void;
}
```

### Usage
```typescript
import { useModalTable } from '@vben/kx-admin';

const { TableModal, tableModalApi, openModal } = useModalTable({
  schema: useSchema(),
  api: saveData,
});

openModal({ title: '创建', row: existingData });
```

```vue
<template>
  <TableModal @success="refreshGrid" />
</template>
```
