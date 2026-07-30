---
concept_id: roku
task_id: recipe-convert-a-static-media-list-to-dynamic-rowlist
title: Recipe: Convert A Static Media List To Dynamic RowList
generated: true
---

# Recipe: Convert A Static Media List To Dynamic RowList

Complete Convert A Static Media List To Dynamic RowList with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Attribute`

## Entities And Tables

- `Page`
- `Attribute`

## Steps

1. Identify content source and required fields.
2. Use entity command or approved data source.
3. Build rows in Lava.
4. Render one RowList content root.
5. Use `Rock:ContentNode` for rows/items.
6. Attach `playVideo` or `pushPage`.
7. Escape dynamic XML attribute values.
8. Set a conservative cache policy.
9. Test focus and playback.
10. Verify interactions.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml.cs
