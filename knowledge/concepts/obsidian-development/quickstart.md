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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks


## High-Signal Sections

- `2-agent-workflow` lines 33-40: 2. Agent Workflow (normal)

## Core Entities

- `Block`: Rock concept/entity referenced by the obsidian-development guide.
- `Page`: Rock concept/entity referenced by the obsidian-development guide.
- `Workflow`: Rock concept/entity referenced by the obsidian-development guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
