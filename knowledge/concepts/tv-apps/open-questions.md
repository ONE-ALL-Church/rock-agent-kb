---
concept_id: tv-apps
title: TV Apps Open Questions
generated: true
---

# TV Apps Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only


## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-tv-apps-mental-model`: 3. TV Apps Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-apple-tv-application-configuration`: Apple TV Application Configuration
- `5-core-configuration-and-data-model-roku-application-configuration`: Roku Application Configuration
- `5-core-configuration-and-data-model-tv-page-configuration`: TV Page Configuration
- `5-core-configuration-and-data-model-remote-authentication-data-model`: Remote Authentication Data Model
- `6-primary-entities-and-relationships-application-to-page`: Application To Page
- `6-primary-entities-and-relationships-application-to-api-key`: Application To API Key
- `6-primary-entities-and-relationships-remoteauthenticationsession-to-person-and-site`: RemoteAuthenticationSession To Person And Site
- `6-primary-entities-and-relationships-page-to-interaction`: Page To Interaction
- `7-common-tv-apps-workflows-create-a-new-apple-tv-app`: Create A New Apple TV App
- `7-common-tv-apps-workflows-create-a-new-roku-app`: Create A New Roku App
- `7-common-tv-apps-workflows-add-media-playback`: Add Media Playback
- `8-apple-tv-deep-dive-apple-tv-platform-contract`: Apple TV Platform Contract
- `8-apple-tv-deep-dive-apple-tv-pages-and-merge-fields`: Apple TV Pages And Merge Fields
- `8-apple-tv-deep-dive-apple-tv-testing-and-demo-key`: Apple TV Testing And Demo Key
- `8-apple-tv-deep-dive-apple-tv-application-images`: Apple TV Application Images
- `9-roku-deep-dive-roku-pages`: Roku Pages
- `9-roku-deep-dive-roku-commands`: Roku Commands
- `10-security-and-authentication-deep-dive-api-key-security`: API Key Security
- `10-security-and-authentication-deep-dive-remote-authentication-flow`: Remote Authentication Flow
- `10-security-and-authentication-deep-dive-remote-auth-component-selection`: Remote Auth Component Selection
- `11-styling-and-controls-deep-dive-apple-tv-styling`: Apple TV Styling
- `11-styling-and-controls-deep-dive-apple-tv-custom-controls`: Apple TV Custom Controls
- `11-styling-and-controls-deep-dive-roku-controls`: Roku Controls
- `12-related-rock-areas-api-integrations-lava-cms-security-media-mobile-api-integrations`: API Integrations
- `12-related-rock-areas-api-integrations-lava-cms-security-media-mobile-lava`: Lava
- `14-developer-api-lava-and-source-code-landmarks`: 14. Developer, API, Lava, And Source-Code Landmarks
- `15-reporting-analytics-and-model-map`: 15. Reporting, Analytics, And Model Map
- `16-version-and-release-caveats`: 16. Version And Release Caveats
- `17-implementation-playbooks-playbook-campus-selection`: Playbook: Campus Selection
- `18-troubleshooting-decision-tree-app-does-not-launch-or-shows-wrong-content`: App Does Not Launch Or Shows Wrong Content
- `18-troubleshooting-decision-tree-page-is-blank`: Page Is Blank
- `18-troubleshooting-decision-tree-roku-focus-does-not-move`: Roku Focus Does Not Move
- `19-agent-task-recipes-recipe-trace-a-page-guid`: Recipe: Trace A Page GUID
- `19-agent-task-recipes-recipe-validate-remote-auth-in-data`: Recipe: Validate Remote Auth In Data
- `19-agent-task-recipes-recipe-decide-cache-policy`: Recipe: Decide Cache Policy

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
