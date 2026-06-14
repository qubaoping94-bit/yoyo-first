# Release Checklist

## Stable Paths

- Workspace: `D:/桌面应用软件下载库/OneDrive/Desktop/two`
- Generated topic output: `D:/桌面应用软件下载库/OneDrive/Desktop/three/output/<slug>/`
- Product config: `scripts/product-evolution-pages.config.json`
- Site list helper: `scripts/site-directory-common.cjs`
- WeChat helper: `scripts/build-wechat-share-poster.cjs`
- Prepared public site: `output/youyou-ai-gallery-site/public`
- Prepared site list: `output/youyou-sites-list-site/public`

## Build Commands

Run from the workspace:

```powershell
node scripts\build-wechat-share-poster.cjs
node scripts\build-site-list-html.cjs
node scripts\prepare-wuji-space-cloudflare-lite.cjs
```

After build, validate the new slug exists in `output/youyou-ai-gallery-site/public/product-evolution/<slug>/` and that the PNG exists beside `index.html`.

## Local QA

Use Playwright with the repo fallback path used by existing audits:

```javascript
let playwright;
try {
  playwright = require(path.join(process.cwd(), "node_modules", ".pnpm", "playwright@1.60.0", "node_modules", "playwright"));
} catch {
  playwright = require("playwright");
}
```

Check both `1440x900` and `390x844`:

- route status is `200`
- `.final-image` exists, completes, and has natural dimensions
- no failed requests
- no horizontal overflow
- topbar title/actions do not overlap
- screenshots are saved under `output/qa/<slug>/`

## Deploy Commands

```powershell
npx.cmd wrangler pages deploy "D:\桌面应用软件下载库\OneDrive\Desktop\two\output\youyou-ai-gallery-site\public" --project-name youyou-ai-gallery --commit-dirty=true
npx.cmd wrangler pages deploy "D:\桌面应用软件下载库\OneDrive\Desktop\two\output\youyou-ai-gallery-site\public" --project-name youyou-wuji-space-ai --commit-dirty=true
npx.cmd wrangler pages deploy "D:\桌面应用软件下载库\OneDrive\Desktop\two\output\youyou-sites-list-site\public" --project-name youyou-sites-list --commit-dirty=true
```

## Public Audits

```powershell
node scripts\audit-public-assets.cjs
$env:AUDIT_PUBLIC='1'; node scripts\audit-contact-sites.cjs
node scripts\audit-wuji-gallery-assets.cjs
node scripts\audit-wuji-space-public.cjs
$env:AUDIT_SKIP_GALLERY_ASSETS='1'; node scripts\audit-public-critical-runtime.cjs
node scripts\audit-site-directory.cjs
```

Also direct-check:

- `https://youyou-ai-gallery.pages.dev/product-evolution/<slug>/`
- the route's final PNG URL
- `https://youyou-sites-list.pages.dev/`

## Final Acceptance

Only mark the task complete when:

- local page QA passes on desktop and mobile
- Cloudflare deploy succeeds for gallery, backup gallery, and site list
- public direct route and image checks return `200`
- public audits report `issueCount: 0`
- Obsidian memory closeout is done when there is reusable value
