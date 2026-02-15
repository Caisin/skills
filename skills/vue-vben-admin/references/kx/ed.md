# KxEd / KxBuf / KxBuffer — 加密解密模块

源码：`packages/kx/src/ed/`

基于 salt + 字节级 XOR 变换的轻量加密模块，用于前后端数据传输加密（非密码学安全加密）。

## KxEd — 加密解密工具

```typescript
import { KxEd } from '@vben/kx';

// 字符串加密/解密（最常用）
const encrypted = KxEd.e_str('hello world');   // hex 字符串
const decrypted = KxEd.de_str(encrypted);      // 'hello world'

// Buffer 加密/解密
const encBuf = KxEd.en(buffer);    // 随机 32 字节 salt + 加密数据
const decBuf = KxEd.de(encBuf);    // 解密还原

// 指定 salt 加密/解密
const salt = KxEd.rand_salt(32);
const enc = KxEd.en_with_salt(data, salt);
const dec = KxEd.de_with_salt(enc, salt);

// XOR 补码变换（255 - 每个字节）
const transformed = KxEd.cx_ed(buffer);

// 随机工具
KxEd.rand_salt(32)       // 随机 Buffer
KxEd.rand_number(1, 100) // 随机整数
KxEd.rand_str(16)        // 随机字母数字字符串
```

### 加密流程
1. 生成随机 32 字节 salt
2. 将 salt 混入数据字节（`mix_salt`）
3. XOR 补码变换（`cx_ed`）
4. 输出格式：`[salt长度(u8)] [salt] [加密数据]`

### 完整 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `e_str(data)` | `(string) => string` | 字符串→加密 hex |
| `de_str(data)` | `(string) => string` | 加密 hex→字符串 |
| `en(data)` | `(Buffer) => Buffer` | Buffer 加密（随机 salt） |
| `de(data)` | `(Buffer) => Buffer` | Buffer 解密 |
| `en_with_salt(data, salt)` | `(Buffer, Buffer) => Buffer` | 指定 salt 加密 |
| `de_with_salt(data, salt)` | `(Buffer, Buffer) => Buffer` | 指定 salt 解密 |
| `cx_ed(data)` | `(Buffer) => Buffer` | XOR 补码变换 |
| `mix_salt(data, salt)` | `(Buffer, Buffer) => Buffer` | 混入 salt |
| `remove_salt(data, salt)` | `(Buffer, Buffer) => Buffer` | 移除 salt |
| `rand_salt(length)` | `(number) => Buffer` | 随机 salt |
| `rand_number(min, max)` | `(number, number) => number` | 随机整数 |
| `rand_str(length)` | `(number) => string` | 随机字符串 |

---

## KxBuf — Buffer 读写游标封装

带读写游标的 Buffer 封装，用于二进制协议的序列化/反序列化。

```typescript
import { KxBuf } from '@vben/kx';

// 创建
const buf = new KxBuf(1024);         // 指定初始大小
const buf2 = KxBuf.from(buffer);     // 包装已有 Buffer
const buf3 = KxBuf.from_str('hello'); // 从字符串创建

// 写入
buf.write_u8(255);
buf.write_u64(123456789);
buf.write_bf(someBuffer);

// 读取
const byte = buf.read_u8();
const bigint = buf.read_u64();

// 获取有效数据
const data = buf.data();  // read_idx 到 write_idx 之间的数据
```

### API

| 方法 | 说明 |
|------|------|
| `new KxBuf(size?)` | 创建，默认 1024 字节 |
| `KxBuf.from(bf)` | 包装已有 Buffer |
| `KxBuf.from_str(str)` | 从字符串创建 |
| `read_u8()` | 读 u8，游标前进 1 |
| `read_u64()` | 读 u64 BE，游标前进 8 |
| `write_u8(v)` | 写 u8，游标前进 1 |
| `write_u64(v)` | 写 u64 BE，游标前进 8 |
| `write_bf(v)` | 写入整个 Buffer |
| `data()` | 返回有效数据切片 |
| `length()` | 返回 Buffer 总长度 |
| `check_exp()` | 自动扩容检查 |

---

## KxBuffer

`buffer` npm 包的 `Buffer` 类的重导出，用于浏览器环境的 Buffer 操作。

```typescript
import { KxBuffer } from '@vben/kx';

const buf = KxBuffer.from('hello', 'utf-8');
const hex = buf.toString('hex');
```
