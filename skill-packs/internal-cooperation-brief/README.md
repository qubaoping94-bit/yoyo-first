# 内部合作汇报 · Codex / WorkBuddy

把零散合作材料整理为**商务蓝手机单图、一页PDF和HTML**。沿用已确认版式：中文章节、括号条目序号、正文常规字重、关键标签加粗；开头默认“目前首要任务”。

助手负责提炼内容，脚本负责稳定排版。无需模型API，不上传业务材料。默认区分对方需求、合作意向、我方拟议策略、内部待决定事项，不编造价格、数量、产能、负责人或排期。

## 直接使用

> 用 internal-cooperation-brief 整理以下材料，按固定商务蓝手机模板生成内部合作汇报，交付微信单图和一页PDF。缺失信息标待定。

Codex也可使用 `$internal-cooperation-brief`。

## 安装

下载本仓库后，在本包目录执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/install.ps1 -Target Both
```

- Codex：`~/.codex/skills/internal-cooperation-brief/`
- WorkBuddy：`~/.workbuddy/skills/internal-cooperation-brief/`
- 也可只装一端：`-Target Codex` 或 `-Target WorkBuddy`。相同安装可跳过，遇到不同版本会停止，避免覆盖。

WorkBuddy也可下载 [独立技能ZIP](downloads/internal-cooperation-brief.zip)，在“专家·技能·连接器 → 技能 → 添加技能 → 上传技能”导入。[官方上传说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)

Codex在下一轮对话可发现新Skill；WorkBuddy可新建对话并确认该技能已启用。文件安装与脚本核验不等于WorkBuddy真实会话验收。

## 环境与验证

Node.js18+；导出需要Playwright与Chromium/Edge/Chrome。HTML生成无需依赖，导出优先复用本机已有Playwright；详见[安装说明](docs/INSTALLATION.md)。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify.ps1
```

入口：[SKILL.md](skills/internal-cooperation-brief/SKILL.md) · [数据格式](skills/internal-cooperation-brief/references/input-format.md) · [完整流程](docs/WORKFLOWS.md) · [核验范围](docs/VALIDATION.md) · [示例提示词](examples/prompts.md)

公开示例全部为虚构说明，不包含真实客户材料、成交价或私人联系信息。真实微信发送后的压缩效果仍需实际手机查看。
