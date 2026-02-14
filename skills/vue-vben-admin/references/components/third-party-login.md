# Third-Party Login

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
