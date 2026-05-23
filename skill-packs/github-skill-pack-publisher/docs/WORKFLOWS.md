# 工作流

## 默认：单 skill 独立发布

1. 确认目标仓库。
2. 确认要发布的单个 skill。
3. 创建 `skill-packs/<skill-name>/`。
4. 复制 `skills/<skill-name>/SKILL.md` 和 `agents/openai.yaml`。
5. 写该 skill 专属 README、docs、examples、manifest、scripts。
6. 验证该技能包。
7. 生成该技能包独立 zip。
8. commit、push、远程确认。

## 明确要求时：多 skill 合集

只有用户明确要求多个 skill 合并，才创建包含多个 skill 的合集包。

