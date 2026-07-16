---
concept_id: connections
title: Connections Open Questions
generated: true
---

# Connections Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `6-primary-entities-and-relationships-connectionopportunity`: ConnectionOpportunity
- `11-assignment-and-follow-up-deep-dive-connector-availability-and-workload`: Connector Availability And Workload
- `14-developer-api-lava-and-source-code-landmarks-lava`: Lava
- `19-agent-task-recipes-recipe-investigate-connector-workload`: Recipe: Investigate Connector Workload
- `20-source-map-and-dependency-notes-community-examples`: Community Examples

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-connections-mental-model`: 3. Connections Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-connection-type-configuration`: Connection Type Configuration
- `5-core-configuration-and-data-model-connection-status-configuration`: Connection Status Configuration
- `5-core-configuration-and-data-model-connection-opportunity-configuration`: Connection Opportunity Configuration
- `5-core-configuration-and-data-model-connection-request-data`: Connection Request Data
- `6-primary-entities-and-relationships-entity-relationship-map`: Entity Relationship Map
- `7-common-connections-workflows-staff-creates-a-request`: Staff Creates A Request
- `7-common-connections-workflows-person-self-service-signup`: Person Self-Service Signup
- `8-opportunities-deep-dive-key-opportunity-settings-to-inspect`: Key Opportunity Settings To Inspect
- `8-opportunities-deep-dive-opportunity-workflow-configuration`: Opportunity Workflow Configuration
- `9-requests-and-statuses-deep-dive-status-vs-state`: Status Vs State
- `9-requests-and-statuses-deep-dive-due-dates-and-due-soon-behavior`: Due Dates And Due-Soon Behavior
- `9-requests-and-statuses-deep-dive-future-follow-up`: Future Follow-Up
- `9-requests-and-statuses-deep-dive-status-automation`: Status Automation
- `10-boards-and-lists-deep-dive-list-view`: List View
- `10-boards-and-lists-deep-dive-grid-and-snapshot-views`: Grid And Snapshot Views
- `11-assignment-and-follow-up-deep-dive-connector-assignment`: Connector Assignment
- `12-related-rock-areas-people-workflows-groups-communications-security-reporting-people`: People
- `12-related-rock-areas-people-workflows-groups-communications-security-reporting-workflows`: Workflows
- `12-related-rock-areas-people-workflows-groups-communications-security-reporting-security`: Security
- `13-administration-and-operational-guardrails-configuration-review-checklist`: Configuration Review Checklist
- `14-developer-api-lava-and-source-code-landmarks-query-page-parameter-landmarks`: Query/Page Parameter Landmarks
- `16-version-and-release-caveats-rock-v10`: Rock v10
- `16-version-and-release-caveats-rock-v12`: Rock v12
- `16-version-and-release-caveats-rock-v19-1-current-release-notes`: Rock v19.1 / Current Release Notes
- `17-implementation-playbooks-playbook-create-a-new-serving-pipeline`: Playbook: Create A New Serving Pipeline
- `17-implementation-playbooks-playbook-add-status-automation`: Playbook: Add Status Automation
- `18-troubleshooting-decision-tree-status-change-did-something-unexpected`: Status Change Did Something Unexpected
- `18-troubleshooting-decision-tree-signup-missing-attributes`: Signup Missing Attributes
- `18-troubleshooting-decision-tree-list-sorting-looks-wrong`: List Sorting Looks Wrong
- `19-agent-task-recipes-recipe-build-opportunity-cards`: Recipe: Build Opportunity Cards
- `approved-claim-coverage`: Approved Claim Coverage
- `20-source-map-and-dependency-notes-live-verification-required`: Live Verification Required

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
