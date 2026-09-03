---
concept_id: obsidian-development
task_id: recipe-create-a-universal-plugin-picker
title: Recipe: Create A Universal Plugin Picker
generated: true
---

# Recipe: Create A Universal Plugin Picker

A plugin field type whose C# implementation supplies structured picker data without owning UI code.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`

## Entities And Tables

- `DataView`

## Steps

1. Select the item, tree, or search picker pattern.
2. Define single- or multi-selection behavior.
3. Return the structured items or selected-item representations required by the pattern.
4. For tree or search data, implement the version-appropriate plugin API endpoint.
5. Under the supplied Rock 2.0 guidance, accept POST input from the request body and use an `api/v2/plugins/{organization-code}/...` route.
6. Apply ordinary authorization and any required grant evaluation in the endpoint.
7. Verify display, editing, stored-value conversion, and Data View filtering. (Universal Field Types)

## Do Not Assume

- The version-scoped route remains correct for every Rock version.
- Universal rendering removes the need for server authorization.
- A working picker proves stored-value compatibility.

## Source Links

- https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types
