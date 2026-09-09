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

- [Recipe: Design a Group Type and hierarchy](tasks/recipe-design-a-group-type-and-hierarchy.md): A bounded Group Type design with explicit hierarchy, roles, attributes, and security.
- [Recipe: Publish a group through Group Finder](tasks/recipe-publish-a-group-through-group-finder.md): An intended group is discoverable without exposing unnecessary location precision.
- [Recipe: Configure focused attendance entry](tasks/recipe-configure-focused-attendance-entry.md): Ministry staff can enter attendance and only the related actions appropriate to that workflow.
- [Recipe: Configure attendance follow-up](tasks/recipe-configure-attendance-follow-up.md): Leaders receive the intended reminders, digests, or absence notifications without duplicate or misrouted messages.
- [Recipe: Enforce a Group Type requirement](tasks/recipe-enforce-a-group-type-requirement.md): The intended population is evaluated and manual additions are blocked or overrideable according to policy.
- [Recipe: Synchronize a group from a Data View](tasks/recipe-synchronize-a-group-from-a-data-view.md): Membership for one role follows a reviewed population rule at a sustainable cadence.
- [Recipe: Secure leader operations](tasks/recipe-secure-leader-operations.md): Leaders can perform approved group tasks without unnecessary database or group-administration access.
- [Recipe: Enable history and archive a group](tasks/recipe-enable-history-and-archive-a-group.md): Group changes are snapshotted and a retired group is recoverable.
- [Recipe: Move group members safely](tasks/recipe-move-group-members-safely.md): Selected memberships move without unexpected loss of notes or attributes.

## High-Signal Sections

- `agent-summary` lines 34-46: Agent Summary (normal)
- `scope-and-boundaries` lines 47-61: Scope And Boundaries (normal)
- `mental-model` lines 62-73: Mental Model (high)
- `group-types-and-hierarchies` lines 74-95: Group Types And Hierarchies (normal)
- `creating-editing-inactivating-and-archiving-groups` lines 96-112: Creating, Editing, Inactivating, And Archiving Groups (normal)
- `members-roles-statuses-and-attributes` lines 113-143: Members, Roles, Statuses, And Attributes (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the groups guide.
- `Block`: Rock concept/entity referenced by the groups guide.
- `Campus`: Rock concept/entity referenced by the groups guide.
- `DataView`: Rock concept/entity referenced by the groups guide.
- `Family`: Rock concept/entity referenced by the groups guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the groups guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the groups guide.
- `Person`: Rock concept/entity referenced by the groups guide.

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
