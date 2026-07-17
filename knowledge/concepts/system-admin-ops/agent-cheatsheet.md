---
concept_id: system-admin-ops
title: System Administration And Operations Agent Cheatsheet
generated: true
---

# System Administration And Operations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Answer “Is The System Healthy?”](tasks/recipe-answer-is-the-system-healthy.md) |  |  |
| [Recipe: Answer “Why Is This Data Wrong?”](tasks/recipe-answer-why-is-this-data-wrong.md) |  |  |
| [Recipe: Answer “Can I Clear Cache?”](tasks/recipe-answer-can-i-clear-cache.md) |  |  |
| [Recipe: Answer “Why Did This Workflow Not Start?”](tasks/recipe-answer-why-did-this-workflow-not-start.md) |  |  |
| [Recipe: Answer “Why Is This Data View Slow?”](tasks/recipe-answer-why-is-this-data-view-slow.md) |  |  |
| [Recipe: Answer “What Changed In This Version That Matters Operationally?”](tasks/recipe-answer-what-changed-in-this-version-that-matters-operationally.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get r |
| `19.1` | core | Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | citation-only | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-system-administration-and-operations-mental-model-layer-1-configuration` | normal | live verification |
| `3-system-administration-and-operations-mental-model-layer-4-security-and-authorization` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-entities-properties-and-attributes` | citation-only | live verification |
| `5-core-configuration-and-data-model-defined-types-and-defined-values` | normal | live verification |
| `5-core-configuration-and-data-model-service-jobs` | high | live verification |
| `5-core-configuration-and-data-model-cache` | normal | live verification |
| `5-core-configuration-and-data-model-security-rules` | community-supported | community-supported |
| `6-primary-entities-and-relationships-servicejob-and-servicejobhistory` | normal | live verification |
| `6-primary-entities-and-relationships-servicejobhistory-fields-to-inspect` | normal | live verification |
| `6-primary-entities-and-relationships-dataview-and-persisted-data-view-state` | normal | live verification |
| `6-primary-entities-and-relationships-exceptionlog` | high | live verification |
| `6-primary-entities-and-relationships-page-block-and-security-relationships` | community-supported | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-investigate-a-failed-service-job` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-confirm-whether-a-job-actually-ran` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-investigate-a-warning-job` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-investigate-stale-search-results` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-investigate-stale-persisted-data-view-results` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-investigate-a-cache-suspect` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-investigate-an-exception-spike` | normal | live verification |
| `7-common-system-administration-and-operations-workflows-workflow-review-operational-health-after-upgrade` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-job-configuration-fields-to-inspect` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-job-history-interpretation` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-job-history-ui-behavior` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-job-history-security` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-job-retention` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-update-persisted-dataviews-job` | normal | live verification |
| `8-jobs-and-scheduling-deep-dive-launch-workflow-job` | community-supported | live verification |
| `9-diagnostics-and-exceptions-deep-dive-diagnostic-mindset` | structural | live verification |
| `exception-investigation-branches-request-time-exception` | normal | live verification |
| `exception-investigation-branches-job-time-exception` | normal | live verification |
| `exception-investigation-branches-dataview-exception` | normal | live verification |
| `exception-investigation-branches-search-exception` | normal | live verification |
| `exception-investigation-branches-cache-exception` | normal | live verification |
| `10-cache-and-indexing-deep-dive-cache-keys` | normal | live verification |
| `10-cache-and-indexing-deep-dive-cache-tags` | citation-only | live verification |
| `10-cache-and-indexing-deep-dive-cache-clearing` | normal | live verification |
| `10-cache-and-indexing-deep-dive-entity-indexing` | normal | live verification |
| `11-cleanup-and-data-integrity-deep-dive-cleanup-as-operational-risk-management` | citation-only | live verification |
| `11-cleanup-and-data-integrity-deep-dive-service-job-history-cleanup` | normal | live verification |
| `11-cleanup-and-data-integrity-deep-dive-rock-cleanup-and-cache-folder-caveat` | normal | live verification |
| `11-cleanup-and-data-integrity-deep-dive-attribute-data-integrity` | normal | live verification |
| `11-cleanup-and-data-integrity-deep-dive-security-data-integrity` | community-supported | community-supported |
| `11-cleanup-and-data-integrity-deep-dive-data-view-integrity` | normal | live verification |
| `11-cleanup-and-data-integrity-deep-dive-integration-and-recipe-integrity` | community-supported | community-supported |
| `12-related-rock-areas-security-workflows-data-views-reports-cache-jobs-release-notes-security` | high | live verification |
| `12-related-rock-areas-security-workflows-data-views-reports-cache-jobs-release-notes-reports` | structural | live verification |
| `12-related-rock-areas-security-workflows-data-views-reports-cache-jobs-release-notes-release-notes` | normal | live verification |
| `13-administration-and-operational-guardrails-treat-lava-apis-as-high-risk` | normal | live verification |
| `13-administration-and-operational-guardrails-validate-community-recipes` | community-supported | live verification |
| `13-administration-and-operational-guardrails-prefer-entity-ids-and-guids-over-names` | structural | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-cache-and-lava-apis` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-helix` | normal | live verification |
| `15-reporting-analytics-and-model-map-model-map` | citation-only | live verification |
| `16-version-and-release-caveats-rock-v19-1-attribute-category-caveat` | normal | live verification |
| `17-implementation-playbooks-playbook-validate-universal-search` | normal | live verification |
| `17-implementation-playbooks-playbook-validate-persisted-data-views` | normal | live verification |
| `17-implementation-playbooks-playbook-review-lava-cache-safety` | normal | live verification |
| `17-implementation-playbooks-playbook-review-lava-webhooks` | normal | live verification |
| `17-implementation-playbooks-playbook-review-security-integrity` | community-supported | live verification |
| `19-agent-task-recipes-recipe-answer-why-did-this-workflow-not-start` | structural | live verification |
| `19-agent-task-recipes-recipe-answer-why-is-this-data-view-slow` | structural | live verification |
| `19-agent-task-recipes-recipe-answer-what-changed-in-this-version-that-matters-operationally` | normal | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `20-source-map-and-dependency-notes` | high | live verification |
