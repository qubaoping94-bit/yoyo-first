# Mike Website Production Pipeline

## 最简单调用方式

安装后直接复制：

```text
使用 $mike-website-production-pipeline 全流程制作并验收这个网站。
```

如果项目已经在当前工作区：

```text
使用 $mike-website-production-pipeline 全流程制作并验收当前网站。按照你的推荐直接推进；需要我选择视觉方向或确认最终效果时再停下来，其余阶段自动继续。
```

## 作用

这是 Mike 网站制作总编排 Skill，负责按固定 Gate 组织：

```text
产品定义
→ 唯一视觉来源
→ Figma / 三套视觉方向 / 参考图
→ Hallmark + Taste 设计系统
→ Mike 单行标题和协调布局门禁
→ 灰阶线框
→ 静态高保真实现
→ 同视口 Design QA
→ Motion Spec
→ GSAP 动效
→ 综合 QA
→ 用户批准
→ 母版冻结
→ 发布和生产复验
```

支持六条视觉路线：`FIGMA`、`IDEATE`、`REFERENCE`、`CLONE`、`DNA`、`REDESIGN`。

## 一键安装

Windows 用户可双击 `install.bat`，或运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装后重启 Codex。

## GitHub 安装命令

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --url "https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/mike-website-production-pipeline/skills/mike-website-production-pipeline"
```

## 项目流程文档初始化

安装后可为网站项目创建标准工作文档：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File "$env:USERPROFILE\.codex\skills\mike-website-production-pipeline\scripts\init-website-workflow.ps1" `
  -ProjectRoot "<项目路径>"
```

脚本只创建缺失文件，不覆盖已有记录。它会生成：

- `CURRENT_STATUS.md`
- `SITE_BRIEF.md`
- `VISUAL_SOURCE.md`
- `HEADING_BUDGET.md`
- `LAYOUT_RULES.md`
- `MOTION_SPEC.md`
- `QA_REPORT.md`
- `RELEASE_REPORT.md`

## 核心硬门禁

- 没有唯一视觉事实，不写高保真页面。
- 没有静态视觉通过，不接入复杂 GSAP。
- 标题能一排说清楚，就不拆成第二排。
- 自动测试不能覆盖人工视觉否决。
- 已批准母版不能直接修改，必须创建隔离候选。
- 没有发布授权，不部署生产环境。
