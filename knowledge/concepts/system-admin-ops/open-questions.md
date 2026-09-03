---
concept_id: system-admin-ops
title: System Administration And Operations Open Questions
generated: true
---

# System Administration And Operations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (193 words)
- `mental-model`: Mental Model (194 words)
- `known-gaps-and-live-verification`: Known Gaps And Live Verification (233 words)

## Community-Supported Only


## Needs Live Verification

- `scope-and-boundaries`: Scope And Boundaries
- `mental-model`: Mental Model
- `jobs-and-scheduling-job-configuration-and-history`: Job configuration and history
- `jobs-and-scheduling-version-specific-job-history-failures`: Version-specific job-history failures
- `jobs-and-scheduling-job-backed-operational-processes`: Job-backed operational processes
- `diagnostics-and-exceptions-exception-history`: Exception history
- `cache-and-persisted-data-cache-manager-and-cache-tags`: Cache Manager and cache tags
- `cleanup-and-data-integrity-photo-verification`: Photo verification
- `troubleshooting-decision-tree-a-scheduled-job-stopped-producing-new-history`: A scheduled job stopped producing new history
- `troubleshooting-decision-tree-a-page-is-slow`: A page is slow
- `troubleshooting-decision-tree-updated-content-remains-stale`: Updated content remains stale
- `troubleshooting-decision-tree-exceptions-repeat-after-a-page-or-block-change`: Exceptions repeat after a page or block change
- `troubleshooting-decision-tree-universal-search-cannot-connect-after-an-environment-refresh`: Universal Search cannot connect after an environment refresh
- `troubleshooting-decision-tree-an-entity-type-returns-no-universal-search-results`: An entity type returns no Universal Search results
- `troubleshooting-decision-tree-universal-search-works-directly-but-not-through-smart-search`: Universal Search works directly but not through Smart Search
- `troubleshooting-decision-tree-an-address-is-missing-coordinates`: An address is missing coordinates
- `troubleshooting-decision-tree-data-automation-changed-more-records-than-expected`: Data Automation changed more records than expected
- `agent-task-recipes-recipe-triage-a-recurring-exception`: Recipe: Triage a recurring exception
- `agent-task-recipes-recipe-refresh-stale-cached-output-with-minimum-scope`: Recipe: Refresh stale cached output with minimum scope
- `agent-task-recipes-recipe-create-and-assign-a-cache-tag`: Recipe: Create and assign a cache tag
- `agent-task-recipes-recipe-audit-a-scheduled-job-s-recent-health`: Recipe: Audit a scheduled job’s recent health
- `agent-task-recipes-recipe-restore-a-missing-universal-search-entity`: Recipe: Restore a missing Universal Search entity
- `agent-task-recipes-recipe-configure-a-bounded-site-index-crawl`: Recipe: Configure a bounded site-index crawl
- `agent-task-recipes-recipe-review-and-resolve-a-duplicate-person-candidate`: Recipe: Review and resolve a duplicate-person candidate
- `agent-task-recipes-recipe-review-a-data-automation-change-before-execution`: Recipe: Review a Data Automation change before execution

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
