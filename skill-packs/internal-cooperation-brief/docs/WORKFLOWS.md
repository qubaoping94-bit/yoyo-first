# 使用流程

1. 把零散工作记录、合作需求、价格及市场策略交给助手，说明用于内部汇报。
2. 助手整理事实、意向、拟议策略及内部待决事项，用“目前首要任务”行动表述开头。未知数据保持未知。
3. 按skills/internal-cooperation-brief/references/input-format.md生成JSON，写到本次任务目录。
4. 执行render.cjs，再执行export.cjs。可用examples/sample.json测试，示例不是实际业务。

```powershell
node skills/internal-cooperation-brief/scripts/render.cjs examples/sample.json <新输出目录>
node skills/internal-cooperation-brief/scripts/export.cjs <新输出目录>/report.html
```

输出report.html、report.json、report.png、report.pdf、mobile-390.png及checks.json。已有输出不会覆盖。

脚本检查图片长度、正文大小、PDF页数及三个手机宽度。助手需再查看图片，确认重点、序号、断行和商业范围保留。多页或过长时压短重复内容，不缩正文或删核心事实；无证据不要连续重试。

固定的是版式和表达规则，不是案例里的企业、价格或任务。风格变更从候选开始，不改写已确认模板；普通周报仍可使用用户原有风格。
