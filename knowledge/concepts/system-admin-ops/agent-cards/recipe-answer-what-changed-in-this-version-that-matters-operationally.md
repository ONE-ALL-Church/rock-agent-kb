---
concept_id: system-admin-ops
task_id: recipe-answer-what-changed-in-this-version-that-matters-operationally
title: Recipe: Answer “What Changed In This Version That Matters Operationally?”
generated: true
---

# Recipe: Answer “What Changed In This Version That Matters Operationally?”

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Identify current version and target version.
2. Read official release notes.
3. Extract Core, Workflow, Reporting, CMS, Security, Lava, API, and Mobile items if relevant.
4. Map each change to local features in use.
5. Produce test checklist.
6. Include source links.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/32
- https://community.rockrms.com/lava/commands/cache-commands
- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/developer/303---blast-off/exception-handling
- https://community.rockrms.com/rocku/cms/cache-tags
- https://community.rockrms.com/lava/lava-api
- https://community.rockrms.com/recipes/503
