---
name: kx-skill-creator
description: |
  Use when 需要在 kx 仓库内创建、维护或批量校验 repo-local skill，尤其是 `.agents/skills/*` 下的 `SKILL.md`、`references`、`evals` 与配套脚手架。

  触发场景：
  - 新增一个仓库内 skill，并希望快速生成骨架
  - 修改 repo-local skill 后，需要统一校验 frontmatter、章节与 evals schema
  - 需要把全局 `skill-creator` 的通用方法落到当前仓库的本地约定

  触发词：创建 skill、维护 skill、SKILL.md、repo-local skill、evals.json、references、skill_tool、skill 规范
---

# kx-skill-creator

`kx-skill-creator` 是当前仓库对全局 `skill-creator` 的 repo-local 拓展 skill。
它专门处理 `.agents/skills/` 下的本地 skill 资产，而不是替代全局的通用 skill 设计方法。

## 适用边界

### 适用

- 新增一个 repo-local skill
- 统一维护 `SKILL.md / references / evals`
- 批量校验 skill artifacts 是否符合当前仓库规范
- 需要生成更贴近当前仓库场景的 `entry / practice / sdk / aigc` skill 骨架

### 不适用

- 纯讨论“skill 应该教什么”的抽象设计
- 跨仓库通用的 skill 策略研究
- 与当前 `.agents/skills/` 无关的外部 skill 改造

## Reference Selection

按任务类型优先读取：

- 想知道 repo-local skill 的结构约定与命令
  - 读 `references/patterns.md`
- 想直接生成或校验 skill artifacts
  - 运行 `scripts/skill_tool.py`

## 资产提炼规则

维护 repo-local skill 时，默认遵守这条额外规则：

```text
❌ 不要把本地机器上的绝对路径、个人工作目录、只能在当前环境成立的引用直接写死进 skill
✅ 要把这些来源提炼成“可复用风格 / 结构模式 / 代码特征 / 约定边界”再写进 skill
```

例如：

```text
❌ 代码风格优先对齐 <absolute-path-a> 与 <absolute-path-b>
✅ 代码风格优先复用“ctl 保持薄、svc 收口事务、router 用 nest 聚合、main.rs 做子命令分流”这类可迁移规则
```

只有在“当前仓库中确实存在、并且需要告诉模型去核实事实来源”的场景下，才适合引用 repo 内相对路径；即便如此，也应优先说明**为什么这些文件重要**，而不是只堆路径。

## crate 视角约定

对于 `kx-biz-param` 这类**可被其他项目直接依赖和复用的 crate 型 skill**，默认遵守这条规则：

```text
✅ 优先使用 crate 名、依赖写法、对外入口（如 router/install）来描述 skill
✅ 优先回答“其他项目怎么引入和复用它”
❌ 不要把 skill 主叙事写成某个源码目录内部维护说明（例如只写某个 bizs/ 路径）
```

例如：

```text
❌ 这是 bizs/xxx 模块，去改 bizs/xxx/src/...
✅ 这是 kx-xxx crate，其他项目可通过 Cargo.toml 引入，并复用它提供的统一入口
```

只有在讨论 crate 内部实现时，才继续下钻到 `src/ctl`、`src/svc`、`src/router` 等源码结构。

## 内置脚本

本 skill 自带脚本：

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py validate
```

### 生成新 skill 骨架

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init <name> --kind generic --when "这里描述触发场景"
```

支持的 `--kind`：

- `generic`
- `entry`
- `practice`
- `sdk`
- `aigc`

### 校验全部 repo-local skill

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py validate
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只改 SKILL.md，不同步 references 或 evals
❌ repo-local skill 结构各写各的，没有统一脚手架或校验
❌ 把当前仓库的本地 skill 维护问题，完全交给全局 skill-creator 而不落当前仓库约定
```

### 正确做法

```text
✅ 先用本 skill 的脚本生成骨架，再补充仓库特有内容
✅ 修改 repo-local skill 后，统一运行 validate
✅ 把“通用 skill 设计方法”与“当前仓库本地约定”分开处理
✅ 如果 skill 面向的是可复用 crate，默认使用 crate 视角来写 description、示例与接入方式
```

## 输出模板

```text
问题归类
建议命令
需要修改的 skill assets
验证方式
下一步
```

## 完整示例

**Input**

```text
我想在这个仓库里新增一个专门给 practice 层用的 skill，顺便要有 evals 和 reference。
```

**Output direction**

```text
- 先说明这是 repo-local skill 维护场景，应使用 kx-skill-creator。
- 推荐直接运行 skill_tool.py init <name> --kind practice。
- 生成骨架后再补 SKILL.md、references、evals 的仓库特定内容。
- 如果这是类似 kx-biz-param 的可复用 crate skill，正文应优先写 crate 名、依赖方式和对外入口，而不是只写源码目录。
- 最后运行 validate。
```
