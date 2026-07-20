# Full website workflow reference

## Contents

1. Capability map
2. Route selection
3. Deliverables by phase
4. Gate criteria
5. Conflict rules
6. Project variants
7. Final checklist

## 1. Capability map

| Capability | Invocation | Primary job | Boundary |
|---|---|---|---|
| Product Design | `get-context`, `research`, `ideate`, `audit`, `image-to-code`, `url-to-code`, `design-qa` | Product structure, visual exploration, implementation from selected visual, comparison QA | No build before a visual target is selected |
| Figma | `figma` | Exact node context, screenshot, variables, components, assets, design-to-code grounding | Requires a precise accessible node; output is not final project architecture |
| Hallmark | `hallmark build/audit/redesign/study` | Macrostructure, design DNA, tokens, section diversity, anti-slop gate | Study structure rather than copy third-party content |
| Taste | `design-taste-frontend` | Design read, typography, color, density, spacing, radius, component proportion, redesign audit | Best for marketing, portfolio, and redesign; not the sole product-UX authority |
| Mike clarity | `mike-web-clarity-gate` | Single-line headings, non-AI language, coordinated layout, mobile hierarchy, final visual veto | Human review remains required |
| GSAP | focused GSAP skills | Timeline, ScrollTrigger, React, plugins, responsive motion, performance | Motion begins only after static approval |
| GPT-5.6 | active Codex model | Synthesis, engineering, debugging, QA orchestration | Cannot replace source truth or approval |

Source links:

- Figma: https://www.figma.com/
- Taste: https://github.com/Leonxlnx/taste-skill
- Hallmark: https://github.com/Nutlope/hallmark
- GSAP skills: https://github.com/greensock/gsap-skills
- Mike clarity: https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/mike-web-clarity-gate

## 2. Route selection

### New site with approved Figma

`get-context → figma context+screenshot → design contract → wireframe → static implementation → design-qa → clarity → motion → full QA`

Do not run visual ideation unless the user asks to challenge or replace the approved design.

### New site without visual source

`get-context → ideate exactly three directions → user selection → Hallmark/Taste contract → heading budget → wireframe → image-to-code → QA → motion`

Stop at `AWAITING_VISUAL_SELECTION` after presenting the three directions.

### Existing site redesign

`baseline freeze → Product Design audit → Hallmark redesign → Taste audit → Mike clarity findings → representative pages → same-viewport comparison → full-site expansion → motion → QA`

Do not expand the entire site until representative pages pass.

### Reference-inspired site

Use Hallmark `study` when the user wants the DNA, not a clone. Use Product Design URL/image-to-code for faithful reconstruction within authorization and copyright boundaries.

## 3. Deliverables by phase

| Phase | Required artifacts |
|---|---|
| Preflight | `PROJECT_CONTEXT.md`, `PROTECTED_BASELINE.md`, baseline screenshots |
| Product | `SITE_BRIEF.md`, `SITEMAP.md`, `USER_JOURNEYS.md`, `CONTENT_SOURCE_LEDGER.md` |
| Visual route | `VISUAL_SOURCE.md`, Figma mapping or selected direction |
| Contract | `DESIGN_DIRECTION.md`, `tokens.css`, `HEADING_BUDGET.md`, `LAYOUT_RULES.md` |
| Wireframe | wireframe source and 1440/390 screenshots |
| Static build | runnable implementation, component/token mapping |
| Static QA | `design-qa.md`, clarity audit JSON/screenshots, findings |
| Motion | `MOTION_SPEC.md`, video/frames, reduced-motion evidence |
| Full QA | `QA_REPORT.md`, viewport evidence, current build identifiers |
| Release | `APPROVED_BASELINE.md`, `RELEASE_REPORT.md`, manifest, deployment and rollback IDs |

## 4. Gate criteria

### Product Gate

- Identity, offer, audience, evidence, and next action are concrete.
- Content sources are verified, supplied, pending, or prohibited; generated material is not presented as evidence.

### Visual Source Gate

- One selected source controls implementation.
- Source and target viewport are available.
- Missing named assets or inaccessible connectors are reported, not silently ignored.

### Design Contract Gate

- One token system and component language.
- One accent logic, radius rule, icon family, and responsive strategy.
- Desktop H1/H2/H3 have a one-line default budget.
- Forbidden AI-template habits are recorded.

### Wireframe Gate

- Clear navigation and content order.
- Stable shared container and alignment lines.
- One primary reading start and visual focus per screen.
- Mobile is recomposed by importance.
- No oversized empty stage or avoidable heading wrap.

### Static Gate

- Same-state, same-viewport source comparison.
- No actionable P0/P1/P2.
- No generic AI-template fingerprint.
- Mike clarity pass.
- Core page usable with motion disabled.

### Motion Gate

- Every motion has a purpose.
- Transform/opacity preferred; layout properties avoided.
- Responsive and reduced-motion variants work.
- Lifecycle cleanup and interruption work.
- Static composition and heading lines do not regress.

### Release Gate

- Current build and evidence correspond.
- User visual approval is explicit.
- Production authority is explicit.
- Production domain passes fresh QA.
- Rollback target is recorded.

## 5. Conflict rules

Resolve conflicts in this order:

1. User instruction and approved baseline.
2. Brand/product facts and approved Figma.
3. Mike clarity hard gates.
4. Selected Product Design direction.
5. Hallmark macrostructure and tokens.
6. Taste refinement.
7. GSAP enhancement.
8. Model preference.

When a lower-priority skill conflicts with a higher source, adapt or skip the lower rule and document why.

## 6. Project variants

### Enterprise or professional service

Prefer bright/neutral reading surfaces, direct product language, evidence, stable grid, restrained motion, and visible consultation path.

### Brand or marketing site

Allow stronger macrostructure and imagery, but preserve concise headings, real brand specificity, and a usable conversion path.

### Product or SaaS

Prioritize real UI, task flow, states, responsive interaction, and product proof. Taste is a refinement layer, not a replacement for Product Design UX structure.

### Dashboard or complex app

Use Product Design and the project's component system as primary. Apply Mike clarity to hierarchy and layout. Use Taste selectively because its default scope excludes dense dashboards and multi-step product UI.

### Portfolio or editorial site

Taste and Hallmark may lead visual direction. Keep title length, content truth, navigation, accessibility, and performance gates unchanged.

## 7. Final checklist

- [ ] Project, scope, authority, and protected baseline are explicit.
- [ ] Product target and user outcome are clear.
- [ ] One visual-source route is selected.
- [ ] Figma context and screenshot both exist when Figma is used.
- [ ] Three directions were shown and one selected when no visual source existed.
- [ ] Design tokens and component rules are unified.
- [ ] Heading budget exists and avoids dramatic forced wrapping.
- [ ] Wireframe passed desktop and mobile structure.
- [ ] Static implementation uses real DOM and complete states.
- [ ] Design QA passed at matching viewport/state.
- [ ] Hallmark and Taste found no blocking template/system issue.
- [ ] Mike clarity gate passed.
- [ ] Motion spec preceded GSAP implementation.
- [ ] Reduced motion and cleanup work.
- [ ] Full technical, responsive, accessibility, and interaction QA passed.
- [ ] User approved the visual baseline.
- [ ] Approved baseline was frozen before further edits.
- [ ] Production was revalidated and rollback recorded.
