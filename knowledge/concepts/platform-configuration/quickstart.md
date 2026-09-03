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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Add and verify a campus attribute](tasks/recipe-add-and-verify-a-campus-attribute.md): A secured campus attribute is visible and stores the intended value on Campus Details.
- [Recipe: Place person attributes on a profile tab](tasks/recipe-place-person-attributes-on-a-profile-tab.md): A selected category of Person Attributes appears in the intended profile location.
- [Recipe: Audit a Defined Value source mismatch](tasks/recipe-audit-a-defined-value-source-mismatch.md): Capture, storage, and reporting use the same intentional Defined Type.
- [Recipe: Operate seasonal Defined Value options](tasks/recipe-operate-seasonal-defined-value-options.md): A stable vocabulary exposes only the intended seasonal options.
- [Recipe: Stage a campus](tasks/recipe-stage-a-campus.md): A campus is configured without prematurely exposing it as active.
- [Recipe: Move an expensive dashboard calculation to scheduled storage](tasks/recipe-move-an-expensive-dashboard-calculation-to-scheduled-storage.md): The dashboard reads a verified stored result instead of rebuilding all history on every request.
- [Recipe: Secure an embedded BI report](tasks/recipe-secure-an-embedded-bi-report.md): Only appropriately authorized and licensed users can open the embedded report.
- [Recipe: Preflight a v19 configuration change](tasks/recipe-preflight-a-v19-configuration-change.md): A version-sensitive feature is enabled with its dependencies and risks tested.
- [Recipe: Design a bounded Rock agent tool](tasks/recipe-design-a-bounded-rock-agent-tool.md): An authorized tool performs one clear task and returns a controlled result.
- [Recipe: Plan a Rock upgrade as configuration change](tasks/recipe-plan-a-rock-upgrade-as-configuration-change.md): The upgrade covers technical validation, security maintenance, and staff adoption.

## High-Signal Sections

- `agent-summary` lines 18-32: Agent Summary (normal)
- `scope-and-boundaries` lines 33-46: Scope And Boundaries (normal)
- `mental-model` lines 47-64: Mental Model (high)
- `attributes-and-attribute-values-choose-the-owning-entity-first` lines 67-83: Choose the owning entity first (normal)
- `attributes-and-attribute-values-separate-the-definition-from-stored-values` lines 84-97: Separate the definition from stored values (normal)
- `attributes-and-attribute-values-present-attributes-intentionally` lines 98-103: Present attributes intentionally (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the platform-configuration guide.
- `Block`: Rock concept/entity referenced by the platform-configuration guide.
- `Campus`: Rock concept/entity referenced by the platform-configuration guide.
- `Check-in Configuration`: Rock concept/entity referenced by the platform-configuration guide.
- `DefinedType`: Rock concept/entity referenced by the platform-configuration guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the platform-configuration guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the platform-configuration guide.
- `Person`: Rock concept/entity referenced by the platform-configuration guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.

## Version Caveats

- `19.1`: Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729
- `17.2`: Fixed an issue where the list of attribute categories shown when editing a Content Channel Item attribute from the Content Channel Type Detail block included incorrect or unrelated categories. This made it difficult to a

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
