# VbenModal

## Define Modal Component (separate file)
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

## Use Modal in Parent
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

## Modal with Form
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
