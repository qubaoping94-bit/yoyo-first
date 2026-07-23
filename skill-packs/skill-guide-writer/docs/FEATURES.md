# 功能说明

`skill-guide-writer` 用于把分散在 `SKILL.md`、README、示例、脚本、仓库和官网中的信息，整理成可直接交付的中文 Markdown 使用说明。

## 核心能力

### 证据驱动审计

- 完整读取目标 `SKILL.md`。
- 按需读取 agent metadata、README、manifest、示例、模板、脚本和直接引用资料。
- 优先采用本地 canonical source 和官方一手资料。
- 对版本、数量、安装命令、平台兼容、许可证和在线地址进行动态核验。
- 冲突无法解决时标记“待官方确认”，不把猜测写成事实。

### 安全目录盘点

`scripts/inventory_skill.py` 会生成 JSON 清单，包括：

- Skill 名称和 description；
- 文件路径、字节数和 SHA-256；
- Markdown 标题结构；
- 移除查询参数后的公开 URL 候选。

脚本默认跳过 `.git`、`node_modules`、虚拟环境、构建目录、缓存以及文件名疑似包含 Secret、Token、Cookie、Credential、API Key 或私钥的内容。

### 自适应文档结构

默认覆盖：

- 第一屏最简调用；
- Skill 定义、价值和核心能力；
- 适合与不适合的场景；
- 输入和输出；
- 使用路线和选择建议；
- 多组可复制调用指令；
- 标准工作流程；
- 安装、发现、验证与排错；
- 依赖、限制、安全与授权；
- 官方地址、版本、核验依据和未确认项。

不适用的章节会被删除，不会用虚构内容填充模板。

### P0/P1/P2 质量门禁

- **P0**：第一屏调用、来源完整、无臆测、无敏感信息、UTF-8 可读。
- **P1**：动态信息当前可核验、复杂功能有路线和调用示例、安装与排错清楚。
- **P2**：记录最后核验日期，集中管理易变信息，分离未验证内容。

## 支持的目标

- 本机已安装 Codex/Claude Code/Agent Skill；
- 本地 `SKILL.md` 或 Skill 文件夹；
- GitHub Skill 仓库或子目录；
- Skill 市场、官方文档或演示页面；
- MCP、插件和可复用 Agent 工作流；
- 需要重新核验的现有 Markdown 使用说明。
