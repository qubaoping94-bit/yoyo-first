---
name: partner-sales-service-ai-frontdesk
description: Initialize and operate a partner enterprise knowledge base for leads, customers, quotations, orders, delivery, settlement, service, follow-up, and read-only management queries. Use for DEMO, SETUP, or LIVE partner sales and service operations requiring previews, authorized confirmation, historical snapshots, and append-only events.
---

# Partner Sales Service AI Frontdesk

On first run open `B模板_逐条IMA原生笔记/00｜先看这里/00-00｜第一次启用｜把企业资料交给AI.txt`, then follow `contracts/activation_contract.json`. Read only canonical `企业启用档案.json` schema `B-PARTNER-PROFILE-1.0.0`. `mode` is computed exclusively: incomplete or unauthorized is SETUP, complete authorized DEMO scope is DEMO, and complete authorized FORMAL scope is LIVE. The confirmation account must exist in employee permissions and possess `企业启用确认`. Activation never creates formal business records. Runtime configuration follows the partner/customer, quotation, order, payment-proof versus actual-receipt, stock-ready, shipment/logistics, sign-and-acceptance, outstanding balance, after-sales and follow-up chain. Queries are read-only and exclude DEMO by default.
