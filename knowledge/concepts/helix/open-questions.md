---
concept_id: helix
title: Helix Open Questions
generated: true
---

# Helix Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `known-gaps-and-live-verification`: Known Gaps And Live Verification (233 words)

## Community-Supported Only

- `agent-task-recipes-recipe-validate-a-rendered-helix-dashboard`: Recipe: Validate a rendered Helix dashboard
- `source-map-community-examples`: Community examples

## Needs Live Verification

- `agent-summary`: Agent Summary
- `htmx`: HTMX
- `lava-applications`: Lava Applications
- `lava-applications-editing-with-magnus`: Editing with Magnus
- `lava-endpoints`: Lava Endpoints
- `lava-endpoints-security-modes`: Security modes
- `lava-endpoints-request-merge-fields`: Request merge fields
- `lava-endpoints-enabled-commands-and-endpoint-responses`: Enabled commands and endpoint responses
- `forms-and-controls-control-shortcodes`: Control shortcodes
- `forms-and-controls-loading-indicators`: Loading indicators
- `security-and-observability-endpoint-security-review`: Endpoint security review
- `strategies-and-limitations-reviewed-community-patterns`: Reviewed community patterns
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-an-htmx-action-does-nothing-or-updates-the-wrong-region`: An HTMX action does nothing or updates the wrong region
- `troubleshooting-decision-tree-the-endpoint-returns-not-found-or-the-wrong-handler-runs`: The endpoint returns not found or the wrong handler runs
- `troubleshooting-decision-tree-a-user-is-denied-while-an-administrator-succeeds`: A user is denied while an administrator succeeds
- `troubleshooting-decision-tree-body-or-rawbody-is-empty-or-unavailable`: Body or RawBody is empty or unavailable
- `troubleshooting-decision-tree-a-loading-spinner-is-missing`: A loading spinner is missing
- `troubleshooting-decision-tree-endpoint-injected-styles-or-scripts-do-not-load`: Endpoint-injected styles or scripts do not load
- `troubleshooting-decision-tree-an-endpoint-is-slow-or-makes-excessive-database-calls`: An endpoint is slow or makes excessive database calls
- `troubleshooting-decision-tree-sorting-or-filtering-resets-after-refresh`: Sorting or filtering resets after refresh
- `agent-task-recipes-recipe-inspect-an-existing-helix-application-before-changing-it`: Recipe: Inspect an existing Helix application before changing it
- `agent-task-recipes-recipe-build-a-read-only-htmx-result-fragment`: Recipe: Build a read-only HTMX result fragment
- `agent-task-recipes-recipe-build-a-validated-mutation-form`: Recipe: Build a validated mutation form
- `agent-task-recipes-recipe-validate-a-rendered-helix-dashboard`: Recipe: Validate a rendered Helix dashboard
- `agent-task-recipes-recipe-decide-whether-to-replace-a-lava-application`: Recipe: Decide whether to replace a Lava Application

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
