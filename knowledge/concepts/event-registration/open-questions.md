---
concept_id: event-registration
title: Event Registration Open Questions
generated: true
---

# Event Registration Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `family-preregistration-and-follow-up`: Family Preregistration And Follow-Up
- `agent-task-recipes-recipe-audit-an-event-registration-dashboard`: Recipe: Audit an event-registration dashboard
- `source-map-approved-community-guidance-and-examples`: Approved community guidance and examples

## Needs Live Verification

- `agent-summary`: Agent Summary
- `registration-instances-put-occurrence-specific-settings-on-the-instance`: Put occurrence-specific settings on the instance
- `forms-identity-eligibility-and-communications-test-combined-eligibility`: Test combined eligibility
- `forms-identity-eligibility-and-communications-verify-communications-as-part-of-the-lifecycle`: Verify communications as part of the lifecycle
- `payments-configure-the-finance-path-deliberately`: Configure the finance path deliberately
- `payments-match-externally-entered-transactions`: Match externally entered transactions
- `event-calendar-link-the-occurrence-registration-and-group`: Link the occurrence, registration, and group
- `family-preregistration-and-follow-up`: Family Preregistration And Follow-Up
- `reporting-and-reconciliation`: Reporting And Reconciliation
- `permissions-and-operational-control`: Permissions And Operational Control
- `troubleshooting-decision-tree-the-public-event-has-no-register-button`: The public event has no Register button
- `troubleshooting-decision-tree-a-representative-person-is-unexpectedly-ineligible`: A representative person is unexpectedly ineligible
- `troubleshooting-decision-tree-a-duplicate-registration-warning-exposes-sensitive-participation`: A duplicate-registration warning exposes sensitive participation
- `troubleshooting-decision-tree-a-person-moved-from-the-wait-list-is-missing-payment-or-form-data`: A person moved from the wait list is missing payment or form data
- `troubleshooting-decision-tree-a-registration-balance-no-longer-matches-its-payment-plan`: A registration balance no longer matches its payment plan
- `troubleshooting-decision-tree-a-batch-transaction-is-not-attached-to-the-registration`: A batch transaction is not attached to the registration
- `troubleshooting-decision-tree-registrants-are-not-entering-the-expected-group`: Registrants are not entering the expected group
- `troubleshooting-decision-tree-dashboard-totals-disagree`: Dashboard totals disagree
- `troubleshooting-decision-tree-a-signature-document-is-missing-or-belongs-to-the-wrong-registration`: A signature document is missing or belongs to the wrong registration
- `agent-task-recipes-recipe-create-a-reusable-registration-and-one-event-instance`: Recipe: Create a reusable registration and one event instance
- `agent-task-recipes-recipe-validate-a-paid-registration-before-launch`: Recipe: Validate a paid registration before launch
- `agent-task-recipes-recipe-promote-a-wait-listed-person-to-full-registration`: Recipe: Promote a wait-listed person to full registration
- `agent-task-recipes-recipe-audit-an-event-registration-dashboard`: Recipe: Audit an event-registration dashboard
- `agent-task-recipes-recipe-launch-family-preregistration-with-follow-up`: Recipe: Launch family preregistration with follow-up
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
