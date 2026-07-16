---
concept_id: connections
title: Connections Agent Cheatsheet
generated: true
---

# Connections Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Audit One Connection Type](tasks/recipe-audit-one-connection-type.md) |  |  |
| [Recipe: Explain Why A Request Is Hidden](tasks/recipe-explain-why-a-request-is-hidden.md) |  |  |
| [Recipe: Validate Signup Flow](tasks/recipe-validate-signup-flow.md) |  |  |
| [Recipe: Build Opportunity Cards](tasks/recipe-build-opportunity-cards.md) |  |  |
| [Recipe: Investigate Connector Workload](tasks/recipe-investigate-connector-workload.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Improved the Connection Request Board with updates to campus filtering, connector preferences, and workflow configuration. Added new block settings to define default Connection State and Status filters. Workflows on the Connection Opportuni |
| `17.2` | core | Fixed an issue where the Connection Opportunity Signup block only displayed request attributes defined on the opportunity itself, now correctly including attributes inherited from the Connection Type. Fixes: #6356 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-connections-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-connection-type-configuration` | high | live verification |
| `5-core-configuration-and-data-model-connection-status-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-connection-opportunity-configuration` | high | live verification |
| `5-core-configuration-and-data-model-connection-request-data` | normal | live verification |
| `6-primary-entities-and-relationships-entity-relationship-map` | normal | live verification |
| `6-primary-entities-and-relationships-connectionopportunity` | community-supported | community-supported |
| `7-common-connections-workflows-staff-creates-a-request` | normal | live verification |
| `7-common-connections-workflows-person-self-service-signup` | normal | live verification |
| `8-opportunities-deep-dive-key-opportunity-settings-to-inspect` | normal | live verification |
| `8-opportunities-deep-dive-opportunity-workflow-configuration` | normal | live verification |
| `9-requests-and-statuses-deep-dive-status-vs-state` | normal | live verification |
| `9-requests-and-statuses-deep-dive-due-dates-and-due-soon-behavior` | normal | live verification |
| `9-requests-and-statuses-deep-dive-future-follow-up` | high | live verification |
| `9-requests-and-statuses-deep-dive-status-automation` | normal | live verification |
| `10-boards-and-lists-deep-dive-list-view` | high | live verification |
| `10-boards-and-lists-deep-dive-grid-and-snapshot-views` | normal | live verification |
| `11-assignment-and-follow-up-deep-dive-connector-assignment` | normal | live verification |
| `11-assignment-and-follow-up-deep-dive-connector-availability-and-workload` | community-supported | community-supported |
| `12-related-rock-areas-people-workflows-groups-communications-security-reporting-people` | normal | live verification |
| `12-related-rock-areas-people-workflows-groups-communications-security-reporting-workflows` | normal | live verification |
| `12-related-rock-areas-people-workflows-groups-communications-security-reporting-security` | normal | live verification |
| `13-administration-and-operational-guardrails-configuration-review-checklist` | citation-only | live verification |
| `14-developer-api-lava-and-source-code-landmarks-query-page-parameter-landmarks` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava` | community-supported | community-supported |
| `16-version-and-release-caveats-rock-v10` | normal | live verification |
| `16-version-and-release-caveats-rock-v12` | normal | live verification |
| `16-version-and-release-caveats-rock-v19-1-current-release-notes` | normal | live verification |
| `17-implementation-playbooks-playbook-create-a-new-serving-pipeline` | normal | live verification |
| `17-implementation-playbooks-playbook-add-status-automation` | normal | live verification |
| `18-troubleshooting-decision-tree-status-change-did-something-unexpected` | normal | live verification |
| `18-troubleshooting-decision-tree-signup-missing-attributes` | normal | live verification |
| `18-troubleshooting-decision-tree-list-sorting-looks-wrong` | normal | live verification |
| `19-agent-task-recipes-recipe-build-opportunity-cards` | normal | live verification |
| `19-agent-task-recipes-recipe-investigate-connector-workload` | community-supported | community-supported |
| `approved-claim-coverage` | citation-only | live verification |
| `20-source-map-and-dependency-notes-community-examples` | community-supported | community-supported |
| `20-source-map-and-dependency-notes-live-verification-required` | structural | live verification |
