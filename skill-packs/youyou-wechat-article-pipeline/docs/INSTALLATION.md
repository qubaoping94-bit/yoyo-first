# 安装与配置

此技能运行于 WorkBuddy。执行 `scripts/install.ps1` 后，默认安装到 `~/.workbuddy/skills/youyou-wechat-article-pipeline`。

## 依赖

- WorkBuddy 与可用的 `ima-mcp`
- Python 3.12+ 与 Pillow
- 本机的文章规则文件、build 模板和素材目录
- 需要推草稿箱时：`wechat-publisher`、Node.js 和仅保存在本机的微信公众号凭据

技能文件使用以下环境变量表达本机路径：

- `WORKBUDDY_ROOT`：文章与素材工作目录，例如 `<你的工作目录>`
- `WORKBUDDY_HOME`：WorkBuddy 用户目录，默认可理解为 `~/.workbuddy`
- `PYTHON_312`：Python 3.12 解释器；未设置时使用 `python`

安装技能不会复制文章资产、知识库内容或凭据。请按 `使用说明书.md` 完成本机配置。
