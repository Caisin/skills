# VxeTable (Grid)

## Basic Table
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

## Remote Data Table (Proxy Config)
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

## Table with Search Form
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

## Built-in Cell Renderers
| Renderer | Description |
|----------|-------------|
| `CellTag` | Render value as Tag (default: 1=enabled/green, 0=disabled/red) |
| `CellSwitch` | Render value as Switch toggle |
| `CellImage` | Render value as Image |
| `CellLink` | Render value as link Button |
| `CellOperation` | Render action buttons (edit/delete with confirm) |

## Grid API Methods
```typescript
gridApi.setLoading(true);
gridApi.setGridOptions({ border: true, stripe: true });
gridApi.reload();  // Reload data
gridApi.query();   // Query with form values
const state = gridApi.useStore((state) => state.gridOptions?.border);
```
