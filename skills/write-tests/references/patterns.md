# Test Patterns

用于为 kx-rs crate 选择测试位置、边界和运行顺序。

## 测试位置

| 行为 | 位置 |
|---|---|
| 私有纯函数、解析器、状态机 | 相邻 `#[cfg(test)] mod tests` |
| crate 公共 API 与跨模块行为 | `<crate>/tests/` |
| 公共 API 最小用法 | rustdoc doc test |
| derive/codegen 成功行为 | 从生成代码使用者视角的集成测试 |
| 编译失败契约 | 复用该 derive crate 已有 UI/compile-test 方式 |

## 推荐顺序

```bash
rtk cargo test -p <crate> <test_name>
rtk cargo test -p <crate>
rtk cargo test --workspace
```

## 常见错误

```text
❌ 测试私有字段布局而非公共行为
❌ 一个测试覆盖多个无关场景
❌ 依赖固定顺序或共享全局状态
```

## 正确做法

```text
✅ 回归测试先证明旧实现失败
✅ fixture 最小且与被测行为分离
✅ 目标测试通过后再扩大验证
```
