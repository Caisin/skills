# KX Skill Creator Patterns

用于当前仓库 repo-local skill 的创建、收敛与校验。

## 适用场景

- 新建 `.agents/skills/<name>/`
- 统一维护 `SKILL.md / references / evals`
- 需要快速生成更贴近当前仓库场景的 skill 骨架

## 推荐命令

### 生成通用骨架

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init my-skill --kind generic --when "这里描述触发场景"
```

### 生成更贴近仓库语义的骨架

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init my-entry-skill --kind entry --when "需要先判断任务落点"
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init my-practice-skill --kind practice --when "任务已经明确进入实践层开发"
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init my-sdk-skill --kind sdk --when "任务明确属于 sdks/ 第三方接入开发"
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init my-aigc-skill --kind aigc --when "任务明确落在 sdks/aigc"
```

### 全量校验

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py validate
```

## 常见错误

```text
❌ 骨架生成后不补真实触发词与真实示例，直接提交
❌ 改了 skill 结构却不跑 validate
❌ 没有区分 entry / practice / sdk / aigc 等不同语义，导致 description 与正文错位
```

## 正确做法

```text
✅ 先选对 --kind，再补仓库真实内容
✅ 提交前统一跑 validate
✅ 新增或调整 skill 规范时，同步更新 AGENTS.md 与相关 repo-local skills
```

## 路径引用规则

```text
❌ 在 skill 里写死 <absolute-path> 这类本地绝对路径，把风格约定绑死在某台机器或某个工作区
❌ 只给路径，不提炼这些参考代码背后的结构模式和可迁移规则
✅ 优先把参考实现抽象成可复用的风格描述，例如：目录职责、接口形状、事务边界、启动方式、路由聚合方式
✅ 如果必须引用仓库内文件，优先使用 repo 相对路径，并同时说明“为什么看这里”
```
