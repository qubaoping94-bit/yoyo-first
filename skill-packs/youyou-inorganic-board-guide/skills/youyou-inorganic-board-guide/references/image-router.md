# Image Router

Use this file whenever an answer about Youyou inorganic board would be easier to understand with visuals. The default experience should be `文字答案 + 网站链接 + 1-3 张相关图库图片`.

## Core Rule

For any customer/dealer answer about product system, product structure, applications, performance topics, showroom explanation, or WeChat forwarding, include matching images from the public Youyou AI gallery when available.

Image selection must prioritize the text printed inside each gallery image. Use OCR text from the gallery as the first matching standard, then use title, category, prompt, notes, and image category as secondary signals.

Recommended helper:

```powershell
node scripts\find-gallery-images.mjs "客户问题或主题关键词" --limit 3
```

The helper reads both:

```text
https://youyou-ai-gallery.pages.dev/assets/gallery-data.js
https://youyou-ai-gallery.pages.dev/assets/gallery-ocr-data.js
```

It returns Markdown-ready thumbnail links, high-resolution URLs, OCR hit terms, and a short image-text excerpt.

## Topic To Image Category

| Customer topic | Prefer images from | OCR/search keywords |
|---|---|---|
| First product introduction | 产品样板, 现代科技主视觉, 现代人物系列 | `优优无机板 产品体系 无机空间 门墙柜 环保 稳定` |
| Core board / material | 产品样板, 参数对比海报, 现代科技主视觉 | `无机板 样板 结构 玄武岩 材料 核心材料` |
| Inorganic door | 产品样板, 现代科技主视觉 | `无机门 门板 静音 芯材 门套 门墙柜` |
| Wall panel | 产品样板, 项目案例现场 | `无机墙板 墙面 12mm 空间 护墙` |
| Furniture board / cabinet | 产品样板, 项目案例现场 | `无机复合家具板 家具板 柜 门墙柜` |
| Dealer forwarding | 现代人物系列, 现代科技主视觉 | `经销商 招商 朋友圈 渠道 转发 代理` |
| Environmental / health | 参数对比海报, 现代科技主视觉 | `环保 无机 甲醛 健康空间 装修板材` |
| Waterproof / moisture | 参数对比海报, 现代科技主视觉 | `防水 防潮 潮湿 回南天 厨卫 湿区` |
| Mildew / hygiene | 参数对比海报, 现代科技主视觉 | `防霉 抗菌 卫生 潮湿 洁净 易清洁` |
| Fire-resistant | 参数对比海报, 现代科技主视觉 | `阻燃 不燃 防火 A级 安全 核心材料` |
| Sound / quiet | 参数对比海报, 产品样板 | `隔音 降噪 静音 无机门 门板 芯材` |
| Cracking / deformation | 参数对比海报, 产品样板 | `不开裂 不变形 稳定 冷热 极干 极潮 耐用` |
| Project cases | 项目案例现场 | `项目 案例 现场 空间 应用 落地` |
| AI business sample | AI系统赋能海报 | `AI 赋能 企业 增长 系统 训练样本` |

## Image Output Contract

Use this format:

```text
配套图片：
1. <title> - <why this image helps the customer understand the answer>
   图片文字命中：<OCR hit terms>
   图片文字摘录：<short OCR excerpt>
   缩略图：<thumb URL>
   高清图：<image URL>
```

If Markdown images are appropriate:

```markdown
[![<title>](<thumb URL>)](<image URL>)
```

## Selection Quality

- Prefer images whose OCR text directly contains the user's concern, such as `防潮`, `阻燃`, `无机门`, `经销商`, `朋友圈`, or `AI赋能`.
- Treat OCR hits as stronger evidence than image title, prompt, category, or visual attractiveness.
- Prefer `产品样板` for product/structure questions.
- Prefer `参数对比海报` for performance topics.
- Prefer `项目案例现场` for application and case questions.
- Prefer `现代人物系列` for dealer/customer forwarding only when the OCR text also supports the sales or customer-education topic.
- Prefer `AI系统赋能海报` only when the user asks about AI business enablement.
- Avoid ancient-person, poetry, or unrelated scenic images unless the user explicitly asks for that style.
- Do not use images with irrelevant OCR text just because they look high-end.
- If image matching is weak, say `我先给你配一组最接近的图库图，后续可以按具体场景再精筛。`
