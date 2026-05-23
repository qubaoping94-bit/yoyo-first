# ai-product-delivery-pipeline

独立技能包：AI 产品工程化交付流水线。

这个 skill 负责把 AI Web 产品、AI SaaS、内部 AI 工具或 Agent 应用，从需求梳理推进到工程实现、体验打磨、AI 架构、Azure AI 接入、部署准备、验证和上线。

## 包内容

```text
skills/ai-product-delivery-pipeline/
scripts/install.ps1
scripts/install-companion-skills.ps1
scripts/verify.ps1
manifest/skill-pack.json
manifest/companion-skills.json
docs/
examples/prompts.md
```

## 安装

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

如需同时安装配套 skill：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -WithCompanions
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

