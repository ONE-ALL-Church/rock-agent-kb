---
concept_id: hosting-infrastructure
title: Hosting And Infrastructure Open Questions
generated: true
---

# Hosting And Infrastructure Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (164 words)
- `agent-task-recipes-recipe-perform-a-pre-launch-infrastructure-review`: Recipe: Perform a pre-launch infrastructure review (127 words)

## Community-Supported Only

- `operational-readiness-smtp`: SMTP
- `source-map-community-examples-not-promoted-to-official-behavior`: Community examples not promoted to official behavior

## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `mental-model-5-operational-proof`: 5. Operational proof
- `saas-hosting`: SaaS Hosting
- `azure-hosting-recommended-service-pattern`: Recommended service pattern
- `azure-hosting-azure-sql-identity-setup`: Azure SQL identity setup
- `internal-hosting-iis-configuration`: IIS configuration
- `internal-hosting-initial-rock-installation`: Initial Rock installation
- `web-farms-and-server-clusters-session-affinity`: Session affinity
- `web-farms-and-server-clusters-routes-and-node-coordination`: Routes and node coordination
- `read-only-and-analytics-database-contexts-rockcontextreadonly`: `RockContextReadOnly`
- `read-only-and-analytics-database-contexts-rockcontextanalytics`: `RockContextAnalytics`
- `operational-readiness-smtp`: SMTP
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-rock-page-is-slow`: A Rock page is slow
- `troubleshooting-decision-tree-files-or-images-work-intermittently-in-a-web-farm`: Files or images work intermittently in a web farm
- `troubleshooting-decision-tree-check-in-loses-state-or-behaves-differently-between-requests`: Check-in loses state or behaves differently between requests
- `troubleshooting-decision-tree-a-scheduled-job-runs-more-than-once-in-a-web-farm`: A scheduled job runs more than once in a web farm
- `troubleshooting-decision-tree-a-web-farm-node-is-missing-or-appears-unresponsive`: A web-farm node is missing or appears unresponsive
- `troubleshooting-decision-tree-a-new-page-route-works-on-only-some-nodes`: A new page route works on only some nodes
- `troubleshooting-decision-tree-rock-cannot-connect-to-sql-server`: Rock cannot connect to SQL Server
- `troubleshooting-decision-tree-a-data-view-or-report-fails-against-the-read-only-database`: A Data View or report fails against the read-only database
- `troubleshooting-decision-tree-analytics-still-load-the-primary-database`: Analytics still load the primary database
- `troubleshooting-decision-tree-http-does-not-redirect-to-https`: HTTP does not redirect to HTTPS
- `agent-task-recipes-recipe-select-a-hosting-model`: Recipe: Select a hosting model
- `agent-task-recipes-recipe-build-an-azure-capacity-baseline`: Recipe: Build an Azure capacity baseline
- `agent-task-recipes-recipe-prepare-a-saas-migration`: Recipe: Prepare a SaaS migration
- `agent-task-recipes-recipe-provision-the-documented-azure-layout`: Recipe: Provision the documented Azure layout
- `agent-task-recipes-recipe-offload-reports-and-analytics-to-a-read-only-database`: Recipe: Offload reports and analytics to a read-only database
- `agent-task-recipes-recipe-diagnose-a-slow-rock-19-page`: Recipe: Diagnose a slow Rock 19 page
- `agent-task-recipes-recipe-perform-a-pre-launch-infrastructure-review`: Recipe: Perform a pre-launch infrastructure review
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

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
