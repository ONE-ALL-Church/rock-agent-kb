---
concept_id: workflows
title: Workflows Agent Cheatsheet
generated: true
---

# Workflows Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Design a bounded workflow type](tasks/recipe-design-a-bounded-workflow-type.md) | `Person`, `Label`, `Workflow`, `Attribute` | `Person`, `Label`, `Workflow`, `Attribute` |
| [Recipe: Review a workflow form change](tasks/recipe-review-a-workflow-form-change.md) | `Person`, `Workflow`, `Attribute` | `Person`, `Workflow`, `Attribute` |
| [Recipe: Configure a selective workflow webhook](tasks/recipe-configure-a-selective-workflow-webhook.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Diagnose an active workflow instance](tasks/recipe-diagnose-an-active-workflow-instance.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Audit a connection follow-up process](tasks/recipe-audit-a-connection-follow-up-process.md) | `Person`, `Campus`, `Workflow` | `Person`, `Campus`, `Workflow` |
| [Recipe: Import or adapt a workflow safely](tasks/recipe-import-or-adapt-a-workflow-safely.md) | `Group`, `Campus`, `Workflow`, `Page`, `Attribute` | `Group`, `Campus`, `Workflow`, `Page`, `Attribute` |
| [Recipe: Design background orchestration](tasks/recipe-design-background-orchestration.md) | `Page`, `Block` | `Page`, `Block` |

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
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `agent-summary` | normal | live verification |
| `mental-model` | normal | live verification |
| `triggers-and-activation-entry-pages-and-direct-links` | normal | live verification |
| `triggers-and-activation-lava-workflowactivate` | normal | live verification |
| `workflow-forms-chained-forms-and-branching` | normal | live verification |
| `workflow-forms-form-builder` | normal | live verification |
| `workflow-forms-person-and-family-entry-patterns` | community-supported | live verification |
| `workflow-integrations-lava-entity-operations` | community-supported | live verification |
| `managing-workflow-instances-and-staff-work` | normal | live verification |
| `connections-as-operational-workflows` | citation-only | live verification |
| `adjacent-operational-patterns` | community-supported | community-supported |
| `security-and-governance` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-or-form-is-not-visible` | normal | live verification |
| `troubleshooting-decision-tree-a-form-field-is-missing-unexpectedly-required-or-exposing-data` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-action-was-skipped` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-is-stuck-or-repeatedly-processing` | normal | live verification |
| `troubleshooting-decision-tree-a-webhook-returns-404-or-launches-the-wrong-number-of-workflows` | normal | live verification |
| `troubleshooting-decision-tree-workflowactivate-starts-a-workflow-but-values-are-blank` | community-supported | live verification |
| `troubleshooting-decision-tree-a-connection-request-is-missing-from-a-board-or-list` | citation-only | live verification |
| `troubleshooting-decision-tree-sql-or-reporting-cannot-see-a-value-just-submitted-by-a-form` | normal | live verification |
| `troubleshooting-decision-tree-lava-output-is-blank-or-a-parser-error-points-at-the-wrong-line` | normal | live verification |
| `agent-task-recipes-recipe-design-a-bounded-workflow-type` | normal | live verification |
| `agent-task-recipes-recipe-review-a-workflow-form-change` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-selective-workflow-webhook` | normal | live verification |
| `agent-task-recipes-recipe-diagnose-an-active-workflow-instance` | normal | live verification |
| `agent-task-recipes-recipe-audit-a-connection-follow-up-process` | citation-only | live verification |
| `agent-task-recipes-recipe-import-or-adapt-a-workflow-safely` | normal | live verification |
| `agent-task-recipes-recipe-design-background-orchestration` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-community-examples-and-reviewed-patterns` | community-supported | community-supported |
| `approved-media-coverage` | community-supported | community-supported |
