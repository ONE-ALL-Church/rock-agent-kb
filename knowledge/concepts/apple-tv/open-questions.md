---
concept_id: apple-tv
title: Apple TV Apps Open Questions
generated: true
---

# Apple TV Apps Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only


## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `mental-model`: Mental Model
- `creating-and-configuring-an-application`: Creating And Configuring An Application
- `pages-lava-and-cache-behavior-page-content-and-merge-fields`: Page content and merge fields
- `pages-lava-and-cache-behavior-creating-page-content`: Creating page content
- `pages-lava-and-cache-behavior-cacheability`: Cacheability
- `sign-in-logout-and-remote-authentication-tv-side-login-flow`: TV-side login flow
- `sign-in-logout-and-remote-authentication-logout-and-navigation-state`: Logout and navigation state
- `javascript-and-rock-commands`: JavaScript And Rock Commands
- `templates-and-rock-specific-controls-choosing-a-tvml-template`: Choosing a TVML template
- `styling-themes-and-text-tvml-styling-model`: TVML styling model
- `styling-themes-and-text-light-and-dark-themes`: Light and dark themes
- `application-images-top-shelf-images`: Top Shelf images
- `testing-and-demo-mode`: Testing And Demo Mode
- `lava-apis-and-security`: Lava APIs And Security
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-the-application-or-start-screen-does-not-load`: The application or Start Screen does not load
- `troubleshooting-decision-tree-a-page-is-blank-malformed-or-rejected`: A page is blank, malformed, or rejected
- `troubleshooting-decision-tree-login-shows-no-qr-code-or-manual-code`: Login shows no QR code or manual code
- `troubleshooting-decision-tree-back-navigation-exposes-the-pre-login-or-personalized-page-unexpectedly`: Back navigation exposes the pre-login or personalized page unexpectedly
- `troubleshooting-decision-tree-video-or-audio-does-not-play`: Video or audio does not play
- `troubleshooting-decision-tree-playback-resumes-incorrectly-or-creates-duplicate-interactions`: Playback resumes incorrectly or creates duplicate interactions
- `troubleshooting-decision-tree-colors-or-badges-disappear-in-one-theme`: Colors or badges disappear in one theme
- `troubleshooting-decision-tree-a-template-change-does-not-appear`: A template change does not appear
- `troubleshooting-decision-tree-demo-commands-do-not-work`: Demo commands do not work
- `troubleshooting-decision-tree-a-countdown-immediately-navigates-or-starts-media`: A countdown immediately navigates or starts media
- `troubleshooting-decision-tree-a-lava-webhook-exposes-more-data-than-expected`: A Lava webhook exposes more data than expected
- `agent-task-recipes-recipe-create-a-minimal-rock-apple-tv-application`: Recipe: Create a minimal Rock Apple TV application
- `agent-task-recipes-recipe-add-a-cache-aware-tvml-page`: Recipe: Add a cache-aware TVML page
- `agent-task-recipes-recipe-implement-remote-sign-in`: Recipe: Implement remote sign-in
- `agent-task-recipes-recipe-add-tracked-video-or-audio-playback`: Recipe: Add tracked video or audio playback
- `agent-task-recipes-recipe-build-a-theme-safe-styling-pass`: Recipe: Build a theme-safe styling pass
- `agent-task-recipes-recipe-prepare-the-application-image-package`: Recipe: Prepare the application image package
- `agent-task-recipes-recipe-test-through-demo-mode`: Recipe: Test through demo mode
- `agent-task-recipes-recipe-review-a-lava-api-before-connecting-it-to-apple-tv`: Recipe: Review a Lava API before connecting it to Apple TV
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `source-map`: Source Map

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
