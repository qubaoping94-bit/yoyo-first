---
name: customer-acquisition-pipeline
description: Use when a user wants Codex to run or design a lead generation, customer acquisition, outbound sales, 获客流水线, 线索挖掘, 飞书客户库, or cold outreach workflow using scraped public data, Lark Base CRM records, and cold email drafts.
---

# Customer Acquisition Pipeline

## Overview

Coordinate a Codex-managed acquisition loop: find public prospect signals, store normalized lead records in Lark Base, and draft personalized cold outreach. This skill is an orchestration layer; it routes work to companion skills instead of replacing them.

Companion skills:

- `just-scrape`: search, scrape, crawl, extract structured data, and monitor public web pages.
- `lark-shared`: authenticate and configure `lark-cli` safely before using Lark/Feishu resources.
- `lark-base`: create, update, query, and manage Lark Base tables, fields, records, views, and dashboards.
- `cold-email`: write B2B cold emails, subject lines, CTAs, and follow-up sequences.

## Operating Boundary

Default to research, CRM updates, and draft generation. Do not actually send outbound email, submit contact forms, message prospects, or run bulk automation unless the user explicitly asks for that action and the available toolchain supports it.

Respect site terms, robots restrictions, rate limits, privacy rules, and email compliance expectations. Treat personal contact data, auth tokens, Lark Base links, cookies, API keys, and prospect lists as sensitive.

Before destructive Lark actions such as deleting tables, fields, records, views, dashboards, or permissions, get explicit confirmation. Before any live outbound send, get explicit confirmation and show the exact message, recipient list, and sending method.

## Intake

Collect or infer the minimum viable brief:

- ICP: target industry, company type, role, region, size, buying trigger, exclusion criteria.
- Offer: product, pain solved, proof point, call to action, landing page or calendar link.
- Source plan: search queries, URLs, directories, competitor/customer lists, social proof sources, or seed accounts.
- Lark Base target: existing base/table link or permission to create a new lead database.
- Outreach preference: language, tone, CTA, follow-up count, compliance constraints.

If inputs are missing, proceed with a small pilot assumption and label it. Ask only for blockers such as missing Lark access, missing API credentials, or lack of an offer.

## Workflow

1. **Plan the acquisition loop**
   - Define the ICP and disqualifiers.
   - Convert the ICP into search queries and source URLs.
   - Define a pilot batch size before broad scraping; prefer 10-30 leads for the first pass.

2. **Acquire and extract leads**
   - Use `just-scrape` for search, page scraping, crawling, extraction, or monitoring.
   - Extract structured records rather than raw page dumps whenever possible.
   - Capture source URL, evidence snippet, and collection date for every lead.
   - Avoid bypassing paywalls, logins, bot protections, or private pages.

3. **Normalize and score**
   - Deduplicate by company domain, company name, contact email, and source URL.
   - Mark missing fields as unknown instead of inventing them.
   - Score fit using explicit ICP criteria and a short reason.
   - Put questionable records into `needs-review`, not into ready-to-contact.

4. **Create or update Lark Base**
   - Use `lark-shared` first if authentication, identity, scope, or permission state is unclear.
   - Use `lark-base` to create tables, fields, views, records, and dashboards.
   - Prefer updating existing matching records over creating duplicates.
   - Keep status fields current so the pipeline can resume later.

5. **Draft outreach**
   - Use `cold-email` after each lead has enough context for personalization.
   - Write emails from real lead evidence: company activity, role context, pain signal, or relevant trigger.
   - Keep the first email short, specific, and low-pressure.
   - Generate follow-ups that add useful angles instead of repeating the same ask.

6. **Report and hand off**
   - Summarize batch size, source coverage, Lark updates, draft count, skipped records, and blockers.
   - Include next recommended action: review leads, approve drafts, enrich missing data, or expand sources.

## Lark Base Schema

Use this baseline CRM table unless the user already has a schema:

| Field | Type | Notes |
|---|---|---|
| Company | text | Company or organization name |
| Website | url | Canonical website/domain |
| Contact Name | text | Use unknown when not available |
| Role | text | Decision maker or likely buyer role |
| Email | text | Store only if public or user-provided |
| Source URL | url | Where the evidence came from |
| Evidence | long text | Short factual reason this lead matches |
| ICP Fit | single select | high, medium, low, not-fit |
| Status | single select | new, researched, needs-review, drafted, approved, contacted, replied, not-fit |
| Draft Email | long text | Current best first-touch draft |
| Follow-up Sequence | long text | Multi-touch draft sequence |
| Owner | text | User/team owner if known |
| Last Updated | date | Update on every batch |

Useful views:

- New Leads: `Status = new or researched`
- Needs Review: missing email, weak evidence, or uncertain ICP fit
- Drafts Ready: `Status = drafted`
- Follow-up Queue: contacted leads with no reply after the chosen wait interval
- Not Fit Archive: low quality or excluded leads

## Quality Gates

Before marking a lead `drafted`, verify:

- The source is public and recorded.
- The company appears to match the ICP.
- The personalization point is specific and factual.
- The CTA matches the user's offer.
- The email does not imply facts that were not verified.

Before expanding from pilot to scale, verify:

- Duplicate rate is acceptable.
- Lark table fields and views are usable.
- Draft quality is good enough for human approval.
- The user understands that this skill does not send emails by default.

## Prompt Patterns

Reusable user prompts this skill should handle:

- "Use this Douyin workflow to build an automated acquisition pipeline for my AI consulting offer."
- "Find 20 public leads, put them in Feishu Base, and draft cold emails."
- "Take these target websites, scrape prospects, dedupe them, and create a Lark Base customer table."
- "Continue the获客流水线 from last time and draft follow-ups for leads that have not replied."
- "Turn this list of companies into a reviewed outbound campaign, but do not send anything."

## Final Response

Respond in the user's language. Include:

- What sources were searched or scraped.
- How many leads were found, deduped, accepted, and skipped.
- Lark Base table/view updates made or prepared.
- Outreach drafts generated and their status.
- Risks, missing permissions, or actions that still need approval.

If the user asked to package or publish the workflow, mention this skill as an independent skill package unless they explicitly requested a combined multi-skill bundle.
