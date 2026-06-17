# Youyou Inorganic Board Guide

This package installs one Codex skill that acts as a customer/dealer-facing product consultant for Youyou inorganic board. It is designed as a high-touch guide, not a document dump: it classifies the user intent, chooses a service mode, answers with polished customer-ready wording, and routes people to the right public Youyou website.

## Included Skill

- `youyou-inorganic-board-guide` - explains the Youyou inorganic-board product system, answers common customer/dealer questions, drafts forwarding copy, handles专项答疑, supports selection and showroom scenarios, protects claim quality, and routes users to public Youyou websites, galleries, moments copy, and product-evolution demo pages.

## Quick Install

Run from this package folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

Restart Codex or open a new Codex session after installing so the skill list refreshes.

## Quick Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

To also check current public website links:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -CheckLinks
```

The normal verification also runs the packaged skill smoke test, which checks required references, output guidance, prompt metadata, and template cleanup.

## Typical Prompt

```text
Use $youyou-inorganic-board-guide to introduce Youyou inorganic board and recommend the right public website links for a dealer to send to a customer.
```

## Documentation

- `docs/FEATURES.md` - what the skill covers
- `docs/INSTALLATION.md` - local install and verification details
- `docs/WORKFLOWS.md` - repeatable customer/dealer guidance flows
- `docs/SECURITY.md` - public-material and claim boundaries
- `docs/GITHUB_UPLOAD.md` - upload and manual fallback notes

## Repository

Target repository: `https://github.com/qubaoping94-bit/yoyo-first`
