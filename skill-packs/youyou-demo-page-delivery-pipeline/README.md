# youyou-demo-page-delivery-pipeline

独立技能包：优优无机板演示系统页面交付流水线。

这个 skill 用于把“参考图或主题”转成一套可长期复用的交付流程：生成主图、制作发布会全屏 HTML、接入产品演化总站、刷新网站总汇和微信分享素材、部署 Cloudflare Pages，并完成公开审计和记忆收尾。

## 适合场景

- 继续制作“优优无机板...专项演示系统”
- 从参考海报提炼卖点，转成小黑长卷或发布会演示页
- 把新演示页接入 `youyou-ai-gallery.pages.dev/product-evolution/`
- 需要同时生成本地文件、公开链接、分享话术和审计证据

## 安装

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装后建议重启 Codex 或新开会话，让新 skill 进入可用技能列表。

## 验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

## 文档

- [功能说明](docs/FEATURES.md)
- [安装说明](docs/INSTALLATION.md)
- [工作流说明](docs/WORKFLOWS.md)
- [安全说明](docs/SECURITY.md)
- [GitHub 上传说明](docs/GITHUB_UPLOAD.md)
- [示例提示词](examples/prompts.md)

