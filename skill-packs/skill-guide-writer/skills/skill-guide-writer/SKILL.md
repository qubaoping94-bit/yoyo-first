---
name: skill-guide-writer
description: Audit a local or repository-backed AI skill and produce a complete, evidence-based Markdown usage guide, normally in Chinese, with the simplest directly copyable invocation on the first screen. Use when the user asks to summarize, document, explain, catalog, compare, or create a reusable README-style guide for a Codex, Claude Code, Agent, MCP, plugin, or SKILL.md-based skill, including capabilities, use cases, installation, commands, online galleries/demos, workflows, limitations, safety notes, and source links.
---

# Skill Guide Writer

Create a polished user-facing guide from source evidence. Do not merely paraphrase a README.

## Required inputs

Identify the target from any combination of:

- installed skill name or folder;
- `SKILL.md`, repository, marketplace, or website URL;
- user-provided files;
- desired output path, language, audience, or detail level.

If the target is discoverable locally, proceed without asking. If no target can be identified, ask for the skill name, path, or URL. Default to Chinese, comprehensive detail, and `<skill-name>使用说明.md` on the Desktop when the user gives no output preference.

## Workflow

### 1. Resolve and inventory the target

Locate the canonical skill folder and fully read its `SKILL.md` to EOF before writing. Run `scripts/inventory_skill.py <target-folder>` to obtain a safe structural inventory. The script is a starting point, not a substitute for reading.

Inspect only directly relevant supporting files: agent metadata, README, manifest/package metadata, examples, referenced guides, gallery index, and scripts needed to verify commands. Follow references one level at a time and avoid loading unrelated large directories.

Never read, echo, or summarize secrets. Skip `.env`, credentials, cookies, tokens, private keys, account data, and suspicious query parameters.

### 2. Build an evidence ledger

Record each important claim with its source:

1. `SKILL.md` and bundled files;
2. official repository documentation and releases;
3. official project site, gallery, demo, or package registry;
4. source-code inspection or a safe local smoke test;
5. clearly labeled inference when no direct claim exists.

For changing facts—counts, versions, installation commands, current URLs, availability, compatibility—verify against current official sources when internet access is available. Prefer primary sources. Never invent a gallery, demo, license, dependency, or supported platform.

Resolve conflicts by favoring the most recent canonical source and disclose material discrepancies in the guide.

### 3. Decide the guide shape

Read [references/guide-spec.md](references/guide-spec.md) before drafting. Use its decision rules and completeness matrix.

Copy [assets/skill-guide-template.md](assets/skill-guide-template.md) as the structural starting point. Adapt sections to the actual skill; remove inapplicable placeholders instead of filling them with guesses.

### 4. Put the simplest call first

The first visible screen must contain, in this order:

1. the document title;
2. a bold label stating that the next instruction can be copied directly;
3. one fenced, natural-language invocation that names the skill explicitly;
4. the most valuable official live link, when one exists;
5. the official repository or canonical source link, when one exists.

Make the first invocation outcome-oriented and usable without editing when possible. Do not lead with installation, background, a table of contents, or internal implementation details.

### 5. Write for use, not promotion

Explain what the skill does, who it is for, suitable and unsuitable tasks, inputs, outputs, routes/modes, workflow, exact invocation patterns, installation or discovery, dependencies, limitations, safety, licensing, and troubleshooting when supported by evidence.

Use copyable prompts for the common, advanced, constrained, and continuation/editing cases. Preserve exact commands and paths in code fences. Describe technical terms in plain language.

Distinguish explicitly:

- confirmed capability;
- optional or environment-dependent capability;
- not verified or not available;
- behavior of the underlying tool versus behavior added by the skill.

### 6. Validate before delivery

Check the finished Markdown against every `P0` gate in [references/guide-spec.md](references/guide-spec.md). Also verify:

- file exists and is UTF-8 readable;
- first screen contains the copyable invocation;
- skill name is correct and consistent;
- all local paths and code fences are syntactically intact;
- every public URL is exact and, when practical, reachable;
- no placeholder, unsupported claim, secret, or private data remains;
- counts and version-sensitive claims carry a source or verification date;
- the guide is complete without requiring the reader to inspect commentary.

Report the output path, key sections, verification performed, and any unresolved evidence gap. Never claim a link or feature was verified when it was not.

## Invocation examples

- `用 $skill-guide-writer 全面总结 video-shotcraft，并在桌面生成中文 Markdown 使用说明。`
- `用 $skill-guide-writer 审计这个 GitHub skill，核验安装方式、在线演示和限制，输出给非技术用户看的详细指南。`
- `用 $skill-guide-writer 更新现有说明文档，只修改已经由官方资料证实的过时内容。`

## Resource routing

- Always read `references/guide-spec.md` for the document contract and QA gates.
- Use `assets/skill-guide-template.md` as the output skeleton; do not ship unfilled placeholders.
- Run `scripts/inventory_skill.py` for local targets; inspect its JSON and then read the relevant files yourself.
