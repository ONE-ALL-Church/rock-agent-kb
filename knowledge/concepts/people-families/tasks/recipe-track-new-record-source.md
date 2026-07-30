---
concept_id: people-families
task_id: recipe-track-new-record-source
title: Recipe: Track New Record Source
generated: true
---

# Recipe: Track New Record Source

Complete Track New Record Source with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Family`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `Family`
- `Workflow`
- `Attribute`

## Steps

1. Check Rock version.
2. If v18.1+, inspect Person Record Source configuration for Add Family, Get Person From Fields, and Check-in new records (Rock Core Release Notes).
3. Inspect person created date and created by alias.
4. Inspect history.
5. Inspect local "How Created" attributes only if defined.
6. Inspect source workflows and registrations.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/commands/entity-commands
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/rocku/individuals-in-rock
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://community.rockrms.com/developer/303---blast-off/attributes
