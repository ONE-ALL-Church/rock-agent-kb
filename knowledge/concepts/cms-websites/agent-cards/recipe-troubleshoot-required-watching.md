---
concept_id: cms-websites
task_id: recipe-troubleshoot-required-watching
title: Recipe: “Troubleshoot Required Watching”
generated: true
---

# Recipe: “Troubleshoot Required Watching”

RockU identifies Required Watching as part of the CMS/media learning path (Rock Media Required Watching).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Block`

## Entities And Tables

- `Person`
- `Block`

## Steps

1. Confirm media item plays.
2. Confirm required watching feature is configured.
3. Confirm current person is identified.
4. Confirm media analytics are recorded.
5. Confirm completion threshold.
6. Confirm viewer is in required audience.
7. Confirm no browser restrictions block events.
8. Confirm reports use correct media interaction data.
9. Test with a new user.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/rocku/cms/rock-media-required-watching
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts
- https://community.rockrms.com/rocku/cms/rock-media-analytics
- https://community.rockrms.com/rocku/cms/publishing-rock-media
