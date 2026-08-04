---
concept_id: platform-configuration
task_id: recipe-triage-attribute-security
title: Recipe: Triage Attribute Security
generated: true
---

# Recipe: Triage Attribute Security

Complete Triage Attribute Security with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`
- `Attribute`

## Entities And Tables

- `Block`
- `Attribute`

## Steps

1. Reproduce as affected user.
2. Reproduce as admin.
3. Check base entity view permission.
4. Check attribute authorization.
5. Check block authorization.
6. Check Lava security behavior.
7. Check Rock version.
8. Decide whether to adjust security, template context, or data placement.

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
