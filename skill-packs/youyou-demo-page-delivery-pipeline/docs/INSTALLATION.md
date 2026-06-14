# 安装说明

## 一键安装

在本目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

脚本会把 `skills\youyou-demo-page-delivery-pipeline` 复制到：

```text
%USERPROFILE%\.codex\skills\youyou-demo-page-delivery-pipeline
```

## 指定安装目录

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexSkillsDir "C:\Users\11434\.codex\skills"
```

## 伴随 skill

该流水线在实际制作页面时通常还会使用：

- `youyou-special-demo-system`
- `ian-xiaohei-scenes`
- `html-production-defaults`

运行下面命令可检查这些伴随 skill 是否已存在：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-companion-skills.ps1
```

## 安装后

重启 Codex 或新开会话，让 skill 列表刷新。

