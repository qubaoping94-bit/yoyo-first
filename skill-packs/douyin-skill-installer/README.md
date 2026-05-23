# douyin-skill-installer

独立技能包：抖音 Skill 提取安装器。

这个 skill 用于从抖音/短视频/教程分享内容中提取提到的 Codex 或 agent skill，映射真实来源，进行安全核验，然后安装并验证。

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

