# Installation

## Install the Orchestration Skill

From this package directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

By default the script copies:

```text
skills/customer-acquisition-pipeline
```

to:

```text
%USERPROFILE%\.codex\skills\customer-acquisition-pipeline
```

You can pass a custom skills directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexSkillsDir "D:\my-skills"
```

## Install Companion Skills

For the full Douyin workflow:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-companion-skills.ps1
```

The companion installer uses the local Codex skill installer script and official GitHub sources:

- `ScrapeGraphAI/just-scrape`, `skills/just-scrape`
- `larksuite/cli`, `skills/lark-shared`
- `larksuite/cli`, `skills/lark-base`
- `coreyhaines31/marketingskills`, `skills/cold-email`

## External CLI Setup

Some companion skills require additional tools:

- `just-scrape` expects the `just-scrape` CLI and `SGAI_API_KEY`.
- `lark-base` expects `lark-cli` and working Lark/Feishu authentication.
- `cold-email` is a writing skill and does not need an email sending provider.

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

After install:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -InstalledOnly
```

Restart Codex or open a new session after installing new skills.
