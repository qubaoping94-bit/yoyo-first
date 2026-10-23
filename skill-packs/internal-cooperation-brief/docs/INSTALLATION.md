# 安装与依赖

## Codex和WorkBuddy

`scripts/install.ps1 -Target Both`为两个应用安装同一份标准Skill。只安装一端时选择Codex或WorkBuddy。该脚本不会编辑账号配置，不删除或覆盖不同版本。

WorkBuddy也可用官方“添加技能 → 上传技能”导入downloads/internal-cooperation-brief.zip；ZIP根目录即SKILL.md。agents/openai.yaml是Codex界面配置，主入口与脚本不依赖它。

新建对话后明确说“用internal-cooperation-brief技能整理”。若WorkBuddy未发现，检查技能已启用；不要把本地文件复制成功当作应用内调用验收。

## 运行环境

Node.js18+。在工具运行目录安装Playwright：

```powershell
npm install --no-save playwright
npx playwright install chromium
```

也可复用系统Edge/Chrome。导出器自动寻找已装playwright及本机npm缓存；可显式加`--playwright-path <包目录>`。首次安装依赖需要网络，报告生成与导出不需要联网或API Key。

Windows优先Microsoft YaHei，macOS优先PingFang SC；其他系统回退sans-serif，字体不同会改变断行，需要重新核验。输出目录不要选skill目录。

## 历史安装保护

安装器预检所有目标。完全相同的安装跳过；不同版本会停止并提示先另存旧版。不执行卸载、删除或自动替换。
