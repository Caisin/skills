# VbenDrawer

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
