# youyou-dealer-ppt

> v3.0.0：单一 JSON 内容源、9 种可组合页型、图片／主张台账，以及 HTML→PDF／图片型视觉保真 PPTX／可编辑内容版 PPTX 导出。2026-10-09 Mike 确认 21 页视觉回归版；具体新稿仍须逐页验收与业务内容审批。

独立技能包，用于制作优优无机板经销商、产品知识和商业演讲。当前优先标准是用户指定的 2026-09-27 正式交付 **21 页八零功能与经营演讲系统**：浅米色网格、近黑大字、红色强调、低无意义留白、清晰证据边界、演讲者备注和可靠翻页。

本包记录样例标准，不发布用户的 EXE、快捷方式、运行配置或完整 21 页样例截图。`assets/approved-21-fixture.html` 是不含业务内容的 21 页样例风格参考页型；`approved-black-red-template.html` 是历史 27 页视觉种子，不得误认作当前样例或事实真源。

2.1.0 增加了画布比例、左侧红色识别条、网格、字号、内容版本冲突和证据台账的静态预检。新稿先对照参考页型做代表页，再逐页目检；静态检查通过并不等于视觉或业务主张已经获批。

安装：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

验证：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
python .\skills\youyou-dealer-ppt\scripts\audit-fidelity.py <deck-html> --pptx <deck.pptx> --pdf <deck.pdf> --report <audit.json>
```

使用时请说明项目所需输出格式；默认先核对样例与新稿资料、主张证据，再制作和逐页验收。技能说明见 [SKILL.md](skills/youyou-dealer-ppt/SKILL.md)。

生成与导出（在 `skills/youyou-dealer-ppt` 目录；示例无业务主张）：

```powershell
python .\scripts\test-build.py
python .\scripts\build-deck.py .\assets\deck-example.json <输出目录>
python .\scripts\export-deck.py <输出目录>\index.html <输出目录> --editable --browser-path <本机Edge或Chromium路径>
python .\scripts\audit-render.py <输出目录>\index.html <输出目录>\render-audit.json --browser-path <本机Edge或Chromium路径>
python .\scripts\audit-output.py <输出目录>
python .\scripts\test-export.py
```

导出依赖 Python 3 的 `playwright`、`Pillow`、`PyMuPDF`、`python-pptx`；浏览器需要本机 Chromium/Edge。安装依赖前请用隔离虚拟环境，仓库不附带第三方运行时。正式演讲前仍须人工检查全部页面、内容证据和版权。

真实样例四类代表页回归素材：`skills/youyou-dealer-ppt/assets/baseline-regression-four.json`。它逐字取自 2026-09-27 正式样例，并保留历史内容 `CONTENT_HOLD`，仅供同视口视觉对照；不会替代或修改 21 页源稿。用 `scripts/audit-baseline-regression.py` 对照样例 `source/index.html` 和 `source/content-ledger.json` 检查可见文案与备注，再用 `scripts/capture-regression.cjs` 拍摄 1920×1080 页面。新项目仍需先请 Mike 确认代表页，再扩展全稿。

双模式边界见 [delivery-modes.md](skills/youyou-dealer-ppt/references/delivery-modes.md)：默认 PPTX 保真但页内文字不可单独编辑；可编辑 PPTX 是内容版，不能宣称像素同版。五大平权分类须提供五个经业务批准的名称及可追溯来源，否则正式构建阻断。

可使用 `scripts/import-approved-sample.py` 从本机正式样例的 `source/index.html` 和 `source/content-ledger.json` 生成 21 页 `CONTENT_HOLD` 回归 JSON（需 `beautifulsoup4`）。完整源稿不进入仓库。先用 `audit-baseline-regression.py` 核对 21 页可见文字和备注，再用 `capture-regression.cjs` 在三视口查越界并留 1920×1080 截图；Python Playwright 不可用时，`export-deck.py --from-frames` 可复用这些已审计截图生成 PDF 和两种 PPTX。最后运行 `audit-output.py`，并将可编辑 PPTX 经演示软件转成 PDF 后运行 `audit-editable.py --rendered-pdf <文件>`。2026-10-09 的视觉认可不等于未来新稿自动通过。

`scripts/build-visual-review.py` 可将原 21 页截图与新稿截图生成同视口并排审阅页；它只读本地样例和本次截图，不将原图提交仓库。每份新的完整演讲稿仍需 Mike 独立视觉确认。
