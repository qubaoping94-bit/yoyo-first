# 优优 AI 产品顾问 Skill

这是面向客户、经销商和销售团队的优优无机板产品顾问 Skill。安装后，Codex/Agent 可以直接按优优标准文库回答客户问题，覆盖五大平权、A级不燃、防潮耐水、低异味、环保甲醛、公司介绍、经销商转发话术等主题。

## 一键安装

Windows 用户解压本仓库后，双击：

```text
install.bat
```

或右键 PowerShell 运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装完成后重启 Codex，即可使用：

```text
Use $youyou-ai-product-advisor to answer: 优优无机板防潮耐水吗？
```

## GitHub 安装命令

仓库上传后，也可以用 Codex 自带安装器安装：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --url "https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/youyou-ai-product-advisor/skills/youyou-ai-product-advisor"
```

## 内容

- `skills/youyou-ai-product-advisor/SKILL.md`：Skill 入口说明。
- `references/knowledge-library.md`：完整客户可见标准文库。
- `references/knowledge-data.json`：机器可检索文库。
- `references/standard-question-routes.json`：标准问法路由。
- `scripts/find-youyou-answer.mjs`：本地命中文库脚本。
- `scripts/smoke-test.mjs`：基础命中率自测。
- `scripts/install.ps1`：一键安装到本机 Codex skills 目录。
- `scripts/verify.ps1`：验证技能包结构和命中率。

## 固定线上入口

- 优优 AI 产品顾问：https://youyou-ai-product-advisor.pages.dev/
- 微信入口：https://youyou-ai-product-advisor.pages.dev/wechat/
- 优优图库：https://youyou-ai-gallery.pages.dev/
