# @vben/kx 工具库

`packages/kx/` — kx-admin 的核心工具库，提供环境变量、时间处理、树结构、查询处理、国际化、表单字段转换、消息弹窗、加密等通用功能。

包名：`@vben/kx`

## 模块索引

| 模块 | 导入 | 说明 |
|------|------|------|
| [Envs](#envs) | `import { Envs } from '@vben/kx'` | 环境变量读取 |
| [时间工具](#时间工具) | `import { timestampToTime, toUnix, ... } from '@vben/kx'` | 日期时间处理 |
| [树结构](#树结构) | `import { listToTree, treeToList, TreeCfg } from '@vben/kx'` | 列表↔树转换 |
| [查询处理](#查询处理) | `import { filter_data, process_req, ... } from '@vben/kx'` | 请求数据清洗 |
| [FormFields](#formfields) | `import { FormFields } from '@vben/kx'` | 表单字段值转换 |
| [I18ns](#i18ns) | `import { I18ns } from '@vben/kx'` | 国际化工具 |
| [Msgs](#msgs) | `import { Msgs } from '@vben/kx'` | 消息/确认弹窗 |
| [FormModal](#formmodal) | `import { FormModal } from '@vben/kx'` | 通用表单弹窗组件 |
| [加密模块](kx/ed.md) | `import { KxEd, KxBuf, KxBuffer } from '@vben/kx'` | 加密解密（独立文档） |

---

## Envs

环境变量读取工具类，封装 `import.meta.env`。

```typescript
import { Envs } from '@vben/kx';

Envs.isProd          // boolean — 是否生产环境
Envs.appTitle        // string — VITE_APP_TITLE
Envs.appVersion      // string — VITE_APP_VERSION
Envs.appNamespace    // string — VITE_APP_NAMESPACE
Envs.base            // string — VITE_BASE（默认 '/'）
Envs.isHashRouter    // boolean — VITE_ROUTER_HISTORY === 'hash'
Envs.enableConsole   // boolean — VITE_ENABLE_CONSOLE
Envs.apiSecurity     // boolean — VITE_API_SECURITY

// 解析工具方法
Envs.bool(value, defaultValue?)   // 'true'/'1' → true
Envs.str(value, defaultValue?)    // 字符串环境变量
Envs.num(value, defaultValue?)    // 数字环境变量
```

---

## 时间工具

基于 dayjs 的日期时间工具函数。

```typescript
import { timestampToTime, toUnix, timestamp, toDayStartUnix, toDayEndUnix } from '@vben/kx';

// 格式化时间戳为字符串
timestampToTime(1700000000)     // '2023-11-14 22:13:20'
timestampToTime(1700000000000)  // 自动识别 10位/13位时间戳

// 转换为 unix 时间戳（秒）
toUnix('2023-11-14')            // number
toUnix(new Date())              // number

// 当前时间戳
timestamp()                     // number（秒）

// 日期边界
toDayStartUnix('2023-11-14')   // 当天 00:00:00 的时间戳
toDayEndUnix('2023-11-14')     // 当天 23:59:59 的时间戳

// 数字补零
pad2(5)                         // '05'
padding(5, 4)                   // '0005'
```

---

## 树结构

列表与树结构互转工具。

```typescript
import { listToTree, treeToList, TreeCfg } from '@vben/kx';

// 默认配置：id='id', pid='pid', children='children', sort='order_no'
const tree = listToTree(flatList);

// 自定义字段名
const cfg = TreeCfg.create({
  id_key: 'menu_id',
  pid_key: 'parent_id',
  children_key: 'sub_menus',
  sort_key: 'sort',
});
const tree = listToTree(flatList, cfg);

// 树转回列表
const list = treeToList(tree, cfg);
```

### TreeCfg 配置

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `id_key` | `'id'` | 节点 ID 字段 |
| `pid_key` | `'pid'` | 父节点 ID 字段 |
| `children_key` | `'children'` | 子节点数组字段 |
| `sort_key` | `'order_no'` | 排序字段 |

---

## 查询处理

请求数据清洗和处理工具。

```typescript
import { filter_data, process_req, is_empty, del_ks } from '@vben/kx';

// 过滤空值（直接修改对象）
const data = { name: 'test', age: null, desc: '' };
filter_data(data);  // { name: 'test' }  — 移除 null/undefined/''/'{}'

// 判断是否为空值
is_empty(null)      // true
is_empty('')        // true
is_empty('{}')      // true

// 删除嵌套属性
del_ks(obj, 'a.b.c');  // 删除 obj.a.b.c

// 处理请求：深拷贝 → 自定义处理 → 过滤空值
const req = process_req(rawData, (data) => {
  // 自定义转换逻辑
  data.time = toUnix(data.time);
});
```

---

## FormFields

表单字段值转换工具，常用于 VbenForm schema 的 `fieldName` 配合 `componentProps` 处理时间范围等场景。

```typescript
import { FormFields } from '@vben/kx';

// 时间范围 → 日期起止 unix 时间戳
// 将 timeRange 字段拆分为 start_time（当天00:00:00）和 end_time（当天23:59:59）
FormFields.timeRangeToDayStartEndUnixRange('time')
// (value, setFieldValue) => 设置 start_time / end_time

// 时间范围 → 精确 unix 时间戳
FormFields.timeRangeToUnixRange('time')

// 单个时间 → unix 时间戳
FormFields.timeToUnix('created_at')

// 下拉选项过滤（label+value 模糊匹配）
FormFields.filterOption(inputValue, option)
```

### 在 VbenForm 中使用 valueFormat

```typescript
{
  component: 'RangePicker',
  fieldName: 'timeRange',
  label: '时间范围',
  formItemClass: 'col-span-2',
}
// 在 proxyConfig.ajax.query 中使用：
const formValues = process_req(gridApi.formApi.form.values, (data) => {
  FormFields.timeRangeToDayStartEndUnixRange('timeRange')(
    data.timeRange,
    (key, val) => { data[key] = val; }
  );
  delete data.timeRange;
});
```

---

## I18ns

国际化工具，封装 `@vben/locales` 的底层 i18n 实例。

```typescript
import { I18ns } from '@vben/kx';

// 获取当前语言
I18ns.curLocale()       // 'zh-CN' | 'en-US' | ...

// 获取当前语言的所有消息
I18ns.curMsg()          // { common: { edit: '编辑', ... }, ... }

// 获取所有语言的消息
I18ns.messages()

// 获取扁平化的 i18n key 选项列表（用于 AutoComplete）
I18ns.curOptions()      // [{ label: '编辑', value: 'common.edit' }, ...]

// 合并新的翻译消息
I18ns.mergeLocaleMessage('zh-CN', { module: { title: '模块' } })

// 扁平化工具
I18ns.flatten({ a: { b: 'hello' } })  // [{ label: 'hello', value: 'a.b' }]
```

---

## Msgs

消息和确认弹窗工具，封装 Ant Design Vue Modal/message。

```typescript
import { Msgs } from '@vben/kx';

// Promise 化的确认弹窗
const confirmed = await Msgs.confirm('确定要执行此操作吗？', '提示');
if (confirmed) { /* ... */ }

// 删除操作（带 loading + 成功提示）
Msgs.del({
  name: '用户张三',
  del_fn: () => deleteApi(id),
  succ_fn: () => gridApi.reload(),
});
```

