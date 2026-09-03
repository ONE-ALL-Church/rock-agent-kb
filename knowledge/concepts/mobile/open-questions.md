---
concept_id: mobile
title: Rock Mobile Open Questions
generated: true
---

# Rock Mobile Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (172 words)
- `version-and-authority-caveats`: Version And Authority Caveats (164 words)
- `known-gaps-and-live-verification`: Known Gaps And Live Verification (216 words)

## Community-Supported Only

- `content-xaml-and-lava-escaping-xaml-producing-lava`: Escaping XAML-producing Lava
- `troubleshooting-decision-tree-one-record-causes-a-xaml-page-to-fail`: One record causes a XAML page to fail

## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `application-configuration-and-deployment`: Application Configuration And Deployment
- `content-xaml-and-lava-dynamic-versus-static-content`: Dynamic versus static content
- `content-xaml-and-lava-escaping-xaml-producing-lava`: Escaping XAML-producing Lava
- `controls-context-menus`: Context menus
- `controls-borders-and-migration-era-controls`: Borders and migration-era controls
- `mobile-check-in-prerequisites-and-configuration`: Prerequisites and configuration
- `mobile-engagement-and-background-work`: Mobile Engagement And Background Work
- `outreach-toolbox`: Outreach Toolbox
- `push-notifications`: Push Notifications
- `app-publishing-android-signing`: Android signing
- `mobile-releases-xamarin-forms-to-net-maui`: Xamarin Forms to .NET MAUI
- `troubleshooting-decision-tree-changes-do-not-appear-in-the-app`: Changes do not appear in the app
- `troubleshooting-decision-tree-the-app-crashes-immediately-after-opening`: The app crashes immediately after opening
- `troubleshooting-decision-tree-personalized-content-is-blank-or-anonymous`: Personalized content is blank or anonymous
- `troubleshooting-decision-tree-one-record-causes-a-xaml-page-to-fail`: One record causes a XAML page to fail
- `troubleshooting-decision-tree-a-command-does-nothing`: A command does nothing
- `troubleshooting-decision-tree-a-page-layout-breaks-after-moving-to-shell-v6`: A page layout breaks after moving to Shell v6
- `troubleshooting-decision-tree-a-context-menu-works-differently-on-android`: A context menu works differently on Android
- `troubleshooting-decision-tree-push-notifications-are-not-arriving`: Push notifications are not arriving
- `troubleshooting-decision-tree-mobile-check-in-cannot-find-a-kiosk`: Mobile check-in cannot find a kiosk
- `troubleshooting-decision-tree-mobile-check-in-finds-a-kiosk-but-says-no-service-is-available`: Mobile check-in finds a kiosk but says no service is available
- `troubleshooting-decision-tree-check-in-completes-but-labels-do-not-print`: Check-in completes but labels do not print
- `troubleshooting-decision-tree-the-app-is-unavailable-on-newer-android-devices`: The app is unavailable on newer Android devices
- `troubleshooting-decision-tree-outreach-toolbox-is-missing-or-reminders-do-not-fire`: Outreach Toolbox is missing or reminders do not fire
- `agent-task-recipes-recipe-create-and-test-a-minimal-mobile-application`: Recipe: Create and test a minimal mobile application
- `agent-task-recipes-recipe-build-personalized-content-block-output-safely`: Recipe: Build personalized Content block output safely
- `agent-task-recipes-recipe-add-a-command-driven-interaction`: Recipe: Add a command-driven interaction
- `agent-task-recipes-recipe-migrate-a-page-from-shell-v5-to-v6`: Recipe: Migrate a page from Shell v5 to v6+
- `agent-task-recipes-recipe-prepare-mobile-check-in`: Recipe: Prepare mobile check-in
- `agent-task-recipes-recipe-prepare-an-app-factory-publication`: Recipe: Prepare an App Factory publication
- `agent-task-recipes-recipe-validate-push-notifications`: Recipe: Validate push notifications
- `agent-task-recipes-recipe-orchestrate-slow-media-or-content-work`: Recipe: Orchestrate slow media or content work
- `agent-task-recipes-recipe-validate-outreach-toolbox-for-ministry-use`: Recipe: Validate Outreach Toolbox for ministry use
- `source-map-official-rock-mobile-documentation`: Official Rock Mobile documentation

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
