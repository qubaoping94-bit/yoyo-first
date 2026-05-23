# 安装说明

## 前置条件

- Windows PowerShell
- Codex 本地 skill 目录：`%USERPROFILE%\.codex\skills`
- Python，可选但推荐，用于运行 Codex skill validator 和官方 skill installer
- Git，可选，用于从 GitHub 安装配套 skill

## 安装自定义 skill

在项目根目录运行：

```powershell
.\scripts\install.ps1
```

如果 Windows 禁止运行 `.ps1`：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

默认会复制：

- `skills/ai-product-delivery-pipeline`
- `skills/douyin-skill-installer`

到：

```text
C:\Users\<你>\.codex\skills
```

## 同时安装配套 skill

```powershell
.\scripts\install.ps1 -WithCompanions
```

这会额外调用：

```powershell
.\scripts\install-companion-skills.ps1
```

并安装：

- `vercel-react-best-practices`
- `web-design-guidelines`
- `microsoft-foundry`
- `azure-ai`
- `azure-aigateway`
- `azure-prepare`
- `azure-validate`
- `azure-deploy`

## 只安装配套 skill

```powershell
.\scripts\install-companion-skills.ps1
```

该脚本依赖本机已有 Codex 的官方 `skill-installer`：

```text
%USERPROFILE%\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py
```

如果这个文件不存在，需要先在 Codex 中安装/恢复系统 skill installer。

## 安装后验证

```powershell
.\scripts\verify.ps1
```

如果 Windows 禁止运行 `.ps1`：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

如果看到每个 skill 都显示 `OK` 或 `Skill is valid!`，说明安装正常。

## 让 Codex 识别新 skill

安装后需要：

- 重启 Codex，或
- 新开一个会话

这样新 skill 才会进入当前可用 skill 列表。
