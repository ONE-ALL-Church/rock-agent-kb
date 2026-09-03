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

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `mental-model`: Mental Model
- `apple-tv-application-configuration`: Application configuration
- `apple-tv-pages-and-lava-output`: Pages and Lava output
- `apple-tv-commands`: Commands
- `roku-application-configuration`: Application configuration
- `security-and-authentication-remote-authentication-architecture`: Remote authentication architecture
- `security-and-authentication-source-code-observation`: Source-code observation
- `security-and-authentication-api-and-webhook-boundary`: API and webhook boundary
- `styling-and-controls-roku-controls-focus-and-layout`: Roku controls, focus, and layout
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-the-tv-application-administration-feature-is-missing`: The TV application administration feature is missing
- `troubleshooting-decision-tree-a-page-is-blank-rejected-or-never-appears`: A page is blank, rejected, or never appears
- `troubleshooting-decision-tree-a-roku-page-marked-show-in-menu-is-absent`: A Roku page marked “Show in Menu” is absent
- `troubleshooting-decision-tree-roku-focus-does-not-move-or-starts-on-the-wrong-item`: Roku focus does not move or starts on the wrong item
- `troubleshooting-decision-tree-a-command-does-nothing`: A command does nothing
- `troubleshooting-decision-tree-remote-sign-in-shows-no-qr-code-or-code`: Remote sign-in shows no QR code or code
- `troubleshooting-decision-tree-a-remote-authentication-code-is-rejected`: A remote-authentication code is rejected
- `troubleshooting-decision-tree-media-does-not-start`: Media does not start
- `troubleshooting-decision-tree-playback-starts-at-the-wrong-position-or-creates-a-new-interaction`: Playback starts at the wrong position or creates a new interaction
- `troubleshooting-decision-tree-a-page-shows-stale-or-another-context-s-content`: A page shows stale or another context’s content
- `agent-task-recipes-recipe-create-an-apple-tv-application-skeleton`: Recipe: Create an Apple TV application skeleton
- `agent-task-recipes-recipe-build-a-roku-content-page`: Recipe: Build a Roku content page
- `agent-task-recipes-recipe-add-roku-navigation-with-application-context`: Recipe: Add Roku navigation with application context
- `agent-task-recipes-recipe-configure-remote-tv-sign-in`: Recipe: Configure remote TV sign-in
- `agent-task-recipes-recipe-add-tracked-media-playback-with-resume`: Recipe: Add tracked media playback with resume
- `agent-task-recipes-recipe-make-an-apple-tv-page-theme-aware`: Recipe: Make an Apple TV page theme-aware
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
