---
concept_id: lava
task_id: recipe-inventory-lava-risk-on-a-page
title: Recipe: Inventory Lava Risk On A Page
generated: true
---

# Recipe: Inventory Lava Risk On A Page

Complete Inventory Lava Risk On A Page with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Workflow`
- `Page`
- `Block`

## Steps

1. Page ID / route.
2. Site / layout / theme.
3. Blocks containing Lava.
4. Include paths.
5. Shortcodes used.
6. Enabled commands per block.
7. Shortcode enabled commands.
8. Cache settings.
9. Security bypasses.
10. SQL usage.
11. Web requests.
12. Workflow/interaction/write commands.
13. Exceptions linked to page.
14. Recommended remediation.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/lava/commands/taglist-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/fluid/differences
- https://community.rockrms.com/recipes/393
- https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file
- https://community.rockrms.com/recipes/290
- https://community.rockrms.com/recipes/408
