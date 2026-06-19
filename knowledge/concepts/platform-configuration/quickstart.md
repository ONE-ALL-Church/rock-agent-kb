---
concept_id: platform-configuration
title: Platform Configuration Quickstart
generated: true
---

# Platform Configuration Quickstart

Attributes, defined types, categories, entity types, campuses, global attributes, system settings, and cross-domain configuration patterns.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Find Available Attributes For An Add Or Update Operation](tasks/recipe-find-available-attributes-for-an-add-or-update-operation.md): Follow the guide section for Recipe: Find Available Attributes For An Add Or Update Operation.
- [Recipe: Explain A Platform Configuration Object To A User](tasks/recipe-explain-a-platform-configuration-object-to-a-user.md): Follow the guide section for Recipe: Explain A Platform Configuration Object To A User.
- [Recipe: Safely Answer “Can We Delete This?”](tasks/recipe-safely-answer-can-we-delete-this.md): Follow the guide section for Recipe: Safely Answer “Can We Delete This?”.
- [Recipe: Build A Source-Backed Explanation](tasks/recipe-build-a-source-backed-explanation.md): Follow the guide section for Recipe: Build A Source-Backed Explanation.
- [Recipe: Triage Attribute Security](tasks/recipe-triage-attribute-security.md): Follow the guide section for Recipe: Triage Attribute Security.
- [Recipe: Convert A Free-Text Attribute To A Defined Value](tasks/recipe-convert-a-free-text-attribute-to-a-defined-value.md): Follow the guide section for Recipe: Convert A Free-Text Attribute To A Defined Value.
- [Recipe: Diagnose Attribute Field Type Mismatch](tasks/recipe-diagnose-attribute-field-type-mismatch.md): Follow the guide section for Recipe: Diagnose Attribute Field Type Mismatch.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-48: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 49-104: 2. Scope And Terminology (normal)
- `3-platform-configuration-mental-model` lines 105-145: 3. Platform Configuration Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 146-172: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-entity-types` lines 175-199: Entity Types (normal)
- `5-core-configuration-and-data-model-attributes` lines 200-211: Attributes (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the platform-configuration guide.
- `Block`: Rock concept/entity referenced by the platform-configuration guide.
- `Campus`: Rock concept/entity referenced by the platform-configuration guide.
- `Check-in Configuration`: Rock concept/entity referenced by the platform-configuration guide.
- `DefinedType`: Rock concept/entity referenced by the platform-configuration guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the platform-configuration guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the platform-configuration guide.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the platform-configuration guide.

## Version Caveats

- `19.1`: Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729
- `17.2`: Fixed an issue where the list of attribute categories shown when editing a Content Channel Item attribute from the Content Channel Type Detail block included incorrect or unrelated categories. This made it difficult to a
- `18.2`: Fixed an issue where the Attribute Editor did not correctly save configuration changes when creating an Attribute designed to store other Attributes (e.g., an Attribute of type Attribute). This affected scenarios such as

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
