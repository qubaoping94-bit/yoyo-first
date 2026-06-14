---
name: youyou-demo-page-delivery-pipeline
description: Build and publish repeatable Youyou inorganic board demo-system pages. Use when the user asks to create, continue, revise, package, deploy, or audit a "优优无机板...演示系统" page from reference images or a theme, especially when the deliverable should include an AI-generated main visual, fullscreen launch HTML, product-evolution site entry, WeChat/site-directory share updates, Cloudflare Pages deployment, public audits, and memory closeout.
---

# Youyou Demo Page Delivery Pipeline

Use this skill to deliver a complete 优优无机板演示系统 page, not only a standalone image. The normal output is: a final PNG, a fullscreen HTML launch page, a product-evolution entry, refreshed share materials, deployed public URLs, audit evidence, and a short Chinese closeout.

## Required Context

- Read `D:\桌面应用软件下载库\OneDrive\Desktop\个人本地知识库\Codex记忆\AGENTS.md` and `INDEX.md`, then only the 1-3 relevant memory files. For Youyou web work, usually read `项目\优优无机板产品网站.md`.
- If the task is a visual demo page, also use:
  - `youyou-special-demo-system`
  - `ian-xiaohei-scenes`
  - `html-production-defaults`
- Work from `D:\桌面应用软件下载库\OneDrive\Desktop\two` unless the user specifies another repo.

## Stable Paths

- Source repo: `D:\桌面应用软件下载库\OneDrive\Desktop\two`
- Output root: `D:\桌面应用软件下载库\OneDrive\Desktop\three\output\<slug>\`
- Product evolution config: `D:\桌面应用软件下载库\OneDrive\Desktop\two\scripts\product-evolution-pages.config.json`
- Site directory common data: `D:\桌面应用软件下载库\OneDrive\Desktop\two\scripts\site-directory-common.cjs`
- WeChat share script: `D:\桌面应用软件下载库\OneDrive\Desktop\two\scripts\build-wechat-share-poster.cjs`
- Public product route: `https://youyou-ai-gallery.pages.dev/product-evolution/<slug>/`

## Delivery Workflow

1. Define the page brief.
   - Extract theme, exact Chinese title, desired use case, reference-image strengths, and forbidden changes.
   - Choose a lowercase hyphen slug, usually `youyou-<topic>-demo`.
   - Avoid unverified numbers, test standards, medical claims, guaranteed years, and absolute promises unless the user provides evidence.

2. Generate or revise the main visual.
   - Prefer the 小黑长卷 / near-white material story style for the demo-system series unless the user explicitly asks for another style.
   - Keep real material objects, small black helper figures, thin route lines, short Chinese labels, restrained Youyou green, and enough white space.
   - For reference-image edits, preserve unaffected scenes and only change the requested section.
   - Inspect the image before accepting it. Record image path, dimensions, and ratio.

3. Build the fullscreen launch HTML.
   - Put the PNG and HTML in `D:\...\three\output\<slug>\`.
   - Create both `index.html` and a same-title Chinese HTML file when useful.
   - Use a black launch-stage wrapper with the main image as the first visual signal.
   - Do not overlay node text on the image unless the user asks for web-layer labels.
   - Set `--screen-ratio` from the real image dimensions. Do not pad the image only to force a target ratio.
   - Include fullscreen affordance: click button, double-click, and `F`.
   - Prevent topbar overlap on mobile: reserve right padding for the fullscreen button and clamp long Chinese titles to two lines.

4. Register the product-evolution page.
   - Append one object to `scripts\product-evolution-pages.config.json`; this file is a top-level JSON array.
   - Required fields normally include `slug`, `title`, `shortTitle`, `subtitle`, `description`, `sourceHtml`, `sourceDir`, `assets.heroImage`, `date`, `audience`, `tags`, and `useCase`.
   - Use `apply_patch` for manual JSON/script edits. Avoid PowerShell pipelines that can corrupt Chinese text.
   - Validate with Node `JSON.parse` and confirm the new entry index/count.

5. Refresh directory and share surfaces.
   - Update `scripts\site-directory-common.cjs` when the page should appear in the website directory, gallery `/sites/`, or extra links.
   - Update `scripts\build-wechat-share-poster.cjs` so the WeChat sharing text includes the new page and use case.
   - Run:
     ```powershell
     node scripts\build-wechat-share-poster.cjs
     node scripts\build-site-list-html.cjs
     node scripts\prepare-wuji-space-cloudflare-lite.cjs
     ```

6. Local QA before deploy.
   - Serve or open the built product-evolution page and test desktop plus mobile.
   - Check the title, image load, natural image size, navigation, fullscreen button, no horizontal overflow, and no incoherent overlap.
   - Save screenshots under `D:\...\two\output\qa\<slug>\`.

7. Deploy.
   - Deploy the prepared public folder to all three Pages projects:
     ```powershell
     npx.cmd wrangler pages deploy "D:\桌面应用软件下载库\OneDrive\Desktop\two\output\youyou-ai-gallery-site\public" --project-name youyou-ai-gallery --commit-dirty=true
     npx.cmd wrangler pages deploy "D:\桌面应用软件下载库\OneDrive\Desktop\two\output\youyou-ai-gallery-site\public" --project-name youyou-wuji-space-ai --commit-dirty=true
     npx.cmd wrangler pages deploy "D:\桌面应用软件下载库\OneDrive\Desktop\two\output\youyou-sites-list-site\public" --project-name youyou-sites-list --commit-dirty=true
     ```
   - Stable final URL is usually `https://youyou-ai-gallery.pages.dev/product-evolution/<slug>/`.

8. Public audits.
   - Run and record `issueCount`:
     ```powershell
     node scripts\audit-public-assets.cjs
     $env:AUDIT_PUBLIC='1'; node scripts\audit-contact-sites.cjs
     node scripts\audit-wuji-gallery-assets.cjs
     node scripts\audit-wuji-space-public.cjs
     $env:AUDIT_SKIP_GALLERY_ASSETS='1'; node scripts\audit-public-critical-runtime.cjs
     ```
   - Give the critical runtime audit a long timeout; it can take several minutes.
   - If an audit fails, fix and redeploy before claiming the page is complete.

9. Memory closeout.
   - Update `D:\桌面应用软件下载库\OneDrive\Desktop\个人本地知识库\Codex记忆\项目\优优无机板产品网站.md` with only durable facts and decisions:
     - output directory, final PNG/HTML names, dimensions, slug, public URL
     - intended customer use case
     - verification/audit results
     - new workflow or skill paths if created
   - Put unresolved follow-up items in `TODO.md` or `agent\open-loops.md`.

## Final Reply Shape

Reply in concise Chinese. Include:

- Stable public URL
- Local output PNG/HTML paths
- A one-line verification summary with the important `issueCount=0` audits
- Memory files or skills updated
- A Markdown image preview using the absolute local PNG path when helpful

## Common Pitfalls

- Do not treat `product-evolution-pages.config.json` as `{ pages: [...] }`; it is an array.
- Do not rely on `git status` as a verification signal for this workspace.
- Do not use web-layer text to cover up wrong image text unless the user asked for that approach.
- Do not let the fullscreen button overlap long Chinese titles on mobile.
- Do not skip share-poster and site-directory updates when the page is meant to be reusable by the user.
- Do not publish claims like `45dB`, percentages, test standards, antibacterial rates, or service life unless the user supplied verified source material.
