---
concept_id: platform-configuration
task_id: recipe-audit-a-defined-value-source-mismatch
title: Recipe: Audit a Defined Value source mismatch
generated: true
---

# Recipe: Audit a Defined Value source mismatch

Capture, storage, and reporting use the same intentional Defined Type.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Attribute`

## Steps

1. Identify the affected workflow attribute or form field.
2. Record the expected Defined Type.
3. Inspect the selector’s SQL, Lava, or other data source.
4. Resolve sample stored values to their Defined Values and parent Defined Types.
5. Inspect workflow actions that copy or transform the value.
6. Inspect downstream joins and filters.
7. Classify existing mismatches by source and date.
8. Choose the authoritative Defined Type with the process owner.
9. Prepare separate capture and historical-data corrections.
10. Re-test submission and reporting before rollout.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
