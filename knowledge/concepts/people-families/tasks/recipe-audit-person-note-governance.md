---
concept_id: people-families
task_id: recipe-audit-person-note-governance
title: Recipe: Audit Person Note governance
generated: true
---

# Recipe: Audit Person Note governance

Notes are categorized, visible, and consumed according to documented staff purpose and authorization.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Location`
- `Workflow`

## Entities And Tables

- `Location`
- `Workflow`

## Steps

1. Inventory the relevant Note Types without exporting note bodies.
2. Identify each Note Type’s target entity and profile location.
3. Review who can view, create, edit, and administer the type.
4. Identify sensitive categories and their intended lifecycle.
5. Review author/date metadata expectations.
6. Identify reports and workflows that consume the notes.
7. Test representative authorized and unauthorized roles.
8. Record configuration findings without reproducing sensitive content.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Workflow/Action/People/SetPersonAttribute.cs
- https://community.rockrms.com/rocku/core-concepts/note-types
- https://community.rockrms.com/rocku/workflows
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification
