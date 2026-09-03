---
concept_id: content-personalization
title: Content And Personalization Open Questions
generated: true
---

# Content And Personalization Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `known-gaps-and-live-verification`: Known Gaps And Live Verification (226 words)

## Community-Supported Only


## Needs Live Verification

- `scope-and-boundaries`: Scope And Boundaries
- `content-channels-manage-editorial-work`: Manage editorial work
- `content-channels-relate-items`: Relate items
- `content-channels-automate-item-attributes`: Automate item attributes
- `social-metadata`: Social Metadata
- `localization`: Localization
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-content-item-does-not-appear`: A content item does not appear
- `troubleshooting-decision-tree-content-collection-results-are-stale-or-empty`: Content Collection results are stale or empty
- `troubleshooting-decision-tree-personalized-content-is-wrong-or-stale`: Personalized content is wrong or stale
- `troubleshooting-decision-tree-one-visitor-sees-another-visitor-s-personalized-values`: One visitor sees another visitor’s personalized values
- `troubleshooting-decision-tree-an-adaptive-message-adaptation-does-not-display`: An Adaptive Message adaptation does not display
- `troubleshooting-decision-tree-an-externally-uploaded-asset-is-missing`: An externally uploaded asset is missing
- `troubleshooting-decision-tree-media-analytics-or-resume-behavior-is-unexpected`: Media analytics or resume behavior is unexpected
- `troubleshooting-decision-tree-a-required-media-watch-form-cannot-be-submitted`: A required Media Watch form cannot be submitted
- `troubleshooting-decision-tree-a-social-share-preview-is-wrong`: A social share preview is wrong
- `troubleshooting-decision-tree-dates-phone-numbers-currency-or-addresses-appear-incorrectly-localized`: Dates, phone numbers, currency, or addresses appear incorrectly localized
- `agent-task-recipes-recipe-publish-a-governed-content-channel-item`: Recipe: Publish a governed Content Channel Item
- `agent-task-recipes-recipe-add-personalization-to-content-channel-items`: Recipe: Add personalization to Content Channel Items
- `agent-task-recipes-recipe-refresh-personalization-membership`: Recipe: Refresh personalization membership
- `agent-task-recipes-recipe-build-and-refresh-a-content-collection`: Recipe: Build and refresh a Content Collection
- `agent-task-recipes-recipe-configure-a-content-component-template`: Recipe: Configure a Content Component template
- `agent-task-recipes-recipe-automate-a-channel-item-attribute-with-lava`: Recipe: Automate a channel item attribute with Lava
- `agent-task-recipes-recipe-publish-a-media-element-through-a-channel`: Recipe: Publish a Media Element through a channel
- `agent-task-recipes-recipe-configure-localized-currency-display-safely`: Recipe: Configure localized currency display safely

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
