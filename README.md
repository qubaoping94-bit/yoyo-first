# Codex AI Product Skill Kit

这是一套面向 Codex 的 AI 产品工程化交付技能包，包含两个自定义 skill：

- `ai-product-delivery-pipeline`：AI 产品工程化交付流水线，总控型 skill。
- `douyin-skill-installer`：从抖音视频内容中识别并安装提到的 Codex/agent skill。

它们适合长期复用在两类任务里：

- 把 AI Web 产品、AI SaaS、内部 AI 工具、Agent 应用从想法推进到可上线版本。
- 从抖音/短视频/教程内容里提取 skill 名称，查找官方来源，安全核验后安装到 Codex。

## 目录结构

```text
codex-ai-product-skill-kit/
  skills/
    ai-product-delivery-pipeline/
      SKILL.md
      agents/openai.yaml
    douyin-skill-installer/
      SKILL.md
      agents/openai.yaml
  scripts/
    install.ps1
    install-companion-skills.ps1
    verify.ps1
  manifest/
    skill-pack.json
    companion-skills.json
  docs/
    FEATURES.md
    INSTALLATION.md
    WORKFLOWS.md
    SECURITY.md
    GITHUB_UPLOAD.md
  examples/
    prompts.md
  THIRD_PARTY_NOTICES.md
  LICENSE
```

## 快速安装

在 PowerShell 中运行：

```powershell
cd "D:\桌面应用软件下载库\OneDrive\Desktop\two\codex-ai-product-skill-kit"
.\scripts\install.ps1
```

如果系统提示 PowerShell 禁止运行脚本，使用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

如果要同时安装配套依赖 skill：

```powershell
.\scripts\install.ps1 -WithCompanions
```

安装后建议重启 Codex 或新开会话，让新 skill 进入可用 skill 列表。

## 快速验证

```powershell
.\scripts\verify.ps1
```

或：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

验证脚本会检查：

- skill 目录是否存在
- `SKILL.md` 是否存在
- `agents/openai.yaml` 是否存在
- 如本机存在 Codex 官方 validator，则运行 `quick_validate.py`

## 主要能力

| Skill | 用途 | 典型触发 |
|---|---|---|
| `ai-product-delivery-pipeline` | 编排 AI 产品从需求到上线的完整工程化流程 | "做一个 AI 产品并上线"、"把这个 demo 变成可交付产品" |
| `douyin-skill-installer` | 从抖音内容中提取 skill 名称、定位来源、核验并安装 | "根据这个抖音链接安装里面提到的 skill" |

## 推荐配套 skill

`ai-product-delivery-pipeline` 会按任务阶段调用或建议使用这些配套能力：

- `Code`
- `frontend-design`
- `vercel-react-best-practices`
- `web-design-guidelines`
- `microsoft-foundry`
- `azure-ai`
- `azure-aigateway`
- `azure-prepare`
- `azure-validate`
- `azure-deploy`

其中 Vercel 和 Microsoft Azure 相关 skill 可通过 `scripts/install-companion-skills.ps1` 安装。

## 文档入口

- [完整功能说明](docs/FEATURES.md)
- [安装说明](docs/INSTALLATION.md)
- [工作流说明](docs/WORKFLOWS.md)
- [安全与核验原则](docs/SECURITY.md)
- [GitHub 上传说明](docs/GITHUB_UPLOAD.md)
- [示例提示词](examples/prompts.md)

## 上传到 GitHub

如果你已经创建了 GitHub 空仓库：

```powershell
cd "D:\桌面应用软件下载库\OneDrive\Desktop\two\codex-ai-product-skill-kit"
git remote add origin https://github.com/<your-name>/<your-repo>.git
git branch -M main
git push -u origin main
```

如果仓库已有内容，先阅读 [GitHub 上传说明](docs/GITHUB_UPLOAD.md)，避免覆盖远程内容。
