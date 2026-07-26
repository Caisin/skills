# Database Test Patterns

用于选择数据库 feature、隔离方式并报告外部环境验证。

## 命令模式

先从目标 crate 的 `Cargo.toml` 核实 feature：

```bash
rtk cargo test -p kx-sea-orm --features sqlite <test_name>
rtk cargo test -p kx-sea-orm --features postgres <test_name>
rtk cargo test -p kx-sea-orm --features mysql <test_name>
```

上述命令只说明 feature 选择方式；是否需要连接串、服务版本或串行运行由目标测试决定。

## 隔离与证据

```text
编译证据：目标 feature 能构建
连接证据：测试能连接专用服务
行为证据：断言验证目标数据库语义
清理证据：临时数据/库已回收
```

## 常见错误

```text
❌ 硬编码个人数据库连接串
❌ 把连接成功当作事务/迁移行为正确
❌ 外部服务缺失时跳过但报告为通过
```

## 正确做法

```text
✅ 使用专用环境变量或临时 fixture
✅ 只在对应后端断言后端特有语义
✅ 精确记录已验证层级和未验证条件
```
