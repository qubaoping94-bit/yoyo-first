---
name: manufacturing-enterprise-operations-ai-frontdesk
description: Initialize and operate a manufacturing enterprise knowledge base across sales, orders, BOM, procurement, production, quality, delivery, finance, and after-sales. Use for DEMO, SETUP, or LIVE enterprise operations where previews, permission confirmation, historical snapshots, read-only queries, and append-only events are required.
---

# Manufacturing Enterprise Operations AI Frontdesk

On the first run, open `A模板_逐条IMA原生笔记/00｜先看这里/00-00｜第一次启用｜把企业资料交给AI.txt` and follow `contracts/activation_contract.json`. Read only the canonical `企业启用档案.json` schema `A-MFG-PROFILE-1.1.0`; DEMO configurations use exactly the same schema and differ only in values. `mode` is the single runtime state computed by the renderer: incomplete or unauthorized is SETUP, a complete authorized DEMO scope is DEMO, and only a complete authorized FORMAL scope is LIVE. The `confirmation` account must exist in `employees_roles_permissions`, match its name/role snapshot, and possess `企业启用确认`; a boolean or status alone never activates the profile. The administrator must not hand-edit JSON. Activation renders configuration only and keeps formal writes and formal records at 0. Queries stay read-only and exclude DEMO unless requested.
