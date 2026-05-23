# Security

## Do Not Trust the Video Alone

Douyin videos can use marketing names that do not exactly match real package names. Always connect each claimed skill to a concrete source such as a local installed skill, curated list entry, or trusted GitHub repo/path.

## Vet Before Installing

Review:

- Repository owner and update activity.
- Exact target skill path.
- `SKILL.md` frontmatter.
- Scripts and executable files.
- References to credentials, cookies, SSH keys, browser sessions, tokens, cloud accounts, or destructive commands.

Ask before installing high-risk or unclear sources.

## Publication Hygiene

Do not commit:

- API keys
- cookies
- browser profiles
- screenshots containing private data
- raw lead lists
- customer records
- Lark/Feishu tokens or URLs that should stay private
- temporary clone directories

## Destructive Operations

Do not force push, reset hard, delete remote content, or overwrite unrelated repository files unless the user explicitly asks for that operation.

Clean temporary folders only after resolving their absolute path and confirming it is inside the intended workspace.
