---
concept_id: lava
task_id: recipe-create-a-staff-friendly-link-copy-shortcode
title: Recipe: Create A Staff-Friendly Link Copy Shortcode
generated: true
---

# Recipe: Create A Staff-Friendly Link Copy Shortcode

Pattern from community recipe: a shortcode can generate a copyable public URL for staff workflows, such as registration or forms (Easy Copy Url Shortcode).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Label`
- `Workflow`
- `Page`
- `Attribute`

## Entities And Tables

- `Label`
- `Workflow`
- `Page`
- `Attribute`

## Steps

1. Use inline shortcode.
2. Parameters: `input`, `label`, `buttontext`, `class`.
3. No enabled commands unless the shortcode itself looks up records.
4. Escape input into HTML attributes.
5. If generating URLs from registration or form entities, verify page routes and public access.
6. Test internal and public contexts.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/lava-api
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/lava/commands/cache-commands
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs
- https://community.rockrms.com/lava/commands/stylesheet-commands
- https://community.rockrms.com/lava
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/lava/commands/entity-commands
