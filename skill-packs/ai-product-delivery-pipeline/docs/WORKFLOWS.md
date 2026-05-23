# 工作流

## 从想法到上线

1. 明确产品类型、用户、AI 能力、数据和安全边界。
2. 制定交付计划和验收标准。
3. 实现或改造应用。
4. 检查 React/Next.js 工程质量。
5. 打磨 UI/UX。
6. 设计 Foundry/Agent/评测架构。
7. 接入 Azure AI 服务。
8. 需要治理时加入 AI Gateway。
9. 使用 `azure-prepare` 生成部署计划和基础设施。
10. 使用 `azure-validate` 做预检。
11. 使用 `azure-deploy` 上线并验证 URL。

## 只做部分阶段

- 只做前端：停在 React + UX 阶段。
- 只做 AI 架构：停在 Foundry/Azure AI 阶段。
- 只做部署：先检查 `.azure/deployment-plan.md`，没有则 prepare，有但未验证则 validate。

