# Workflows

## First Customer Introduction

1. Start with the product-consultant self-introduction from `SKILL.md`.
2. Explain Youyou as `one core inorganic-board material -> doors/walls/furniture boards -> integrated inorganic space`.
3. Recommend the website hub and product-evolution hub.
4. Ask what scenario the customer cares about: home, hotel, commercial, education, healthcare, office, dealer showroom, or project delivery.

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
