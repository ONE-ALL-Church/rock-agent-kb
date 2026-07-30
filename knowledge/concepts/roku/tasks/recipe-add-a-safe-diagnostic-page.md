---
concept_id: roku
task_id: recipe-add-a-safe-diagnostic-page
title: Recipe: Add A Safe Diagnostic Page
generated: true
---

# Recipe: Add A Safe Diagnostic Page

Do not show API keys, tokens, person IDs, email addresses, or sensitive attributes. Remove or lock down the page before production launch.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Label`
- `Page`
- `Attribute`

## Entities And Tables

- `Person`
- `Label`
- `Page`
- `Attribute`

## Steps

1. App/environment label.
2. Whether `CurrentPerson` is present.
3. Selected context keys.
4. Current time.
5. A button to test navigation.
6. A button to clear context.

## Do Not Assume

- Do not show API keys, tokens, person IDs, email addresses, or sensitive attributes.

## Source Links

- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/lava/commands/personalize-commands
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/PersonalizationSegmentDetail/pageViewSegmentFilterBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml.cs
