# 优优社交卡通用 Skill 使用说明

**复制下面这句话，在提供文章后直接使用：**

```text
用 $youyou-card-pipeline 把我提供的文章制作成8张1080×1440图卡，保持统一字阶，并生成正文不超过1000字符的小红书配文；完成校验和逐张目检后交付。
```

八卡示例：[查看完整示例画廊](https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/youyou-card-pipeline/examples/demo)

发布仓库：[qubaoping94-bit/yoyo-first](https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/youyou-card-pipeline)

## 这是什么

`youyou-card-pipeline` 是把文章转换为八张社交图卡与配套文案的生产流程。此版为 **2.0.0，Codex 与 WorkBuddy 共用同一份 Skill**。它保留原 WorkBuddy 版的 Swiss × IKB Blue 视觉规则、七条铁律和配文字数要求，补入可独立运行的模板与脚本，取消固定盘符和外部历史母本的强制依赖。

文章理解、文案提炼与审美检查由宿主 Agent 完成；脚本负责结构构建、图片渲染、尺寸/字号/溢出检查与字数计数。它不是单独的设计软件，也不是自动发帖工具。

## 核心能力

- 从用户文章提炼八卡结构，生成可编辑 deck.json 和 index.html。
- 内置封面、双模块、三列、四格、编号清单和蓝块收尾版式。
- 统一主标题112px、节点48/30px、编号100/52/28px、模块46/32px、收束38px等字阶，禁止逐卡缩字。
- 导出 xhs-01.png 至 xhs-08.png，逐张精确1080×1440。
- 检查8卡数量与顺序、画布尺寸、字号、文字和面板边界，以及第8卡蓝块；保存 JSON 校验报告。
- 生成 xhs-note.md，强制检查正文去空白后不超过1000字符，标点计入。
- 按宿主可用工具展示交付，保留来源、目检与未验证事项。

## 适合怎样使用

适合把知识文章、经销商讲解、产品价值说明或已核实的观点做成一组图文。输入不足时先分析与整理，不能从模板补造数据。默认八卡方案不适合直接充当产品检测报告、摄影证据、印刷文件、自动账号发布或任意页数的演示文稿。自定义母本可以在候选中沿用，但偏离尺寸、字阶或顺序的要求要明确记录，并调整校验规则。

## 输入与输出

提供文章全文或可读取的 Markdown 文件；说明受众、目的、必须保留或删除的内容。如果文章包含检测等级、配方、价格等，提供当前来源。不要求绑定个人账号或 API Key。

默认输出到当前工作目录的 `output/youyou-cards-主题-日期/`。其中保存 deck.json、index.html、xhs-note.md、交付记录.md；output 子目录保存8张 PNG 与渲染校验报告。已有认可成品时另建候选，避免覆盖。

## 路线选择与调用示例

默认用内置模板完整出图。已有认可母本时先提供源文件，以候选形式修改。只需配文或诊断时明确限定范围。

推荐完整制作：
```text
用 $youyou-card-pipeline 处理我附上的文章，面向优优经销商，保留原文事实和核心观点，整理为八卡，生成配文与可编辑源文件。保持统一字阶，运行尺寸、溢出和字数检查，逐张检查后交付，并列明资料不足的地方。
```

限定内容：
```text
用 $youyou-card-pipeline 为这篇文章配图配文。删除文中“五大平权”模块，结合其余内容说明“标配即顶配”。只使用我提供的事实，不新增竞品价格、认证或性能结论。
```

继续修改：
```text
用 $youyou-card-pipeline 修改当前这组八卡，把第3卡文案再精简，保留所有字号、尺寸与其余卡片内容。在新候选目录保存结果，重新校验并目检全部八张，同时同步配文。
```

只分析：
```text
用 $youyou-card-pipeline 先分析我提供的文章，输出八卡内容提纲和需要补证据的地方，暂不渲染、不公开发布。
```

只检查：
```text
用 $youyou-card-pipeline 检查我提供的 index.html 和 xhs-note.md，核对尺寸、字阶、溢出、正文字符数和收尾蓝块，列出问题，暂不修改源文件。
```

WorkBuddy 若未识别 `$` 写法，可直接说“使用 youyou-card-pipeline 技能”，其余要求相同。能否自动触发取决于宿主的技能发现与加载机制；安装后建议新开会话。

## 标准工作流程

1. 完整读文章与补充，确认受众和内容边界。
2. 整理 deck.json。固定封面、五张内容卡、清单、第8卡收尾；内容卡包含三列与四格。
3. 构建 HTML，按实际运行环境渲染，检查几何、字号和PNG尺寸。
4. 写推荐标题、正文、标签、来源说明与内容边界，运行字符计数。
5. 查看全部八张图，检查裁切、对齐、箭头、蓝块、留白和可读性。
6. 修复后验收，保存交付记录，再用宿主工具交付。

脚本通过只证明所检查的结构与几何条件，不能代替事实核验和视觉审美。

## 安装、发现与验证

下载或克隆仓库，进入 `skill-packs/youyou-card-pipeline`。以下 PowerShell 命令以包目录为当前目录：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -HostTarget Both
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Both 安装同一份到用户目录下 `.codex/skills/youyou-card-pipeline` 和 `.workbuddy/skills/youyou-card-pipeline`。只装一个可改为 Codex 或 WorkBuddy。更新会先把原文件夹备份到对应 `.codex/skill-backups` 或 `.workbuddy/skill-backups`，再安装；不会在发现目录里留下同名备份入口。安装后新开会话，在技能列表确认名称，再复制首屏指令。

验证脚本检查入口、必要文件、示例卡数与发布文件哈希；它不运行浏览器。检查实际安装目录可传 `-SkillDirectory`，路径使用自己的用户目录。

如需在其他系统使用，可手动复制 `skills/youyou-card-pipeline` 到该宿主的实际技能目录；Python/Node脚本没有固定Windows路径，但此版尚未在 macOS/Linux 或不同宿主UI上完成端到端实测。

## 依赖与运行方式

构建和计数需 Python 3.9+，只用标准库。渲染和几何检查需 Node.js 20+、Playwright >=1.60.0 <2，以及对应 Chromium 或已安装 Chrome/Edge。优先复用宿主已有运行时；Codex 可以查询 load_workspace_dependencies 返回的真实模块路径。缺依赖才建立独立环境。

在包目录运行下列命令可为 Codex 安装目录下载依赖与 Chromium；WorkBuddy 将 HostTarget 改为 WorkBuddy：
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-runtime.ps1 -HostTarget Codex -InstallChromium
```

此命令会联网下载，不在安装 Skill 时自动执行。已有 Chrome 时可省略 InstallChromium，在渲染命令加 `--channel chrome`。宿主已有 Playwright 时，用 `--playwright-module` 指定经核验的 index.mjs，不需重复下载。

从已安装技能目录运行可复现示例：
```powershell
python .\scripts\build_deck.py --input .\assets\deck.example.json --output .\demo
node .\scripts\render_deck.mjs --html .\demo\index.html --output .\demo\output
node .\scripts\validate_deck.mjs --html .\demo\index.html
```

渲染可选参数：`--channel chrome` / `--channel msedge`、`--playwright-module` 后接已有模块绝对路径、`--report` 后接报告路径。不指定channel时使用Playwright配套Chromium。正式项目把输出目录设在工作区，避免成品混入技能目录。

配文核对：`python scripts/count_body_chars.py` 后接实际 xhs-note.md 路径。要求恰有一组 `### 正文内容` 和 `### 推荐标签`；退出0通过、1超限、2格式错误。仅去除空白，标点也计数，上限不可提高。这个限额只约束该正文块，不代表平台完整发布规则。

环境细节依据 [Playwright 浏览器文档](https://playwright.dev/docs/browsers) 与 [Node 库文档](https://playwright.dev/docs/library)。

## Codex 与 WorkBuddy 的差别

| 项目 | Codex | WorkBuddy |
|---|---|---|
| 内容、模板、脚本 | 同一份 | 同一份 |
| 默认发现目录 | 用户目录/.codex/skills | 用户目录/.workbuddy/skills |
| 调用 | $youyou-card-pipeline | 同名技能，按宿主触发 |
| 文件展示 | 当前会话工具、文件链接，有工具时打开预览 | 有 present_files 时按8PNG+配文展示，否则附件/链接 |
| 日志 | 输出目录交付记录；项目日志按已确认规则 | 相同 |

`agents/openai.yaml` 为 Codex 提供展示信息；通用流程写在 SKILL.md 中，不依赖此元信息才能执行。原 WorkBuddy 的 guizang-social-card-skill 外部依赖已被内置模板和独立脚本替代。两宿主无需互相安装，也无需复制另一宿主的私有历史目录。

## 常见问题与更新恢复

找不到技能：检查实际发现目录、新开会话，并显式指定技能名称。不要把整个技能包直接当成 Skill 放入发现目录，只复制其 skills 子目录中的同名文件夹。

找不到 Playwright：安装依赖，或确认 --playwright-module 指向真实入口。找不到浏览器：安装匹配 Chromium，或明确使用已安装的 Chrome/Edge channel。Windows npm.ps1 被策略阻断时使用 npm.cmd/npx.cmd。

文字溢出：先缩短内容或统一调整候选版式，不逐卡缩字号。字体替换会改变换行，各系统都要重新渲染并逐张查看。报告出现 issues 或非零退出时，不交付为验收完成。

字数错误：检查正文/标签标题是否完整且唯一，超过1000则精简正文。乱码：文件保存UTF-8；Windows旧默认编码下运行校验工具可以加 python -X utf8。

更新：下载新版本后重新运行 install.ps1。恢复：关闭相关宿主，把当前技能文件夹移到另一个备份位置，再把所需 skill-backups 版本复制回技能目录。卸载只移除同名技能文件夹，成品与备份独立保留；恢复旧版后其哈希不同，不能使用新版校验清单宣称一致。

## 安全、隐私与许可

构建脚本转义文本；渲染内置本地模板时阻止 HTTP/HTTPS 请求，不使用外部字体/CDN。脚本仍能读取指定本地文件、写入输出并启动浏览器；HTTP阻断不是任意HTML沙箱。仅渲染授权可信源文件。依赖下载会联网，宿主模型自身数据处理取决于其配置。

默认不发帖、不写公开平台、不索取凭据；文章公开、图片上传、客户资料传播必须另有授权。公共包不含个人原稿、Cookie、Token或历史业务素材。产品事实必须依据当前资料，示例只解释制作流程。

本包遵循仓库MIT许可；Playwright为Apache-2.0依赖，未将其代码打入包。文章、品牌素材、字体和第三方资产的权利需单独确认，仓库许可不替这些资产授权。

## 版本、来源与核验

版本2.0.0；核验日期2026-10-09。当前依据是同包 SKILL.md、三份 references、内置模板与示例、五个脚本及发布清单。原始版本来自用户提供的 WorkBuddy youyou-card-pipeline；通用改造保留字阶与内容约束，新增宿主适配与独立引擎。

已实测：Windows、Python3.12.10、Node24.15.0、宿主已有Playwright1.62.1与Chrome；8图渲染、尺寸/字号/边界校验及逐张目检。字数边界与故意溢出输入的反例检查见 docs/VALIDATION.md。两处安装目录用同一发布文件清单核对。尚未实测：两宿主UI自动发现/展示全流程、其他操作系统、所有可能字体或原文长度。示例通过不保证任意文章直接能放下。
