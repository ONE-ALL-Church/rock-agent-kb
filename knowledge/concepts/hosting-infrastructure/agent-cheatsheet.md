---
concept_id: hosting-infrastructure
title: Hosting And Infrastructure Agent Cheatsheet
generated: true
---

# Hosting And Infrastructure Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Select a hosting model](tasks/recipe-select-a-hosting-model.md) | `Workflow` | `Workflow` |
| [Recipe: Build an Azure capacity baseline](tasks/recipe-build-an-azure-capacity-baseline.md) | `Attendance`, `Schedule` | `Attendance`, `Schedule` |
| [Recipe: Prepare a SaaS migration](tasks/recipe-prepare-a-saas-migration.md) | `Schedule` | `Schedule` |
| [Recipe: Provision the documented Azure layout](tasks/recipe-provision-the-documented-azure-layout.md) | `Step`, `Group` | `Step`, `Group` |
| [Recipe: Prepare an internal Rock 19 web server](tasks/recipe-prepare-an-internal-rock-19-web-server.md) |  |  |
| [Recipe: Activate a Rock 19 web farm](tasks/recipe-activate-a-rock-19-web-farm.md) | `Schedule`, `Page` | `Schedule`, `Page` |
| [Recipe: Offload reports and analytics to a read-only database](tasks/recipe-offload-reports-and-analytics-to-a-read-only-database.md) | `Attendance`, `DataView`, `Block` | `Attendance`, `DataView`, `Block` |
| [Recipe: Diagnose a slow Rock 19 page](tasks/recipe-diagnose-a-slow-rock-19-page.md) | `Page`, `DataView`, `Block` | `Page`, `DataView`, `Block` |
| [Recipe: Perform a pre-launch infrastructure review](tasks/recipe-perform-a-pre-launch-infrastructure-review.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Added an automatic data migration that moves File Storage Provider settings from any existing legacy Azure Blob Storage provider plugin (Pillars) to the core Azure Blob Storage provider. This is required because the legacy provider can no l |
| `17.5` | core | Fixed an error that occurred when editing a Content Channel Type with Attributes of type Image, File, or Binary File. The issue happened if the storage location was set to Azure Blob Storage or File System (or newly created FileType). This  |
| `17.0` | core | Improved database performance with new and revised indexes across multiple tables. These changes improve query efficiency for transactions, person records, group hierarchies, and interactions, based on SQL Server recommendations and other a |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | live verification |
| `mental-model-5-operational-proof` | citation-only | live verification |
| `saas-hosting` | normal | live verification |
| `azure-hosting-recommended-service-pattern` | normal | live verification |
| `azure-hosting-azure-sql-identity-setup` | normal | live verification |
| `internal-hosting-iis-configuration` | normal | live verification |
| `internal-hosting-initial-rock-installation` | normal | live verification |
| `web-farms-and-server-clusters-session-affinity` | normal | live verification |
| `web-farms-and-server-clusters-routes-and-node-coordination` | normal | live verification |
| `read-only-and-analytics-database-contexts-rockcontextreadonly` | normal | live verification |
| `read-only-and-analytics-database-contexts-rockcontextanalytics` | normal | live verification |
| `operational-readiness-smtp` | community-supported | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-rock-page-is-slow` | normal | live verification |
| `troubleshooting-decision-tree-files-or-images-work-intermittently-in-a-web-farm` | normal | live verification |
| `troubleshooting-decision-tree-check-in-loses-state-or-behaves-differently-between-requests` | normal | live verification |
| `troubleshooting-decision-tree-a-scheduled-job-runs-more-than-once-in-a-web-farm` | high | live verification |
| `troubleshooting-decision-tree-a-web-farm-node-is-missing-or-appears-unresponsive` | normal | live verification |
| `troubleshooting-decision-tree-a-new-page-route-works-on-only-some-nodes` | normal | live verification |
| `troubleshooting-decision-tree-rock-cannot-connect-to-sql-server` | normal | live verification |
| `troubleshooting-decision-tree-a-data-view-or-report-fails-against-the-read-only-database` | normal | live verification |
| `troubleshooting-decision-tree-analytics-still-load-the-primary-database` | normal | live verification |
| `troubleshooting-decision-tree-http-does-not-redirect-to-https` | normal | live verification |
| `agent-task-recipes-recipe-select-a-hosting-model` | normal | live verification |
| `agent-task-recipes-recipe-build-an-azure-capacity-baseline` | normal | live verification |
| `agent-task-recipes-recipe-prepare-a-saas-migration` | normal | live verification |
| `agent-task-recipes-recipe-provision-the-documented-azure-layout` | normal | live verification |
| `agent-task-recipes-recipe-offload-reports-and-analytics-to-a-read-only-database` | normal | live verification |
| `agent-task-recipes-recipe-diagnose-a-slow-rock-19-page` | normal | live verification |
| `agent-task-recipes-recipe-perform-a-pre-launch-infrastructure-review` | needs-citation | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-community-examples-not-promoted-to-official-behavior` | community-supported | community-supported |
