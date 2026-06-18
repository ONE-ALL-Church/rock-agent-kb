---
concept_id: prayer-care
title: Prayer And Care Quickstart
generated: true
---

# Prayer And Care Quickstart

Prayer requests, prayer teams, moderation, categories, care follow-up, visibility, communication, and privacy-sensitive ministry workflows.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks


## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-34: 1. Executive Summary For Agents (normal)
- `2-agent-workflow` lines 35-42: 2. Agent Workflow (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Block`: Rock concept/entity referenced by the prayer-care guide.
- `Campus`: Rock concept/entity referenced by the prayer-care guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Page`: Rock concept/entity referenced by the prayer-care guide.
- `Person`: Rock concept/entity referenced by the prayer-care guide.
- `Workflow`: Rock concept/entity referenced by the prayer-care guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
