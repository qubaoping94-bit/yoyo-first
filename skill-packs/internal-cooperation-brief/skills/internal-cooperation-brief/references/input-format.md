# 数据与运行

需要Node.js18+。生成HTML只用标准库；导出需要Playwright及Chromium/Edge/Chrome。主流程不依赖Codex工具，WorkBuddy运行相同命令。

```json
{
  "title": "示例企业合作汇报",
  "meta": "内部经营汇报 · 合作沟通中",
  "focus": {"label":"目前首要任务","lines":["评估采购条件与供货能力，","明确合作路径及推进安排。"]},
  "sections": [
    {"title":"对方需求","status":"已收到","items":[{"label":"规格","text":"以本次材料为准，未知项待确认。","keepTogether":[],"emphasis":[]}]},
    {"title":"合作方式","status":"对方意向","items":[{"label":"路径","text":"记录实际提出的合作方式。"}],"shared":"只写有来源的共同要求。"},
    {"title":"我方策略","status":"拟议方案","items":[{"label":"渠道","text":"保留用户提出的经营思路。"}]},
    {"title":"内部待决定","status":"建议讨论","decision":true,"items":[{"label":"分工","text":"明确负责人，未指定则标待定。"}]}
  ],
  "note":"合作及策略未定案，缺失条件待确认。"
}
```

所有字段都是纯文字；脚本自动转义HTML。keepTogether为正文中需要整组不换行的片段；emphasis为少量金额等强调片段，也防拆行。章节及条目输入不带序号，自动生成。

默认每章1–3条，尽量每条2行。首要任务只固定标题，不固定案例任务。没有金额不编金额，不为短图丢主要商业范围。

```powershell
node <skill-dir>/scripts/render.cjs <整理稿.json> <新输出目录>
node <skill-dir>/scripts/export.cjs <输出目录>/report.html
```

脚本拒绝覆盖输出；调整后用新目录保留上版。不要把本次数据写入skill目录。

导出器加载已安装playwright，或本机npm缓存已有包；不会自动联网安装。可用`--playwright-path <playwright包目录>`指定路径。依赖缺失时在工具目录执行`npm install --no-save playwright`，然后指定该目录node_modules/playwright；缺浏览器时执行`npx playwright install chromium`。Edge/Chrome可作回退。仓库不包含node_modules或浏览器。

PDF多页/溢出/图片过长时先压短重复内容和长句，不缩小已确认正文。一次失败后根据具体检查结果修正，不无变化重跑。

WorkBuddy只需读取SKILL.md及上述脚本。agents/openai.yaml是Codex可选界面配置，不是运行依赖；跨平台包验证不等于已在WorkBuddy真实会话调用。
