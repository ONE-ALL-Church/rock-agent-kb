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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Identify A Person Safely](tasks/recipe-identify-a-person-safely.md): Follow the guide section for Recipe: Identify A Person Safely.
- [Recipe: Explain Why `PersonAlias` Matters](tasks/recipe-explain-why-personalias-matters.md): Follow the guide section for Recipe: Explain Why `PersonAlias` Matters.
- [Recipe: Inspect A Person Attribute](tasks/recipe-inspect-a-person-attribute.md): Follow the guide section for Recipe: Inspect A Person Attribute.
- [Recipe: Determine If A Value Is Person Id Or Alias Guid](tasks/recipe-determine-if-a-value-is-person-id-or-alias-guid.md): Follow the guide section for Recipe: Determine If A Value Is Person Id Or Alias Guid.
- [Recipe: Audit A Family For Check-In](tasks/recipe-audit-a-family-for-check-in.md): Follow the guide section for Recipe: Audit A Family For Check-In.
- [Recipe: Review A Person Profile Customization](tasks/recipe-review-a-person-profile-customization.md): Follow the guide section for Recipe: Review A Person Profile Customization.
- [Recipe: Triage An Accidental Merge](tasks/recipe-triage-an-accidental-merge.md): Follow the guide section for Recipe: Triage An Accidental Merge.
- [Recipe: Track New Record Source](tasks/recipe-track-new-record-source.md): Follow the guide section for Recipe: Track New Record Source.
- [Recipe: Build A Staff Directory From Person Attributes](tasks/recipe-build-a-staff-directory-from-person-attributes.md): Follow the guide section for Recipe: Build A Staff Directory From Person Attributes.
- [Recipe: Add A Bookmarked Groups-Like Profile Panel](tasks/recipe-add-a-bookmarked-groups-like-profile-panel.md): Follow the guide section for Recipe: Add A Bookmarked Groups-Like Profile Panel.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-53: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 54-101: 2. Scope And Terminology (normal)
- `3-people-and-families-mental-model` lines 102-138: 3. People And Families Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 139-176: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-person` lines 181-206: Person (normal)
- `5-core-configuration-and-data-model-personalias` lines 207-222: PersonAlias (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the people-families guide.
- `Block`: Rock concept/entity referenced by the people-families guide.
- `Campus`: Rock concept/entity referenced by the people-families guide.
- `Check-in Configuration`: Rock concept/entity referenced by the people-families guide.
- `DataView`: Rock concept/entity referenced by the people-families guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the people-families guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the people-families guide.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the people-families guide.

## Version Caveats

- `18.3`: Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup
- `18.2`: Fixed an issue where the Attribute Editor did not correctly save configuration changes when creating an Attribute designed to store other Attributes (e.g., an Attribute of type Attribute). This affected scenarios such as
- `18.1`: Improved the Person Record Source feature by adding support for setting a Record Source within the Get Person From Fields Workflow Action and the internal Add Family page. Also added a configuration option to define a de
- `19.1`: Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729
- `19.1`: Added Registrant eligibility rules to the Registration Template Detail Block and updated the Registration Entry Block to prevent incorrect family member registrations. Added new "Registrant Eligibility" settings to the R
- `19.1`: Fixed an issue where editing an Event Occurrence Attribute on the Event Item Detail block would incorrectly reject the attribute key value with a validation error, preventing the attribute from being saved.
- `18.2`: Fixed an issue where submitting a registration would disable an individual's SMS setting when the "Show SMS Opt-In" option on the Registration Template was set to False. The registration process will now preserve the ind
- `18.2`: Fixed an issue where creating a Benevolence Request from a Person Profile did not automatically associate the current person, requiring the individual to be manually selected after the request was created. Fixes: #6631

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
