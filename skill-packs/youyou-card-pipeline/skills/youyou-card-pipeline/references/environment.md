# 通用运行环境

同一套文件供 Codex 与 WorkBuddy 使用，区别仅在 Skill 发现目录与文件展示工具。Windows 默认安装目录分别为用户目录下 .codex/skills/youyou-card-pipeline 和 .workbuddy/skills/youyou-card-pipeline。使用仓库包 scripts/install.ps1 -HostTarget Both 可安装到两处；原目录先备份至对应 .codex/skill-backups 或 .workbuddy/skill-backups，不在 skills 中留下重复入口。

构建与字数检查：Python 3.9+，仅标准库。渲染与几何校验：Node.js 20+、Playwright >=1.60.0 <2 与兼容浏览器。优先使用宿主现有环境。Codex 可用 load_workspace_dependencies 查询已配置 Node/Playwright；用 --playwright-module 指定其 index.mjs 的真实绝对路径。禁止猜测用户目录或缓存版本。

首次建立独立运行时，可在技能目录运行 npm install --ignore-scripts；然后 npx playwright install chromium。Windows 使用 npm.cmd/npx.cmd 可避免 npm.ps1 执行策略问题。下载需要网络。已装 Google Chrome 可在渲染/校验命令加 --channel chrome；Edge 加 --channel msedge。依赖安装后渲染内置模板不请求外网。

命令从技能目录执行，替换示例参数为真实路径：
```text
python scripts/build_deck.py --input assets/deck.example.json --output <输出目录>
node scripts/render_deck.mjs --html <输出目录/index.html> --output <输出目录/output>
node scripts/validate_deck.mjs --html <输出目录/index.html>
python scripts/count_body_chars.py <输出目录/xhs-note.md>
```

渲染可加 --playwright-module <已有模块入口>、--channel chrome、--report <报告路径>。不传 channel 时使用 Playwright 配套 Chromium。报告 ok=false 或非零退出时必须修复再交付。检查自定义 HTML 时只能使用用户授权、可信的本地文档；阻断 HTTP 不是任意 HTML 的安全沙箱。

WorkBuddy 有 present_files 才调用；Codex 使用当前文件展示/打开工具。两者均写输出目录交付记录.md；项目日志只追加到已确认路径。重开宿主会话以重新发现安装后的 Skill。
