---
concept_id: developer-resources
title: Rock Developer Resources Open Questions
generated: true
---

# Rock Developer Resources Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `29-source-map-and-dependency-notes-community-examples-and-q-a`: Community Examples And Q&A

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-rock-developer-resources-mental-model-layer-1-platform-and-runtime`: Layer 1: Platform and runtime
- `3-rock-developer-resources-mental-model-layer-3-data-model-and-persistence`: Layer 3: Data model and persistence
- `3-rock-developer-resources-mental-model-layer-5-release-and-branch-reality`: Layer 5: Release and branch reality
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-pages-layouts-sites-and-blocks`: Pages, layouts, sites, and blocks
- `5-core-configuration-and-data-model-attributes-and-defined-values`: Attributes and defined values
- `5-core-configuration-and-data-model-custom-entities-and-services`: Custom entities and services
- `5-core-configuration-and-data-model-lava-applications-and-lava-endpoints`: Lava Applications and Lava Endpoints
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `6-primary-entities-and-relationships-page-block-and-block-type`: Page, block, and block type
- `6-primary-entities-and-relationships-person-and-personalias`: Person and PersonAlias
- `6-primary-entities-and-relationships-attribute-attributevalue-definedtype-definedvalue`: Attribute, AttributeValue, DefinedType, DefinedValue
- `6-primary-entities-and-relationships-workflow-and-workflow-actions`: Workflow and workflow actions
- `6-primary-entities-and-relationships-lavaapplication-and-lavaendpoint`: LavaApplication and LavaEndpoint
- `6-primary-entities-and-relationships-interaction-and-analytics`: Interaction and analytics
- `6-primary-entities-and-relationships-theme`: Theme
- `7-common-rock-developer-resources-workflows-package-and-deploy-a-plugin-or-theme`: Package and deploy a plugin or theme
- `7-common-rock-developer-resources-workflows-diagnose-a-broken-developer-feature`: Diagnose a broken developer feature
- `8-developer-codex-deep-dive`: 8. Developer Codex Deep Dive
- `8-developer-codex-deep-dive-code-generator-and-model-changes`: Code generator and model changes
- `8-developer-codex-deep-dive-obsidian-chop-swap-sneak`: Obsidian Chop, Swap, Sneak
- `8-developer-codex-deep-dive-testing-and-peer-review`: Testing and peer review
- `9-developer-101-launchpad-deep-dive-operational-pattern`: Operational pattern
- `9-developer-101-launchpad-deep-dive-personalias-vs-person`: PersonAlias vs Person
- `9-developer-101-launchpad-deep-dive-security`: Security
- `10-developer-202-ignition-deep-dive-migrations-in-202`: Migrations in 202
- `10-developer-202-ignition-deep-dive-data-migration-helper-methods`: Data migration helper methods
- `10-developer-202-ignition-deep-dive-agent-cautions`: Agent cautions
- `11-developer-303-blast-off-deep-dive-data-view-filters-and-dynamic-linq`: Data view filters and Dynamic LINQ
- `11-developer-303-blast-off-deep-dive-rest-api`: REST API
- `12-obsidian-deep-dive-detail-blocks`: Detail blocks
- `12-obsidian-deep-dive-grids`: Grids
- `12-obsidian-deep-dive-field-types-and-ui-controls`: Field types and UI controls
- `13-helix-deep-dive-plugin-vs-core-status`: Plugin vs core status
- `13-helix-deep-dive-lava-applications`: Lava Applications
- `13-helix-deep-dive-lava-endpoints`: Lava Endpoints
- `14-ai-agents-deep-dive-live-verification`: Live verification

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
