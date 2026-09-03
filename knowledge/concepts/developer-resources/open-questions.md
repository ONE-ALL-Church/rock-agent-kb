---
concept_id: developer-resources
title: Rock Developer Resources Open Questions
generated: true
---

# Rock Developer Resources Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (154 words)
- `version-and-authority-caveats`: Version And Authority Caveats (193 words)
- `agent-task-recipes-recipe-verify-a-save-or-rock-managed-file-deployment`: Recipe: Verify a save or Rock-managed file deployment (171 words)
- `known-gaps-and-live-verification`: Known Gaps And Live Verification (222 words)

## Community-Supported Only

- `helix-development-content-blocks-and-routing`: Content blocks and routing

## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `mental-model`: Mental Model
- `learning-path-quickstart-101-202-and-303`: Learning Path: Quickstart, 101, 202, And 303
- `developer-codex`: Developer Codex
- `developer-codex-naming-and-compatibility`: Naming and compatibility
- `obsidian-development`: Obsidian Development
- `obsidian-development-plugin-development`: Plugin development
- `obsidian-development-replacing-webforms-blocks`: Replacing WebForms blocks
- `helix-development-applications-and-endpoints`: Applications and endpoints
- `helix-development-content-blocks-and-routing`: Content blocks and routing
- `helix-development-security-and-data-integrity`: Security and data integrity
- `helix-development-packaging-status-conflict`: Packaging-status conflict
- `ai-agents`: AI Agents
- `rock-mobile-development`: Rock Mobile Development
- `apple-tv-and-roku-development-apple-tv`: Apple TV
- `apple-tv-and-roku-development-roku`: Roku
- `packaging-plugins-and-themes`: Packaging Plugins And Themes
- `utility-design-query-branch-and-release-references`: Utility, Design, Query, Branch, And Release References
- `troubleshooting-decision-tree-a-rest-request-returns-an-authorization-error`: A REST request returns an authorization error
- `troubleshooting-decision-tree-an-obsidian-action-works-but-redirect-or-metadata-lava-does-nothing`: An Obsidian action works but redirect or metadata Lava does nothing
- `troubleshooting-decision-tree-an-obsidian-block-shows-stale-or-mismatched-generated-types`: An Obsidian block shows stale or mismatched generated types
- `troubleshooting-decision-tree-a-webforms-to-obsidian-replacement-loses-settings`: A WebForms-to-Obsidian replacement loses settings
- `troubleshooting-decision-tree-a-helix-request-does-not-update-the-target-content`: A Helix request does not update the target content
- `troubleshooting-decision-tree-a-helix-form-submits-or-validates-unpredictably`: A Helix form submits or validates unpredictably
- `troubleshooting-decision-tree-a-mobile-feature-works-on-one-device-but-not-another`: A mobile feature works on one device but not another
- `troubleshooting-decision-tree-roku-navigation-or-focus-is-broken`: Roku navigation or focus is broken
- `troubleshooting-decision-tree-slingshot-imported-records-but-downstream-reporting-is-wrong`: Slingshot imported records but downstream reporting is wrong
- `agent-task-recipes-recipe-select-the-correct-developer-resource`: Recipe: Select the correct developer resource
- `agent-task-recipes-recipe-review-an-obsidian-block-change`: Recipe: Review an Obsidian block change
- `agent-task-recipes-recipe-regenerate-artifacts-after-a-model-change`: Recipe: Regenerate artifacts after a model change
- `agent-task-recipes-recipe-review-a-helix-endpoint-before-changing-it`: Recipe: Review a Helix endpoint before changing it
- `agent-task-recipes-recipe-validate-rock-mobile-compatibility`: Recipe: Validate Rock Mobile compatibility
- `agent-task-recipes-recipe-build-or-repair-a-roku-page`: Recipe: Build or repair a Roku page
- `agent-task-recipes-recipe-prepare-a-plugin-or-theme-package`: Recipe: Prepare a plugin or theme package
- `agent-task-recipes-recipe-validate-a-slingshot-migration`: Recipe: Validate a Slingshot migration
- `agent-task-recipes-recipe-inspect-page-content-with-a-rock-ai-agent`: Recipe: Inspect page content with a Rock AI agent
- `agent-task-recipes-recipe-verify-a-save-or-rock-managed-file-deployment`: Recipe: Verify a save or Rock-managed file deployment

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
