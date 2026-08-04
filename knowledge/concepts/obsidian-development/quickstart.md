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

- [Recipe: Identify The Source Files Behind A Visible Obsidian Block](tasks/recipe-identify-the-source-files-behind-a-visible-obsidian-block.md): Start from the live block type and follow the conventions documented in the Obsidian developer documentation and Grid Columns. Confirm paths against the exact source revision because core, generated view-model, and plugin layouts can differ by version.
- [Recipe: Determine Whether A Bug Is Version-Related](tasks/recipe-determine-whether-a-bug-is-version-related.md): Complete Determine Whether A Bug Is Version-Related with evidence-backed checks and a verifiable outcome.
- [Recipe: Review An Obsidian Pull Request](tasks/recipe-review-an-obsidian-pull-request.md): Review against the current Obsidian developer documentation, Null vs Undefined, and Rock Core Release Notes. Build and exercise the changed block on its supported Rock version; static review alone cannot establish authorization, payload, grid, or lifecycle behavior.
- [Recipe: Audit A Block For Security](tasks/recipe-audit-a-block-for-security.md): Complete Audit A Block For Security with evidence-backed checks and a verifiable outcome.
- [Recipe: Audit A Grid For Operational Readiness](tasks/recipe-audit-a-grid-for-operational-readiness.md): Complete Audit A Grid For Operational Readiness with evidence-backed checks and a verifiable outcome.
- [Recipe: Decide Whether To Use Browser Bus](tasks/recipe-decide-whether-to-use-browser-bus.md): The browser bus is page-local only (Browser Bus).

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-45: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 46-73: 2. Scope And Terminology (normal)
- `3-obsidian-development-mental-model` lines 74-101: 3. Obsidian Development Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 102-130: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model` lines 131-150: 5. Core Configuration And Data Model (normal)
- `6-primary-entities-and-relationships` lines 151-168: 6. Primary Entities And Relationships (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the obsidian-development guide.
- `Block`: Rock concept/entity referenced by the obsidian-development guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the obsidian-development guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the obsidian-development guide.
- `Person`: Rock concept/entity referenced by the obsidian-development guide.
- `Step`: Person-specific engagement milestone instance.
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
