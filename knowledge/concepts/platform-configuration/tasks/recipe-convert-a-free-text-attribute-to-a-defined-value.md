---
concept_id: platform-configuration
task_id: recipe-convert-a-free-text-attribute-to-a-defined-value
title: Recipe: Convert A Free-Text Attribute To A Defined Value
generated: true
---

# Recipe: Convert A Free-Text Attribute To A Defined Value

Complete Convert A Free-Text Attribute To A Defined Value with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attribute`

## Entities And Tables

- `Attribute`

## Steps

1. Inventory existing text values.
2. Normalize spelling/case.
3. Create defined type and values.
4. Create replacement attribute with defined value field type.
5. Map old values to defined values.
6. Migrate values in staging.
7. Update Lava/reports/forms.
8. Hide old attribute after validation.
9. Keep old data until retention/review is complete.
10. Delete only after references are gone and stakeholders approve.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/filters/attribute-filters
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
- https://community.rockrms.com/documentation/bookcontent/39
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/ModelMap
