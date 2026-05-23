# 功能说明

## 1. AI 产品工程化交付流水线

Skill 名称：`ai-product-delivery-pipeline`

定位：总控型、编排型 skill。它不是替代其他专业 skill，而是在一个 AI 产品交付任务里判断当前应该进入哪个阶段、调用哪个专业能力、通过什么检查后才能继续。

### 适用场景

- 从 0 到 1 创建 AI Web 产品
- 把本地 demo 改造成生产可用产品
- 开发 AI SaaS、内部 AI 工具、Agent 应用、知识库问答、OCR/语音/搜索类产品
- 审查已有 React/Next.js 产品的工程质量和 UX
- 将 AI 产品接入 Azure AI、Azure Foundry，并最终部署上线

### 覆盖阶段

| 阶段 | 内容 |
|---|---|
| 需求澄清 | 明确用户、场景、AI 能力、数据、安全、上线目标 |
| 项目规划 | 拆分里程碑、验收标准、风险点 |
| 产品实现 | 编写或改造前端、后端、测试 |
| React 质量 | 检查 Next.js/React 性能、数据请求、渲染、bundle |
| UI/UX | 检查设计层级、响应式、可访问性、状态和交互 |
| AI 架构 | 设计 Agent、Prompt、评测、监控、Foundry 项目 |
| Azure AI | 接入 OpenAI、AI Search、OCR、Speech、Document Intelligence |
| AI 网关 | 加入 APIM、限流、缓存、内容安全、成本控制 |
| 部署准备 | 生成 `.azure/deployment-plan.md`、infra、`azure.yaml` |
| 部署验证 | 跑 preflight、验证配置、记录 proof |
| 上线部署 | 执行部署并核验 live URL |

### 输出结果

一次完整执行后，应该能输出：

- 完成了哪些阶段
- 使用了哪些 specialist skill
- 改动了哪些文件
- 运行了哪些验证
- 是否已经部署成功
- live URL 或未部署原因
- 剩余风险和后续建议

## 2. 抖音 Skill 提取安装器

Skill 名称：`douyin-skill-installer`

定位：把抖音/短视频里提到的 Codex skill 或 agent workflow，转化为本地可安装、可验证的 Codex skill。

### 适用场景

- 用户给一个抖音链接，希望安装视频里提到的 skill
- 视频里只出现营销名或简称，需要映射到真实 GitHub package
- 需要判断某个 skill 来源是否可靠
- 需要从视频章节、字幕、标题、网页文本中提取 skill 清单

### 核心步骤

1. 提取视频内容：优先使用本地 Douyin 捕获流程，必要时用浏览器/Playwright 兜底。
2. 识别 skill 名称：提取视频中靠近 `skill`、`Codex`、`workflow`、`install` 等关键词的候选名称。
3. 映射真实来源：从本地已安装、官方 curated list、GitHub 官方仓库中查找真实 skill。
4. 安全核验：检查 repo、路径、`SKILL.md`、脚本、敏感命令、凭据风险。
5. 安装：使用本地 `skill-installer` 脚本。
6. 验证：检查安装目录和 frontmatter。

### 示例映射

| 视频名称 | 实际 skill | 来源 |
|---|---|---|
| Vercel React | `vercel-react-best-practices` | `vercel-labs/agent-skills` |
| Web Design | `web-design-guidelines` | `vercel-labs/agent-skills` |
| Foundry | `microsoft-foundry` | `microsoft/github-copilot-for-azure` |
| Azure AI | `azure-ai` | `microsoft/github-copilot-for-azure` |
| Azure Deploy | `azure-deploy` | `microsoft/github-copilot-for-azure` |

## 3. GitHub Skill 包发布器

Skill 名称：`github-skill-pack-publisher`

定位：把本地 Codex skill 或重复工作流整理成可上传、可安装、可验证的 GitHub 仓库项目。

### 适用场景

- 用户要求把刚生成的 skill 上传到 GitHub
- 用户希望把一组 skill 打包成公开仓库
- 用户需要 README、功能说明、安装说明、安全说明、示例提示词等完整材料
- 用户需要本地 zip 包和 GitHub 远程仓库同时保存
- 用户以后会大量重复类似发布操作，希望按同一套标准执行

### 标准交付物

| 类型 | 内容 |
|---|---|
| skill 源码 | `skills/<skill-name>/SKILL.md` 与 `agents/openai.yaml` |
| 文档 | `README.md`、`docs/FEATURES.md`、`docs/INSTALLATION.md`、`docs/WORKFLOWS.md`、`docs/SECURITY.md` |
| 脚本 | `scripts/install.ps1`、`scripts/install-companion-skills.ps1`、`scripts/verify.ps1` |
| 清单 | `manifest/skill-pack.json`、`manifest/companion-skills.json` |
| 示例 | `examples/prompts.md` |
| 发布辅助 | `.github/workflows/validate.yml`、`.gitignore`、`LICENSE`、`THIRD_PARTY_NOTICES.md` |

### 执行结果

执行完成后应报告：

- GitHub 仓库地址
- 新增或更新的 skill
- commit hash
- zip 路径
- 本地验证结果
- 是否已远程确认
