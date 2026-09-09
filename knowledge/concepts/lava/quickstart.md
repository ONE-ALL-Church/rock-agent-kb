---
concept_id: lava
title: Lava Quickstart
generated: true
---

# Lava Quickstart

Lava syntax, filters, commands, shortcodes, remote Lava, and safe operational use.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Review an existing Lava surface safely](tasks/recipe-review-an-existing-lava-surface-safely.md): A bounded risk assessment without changing the target.
- [Recipe: Build a bounded read-only entity view](tasks/recipe-build-a-bounded-read-only-entity-view.md): A limited list using an Entity command.
- [Recipe: Prepare a Lava entity write](tasks/recipe-prepare-a-lava-entity-write.md): An idempotent, verifiable single-entity change plan.
- [Recipe: Preflight a workflow activation](tasks/recipe-preflight-a-workflow-activation.md): A workflow is activated with verified attribute values.
- [Recipe: Publish a reusable shortcode](tasks/recipe-publish-a-reusable-shortcode.md): A stable shortcode contract for content authors.
- [Recipe: Build a read-only Helix active-search page](tasks/recipe-build-a-read-only-helix-active-search-page.md): A server-rendered page enhanced with bounded HTMX filtering.
- [Recipe: Validate a Rock Mobile Lava block](tasks/recipe-validate-a-rock-mobile-lava-block.md): Correct, fresh and valid mobile output for the supported shells.
- [Recipe: Design a Lava-backed AI tool](tasks/recipe-design-a-lava-backed-ai-tool.md): A narrow tool the model can select and use without excessive access.

## High-Signal Sections

- `agent-summary` lines 34-47: Agent Summary (normal)
- `mental-model` lines 56-78: Mental Model (normal)
- `core-syntax-and-engine` lines 79-96: Core Syntax And Engine (normal)
- `core-syntax-and-engine-fluid-and-dotliquid` lines 97-115: Fluid and DotLiquid (normal)
- `filters` lines 116-128: Filters (normal)
- `filters-text-and-output-encoding` lines 129-134: Text and output encoding (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the lava guide.
- `Block`: Rock concept/entity referenced by the lava guide.
- `DataView`: Rock concept/entity referenced by the lava guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Label`: Rock concept/entity referenced by the lava guide.
- `Page`: Rock concept/entity referenced by the lava guide.
- `Person`: Rock concept/entity referenced by the lava guide.
- `PersonAlias`: Rock concept/entity referenced by the lava guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the lava guide.

## Version Caveats

- `19.1`: Added a new Shortcode Scope Behavior property to the Lava Shortcode Entity. This setting allows Rock administrators to choose whether variables defined inside a shortcode should be isolated from or shared with the surrou

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
