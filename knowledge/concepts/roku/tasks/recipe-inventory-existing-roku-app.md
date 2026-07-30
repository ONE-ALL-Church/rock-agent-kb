---
concept_id: roku
task_id: recipe-inventory-existing-roku-app
title: Recipe: Inventory Existing Roku App
generated: true
---

# Recipe: Inventory Existing Roku App

Complete Inventory Existing Roku App with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`

## Entities And Tables

- `Person`
- `Page`

## Steps

1. Locate Roku/Lava application records.
2. Record application name, GUID/ID, API key presence, auth page, page-view setting, retention.
3. List pages with GUIDs, names, Show in Menu, cache settings.
4. Identify pages using `CurrentPerson`, `Context`, media commands, login, or SQL.
5. Identify enabled Lava commands.
6. Check recent exceptions.
7. Check recent interactions.
8. Produce a map of page links by scanning `rockPageGuid` references.
9. Flag public-cached personalized pages.
10. Flag YouTube media URLs.

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
