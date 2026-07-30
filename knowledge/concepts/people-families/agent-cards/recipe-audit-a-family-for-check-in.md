---
concept_id: people-families
task_id: recipe-audit-a-family-for-check-in
title: Recipe: Audit A Family For Check-In
generated: true
---

# Recipe: Audit A Family For Check-In

Source landmarks: Check-In RockU (Check-In), `FindFamilies.cs` (source), `FindRelationships.cs` (source).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Check-in Configuration`
- `Family`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Check-in Configuration`
- `Family`
- `Workflow`
- `Attribute`

## Steps

1. Family group.
2. Members and roles.
3. Active statuses.
4. Known relationships.
5. `CanCheckin` role attributes.
6. Check-in configuration template.
7. Relationship settings.
8. Security code settings.
9. Family search type.
10. Schedules and locations.
11. Age/grade/gender restrictions.
12. Group type check-in rule.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/rocku/individuals-in-rock/family-attributes
- https://community.rockrms.com/rocku/check-in/person-attributes-check-in-manager
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
