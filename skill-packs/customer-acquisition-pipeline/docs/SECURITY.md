# Security

## Source Vetting

Companion skills were selected from named GitHub repositories:

- `ScrapeGraphAI/just-scrape`
- `larksuite/cli`
- `coreyhaines31/marketingskills`

The target skill folders contain documentation and references. The selected skill folders do not vendor executable scripts in this package.

## Sensitive Data

Treat these as sensitive:

- Lark/Feishu tokens and app secrets.
- ScrapeGraph API keys.
- Cookies, browser sessions, or private pages.
- Prospect lists and contact details.
- Lark Base URLs and record identifiers.

Never commit secrets into this repository. Keep `.env`, cookies, exported CRM lists, and raw lead data out of Git.

## Network and Data Boundaries

Use public, permitted data sources. Do not bypass paywalls, private groups, logins, bot protections, or terms that prohibit scraping.

Default output should be research, CRM records, and email drafts. Live sending requires explicit user approval and a separate sending-capable tool.

## Destructive Actions

Require explicit confirmation before:

- Deleting Lark Base records, tables, fields, views, dashboards, roles, or permissions.
- Replacing an existing CRM schema.
- Running high-volume scraping.
- Sending or scheduling outbound emails.

## Compliance Notes

Cold outreach can be regulated by jurisdiction and channel. Confirm unsubscribe language, sender identity, legitimate interest/consent basis, and suppression lists before live sending.
