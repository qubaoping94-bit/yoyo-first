# 功能说明

`douyin-skill-installer` 将短视频中的 skill 推荐转成可验证的本地安装动作。

## 能力

- 从抖音链接、分享文案、标题、章节、字幕或页面文本中提取候选 skill。
- 把视频中的营销名或简称映射成真实 skill 包名。
- 优先查本地已安装 skill 和官方 curated list。
- 对 GitHub 来源进行安全核验。
- 安装后检查 `SKILL.md` 和 frontmatter。
- 输出安装清单、来源仓库和不确定项。

