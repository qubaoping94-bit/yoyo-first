# Workflows

## Full Douyin-to-GitHub Flow

1. Receive Douyin share text, URL, screenshot, or video summary.
2. Extract evidence from the video and avoid guessing from the title alone.
3. Identify named skills and map them to concrete sources.
4. Vet source repos and target skill directories.
5. Install and validate each skill.
6. Decide whether the skills form a real workflow.
7. Create a combined workflow skill only when there is a natural sequence and business outcome.
8. Package the new workflow skill as an independent skill pack.
9. Generate a zip archive.
10. Commit, push, and confirm the GitHub directory.

## Workflow Decision

Create a combined workflow skill when:

- The skills form a clear sequence.
- Outputs from one step become inputs for the next step.
- The user is likely to repeat the whole chain.
- The final outcome is more useful than the individual skills alone.

Do not create a combined workflow skill when:

- The skills are unrelated recommendations.
- The video only lists alternatives.
- Source mapping is uncertain.
- Safety or permission risks cannot be bounded.

## Packaging Rule

Default to one independent package per new skill:

```text
skill-packs/<new-workflow-skill-name>
```

Create a multi-skill bundle only when the user explicitly asks for a combined bundle.

## Reusable Prompt

```text
用 $douyin-workflow-skill-publisher 处理这个抖音链接：识别视频提到的 skill，安装并校验；如果能组成可复用工作流，就生成组合 workflow skill，按独立包规则上传到我的 GitHub 仓库。
```
