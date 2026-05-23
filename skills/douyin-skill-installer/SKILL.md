---
name: douyin-skill-installer
description: Use when a user provides a Douyin/TikTok China link, share text, or video summary and asks to identify, install, update, or explain Codex/agent skills mentioned in the video.
---

# Douyin Skill Installer

## Overview

Turn a Douyin skill-recommendation video into installed local Codex skills. The job is to extract the video's actual content, identify the named skills, map marketing names to real skill packages, vet sources, install, and verify.

## Workflow

1. **Extract the video content**
   - Use the local `douyin-to-launch-html` workflow first when available.
   - If Douyin blocks metadata or asks for fresh cookies, resolve the short link and use a real browser or Playwright fallback to inspect the page title, captions, transcript, chapters, and visible text.
   - Keep the raw extracted evidence long enough to cite the skill names and avoid guessing from the URL alone.

2. **Identify candidate skills**
   - Extract all names near terms like `skill`, `Codex Skill`, `agent skill`, `MCP`, `workflow`, `install`, and `project pipeline`.
   - Normalize natural names into likely folder names, but do not assume the spoken/display name is the install name.
   - Build a mapping table: `video name -> likely package -> source repo/path -> confidence`.

3. **Find install sources**
   - Check already installed local skills first to avoid duplicates.
   - Check curated skill lists with the local `skill-installer` scripts.
   - If a skill is not curated, search for official or high-trust repositories. Prefer repos from the product owner or the organization named in the video.
   - Use exact skill `name:` from `SKILL.md` frontmatter as the install name when possible.

4. **Vet before GitHub install**
   - Use `skill-vetter` principles before installing from GitHub.
   - Inspect repo owner, activity, license, target paths, `SKILL.md`, scripts, and suspicious patterns such as hidden credential capture, browser cookie access, destructive commands, unexpected network fetches, or self-modifying installers.
   - Treat cloud-deployment skills that mention credentials, tokens, or CLI login as medium risk by default; install only if the content is documentation/workflow-oriented and the source is trusted.
   - Stop and ask the user before installing high-risk, unclear, abandoned, or unofficial candidates.

5. **Install**
   - Use `skill-installer` for curated or GitHub installs.
   - Install each skill into the user's Codex skills directory.
   - If the destination exists, report it as already installed unless the user explicitly asked to update.
   - When installing from a multi-skill repo, pass the exact subpath and use `--name` only when needed to preserve the skill's frontmatter name.

6. **Verify and clean up**
   - Confirm each installed directory has a readable `SKILL.md`.
   - Read the first lines of each installed `SKILL.md` to confirm `name:` and `description:`.
   - Remove temporary clone/vetting folders only after verifying their resolved paths are inside the intended workspace.
   - Tell the user that a Codex restart or new session may be needed before newly installed skills appear in the active skill list.

## Decision Rules

- Do not install from a Douyin claim alone. Always connect the named skill to a concrete package or repo path.
- If multiple packages match, choose the official owner first; otherwise present options and ask.
- If a video gives an ordered workflow, preserve the order in the final summary.
- If extraction fails completely, report the blocker and ask for a screenshot, transcript, or video text instead of inventing names.
- If a mentioned skill depends on missing companion skills, call that out in the final result.

## Common Commands

Use the local skill installer scripts when present:

```powershell
python C:\Users\11434\.codex\skills\.system\skill-installer\scripts\list-skills.py --format json
python C:\Users\11434\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo owner/repo --path path/to/skill
```

For GitHub installs with a custom destination name:

```powershell
python C:\Users\11434\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo owner/repo --path path/to/skill --name actual-skill-name
```

## Example Mapping

For the video "5 Codex Skill project production line":

| Video name | Installed skill | Source |
|---|---|---|
| Vercel React | `vercel-react-best-practices` | `vercel-labs/agent-skills`, `skills/react-best-practices` |
| Web Design | `web-design-guidelines` | `vercel-labs/agent-skills`, `skills/web-design-guidelines` |
| Foundry | `microsoft-foundry` | `microsoft/github-copilot-for-azure`, `plugin/skills/microsoft-foundry` |
| Azure AI | `azure-ai` | `microsoft/github-copilot-for-azure`, `plugin/skills/azure-ai` |
| Azure Deploy | `azure-deploy` | `microsoft/github-copilot-for-azure`, `plugin/skills/azure-deploy` |

## Final Response

Summarize in Chinese when the user is Chinese:

- what was extracted from the video,
- what was installed or already present,
- any skipped/uncertain items and why,
- source repos used,
- verification result,
- restart/new-session note.
