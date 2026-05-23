# GitHub Upload Notes

This package follows the repository default: one independent skill package per skill.

Recommended location:

```text
skill-packs/customer-acquisition-pipeline
```

Recommended release artifact:

```text
customer-acquisition-pipeline-skill-pack.zip
```

Before pushing:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Do not upload:

- `.env`
- API keys
- cookies
- exported lead lists
- private Lark Base data
- browser profiles
