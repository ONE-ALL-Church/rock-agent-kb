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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Configure a serving team for scheduling](tasks/recipe-configure-a-serving-team-for-scheduling.md): A bounded serving group is ready for assignments at verified locations and times.
- [Recipe: Send and triage volunteer confirmations](tasks/recipe-send-and-triage-volunteer-confirmations.md): The intended volunteers receive a confirmation request without an uncontrolled duplicate send.
- [Recipe: Configure an RSVP-based serving invitation](tasks/recipe-configure-an-rsvp-based-serving-invitation.md): A group occurrence can collect and display bounded accept or decline responses.
- [Recipe: Close out serving attendance](tasks/recipe-close-out-serving-attendance.md): The occurrence records who served or that the team did not meet, with discrepancies ready for human review.
- [Recipe: Build an LMS-based volunteer training path](tasks/recipe-build-an-lms-based-volunteer-training-path.md): A volunteer completes defined learning activities and reaches an explicitly reviewed operational result.
- [Recipe: Configure an attendance digest](tasks/recipe-configure-an-attendance-digest.md): Leaders at the intended regional level receive attendance summaries for their child attendance groups.
- [Recipe: Secure an embedded volunteer dashboard](tasks/recipe-secure-an-embedded-volunteer-dashboard.md): The Rock page and external reporting provider both authorize only the intended viewers.
- [Recipe: Pilot Outreach Toolbox for relationship-care follow-up](tasks/recipe-pilot-outreach-toolbox-for-relationship-care-follow-up.md): A bounded group of signed-in mobile users can see, receive, complete, and review configured outreach touchpoints.

## High-Signal Sections

- `agent-summary` lines 18-32: Agent Summary (normal)
- `mental-model-policy-team-assignment-response-and-attendance` lines 52-63: Policy, team, assignment, response, and attendance (high)
- `mental-model-group-scheduling-and-group-rsvp-are-related-but-different` lines 64-71: Group Scheduling and Group RSVP are related but different (normal)
- `serving-teams-and-roles-establish-the-operating-group-structure` lines 78-93: Establish the operating group structure (normal)
- `serving-teams-and-roles-distinguish-operational-roles` lines 94-106: Distinguish operational roles (normal)
- `serving-teams-and-roles-be-precise-when-identifying-volunteers-in-reports` lines 107-112: Be precise when identifying volunteers in reports (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Block`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Campus`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Family`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Person`: Rock concept/entity referenced by the serving-volunteer-ops guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the serving-volunteer-ops guide.

## Version Caveats

- `19.3`: Fixed an issue with the RSVP Response block where the heading would show the generic "RSVP for Event" text instead of the Attendance Occurrence Name when accessed through the Accept or Decline link in an RSVP email. Fixe
- `18.3`: Fixed the Send Attendance Reminder job so Group leaders still receive reminders when a Group only has scheduling/RSVP-related Attendance records. The job now treats those tracking records as not being “attendance” and on

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
