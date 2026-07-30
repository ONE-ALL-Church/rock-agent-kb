---
concept_id: people-families
task_id: recipe-identify-a-person-safely
title: Recipe: Identify A Person Safely
generated: true
---

# Recipe: Identify A Person Safely

Then verify whether any referenced workflow, attendance, communication, registration, or financial record uses `PersonAliasId` or alias GUID.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `PersonAlias`
- `Group`
- `Family`
- `Workflow`

## Entities And Tables

- `Attendance`
- `Person`
- `PersonAlias`
- `Group`
- `Family`
- `Workflow`

## Steps

1. `Person.Id`
2. `Person.Guid`
3. `PrimaryAlias.Id`
4. `PrimaryAlias.Guid`
5. all aliases
6. full name and nickname
7. birthdate
8. email
9. phone numbers
10. record status
11. connection status
12. family group id
13. family role

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/rocku/individuals-in-rock
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members
- https://community.rockrms.com/rocku/check-in/person-attributes-check-in-manager
