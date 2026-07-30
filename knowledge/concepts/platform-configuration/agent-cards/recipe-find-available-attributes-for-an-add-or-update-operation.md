---
concept_id: platform-configuration
task_id: recipe-find-available-attributes-for-an-add-or-update-operation
title: Recipe: Find Available Attributes For An Add Or Update Operation
generated: true
---

# Recipe: Find Available Attributes For An Add Or Update Operation

The AvailableAttributes developer docs explicitly distinguish available attribute definitions from actual values and note the add-operation case where no existing entity exists (AvailableAttributes Tools).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attribute`

## Entities And Tables

- `Attribute`

## Steps

1. Identify the entity type.
2. If updating, load the existing entity.
3. If adding, initialize the entity context enough to determine available attributes.
4. Retrieve attribute definitions, not values.
5. Capture key, name, field type, required status, default, qualifiers, and allowed values.
6. Ask for or construct values in the correct raw format.
7. Submit values by key or expected API shape.
8. Re-read the entity and verify stored values.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/filters/attribute-filters
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor
- https://community.rockrms.com/documentation/bookcontent/39
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/individuals-in-rock/person-attributes
