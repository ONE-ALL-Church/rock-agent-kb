---
concept_id: people-families
title: People And Families Quickstart
generated: true
---

# People And Families Quickstart

Person records, families, aliases, attributes, relationships, and data hygiene.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Add a person or family without creating a duplicate](tasks/recipe-add-a-person-or-family-without-creating-a-duplicate.md): The correct person records are attached to the correct family with no avoidable duplicate.
- [Recipe: Correct a family structure or household move](tasks/recipe-correct-a-family-structure-or-household-move.md): Family membership, primary-family context, address history, and downstream behavior reflect the reviewed household reality.
- [Recipe: Design or review a person or family attribute](tasks/recipe-design-or-review-a-person-or-family-attribute.md): The attribute has a clear owner, correct entity, maintainable value, appropriate display, and bounded security.
- [Recipe: Audit Person Note governance](tasks/recipe-audit-person-note-governance.md): Notes are categorized, visible, and consumed according to documented staff purpose and authorization.
- [Recipe: Prepare a duplicate-person merge for authorized review](tasks/recipe-prepare-a-duplicate-person-merge-for-authorized-review.md): A reviewer receives a bounded comparison and can merge without relying on recency alone.
- [Recipe: Validate family preregistration end to end](tasks/recipe-validate-family-preregistration-end-to-end.md): A visitor can preregister without producing preventable duplicates, and the resulting people data leads to check-in and staff action.
- [Recipe: Diagnose a connection request from the person record](tasks/recipe-diagnose-a-connection-request-from-the-person-record.md): The failure is classified as person context, request state, opportunity configuration, assignment, activity, or automation.
- [Recipe: Run a bounded people-data cleanup](tasks/recipe-run-a-bounded-people-data-cleanup.md): A defined population is corrected by a testable rule with before-and-after evidence.

## High-Signal Sections

- `agent-summary` lines 18-30: Agent Summary (normal)
- `mental-model` lines 54-70: Mental Model (normal)
- `person-model-and-record-lifecycle-creating-and-locating-people` lines 73-78: Creating and locating people (normal)
- `person-model-and-record-lifecycle-editing-inactivating-and-preserving-history` lines 79-90: Editing, inactivating, and preserving history (normal)
- `person-model-and-record-lifecycle-derived-person-data` lines 91-96: Derived person data (normal)
- `person-profile-and-access-boundaries` lines 97-113: Person Profile And Access Boundaries (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the people-families guide.
- `Block`: Rock concept/entity referenced by the people-families guide.
- `Campus`: Rock concept/entity referenced by the people-families guide.
- `Family`: Rock concept/entity referenced by the people-families guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the people-families guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the people-families guide.
- `Person`: Rock concept/entity referenced by the people-families guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.

## Version Caveats

- `18.3`: Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup
- `18.2`: Fixed an issue where the Attribute Editor did not correctly save configuration changes when creating an Attribute designed to store other Attributes (e.g., an Attribute of type Attribute). This affected scenarios such as

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
