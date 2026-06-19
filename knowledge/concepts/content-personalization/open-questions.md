---
concept_id: content-personalization
title: Content And Personalization Open Questions
generated: true
---

# Content And Personalization Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `8-content-channels-deep-dive-channel-configuration`: Channel configuration (97 words)
- `10-adaptive-messages-deep-dive-when-to-use-adaptive-messages`: When to use adaptive messages (104 words)
- `10-adaptive-messages-deep-dive-troubleshooting-adaptive-messages`: Troubleshooting adaptive messages (126 words)
- `15-reporting-analytics-and-model-map-content-item-reporting`: Content item reporting (104 words)
- `18-troubleshooting-decision-tree-content-item-is-missing-from-a-page`: Content item is missing from a page (115 words)
- `18-troubleshooting-decision-tree-asset-image-does-not-display`: Asset image does not display (104 words)

## Community-Supported Only


## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `3-content-and-personalization-mental-model`: 3. Content And Personalization Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model`: 5. Core Configuration And Data Model
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `7-common-content-and-personalization-workflows-create-a-structured-content-channel`: Create a structured content channel
- `7-common-content-and-personalization-workflows-publish-a-content-item`: Publish a content item
- `7-common-content-and-personalization-workflows-display-a-list-of-channel-items`: Display a list of channel items
- `7-common-content-and-personalization-workflows-display-a-single-channel-item`: Display a single channel item
- `7-common-content-and-personalization-workflows-aggregate-content-into-a-collection`: Aggregate content into a collection
- `7-common-content-and-personalization-workflows-add-personalization-to-channel-items`: Add personalization to channel items
- `8-content-channels-deep-dive-channel-configuration`: Channel configuration
- `8-content-channels-deep-dive-display-and-lava`: Display and Lava
- `8-content-channels-deep-dive-security`: Security
- `9-asset-manager-deep-dive-viewing-and-managing-assets`: Viewing and managing assets
- `9-asset-manager-deep-dive-storage-provider-setup`: Storage provider setup
- `9-asset-manager-deep-dive-image-and-file-performance`: Image and file performance
- `9-asset-manager-deep-dive-structured-content-file-behavior`: Structured content file behavior
- `10-adaptive-messages-deep-dive-setup-model`: Setup model
- `10-adaptive-messages-deep-dive-entity-and-api-landmarks`: Entity and API landmarks
- `10-adaptive-messages-deep-dive-troubleshooting-adaptive-messages`: Troubleshooting adaptive messages
- `11-personalization-and-segments-deep-dive-site-level-prerequisites`: Site-level prerequisites
- `11-personalization-and-segments-deep-dive-segment-types`: Segment types
- `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-lava`: Lava
- `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-security`: Security
- `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-communications`: Communications
- `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-media`: Media
- `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-workflows`: Workflows
- `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-people`: People
- `13-administration-and-operational-guardrails-change-management`: Change management
- `13-administration-and-operational-guardrails-job-monitoring`: Job monitoring
- `13-administration-and-operational-guardrails-cache-and-indexing`: Cache and indexing
- `14-developer-api-lava-and-source-code-landmarks-rest-and-model-landmarks`: REST and model landmarks
- `14-developer-api-lava-and-source-code-landmarks-content-channel-item-personal-list-lava-block`: Content Channel Item Personal List Lava block
- `14-developer-api-lava-and-source-code-landmarks-lava-interaction-logging`: Lava interaction logging
- `15-reporting-analytics-and-model-map-content-item-reporting`: Content item reporting
- `15-reporting-analytics-and-model-map-content-collection-analytics`: Content collection analytics
- `15-reporting-analytics-and-model-map-personalization-reporting`: Personalization reporting
- `16-version-and-release-caveats`: 16. Version And Release Caveats

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
