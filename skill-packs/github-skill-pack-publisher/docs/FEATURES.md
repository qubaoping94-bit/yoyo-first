# 功能说明

`github-skill-pack-publisher` 用于把 skill 发布流程标准化。

## 能力

- 创建或更新本地 skill。
- 默认按单 skill 独立包生成仓库结构。
- 写完整 README、功能说明、安装说明、工作流、安全说明和示例提示词。
- 生成安装脚本、验证脚本、manifest 和 GitHub Actions。
- 本地验证 `Skill is valid!`。
- 生成 zip。
- clone GitHub 仓库、commit、push。
- 用远程 hash 或网页确认上传成功。

## 默认打包策略

默认：一个 skill 一个独立技能包。

只有当用户明确说“把这些 skill 合并成一个包”“做合集包”“打包在一起”时，才使用多 skill 合集结构。

