# Alert / Confirm / Prompt

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
