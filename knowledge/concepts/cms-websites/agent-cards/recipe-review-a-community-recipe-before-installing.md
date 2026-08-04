---
concept_id: cms-websites
task_id: recipe-review-a-community-recipe-before-installing
title: Recipe: “Review A Community Recipe Before Installing”
generated: true
---

# Recipe: “Review A Community Recipe Before Installing”

Complete “Review A Community Recipe Before Installing” with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Read recipe disclaimer and treat it as unreviewed community code (Search Rock Pages).
2. Identify every SQL query.
3. Identify every Lava command.
4. Identify every script/style injection.
5. Identify page/block security assumptions.
6. Identify version assumptions.
7. Test in non-production.
8. Replace broad permissions with least privilege.
9. Document local changes.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/recipes/261
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/page-builder
- https://community.rockrms.com/recipes/432
- https://community.rockrms.com/lava/commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts
- https://community.rockrms.com/rocku/cms/tabler-icons
