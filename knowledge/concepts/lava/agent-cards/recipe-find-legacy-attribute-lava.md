---
concept_id: lava
task_id: recipe-find-legacy-attribute-lava
title: Recipe: Find Legacy Attribute Lava
generated: true
---

# Recipe: Find Legacy Attribute Lava

Source pattern: Finding and Fixing Legacy Lava.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Search Exception List for legacy Lava warnings.
2. Record example syntax.
3. Locate source page/workflow/block.
4. Search stored templates for the same pattern.
5. Replace with `| Attribute:'Key'`.
6. Verify real entity property names are not accidentally changed.
7. Retest under Fluid.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/lava-api
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks
- https://community.rockrms.com/lava/commands/cache-commands
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx.cs
- https://community.rockrms.com/rocku/cms/advanced-html-block
