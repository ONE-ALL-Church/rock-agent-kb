---
concept_id: lava
task_id: recipe-prepare-a-lava-entity-write
title: Recipe: Prepare a Lava entity write
generated: true
---

# Recipe: Prepare a Lava entity write

An idempotent, verifiable single-entity change plan.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attribute`

## Entities And Tables

- `Attribute`

## Steps

1. Confirm Modify Entity is available on the target version.
2. Resolve the target by a stable identifier.
3. Separate create and update paths.
4. Supply values in each property or attribute’s required stored format.
5. Execute one parent write.
6. Check `ModifyResult.Success`.
7. Capture the canonical returned ID or GUID immediately.
8. Read the entity back.
9. Only then perform dependent writes.
10. Render a bounded diagnostic summary without private data.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava
- https://community.rockrms.com/lava/commands/modify-entity
- https://community.rockrms.com/lava/commands/entity-commands
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/lava/commands/workflow-activate-commands
