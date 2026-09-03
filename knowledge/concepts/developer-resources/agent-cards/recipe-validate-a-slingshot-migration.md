---
concept_id: developer-resources
task_id: recipe-validate-a-slingshot-migration
title: Recipe: Validate a Slingshot migration
generated: true
---

# Recipe: Validate a Slingshot migration

Demonstrate that imported data supports the intended Rock workflows.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Workflow`

## Entities And Tables

- `Attendance`
- `Workflow`

## Steps

1. Define the source system, record types, and time range.
2. Produce the `.slingshot` file.
3. Record its Foreign System Key and migration scope.
4. Import into a non-production validation environment.
5. Monitor the import and capture errors without exposing private records.
6. Validate representative entities and relationships.
7. Configure downstream Rock features that do not become operational from import alone.
8. Test the actual workflows and reports.
9. Record cleanup needs and obtain review for any scripts.
10. Repeat the migration from a known starting state before scheduling production work.

## Do Not Assume

- Imported rows are correctly configured.
- Attendance presence means analytics is ready.
- Cleanup SQL is portable across installations.
- Configure downstream Rock features that do not become operational from import alone.

## Source Links

- https://community.rockrms.com/developer/slingshot/about-slingshot
