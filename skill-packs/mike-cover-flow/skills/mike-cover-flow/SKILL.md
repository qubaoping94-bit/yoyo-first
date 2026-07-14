---
name: mike-cover-flow
description: Build or integrate a Cover Flow / immersive image carousel for websites using Mike's accepted interaction, composition, content, audio, accessibility, and production QA standards. Use when a user asks for 图片流、图片滚动、Cover Flow、沉浸看图、3D 卡片轮播、首页图片流，or wants the approved UUAI-gallery-style effect reused on another website.
---

# Mike Cover Flow

Build a website-native image experience, not a dark demo stage or generic slider. Preserve the host site's content model and visual language while applying the interaction contract below.

## Start from the host site

1. Inspect the real page, data source, existing gallery/detail/download behavior, breakpoints, and deployment boundary.
2. Decide the placement before coding. Prefer a dedicated immersive route or a homepage hero replacement only when explicitly approved.
3. Keep existing search, grid, lightbox, downloads, text sections, and downstream homepage layout unless the user asks to replace them.
4. Use real project data. Do not duplicate original images or invent titles, prompts, categories, counts, or production status.
5. Build an isolated local preview first when placement or composition is still under review. Do not call a preview integrated, deployed, or live.

## Interaction contract

- Store position as a continuous floating-point value. Never drive pointer or wheel motion by integer-index jumps.
- Animate through one `requestAnimationFrame` loop with spring/damping or equivalent inertial integration.
- Make release velocity affect travel distance: slow drag, quick flick, and trackpad wheel must feel materially different.
- Decay velocity naturally, then settle to the nearest detent. Do not snap immediately on pointer release.
- Interpolate every card continuously through center: `translateX`, `translateZ`, `rotateY`, `scale`, `opacity`, blur, and shadow.
- Keep loop boundaries continuous. Crossing first/last must not reverse, flash, or jump.
- Support mouse press-drag, touch horizontal drag, trackpad/wheel, arrow keys, Home/End where useful, and side-card click.
- Drag only after `pointerdown`. Never switch cards on hover.
- Add pointer micro-parallax without changing the active item.
- Update transforms and opacity through refs/direct DOM writes. Avoid per-frame framework state rerenders and layout properties.
- Prevent text selection, native image dragging, layout shaking, and accidental horizontal page overflow.

Use the accepted spatial baseline as the first calibration target when the card format fits: perspective `1800px`, center card around `350×480`, orbit top near `51%`, adjacent horizontal spacing around `306px` then `136px`, depth `190 - 54 * abs(offset)`, and rotation around `62deg * sign(offset) * pow(min(abs(offset),1),1.65)`. Adapt proportionally for natural image aspect ratios; do not copy numbers blindly when they damage composition.

## Image composition contract

- Show the actual image completely by default. Preserve its natural aspect ratio and never stretch it.
- Prefer the original/full image for the center card and lightweight thumbnails for neighboring cards. Load only one center original at a time.
- Do not use `object-fit: cover` when it cuts people, products, titles, brand marks, or important composition.
- Do not automatically crop white borders if that changes the complete artwork. A thumbnail canvas border is not permission to crop the source image.
- Size the center image for the whole page composition, not to fill every available pixel. It must feel balanced with the header and following sections.
- Keep 5–9 DOM cards. For large libraries, browse the full result set through a windowed 5–9-node renderer.
- Lazy-load images and provide loading, failure, empty-result, and remote-index states.

## Visual integration contract

- Make the Cover Flow float transparently in the host site's own background. Do not introduce a black/dark-gray stage, black card frames, empty hats, or a full-width dark metadata bar unless the site's established design explicitly requires them.
- Remove visible seams between the Cover Flow and adjacent sections. Match the actual rendered background on the concrete child containers, not only outer wrappers.
- Validate seams with screenshots and pixel sampling; computed `background-color` alone is insufficient because background images/gradients can still differ.
- Avoid iframe integration for final production when it creates independent backgrounds, sizing gaps, duplicated controls, or accessibility boundaries. If an iframe is unavoidable, force both documents and all stage containers to the same background and test the rendered pixels.
- Keep metadata and actions minimal. If needed, use a small corner glass panel that never competes with the image. If the user asks to remove it, remove it entirely.
- Do not show a prominent sound toggle when the user wants sound on by default. Keep sound enabled and unlock Web Audio on the first real user gesture as browsers require.
- Keep the homepage header and all approved downstream content in their existing order. Remove duplicate navigation CTAs when the new hero already provides that destination.

## Audio contract

Create restrained original Web Audio cues; do not ship copied audio assets.

- `detent`: brief, quiet tick when crossing an item boundary.
- `flick`: short filtered whoosh only for genuinely fast release.
- `land`: soft low cue when settling.
- Limit rate, gain, and simultaneous voices. Never emit sound every frame.
- Default to enabled when requested, but create/resume `AudioContext` only after a genuine pointer, wheel, click, or keyboard gesture.
- Suspend audio while the document is hidden.
- Respect a mute preference only when a visible mute control or explicit product requirement exists.

## Mobile, accessibility, and fallback

- Preserve vertical page scrolling. Use `touch-action: pan-y`; do not lock the page for horizontal gestures.
- Keep interactive targets at least `44×44px`.
- Ensure 360, 390, 430, 768, 1440, and relevant landscape views do not overflow horizontally.
- Provide keyboard operation, visible focus, meaningful region/carousel labels, active-item semantics, and polite announcements without per-frame screen-reader noise.
- Under `prefers-reduced-motion`, shorten or remove inertia/parallax and provide controlled discrete transitions.
- Provide a usable no-JS fallback, usually a simple list/grid or direct links.

## Placement exclusions

Do not use Cover Flow for navigation, AI conversations, forms, long-form reading, evidence pages, full directories, or an unwindowed complete gallery. Do not place it in a hero unless the user explicitly approves hero replacement. Keep item count in a curated component to 4–9; use windowing for a large browseable dataset.

## Production workflow

1. Reproduce the accepted physics in an isolated 5-card sample if interaction fidelity is uncertain.
2. Build a same-screen calibration mode or deterministic input trace when matching a reference. Compare keyframes rather than judging only by memory.
3. Integrate real data with windowing, center-original loading, details, URL state, and existing site actions.
4. Tune composition using desktop and mobile screenshots. Treat user-marked screenshots as binding visual evidence.
5. Validate the final host page, not only the isolated component.
6. Deploy only after explicit approval. Preserve a rollback point and recheck the production domain after deployment.

## Required evidence

Report measured results, never assumed “60fps”. Capture:

- Average and maximum frame interval and long tasks during deterministic drag/wheel/flick traces.
- Console errors, page errors, failed responses, and horizontal overflow.
- Active DOM card count, full-image request count, result count, and center-image natural/display ratio.
- Desktop and mobile screenshots; include the user's reported viewport when provided.
- Background pixel samples across any disputed section seam.
- Keyboard, pointer, wheel, reduced-motion, screen-reader semantics, and no-JS checks.
- HTTP 200 for the host page and any dedicated route.

For a production build, target roughly `10–15kB gzip` for the native motion core when practical, without sacrificing required accessibility or correctness.

## Failure patterns to reject

- Integer index changes inside `pointermove` or `wheel`.
- Immediate one-card snap after every drag.
- React/framework state updates every animation frame.
- Hover-to-switch behavior.
- `object-fit: cover` that cuts the actual artwork.
- Large lower-left metadata panels that obscure the gallery.
- Dark stage/card chrome pasted onto a warm or white site.
- Backgrounds that are numerically declared equal but visibly differ because of gradients, child backgrounds, iframe remainder space, or stale screenshots.
- Reporting an old cached screenshot as current evidence. Use unique evidence paths and confirm timestamps/pixels.
- Claiming integration, deployment, or production verification before it actually happened.

End with an explicit status distinguishing local preview, locally integrated build, deployment-ready handoff, and production-verified release.

