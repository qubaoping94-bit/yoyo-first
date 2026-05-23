# 安装说明

## 安装主 skill

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装到：

```text
%USERPROFILE%\.codex\skills\ai-product-delivery-pipeline
```

## 安装主 skill + 配套 skill

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -WithCompanions
```

配套 skill 会从 Vercel 和 Microsoft 官方仓库安装。

## 验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

安装后重启 Codex 或新开会话。

