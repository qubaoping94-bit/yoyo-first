---
name: github-skill-pack-publisher
description: Use when a user wants to package Codex/agent skills or reusable workflows, write complete GitHub-ready documentation, create install and verify scripts, generate a zip archive, commit, push, and confirm publication to a GitHub repository.
---

# GitHub Skill Pack Publisher

## Overview

Use this workflow to turn local Codex skills or repeatable agent workflows into polished GitHub repository packages. The default is one independent package per skill; create a combined multi-skill package only when the user explicitly asks for a bundle, collection, or several skills packaged together.

## When to Use

Use for requests like:

- "Upload this skill to my GitHub repo."
- "Package these skills with full documentation."
- "Save this workflow as a skill and publish it."
- "Create a repo-ready skill pack with install scripts and README."
- "I will do many similar operations later; make this a reusable workflow."

Do not use for a normal code push that does not involve packaging skills, reusable workflows, install docs, or release-style repository structure.

## Required Inputs

Discover these from the user's message, screenshot, browser page, local git config, or current workspace:

- Target GitHub repository URL or `owner/repo`.
- Skill names or workflow names to package.
- Whether to include only custom skills or also install companion skills from upstream sources.
- Preferred local package folder and zip location.
- Whether to push directly, prepare a local repo only, or provide manual upload instructions.

If the repo URL cannot be inferred safely, ask for it before pushing.

## Default Packaging Rule

- Default: one skill becomes one independent skill package.
- If the user asks to publish 3 skills, create 3 separate package folders and 3 separate archives unless they explicitly request a combined bundle.
- Only create a multi-skill package when the user explicitly asks to combine, bundle, merge, package together, or create one shared package containing multiple skills.
- The root of a GitHub repository may act as an index, but it should not pretend to be a combined package unless the user asked for that.

## Standard Single-Skill Package Structure

Use this structure unless the target repo already has a strong convention:

```text
skill-packs/<skill-name>/
  skills/
    <skill-name>/
      SKILL.md
      agents/openai.yaml
  scripts/
    install.ps1
    install-companion-skills.ps1
    verify.ps1
  manifest/
    skill-pack.json
    companion-skills.json
  docs/
    FEATURES.md
    INSTALLATION.md
    WORKFLOWS.md
    SECURITY.md
  examples/
    prompts.md
  README.md
```

For a multi-skill bundle requested explicitly by the user, place multiple skill folders under `skills/` and label the package `type` as `multi-skill-pack` in the manifest.

## Workflow

1. **Inspect environment**
   - Check current directory, `git status`, `git remote -v`, `git config user.name`, and `git config user.email`.
   - Check whether `gh` exists, but do not require it. Git HTTPS push is enough when credentials are available.
   - If a browser screenshot shows a GitHub repo, infer `owner/repo` only when the URL/repo name is unambiguous.

2. **Collect skill sources**
   - Copy custom skill folders from the local Codex skills directory, usually `%USERPROFILE%\.codex\skills`.
   - Include `SKILL.md` and `agents/openai.yaml`.
   - Do not vendor large third-party companion skills unless the user explicitly asks. Prefer a companion manifest and installer script pointing to official upstream repos.
   - For multiple skills, repeat the package structure independently for each skill unless the user explicitly asked for one combined bundle.

3. **Write comprehensive repository docs**
   - `README.md`: purpose, skill list, quick install, quick verify, docs links, GitHub upload notes.
   - `docs/FEATURES.md`: full feature description for every included skill.
   - `docs/INSTALLATION.md`: local install, companion install, execution policy fallback, restart/new-session note.
   - `docs/WORKFLOWS.md`: repeated workflows and routing rules.
   - `docs/SECURITY.md`: source vetting, secrets, cloud credentials, destructive actions, upload hygiene.
   - `docs/GITHUB_UPLOAD.md`: push instructions and manual upload fallback.
   - `examples/prompts.md`: realistic prompts the user can reuse.
   - `THIRD_PARTY_NOTICES.md`: list upstream repos for companion skills.

4. **Add scripts and manifests**
   - `scripts/install.ps1` copies packaged skills into the local Codex skills directory.
   - `scripts/install-companion-skills.ps1` installs upstream companion skills through the local Codex skill installer.
   - `scripts/verify.ps1` validates packaged skills and, optionally, installed skills.
   - `manifest/skill-pack.json` lists packaged skills and purpose.
   - `manifest/companion-skills.json` lists upstream companion skills, repo, path, install name, and phase.
   - `.github/workflows/validate.yml` runs repository structure validation.

5. **Validate locally**
   - Run PowerShell scripts with execution-policy fallback when needed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

   - If Codex `quick_validate.py` exists, validate every packaged skill with `PYTHONUTF8=1`.
   - Fix validator errors before upload.

6. **Create zip archives**
   - Generate one `<skill-name>-skill-pack.zip` per independent package.
   - For explicit combined bundles, generate one `<package-name>.zip` beside the package directory.
   - Exclude `.git` folders and sensitive files.
   - Report all absolute zip paths.

7. **Publish to GitHub**
   - If pushing to an existing repo, clone to a clean temporary/local upload directory.
   - Copy package contents into the clone.
   - Preserve unrelated remote files unless the user asked to replace the repo.
   - Commit with a clear message, then push.
   - If push fails because credentials are missing, leave the prepared local repo intact and provide exact push/manual upload steps.

8. **Confirm remote state**
   - Run `git ls-remote origin main` or the target branch.
   - Open or fetch the GitHub repo page when possible and confirm key directories are visible.
   - Report latest commit hashes and links.

## Git Safety Rules

- Never use destructive git commands such as `reset --hard` or forced push unless explicitly requested.
- Before copying over an existing clone, prefer a fresh clone or a timestamped upload directory.
- Do not commit `.env`, tokens, cookies, browser session files, or private project code unrelated to the package.
- If remote has existing content, pull/clone first and merge through normal git history.
- Keep commit messages specific, for example `Add Codex AI product skill kit` or `Add GitHub skill pack publisher workflow`.

## Verification Checklist

Before final response, confirm:

- The local packaged skills validate.
- The zip exists and has a nonzero size.
- Git working tree is clean after commit, or explain remaining changes.
- Push succeeded, or upload fallback is ready.
- Remote branch hash matches the pushed commit.
- README and key directories are visible remotely when browsing is available.

## Final Response

Respond in the user's language. Include:

- Repository URL.
- New or updated skill names.
- Commit hash or hashes.
- Zip path.
- Validation results.
- Any manual action still required, such as restarting Codex or checking GitHub Actions.
