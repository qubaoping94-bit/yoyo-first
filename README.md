# YOYO Codex Skill Packs

这个仓库现在按“一个 skill 一个独立技能包”的方式组织。

默认规则：

- 每个 skill 单独打包、单独文档、单独安装、单独验证。
- 只有明确要求“多个 skill 合并成一个包”时，才创建合集包。
- 根目录只做索引，不再作为综合技能包使用。

## 独立技能包

| 技能包 | 用途 | 入口 |
|---|---|---|
| `ai-product-delivery-pipeline` | AI 产品工程化交付流水线，从需求、前端、AI 架构、Azure AI 到验证部署 | [skill-packs/ai-product-delivery-pipeline](skill-packs/ai-product-delivery-pipeline) |
| `douyin-skill-installer` | 从抖音/短视频内容识别、核验并安装提到的 Codex/agent skill | [skill-packs/douyin-skill-installer](skill-packs/douyin-skill-installer) |
| `github-skill-pack-publisher` | 把 skill/workflow 整理成独立 GitHub 技能包、文档、脚本、zip 并上传 | [skill-packs/github-skill-pack-publisher](skill-packs/github-skill-pack-publisher) |

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

