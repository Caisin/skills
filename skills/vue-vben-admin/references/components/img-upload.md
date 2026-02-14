# ImgUpload & StorageImg (kx-admin)

基于 Ant Design Vue Upload + 后端文件存储的图片上传与展示组件。

## Table of Contents
- [ImgUpload](#imgupload)
- [StorageImg](#storageimg)

---

## ImgUpload

图片上传组件，v-model 绑定文件 ID（`number | number[]`），自动回显已上传图片。

### Props
```typescript
interface ImageUploadProps {
  modelValue?: number | number[];
  /** 最大上传数量，默认 1 */
  maxCount?: number;
  /** 接受的文件类型，默认 .png,.jpg,.svg,.jpeg */
  accept?: string;
  /** 自定义上传函数，默认 FileApi.upload_img */
  customRequest?: UploadProps['customRequest'];
  /** 是否禁用 */
  disabled?: boolean;
}
```

### 在表单 Schema 中使用
```typescript
{
  component: 'ImgUpload',
  fieldName: 'cover',
  label: '封面',
  componentProps: {
    maxCount: 1,
    accept: '.png,.jpg,.jpeg',
  },
}
```

### 多图上传
```typescript
{
  component: 'ImgUpload',
  fieldName: 'images',
  label: '图片列表',
  componentProps: {
    maxCount: 5,
  },
}
```

### 自定义上传函数
```typescript
{
  component: 'ImgUpload',
  fieldName: 'avatar',
  label: '头像',
  componentProps: {
    customRequest: (options) => FileApi.upload('custom_code', options),
    maxCount: 1,
  },
}
```

### 直接在模板中使用
```vue
<script setup>
import { ref } from 'vue';
import { ImgUpload } from '#/components/img-upload';

const coverId = ref<number>();
</script>

<template>
  <ImgUpload v-model="coverId" :max-count="1" />
</template>
```

### 值说明
- `maxCount=1` 时，modelValue 为 `number`（单个文件 ID）
- `maxCount>1` 时，modelValue 为 `number[]`（文件 ID 数组）
- 组件会自动通过 `FileApi.preview` / `FileApi.urls` 回显已有图片

---

## StorageImg

根据文件 ID 展示存储图片，自动调用 `FileApi.preview` 获取 URL，带 loading 状态。

### Props
```typescript
interface StorageImgProps {
  fileId: number | string;
  /** 加载失败时的占位图 */
  fallback?: string;
}
```

### 基础用法
```vue
<StorageImg :file-id="123" />
```

### 指定尺寸
```vue
<StorageImg :file-id="item.cover" :width="150" />
```

### 自定义样式
```vue
<StorageImg :file-id="item.cover" class="h-20 w-20 rounded" />
```
不传 `class` 时默认 `w-full`。

### 在 VxeTable 中作为渲染器
已注册为 VxeTable 渲染器，可直接在列配置中使用：
```typescript
{
  field: 'cover',
  title: '封面',
  cellRender: { name: 'StorageImg' },
}
```

### 失败占位图
```vue
<StorageImg :file-id="item.cover" fallback="/placeholder.png" />
```
