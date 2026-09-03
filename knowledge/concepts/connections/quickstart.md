---
concept_id: connections
title: Connections Quickstart
generated: true
---

# Connections Quickstart

Connection types, opportunities, requests, statuses, boards, lists, assignments, follow-up, and pipeline reporting.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Configure a new connection pipeline](tasks/recipe-configure-a-new-connection-pipeline.md): A bounded connection type and opportunity are ready for controlled staff testing.
- [Recipe: Triage an unassigned or overdue queue](tasks/recipe-triage-an-unassigned-or-overdue-queue.md): Every selected request has a verified owner or an explicit disposition.
- [Recipe: Transfer and complete a request safely](tasks/recipe-transfer-and-complete-a-request-safely.md): The request reaches the correct destination with ownership and placement preserved.
- [Recipe: Launch a connection campaign](tasks/recipe-launch-a-connection-campaign.md): An eligible audience enters a controlled, assignable follow-up queue.
- [Recipe: Connect preregistration to staff follow-up](tasks/recipe-connect-preregistration-to-staff-follow-up.md): A preregistered family reaches a verified staff-owned next step without avoidable duplicate records.
- [Recipe: Validate status automation](tasks/recipe-validate-status-automation.md): A status rule moves only currently eligible requests and can be retried safely.

## High-Signal Sections

- `agent-summary` lines 18-36: Agent Summary (normal)
- `mental-model` lines 52-72: Mental Model (normal)
- `opportunities` lines 73-94: Opportunities (normal)
- `requests-and-statuses` lines 95-104: Requests And Statuses (normal)
- `requests-and-statuses-state` lines 105-115: State (normal)
- `requests-and-statuses-status` lines 116-123: Status (high)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the connections guide.
- `Block`: Rock concept/entity referenced by the connections guide.
- `Campus`: Rock concept/entity referenced by the connections guide.
- `DataView`: Rock concept/entity referenced by the connections guide.
- `Family`: Rock concept/entity referenced by the connections guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the connections guide.
- `Page`: Rock concept/entity referenced by the connections guide.
- `Person`: Rock concept/entity referenced by the connections guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the connections guide.

## Version Caveats

- `19.3`: Fixed an issue where a workflow could not be removed from a Connection Opportunity or Connection Type after it had been triggered from a Connection Request. Fixes: #6875
- `18.1`: Improved the Connection Request Board with updates to campus filtering, connector preferences, and workflow configuration. Added new block settings to define default Connection State and Status filters. Workflows on the

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
