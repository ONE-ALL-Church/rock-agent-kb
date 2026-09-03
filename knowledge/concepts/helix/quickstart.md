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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inspect an existing Helix application before changing it](tasks/recipe-inspect-an-existing-helix-application-before-changing-it.md): A bounded map of the current application flow and its security-sensitive surfaces.
- [Recipe: Build a read-only HTMX result fragment](tasks/recipe-build-a-read-only-htmx-result-fragment.md): A page-hosted query interaction that returns only authorized display content.
- [Recipe: Build a validated mutation form](tasks/recipe-build-a-validated-mutation-form.md): A non-GET endpoint that rejects unauthorized or invalid direct calls as well as invalid browser submissions.
- [Recipe: Render endpoint content on first paint](tasks/recipe-render-endpoint-content-on-first-paint.md): Endpoint-generated content appears during the initial page render without a second request or avoidable layout shift.
- [Recipe: Validate a rendered Helix dashboard](tasks/recipe-validate-a-rendered-helix-dashboard.md): Evidence that source targeting, authorization, data semantics, interaction behavior, and responsive layout all work in the actual page context.
- [Recipe: Decide whether to replace a Lava Application](tasks/recipe-decide-whether-to-replace-a-lava-application.md): A documented decision to retain Helix or move to a purpose-built solution.

## High-Signal Sections

- `agent-summary` lines 18-25: Agent Summary (normal)
- `scope-and-boundaries` lines 26-43: Scope And Boundaries (normal)
- `mental-model` lines 44-68: Mental Model (normal)
- `overview-and-roadmap` lines 69-82: Overview And Roadmap (normal)
- `htmx` lines 83-105: HTMX (normal)
- `lava-applications` lines 106-118: Lava Applications (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the helix guide.
- `Block`: Rock concept/entity referenced by the helix guide.
- `Campus`: Rock concept/entity referenced by the helix guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the helix guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the helix guide.
- `Person`: Rock concept/entity referenced by the helix guide.
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
