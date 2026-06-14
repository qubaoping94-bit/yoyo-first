# Installation

## Local Install

From this package folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

The script copies `skills/youyou-special-demo-delivery-pipeline` into:

```text
%USERPROFILE%\.codex\skills\youyou-special-demo-delivery-pipeline
```

Open a new Codex session after installation.

## Verify Package

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

The verifier checks package structure, required skill files, frontmatter, docs, scripts, manifests, and optional local installation.

## Companion Skills

The workflow works best when these skills are already available:

- `youyou-special-demo-system`
- `ian-xiaohei-scenes`
- `html-production-defaults`
- `github-skill-pack-publisher`

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-companion-skills.ps1
```

This script only checks and reports companion skill presence. It does not download third-party code automatically.

