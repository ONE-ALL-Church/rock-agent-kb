---
concept_id: mobile
title: Rock Mobile Open Questions
generated: true
---

# Rock Mobile Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `13-developer-api-lava-and-source-code-landmarks-xaml-and-lava`: XAML And Lava
- `19-source-map-and-dependency-notes-community-examples`: Community Examples

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-rock-mobile-mental-model-deployment-flow`: Deployment Flow
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-creating-the-mobile-application`: Creating The Mobile Application
- `5-core-configuration-and-data-model-application-type`: Application Type
- `5-core-configuration-and-data-model-lock-orientation`: Lock Orientation
- `5-core-configuration-and-data-model-application-pages`: Application Pages
- `5-core-configuration-and-data-model-api-key`: API Key
- `5-core-configuration-and-data-model-flyout-xaml`: Flyout XAML
- `5-core-configuration-and-data-model-homepage-routing-logic`: Homepage Routing Logic
- `5-core-configuration-and-data-model-palette-colors-and-styling-values`: Palette Colors And Styling Values
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `6-primary-entities-and-relationships-mobile-application-relationship-map`: Mobile Application Relationship Map
- `6-primary-entities-and-relationships-page-block-and-security-relationships`: Page, Block, And Security Relationships
- `6-primary-entities-and-relationships-check-in-source-code-landmarks`: Check-In Source-Code Landmarks
- `7-common-rock-mobile-workflows-build-a-first-app`: Build A First App
- `7-common-rock-mobile-workflows-change-a-page-or-block`: Change A Page Or Block
- `7-common-rock-mobile-workflows-add-a-webview-integration`: Add A WebView Integration
- `7-common-rock-mobile-workflows-configure-push-notifications`: Configure Push Notifications
- `7-common-rock-mobile-workflows-upgrade-from-xamarin-forms-to-maui`: Upgrade From Xamarin Forms To MAUI
- `8-commands-deep-dive-command-binding-pattern`: Command Binding Pattern
- `8-commands-deep-dive-commandreference`: CommandReference
- `8-commands-deep-dive-operational-command-troubleshooting`: Operational Command Troubleshooting
- `9-controls-deep-dive-webview`: WebView
- `9-controls-deep-dive-context-menu`: Context Menu
- `9-controls-deep-dive-ondeviceplatform-and-maui-platform-support`: OnDevicePlatform And MAUI Platform Support
- `9-controls-deep-dive-cards-and-styling`: Cards And Styling
- `9-controls-deep-dive-media-controls`: Media Controls
- `10-mobile-releases-deep-dive-release-version-table`: Release Version Table
- `10-mobile-releases-deep-dive-v7-0`: v7.0
- `10-mobile-releases-deep-dive-v6-0`: v6.0
- `11-related-rock-areas-api-check-in-cms-security-api`: API
- `11-related-rock-areas-api-check-in-cms-security-check-in`: Check-In
- `12-administration-and-operational-guardrails-deployment-guardrails`: Deployment Guardrails
- `12-administration-and-operational-guardrails-shell-update-guardrails`: Shell Update Guardrails
- `12-administration-and-operational-guardrails-app-store-guardrails`: App Store Guardrails
- `12-administration-and-operational-guardrails-android-keystore-guardrails`: Android Keystore Guardrails
- `12-administration-and-operational-guardrails-in-app-giving-guardrails`: In-App Giving Guardrails

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
