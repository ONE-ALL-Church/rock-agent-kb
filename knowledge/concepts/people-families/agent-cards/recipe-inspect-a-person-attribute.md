---
concept_id: people-families
task_id: recipe-inspect-a-person-attribute
title: Recipe: Inspect A Person Attribute
generated: true
---

# Recipe: Inspect A Person Attribute

Complete Inspect A Person Attribute with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attribute`
- `Person`
- `Block`

## Entities And Tables

- `Attribute`
- `Person`
- `Block`

## Steps

1. Attribute key.
2. Entity type.
3. Qualifier column/value.
4. Field type.
5. Categories.
6. Security.
7. Attribute value row.
8. Raw value.
9. Formatted value.
10. Typed persisted columns.
11. Lava output.
12. Does the attribute definition exist?
13. Is the entity type `Rock.Model.Person`?
14. Is the category displayed by the block?
15. Does the current user have view access?
16. Does an `AttributeValue` row exist for the person?
17. Is the field type supported by the display surface?
18. Is the value cached?
19. Is the Lava key correct?
20. Did v17.5+ attribute security affect the output?
21. Is the block's entity context actually the person?

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/lava/commands/entity-commands
- https://community.rockrms.com/lava/workflows
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_PersonAttributeValues.sql
- https://community.rockrms.com/rocku/individuals-in-rock/family-attributes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/SetPersonAttribute.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/CodeGen_AddUpdatePersonAttributes.sql
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://www.rockrms.com/releasenotes
