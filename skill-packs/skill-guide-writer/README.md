# skill-guide-writer

> **最简单调用方式——安装后直接复制：**

```text
用 $skill-guide-writer 全面总结目标 Skill，并在桌面生成中文 Markdown 使用说明。
```

`skill-guide-writer` 是一个证据驱动的 Skill 使用说明生成器。它会完整读取目标 `SKILL.md` 和直接相关资料，核验能力、安装命令、官方仓库、在线画廊、限制与安全边界，再输出一份第一屏即可调用、可独立阅读的中文 Markdown 指南。

## 核心特点

- 支持本地 Skill、`SKILL.md`、GitHub 仓库、市场页和现有说明文档。
- 第一屏固定放置可直接复制的最简调用指令。
- 区分已确认能力、环境依赖能力、未验证内容和合理推断。
- 包含安全目录盘点脚本，主动跳过敏感文件并清理 URL 查询参数。
- 使用统一模板和 P0/P1/P2 门禁检查完整性、准确性与可维护性。
- 默认输出简体中文详细版，可按语言、读者和输出位置调整。

## 安装

在本技能包目录执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装后重启 Codex 或新建任务，让 Skill 进入自动发现列表。

## 验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

验证已安装副本：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -InstalledOnly
```

## 文档

- [功能说明](docs/FEATURES.md)
- [安装与验证](docs/INSTALLATION.md)
- [标准工作流](docs/WORKFLOWS.md)
- [安全边界](docs/SECURITY.md)
- [示例提示词](examples/prompts.md)
- [文档输出模板](skills/skill-guide-writer/assets/skill-guide-template.md)
- [详细质量规范](skills/skill-guide-writer/references/guide-spec.md)

## 包结构

```text
skill-guide-writer/
├── skills/skill-guide-writer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/skill-guide-template.md
│   ├── references/guide-spec.md
│   └── scripts/inventory_skill.py
├── scripts/
│   ├── install.ps1
│   └── verify.ps1
├── manifest/skill-pack.json
├── docs/
└── examples/prompts.md
```

## 当前版本

- 技能包版本：`1.0.0`
- 类型：独立单 Skill 包
- 运行依赖：Codex 或兼容 Agent；安全盘点脚本需要 Python 3
- 许可证：继承仓库根目录的 MIT License
