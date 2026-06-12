---
concept_id: groups
title: Groups Quickstart
generated: true
---

# Groups Quickstart

Group types, group members, attendance, group finder, small groups, serving teams, and security.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Identify Why A Group Is Not Visible](tasks/recipe-identify-why-a-group-is-not-visible.md): Follow the guide section for Recipe: Identify Why A Group Is Not Visible.
- [Recipe: Audit A Group Type Before Launch](tasks/recipe-audit-a-group-type-before-launch.md): Follow the guide section for Recipe: Audit A Group Type Before Launch.
- [Recipe: Debug Group Attendance Reminder Failures](tasks/recipe-debug-group-attendance-reminder-failures.md): Follow the guide section for Recipe: Debug Group Attendance Reminder Failures.
- [Recipe: Build A Group Finder QA Checklist](tasks/recipe-build-a-group-finder-qa-checklist.md): Follow the guide section for Recipe: Build A Group Finder QA Checklist.
- [Recipe: Move Members Between Groups Safely](tasks/recipe-move-members-between-groups-safely.md): Follow the guide section for Recipe: Move Members Between Groups Safely.
- [Recipe: Create A Custom Scheduled Volunteer Communication Page](tasks/recipe-create-a-custom-scheduled-volunteer-communication-page.md): Follow the guide section for Recipe: Create A Custom Scheduled Volunteer Communication Page.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-44: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 45-66: 2. Scope And Terminology (normal)
- `3-groups-mental-model` lines 67-88: 3. Groups Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 89-101: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-group-type-configuration` lines 104-127: Group Type Configuration (normal)
- `5-core-configuration-and-data-model-locations-and-schedules` lines 146-157: Locations And Schedules (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `AttendanceOccurrence`: Occurrence context for attendance, including group, schedule, location, date, and SundayDate.
- `Attribute`: Rock concept/entity referenced by the groups guide.
- `Block`: Rock concept/entity referenced by the groups guide.
- `Campus`: Rock concept/entity referenced by the groups guide.
- `Check-in Configuration`: Rock concept/entity referenced by the groups guide.
- `DataView`: Rock concept/entity referenced by the groups guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the groups guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the groups guide.
- `GroupMemberRequirement`: Serving or membership qualification gate that can depend on training, background checks, documents, or manual review.

## Version Caveats

- `18.3`: Fixed an issue where the Attendance Analytics block incorrectly included groups whose Group Type was listed as an "Allowed Child Group Type" of a selected Group Type, even though it was not explicitly selected in the blo

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
