# Mike Web Clarity Gate Skill

用于网站制作、重构和正式验收的清晰度门禁，核心标准是：标题能一排说清楚就不拆第二排，拒绝泛化的 AI 模板视觉，并保持桌面与移动端布局协调。

## 一键安装

Windows 用户可双击 `install.bat`，或运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装后重启 Codex，并使用：

```text
Use $mike-web-clarity-gate to design or audit this website.
```

## GitHub 安装命令

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --url "https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/mike-web-clarity-gate/skills/mike-web-clarity-gate"
```

## 能力

- `BUILD`：设计前建立清晰度 brief、标题预算、网格和响应式规则。
- `AUDIT`：检查标题行数、横向溢出、首屏比例、AI 模板痕迹与布局平衡。
- `HYBRID`：制作后用同一套标准完成正式验收。
- 提供 Playwright 自动审计脚本和完整人工验收量表。

