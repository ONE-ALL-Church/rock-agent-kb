---
concept_id: groups
title: Groups Agent Cheatsheet
generated: true
---

# Groups Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Design a Group Type and hierarchy](tasks/recipe-design-a-group-type-and-hierarchy.md) | `Attendance`, `Group`, `GroupType`, `Location`, `Schedule`, `Attribute` | `Attendance`, `Group`, `GroupType`, `Location`, `Schedule`, `Attribute` |
| [Recipe: Publish a group through Group Finder](tasks/recipe-publish-a-group-through-group-finder.md) | `Group`, `GroupType`, `Location`, `Schedule`, `Page`, `Block`, `Campus`, `Attribute` | `Group`, `GroupType`, `Location`, `Schedule`, `Page`, `Block`, `Campus`, `Attribute` |
| [Recipe: Configure focused attendance entry](tasks/recipe-configure-focused-attendance-entry.md) | `Attendance`, `Group`, `Location`, `Schedule`, `Family`, `Workflow`, `Page`, `Block` | `Attendance`, `Group`, `Location`, `Schedule`, `Family`, `Workflow`, `Page`, `Block` |
| [Recipe: Configure attendance follow-up](tasks/recipe-configure-attendance-follow-up.md) | `Attendance`, `Group`, `GroupType`, `Schedule`, `Attribute` | `Attendance`, `Group`, `GroupType`, `Schedule`, `Attribute` |
| [Recipe: Enforce a Group Type requirement](tasks/recipe-enforce-a-group-type-requirement.md) | `DataView`, `Group`, `GroupType`, `Workflow`, `Block` | `DataView`, `Group`, `GroupType`, `Workflow`, `Block` |
| [Recipe: Synchronize a group from a Data View](tasks/recipe-synchronize-a-group-from-a-data-view.md) | `DataView`, `Group`, `GroupType`, `Workflow`, `Attribute` | `DataView`, `Group`, `GroupType`, `Workflow`, `Attribute` |
| [Recipe: Secure leader operations](tasks/recipe-secure-leader-operations.md) | `Attendance`, `Group`, `GroupType`, `Page`, `Block` | `Attendance`, `Group`, `GroupType`, `Page`, `Block` |
| [Recipe: Enable history and archive a group](tasks/recipe-enable-history-and-archive-a-group.md) | `Group`, `GroupType`, `Workflow` | `Group`, `GroupType`, `Workflow` |
| [Recipe: Move group members safely](tasks/recipe-move-group-members-safely.md) | `Person`, `Group`, `Label`, `Workflow`, `Attribute`, `DataView`, `GroupType` | `Person`, `Group`, `Label`, `Workflow`, `Attribute`, `DataView`, `GroupType` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `mental-model` | high | live verification |
| `creating-editing-inactivating-and-archiving-groups` | normal | live verification |
| `members-roles-statuses-and-attributes` | normal | live verification |
| `group-security-and-leader-operations` | normal | live verification |
| `locations-and-schedules` | high | live verification |
| `group-finder` | normal | live verification |
| `group-attendance-entry` | community-supported | live verification |
| `group-sync-and-communication-lists` | normal | live verification |
| `groups-in-workflows-training-and-reporting` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-add-child-to-selected-is-disabled` | normal | live verification |
| `troubleshooting-decision-tree-a-group-is-missing-from-group-finder` | normal | live verification |
| `troubleshooting-decision-tree-the-day-or-time-filter-does-not-return-a-group` | normal | live verification |
| `troubleshooting-decision-tree-a-leader-cannot-add-a-member-from-group-toolbox` | normal | live verification |
| `troubleshooting-decision-tree-attendance-reminders-are-not-sent` | normal | live verification |
| `troubleshooting-decision-tree-the-absence-notification-job-fails-or-evaluates-the-wrong-people` | normal | live verification |
| `troubleshooting-decision-tree-a-synced-group-or-communication-list-has-unexpected-members` | normal | live verification |
| `troubleshooting-decision-tree-member-attributes-disappeared-after-a-move` | normal | live verification |
| `troubleshooting-decision-tree-a-location-or-schedule-link-is-wrong-after-api-work` | normal | live verification |
| `troubleshooting-decision-tree-a-failed-workflow-may-have-partially-changed-group-data` | community-supported | live verification |
| `agent-task-recipes-recipe-design-a-group-type-and-hierarchy` | normal | live verification |
| `agent-task-recipes-recipe-publish-a-group-through-group-finder` | normal | live verification |
| `agent-task-recipes-recipe-configure-focused-attendance-entry` | citation-only | live verification |
| `agent-task-recipes-recipe-configure-attendance-follow-up` | normal | live verification |
| `agent-task-recipes-recipe-enforce-a-group-type-requirement` | normal | live verification |
| `agent-task-recipes-recipe-secure-leader-operations` | normal | live verification |
| `agent-task-recipes-recipe-enable-history-and-archive-a-group` | normal | live verification |
| `agent-task-recipes-recipe-move-group-members-safely` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
