---
concept_id: helix
title: Helix Quickstart
generated: true
---

# Helix Quickstart

Helix, HTMX, Lava Applications, Lava Endpoints, Lava Application Content blocks, forms and controls, endpoint security, observability, and production-readiness caveats.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Find The Endpoint Behind A Button](tasks/recipe-find-the-endpoint-behind-a-button.md): Follow the guide section for Recipe: Find The Endpoint Behind A Button.
- [Recipe: Determine Whether A Helix App Is Public-Safe](tasks/recipe-determine-whether-a-helix-app-is-public-safe.md): Follow the guide section for Recipe: Determine Whether A Helix App Is Public-Safe.
- [Recipe: Upgrade A Plugin-Era Helix App](tasks/recipe-upgrade-a-plugin-era-helix-app.md): Follow the guide section for Recipe: Upgrade A Plugin-Era Helix App.
- [Recipe: Review A Community Recipe Before Use](tasks/recipe-review-a-community-recipe-before-use.md): Follow the guide section for Recipe: Review A Community Recipe Before Use.
- [Recipe: Add Observability To A Complex Endpoint](tasks/recipe-add-observability-to-a-complex-endpoint.md): Follow the guide section for Recipe: Add Observability To A Complex Endpoint.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-45: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 46-81: 2. Scope And Terminology (normal)
- `3-helix-mental-model` lines 82-112: 3. Helix Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 113-127: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model-lava-application-configuration` lines 130-153: Lava Application Configuration (normal)
- `5-core-configuration-and-data-model-lava-endpoint-configuration` lines 154-172: Lava Endpoint Configuration (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the helix guide.
- `Block`: Rock concept/entity referenced by the helix guide.
- `Campus`: Rock concept/entity referenced by the helix guide.
- `Family`: Rock concept/entity referenced by the helix guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the helix guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the helix guide.
- `Person`: Rock concept/entity referenced by the helix guide.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the helix guide.

## Version Caveats

- `18.1`: Added Helix support for Lava Applications to core. This provides a great new way to build interactive pages in Rock powered by Lava for more advanced administrators.
- `19.1`: Added Body and RawBody merge fields to Lava Applications.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
