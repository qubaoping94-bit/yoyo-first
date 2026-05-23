# Installation

## Install the Skill

From this package directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

The script copies:

```text
skills/douyin-workflow-skill-publisher
```

to:

```text
%USERPROFILE%\.codex\skills\douyin-workflow-skill-publisher
```

Use a custom skills directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexSkillsDir "D:\my-skills"
```

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

After installation:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -InstalledOnly
```

Restart Codex or open a new session after installing the skill.

## Companion Capabilities

This skill coordinates existing local skills. It works best when these are already installed:

- `douyin-skill-installer`
- `skill-vetter`
- `skill-installer`
- `skill-creator`
- `writing-skills`
- `github-skill-pack-publisher`

If a required companion skill is missing, install it first or continue with the closest local fallback.
