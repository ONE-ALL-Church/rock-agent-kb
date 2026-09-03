---
concept_id: data-views-reports
title: Data Views And Reports Agent Cheatsheet
generated: true
---

# Data Views And Reports Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Create a reusable operational Report](tasks/recipe-create-a-reusable-operational-report.md) | `DataView`, `Page`, `Block` | `DataView`, `Page`, `Block` |
| [Recipe: Convert duplicated Reports into one Dynamic Report](tasks/recipe-convert-duplicated-reports-into-one-dynamic-report.md) | `DataView`, `Campus`, `Block` | `DataView`, `Campus`, `Block` |
| [Recipe: Introduce persistence for a slow Data View](tasks/recipe-introduce-persistence-for-a-slow-data-view.md) | `DataView`, `Group`, `Attribute` | `DataView`, `Group`, `Attribute` |
| [Recipe: Diagnose an empty BI dashboard](tasks/recipe-diagnose-an-empty-bi-dashboard.md) | `Page`, `Block`, `Schedule` | `Page`, `Block`, `Schedule` |
| [Recipe: Validate a registration analytics dashboard](tasks/recipe-validate-a-registration-analytics-dashboard.md) | `Person`, `Group`, `Campus`, `Label`, `Page`, `Attribute` | `Person`, `Group`, `Campus`, `Label`, `Page`, `Attribute` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | normal | live verification |
| `data-views` | normal | live verification |
| `report-security` | normal | live verification |
| `dynamic-reports-and-custom-reporting-blocks` | normal | live verification |
| `business-intelligence` | normal | live verification |
| `sql-reporting-patterns` | citation-only | live verification |
| `data-integrity-and-reporting-quality` | citation-only | live verification |
| `domain-reporting-workflows-communication-audiences-and-delivery-health` | community-supported | live verification |
| `domain-reporting-workflows-schedule-dates-and-operational-snapshots` | citation-only | live verification |
| `troubleshooting-decision-tree-a-data-view-returns-the-wrong-records` | normal | live verification |
| `troubleshooting-decision-tree-a-report-is-slow` | normal | live verification |
| `troubleshooting-decision-tree-a-report-exposes-unexpected-sensitive-data` | normal | live verification |
| `troubleshooting-decision-tree-a-dynamic-report-filter-does-not-behave-as-expected` | normal | live verification |
| `troubleshooting-decision-tree-a-lava-entity-query-ignores-its-filters` | citation-only | live verification |
| `troubleshooting-decision-tree-a-bi-report-is-empty-or-missing-a-domain` | normal | live verification |
| `troubleshooting-decision-tree-dashboard-totals-disagree` | normal | live verification |
| `agent-task-recipes-recipe-create-a-reusable-operational-report` | normal | live verification |
| `agent-task-recipes-recipe-convert-duplicated-reports-into-one-dynamic-report` | normal | live verification |
| `agent-task-recipes-recipe-introduce-persistence-for-a-slow-data-view` | normal | live verification |
| `agent-task-recipes-recipe-diagnose-an-empty-bi-dashboard` | normal | live verification |
| `agent-task-recipes-recipe-validate-a-registration-analytics-dashboard` | normal | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
| `source-map-community-reviewed-patterns` | community-supported | community-supported |
| `source-map-immutable-implementation-evidence` | normal | live verification |
