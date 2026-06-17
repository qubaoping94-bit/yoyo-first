# Workflows

## First Customer Introduction

1. Start with the product-consultant self-introduction from `SKILL.md`.
2. Explain Youyou as `one core inorganic-board material -> doors/walls/furniture boards -> integrated inorganic space`.
3. Recommend the website hub and product-evolution hub.
4. Ask what scenario the customer cares about: home, hotel, commercial, education, healthcare, office, dealer showroom, or project delivery.

## Six Service Modes

Use the mode table in `SKILL.md` before answering:

- `快速了解`: short product explanation and first links
- `经销商转发`: WeChat-ready forwarding message
- `专项答疑`: performance concern with evidence boundary
- `选型顾问`: project part or scenario recommendation
- `内容生成`:朋友圈, short video, or customer copy
- `AI商业样本`: Youyou as an实体企业AI训练 and sales enablement sample

## Dealer Forwarding

1. Keep the message short enough for WeChat.
2. Send the website hub first.
3. Add the product-evolution hub if the customer wants material or performance logic.
4. Add the moments copy site if the dealer needs ready-to-send朋友圈 copy.

## Specific Objection Handling

1. Identify the concern: environmental, moisture, mildew, fire-resistant, sound, cracking, deformation, price, or delivery.
2. Use `references/faq-and-sales-scripts.md` for a concise response.
3. Use `references/website-router.md` to pick one relevant demo page.
4. Avoid unsupported metrics; ask for official report or quotation context when needed.

## OCR Image Pairing

1. For product, performance, application, dealer, or customer-education questions, run:

```powershell
node .\skills\youyou-inorganic-board-guide\scripts\find-gallery-images.mjs "<customer question>" --limit 3
```

2. Choose images primarily by `图片文字命中`, not only by title, category, or visual style.
3. Include the image title, why it matches, OCR hit terms, a short OCR excerpt, thumbnail URL, and high-resolution URL.
4. If the chat surface supports Markdown images, use the returned Markdown thumbnail link.
5. If the match is weak, say that this is the closest public gallery match and offer to refine by scenario.

## Public Link Maintenance

Run:

```powershell
node .\skills\youyou-inorganic-board-guide\scripts\check-links.mjs
```

or:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -CheckLinks
```

If one link fails, check whether it is a temporary CDN/router issue before changing skill content.

## Skill Quality Maintenance

Run the smoke test after any content edit:

```powershell
node .\skills\youyou-inorganic-board-guide\scripts\smoke-test.mjs
```

The smoke test should fail if template placeholders return, if required references are missing, or if the default prompt no longer mentions `$youyou-inorganic-board-guide`.

For image-routing changes, also run:

```powershell
node .\skills\youyou-inorganic-board-guide\scripts\find-gallery-images.mjs "防潮 回南天 厨卫" --limit 2
```
