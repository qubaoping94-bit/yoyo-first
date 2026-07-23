# 安装与验证

## 一键安装

在 `skill-packs/skill-guide-writer` 目录执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

默认安装到：

```text
%USERPROFILE%\.codex\skills\skill-guide-writer
```

指定其他 Codex Skills 目录：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexSkillsDir 'D:\custom\skills'
```

安装后重启 Codex 或新建任务，以刷新 Skill 列表。

## 验证技能包

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

验证脚本会：

1. 检查 5 个必要文件；
2. 在可用时运行 Codex `quick_validate.py`；
3. 运行 `inventory_skill.py` 自盘点；
4. 核对 Skill 名称与文件数量。

## 验证已安装副本

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -InstalledOnly
```

自定义安装目录：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -InstalledOnly -CodexSkillsDir 'D:\custom\skills'
```

## 手动安装

完整复制：

```text
skills\skill-guide-writer
```

到：

```text
%USERPROFILE%\.codex\skills\skill-guide-writer
```

不要只复制 `SKILL.md`。`assets`、`references` 和 `scripts` 都属于必要运行资源。

## 运行条件

- Codex 或能够读取 `SKILL.md` 的兼容 Agent；
- Python 3.9 或更高版本，用于安全盘点脚本；
- 网络为可选条件，仅在核验当前官方在线资料时需要。

## Windows 编码说明

验证脚本已设置 `PYTHONUTF8=1`。手动运行 Python 工具遇到 GBK 解码错误时，先执行：

```powershell
$env:PYTHONUTF8='1'
```
