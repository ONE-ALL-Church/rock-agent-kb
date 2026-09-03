---
concept_id: data-views-reports
title: Data Views And Reports Open Questions
generated: true
---

# Data Views And Reports Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `known-gaps-and-live-verification`: Known Gaps And Live Verification (189 words)

## Community-Supported Only

- `domain-reporting-workflows-communication-audiences-and-delivery-health`: Communication audiences and delivery health
- `source-map-community-reviewed-patterns`: Community-reviewed patterns

## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `data-views`: Data Views
- `report-security`: Report Security
- `dynamic-reports-and-custom-reporting-blocks`: Dynamic Reports And Custom Reporting Blocks
- `business-intelligence`: Business Intelligence
- `sql-reporting-patterns`: SQL Reporting Patterns
- `data-integrity-and-reporting-quality`: Data Integrity And Reporting Quality
- `domain-reporting-workflows-communication-audiences-and-delivery-health`: Communication audiences and delivery health
- `domain-reporting-workflows-schedule-dates-and-operational-snapshots`: Schedule dates and operational snapshots
- `troubleshooting-decision-tree-a-data-view-returns-the-wrong-records`: A Data View returns the wrong records
- `troubleshooting-decision-tree-a-report-is-slow`: A Report is slow
- `troubleshooting-decision-tree-a-report-exposes-unexpected-sensitive-data`: A Report exposes unexpected sensitive data
- `troubleshooting-decision-tree-a-dynamic-report-filter-does-not-behave-as-expected`: A Dynamic Report filter does not behave as expected
- `troubleshooting-decision-tree-a-lava-entity-query-ignores-its-filters`: A Lava Entity query ignores its filters
- `troubleshooting-decision-tree-a-bi-report-is-empty-or-missing-a-domain`: A BI report is empty or missing a domain
- `troubleshooting-decision-tree-dashboard-totals-disagree`: Dashboard totals disagree
- `agent-task-recipes-recipe-create-a-reusable-operational-report`: Recipe: Create a reusable operational Report
- `agent-task-recipes-recipe-convert-duplicated-reports-into-one-dynamic-report`: Recipe: Convert duplicated Reports into one Dynamic Report
- `agent-task-recipes-recipe-introduce-persistence-for-a-slow-data-view`: Recipe: Introduce persistence for a slow Data View
- `agent-task-recipes-recipe-diagnose-an-empty-bi-dashboard`: Recipe: Diagnose an empty BI dashboard
- `agent-task-recipes-recipe-validate-a-registration-analytics-dashboard`: Recipe: Validate a registration analytics dashboard
- `source-map-immutable-implementation-evidence`: Immutable implementation evidence

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
