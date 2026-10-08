# 双模式交付验收

默认交付 `presentation.pptx`：每页为高清整页图像，视觉与 HTML/PDF 页面一致；演讲备注可保留，但页面内文字和卡片不能单独编辑。此模式优先满足正式演讲视觉保真。

可选交付 `presentation-editable.pptx`：标题、正文和图片对象可在 PowerPoint 内单独修改；为实现可编辑，布局是简化版本，不承诺与 HTML/PDF/图片型 PPTX 像素一致。使用者若要修改内容，应先改唯一 JSON 源并重新导出全部格式；直接编辑 PPTX 只适合现场临时改字，不会回写 JSON。

每次交付至少核对：

- HTML、PDF、视觉保真 PPTX 页数和页序一致；备注页数一致。
- 图片型 PPTX 内嵌页图与导出 PNG 哈希一致，PDF 同页像素差在项目门槛内；逐页人工目检裁切、空白、字号、图片与文字。
- 可编辑版能选中标题、正文和独立图片；但报告必须写明相对视觉保真版的差异，不得称其为“完全同版”。
- 可编辑版要用演示软件实际渲染后执行 `scripts/audit-editable.py`，核对全部标题、正文、结论、备注是否出现在对象和渲染页面；密集页还须目检文字是否相互重叠。只检查 XML 中有文字对象并不足够。
- `CONTENT_HOLD` 的稿件仅能作为隔离预览；即便格式测试通过，也不能正式对外。

展示给 Mike 时应提供四类代表页的认可母版截图、修改前候选、修改后候选，在同为 1920×1080 的条件下并排比较；只有 Mike 确认视觉方向后，才扩展全套。

若 Python Playwright 不可安装，可使用已安装的 Node Playwright 运行 `capture-regression.cjs` 输出 `frames/slide-XX-<id>.png` 和 `capture-report.json`，再运行 `export-deck.py ... --from-frames`。此路径仍要求截图为 1920×1080、捕获报告 `PASS`，并执行 `audit-output.py`；不能把缺依赖当作跳过浏览器渲染验收的理由。
