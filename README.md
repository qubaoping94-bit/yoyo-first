# YOYO Codex Skill Packs

这个仓库按照“一套 skill 一个独立技能包”的方式组织。

默认规则：

- 每个 skill 单独打包、单独文档、单独安装、单独验证。
- 只有明确要求“多个 skill 合并成一个包”时，才创建合集包。
- 根目录只做索引，不作为综合技能包使用。

## 独立技能包

| 技能包 | 用途 | 入口 |
|---|---|---|
| `ai-product-delivery-pipeline` | AI 产品工程化交付流水线，从需求、前端、AI 架构、Azure AI 到验证部署 | [skill-packs/ai-product-delivery-pipeline](skill-packs/ai-product-delivery-pipeline) |
| `douyin-skill-installer` | 从抖音短视频内容识别、核验并安装提到的 Codex/agent skill | [skill-packs/douyin-skill-installer](skill-packs/douyin-skill-installer) |
| `douyin-workflow-skill-publisher` | 抖音 skill 视频到组合 workflow skill，再到独立 GitHub 技能包发布的完整流水线 | [skill-packs/douyin-workflow-skill-publisher](skill-packs/douyin-workflow-skill-publisher) |
| `github-skill-pack-publisher` | 把 skill/workflow 整理成独立 GitHub 技能包、文档、脚本、zip 并上传 | [skill-packs/github-skill-pack-publisher](skill-packs/github-skill-pack-publisher) |
| `skill-guide-writer` | 全面审计任意 AI Skill，核验能力、安装与在线资源，并生成第一屏可直接调用的中文 Markdown 使用说明 | [skill-packs/skill-guide-writer](skill-packs/skill-guide-writer) |
| `manufacturing-enterprise-operations-ai-frontdesk` | 制造企业通用经营知识库 AI 前台，覆盖销售、订单、BOM、采购、生产、质检、交付、财务和售后 | [skill-packs/manufacturing-enterprise-operations-ai-frontdesk](skill-packs/manufacturing-enterprise-operations-ai-frontdesk) |
| `partner-sales-service-ai-frontdesk` | 合作商通用销售服务知识库 AI 前台，覆盖客户项目、报价订单、到账、交付、售后和经营查询 | [skill-packs/partner-sales-service-ai-frontdesk](skill-packs/partner-sales-service-ai-frontdesk) |
| `senxu-door-business-ai-frontdesk` | 森旭木门内部经营管理样例库专用 AI 前台，用于完整制造业务链展示与培训 | [skill-packs/senxu-door-business-ai-frontdesk](skill-packs/senxu-door-business-ai-frontdesk) |
| `youyou-business-ai-frontdesk` | 优优无机板合作商经营服务样例库专用 AI 前台，含 40 个意图工作流和严格业务边界 | [skill-packs/youyou-business-ai-frontdesk](skill-packs/youyou-business-ai-frontdesk) |
| `customer-acquisition-pipeline` | 抖音获客流水线组合 skill：公开线索抓取、飞书客户库、冷邮件草稿 | [skill-packs/customer-acquisition-pipeline](skill-packs/customer-acquisition-pipeline) |
| `youyou-demo-page-delivery-pipeline` | 优优无机板演示系统页面从参考图到生成、接入、部署、审计和记忆收尾的完整交付流水线 | [skill-packs/youyou-demo-page-delivery-pipeline](skill-packs/youyou-demo-page-delivery-pipeline) |
| `youyou-inorganic-board-guide` | 优优无机板产品顾问 skill：面向客户/经销商讲解产品体系、话术和公开资料入口 | [skill-packs/youyou-inorganic-board-guide](skill-packs/youyou-inorganic-board-guide) |
| `youyou-wechat-article-pipeline` | WorkBuddy 专用的优优无机板公众号文章选题、创作、排版、配图、校验与草稿箱交付流水线 | [skill-packs/youyou-wechat-article-pipeline](skill-packs/youyou-wechat-article-pipeline) |
| `youyou-ai-product-advisor` | 优优 AI 产品顾问 skill：安装后可直接按标准文库回答客户问题、匹配语义问法、生成经销商话术 | [skill-packs/youyou-ai-product-advisor](skill-packs/youyou-ai-product-advisor) |
| `youyou-dealer-ppt` | 以 2026-09-27 正式交付的 21 页八零演讲系统为优先样例，制作与验收优优经销商演示 | [skill-packs/youyou-dealer-ppt](skill-packs/youyou-dealer-ppt) |
| `mike-cover-flow` | 按 Mike 实机验收标准构建顺滑、完整显示并与网站无缝融合的 Cover Flow 图片流 | [skill-packs/mike-cover-flow](skill-packs/mike-cover-flow) |
| `mike-web-clarity-gate` | 在网站制作与验收中约束单行标题、消除 AI 模板感并检查页面布局协调性 | [skill-packs/mike-web-clarity-gate](skill-packs/mike-web-clarity-gate) |
| `mike-website-production-pipeline` | 编排 Product Design、Figma、Hallmark、Taste、Mike 门禁和 GSAP，完成网站设计、开发、验收与发布全流程 | [skill-packs/mike-website-production-pipeline](skill-packs/mike-website-production-pipeline) |

## 通用安装方式

进入任意技能包目录后运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

验证：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

安装后建议重启 Codex 或新开会话，让新 skill 进入可用技能列表。

## 仓库校验

`.github/workflows/validate.yml` 会逐个验证 `skill-packs/*` 下的独立技能包。
