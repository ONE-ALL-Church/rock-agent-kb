---
concept_id: platform-configuration
task_id: recipe-diagnose-attribute-field-type-mismatch
title: Recipe: Diagnose Attribute Field Type Mismatch
generated: true
---

# Recipe: Diagnose Attribute Field Type Mismatch

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Block`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Block`
- `Attribute`

## Steps

1. Inspect field type on the attribute.
2. Inspect raw stored values.
3. Compare stored format with workflow Lava field type docs.
4. Confirm consuming block supports that field type.
5. For mobile, verify supported field type list.
6. If data was stored with the wrong field type, plan migration before switching type.
7. Test old values after field type change.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/filters/attribute-filters
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/lava/workflows
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://community.rockrms.com/rocku/individuals-in-rock/person-attributes
- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
- https://community.rockrms.com/documentation/bookcontent/39
- https://community.rockrms.com/rocku/individuals-in-rock/family-attributes
- https://community.rockrms.com/rocku/individuals-in-rock/bookmarked-attributes
