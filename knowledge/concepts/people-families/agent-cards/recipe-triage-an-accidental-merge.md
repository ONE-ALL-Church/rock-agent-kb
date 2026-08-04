---
concept_id: people-families
task_id: recipe-triage-an-accidental-merge
title: Recipe: Triage An Accidental Merge
generated: true
---

# Recipe: Triage An Accidental Merge

Complete Triage An Accidental Merge with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `Group`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Attendance`
- `Person`
- `Group`
- `Workflow`
- `Attribute`

## Steps

1. Do not create more edits until evidence is collected.
2. Identify merge timestamp and survivor.
3. Collect aliases before and after merge.
4. Inspect history and affected person surfaces.
5. Restore backup to separate database if recovery is required.
6. Use preview/rollback transaction for any script-based recovery.
7. Validate group membership, giving, attendance, attributes, notes, workflows, logins, and aliases.
8. Prefer expert review.

## Do Not Assume

- Do not create more edits until evidence is collected.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/lava/commands/entity-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs
