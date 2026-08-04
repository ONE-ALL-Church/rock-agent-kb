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

- [Recipe: Answer "What Does This Report Actually Show?"](tasks/recipe-answer-what-does-this-report-actually-show.md): Complete Answer "What Does This Report Actually Show?" with evidence-backed checks and a verifiable outcome.
- [Recipe: Answer "Can I Change This Data View?"](tasks/recipe-answer-can-i-change-this-data-view.md): Complete Answer "Can I Change This Data View?" with evidence-backed checks and a verifiable outcome.
- [Recipe: Build "People Who Attended X But Not Y"](tasks/recipe-build-people-who-attended-x-but-not-y.md): Complete Build "People Who Attended X But Not Y" with evidence-backed checks and a verifiable outcome.
- [Recipe: Build "Lapsed Givers"](tasks/recipe-build-lapsed-givers.md): Complete Build "Lapsed Givers" with evidence-backed checks and a verifiable outcome.
- [Recipe: Build "Where Are Our Reporting Tools?"](tasks/recipe-build-where-are-our-reporting-tools.md): Complete Build "Where Are Our Reporting Tools?" with evidence-backed checks and a verifiable outcome.
- [Recipe: Validate A BI Finance Dashboard](tasks/recipe-validate-a-bi-finance-dashboard.md): Complete Validate A BI Finance Dashboard with evidence-backed checks and a verifiable outcome.
- [Recipe: Audit Reporting Security](tasks/recipe-audit-reporting-security.md): Complete Audit Reporting Security with evidence-backed checks and a verifiable outcome.
- [Recipe: Diagnose Slow Reporting](tasks/recipe-diagnose-slow-reporting.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-68: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 69-74: 2. Scope And Terminology (normal)
- `2-scope-and-terminology-core-terms` lines 75-126: Core Terms (high)
- `3-data-views-and-reports-mental-model-the-layered-stack` lines 129-144: The Layered Stack (normal)
- `3-data-views-and-reports-mental-model-data-view-composition` lines 172-183: Data View Composition (normal)
- `3-data-views-and-reports-mental-model-related-data-view-semantics` lines 184-197: Related Data View Semantics (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `AttendanceOccurrence`: Occurrence context for attendance, including group, schedule, location, date, and SundayDate.
- `Attribute`: Rock concept/entity referenced by the data-views-reports guide.
- `Block`: Rock concept/entity referenced by the data-views-reports guide.
- `Campus`: Rock concept/entity referenced by the data-views-reports guide.
- `Check-in Configuration`: Rock concept/entity referenced by the data-views-reports guide.
- `DataView`: Rock concept/entity referenced by the data-views-reports guide.
- `Family`: Rock concept/entity referenced by the data-views-reports guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the data-views-reports guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
