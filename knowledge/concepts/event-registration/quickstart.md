---
concept_id: event-registration
title: Event Registration Quickstart
generated: true
---

# Event Registration Quickstart

Registration instances, templates, payments, forms, event occurrences, and registration operations.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Create a reusable registration and one event instance](tasks/recipe-create-a-reusable-registration-and-one-event-instance.md): A configured but not yet broadly launched instance with explicit ownership of shared and event-specific settings.
- [Recipe: Validate a paid registration before launch](tasks/recipe-validate-a-paid-registration-before-launch.md): Evidence that representative costs and payment paths produce the intended registration and financial state.
- [Recipe: Promote a wait-listed person to full registration](tasks/recipe-promote-a-wait-listed-person-to-full-registration.md): The person becomes a complete, paid-as-required registrant with the intended group membership.
- [Recipe: Audit an event-registration dashboard](tasks/recipe-audit-an-event-registration-dashboard.md): Every published metric has an explicit grain, population, and reconciliation test.
- [Recipe: Launch family preregistration with follow-up](tasks/recipe-launch-family-preregistration-with-follow-up.md): A family can preregister without unnecessary friction, records are usable at check-in, and staff receive an owned follow-up action.

## High-Signal Sections

- `agent-summary` lines 18-32: Agent Summary (normal)
- `mental-model` lines 51-68: Mental Model (normal)
- `registration-instances-build-reusable-behavior-in-the-template` lines 71-78: Build reusable behavior in the template (normal)
- `registration-instances-put-occurrence-specific-settings-on-the-instance` lines 79-86: Put occurrence-specific settings on the instance (normal)
- `registration-instances-manage-at-the-correct-grain` lines 87-92: Manage at the correct grain (normal)
- `forms-identity-eligibility-and-communications-design-the-form-around-the-record-being-updated` lines 95-102: Design the form around the record being updated (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the event-registration guide.
- `Block`: Rock concept/entity referenced by the event-registration guide.
- `Campus`: Rock concept/entity referenced by the event-registration guide.
- `Check-in Configuration`: Rock concept/entity referenced by the event-registration guide.
- `Family`: Rock concept/entity referenced by the event-registration guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the event-registration guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the event-registration guide.
- `Person`: Rock concept/entity referenced by the event-registration guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.

## Version Caveats

- `18.3`: Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant with
- `19.1`: Added a Prevent Duplicate Registrants setting to the Registration Template that prevents the same person record from registering for the same Registration Instance more than once. When enabled, the Registration Entry Blo

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
