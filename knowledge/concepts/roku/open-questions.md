---
concept_id: roku
title: Roku Apps Open Questions
generated: true
---

# Roku Apps Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `known-gaps-and-live-verification`: Known Gaps And Live Verification (269 words)

## Community-Supported Only


## Needs Live Verification

- `agent-summary`: Agent Summary
- `getting-started-and-application-configuration`: Getting Started And Application Configuration
- `page-authoring-and-caching`: Page Authoring And Caching
- `roku-command-model`: Roku Command Model
- `application-context-commands`: Application Context Commands
- `remote-authentication-and-personal-commands`: Remote Authentication And Personal Commands
- `media-playback-and-watch-progress`: Media Playback And Watch Progress
- `layout-nodes-and-rowlist`: Layout Nodes And RowList
- `security-and-api-guardrails`: Security And API Guardrails
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-the-roku-application-cannot-connect-to-rock`: The Roku application cannot connect to Rock
- `troubleshooting-decision-tree-a-page-is-blank-or-does-not-render-as-expected`: A page is blank or does not render as expected
- `troubleshooting-decision-tree-selecting-a-button-or-content-item-does-nothing`: Selecting a button or content item does nothing
- `troubleshooting-decision-tree-back-navigation-returns-to-the-wrong-screen`: Back navigation returns to the wrong screen
- `troubleshooting-decision-tree-personalized-content-is-stale-or-appears-for-the-wrong-person`: Personalized content is stale or appears for the wrong person
- `troubleshooting-decision-tree-the-qr-login-flow-does-not-complete`: The QR login flow does not complete
- `troubleshooting-decision-tree-video-or-audio-does-not-play`: Video or audio does not play
- `troubleshooting-decision-tree-playback-resumes-but-creates-a-new-interaction`: Playback resumes but creates a new interaction
- `troubleshooting-decision-tree-a-rowlist-has-no-rows-or-items`: A RowList has no rows or items
- `agent-task-recipes-recipe-prepare-a-roku-development-readiness-review`: Recipe: Prepare A Roku Development Readiness Review
- `agent-task-recipes-recipe-author-a-focusable-roku-page-skeleton`: Recipe: Author A Focusable Roku Page Skeleton
- `agent-task-recipes-recipe-build-and-validate-a-navigation-action`: Recipe: Build And Validate A Navigation Action
- `agent-task-recipes-recipe-add-campus-or-other-application-context`: Recipe: Add Campus Or Other Application Context
- `agent-task-recipes-recipe-configure-a-remote-login-journey`: Recipe: Configure A Remote Login Journey
- `agent-task-recipes-recipe-configure-resumable-media-playback`: Recipe: Configure Resumable Media Playback
- `agent-task-recipes-recipe-review-a-roku-related-lava-endpoint`: Recipe: Review A Roku-Related Lava Endpoint

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
