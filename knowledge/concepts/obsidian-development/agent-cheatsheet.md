---
concept_id: obsidian-development
title: Obsidian Development Agent Cheatsheet
generated: true
---

# Obsidian Development Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Implement A Secure Block Action](tasks/recipe-implement-a-secure-block-action.md) | `Person`, `Block` | `Person`, `Block` |
| [Recipe: Scaffold And Harden A Detail Block](tasks/recipe-scaffold-and-harden-a-detail-block.md) | `Page`, `Block`, `Attribute` | `Page`, `Block`, `Attribute` |
| [Recipe: Build A Grid With Reliable Actions](tasks/recipe-build-a-grid-with-reliable-actions.md) | `Person`, `Page`, `Attribute` | `Person`, `Page`, `Attribute` |
| [Recipe: Add A Core Field Type To Obsidian](tasks/recipe-add-a-core-field-type-to-obsidian.md) | `Workflow`, `Block`, `Attribute` | `Workflow`, `Block`, `Attribute` |
| [Recipe: Create A Universal Plugin Picker](tasks/recipe-create-a-universal-plugin-picker.md) | `DataView` | `DataView` |
| [Recipe: Add A Custom Block Settings Screen](tasks/recipe-add-a-custom-block-settings-screen.md) | `Block` | `Block` |
| [Recipe: Coordinate Same-Page Blocks With Browser Bus](tasks/recipe-coordinate-same-page-blocks-with-browser-bus.md) | `Page`, `Block`, `Attribute` | `Page`, `Block`, `Attribute` |
| [Recipe: Cache A Read Request](tasks/recipe-cache-a-read-request.md) |  |  |
| [Recipe: Verify A Community-Suggested Block-Action Save Path](tasks/recipe-verify-a-community-suggested-block-action-save-path.md) | `Group`, `Location`, `Schedule`, `Workflow`, `Block`, `Person` | `Group`, `Location`, `Schedule`, `Workflow`, `Block`, `Person` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Fixed editing configuration settings of Universal field types from inside an Obsidian block. This only affected some configuration setting types which might cause the raw value to be stored as JSON. |
| `16.1` | core | Fixed issue of Note Type Field Type not showing up in Following Event Type Detail Obsidian block. Fixes: #5605 |
| `17.1` | core | Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface. |
| `19.1` | core | Fixed an issue where the Obsidian Workflow List block would time out when loading workflows assigned to groups with many members. |
| `18.3` | core | Fixed an issue in Obsidian blocks where Memo Fields configured to allow HTML displayed the HTML tags as encoded text instead of rendering the formatted content within the block. Fixes: #6718 |
| `18.3` | core | Fixed an issue in the Defined Value picker component where Single-Select Defined Value attributes configured with "Enhanced for Long Lists" did not display the searchable enhanced experience in Obsidian blocks (e.g., Workflow Entry and Even |
| `18.3` | core | Fixed an issue in the Obsidian Location Detail block that allowed a Location to be saved with itself (or a child Location) as its parent. This caused the Location tree to fail when loading nested Locations. Fixes: #6669 |
| `18.3` | core | Fixed an issue in the Obsidian Group Requirement Type Detail block that caused Attribute Values to not load or save correctly when editing a requirement type. This prevented individuals from configuring or updating Group Requirement Types a |
| `18.3` | core | Fixed an issue where the Obsidian Group Attendance Detail Block did not function correctly when Predictive Ids were disabled. The block now correctly resolves the selected group using either the Group Guid or IdKey and prevents an unintende |
| `18.2` | core | Fixed a display issue in the Obsidian Signature Document List block, affecting the Document column. Fixes: #6552 |
| `18.2` | core | Fixed an issue where newly added Obsidian block types could fail to appear in the Page Zone Editor after initial startup. |
| `18.1` | core | Added an Obsidian Communication Detail block with improved message visualization and Communication Recipient insights, allowing administrators to review communication content, delivery status, and recipient activity more efficiently. |
| `18.1` | core | Added an Obsidian Communication List block with enhanced status display and optimized data loading, making it easier for administrators to quickly identify message progress and issues. |
| `18.1` | core | Updated the Obsidian Communication List block to disable custom columns, which are not supported by the high-performance query used by this block. Fixes: #6515 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `components-forms-and-typescript-contracts` | normal | live verification |
| `grid-reference-labels-and-number-badges` | normal | live verification |
| `grid-reference-attribute-person-and-rock-field-columns` | normal | live verification |
| `field-types-core-field-type-conversion` | normal | live verification |
| `development-environment-plugin-development` | normal | live verification |
| `development-environment-debugging` | normal | live verification |
| `troubleshooting-decision-tree-a-save-reports-success-but-the-intended-values-do-not-persist` | normal | live verification |
| `troubleshooting-decision-tree-a-grid-is-slow-even-with-a-small-page-size` | normal | live verification |
| `troubleshooting-decision-tree-a-picker-can-be-cleared-or-submitted-unexpectedly` | normal | live verification |
| `troubleshooting-decision-tree-an-older-component-fails-with-syntaxerror-15` | normal | live verification |
| `agent-task-recipes-recipe-implement-a-secure-block-action` | normal | live verification |
| `agent-task-recipes-recipe-scaffold-and-harden-a-detail-block` | normal | live verification |
| `agent-task-recipes-recipe-build-a-grid-with-reliable-actions` | normal | live verification |
| `agent-task-recipes-recipe-add-a-core-field-type-to-obsidian` | normal | live verification |
| `agent-task-recipes-recipe-create-a-universal-plugin-picker` | normal | live verification |
| `agent-task-recipes-recipe-coordinate-same-page-blocks-with-browser-bus` | normal | live verification |
| `agent-task-recipes-recipe-cache-a-read-request` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
