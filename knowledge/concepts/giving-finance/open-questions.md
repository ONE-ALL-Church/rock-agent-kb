---
concept_id: giving-finance
title: Giving And Finance Open Questions
generated: true
---

# Giving And Finance Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `9-statements-deep-dive-statement-eligibility`: Statement Eligibility (111 words)
- `16-implementation-playbooks-playbook-add-a-new-giving-account`: Playbook: Add A New Giving Account (115 words)
- `16-implementation-playbooks-playbook-build-a-giving-analytics-report`: Playbook: Build A Giving Analytics Report (99 words)

## Community-Supported Only

- `7-common-giving-and-finance-workflows-external-giving-imports`: External Giving Imports
- `8-transactions-deep-dive-transaction-attributes`: Transaction Attributes
- `9-statements-deep-dive-receipts-vs-statements`: Receipts Vs Statements
- `11-related-rock-areas-people-groups-workflows-security-reporting-workflows`: Workflows
- `12-administration-and-operational-guardrails-account-governance`: Account Governance
- `13-developer-api-lava-and-source-code-landmarks-lava-considerations`: Lava Considerations
- `16-implementation-playbooks-playbook-import-giving-from-an-external-system`: Playbook: Import Giving From An External System
- `18-agent-task-recipes-recipe-giving-automation-review`: Recipe: Giving Automation Review
- `18-agent-task-recipes-recipe-pledge-progress-analysis`: Recipe: Pledge Progress Analysis

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-financial-accounts`: Financial Accounts
- `5-core-configuration-and-data-model-financial-gateways`: Financial Gateways
- `5-core-configuration-and-data-model-blocks-and-pages`: Blocks And Pages
- `6-primary-entities-and-relationships-batches-and-transactions`: Batches And Transactions
- `6-primary-entities-and-relationships-scheduled-transactions-and-payment-plans`: Scheduled Transactions And Payment Plans
- `6-primary-entities-and-relationships-pledges`: Pledges
- `6-primary-entities-and-relationships-people-personalias-businesses-families-and-giving-units`: People, PersonAlias, Businesses, Families, And Giving Units
- `7-common-giving-and-finance-workflows-text-giving`: Text Giving
- `7-common-giving-and-finance-workflows-manual-entry-and-check-processing`: Manual Entry And Check Processing
- `7-common-giving-and-finance-workflows-external-giving-imports`: External Giving Imports
- `8-transactions-deep-dive-transaction-dates`: Transaction Dates
- `8-transactions-deep-dive-transaction-types`: Transaction Types
- `8-transactions-deep-dive-transaction-security`: Transaction Security
- `9-statements-deep-dive-statement-recipients`: Statement Recipients
- `9-statements-deep-dive-statement-eligibility`: Statement Eligibility
- `10-batches-deep-dive-batch-fields-to-inspect`: Batch Fields To Inspect
- `10-batches-deep-dive-automated-batches`: Automated Batches
- `10-batches-deep-dive-check-scanning-and-mobile-batch-processing`: Check Scanning And Mobile Batch Processing
- `11-related-rock-areas-people-groups-workflows-security-reporting-people`: People
- `11-related-rock-areas-people-groups-workflows-security-reporting-groups`: Groups
- `11-related-rock-areas-people-groups-workflows-security-reporting-workflows`: Workflows
- `11-related-rock-areas-people-groups-workflows-security-reporting-reporting`: Reporting
- `12-administration-and-operational-guardrails-change-control`: Change Control
- `12-administration-and-operational-guardrails-gateway-governance`: Gateway Governance
- `12-administration-and-operational-guardrails-receipt-and-statement-controls`: Receipt And Statement Controls
- `13-developer-api-lava-and-source-code-landmarks-api-considerations`: API Considerations
- `13-developer-api-lava-and-source-code-landmarks-lava-considerations`: Lava Considerations
- `13-developer-api-lava-and-source-code-landmarks-mobile-developer-landmarks`: Mobile Developer Landmarks
- `14-reporting-analytics-and-model-map-giving-analytics`: Giving Analytics
- `14-reporting-analytics-and-model-map-bi-financial-transaction-reporting`: BI Financial Transaction Reporting
- `15-version-and-release-caveats`: 15. Version And Release Caveats
- `16-implementation-playbooks-playbook-add-a-new-giving-account`: Playbook: Add A New Giving Account
- `16-implementation-playbooks-playbook-configure-online-giving`: Playbook: Configure Online Giving
- `16-implementation-playbooks-playbook-enable-mobile-batch-check-scanning`: Playbook: Enable Mobile Batch Check Scanning
- `16-implementation-playbooks-playbook-build-a-giving-analytics-report`: Playbook: Build A Giving Analytics Report
- `16-implementation-playbooks-playbook-import-giving-from-an-external-system`: Playbook: Import Giving From An External System

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
