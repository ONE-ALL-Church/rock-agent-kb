---
concept_id: roku
task_id: recipe-diagnose-a-cache-leak
title: Recipe: Diagnose A Cache Leak
generated: true
---

# Recipe: Diagnose A Cache Leak

Complete Diagnose A Cache Leak with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Device`
- `Page`

## Entities And Tables

- `Person`
- `Device`
- `Page`

## Steps

1. Load personalized page as User A.
2. Record rendered identifying content.
3. Sign out or use separate device/session as User B.
4. Load same page.
5. If User A content appears, inspect page Cacheability Type, Max Age, Max Shared Age, command-level `rockPageCacheControl`, CDN cache key, and whether the URL varies by person.
6. Switch to private/no-store or personal cache behavior.
7. Purge shared cache.
8. Retest with both users.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/lava/commands/personalize-commands
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/PersonalizationSegmentDetail/pageViewSegmentFilterBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml.cs
