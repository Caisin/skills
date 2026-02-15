# Upload 组件 (kx-admin)

基于 Ant Design Vue Upload + 后端文件存储的上传与展示组件。

源码目录：`packages/kx-admin/src/components/upload/`

## Table of Contents
- [FileUpload](#fileupload)
- [ImgUpload](#imgupload)
- [StorageImg](#storageimg)

---

## FileUpload

通用文件上传组件，支持任意文件类型。图片可弹窗预览，其它文件点击后新窗口下载。

### Props
```typescript
interface FileUploadProps {
  modelValue?: number | number[];
  /** 存储编码，决定上传到哪个存储桶，默认 'file' */
  storageCode?: string;
  /** 最大上传数量，默认 1 */
  maxCount?: number;
  /** 接受的文件类型，如 '.pdf,.doc,.png'，不传则不限制 */
  accept?: string;
  /** 自定义上传函数 */
  customRequest?: UploadProps['customRequest'];
  /** 是否禁用 */
  disabled?: boolean;
  /** 列表展示类型，默认 'text' */
  listType?: 'picture' | 'picture-card' | 'text';
}
```

### 在表单 Schema 中使用
```typescript
{
  component: 'FileUpload',
  fieldName: 'attachment',
  label: '附件',
  componentProps: {
    accept: '.pdf,.doc,.docx',
    maxCount: 3,
  },
}
```

### 图片上传（picture-card 模式）
```typescript
{
  component: 'FileUpload',
  fieldName: 'photos',
  label: '照片',
  componentProps: {
    storageCode: 'image',
    listType: 'picture-card',
    accept: '.png,.jpg,.jpeg',
    maxCount: 5,
  },
}
```

### 直接在模板中使用
```vue
<script setup>
import { ref } from 'vue';
import { FileUpload } from '#/components/upload';

const fileId = ref<number>();
</script>

<template>
  <FileUpload v-model="fileId" accept=".pdf,.doc" />
</template>
```

### 预览逻辑
- 图片文件（png/jpg/jpeg/gif/bmp/svg/webp）→ Modal 弹窗预览（StorageImg）
- 其它文件 → 调用 `FileApi.preview` 获取 URL，新窗口打开下载

### 值说明
- `maxCount=1` 时，modelValue 为 `number`（单个文件 ID）
- `maxCount>1` 时，modelValue 为 `number[]`（文件 ID 数组）
- 组件通过 `FileApi.urls` 回显已有文件

### 与 ImgUpload 的区别

| 特性 | ImgUpload | FileUpload |
|------|-----------|------------|
| storageCode | 固定 'image' | 可配置，默认 'file' |
| accept | 默认 `.png,.jpg,.svg,.jpeg` | 不限制（由调用方传入） |
| listType | 固定 `picture-card` | 可配置，默认 `text` |
| 预览 | StorageImg 图片预览 | 图片→预览；其它→下载 |
| 上传按钮 | PlusOutlined 图标 | Button + UploadOutlined |

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

### 直接在模板中使用
```vue
<script setup>
import { ref } from 'vue';
import { ImgUpload } from '#/components/upload';

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
