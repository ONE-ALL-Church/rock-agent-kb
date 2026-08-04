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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Identify Why A Group Is Not Visible](tasks/recipe-identify-why-a-group-is-not-visible.md): Complete Identify Why A Group Is Not Visible with evidence-backed checks and a verifiable outcome.
- [Recipe: Audit A Group Type Before Launch](tasks/recipe-audit-a-group-type-before-launch.md): Complete Audit A Group Type Before Launch with evidence-backed checks and a verifiable outcome.
- [Recipe: Debug Group Attendance Reminder Failures](tasks/recipe-debug-group-attendance-reminder-failures.md): Complete Debug Group Attendance Reminder Failures with evidence-backed checks and a verifiable outcome.
- [Recipe: Build A Group Finder QA Checklist](tasks/recipe-build-a-group-finder-qa-checklist.md): Complete Build A Group Finder QA Checklist with evidence-backed checks and a verifiable outcome.
- [Recipe: Move Members Between Groups Safely](tasks/recipe-move-members-between-groups-safely.md): Complete Move Members Between Groups Safely with evidence-backed checks and a verifiable outcome.
- [Recipe: Create A Custom Scheduled Volunteer Communication Page](tasks/recipe-create-a-custom-scheduled-volunteer-communication-page.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-46: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 47-68: 2. Scope And Terminology (normal)
- `3-groups-mental-model` lines 69-90: 3. Groups Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 91-103: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-group-type-configuration` lines 106-129: Group Type Configuration (normal)
- `5-core-configuration-and-data-model-locations-and-schedules` lines 148-159: Locations And Schedules (normal)

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
