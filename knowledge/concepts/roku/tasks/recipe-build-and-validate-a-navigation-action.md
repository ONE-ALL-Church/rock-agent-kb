---
concept_id: roku
task_id: recipe-build-and-validate-a-navigation-action
title: Recipe: Build And Validate A Navigation Action
generated: true
---

# Recipe: Build And Validate A Navigation Action

A control that produces the intended navigation-stack behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Decide whether the destination should be pushed, replace the current page, pop the current page, or clear to root.
2. Add the chosen command to a Rock Button or ContentNode.
3. For push or replace, supply the destination page identifier and any required query parameters.
4. Decide whether a loading screen should be shown.
5. Decide whether navigation should suppress its interaction record.
6. Review navigation-level cache control.
7. Test the Back-button path from the root through the destination.

## Do Not Assume

- `pushPage` and `replacePage` produce the same Back behavior.
- A valid page identifier means the page renders successfully.
- Navigation cache control replaces review of page-level caching.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/developer/roku-docs/commands
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/SettingsPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/MicrImageHostPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml
