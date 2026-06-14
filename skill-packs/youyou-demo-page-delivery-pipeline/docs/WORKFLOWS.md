# 工作流说明

## 标准交付顺序

1. 读取 Obsidian 记忆入口和优优无机板项目记忆。
2. 根据用户参考图或主题确认标题、slug、卖点和禁区。
3. 生成或修订主图，并检查视觉和文字。
4. 制作黑场发布会式全屏 HTML。
5. 追加 `scripts\product-evolution-pages.config.json`。
6. 更新 `scripts\site-directory-common.cjs` 和 `scripts\build-wechat-share-poster.cjs`。
7. 运行分享素材、网站总汇和产品站构建脚本。
8. 用桌面端和移动端检查页面。
9. 部署到 `youyou-ai-gallery`、`youyou-wuji-space-ai`、`youyou-sites-list`。
10. 运行公开审计并记录 `issueCount=0`。
11. 更新长期记忆，最后用中文汇报公开 URL、本地路径、验证结果和记忆变更。

## 常用触发语

- “做一个优优无机板...专项演示系统”
- “继续工作，把这个演示页上线”
- “参考这些图，生成同系列发布会 HTML”
- “把这套流程接入产品演化总站”
- “当前任务完成后，把工作流写成 skill”

## 交付质量标准

- 主图是第一视觉，不做营销落地页式堆砌。
- 页面比例跟随真实主图尺寸，不为了固定比例强行补白。
- 移动端标题和全屏按钮不能重叠。
- 分享图和微信话术要跟公开 URL 同步更新。
- 审计失败时先修复再部署，不把失败状态当完成。

