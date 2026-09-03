---
concept_id: prayer-care
title: Prayer And Care Agent Cheatsheet
generated: true
---

# Prayer And Care Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Configure moderated public prayer intake](tasks/recipe-configure-moderated-public-prayer-intake.md) | `Page`, `Block`, `Attribute` | `Page`, `Block`, `Attribute` |
| [Recipe: Operate the administrator moderation queue](tasks/recipe-operate-the-administrator-moderation-queue.md) |  |  |
| [Recipe: Build a secured ministry-specific prayer queue](tasks/recipe-build-a-secured-ministry-specific-prayer-queue.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Create and verify a group prayer route](tasks/recipe-create-and-verify-a-group-prayer-route.md) | `Group`, `Page` | `Group`, `Page` |
| [Recipe: Enable prayer-comment digests](tasks/recipe-enable-prayer-comment-digests.md) | `Person`, `Schedule` | `Person`, `Schedule` |
| [Recipe: Add workflow-based care follow-up](tasks/recipe-add-workflow-based-care-follow-up.md) | `Person`, `Workflow`, `Block`, `Attribute` | `Person`, `Workflow`, `Block`, `Attribute` |
| [Recipe: Introduce AI assistance with human review](tasks/recipe-introduce-ai-assistance-with-human-review.md) | `Block` | `Block` |
| [Recipe: Validate Outreach Toolbox for prayer touchpoints](tasks/recipe-validate-outreach-toolbox-for-prayer-touchpoints.md) | `Device`, `Page`, `Group`, `Block` | `Device`, `Page`, `Group`, `Block` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.0` | core | Fixed an issue where Prayer Request Attributes not marked as "Public" were incorrectly displaying in the Obsidian version of the Prayer Request Entry block. These Attributes are now properly hidden on the Prayer Request Entry block. Fixes:  |
| `19.3` | core | Fixed the Prayer Comment List block: custom grid columns can now access the prayer request and requester via the Row Lava merge field, the From-column and date-range filters work, and several performance and dead-code issues were resolved.  |
| `19.1` | core | Improved the Prayer Request List block to display prayer request text at a wider width for better readability. Fixes: #6824 |
| `17.5` | core | Fixed an issue where approving a Prayer Request in the Obsidian Prayer Request Detail block did not update the ApprovedOnDateTime and ApprovedByPersonAliasId fields. Fixes: #6403 |
| `17.2` | core | Fixed an issue where the Prayer Request Detail block in Obsidian did not recognize the PersonId URL parameter, which prevented person data from being pre-filled when creating a new prayer request. Fixes: #6357 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `prayer-request-intake-and-lifecycle` | high | live verification |
| `categories-visibility-and-page-security` | high | live verification |
| `teams-approval-and-human-moderation` | normal | live verification |
| `ai-assisted-processing-and-moderation` | normal | live verification |
| `prayer-sessions-and-prayer-card-view` | normal | live verification |
| `group-specific-prayer-requests` | normal | live verification |
| `comments-communications-and-follow-up` | normal | live verification |
| `community-implementation-patterns` | community-supported | community-supported |
| `troubleshooting-decision-tree-a-submitted-request-does-not-appear-for-the-prayer-team` | normal | live verification |
| `troubleshooting-decision-tree-a-sensitive-request-is-still-visible` | normal | live verification |
| `troubleshooting-decision-tree-prayer-team-members-cannot-add-comments` | normal | live verification |
| `troubleshooting-decision-tree-prayer-comment-digests-are-not-being-delivered` | normal | live verification |
| `troubleshooting-decision-tree-a-group-prayer-page-is-empty-or-shows-the-wrong-scope` | normal | live verification |
| `troubleshooting-decision-tree-ai-processing-is-inconsistent-across-categories` | normal | live verification |
| `troubleshooting-decision-tree-outreach-reminders-do-not-arrive` | citation-only | live verification |
| `agent-task-recipes-recipe-configure-moderated-public-prayer-intake` | normal | live verification |
| `agent-task-recipes-recipe-operate-the-administrator-moderation-queue` | normal | live verification |
| `agent-task-recipes-recipe-build-a-secured-ministry-specific-prayer-queue` | normal | live verification |
| `agent-task-recipes-recipe-create-and-verify-a-group-prayer-route` | normal | live verification |
| `agent-task-recipes-recipe-enable-prayer-comment-digests` | normal | live verification |
| `agent-task-recipes-recipe-add-workflow-based-care-follow-up` | normal | live verification |
| `agent-task-recipes-recipe-introduce-ai-assistance-with-human-review` | normal | live verification |
| `agent-task-recipes-recipe-validate-outreach-toolbox-for-prayer-touchpoints` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-community-examples` | community-supported | community-supported |
