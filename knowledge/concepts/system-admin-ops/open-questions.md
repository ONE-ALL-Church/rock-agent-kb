---
concept_id: system-admin-ops
title: System Administration And Operations Open Questions
generated: true
---

# System Administration And Operations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `5-core-configuration-and-data-model-security-rules`: Security Rules
- `6-primary-entities-and-relationships-page-block-and-security-relationships`: Page, Block, And Security Relationships
- `8-jobs-and-scheduling-deep-dive-launch-workflow-job`: Launch Workflow Job
- `11-cleanup-and-data-integrity-deep-dive-security-data-integrity`: Security Data Integrity
- `11-cleanup-and-data-integrity-deep-dive-integration-and-recipe-integrity`: Integration And Recipe Integrity
- `13-administration-and-operational-guardrails-validate-community-recipes`: Validate Community Recipes
- `17-implementation-playbooks-playbook-review-security-integrity`: Playbook: Review Security Integrity

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-system-administration-and-operations-mental-model-layer-1-configuration`: Layer 1: Configuration
- `3-system-administration-and-operations-mental-model-layer-4-security-and-authorization`: Layer 4: Security And Authorization
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-entities-properties-and-attributes`: Entities, Properties, And Attributes
- `5-core-configuration-and-data-model-defined-types-and-defined-values`: Defined Types And Defined Values
- `5-core-configuration-and-data-model-service-jobs`: Service Jobs
- `5-core-configuration-and-data-model-cache`: Cache
- `6-primary-entities-and-relationships-servicejob-and-servicejobhistory`: ServiceJob And ServiceJobHistory
- `6-primary-entities-and-relationships-servicejobhistory-fields-to-inspect`: ServiceJobHistory Fields To Inspect
- `6-primary-entities-and-relationships-dataview-and-persisted-data-view-state`: DataView And Persisted Data View State
- `6-primary-entities-and-relationships-exceptionlog`: ExceptionLog
- `6-primary-entities-and-relationships-page-block-and-security-relationships`: Page, Block, And Security Relationships
- `7-common-system-administration-and-operations-workflows-workflow-investigate-a-failed-service-job`: Workflow: Investigate A Failed Service Job
- `7-common-system-administration-and-operations-workflows-workflow-confirm-whether-a-job-actually-ran`: Workflow: Confirm Whether A Job Actually Ran
- `7-common-system-administration-and-operations-workflows-workflow-investigate-a-warning-job`: Workflow: Investigate A Warning Job
- `7-common-system-administration-and-operations-workflows-workflow-investigate-stale-search-results`: Workflow: Investigate Stale Search Results
- `7-common-system-administration-and-operations-workflows-workflow-investigate-stale-persisted-data-view-results`: Workflow: Investigate Stale Persisted Data View Results
- `7-common-system-administration-and-operations-workflows-workflow-investigate-a-cache-suspect`: Workflow: Investigate A Cache Suspect
- `7-common-system-administration-and-operations-workflows-workflow-investigate-an-exception-spike`: Workflow: Investigate An Exception Spike
- `7-common-system-administration-and-operations-workflows-workflow-review-operational-health-after-upgrade`: Workflow: Review Operational Health After Upgrade
- `8-jobs-and-scheduling-deep-dive-job-configuration-fields-to-inspect`: Job Configuration Fields To Inspect
- `8-jobs-and-scheduling-deep-dive-job-history-interpretation`: Job History Interpretation
- `8-jobs-and-scheduling-deep-dive-job-history-ui-behavior`: Job History UI Behavior
- `8-jobs-and-scheduling-deep-dive-job-history-security`: Job History Security
- `8-jobs-and-scheduling-deep-dive-job-retention`: Job Retention
- `8-jobs-and-scheduling-deep-dive-update-persisted-dataviews-job`: Update Persisted DataViews Job
- `8-jobs-and-scheduling-deep-dive-launch-workflow-job`: Launch Workflow Job
- `9-diagnostics-and-exceptions-deep-dive-diagnostic-mindset`: Diagnostic Mindset
- `exception-investigation-branches-request-time-exception`: Request-Time Exception
- `exception-investigation-branches-job-time-exception`: Job-Time Exception
- `exception-investigation-branches-dataview-exception`: DataView Exception
- `exception-investigation-branches-search-exception`: Search Exception
- `exception-investigation-branches-cache-exception`: Cache Exception
- `10-cache-and-indexing-deep-dive-cache-keys`: Cache Keys
- `10-cache-and-indexing-deep-dive-cache-tags`: Cache Tags
- `10-cache-and-indexing-deep-dive-cache-clearing`: Cache Clearing
- `10-cache-and-indexing-deep-dive-entity-indexing`: Entity Indexing

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
