# Installation

## Install Locally

Run from the package folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

By default, the script installs to:

```text
%USERPROFILE%\.codex\skills\youyou-inorganic-board-guide
```

Use a custom skills root if needed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -SkillsRoot "C:\Users\you\.codex\skills"
```

Open a new Codex session after installing so the skill list refreshes.

## Verify The Package

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

This checks the package structure and runs the skill smoke test.

To verify the installed copy as well:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -CheckInstalled
```

To check public links:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -CheckLinks
```

## No Companion Skills

This package has no companion skill dependency. It is intentionally lightweight and only contains selected public-facing guidance plus website routing.
