---
name: ai-product-delivery-pipeline
description: Use when a user wants to build, improve, audit, or launch an AI web product, AI SaaS, internal AI tool, agent application, or React/Next.js product that needs engineering quality, UX polish, AI architecture, Azure AI services, validation, and deployment.
---

# AI Product Delivery Pipeline

## Overview

Use this as the orchestration skill for shipping an AI product end to end. It does not replace specialist skills; it decides which specialist skill to load, in what order, and what gate must pass before moving on.

## When to Use

Use for:

- AI SaaS, AI web apps, internal AI tools, agent products, dashboards, and customer-facing demos that must become real products.
- React or Next.js products that need performance, UX, AI service integration, and Azure deployment.
- Requests like "build the whole product", "make this demo production-ready", "ship it", "turn this into an AI product", or "from idea to launch".

Do not use for:

- A tiny one-file edit with no product workflow.
- Pure research, copywriting, or slide work with no app delivery.
- Non-Azure deployment unless the user explicitly asks to adapt the workflow.

## Operating Principle

Move through the pipeline only as far as the user's request justifies. For a design-only request, stop after the UX gate. For a local prototype, stop before Azure preparation. For launch, continue through validation and deployment.

Before each major phase, inspect the current workspace and identify what already exists. Do not recreate working code, infrastructure, or plans without a reason.

## Pipeline

| Phase | Goal | Specialist skill |
|---|---|---|
| 0. Intake | Clarify product, users, data, AI features, deployment target, budget, and deadline | none |
| 1. Delivery plan | Break scope into implementation milestones and acceptance checks | `Code`, `writing-plans` when available |
| 2. Product build | Implement or refactor the app with focused tests and verification | `Code`, `test-driven-development` when useful |
| 3. React quality | Improve React/Next.js structure, performance, rendering, data fetching, and bundle size | `vercel-react-best-practices` |
| 4. UX polish | Build or audit interface quality, visual system, responsive behavior, and accessibility | `frontend-design`, then `web-design-guidelines` |
| 5. AI architecture | Design agents, prompts, evaluation, monitoring, Foundry project structure, and model lifecycle | `microsoft-foundry` |
| 6. Azure AI services | Connect OpenAI, AI Search, OCR, speech, translation, or document intelligence | `azure-ai` |
| 7. AI governance | Add APIM AI gateway, semantic cache, token limits, model governance, content safety, or MCP rate limits when needed | `azure-aigateway` |
| 8. Azure preparation | Generate or update Azure deployment plan, infra, `azure.yaml`, Dockerfiles, and managed identity configuration | `azure-prepare` |
| 9. Preflight validation | Run deployment readiness checks and record validation proof | `azure-validate` |
| 10. Deployment | Execute deployment and verify live endpoints | `azure-deploy` |
| 11. Launch report | Summarize URLs, risks, follow-ups, tests, and operational notes | none |

## Phase Gates

- Do not run deployment commands before `azure-prepare` and `azure-validate` have completed successfully.
- Do not mark Azure deployment ready unless `.azure/deployment-plan.md` exists and has the required status for the next Azure skill.
- Do not use `azure-deploy` to create infrastructure from scratch; use `azure-prepare` first.
- Do not add AI gateway complexity unless the product needs governance, rate limits, caching, multi-model routing, tenant control, compliance, or cost controls.
- Do not ship UI changes without checking mobile layout, text overflow, loading states, empty states, and error states when a frontend exists.
- For cloud or production work, surface destructive actions, cost implications, and account/subscription assumptions before execution.

## Routing Rules

- **New product from scratch**: intake -> plan -> build -> React quality -> UX -> AI architecture -> Azure AI -> prepare -> validate -> deploy.
- **Existing app, needs polish**: inspect -> React quality -> UX -> tests -> report.
- **Existing AI demo, needs production**: inspect -> AI architecture -> Azure AI -> AI governance if needed -> prepare -> validate -> deploy.
- **Only deploy request**: inspect for `.azure/deployment-plan.md`; if absent, route to `azure-prepare`; if present but not validated, route to `azure-validate`; deploy only after validation.
- **Foundry agent request**: route through `microsoft-foundry`; then integrate service/UI/deployment phases only if the user asks for a product surface or launch.
- **Non-Azure cloud request**: do not force Azure skills. Ask for the deployment target or use the relevant deployment skill if installed.

## Intake Checklist

Capture only what is needed to move:

- Product type: SaaS, internal tool, agent, dashboard, website, API, workflow automation.
- Users and top 3 jobs-to-be-done.
- AI capabilities: chat, agent, search/RAG, OCR, speech, tool use, automation, evaluation, fine-tuning.
- Data and security: source data, privacy constraints, auth, tenant model, logs, retention.
- Frontend stack and backend stack.
- Launch target: local demo, staging, production, Azure subscription/region if known.
- Success checks: functional tests, UX criteria, model quality, latency, cost, live URL.

## Completion Contract

At the end of a pipeline run, report:

- What phases were completed.
- Which specialist skills were used.
- What changed in the workspace.
- Verification performed and any failures.
- Deployment status and live URLs when applicable.
- Remaining risks, missing credentials, subscription assumptions, or user approvals needed.

## Installed Companion Skills

This pipeline expects these companion skills to exist when the corresponding phase is needed:

- `vercel-react-best-practices`
- `web-design-guidelines`
- `frontend-design`
- `microsoft-foundry`
- `azure-ai`
- `azure-aigateway`
- `azure-prepare`
- `azure-validate`
- `azure-deploy`

If a companion skill is missing and the user asked for an end-to-end delivery workflow, install or request installation of the missing skill before continuing.
