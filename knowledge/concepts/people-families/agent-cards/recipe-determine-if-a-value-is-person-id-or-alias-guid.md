---
concept_id: people-families
task_id: recipe-determine-if-a-value-is-person-id-or-alias-guid
title: Recipe: Determine If A Value Is Person Id Or Alias Guid
generated: true
---

# Recipe: Determine If A Value Is Person Id Or Alias Guid

Complete Determine If A Value Is Person Id Or Alias Guid with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Workflow`
- `Attribute`

## Steps

1. If it came from a workflow Person attribute `RawValue`, treat it as person alias GUID until proven otherwise (Workflows and Lava).
2. If it is an integer ending in `PersonAliasId`, resolve through `PersonAlias`.
3. If it is an integer named `PersonId`, verify whether it is a current person id.
4. If it is a GUID, compare to `Person.Guid` and `PersonAlias.Guid`.
5. If the record survived a merge, search aliases.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/commands/entity-commands
- https://community.rockrms.com/lava/filters/person-filters
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/rocku/individuals-in-rock/family-attributes
