---
concept_id: workflows
title: Workflows Quickstart
generated: true
---

# Workflows Quickstart

Workflow types, actions, triggers, forms, automation, jobs, and operational process design.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Design a bounded workflow type](tasks/recipe-design-a-bounded-workflow-type.md): A reviewable process model before configuration begins.
- [Recipe: Review a workflow form change](tasks/recipe-review-a-workflow-form-change.md): A field change that preserves validation, visibility, and downstream behavior.
- [Recipe: Configure a selective workflow webhook](tasks/recipe-configure-a-selective-workflow-webhook.md): One intended request starts only the intended workflow with inspectable input.
- [Recipe: Diagnose an active workflow instance](tasks/recipe-diagnose-an-active-workflow-instance.md): The first incorrect state or action is identified without unsafe replay.
- [Recipe: Audit a connection follow-up process](tasks/recipe-audit-a-connection-follow-up-process.md): A Connection process is understood as both person context and operational state.
- [Recipe: Import or adapt a workflow safely](tasks/recipe-import-or-adapt-a-workflow-safely.md): An imported or cloned workflow is validated before activation.
- [Recipe: Design background orchestration](tasks/recipe-design-background-orchestration.md): Slow work proceeds asynchronously with explicit operational state.

## High-Signal Sections

- `agent-summary` lines 34-50: Agent Summary (normal)
- `scope-and-boundaries` lines 51-66: Scope And Boundaries (normal)
- `mental-model` lines 67-86: Mental Model (normal)
- `process-design-before-configuration` lines 87-105: Process Design Before Configuration (normal)
- `triggers-and-activation-entry-pages-and-direct-links` lines 108-115: Entry pages and direct links (normal)
- `triggers-and-activation-person-entity-and-grid-launches` lines 116-121: Person, entity, and grid launches (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the workflows guide.
- `Block`: Rock concept/entity referenced by the workflows guide.
- `Campus`: Rock concept/entity referenced by the workflows guide.
- `DataView`: Rock concept/entity referenced by the workflows guide.
- `Family`: Rock concept/entity referenced by the workflows guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the workflows guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the workflows guide.
- `Person`: Rock concept/entity referenced by the workflows guide.
- `PersonAlias`: Rock concept/entity referenced by the workflows guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
