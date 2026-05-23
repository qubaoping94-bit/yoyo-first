# 工作流说明

## 工作流 A：AI 产品从想法到上线

触发方式：

```text
用 ai-product-delivery-pipeline 帮我把这个 AI 产品从想法做到可上线版本。
```

执行顺序：

1. 需求澄清：产品类型、用户、AI 能力、数据、安全、预算、上线目标。
2. 工程计划：拆分任务、验收标准、测试策略。
3. 产品实现：开发或改造项目。
4. React 质量检查：调用 `vercel-react-best-practices`。
5. UI/UX 打磨：调用 `frontend-design` 和 `web-design-guidelines`。
6. AI 架构：调用 `microsoft-foundry`。
7. Azure AI：调用 `azure-ai`。
8. AI 网关治理：需要限流、缓存、安全、成本控制时调用 `azure-aigateway`。
9. Azure 准备：调用 `azure-prepare`。
10. Azure 验证：调用 `azure-validate`。
11. Azure 部署：调用 `azure-deploy`。
12. 交付报告：输出 URL、测试结果、风险和后续动作。

## 工作流 B：已有 demo 产品化

触发方式：

```text
这个 demo 已经能跑了，帮我变成可交付的 AI 产品。
```

重点：

- 先读现有代码，不重写已有功能。
- 补齐状态、错误处理、测试、日志、环境变量。
- 检查 React/Next.js 性能。
- 检查 UI 的移动端、空状态、错误状态、加载状态。
- 根据需要接入 Azure AI 或 Foundry。
- 只有用户明确要上线时，才进入 Azure 准备/验证/部署。

## 工作流 C：抖音视频安装 skill

触发方式：

```text
根据这个抖音链接安装里面提到的 skill。
```

执行顺序：

1. 提取视频页面内容。
2. 识别视频中提到的 skill。
3. 查本地是否已安装。
4. 查 curated skill list。
5. 查官方 GitHub 来源。
6. 安全核验。
7. 安装。
8. 验证。
9. 输出安装清单和来源。

## 工作流 D：只做部署

触发方式：

```text
把这个项目部署到 Azure。
```

路由规则：

- 如果没有 `.azure/deployment-plan.md`，先用 `azure-prepare`。
- 如果已有 plan 但没有验证 proof，先用 `azure-validate`。
- 只有 plan 已验证后，才用 `azure-deploy`。

这能避免跳过准备和验证直接上线导致失败。

## 工作流 E：打包并发布 skill 到 GitHub

触发方式：

```text
把刚刚这个工作流程保存成 skill，并打包上传到我的 GitHub 仓库，说明要全面。
```

执行顺序：

1. 确认目标 GitHub 仓库和分支。
2. 创建或更新本地 skill。
3. 把 skill 复制进 `skills/` 目录。
4. 更新 README、功能说明、安装说明、工作流、安全说明、示例提示词和 manifest。
5. 增加或更新安装脚本、验证脚本和 GitHub Actions。
6. 运行本地验证。
7. 生成 zip 包。
8. 克隆或更新远程 GitHub 仓库。
9. commit 并 push。
10. 使用 `git ls-remote` 或网页确认远程更新。

注意：

- 没有 GitHub CLI 也可以用普通 Git HTTPS 推送。
- 不提交 `.env`、token、cookie、私有源码等敏感文件。
- 如果认证失败，保留本地准备好的仓库并输出手动上传步骤。
