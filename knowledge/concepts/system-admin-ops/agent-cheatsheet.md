---
concept_id: system-admin-ops
title: System Administration And Operations Agent Cheatsheet
generated: true
---

# System Administration And Operations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Triage a recurring exception](tasks/recipe-triage-a-recurring-exception.md) | `Group`, `Page`, `Block` | `Group`, `Page`, `Block` |
| [Recipe: Refresh stale cached output with minimum scope](tasks/recipe-refresh-stale-cached-output-with-minimum-scope.md) | `Step`, `Page`, `Block` | `Step`, `Page`, `Block` |
| [Recipe: Create and assign a cache tag](tasks/recipe-create-and-assign-a-cache-tag.md) | `Group`, `Block` | `Group`, `Block` |
| [Recipe: Audit a scheduled job’s recent health](tasks/recipe-audit-a-scheduled-job-s-recent-health.md) | `Schedule`, `Label` | `Schedule`, `Label` |
| [Recipe: Restore a missing Universal Search entity](tasks/recipe-restore-a-missing-universal-search-entity.md) | `Group`, `GroupType`, `Schedule`, `Attribute`, `Person` | `Group`, `GroupType`, `Schedule`, `Attribute`, `Person` |
| [Recipe: Configure a bounded site-index crawl](tasks/recipe-configure-a-bounded-site-index-crawl.md) | `Location`, `Schedule`, `Page` | `Location`, `Schedule`, `Page` |
| [Recipe: Review and resolve a duplicate-person candidate](tasks/recipe-review-and-resolve-a-duplicate-person-candidate.md) | `Person`, `Attribute` | `Person`, `Attribute` |
| [Recipe: Review a Data Automation change before execution](tasks/recipe-review-a-data-automation-change-before-execution.md) | `Person`, `DataView`, `Group`, `Schedule`, `Campus`, `Family`, `Workflow` | `Person`, `DataView`, `Group`, `Schedule`, `Campus`, `Family`, `Workflow` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
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
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get r |
| `19.3` | core | Fixed Person Attribute Values configured for indexing not being included in Universal Search results after a bulk re-index, and restored the missing "Indexing Enabled" option in the Attributes block so Attributes can be flagged for indexing |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | needs-citation | live verification |
| `mental-model` | needs-citation | live verification |
| `jobs-and-scheduling-job-configuration-and-history` | high | live verification |
| `jobs-and-scheduling-version-specific-job-history-failures` | normal | live verification |
| `jobs-and-scheduling-job-backed-operational-processes` | high | live verification |
| `diagnostics-and-exceptions-exception-history` | normal | live verification |
| `cache-and-persisted-data-cache-manager-and-cache-tags` | normal | live verification |
| `cleanup-and-data-integrity-photo-verification` | normal | live verification |
| `troubleshooting-decision-tree-a-scheduled-job-stopped-producing-new-history` | normal | live verification |
| `troubleshooting-decision-tree-a-page-is-slow` | normal | live verification |
| `troubleshooting-decision-tree-updated-content-remains-stale` | normal | live verification |
| `troubleshooting-decision-tree-exceptions-repeat-after-a-page-or-block-change` | normal | live verification |
| `troubleshooting-decision-tree-universal-search-cannot-connect-after-an-environment-refresh` | normal | live verification |
| `troubleshooting-decision-tree-an-entity-type-returns-no-universal-search-results` | normal | live verification |
| `troubleshooting-decision-tree-universal-search-works-directly-but-not-through-smart-search` | normal | live verification |
| `troubleshooting-decision-tree-an-address-is-missing-coordinates` | normal | live verification |
| `troubleshooting-decision-tree-data-automation-changed-more-records-than-expected` | normal | live verification |
| `agent-task-recipes-recipe-triage-a-recurring-exception` | normal | live verification |
| `agent-task-recipes-recipe-refresh-stale-cached-output-with-minimum-scope` | normal | live verification |
| `agent-task-recipes-recipe-create-and-assign-a-cache-tag` | normal | live verification |
| `agent-task-recipes-recipe-audit-a-scheduled-job-s-recent-health` | normal | live verification |
| `agent-task-recipes-recipe-restore-a-missing-universal-search-entity` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-bounded-site-index-crawl` | normal | live verification |
| `agent-task-recipes-recipe-review-and-resolve-a-duplicate-person-candidate` | normal | live verification |
| `agent-task-recipes-recipe-review-a-data-automation-change-before-execution` | normal | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
