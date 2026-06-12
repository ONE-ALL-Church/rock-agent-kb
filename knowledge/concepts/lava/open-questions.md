---
concept_id: lava
title: Lava Open Questions
generated: true
---

# Lava Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `7-common-lava-workflows-launching-a-workflow-from-lava`: Launching A Workflow From Lava (87 words)
- `11-related-rock-areas-cms-workflows-sql-security-cms`: CMS (85 words)
- `16-implementation-playbooks-playbook-add-a-safe-read-only-entity-list`: Playbook: Add A Safe Read-Only Entity List (104 words)

## Community-Supported Only

- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `7-common-lava-workflows-building-a-dynamic-report-page`: Building A Dynamic Report Page
- `7-common-lava-workflows-formatting-data-with-shortcodes`: Formatting Data With Shortcodes
- `9-filters-deep-dive-legacy-attribute-syntax`: Legacy Attribute Syntax
- `12-administration-and-operational-guardrails-exception-list-checklist`: Exception List Checklist
- `13-developer-api-lava-and-source-code-landmarks-rocku`: RockU
- `14-reporting-analytics-and-model-map-reporting-with-lava`: Reporting With Lava
- `14-reporting-analytics-and-model-map-model-map`: Model Map
- `18-agent-task-recipes-recipe-find-legacy-attribute-lava`: Recipe: Find Legacy Attribute Lava
- `18-agent-task-recipes-recipe-create-a-staff-friendly-link-copy-shortcode`: Recipe: Create A Staff-Friendly Link Copy Shortcode
- `18-agent-task-recipes-recipe-add-a-translation-shortcode`: Recipe: Add A Translation Shortcode
- `approved-media-coverage`: Approved Media Coverage
- `19-source-map-and-dependency-notes-community-pattern-sources`: Community Pattern Sources

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-lava-engine-liquid-framework`: Lava Engine Liquid Framework
- `5-core-configuration-and-data-model-default-enabled-lava-commands`: Default Enabled Lava Commands
- `5-core-configuration-and-data-model-html-block-command-enablement`: HTML Block Command Enablement
- `5-core-configuration-and-data-model-communication-entry-command-enablement`: Communication Entry Command Enablement
- `5-core-configuration-and-data-model-lava-shortcode-entity`: Lava Shortcode Entity
- `5-core-configuration-and-data-model-lava-shortcode-cache`: Lava Shortcode Cache
- `5-core-configuration-and-data-model-lava-webhooks`: Lava Webhooks
- `5-core-configuration-and-data-model-remote-lava-rest-endpoint`: Remote Lava REST Endpoint
- `6-primary-entities-and-relationships-block-page-site-theme-and-include-files`: Block, Page, Site, Theme, And Include Files
- `6-primary-entities-and-relationships-entity-commands-and-rock-models`: Entity Commands And Rock Models
- `6-primary-entities-and-relationships-attribute-and-attributevalue`: Attribute And AttributeValue
- `6-primary-entities-and-relationships-workflow-workflow-type-activity-type-and-attributes`: Workflow, Workflow Type, Activity Type, And Attributes
- `6-primary-entities-and-relationships-interaction-records`: Interaction Records
- `6-primary-entities-and-relationships-devices-and-printers`: Devices And Printers
- `6-primary-entities-and-relationships-search-index-documents`: Search Index Documents
- `7-common-lava-workflows-building-a-dynamic-report-page`: Building A Dynamic Report Page
- `7-common-lava-workflows-calling-external-apis`: Calling External APIs
- `7-common-lava-workflows-adding-page-level-css`: Adding Page-Level CSS
- `8-commands-deep-dive-entity-command`: Entity Command
- `8-commands-deep-dive-interaction-write-commands`: Interaction Write Commands
- `8-commands-deep-dive-adaptive-message-command`: Adaptive Message Command
- `8-commands-deep-dive-helix-commands-and-data-modification`: Helix Commands And Data Modification
- `9-filters-deep-dive`: 9. Filters Deep Dive
- `9-filters-deep-dive-attribute-filter`: Attribute Filter
- `9-filters-deep-dive-legacy-attribute-syntax`: Legacy Attribute Syntax
- `9-filters-deep-dive-date-filters`: Date Filters
- `9-filters-deep-dive-person-filters`: Person Filters
- `9-filters-deep-dive-text-filters`: Text Filters
- `9-filters-deep-dive-culture-affected-filters`: Culture-Affected Filters
- `10-shortcodes-deep-dive-shortcode-configuration-fields`: Shortcode Configuration Fields
- `10-shortcodes-deep-dive-enabled-commands-inside-shortcodes`: Enabled Commands Inside Shortcodes
- `10-shortcodes-deep-dive-scope-behavior`: Scope Behavior
- `11-related-rock-areas-cms-workflows-sql-security-cms`: CMS
- `11-related-rock-areas-cms-workflows-sql-security-workflows`: Workflows
- `11-related-rock-areas-cms-workflows-sql-security-sql`: SQL
- `12-administration-and-operational-guardrails-pre-change-checklist`: Pre-Change Checklist

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
