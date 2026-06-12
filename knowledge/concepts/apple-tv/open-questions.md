---
concept_id: apple-tv
title: Apple TV Apps Open Questions
generated: true
---

# Apple TV Apps Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `17-implementation-playbooks-playbook-weekend-messages-app`: Playbook: Weekend Messages App (141 words)
- `17-implementation-playbooks-playbook-campus-aware-app`: Playbook: Campus-Aware App (89 words)
- `17-implementation-playbooks-playbook-remote-login`: Playbook: Remote Login (91 words)

## Community-Supported Only


## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-apple-tv-apps-mental-model`: 3. Apple TV Apps Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-apple-tv-app-record`: Apple TV App Record
- `5-core-configuration-and-data-model-tv-page-record`: TV Page Record
- `5-core-configuration-and-data-model-page-list-block-options`: Page List Block Options
- `5-core-configuration-and-data-model-remote-authentication-data-model`: Remote Authentication Data Model
- `5-core-configuration-and-data-model-lava-endpoint-and-api-context`: Lava Endpoint And API Context
- `6-primary-entities-and-relationships-apple-tv-app-to-site`: Apple TV App To Site
- `6-primary-entities-and-relationships-apple-tv-app-to-tv-pages`: Apple TV App To TV Pages
- `6-primary-entities-and-relationships-tv-pages-to-lava-merge-fields`: TV Pages To Lava Merge Fields
- `6-primary-entities-and-relationships-tv-pages-to-commands`: TV Pages To Commands
- `7-common-apple-tv-apps-workflows-create-a-new-app`: Create A New App
- `7-common-apple-tv-apps-workflows-add-a-content-page`: Add A Content Page
- `7-common-apple-tv-apps-workflows-build-a-campus-selector`: Build A Campus Selector
- `7-common-apple-tv-apps-workflows-add-login`: Add Login
- `7-common-apple-tv-apps-workflows-play-media`: Play Media
- `8-building-your-first-apple-tv-app-deep-dive-step-1-confirm-preconditions`: Step 1: Confirm Preconditions
- `8-building-your-first-apple-tv-app-deep-dive-step-2-create-the-app`: Step 2: Create The App
- `8-building-your-first-apple-tv-app-deep-dive-step-3-create-the-start-screen`: Step 3: Create The Start Screen
- `8-building-your-first-apple-tv-app-deep-dive-step-6-add-images`: Step 6: Add Images
- `8-building-your-first-apple-tv-app-deep-dive-step-7-test-the-app`: Step 7: Test The App
- `9-apple-tv-sign-in-and-authentication-deep-dive-server-setup`: Server Setup
- `9-apple-tv-sign-in-and-authentication-deep-dive-security-guardrails`: Security Guardrails
- `10-apple-tv-javascript-commands-deep-dive-navigation-commands`: Navigation Commands
- `10-apple-tv-javascript-commands-deep-dive-media-commands`: Media Commands
- `10-apple-tv-javascript-commands-deep-dive-personal-commands`: Personal Commands
- `10-apple-tv-javascript-commands-deep-dive-utility-commands`: Utility Commands
- `10-apple-tv-javascript-commands-deep-dive-demo-commands`: Demo Commands
- `11-apple-tv-styling-deep-dive`: 11. Apple TV Styling Deep Dive
- `11-apple-tv-styling-deep-dive-style-placement`: Style Placement
- `11-apple-tv-styling-deep-dive-global-styles`: Global Styles
- `11-apple-tv-styling-deep-dive-themes-and-media-queries`: Themes And Media Queries
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-lava`: Lava
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-cms`: CMS
- `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-media`: Media
- `13-administration-and-operational-guardrails-environment-separation`: Environment Separation
- `13-administration-and-operational-guardrails-api-key-hygiene`: API Key Hygiene

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
