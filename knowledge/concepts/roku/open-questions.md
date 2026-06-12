---
concept_id: roku
title: Roku Apps Open Questions
generated: true
---

# Roku Apps Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `7-common-roku-apps-workflows-add-a-page`: Add A Page (97 words)
- `17-implementation-playbooks-playbook-create-a-minimal-roku-home-page`: Playbook: Create A Minimal Roku Home Page (111 words)

## Community-Supported Only


## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `3-roku-apps-mental-model`: 3. Roku Apps Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-application-configuration`: Application Configuration
- `5-core-configuration-and-data-model-page-configuration`: Page Configuration
- `5-core-configuration-and-data-model-lava-merge-fields`: Lava Merge Fields
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `7-common-roku-apps-workflows-build-a-first-app`: Build A First App
- `7-common-roku-apps-workflows-build-a-menu`: Build A Menu
- `7-common-roku-apps-workflows-add-login`: Add Login
- `8-roku-getting-started-deep-dive-provisioning`: Provisioning
- `8-roku-getting-started-deep-dive-page-construction`: Page Construction
- `8-roku-getting-started-deep-dive-device-validation`: Device Validation
- `9-roku-commands-deep-dive-navigation-commands`: Navigation Commands
- `9-roku-commands-deep-dive-media-commands`: Media Commands
- `10-roku-controls-deep-dive-rock-page`: Rock:Page
- `10-roku-controls-deep-dive-rock-button`: Rock:Button
- `10-roku-controls-deep-dive-rock-focusgroup`: Rock:FocusGroup
- `10-roku-controls-deep-dive-built-in-scenegraph-nodes`: Built-In SceneGraph Nodes
- `11-roku-layouts-and-resources-deep-dive-rowlist`: RowList
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-api-integrations`: API Integrations
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-lava`: Lava
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-cms`: CMS
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-security`: Security
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-media`: Media
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-tv-apps`: TV Apps
- `13-administration-and-operational-guardrails-version-gate`: Version Gate
- `13-administration-and-operational-guardrails-environment-separation`: Environment Separation
- `13-administration-and-operational-guardrails-secret-handling`: Secret Handling
- `13-administration-and-operational-guardrails-interaction-tracking`: Interaction Tracking
- `13-administration-and-operational-guardrails-content-governance`: Content Governance
- `15-reporting-analytics-and-model-map`: 15. Reporting, Analytics, And Model Map
- `16-version-and-release-caveats`: 16. Version And Release Caveats
- `17-implementation-playbooks-playbook-create-a-minimal-roku-home-page`: Playbook: Create A Minimal Roku Home Page
- `17-implementation-playbooks-playbook-build-a-media-row`: Playbook: Build A Media Row
- `17-implementation-playbooks-playbook-add-campus-selection`: Playbook: Add Campus Selection
- `17-implementation-playbooks-playbook-add-login`: Playbook: Add Login
- `17-implementation-playbooks-playbook-tune-caching`: Playbook: Tune Caching
- `19-agent-task-recipes-recipe-review-a-roku-page-for-safety`: Recipe: Review A Roku Page For Safety

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
