---
concept_id: lava
title: Lava Open Questions
generated: true
---

# Lava Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (109 words)

## Community-Supported Only

- `filters-text-and-output-encoding`: Text and output encoding
- `filters-where-and-short-link-caveats`: `where` and short-link caveats
- `commands`: Commands
- `commands-workflow-activation`: Workflow activation
- `reporting-and-persisted-results`: Reporting And Persisted Results
- `troubleshooting-decision-tree-an-entity-command-returns-no-rows-or-fails-before-iteration`: An entity command returns no rows or fails before iteration
- `troubleshooting-decision-tree-a-workflow-starts-but-submitted-values-are-missing`: A workflow starts but submitted values are missing
- `troubleshooting-decision-tree-a-helix-endpoint-works-for-administrators-but-not-its-audience`: A Helix endpoint works for administrators but not its audience
- `agent-task-recipes-recipe-review-an-existing-lava-surface-safely`: Recipe: Review an existing Lava surface safely
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `source-map-reviewed-community-patterns`: Reviewed community patterns

## Needs Live Verification

- `agent-summary`: Agent Summary
- `core-syntax-and-engine`: Core Syntax And Engine
- `core-syntax-and-engine-fluid-and-dotliquid`: Fluid and DotLiquid
- `filters-text-and-output-encoding`: Text and output encoding
- `filters-dates-and-time-zones`: Dates and time zones
- `filters-where-and-short-link-caveats`: `where` and short-link caveats
- `commands`: Commands
- `commands-entity-retrieval`: Entity retrieval
- `commands-workflow-activation`: Workflow activation
- `shortcodes`: Shortcodes
- `execution-contexts-and-output-contracts-advanced-html-and-communications`: Advanced HTML and communications
- `execution-contexts-and-output-contracts-rock-mobile`: Rock Mobile
- `execution-contexts-and-output-contracts-tv-applications`: TV applications
- `remote-lava-and-apis`: Remote Lava And APIs
- `helix-and-lava-applications`: Helix And Lava Applications
- `workflows-and-lava`: Workflows And Lava
- `lava-backed-ai-tools`: Lava-Backed AI Tools
- `troubleshooting-decision-tree-lava-renders-blank-or-a-merge-field-is-missing`: Lava renders blank or a merge field is missing
- `troubleshooting-decision-tree-a-parser-error-points-at-an-innocent-looking-line`: A parser error points at an innocent-looking line
- `troubleshooting-decision-tree-an-entity-command-returns-no-rows-or-fails-before-iteration`: An entity command returns no rows or fails before iteration
- `troubleshooting-decision-tree-a-modify-command-appears-to-succeed-but-data-is-unchanged`: A modify command appears to succeed but data is unchanged
- `troubleshooting-decision-tree-a-later-write-fails-with-an-earlier-validation-error`: A later write fails with an earlier validation error
- `troubleshooting-decision-tree-a-workflow-starts-but-submitted-values-are-missing`: A workflow starts but submitted values are missing
- `troubleshooting-decision-tree-a-shortcode-displays-as-raw-text`: A shortcode displays as raw text
- `troubleshooting-decision-tree-a-helix-endpoint-works-for-administrators-but-not-its-audience`: A Helix endpoint works for administrators but not its audience
- `troubleshooting-decision-tree-an-htmx-fragment-loses-scripts-styles-or-ui-state`: An HTMX fragment loses scripts, styles or UI state
- `troubleshooting-decision-tree-rock-mobile-content-is-stale-anonymous-or-invalid-xaml`: Rock Mobile content is stale, anonymous or invalid XAML
- `troubleshooting-decision-tree-a-remote-lava-route-exposes-more-than-intended`: A remote Lava route exposes more than intended
- `agent-task-recipes-recipe-review-an-existing-lava-surface-safely`: Recipe: Review an existing Lava surface safely
- `agent-task-recipes-recipe-build-a-bounded-read-only-entity-view`: Recipe: Build a bounded read-only entity view
- `agent-task-recipes-recipe-preflight-a-workflow-activation`: Recipe: Preflight a workflow activation
- `agent-task-recipes-recipe-publish-a-reusable-shortcode`: Recipe: Publish a reusable shortcode
- `agent-task-recipes-recipe-build-a-read-only-helix-active-search-page`: Recipe: Build a read-only Helix active-search page
- `agent-task-recipes-recipe-validate-a-rock-mobile-lava-block`: Recipe: Validate a Rock Mobile Lava block
- `agent-task-recipes-recipe-design-a-lava-backed-ai-tool`: Recipe: Design a Lava-backed AI tool
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
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
