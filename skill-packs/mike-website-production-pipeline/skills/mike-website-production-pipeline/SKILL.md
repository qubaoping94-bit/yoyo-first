---
name: mike-website-production-pipeline
description: Orchestrate complete website production from product definition and visual direction through Figma implementation, design-system refinement, anti-AI-template review, GSAP motion, responsive QA, approval, deployment, and rollback. Use when creating, redesigning, upgrading, auditing, accepting, or releasing a website, landing page, brand site, product site, portfolio, content site, or web application, especially when the work should combine Product Design, Figma, Hallmark, Taste Skill, GSAP Skills, GPT-5.6, and mike-web-clarity-gate.
---

# Mike Website Production Pipeline

Operate as the single workflow controller. Route specialized work to the relevant installed skills; do not merge their instructions into improvised rules. Preserve one source of truth, one approved visual direction, and explicit Gate status.

## Load references

Read [references/full-workflow.md](references/full-workflow.md) for every new site, major redesign, full-site audit, or release. For a small isolated edit, use the relevant phase only.

Read the focused dependency skill before invoking it:

- Product definition or visual exploration: Product Design `index`, `get-context`, `ideate`, `image-to-code`, `audit`, or `design-qa`.
- Confirmed Figma source: `figma`.
- Macrostructure, design DNA, tokens, anti-slop build/redesign: `hallmark`.
- Typography, palette, density, component proportion, redesign refinement: `design-taste-frontend`.
- Heading brevity, non-AI visual language, coordinated layout, final visual gate: `mike-web-clarity-gate`.
- Motion: the narrowest applicable GSAP skill, such as `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-react`, `gsap-plugins`, or `gsap-performance`.

If a required plugin or skill is unavailable, report that gap and use the best local fallback without pretending the missing capability ran.

## Non-negotiable order

```text
Preflight and baseline
→ Product and user outcome
→ Select one visual-source route
→ Lock design system and heading budget
→ Grey wireframe and responsive structure
→ Static high-fidelity implementation
→ Source-vs-render design QA
→ Static visual gates
→ Motion specification
→ GSAP implementation
→ Full QA
→ Approval freeze
→ Deploy and production revalidation
```

Do not reorder these dependencies. In particular:

- Do not write high-fidelity UI without one visual source of truth.
- Do not generate visual directions when an approved Figma frame already controls the work.
- Do not add complex GSAP before the static visual gates pass.
- Do not let automated checks override an explicit human visual rejection.
- Do not modify an approved baseline directly; create an isolated candidate.

## Phase 0: Preflight

1. Read project instructions and relevant long-term memory.
2. Inspect repository status, framework, routes, scripts, design files, tokens, assets, Storybook, and current deployment.
3. Identify user-owned changes and protected surfaces.
4. Capture same-viewport baseline evidence for redesigns.
5. Write current scope, protected items, allowed changes, and release authority.

Gate: project path, scope, baseline, and authority are unambiguous.

## Phase 1: Product brief

Use Product Design `get-context` when the product target or intended user outcome needs structure. Define audience, task, offer, evidence, primary action, routes, content sources, and five-second understanding.

Gate: the site can answer who it is, what it offers, who it serves, why it is credible, and what the user should do next.

## Phase 2: Choose one visual route

Choose exactly one:

- `FIGMA`: Read exact node context, metadata when needed, screenshot, variables, components, and assets. Begin implementation only after structured context and screenshot both exist.
- `IDEATE`: With no visual target, use Product Design to generate exactly three distinct high-fidelity directions. Stop until the user selects one.
- `REFERENCE`: For a selected screenshot or mock, use Product Design `image-to-code`.
- `CLONE`: For faithful frontend recreation of a live public URL, use Product Design `url-to-code`.
- `DNA`: For inspiration without copying, use Hallmark `study`, present the diagnosis, and wait for adoption.
- `REDESIGN`: Audit the existing site first, then use Hallmark `redesign`, Taste, and Mike clarity review.

Gate: one visual source of truth is selected and recorded. Multiple unmerged targets block implementation.

## Phase 3: Design contract

1. Use Hallmark to choose macrostructure, theme, token system, and section diversity.
2. Use Taste to set the design read and calibrate variance, motion, density, type, color, spacing, radius, shadows, and icon family.
3. Use Mike clarity gate to create a heading budget and layout rules.
4. Record the approved source, token ownership, responsive exceptions, and protected elements.

Desktop H1/H2/H3 default to one line. Rewrite before shrinking. Allow a second line only with a documented semantic reason.

Gate: one design system, one accent logic, one radius rule, one icon family, and a heading budget exist.

## Phase 4: Wireframe

Build a grey, real-copy wireframe. Validate navigation, reading order, container alignment, column ratios, section purpose, CTA position, mobile reordering, and heading lines before decorative styling.

Gate: 1440, 1024, 390, and 360 layouts are structurally coherent. No meaningless empty stage, title domination, or desktop leftovers on mobile.

## Phase 5: Static implementation

Translate the approved visual source into maintainable project code. Reuse the existing framework, components, tokens, routing, state, assets, and accessibility patterns. Implement real DOM and required loading, empty, error, disabled, hover, focus, and active states.

Keep core content visible without JavaScript. Do not use a screenshot as the page. Do not add complex animation yet.

Gate: build and core interactions work; the static page is ready for visual comparison.

## Phase 6: Static QA

Run all three layers:

1. Product Design `design-qa`: compare source and implementation at the same viewport and state. Fix every P0/P1/P2 and rerun until `design-qa.md` says `final result: passed`.
2. Hallmark + Taste: audit template fingerprints, macrostructure drift, type, color, density, radius, components, and design-system integrity.
3. `mike-web-clarity-gate`: measure heading lines and overflow, then perform the human non-AI-language and layout-coordination review.

Gate: design QA passed, Hallmark/Taste have no blocking issue, and Mike returns `CLARITY_GATE_PASS` or an explicitly approved exception.

## Phase 7: Motion spec and GSAP

Write `MOTION_SPEC.md` first. For every motion record trigger, purpose, target, property, duration, ease, interrupt behavior, mobile behavior, reduced-motion behavior, and cleanup.

Use the narrowest GSAP skills required. Prefer timelines, transform, opacity, responsive matchMedia, React cleanup, and performance-safe updates. Motion must not change approved heading lines, content visibility, or layout dimensions.

Gate: motion has a stated purpose, core content remains available without it, reduced motion works, and no layout or performance regression appears.

## Phase 8: Full QA

Verify current source, current build, and current URL:

- build, typecheck, lint, tests, routes, refresh, direct inner-page access;
- console, page, request, asset, font, and image failures;
- 1440, 1024, 390, 360 plus project-specific viewports;
- overflow, collision, clipping, heading orphans, 200% zoom;
- keyboard, focus, Esc, contrast, semantics, reduced motion;
- loading, empty, error, disabled, and critical user tasks;
- motion continuity, interruption, cleanup, and performance;
- source-versus-render and before-versus-after evidence.

Gate: no unresolved P0/P1/P2, no clarity failure, and no release blocker hidden behind a technical pass.

## Phase 9: Approval and release

Only the user can approve the visual baseline. Freeze the approved version with source hash, commit, build, screenshots, QA report, and date. Create future changes from an isolated copy.

Deploy only with explicit release authority. Record production URL, deployment ID, previous rollback ID, canonical, robots, sitemap, critical routes, and production QA. Revalidate production instead of reusing local evidence.

## Required statuses

Use precise states:

- `DISCOVERY_IN_PROGRESS`
- `AWAITING_VISUAL_SELECTION`
- `DESIGN_CONTRACT_READY`
- `WIREFRAME_GATE_FAIL` or `WIREFRAME_GATE_PASS`
- `STATIC_QA_BLOCKED` or `STATIC_QA_PASS`
- `MOTION_QA_BLOCKED` or `MOTION_QA_PASS`
- `RELEASE_BLOCKED`
- `READY_FOR_USER_VISUAL_REVIEW`
- `DELIVERY_APPROVED`
- `PRODUCTION_VALIDATED`

Never use `done`, `complete`, or `approved` when a later required Gate remains open.

## Project templates

To create the standard evidence files in a project, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/init-website-workflow.ps1 -ProjectRoot <project-path>
```

The script creates only missing files under `docs/website-workflow`; it never overwrites existing evidence.

## Handoff

Lead with the current Gate outcome. List changed routes, evidence, unresolved findings, protected baseline, release status, and the next authorized action. Keep implementation claims separate from user approval and production validation.
