# github-skill-pack-publisher

独立技能包：GitHub Skill 包发布器。

这个 skill 负责把本地 Codex skill 或重复工作流整理成独立技能包，生成完整文档、安装脚本、验证脚本、zip，并提交推送到 GitHub。

核心默认规则：

- 一个 skill 默认生成一个独立技能包。
- 多个 skill 只有在用户明确要求“合并打包”时才做合集包。

## 安装

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

## 验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

## 文档

- [功能说明](docs/FEATURES.md)
- [安装说明](docs/INSTALLATION.md)
- [工作流说明](docs/WORKFLOWS.md)
- [安全说明](docs/SECURITY.md)
- [示例提示词](examples/prompts.md)

