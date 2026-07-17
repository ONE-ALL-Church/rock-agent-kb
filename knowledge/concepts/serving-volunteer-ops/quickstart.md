---
concept_id: serving-volunteer-ops
title: Serving And Volunteer Operations Quickstart
generated: true
---

# Serving And Volunteer Operations Quickstart

Serving teams, volunteer schedules, requirements, confirmations, attendance, volunteer communications, and follow-up.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Find The Real Object Behind A Serving Issue](tasks/recipe-find-the-real-object-behind-a-serving-issue.md): Follow the guide section for Recipe: Find The Real Object Behind A Serving Issue.
- [Recipe: Confirm A Volunteer Is Eligible To Serve](tasks/recipe-confirm-a-volunteer-is-eligible-to-serve.md): Follow the guide section for Recipe: Confirm A Volunteer Is Eligible To Serve.
- [Recipe: Explain Why A Volunteer Was Not Scheduled](tasks/recipe-explain-why-a-volunteer-was-not-scheduled.md): Follow the guide section for Recipe: Explain Why A Volunteer Was Not Scheduled.
- [Recipe: Verify Schedule Confirmation Send Health](tasks/recipe-verify-schedule-confirmation-send-health.md): Follow the guide section for Recipe: Verify Schedule Confirmation Send Health.
- [Recipe: Safely Customize A Volunteer-Facing Page](tasks/recipe-safely-customize-a-volunteer-facing-page.md): Follow the guide section for Recipe: Safely Customize A Volunteer-Facing Page.
- [Recipe: Investigate Family Serving Response Request](tasks/recipe-investigate-family-serving-response-request.md): Follow the guide section for Recipe: Investigate Family Serving Response Request.
- [Recipe: Build A Serving Health Dashboard](tasks/recipe-build-a-serving-health-dashboard.md): Follow the guide section for Recipe: Build A Serving Health Dashboard.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-60: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology-core-terms` lines 67-110: Core Terms (high)
- `3-serving-and-volunteer-operations-mental-model-layer-2-where-and-when` lines 137-146: Layer 2: Where And When (normal)
- `3-serving-and-volunteer-operations-mental-model-layer-3-assignment-and-response` lines 147-154: Layer 3: Assignment And Response (normal)
- `3-serving-and-volunteer-operations-mental-model-layer-4-actual-attendance` lines 155-162: Layer 4: Actual Attendance (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 184-199: 4. Source Authority And How To Use This Guide (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `AttendanceOccurrence`: Occurrence context for attendance, including group, schedule, location, date, and SundayDate.
- `Attribute`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Block`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Campus`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Check-in Configuration`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Family`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the serving-volunteer-ops guide.

## Version Caveats

- `18.3`: Fixed the Send Attendance Reminder job so Group leaders still receive reminders when a Group only has scheduling/RSVP-related Attendance records. The job now treats those tracking records as not being “attendance” and on
- `17.2`: Fixed an issue where the Group Scheduling Confirmation workflow could incorrectly record a response if the confirmation email was opened by an automated link-checker, or if a decline reason was required but not provided.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
