# Website clarity and coordination rubric

Use this rubric for full-site work, redesigns, formal acceptance, and release audits.

## 1. Heading gate

### Hard rules

- H1 communicates the page's concrete value, not a vague worldview.
- Desktop H1/H2/H3 remain one line whenever the same meaning can be expressed naturally in one line.
- A heading does not wrap because of an artificially narrow column, giant type, manual `<br>`, or decorative side content.
- Mobile may use two lines only when the phrase remains concise and a one-line version would be too small or semantically damaged.
- Avoid single-character orphan lines, hanging punctuation, isolated numbers, and broken product names.
- Do not use forced non-breaking characters or hidden duplicate headings to game line-count tests.

### Recommended size ranges

| Level | Desktop | Mobile |
|---|---:|---:|
| Hero H1 | 42–64px | 30–42px |
| Page H1 | 36–52px | 28–38px |
| Section H2 | 28–40px | 24–32px |
| H3 | 18–26px | 18–24px |
| Body | 16–19px | 16–18px |

These are defaults, not a reason to shrink long copy. Rewrite first.

### Heading budget table

| Route/section | Level | Final text | Desktop max lines | Mobile max lines | Exception reason |
|---|---|---|---:|---:|---|

Every documented exception must state why shorter wording, wider content, or a smaller valid size would be worse.

## 2. Non-AI visual language gate

Flag combinations, not isolated techniques. A page becomes template-like when several of these recur without business justification:

- abstract superlative hero copy with no product noun;
- 72–120px Chinese slogans used as the main spectacle;
- blue-purple gradients, glow or glass panels as default identity;
- repeated eyebrow label + giant heading + short paragraph + three equal cards;
- every section floating in its own rounded rectangle;
- decorative English labels, chapter numbers, terminal text, grids, particles or scan lines;
- fake dashboards, fake testimonials, fake logos, fake metrics or generated evidence;
- identical composition repeated across unrelated routes;
- animation that hides weak static composition;
- AI chat entry inserted despite no user need.

Pass when the design feels specific to the organization, content, audience, and task; visuals carry real information; and section structure follows content purpose.

## 3. Layout coordination gate

### Container and alignment

- Navigation, hero, content, conversion area, and footer use intentional shared boundaries.
- Use a consistent maximum width and gutter system; exceptions must be visible and purposeful.
- Text blocks, media, controls, and section headings align to stable axes.
- Adjacent columns have a justified ratio; neither side appears accidentally empty or compressed.

### Density and rhythm

- Each section contains one main idea and one clear visual focus.
- Empty space separates groups; it does not create a large unproductive stage.
- Section padding reflects content density and is not mechanically identical everywhere.
- Avoid dense card walls and the opposite extreme of sparse text floating in oversized sections.
- Body line length is usually 28–42 Chinese characters or 45–75 Latin characters.

### Responsive composition

- Reorder mobile content by importance.
- Keep primary CTA visible without allowing it to crowd navigation or headings.
- Do not preserve desktop sidebars, empty columns, or oversized hero heights on mobile.
- Test 200% zoom, long Chinese text, and narrow 320–360px widths when relevant.

## 4. Hierarchy gate

- A five-second glance reveals identity, offer, audience, and next action.
- One screen has one dominant heading, not multiple competing display elements.
- Eyebrows, labels, metadata, body text, and captions remain visibly distinct.
- Do not enlarge all supporting text globally; preserve contrast between roles.
- Primary and secondary CTA differ clearly without excessive button proliferation.

## 5. Content and evidence gate

- Replace abstract capability words with concrete products, services, scenarios, or outcomes.
- Mark unverified claims and placeholders; do not present generated assets as evidence.
- Prefer real UI, work, products, people, spaces, examples, documents, or data.
- Keep internal release status, mock labels, and engineering language out of customer-facing pages unless intentionally disclosed.

## 6. Motion gate

- Core information is visible before animation starts and when JavaScript fails.
- Motion has a named purpose: feedback, state, continuity, or orientation.
- Avoid continuous floating, breathing, scanning, particle, parallax, or long reveal effects by default.
- Support `prefers-reduced-motion` and make interactions interruptible.

## 7. Objective acceptance thresholds

Unless a documented product reason overrides them:

- zero horizontal page overflow at tested viewports;
- zero failed critical assets, console errors, or page errors;
- zero avoidable multi-line desktop H1/H2/H3;
- zero manually forced dramatic line breaks in primary headings;
- zero single-character orphan lines in Chinese headings;
- hero does not consume nearly the entire first viewport without providing evidence or a clear task;
- primary content and CTA are usable at 200% zoom;
- reduced-motion path remains complete.

## 8. Review output template

| Severity | Route | Viewport | Section/selector | Evidence | Root cause | Required fix |
|---|---|---|---|---|---|---|

Finish with:

1. gate status;
2. heading exceptions, if any;
3. AI-template signals found or confirmed absent;
4. layout coordination summary;
5. protected elements that must not regress;
6. same-viewport evidence locations.

