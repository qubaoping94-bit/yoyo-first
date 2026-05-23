# Features

## What This Skill Does

`douyin-workflow-skill-publisher` captures the complete repeatable workflow for turning a Douyin skill video into a reusable Codex workflow skill and an independent GitHub skill pack.

Core capabilities:

- Extract evidence from Douyin share text, short links, final URLs, page text, captions, and sampled frames.
- Identify skill names from the video and map each to a trusted local or GitHub source.
- Vet third-party skill sources before installation.
- Install and validate mentioned skills.
- Detect whether the installed skills form a real workflow.
- Create a new combined workflow skill when the skill chain has a natural handoff.
- Package the new workflow skill independently.
- Generate docs, manifests, install scripts, companion install scripts, verification scripts, and zip archives.
- Commit, push, and confirm publication in a GitHub repository.

## What Makes It Different

This is not just a Douyin extractor. It extends the process through workflow synthesis and GitHub publication, while preserving the default packaging rule: one new skill equals one independent skill pack.

## Default Output

A successful run should produce:

- Installed and validated mentioned skills.
- A decision on whether a combined workflow should exist.
- A new local workflow skill when appropriate.
- A new independent package under `skill-packs/<skill-name>`.
- A zip archive.
- A Git commit and pushed GitHub directory when publication is requested or inferred from the repeated workflow.
