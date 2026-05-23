# Features

## What This Skill Does

`customer-acquisition-pipeline` is a workflow skill for lead generation and outbound preparation. It coordinates specialized companion skills instead of duplicating their documentation.

Core capabilities:

- Convert an ICP, offer, and source plan into a small acquisition pilot.
- Use public web data as lead evidence through `just-scrape`.
- Normalize and deduplicate leads before writing them into Lark Base.
- Create or update a practical CRM-style Lark Base schema.
- Use fit scores and statuses so the work can resume across sessions.
- Draft first-touch and follow-up cold emails with `cold-email`.
- Keep live sending outside the default scope until the user explicitly approves it.

## Intended Users

Use this pack when you repeatedly ask Codex to:

- Build a lead list for a product or service.
- Turn public websites or search results into prospect records.
- Maintain a Feishu/Lark Base customer table.
- Draft personalized outbound emails.
- Continue an acquisition workflow from a previous batch.

## Non-Goals

This skill does not:

- Bypass paywalls, login gates, or anti-bot protections.
- Guarantee replies, meetings, or revenue.
- Send emails by itself.
- Replace legal review for privacy, advertising, or email compliance.
- Store secrets in the repository.

## Default Field Model

The skill recommends a CRM table with fields for company, website, contact, role, email, source URL, evidence, ICP fit, status, draft email, follow-up sequence, owner, and last updated date.

## Status Model

Recommended statuses:

- `new`
- `researched`
- `needs-review`
- `drafted`
- `approved`
- `contacted`
- `replied`
- `not-fit`
