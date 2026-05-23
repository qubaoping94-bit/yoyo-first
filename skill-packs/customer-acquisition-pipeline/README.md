# customer-acquisition-pipeline

Independent skill pack for a Codex-managed customer acquisition pipeline.

This pack turns the Douyin workflow "just-scrape + lark-base + cold-email" into one reusable orchestration skill. The skill helps Codex find public leads, normalize them into a Lark Base CRM table, and draft personalized cold outreach without sending anything by default.

## Included Skill

- `customer-acquisition-pipeline`: orchestrates public lead acquisition, Lark Base CRM updates, and cold-email draft generation.

## Companion Skills

Install these when you want the full workflow:

- `just-scrape` from `ScrapeGraphAI/just-scrape`
- `lark-shared` from `larksuite/cli`
- `lark-base` from `larksuite/cli`
- `cold-email` from `coreyhaines31/marketingskills`

## Install

Install the orchestration skill:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

Install the companion skills:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-companion-skills.ps1
```

Verify the packaged skill:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Restart Codex or open a new session after installation so the new skill list is refreshed.

## Documentation

- [Features](docs/FEATURES.md)
- [Installation](docs/INSTALLATION.md)
- [Workflows](docs/WORKFLOWS.md)
- [Security](docs/SECURITY.md)
- [GitHub upload notes](docs/GITHUB_UPLOAD.md)
- [Prompt examples](examples/prompts.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
