# GitHub Upload Notes

This package follows the user's default rule:

```text
one skill = one independent skill pack
```

Recommended package path:

```text
skill-packs/douyin-workflow-skill-publisher
```

Recommended zip:

```text
douyin-workflow-skill-publisher-skill-pack.zip
```

Before pushing:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

When adding future generated workflow skills, publish each as its own sibling package under `skill-packs/` unless the user explicitly requests a bundle.
