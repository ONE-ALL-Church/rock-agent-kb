---
concept_id: lava
task_id: recipe-review-a-shortcode-for-production
title: Recipe: Review A Shortcode For Production
generated: true
---

# Recipe: Review A Shortcode For Production

Complete Review A Shortcode For Production with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`
- `Attribute`

## Entities And Tables

- `Block`
- `Attribute`

## Steps

1. `Name`
2. `TagName`
3. `TagType`
4. `IsActive`
5. `IsSystem`
6. `Categories`
7. `Documentation`
8. `Markup`
9. `Parameters`
10. `EnabledLavaCommands`
11. `ShortcodeScopeBehavior`
12. Entity attributes
13. Call sites
14. Version requirements
15. Security bypasses
16. Cache behavior
17. Keep as-is.
18. Narrow commands.
19. Fix parameters.
20. Add documentation.
21. Convert to block/inline only if no callers exist or all callers can be updated.
22. Replace SQL with entity command or parameterized SQL.
23. Add tests or staging validation.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks
- https://community.rockrms.com/recipes/107
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/lava/tags/include-tags
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava
- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/lava/shortcodes/types-of-shortcodes
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WebRequestBlock.cs
