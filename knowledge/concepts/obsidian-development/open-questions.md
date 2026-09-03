---
concept_id: obsidian-development
title: Obsidian Development Open Questions
generated: true
---

# Obsidian Development Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `scope-and-boundaries`: Scope And Boundaries
- `caching-api-calls`: Caching API Calls
- `development-environment-plugin-development`: Plugin Development
- `troubleshooting-decision-tree-an-older-component-fails-with-syntaxerror-15`: An Older Component Fails With `SyntaxError 15`
- `agent-task-recipes-recipe-cache-a-read-request`: Recipe: Cache A Read Request
- `agent-task-recipes-recipe-verify-a-community-suggested-block-action-save-path`: Recipe: Verify A Community-Suggested Block-Action Save Path

## Needs Live Verification

- `components-forms-and-typescript-contracts`: Components, Forms, And TypeScript Contracts
- `grid-reference-labels-and-number-badges`: Labels And Number Badges
- `grid-reference-attribute-person-and-rock-field-columns`: Attribute, Person, And Rock Field Columns
- `field-types-core-field-type-conversion`: Core Field Type Conversion
- `development-environment-plugin-development`: Plugin Development
- `development-environment-debugging`: Debugging
- `troubleshooting-decision-tree-a-save-reports-success-but-the-intended-values-do-not-persist`: A Save Reports Success But The Intended Values Do Not Persist
- `troubleshooting-decision-tree-a-grid-is-slow-even-with-a-small-page-size`: A Grid Is Slow Even With A Small Page Size
- `troubleshooting-decision-tree-a-picker-can-be-cleared-or-submitted-unexpectedly`: A Picker Can Be Cleared Or Submitted Unexpectedly
- `troubleshooting-decision-tree-an-older-component-fails-with-syntaxerror-15`: An Older Component Fails With `SyntaxError 15`
- `agent-task-recipes-recipe-implement-a-secure-block-action`: Recipe: Implement A Secure Block Action
- `agent-task-recipes-recipe-scaffold-and-harden-a-detail-block`: Recipe: Scaffold And Harden A Detail Block
- `agent-task-recipes-recipe-build-a-grid-with-reliable-actions`: Recipe: Build A Grid With Reliable Actions
- `agent-task-recipes-recipe-add-a-core-field-type-to-obsidian`: Recipe: Add A Core Field Type To Obsidian
- `agent-task-recipes-recipe-create-a-universal-plugin-picker`: Recipe: Create A Universal Plugin Picker
- `agent-task-recipes-recipe-coordinate-same-page-blocks-with-browser-bus`: Recipe: Coordinate Same-Page Blocks With Browser Bus
- `agent-task-recipes-recipe-cache-a-read-request`: Recipe: Cache A Read Request
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
