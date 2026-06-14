---
name: youyou-special-demo-delivery-pipeline
description: Use when creating, revising, publishing, or auditing Youyou inorganic-board special-topic demo systems, product-evolution pages, WeChat share assets, Cloudflare Pages deployments, or repeatable Youyou dealer presentation workflows from reference images.
---

# Youyou Special Demo Delivery Pipeline

## Overview

Use this skill to turn a Youyou inorganic-board topic request into a complete delivery unit: reference-image analysis, master visual generation or revision, local HTML page, product-evolution hub entry, WeChat share copy/assets, Cloudflare deployment, public audit, and memory closeout.

## Start Here

1. Read the workspace `AGENTS.md` and the Obsidian Codex memory index before substantial work.
2. Use local source of truth first: existing `scripts/`, `product-evolution-pages.config.json`, the user's reference images, and prior Youyou output folders.
3. If the task needs the established visual language, use companion skills when available: `youyou-special-demo-system`, `ian-xiaohei-scenes`, and `html-production-defaults`.
4. Before running build, deploy, or audit commands, read `references/release-checklist.md`.

## Workflow

1. **Extract the topic.** Convert the user title into a stable slug, short title, customer use case, tags, and one plain-language central thesis.
2. **Study references.** Capture visual direction, scene logic, headline tone, support modules, and useful copy. Do not blindly copy bad text or unsupported numbers.
3. **Set claim boundaries.** Avoid unverified metrics, standards, years, patent counts, percentages, or test values unless the user supplies reliable source material.
4. **Generate or revise the master image.** Save the final PNG under `D:/桌面应用软件下载库/OneDrive/Desktop/three/output/<slug>/`. When editing a previous image, preserve unrelated illustrations and only change the requested section.
5. **Build the page.** Create `index.html` plus a Chinese-title redirect HTML in the same output folder. The page should present the image as the first screen, include fullscreen/zoom affordances, and avoid horizontal overflow.
6. **Register the page.** Append one object to `scripts/product-evolution-pages.config.json`, then update `scripts/site-directory-common.cjs` and `scripts/build-wechat-share-poster.cjs` so the hub, site list, and WeChat copy all mention the new page.
7. **Regenerate assets.** Run the existing build scripts, then confirm the prepared public site includes the new route and PNG.
8. **QA locally.** Check desktop and mobile viewports. Verify the page status, `.final-image` loading, natural image size, no horizontal overflow, and no topbar overlap.
9. **Deploy.** Publish the prepared public folder to the configured Cloudflare Pages projects, then publish the site-list project.
10. **Audit publicly.** Run direct online route checks and the existing audit scripts. Do not call the task done until the new page URL, PNG URL, product-evolution hub, and site-list surfaces are verified.
11. **Memory closeout.** If the workflow or page facts have long-term value, update the Obsidian Codex memory notes requested by `AGENTS.md`.
12. **Final response.** Report the public URL, local output path, validation status, and memory files touched. Keep it concise and Chinese-first.

## Decision Rules

- If the user says to continue, continue the delivery chain instead of reworking minor visual details.
- If image text is imperfect but the user accepts it or says not to dwell on fonts, proceed to page build and deployment.
- If a generated image changes unrelated content during a targeted revision, regenerate with stronger preservation instructions before accepting it.
- If PowerShell corrupts Chinese text in inline scripts, switch to ASCII checks, parse from files, or build paths from `process.cwd()`.
- If a selector check fails, inspect the page before assuming the render is broken. Current generated pages usually use `.final-image`.

## Common Mistakes

- Stopping at a generated PNG without adding it to the hub, share materials, and public site.
- Publishing before running local desktop/mobile checks.
- Treating historical green audits as current proof.
- Adding unverified performance claims because a reference poster contained them.
- Forgetting that `product-evolution-pages.config.json` is a top-level array and should be appended carefully.
- Re-reading the entire memory vault; read only the index and 1-3 relevant notes.
