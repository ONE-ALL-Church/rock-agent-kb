---
concept_id: giving-finance
title: Giving And Finance Open Questions
generated: true
---

# Giving And Finance Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `source-map-community-example`: Community example

## Needs Live Verification

- `scope-and-boundaries`: Scope And Boundaries
- `mental-model`: Mental Model
- `transactions`: Transactions
- `payment-gateways`: Payment Gateways
- `online-giving-and-receipts`: Online Giving And Receipts
- `text-giving`: Text Giving
- `batches`: Batches
- `giving-units-businesses-and-pledges`: Giving Units, Businesses, And Pledges
- `reporting-and-reconciliation`: Reporting And Reconciliation
- `security-and-administration`: Security And Administration
- `troubleshooting-decision-tree-a-gateway-accepted-a-payment-but-no-rock-transaction-is-visible`: A gateway accepted a payment, but no Rock transaction is visible
- `troubleshooting-decision-tree-a-transaction-is-in-the-wrong-batch-or-no-expected-batch-exists`: A transaction is in the wrong batch or no expected batch exists
- `troubleshooting-decision-tree-a-statement-omits-a-gift-includes-an-unexpected-gift-or-combines-the-wrong-people`: A statement omits a gift, includes an unexpected gift, or combines the wrong people
- `troubleshooting-decision-tree-giving-overview-journey-or-alerts-appear-stale-or-incorrect`: Giving Overview, Journey, or alerts appear stale or incorrect
- `troubleshooting-decision-tree-text-giving-setup-processing-refund-or-failure-messaging-does-not-work`: Text Giving setup, processing, refund, or failure messaging does not work
- `troubleshooting-decision-tree-users-can-see-finance-data-they-should-not-see-or-cannot-see-an-embedded-dashboard`: Users can see finance data they should not see, or cannot see an embedded dashboard
- `agent-task-recipes-recipe-trace-a-public-gift-end-to-end`: Recipe: Trace a public gift end to end
- `agent-task-recipes-recipe-validate-an-online-giving-page-before-launch`: Recipe: Validate an online giving page before launch
- `agent-task-recipes-recipe-generate-and-validate-contribution-statements`: Recipe: Generate and validate contribution statements
- `agent-task-recipes-recipe-build-a-detail-preserving-finance-report`: Recipe: Build a detail-preserving finance report
- `agent-task-recipes-recipe-transfer-scheduled-giving-to-a-new-gateway`: Recipe: Transfer scheduled giving to a new gateway
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

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
