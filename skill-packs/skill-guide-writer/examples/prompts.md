# 示例提示词

## 最简调用

```text
用 $skill-guide-writer 全面总结 video-shotcraft，并在桌面生成中文 Markdown 使用说明。
```

## 根据本地路径总结

```text
用 $skill-guide-writer 审计 C:\Users\<用户名>\.codex\skills\<skill-name>，完整读取它的 SKILL.md 和直接相关资料，在桌面生成详细中文使用说明。
```

## 根据 GitHub 地址总结

```text
用 $skill-guide-writer 全面总结这个 GitHub Skill：<仓库 URL>。核验核心能力、安装方式、官方演示、在线画廊、许可证和限制，并生成中文 Markdown 文档。
```

## 推荐完整调用

```text
用 $skill-guide-writer 全面审计 <Skill 名称或地址>。必须完整读取 SKILL.md 和直接相关资料，核验官方仓库、在线演示、安装命令与动态信息，区分已确认能力、环境依赖能力和未验证内容；面向非技术用户生成详细中文 Markdown，第一屏先放可直接复制的最简调用指令，最后执行 P0、P1、P2 质量检查。
```

## 只读安全审计

```text
用 $skill-guide-writer 总结 <Skill 名称或地址>，只执行只读审计和安全的本地验证；不得读取或回显 Secret、Token、Cookie、API Key，不得调用真实 Provider，不得安装、部署或执行外部平台写入。
```

## 更新现有文档

```text
用 $skill-guide-writer 更新 <现有 Markdown 路径>。重新核验目标 Skill 的当前 SKILL.md、官方仓库、版本、安装命令和在线地址；保留仍然正确的内容，只修改有证据支持的过时信息，并列出无法确认的项目。
```

## 多个 Skill 分别整理

```text
用 $skill-guide-writer 分别总结下面这些 Skill，每个 Skill 独立生成一份中文 Markdown 使用说明，统一结构但不得在不同 Skill 之间复用未经核验的能力描述：<Skill 清单>。
```
