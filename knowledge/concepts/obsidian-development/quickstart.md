---
concept_id: obsidian-development
title: Obsidian Development Quickstart
generated: true
---

# Obsidian Development Quickstart

Obsidian block development, grid reference, custom actions, field types, browser bus, TypeScript patterns, development environment, and migration from WebForms blocks.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Implement A Secure Block Action](tasks/recipe-implement-a-secure-block-action.md): A server action that accepts client data without trusting client state.
- [Recipe: Scaffold And Harden A Detail Block](tasks/recipe-scaffold-and-harden-a-detail-block.md): A standardized detail block with an explicit write boundary.
- [Recipe: Build A Grid With Reliable Actions](tasks/recipe-build-a-grid-with-reliable-actions.md): A grid whose filters, exports, and actions operate on the intended rows.
- [Recipe: Add A Core Field Type To Obsidian](tasks/recipe-add-a-core-field-type-to-obsidian.md): A registered core field type with compatible server and client representations.
- [Recipe: Create A Universal Plugin Picker](tasks/recipe-create-a-universal-plugin-picker.md): A plugin field type whose C# implementation supplies structured picker data without owning UI code.
- [Recipe: Add A Custom Block Settings Screen](tasks/recipe-add-a-custom-block-settings-screen.md): An administrate-only `.obs` settings interface backed by block actions.
- [Recipe: Coordinate Same-Page Blocks With Browser Bus](tasks/recipe-coordinate-same-page-blocks-with-browser-bus.md): One block reacts to an event from another block on the same page.
- [Recipe: Cache A Read Request](tasks/recipe-cache-a-read-request.md): Concurrent callers share one in-flight request and reuse its result for a bounded period.
- [Recipe: Verify A Community-Suggested Block-Action Save Path](tasks/recipe-verify-a-community-suggested-block-action-save-path.md): A proposed operational save path is evaluated without treating one organization’s experience as universal Rock behavior.

## High-Signal Sections

- `agent-summary` lines 34-46: Agent Summary (normal)
- `scope-and-boundaries` lines 47-60: Scope And Boundaries (normal)
- `mental-model` lines 61-74: Mental Model (normal)
- `blocks-block-initialization-and-actions` lines 77-91: Block Initialization And Actions (normal)
- `blocks-list-blocks` lines 92-97: List Blocks (normal)
- `blocks-detail-blocks-and-webforms-migration` lines 98-110: Detail Blocks And WebForms Migration (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the obsidian-development guide.
- `Block`: Rock concept/entity referenced by the obsidian-development guide.
- `DataView`: Rock concept/entity referenced by the obsidian-development guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the obsidian-development guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the obsidian-development guide.
- `Person`: Rock concept/entity referenced by the obsidian-development guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the obsidian-development guide.

## Version Caveats

- `18.1`: Fixed editing configuration settings of Universal field types from inside an Obsidian block. This only affected some configuration setting types which might cause the raw value to be stored as JSON.
- `16.1`: Fixed issue of Note Type Field Type not showing up in Following Event Type Detail Obsidian block. Fixes: #5605
- `17.1`: Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface.
- `19.1`: Fixed an issue where the Obsidian Workflow List block would time out when loading workflows assigned to groups with many members.
- `18.3`: Fixed an issue in Obsidian blocks where Memo Fields configured to allow HTML displayed the HTML tags as encoded text instead of rendering the formatted content within the block. Fixes: #6718
- `18.3`: Fixed an issue in the Defined Value picker component where Single-Select Defined Value attributes configured with "Enhanced for Long Lists" did not display the searchable enhanced experience in Obsidian blocks (e.g., Wor
- `18.3`: Fixed an issue in the Obsidian Location Detail block that allowed a Location to be saved with itself (or a child Location) as its parent. This caused the Location tree to fail when loading nested Locations. Fixes: #6669
- `18.3`: Fixed an issue in the Obsidian Group Requirement Type Detail block that caused Attribute Values to not load or save correctly when editing a requirement type. This prevented individuals from configuring or updating Group

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
