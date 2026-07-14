# Mike Cover Flow Skill

这是 Mike 在优优 AI 图库图片流项目中完成多轮实机校准后沉淀的可复用 Cover Flow 技能。

它用于在其他网站中构建连续、顺滑、完整显示图片并与宿主页面无缝融合的沉浸式图片流，同时约束移动端滚动、无障碍、窗口化、音效和生产验收。

## 一键安装

Windows 用户可双击：

\`\`\`text
install.bat
\`\`\`

或运行：

\`\`\`powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\install.ps1
\`\`\`

安装后重启 Codex，并使用：

\`\`\`text
Use $mike-cover-flow to build an immersive Cover Flow for this website.
\`\`\`

## GitHub 安装命令

\`\`\`powershell
python "$env:USERPROFILE\\.codex\\skills\\.system\\skill-installer\\scripts\\install-skill-from-github.py" --url "https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/mike-cover-flow/skills/mike-cover-flow"
\`\`\`

## 核心标准

- 连续浮点位置、RAF 惯性、速度影响释放距离、自然衰减与吸附。
- 完整图片自然比例；中心原图、邻卡缩略图；5–9 个 DOM 节点窗口化。
- 透明悬浮并融入宿主背景，禁止黑色演示舞台、巨大信息卡和可见色带。
- 音效克制、默认开启、首次真实手势解锁；手机不锁死纵向滚动。
- 桌面和移动端必须提供截图、性能、无障碍、真实像素接缝与生产域名证据。

