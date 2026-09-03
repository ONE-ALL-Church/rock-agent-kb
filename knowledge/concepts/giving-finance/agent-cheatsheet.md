---
concept_id: giving-finance
title: Giving And Finance Agent Cheatsheet
generated: true
---

# Giving And Finance Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Trace a public gift end to end](tasks/recipe-trace-a-public-gift-end-to-end.md) | `Person`, `Location`, `Page` | `Person`, `Location`, `Page` |
| [Recipe: Validate an online giving page before launch](tasks/recipe-validate-an-online-giving-page-before-launch.md) | `Schedule`, `Campus`, `Page`, `Block` | `Schedule`, `Campus`, `Page`, `Block` |
| [Recipe: Reconcile an online batch](tasks/recipe-reconcile-an-online-batch.md) | `Workflow` | `Workflow` |
| [Recipe: Generate and validate contribution statements](tasks/recipe-generate-and-validate-contribution-statements.md) | `Person`, `Family` | `Person`, `Family` |
| [Recipe: Build a detail-preserving finance report](tasks/recipe-build-a-detail-preserving-finance-report.md) | `Person`, `Group`, `Location`, `Family`, `Page` | `Person`, `Group`, `Location`, `Family`, `Page` |
| [Recipe: Transfer scheduled giving to a new gateway](tasks/recipe-transfer-scheduled-giving-to-a-new-gateway.md) | `Schedule`, `Block` | `Schedule`, `Block` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added Financial Batch Detail block to support check scanning, creation of batch, batch detail viewing, and batch modifications. Also added Financial Batch List to view available batches. |
| `18.3` | core | Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup parameter) was excl |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | normal | live verification |
| `mental-model` | normal | live verification |
| `transactions` | normal | live verification |
| `payment-gateways` | normal | live verification |
| `online-giving-and-receipts` | normal | live verification |
| `text-giving` | normal | live verification |
| `batches` | normal | live verification |
| `giving-units-businesses-and-pledges` | normal | live verification |
| `reporting-and-reconciliation` | normal | live verification |
| `security-and-administration` | normal | live verification |
| `troubleshooting-decision-tree-a-gateway-accepted-a-payment-but-no-rock-transaction-is-visible` | normal | live verification |
| `troubleshooting-decision-tree-a-transaction-is-in-the-wrong-batch-or-no-expected-batch-exists` | normal | live verification |
| `troubleshooting-decision-tree-a-statement-omits-a-gift-includes-an-unexpected-gift-or-combines-the-wrong-people` | normal | live verification |
| `troubleshooting-decision-tree-giving-overview-journey-or-alerts-appear-stale-or-incorrect` | normal | live verification |
| `troubleshooting-decision-tree-text-giving-setup-processing-refund-or-failure-messaging-does-not-work` | normal | live verification |
| `troubleshooting-decision-tree-users-can-see-finance-data-they-should-not-see-or-cannot-see-an-embedded-dashboard` | normal | live verification |
| `agent-task-recipes-recipe-trace-a-public-gift-end-to-end` | citation-only | live verification |
| `agent-task-recipes-recipe-validate-an-online-giving-page-before-launch` | normal | live verification |
| `agent-task-recipes-recipe-generate-and-validate-contribution-statements` | normal | live verification |
| `agent-task-recipes-recipe-build-a-detail-preserving-finance-report` | normal | live verification |
| `agent-task-recipes-recipe-transfer-scheduled-giving-to-a-new-gateway` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-community-example` | community-supported | community-supported |
