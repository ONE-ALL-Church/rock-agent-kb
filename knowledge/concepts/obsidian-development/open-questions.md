---
concept_id: obsidian-development
title: Obsidian Development Open Questions
generated: true
---

# Obsidian Development Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only


## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `3-obsidian-development-mental-model`: 3. Obsidian Development Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model`: 5. Core Configuration And Data Model
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `7-common-obsidian-development-workflows-build-a-new-core-list-block`: Build A New Core List Block
- `7-common-obsidian-development-workflows-build-a-detail-block`: Build A Detail Block
- `7-common-obsidian-development-workflows-convert-webforms-behavior-to-obsidian`: Convert WebForms Behavior To Obsidian
- `7-common-obsidian-development-workflows-troubleshoot-an-existing-obsidian-screen`: Troubleshoot An Existing Obsidian Screen
- `8-blocks-deep-dive-c-block-responsibilities`: C# Block Responsibilities
- `8-blocks-deep-dive-typescript-component-responsibilities`: TypeScript Component Responsibilities
- `8-blocks-deep-dive-block-actions`: Block Actions
- `8-blocks-deep-dive-blockcrumbs-and-navigation-context`: BlockCrumbs And Navigation Context
- `8-blocks-deep-dive-detail-blocks`: Detail Blocks
- `8-blocks-deep-dive-list-blocks`: List Blocks
- `8-blocks-deep-dive-person-preferences`: Person Preferences
- `9-grid-reference-deep-dive-standard-column-properties`: Standard Column Properties
- `9-grid-reference-deep-dive-textcolumn`: TextColumn
- `9-grid-reference-deep-dive-booleancolumn`: BooleanColumn
- `9-grid-reference-deep-dive-labelcolumn`: LabelColumn
- `9-grid-reference-deep-dive-highlightdetailcolumn`: HighlightDetailColumn
- `9-grid-reference-deep-dive-personcolumn`: PersonColumn
- `9-grid-reference-deep-dive-selectcolumn`: SelectColumn
- `9-grid-reference-deep-dive-reordercolumn`: ReorderColumn
- `9-grid-reference-deep-dive-securitycolumn`: SecurityColumn
- `10-field-types-deep-dive-converting-core-field-types`: Converting Core Field Types
- `10-field-types-deep-dive-field-type-gallery`: Field Type Gallery
- `10-field-types-deep-dive-common-field-type-failure-modes`: Common Field Type Failure Modes
- `11-development-environment-deep-dive-core-development-setup`: Core Development Setup
- `11-development-environment-deep-dive-vs-code-debugging`: VS Code Debugging
- `11-development-environment-deep-dive-plugin-development-setup`: Plugin Development Setup
- `11-development-environment-deep-dive-build-and-type-checking`: Build And Type Checking
- `12-related-rock-areas-developer-resources-api-integrations-security-cms-platform-configuration-workflows-cms`: CMS
- `12-related-rock-areas-developer-resources-api-integrations-security-cms-platform-configuration-workflows-platform-configuration`: Platform Configuration
- `12-related-rock-areas-developer-resources-api-integrations-security-cms-platform-configuration-workflows-workflows`: Workflows
- `13-administration-and-operational-guardrails-security-first`: Security First
- `13-administration-and-operational-guardrails-configuration-hygiene`: Configuration Hygiene
- `13-administration-and-operational-guardrails-admin-ui-expectations`: Admin UI Expectations
- `15-reporting-analytics-and-model-map-field-types-and-filtering`: Field Types And Filtering

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
