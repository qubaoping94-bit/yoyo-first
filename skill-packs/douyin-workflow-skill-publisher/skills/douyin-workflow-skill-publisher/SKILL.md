---
name: douyin-workflow-skill-publisher
description: Use when a user provides a Douyin/TikTok China link, share text, video summary, or screenshot and asks to install mentioned Codex/agent skills, determine whether they form a reusable workflow, create a combined workflow skill, package it independently, and upload or prepare it for GitHub.
---

# Douyin Workflow Skill Publisher

## Overview

Turn a Douyin skill-recommendation video into a reusable Codex workflow skill and an independent GitHub-ready skill pack. This is a higher-level workflow that coordinates extraction, skill installation, workflow synthesis, skill creation, packaging, validation, and publication.

## Required Sub-Skills

Use these skills when available:

- `douyin-skill-installer` for extracting the video, identifying named skills, mapping them to sources, vetting, installing, and verifying.
- `skill-vetter` before installing any unknown GitHub skill.
- `skill-installer` for curated or GitHub skill installation.
- `skill-creator` and `writing-skills` when creating the new workflow skill.
- `github-skill-pack-publisher` when packaging, zipping, committing, pushing, or confirming publication.

Use `douyin-to-launch-html`, a browser, or Playwright when Douyin blocks metadata, captions, or visible text extraction.

## Trigger Examples

- "根据这个抖音链接安装其中的 skill，如果能组成工作流就生成组合 skill 并上传 GitHub。"
- "把刚才抖音里这几个 skill 串起来，以后我经常做这种任务。"
- "从这个视频提取 skill，安装，组合成 workflow，再做成独立技能包。"
- "复制打开抖音，看看里面提到的 skill，安装并打包发布。"

## Workflow

1. **Extract evidence from Douyin**
   - Preserve the original share text and short URL.
   - Resolve the short link and capture the final video URL when possible.
   - Extract page title, visible text, captions, transcript, comments only when relevant, and frame text.
   - If metadata fails, use browser/Playwright fallback and sample frames.
   - Do not infer skill names from the title alone; keep evidence that supports each identified name.

2. **Identify and map skills**
   - Build a table: video name, normalized skill name, source repo/path, confidence, reason.
   - Check local installed skills first.
   - Search curated lists or high-trust GitHub sources for missing skills.
   - Prefer official owners and exact `SKILL.md` frontmatter names.
   - Identify required companion skills or shared auth/config skills.

3. **Vet before installing**
   - Review repo owner, update activity, license, target skill path, `SKILL.md`, scripts, and reference files.
   - Reject or ask before unclear, high-risk, obfuscated, credential-harvesting, destructive, or unofficial sources.
   - Treat skills that need credentials, browser access, cloud deploy, data scraping, CRM writes, or external APIs as medium or higher risk.
   - Document risk boundaries in the final workflow skill.

4. **Install and verify mentioned skills**
   - Install with the local `skill-installer` helper.
   - If a skill already exists, report it as already installed unless the user asks to update.
   - Run `quick_validate.py` on each installed skill.
   - If upstream frontmatter has unsupported keys, make the smallest compatibility fix needed and revalidate.
   - Tell the user that a restart or new session may be needed.

5. **Decide whether a combined workflow exists**
   - A combined workflow exists when the skills have a natural order, shared input/output handoff, or repeatable business outcome.
   - Do not force a workflow if the skills are unrelated. In that case, publish them separately and explain no combined skill was created.
   - Define the workflow purpose, target user, stages, handoff artifacts, default safety boundaries, and final output contract.

6. **Create the combined workflow skill**
   - Use a concise hyphen-case name under 64 characters.
   - Initialize the skill in the local Codex skills directory.
   - Keep `SKILL.md` focused on orchestration: when to call each companion skill, what decisions to make, what to verify, and what not to do by default.
   - Include companion skill names, setup requirements, safety gates, and final response expectations.
   - Generate or update `agents/openai.yaml`.
   - Validate with `quick_validate.py`.

7. **Package independently**
   - Follow the user's default rule: one skill becomes one independent skill package unless they explicitly request a bundle.
   - Use this structure:

```text
skill-packs/<workflow-skill-name>/
  skills/<workflow-skill-name>/SKILL.md
  skills/<workflow-skill-name>/agents/openai.yaml
  scripts/install.ps1
  scripts/install-companion-skills.ps1
  scripts/verify.ps1
  manifest/skill-pack.json
  manifest/companion-skills.json
  docs/FEATURES.md
  docs/INSTALLATION.md
  docs/WORKFLOWS.md
  docs/SECURITY.md
  docs/GITHUB_UPLOAD.md
  examples/prompts.md
  README.md
  THIRD_PARTY_NOTICES.md
```

   - Do not vendor large third-party skills unless explicitly asked.
   - Use companion manifests and installer scripts pointing at upstream repos.

8. **Validate, zip, publish, and confirm**
   - Run the new package `scripts/verify.ps1`.
   - Run the repo-wide validation for all independent packages when publishing into an existing skill-pack repo.
   - Create one zip archive for the new independent package.
   - Pull `main` with `--ff-only`, commit, push, and verify the remote hash.
   - Open or fetch the GitHub page to confirm the new directory is visible.
   - Clean temporary clone/vetting folders only after verifying resolved paths are inside the intended workspace.

## Quality Gates

Before creating a workflow skill, confirm:

- Every mentioned skill has evidence from the video or user-provided summary.
- Every installed skill maps to a concrete repo/path or known local source.
- The workflow has a real handoff between stages.
- The new skill states what it will not do by default.
- All local and packaged skills validate.
- The GitHub package is independent unless the user explicitly requested a combined bundle.

## Common Mistakes

- Installing based only on the video's marketing phrase.
- Forgetting companion skills, such as shared auth/config helpers.
- Treating content-writing skills as live sending or automation tools.
- Publishing several unrelated skills as one bundle without explicit user instruction.
- Leaving temporary clones, cookies, screenshots, prospect data, API keys, or raw lead lists in the repo.
- Claiming upload is done before checking `git ls-remote` or the GitHub page.

## Final Response

Respond in the user's language. Include:

- Video URL or share text processed.
- Skills identified, installed, already present, skipped, and their sources.
- Whether a combined workflow was created and why.
- New workflow skill name.
- GitHub package URL when published.
- Commit hash and zip path when created.
- Validation result.
- Any remaining manual action, such as restarting Codex, setting API keys, or authenticating a CLI.
