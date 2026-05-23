# douyin-workflow-skill-publisher

Independent skill pack for turning Douyin skill-recommendation videos into installed skills, synthesized workflow skills, and GitHub-ready independent skill packages.

Use this when a repeat task looks like:

```text
根据这个抖音链接内容安装其中的 skill，如果能组成一套工作流，就生成组合 workflow skill，并上传到 GitHub 仓库。
```

## Included Skill

- `douyin-workflow-skill-publisher`: orchestrates Douyin extraction, skill source mapping, vetting, installation, workflow synthesis, local skill creation, independent packaging, zip generation, GitHub push, and remote confirmation.

## Companion Skills

This workflow uses these skills when available:

- `douyin-skill-installer`
- `skill-vetter`
- `skill-installer`
- `skill-creator`
- `writing-skills`
- `github-skill-pack-publisher`

## Install

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

Verify:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Restart Codex or open a new session after installation.

## Documentation

- [Features](docs/FEATURES.md)
- [Installation](docs/INSTALLATION.md)
- [Workflows](docs/WORKFLOWS.md)
- [Security](docs/SECURITY.md)
- [GitHub upload notes](docs/GITHUB_UPLOAD.md)
- [Prompt examples](examples/prompts.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
