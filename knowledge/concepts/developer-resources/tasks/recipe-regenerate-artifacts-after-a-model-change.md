---
concept_id: developer-resources
task_id: recipe-regenerate-artifacts-after-a-model-change
title: Recipe: Regenerate artifacts after a model change
generated: true
---

# Recipe: Regenerate artifacts after a model change

Produce synchronized C# and Obsidian view models.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Make the bounded model change.
2. Build Rock.
3. Confirm which DLL the generator will use and that it is current.
4. Run model generation.
5. Add new generated C# files to their projects.
6. Build Rock and the view-model project.
7. Run Obsidian view-model generation in preview mode.
8. Review every proposed change.
9. Save only the expected files.
10. Rebuild and run relevant tests.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes
