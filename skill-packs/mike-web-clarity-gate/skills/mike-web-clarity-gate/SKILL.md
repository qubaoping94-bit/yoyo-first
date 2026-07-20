---
name: mike-web-clarity-gate
description: Design and audit mature websites with concise single-line headings, natural non-AI visual language, coordinated layouts, stable hierarchy, and responsive readability. Use when creating, redesigning, reviewing, accepting, or visually debugging websites, landing pages, product pages, dashboards, minisites, HTML/React/Vue interfaces, especially when the user says headings must fit one line, the page feels AI-generated, typography is oversized, sections are repetitive, or layout is unbalanced.
---

# Mike Web Clarity Gate

Apply one standard in two modes: `BUILD` before and during implementation; `AUDIT` after implementation or before release. Treat clarity as a hard gate, not a decorative preference.

## Core contract

1. Prefer one-line Chinese headings. If the meaning fits in one line at the target viewport, do not force a second line.
2. Rewrite before shrinking. Shorten vague modifiers, remove duplicated concepts, then adjust width and type scale.
3. Do not create an “AI website look”: no generic giant slogans, blue-purple glow, glass-card grids, repeated eyebrow + huge serif heading + three-card sections, decorative English labels, fake metrics, or motion without business purpose.
4. Keep one primary reading start and one primary visual focus per screen.
5. Make navigation, hero, sections, media, CTA, and footer share a coherent container and alignment system.
6. Preserve readable hierarchy. Do not enlarge all text together or solve one breakpoint with global `!important` overrides.
7. Use real product, work, people, space, UI, or evidence as the visual subject. Decoration cannot substitute for content.
8. Mobile is a recomposition, not a squeezed desktop page.

Read [references/rubric.md](references/rubric.md) whenever performing a full build plan, redesign, formal acceptance, or release audit. For a small local fix, use the core contract and the relevant gate only.

## Select mode

- `BUILD`: The user asks to make, redesign, upgrade, implement, or refactor a website.
- `AUDIT`: The user asks to inspect, review, accept, compare, diagnose, or approve a website.
- `HYBRID`: The user asks to upgrade and deliver. Run BUILD first, then AUDIT on the built artifact.

## BUILD workflow

### 1. Write the clarity brief

Record:

- audience, task, evidence, primary action;
- one plain-language page promise;
- target viewports;
- forbidden visual habits;
- protected approved elements.

Do not begin high-fidelity styling until the page promise and content order are clear.

### 2. Set a heading budget

For every H1/H2/H3, record text, semantic role, target viewport, maximum line count, and maximum width. Default:

- desktop H1/H2/H3: one line;
- mobile: one line when ordinary Chinese can express the meaning; allow two lines only when shortening would remove essential meaning or create an unreadably small size;
- never insert a line break only for drama.

Resolve overflow in this order:

1. remove filler and repeated meaning;
2. use a shorter natural phrase;
3. widen the legitimate content area;
4. reduce font size within the hierarchy;
5. allow a semantic two-line break as a documented exception.

### 3. Build the layout skeleton

Use a stable container, deliberate column ratios, shared alignment lines, and a spacing scale. Verify the grey-box wireframe before gradients, imagery, or motion. Ensure each section answers one question and has a visible relationship to adjacent sections.

### 4. Add visual identity without templates

Choose a visual subject tied to the business. Vary section composition by content purpose while keeping tokens consistent. Cards are for real grouping or interaction, not the default wrapper for every paragraph.

### 5. Add motion last

Add motion only for feedback, state change, spatial continuity, or reading orientation. Keep core content visible without JavaScript and support reduced motion.

### 6. Run the audit gate

Serve the current build and run:

```powershell
node scripts/audit-layout.mjs <url> <output-directory>
```

Run it from the website project or call the script by absolute path. The script uses the project's Playwright. In Codex Desktop, load workspace dependencies and set `CODEX_NODE_MODULES` to the returned Node packages path when the project has no Playwright dependency. Inspect the screenshots and report; automation does not decide visual maturity by itself.

## AUDIT workflow

### 1. Establish evidence

Audit the current source, current build, and current URL. Capture at least 1440x900 and 390x844; add 1280, 1024, 430, 360, or 320 when the audience or layout requires them.

### 2. Run objective checks

Use `scripts/audit-layout.mjs` to measure heading line counts, heading width, viewport overflow, hero height, dominant alignments, console errors, and failed requests.

### 3. Perform the human review

Use [references/rubric.md](references/rubric.md). Specifically ask:

- Can every heading be shorter and stay precise?
- Does any heading wrap because it is oversized rather than meaningful?
- Does the page resemble a generic AI-generated template?
- Is empty space grouping content or merely creating a stage?
- Do columns, images, text, and CTA feel balanced at the actual viewport?
- Is the mobile order deliberate?

### 4. Report findings by severity

- `P0`: broken navigation/task, unreadable content, severe overflow, missing core content.
- `P1`: avoidable multi-line key heading, giant slogan, obvious AI-template structure, major imbalance, mobile title domination.
- `P2`: local alignment, spacing, density, or hierarchy inconsistency.
- `P3`: polish that does not block release.

For every finding include URL, viewport, selector or section, evidence, why it matters, and the smallest root-level fix. Do not prescribe endless overlay CSS.

### 5. Decide the gate

Return exactly one status:

- `CLARITY_GATE_PASS`
- `CLARITY_GATE_FAIL`
- `CLARITY_GATE_PASS_WITH_DOCUMENTED_EXCEPTIONS`

Fail the gate when a primary H1/H2 wraps avoidably, the design relies on generic AI visual tropes, the layout is materially unbalanced, or mobile hierarchy is broken. Technical success cannot override a visual failure.

## Required deliverables

For BUILD or HYBRID, produce a short clarity brief, heading budget, layout rules, and final audit. For AUDIT, produce an evidence-backed findings table and gate status. Preserve same-viewport before/after screenshots for meaningful redesigns.
