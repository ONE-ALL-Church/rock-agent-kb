---
concept_id: data-views-reports
title: Data Views And Reports Quickstart
generated: true
---

# Data Views And Reports Quickstart

Data views, reports, SQL, BI, metrics, analytics, and model/data discovery.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Create a reusable operational Report](tasks/recipe-create-a-reusable-operational-report.md): One governed population definition and one Report that presents it without duplicating filter logic.
- [Recipe: Convert duplicated Reports into one Dynamic Report](tasks/recipe-convert-duplicated-reports-into-one-dynamic-report.md): One Report supports controlled viewer-selected criteria.
- [Recipe: Introduce persistence for a slow Data View](tasks/recipe-introduce-persistence-for-a-slow-data-view.md): Faster consumer performance with an explicitly accepted freshness window.
- [Recipe: Diagnose an empty BI dashboard](tasks/recipe-diagnose-an-empty-bi-dashboard.md): Identify whether the failure is Rock population, job processing, external refresh, licensing, or authorization.
- [Recipe: Validate a registration analytics dashboard](tasks/recipe-validate-a-registration-analytics-dashboard.md): Every displayed total has an explicit grain and reconciled population.

## High-Signal Sections

- `agent-summary` lines 18-32: Agent Summary (normal)
- `scope-and-boundaries` lines 33-51: Scope And Boundaries (normal)
- `mental-model` lines 52-72: Mental Model (normal)
- `data-views` lines 73-93: Data Views (normal)
- `reports` lines 94-105: Reports (normal)
- `report-security` lines 106-121: Report Security (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the data-views-reports guide.
- `Block`: Rock concept/entity referenced by the data-views-reports guide.
- `Campus`: Rock concept/entity referenced by the data-views-reports guide.
- `DataView`: Rock concept/entity referenced by the data-views-reports guide.
- `Family`: Rock concept/entity referenced by the data-views-reports guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the data-views-reports guide.
- `Page`: Rock concept/entity referenced by the data-views-reports guide.
- `Person`: Rock concept/entity referenced by the data-views-reports guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the data-views-reports guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
