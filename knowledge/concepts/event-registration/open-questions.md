---
concept_id: event-registration
title: Event Registration Open Questions
generated: true
---

# Event Registration Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `5-core-configuration-and-data-model-data-model-orientation`: Data Model Orientation
- `6-primary-entities-and-relationships-registration-template`: Registration Template
- `8-registration-instances-deep-dive-capacity-and-spots`: Capacity And Spots
- `10-related-rock-areas-events-finance-workflows-communications-groups-finance`: Finance
- `10-related-rock-areas-events-finance-workflows-communications-groups-workflows`: Workflows
- `11-administration-and-operational-guardrails-naming`: Naming
- `11-administration-and-operational-guardrails-notes-and-auditability`: Notes And Auditability
- `12-developer-api-lava-and-source-code-landmarks-api-linkage-caveat`: API Linkage Caveat
- `13-reporting-analytics-and-model-map-reporting-entity-choice`: Reporting Entity Choice
- `13-reporting-analytics-and-model-map-model-map-verification`: Model Map Verification
- `13-reporting-analytics-and-model-map-analytics-checks`: Analytics Checks
- `17-agent-task-recipes-recipe-build-a-registrant-packet-export`: Recipe: Build A Registrant Packet Export
- `17-agent-task-recipes-recipe-add-staff-notes-to-registration-detail`: Recipe: Add Staff Notes To Registration Detail
- `17-agent-task-recipes-recipe-investigate-api-registration-url-issues`: Recipe: Investigate API Registration URL Issues

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-event-registration-mental-model`: 3. Event Registration Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-configuration-surfaces`: Configuration Surfaces
- `5-core-configuration-and-data-model-data-model-orientation`: Data Model Orientation
- `6-primary-entities-and-relationships-registration`: Registration
- `6-primary-entities-and-relationships-registrationregistrant`: RegistrationRegistrant
- `6-primary-entities-and-relationships-event-item-occurrence-and-linkage`: Event Item Occurrence And Linkage
- `6-primary-entities-and-relationships-attributes-and-form-fields`: Attributes And Form Fields
- `7-common-event-registration-workflows-paid-registration`: Paid Registration
- `7-common-event-registration-workflows-wait-list-registration`: Wait List Registration
- `7-common-event-registration-workflows-group-placement`: Group Placement
- `8-registration-instances-deep-dive-instance-identity`: Instance Identity
- `8-registration-instances-deep-dive-active-and-date-windows`: Active And Date Windows
- `8-registration-instances-deep-dive-url-slug-and-public-linkage`: URL Slug And Public Linkage
- `8-registration-instances-deep-dive-attributes`: Attributes
- `9-payments-deep-dive-partial-payments`: Partial Payments
- `9-payments-deep-dive-payment-plans`: Payment Plans
- `9-payments-deep-dive-payment-gateways-and-saved-accounts`: Payment Gateways And Saved Accounts
- `11-administration-and-operational-guardrails-naming`: Naming
- `11-administration-and-operational-guardrails-change-management`: Change Management
- `11-administration-and-operational-guardrails-operational-health-checks`: Operational Health Checks
- `12-developer-api-lava-and-source-code-landmarks-public-mobile-event-occurrence-rendering`: Public/Mobile Event Occurrence Rendering
- `12-developer-api-lava-and-source-code-landmarks-api-linkage-caveat`: API Linkage Caveat
- `13-reporting-analytics-and-model-map-model-map-verification`: Model Map Verification
- `14-version-and-release-caveats-rock-18-3`: Rock 18.3
- `14-version-and-release-caveats-v16-10-v17-0-spotlight`: v16.10 / v17.0 Spotlight
- `15-implementation-playbooks-playbook-a-create-a-standard-paid-event-registration`: Playbook A: Create A Standard Paid Event Registration
- `15-implementation-playbooks-playbook-b-add-eligibility-rules-in-v19-1`: Playbook B: Add Eligibility Rules In v19.1+
- `15-implementation-playbooks-playbook-c-prevent-duplicate-registrants-in-v19-1`: Playbook C: Prevent Duplicate Registrants In v19.1+
- `15-implementation-playbooks-playbook-d-configure-payment-reminders`: Playbook D: Configure Payment Reminders
- `15-implementation-playbooks-playbook-e-diagnose-a-missing-public-registration-button`: Playbook E: Diagnose A Missing Public Registration Button
- `16-troubleshooting-decision-tree-public-page-says-registration-is-closed`: Public page says registration is closed
- `17-agent-task-recipes-recipe-verify-a-public-registration-url`: Recipe: Verify A Public Registration URL
- `17-agent-task-recipes-recipe-audit-payment-risk`: Recipe: Audit Payment Risk
- `17-agent-task-recipes-recipe-audit-discount-codes`: Recipe: Audit Discount Codes
- `17-agent-task-recipes-recipe-audit-wait-list`: Recipe: Audit Wait List
- `17-agent-task-recipes-recipe-add-staff-notes-to-registration-detail`: Recipe: Add Staff Notes To Registration Detail

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
