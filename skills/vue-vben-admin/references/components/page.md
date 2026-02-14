# Page Component

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
