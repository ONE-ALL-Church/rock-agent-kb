---
concept_id: check-in
title: Check-In Quickstart
generated: true
---

# Check-In Quickstart

Attendance, kiosks, labels, families, schedules, locations, mobile check-in, and troubleshooting.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Diagnose Labels Not Printing](tasks/diagnose-labels-not-printing.md): Find whether the failure is configuration, device routing, printer hardware, label definition, mobile/cloud print, or version-specific behavior.
- [Diagnose Person Found But No Eligible Rooms](tasks/diagnose-person-not-eligible.md): Trace eligibility from person/family search through configuration, group type, group, location, schedule, campus, capacity, and version caveats.
- [Add A New Check-In Room](tasks/add-new-room.md): Add a room without breaking eligibility, labels, printer routing, capacity, or reporting.
- [Audit Mobile Check-In](tasks/audit-mobile-check-in.md): Confirm mobile check-in uses the intended configuration template, kiosk, areas, authentication, and print route.
- [Build Or Debug Attendance Reporting](tasks/build-attendance-report.md): Use the attendance data model correctly so reports match check-in behavior.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-49: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 50-85: 2. Scope And Terminology (high)
- `3-check-in-mental-model` lines 86-122: 3. Check-In Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 123-163: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-check-in-systems` lines 168-179: Check-In Systems (normal)
- `5-core-configuration-and-data-model-check-in-type-individual-vs-family` lines 180-187: Check-In Type: Individual vs Family (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `AttendanceOccurrence`: Occurrence context for attendance, including group, schedule, location, date, and SundayDate.
- `Attribute`: Rock concept/entity referenced by the check-in guide.
- `Block`: Rock concept/entity referenced by the check-in guide.
- `Campus`: Rock concept/entity referenced by the check-in guide.
- `Check-in Configuration`: Rock concept/entity referenced by the check-in guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Device/Kiosk`: Rock concept/entity referenced by the check-in guide.
- `Family`: Rock concept/entity referenced by the check-in guide.
- `Family Group`: Rock concept/entity referenced by the check-in guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the check-in guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
