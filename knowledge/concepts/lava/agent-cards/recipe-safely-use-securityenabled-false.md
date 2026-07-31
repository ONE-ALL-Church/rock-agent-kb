---
concept_id: lava
task_id: recipe-safely-use-securityenabled-false
title: Recipe: Safely Use `securityenabled:'false'`
generated: true
---

# Recipe: Safely Use `securityenabled:'false'`

Source: Entity, Attributes.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Page`
- `Block`
- `Attribute`

## Steps

1. The page audience is trusted, or data is public by design.
2. Entity-level security checks are not needed for the intended output.
3. The template does not expose sensitive fields.
4. The reason is documented.
5. Performance benefit is real.
6. Entity type.
7. Page permissions.
8. Block permissions.
9. Caller identity.
10. Attributes exposed.
11. Related entity data exposed through `include` or navigation properties.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava
- https://community.rockrms.com/recipes/107
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava
- https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/commands/taglist-commands
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersRequestBag.d.ts
