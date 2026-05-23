# GitHub 上传说明

## 情况 1：你已经有一个空 GitHub 仓库

在 GitHub 创建一个空仓库，例如：

```text
https://github.com/<your-name>/codex-ai-product-skill-kit
```

然后在本地运行：

```powershell
cd "D:\桌面应用软件下载库\OneDrive\Desktop\two\codex-ai-product-skill-kit"
git remote add origin https://github.com/<your-name>/codex-ai-product-skill-kit.git
git branch -M main
git push -u origin main
```

## 情况 2：远程仓库已经有 README 或其他文件

先拉取远程内容：

```powershell
git remote add origin https://github.com/<your-name>/<repo>.git
git pull origin main --allow-unrelated-histories
```

如果出现冲突，先解决冲突，再提交：

```powershell
git add .
git commit -m "Resolve initial merge"
git push -u origin main
```

## 情况 3：没有安装 GitHub CLI

本机没有 `gh` 命令也没关系，可以使用普通 Git HTTPS 推送。

第一次 push 时 GitHub 可能要求登录。现在 GitHub 通常不接受账户密码推送，需要：

- Git Credential Manager 浏览器登录，或
- Personal Access Token

## 情况 4：想用网页上传

也可以直接上传压缩包：

1. 打开 GitHub 仓库页面。
2. 点击 `Add file`。
3. 选择 `Upload files`。
4. 上传 `codex-ai-product-skill-kit.zip`。
5. 填写 commit message。
6. 点击 `Commit changes`。

推荐还是用 Git 推送，因为目录结构和后续更新更清晰。

