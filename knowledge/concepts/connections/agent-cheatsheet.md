---
concept_id: connections
title: Connections Agent Cheatsheet
generated: true
---

# Connections Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Configure a new connection pipeline](tasks/recipe-configure-a-new-connection-pipeline.md) | `Group`, `Campus`, `Workflow` | `Group`, `Campus`, `Workflow` |
| [Recipe: Triage an unassigned or overdue queue](tasks/recipe-triage-an-unassigned-or-overdue-queue.md) | `Group`, `Campus` | `Group`, `Campus` |
| [Recipe: Transfer and complete a request safely](tasks/recipe-transfer-and-complete-a-request-safely.md) | `Group`, `Campus`, `Attribute` | `Group`, `Campus`, `Attribute` |
| [Recipe: Launch a connection campaign](tasks/recipe-launch-a-connection-campaign.md) | `DataView`, `Group`, `Campus`, `Family` | `DataView`, `Group`, `Campus`, `Family` |
| [Recipe: Connect preregistration to staff follow-up](tasks/recipe-connect-preregistration-to-staff-follow-up.md) | `Person`, `Step`, `Campus`, `Family`, `Workflow`, `Page`, `Attribute`, `Schedule` | `Person`, `Step`, `Campus`, `Family`, `Workflow`, `Page`, `Attribute`, `Schedule` |
| [Recipe: Validate status automation](tasks/recipe-validate-status-automation.md) | `DataView` | `DataView` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.3` | core | Fixed an issue where a workflow could not be removed from a Connection Opportunity or Connection Type after it had been triggered from a Connection Request. Fixes: #6875 |
| `18.1` | core | Improved the Connection Request Board with updates to campus filtering, connector preferences, and workflow configuration. Added new block settings to define default Connection State and Status filters. Workflows on the Connection Opportuni |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | needs-citation |
| `mental-model` | normal | live verification |
| `opportunities` | normal | live verification |
| `requests-and-statuses-state` | normal | live verification |
| `requests-and-statuses-status` | high | live verification |
| `requests-and-statuses-due-dates` | normal | live verification |
| `boards-and-lists-list-view` | normal | live verification |
| `assignment-and-follow-up` | normal | live verification |
| `placement-completion-and-transfer` | normal | live verification |
| `workflows-and-status-automation` | high | live verification |
| `connection-campaigns` | normal | live verification |
| `public-intake-and-cross-system-handoffs` | community-supported | live verification |
| `reporting-ai-and-governance` | high | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-connector-cannot-see-an-expected-request` | high | live verification |
| `troubleshooting-decision-tree-a-list-field-source-grouping-option-or-view-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-a-request-cannot-skip-to-a-later-status-or-cannot-be-completed` | normal | live verification |
| `troubleshooting-decision-tree-due-soon-or-overdue-counts-look-wrong` | normal | live verification |
| `troubleshooting-decision-tree-a-future-follow-up-request-did-not-return-to-the-active-queue` | normal | live verification |
| `troubleshooting-decision-tree-a-campaign-creates-no-requests-or-assigns-them-to-the-wrong-people` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-did-not-launch-or-a-bulk-action-affected-only-some-requests` | high | live verification |
| `troubleshooting-decision-tree-an-ai-summary-is-unavailable-or-unreliable` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-new-connection-pipeline` | normal | live verification |
| `agent-task-recipes-recipe-triage-an-unassigned-or-overdue-queue` | normal | live verification |
| `agent-task-recipes-recipe-transfer-and-complete-a-request-safely` | normal | live verification |
| `agent-task-recipes-recipe-launch-a-connection-campaign` | normal | live verification |
| `agent-task-recipes-recipe-connect-preregistration-to-staff-follow-up` | community-supported | live verification |
| `agent-task-recipes-recipe-validate-status-automation` | needs-citation | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
| `source-map-community-reviewed-guidance-and-examples` | community-supported | live verification |
