# 通用演讲内容源 v1

以 `assets/deck-example.json` 为可运行例。一个 JSON 是 HTML、PDF 和 PPTX 的唯一文字/页序来源；不要分别手改导出件。`slides` 使用稳定 `id`，每页包括 `layout`、`kicker`、`title`、`subtitle`、`items`、`conclusion`、`notes`、`image`、`claim_ids`。可省略不适用的字段；勿复制样例业务内容。

可用页型：`cover`（封面图文）、`section`（章节）、`cards`（2—8 大卡）、`comparison`（恰好两侧对照）、`process`（2—6 步）、`evidence`（恰好主张／证据／边界三组）、`table`（2—8 项汇总，八零专题可使用）、`image`（图文）、`summary`（2—4 项结论）。先选符合信息关系的页型，再调文案；不能靠换色伪装页型。

`claims` 是当前稿的主张台账，键为稳定 ID；每条写 `text`、`source`、`status`（只能 `approved` 或 `hold`）、`scope`、`limitations`。每页 `claim_ids` 必须引用现有台账。缺来源、`hold` 或五大平权版本未确认时，构建命令阻断正式模式。预览可用 `--allow-hold`，输出仍标为 `CONTENT_HOLD`。`content_version` 对“五大平权”等分歧必须有业务负责人批准的来源；不能由脚本自行选择。

`assets` 是图片清单，图片 ID 对应 `path`、`purpose`、`rights`、`text_sensitive`。页面的 `image` 引用图片 ID。仅本地文件允许导入，构建时嵌入 HTML 以便离线使用；缺图、重复用于不相干页面、文字敏感图使用 `cover` 裁切，都要在验收报告中指出。图片授权仍需人工核对。

构建：`python scripts/build-deck.py assets/deck-example.json <输出目录> --allow-hold`。正式稿去掉 `--allow-hold`。导出：`python scripts/export-deck.py <输出目录>/index.html <输出目录> --editable`；需 `playwright`、`Pillow`、`PyMuPDF`、`python-pptx` 和本机 Chromium/Edge。视觉保真 `presentation.pptx` 是整页图像，不可编辑文字；`presentation-editable.pptx` 只提供内容可编辑的简化布局，不宣称像素等同。HTML/PDF/PPTX 的页序均来自同一个 manifest。
