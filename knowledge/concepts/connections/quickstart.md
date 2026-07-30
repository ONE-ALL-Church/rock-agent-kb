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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Audit One Connection Type](tasks/recipe-audit-one-connection-type.md): Complete Audit One Connection Type with evidence-backed checks and a verifiable outcome.
- [Recipe: Explain Why A Request Is Hidden](tasks/recipe-explain-why-a-request-is-hidden.md): Cite mobile connected-state exclusion if relevant (Connection Request List mobile docs).
- [Recipe: Validate Signup Flow](tasks/recipe-validate-signup-flow.md): Cite Add Request mobile docs for parameter behavior and v17.2/v18.1 release notes for attributes/record source if applicable (Add Connection Request mobile docs, release notes).
- [Recipe: Build Opportunity Cards](tasks/recipe-build-opportunity-cards.md): Complete Build Opportunity Cards with evidence-backed checks and a verifiable outcome.
- [Recipe: Investigate Connector Workload](tasks/recipe-investigate-connector-workload.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-54: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 55-93: 2. Scope And Terminology (high)
- `3-connections-mental-model` lines 94-119: 3. Connections Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 120-144: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-configuration-surfaces` lines 147-163: Configuration Surfaces (normal)
- `5-core-configuration-and-data-model-connection-type-configuration` lines 164-188: Connection Type Configuration (high)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the connections guide.
- `Block`: Rock concept/entity referenced by the connections guide.
- `Campus`: Rock concept/entity referenced by the connections guide.
- `Check-in Configuration`: Rock concept/entity referenced by the connections guide.
- `Family`: Rock concept/entity referenced by the connections guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the connections guide.
- `Page`: Rock concept/entity referenced by the connections guide.
- `Person`: Rock concept/entity referenced by the connections guide.
- `PersonAlias`: Rock concept/entity referenced by the connections guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.

## Version Caveats

- `18.1`: Improved the Connection Request Board with updates to campus filtering, connector preferences, and workflow configuration. Added new block settings to define default Connection State and Status filters. Workflows on the
- `17.2`: Fixed an issue where the Connection Opportunity Signup block only displayed request attributes defined on the opportunity itself, now correctly including attributes inherited from the Connection Type. Fixes: #6356

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
