# GitHub 上传说明

本包已按仓库标准结构放置在：

```text
skill-packs/youyou-demo-page-delivery-pipeline
```

## 推荐发布方式

```powershell
git add skill-packs/youyou-demo-page-delivery-pipeline README.md
git commit -m "Add Youyou demo page delivery skill pack"
git push origin main
```

## 手动上传备选

如果 Git 凭据不可用，可以把本地 zip 上传到 GitHub，或在网页端把整个 `skill-packs/youyou-demo-page-delivery-pipeline` 目录内容逐项上传。

上传后运行仓库 Actions，或本地执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\skill-packs\youyou-demo-page-delivery-pipeline\scripts\verify.ps1
```

