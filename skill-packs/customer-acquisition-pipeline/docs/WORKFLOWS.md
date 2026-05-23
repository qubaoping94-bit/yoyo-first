# Workflows

## Pilot Lead Batch

1. Define ICP and exclusions.
2. Pick 3-5 sources or search queries.
3. Use `just-scrape` to collect a small public-data batch.
4. Normalize and dedupe leads.
5. Use `lark-base` to create or update lead records.
6. Use `cold-email` to draft short, personalized first-touch emails.
7. Report accepted leads, skipped leads, Lark updates, and draft status.

## Existing Lark Base Continuation

1. Use `lark-shared` if authentication or identity is unclear.
2. Use `lark-base` to inspect the existing table and fields.
3. Query records by status, such as `new`, `needs-review`, or `drafted`.
4. Fill missing research with `just-scrape` only when needed.
5. Generate or revise drafts with `cold-email`.
6. Update status and last-updated fields.

## Review Before Outreach

1. Filter Lark records where `Status = drafted`.
2. Inspect evidence, ICP fit, and the draft email.
3. Separate weak records into `needs-review`.
4. Mark approved records as `approved`.
5. Do not send email unless the user explicitly approves a sending tool, recipient list, and message content.

## Scaling the Pipeline

Scale only after the pilot has acceptable quality:

- Duplicate rate is low.
- Lark views make review easy.
- Email drafts sound specific and human.
- The user approves the ICP assumptions.
- Compliance boundaries are clear.

## Common Prompt

```text
Use $customer-acquisition-pipeline to find 20 public leads for my AI consulting offer, put them into my Feishu Base, draft one cold email and two follow-ups for each, but do not send anything.
```
