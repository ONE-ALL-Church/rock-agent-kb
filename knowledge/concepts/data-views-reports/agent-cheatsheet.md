---
concept_id: data-views-reports
title: Data Views And Reports Agent Cheatsheet
generated: true
---

# Data Views And Reports Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Answer "What Does This Report Actually Show?"](tasks/recipe-answer-what-does-this-report-actually-show.md) |  |  |
| [Recipe: Answer "Can I Change This Data View?"](tasks/recipe-answer-can-i-change-this-data-view.md) |  |  |
| [Recipe: Build "People Who Attended X But Not Y"](tasks/recipe-build-people-who-attended-x-but-not-y.md) |  |  |
| [Recipe: Build "Lapsed Givers"](tasks/recipe-build-lapsed-givers.md) |  |  |
| [Recipe: Build "Where Are Our Reporting Tools?"](tasks/recipe-build-where-are-our-reporting-tools.md) |  |  |
| [Recipe: Validate A BI Finance Dashboard](tasks/recipe-validate-a-bi-finance-dashboard.md) |  |  |
| [Recipe: Audit Reporting Security](tasks/recipe-audit-reporting-security.md) |  |  |
| [Recipe: Diagnose Slow Reporting](tasks/recipe-diagnose-slow-reporting.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `AttendanceOccurrence` | `Attendance`, `Group`, `Schedule`, `Location`, `Campus` | Use this for reporting context. Check group, location, schedule, and SundayDate before blaming the UI. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `2-scope-and-terminology-core-terms` | high | live verification |
| `3-data-views-and-reports-mental-model-record-set-vs-presentation` | community-supported | community-supported |
| `3-data-views-and-reports-mental-model-data-view-composition` | normal | live verification |
| `3-data-views-and-reports-mental-model-related-data-view-semantics` | normal | live verification |
| `3-data-views-and-reports-mental-model-data-view-caching-and-persisted-values` | high | live verification |
| `3-data-views-and-reports-mental-model-reports-are-not-security-boundaries-by-themselves` | community-supported | live verification |
| `4-source-authority-and-how-to-use-this-guide` | community-supported | community-supported |
| `4-source-authority-and-how-to-use-this-guide-how-agents-should-use-this-guide` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide-citation-policy` | structural | live verification |
| `5-core-configuration-and-data-model-data-view-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-data-view-filter-data-model` | normal | live verification |
| `5-core-configuration-and-data-model-dynamic-report-block-configuration` | community-supported | live verification |
| `5-core-configuration-and-data-model-lava-sql-configuration` | normal | live verification |
| `6-primary-entities-and-relationships-dataview` | normal | live verification |
| `6-primary-entities-and-relationships-dataviewfilter` | normal | live verification |
| `6-primary-entities-and-relationships-report` | structural | live verification |
| `6-primary-entities-and-relationships-reportfield` | community-supported | live verification |
| `6-primary-entities-and-relationships-category` | normal | live verification |
| `6-primary-entities-and-relationships-block-and-page` | community-supported | live verification |
| `6-primary-entities-and-relationships-attribute-and-attributevalue` | structural | live verification |
| `6-primary-entities-and-relationships-person-and-alias` | normal | live verification |
| `6-primary-entities-and-relationships-attendance` | normal | live verification |
| `6-primary-entities-and-relationships-finance` | community-supported | community-supported |
| `6-primary-entities-and-relationships-analytics-models` | citation-only | live verification |
| `7-common-data-views-and-reports-workflows-workflow-1-build-a-staff-list-report` | citation-only | live verification |
| `7-common-data-views-and-reports-workflows-workflow-2-build-a-ministry-dashboard` | community-supported | live verification |
| `7-common-data-views-and-reports-workflows-workflow-3-build-a-data-view-finder` | community-supported | live verification |
| `7-common-data-views-and-reports-workflows-workflow-4-build-a-report-finder` | community-supported | community-supported |
| `7-common-data-views-and-reports-workflows-workflow-5-convert-a-one-off-sql-request-into-a-governed-report` | community-supported | community-supported |
| `7-common-data-views-and-reports-workflows-workflow-6-build-a-bi-report` | citation-only | live verification |
| `8-data-views-deep-dive-filter-tree-design` | structural | live verification |
| `8-data-views-deep-dive-security` | citation-only | live verification |
| `8-data-views-deep-dive-related-data-views` | normal | live verification |
| `8-data-views-deep-dive-post-filter-transformations` | normal | live verification |
| `8-data-views-deep-dive-data-view-usage-before-editing` | normal | live verification |
| `8-data-views-deep-dive-testing-data-views` | normal | live verification |
| `8-data-views-deep-dive-common-data-view-anti-patterns` | normal | live verification |
| `9-reports-deep-dive-report-field-design` | community-supported | community-supported |
| `9-reports-deep-dive-dynamic-report-runtime-filters` | citation-only | live verification |
| `9-reports-deep-dive-reports-as-page-contracts` | community-supported | live verification |
| `9-reports-deep-dive-report-security` | structural | live verification |
| `9-reports-deep-dive-report-inventory-and-governance` | community-supported | community-supported |
| `10-business-intelligence-deep-dive-bi-model-layer` | community-supported | community-supported |
| `10-business-intelligence-deep-dive-bi-job` | citation-only | live verification |
| `10-business-intelligence-deep-dive-power-bi-template` | citation-only | live verification |
| `10-business-intelligence-deep-dive-embedded-reports` | citation-only | live verification |
| `10-business-intelligence-deep-dive-bi-finance-reports` | community-supported | community-supported |
| `10-business-intelligence-deep-dive-bi-family-reports` | community-supported | community-supported |
| `11-related-rock-areas-sql-model-map-lava-finance-attendance-sql` | normal | live verification |
| `11-related-rock-areas-sql-model-map-lava-finance-attendance-model-map` | community-supported | live verification |
| `11-related-rock-areas-sql-model-map-lava-finance-attendance-finance` | community-supported | community-supported |
| `11-related-rock-areas-sql-model-map-lava-finance-attendance-attendance` | normal | live verification |
| `12-administration-and-operational-guardrails-reporting-governance` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-performance-guardrails` | citation-only | live verification |
| `12-administration-and-operational-guardrails-database-maintenance` | community-supported | live verification |
| `12-administration-and-operational-guardrails-change-control` | structural | live verification |
| `13-developer-api-lava-and-source-code-landmarks-data-filter-components` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-obsidian-filter-bags` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-tests-as-operational-models` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-api-and-entity-commands` | normal | live verification |
| `14-reporting-analytics-and-model-map-analytics-tables-vs-transactional-tables` | community-supported | community-supported |
| `14-reporting-analytics-and-model-map-metrics-and-measurement-classifications` | normal | live verification |
| `14-reporting-analytics-and-model-map-model-discovery-process` | community-supported | live verification |
| `15-version-and-release-caveats-rock-version-matters` | normal | live verification |
| `15-version-and-release-caveats-dynamic-report-filtering` | citation-only | live verification |
| `15-version-and-release-caveats-lava-sql-parameters-and-timeout` | normal | live verification |
| `15-version-and-release-caveats-data-view-caching` | high | live verification |
| `15-version-and-release-caveats-bi-template-version` | citation-only | live verification |
| `15-version-and-release-caveats-analytics-source-giving-unit` | citation-only | live verification |
| `15-version-and-release-caveats-source-code-branch-caveat` | structural | live verification |
| `16-implementation-playbooks-playbook-a-create-a-new-data-view-and-report` | citation-only | live verification |
| `16-implementation-playbooks-playbook-b-fix-a-data-view-returning-too-many-rows` | structural | live verification |
| `16-implementation-playbooks-playbook-d-build-a-finance-giving-report` | community-supported | community-supported |
| `16-implementation-playbooks-playbook-f-build-a-reporting-inventory-dashboard` | community-supported | community-supported |
| `16-implementation-playbooks-playbook-g-retire-a-report-or-data-view` | normal | live verification |
| `18-agent-task-recipes-recipe-answer-what-does-this-report-actually-show` | structural | live verification |
| `18-agent-task-recipes-recipe-answer-can-i-change-this-data-view` | structural | live verification |
| `18-agent-task-recipes-recipe-build-people-who-attended-x-but-not-y` | structural | live verification |
| `18-agent-task-recipes-recipe-build-lapsed-givers` | community-supported | community-supported |
| `18-agent-task-recipes-recipe-build-where-are-our-reporting-tools` | community-supported | community-supported |
| `18-agent-task-recipes-recipe-audit-reporting-security` | structural | live verification |
| `18-agent-task-recipes-recipe-diagnose-slow-reporting` | structural | live verification |
| `approved-claim-coverage` | normal | live verification |
| `19-source-map-and-dependency-notes-official-and-training-sources` | normal | live verification |
| `19-source-map-and-dependency-notes-source-code-landmarks` | normal | live verification |
| `19-source-map-and-dependency-notes-community-and-partner-pattern-sources` | normal | live verification |
