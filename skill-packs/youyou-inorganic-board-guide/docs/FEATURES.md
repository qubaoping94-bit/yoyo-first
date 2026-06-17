# Features

## Product Consultant Behavior

- Starts with a fixed Youyou inorganic-board product-consultant introduction.
- Explains Youyou as a material-to-space system rather than a single commodity board.
- Covers the product matrix: Youyou inorganic board, inorganic door, inorganic wall panel, inorganic composite furniture board, and door-wall-cabinet integrated inorganic space.
- Gives short, customer-facing explanations suitable for dealers and early-stage customers.
- Classifies requests into six service modes: quick understanding, dealer forwarding,专项答疑, selection advisor, content generation, and AI business sample.
- Uses standard output contracts for link recommendations, dealer forwarding, and evidence-sensitive performance answers.

## Public Link Routing

- Recommends the main public website hub for first-time customers.
- Routes visual requests to the Youyou AI gallery.
- Routes performance or topic-specific questions to product-evolution demo pages.
- Routes WeChat or朋友圈 copy requests to the moments copy site.

## OCR Gallery Image Matching

- Adds 1-3 relevant images from the public Youyou AI gallery when the answer benefits from visuals.
- Reads `gallery-ocr-data.js` and treats image text as the primary selection standard.
- Uses image title, category, prompt, and notes only as secondary signals after OCR text.
- Outputs thumbnail URL, high-resolution URL, OCR hit terms, and a short image-text excerpt.
- Helps customers understand specific questions such as 防潮, 阻燃, 无机门, 静音, 经销商转发, and AI赋能 with matching visual material.

## FAQ And Dealer Scripts

- Provides forwarding scripts for dealers.
- Answers common questions about environmental positioning, waterproof/moisture concerns, mildew/hygiene, fire-resistant topics, pricing, construction, and comparison with ordinary panels.
- Keeps answers concise and action-oriented.

## Claim Safety

- Avoids unsupported standards, rates, fixed years, patent counts, prices, or engineering promises.
- Instructs Codex to ask for official reports, quotations, drawings, samples, or project plans before making final technical commitments.
- Excludes private desktop paths, unpublished sensitive material, credentials, and private contact details from public-facing answers.

## Quality Gates

- `scripts/smoke-test.mjs` checks required files, prompt metadata, key guidance, public-link references, and template cleanup.
- `scripts/check-links.mjs` fetches the public Youyou pages, verifies successful HTML responses, and checks key page text on primary entrypoints.
- `scripts/find-gallery-images.mjs` fetches the public gallery data and OCR index, then verifies that a customer topic can return matched gallery images.
