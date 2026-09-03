---
concept_id: roku
task_id: recipe-add-campus-or-other-application-context
title: Recipe: Add Campus Or Other Application Context
generated: true
---

# Recipe: Add Campus Or Other Application Context

A selected value remains available to pages until the application closes or the context is cleared.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Choose a stable context key.
2. Add `setContext` to the selection control.
3. Supply the selected value.
4. If navigation should immediately follow, comma-chain `setContext` and `pushPage`.
5. Read the value from the page’s `Context` merge field.
6. Add an explicit `clearContext` path when the selection must be reset.
7. Test application-close behavior separately.

## Do Not Assume

- A context value persists after the application closes.
- Comma-chained commands provide transactional rollback.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs/commands/utility
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/developer/roku-docs/commands
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/SettingsPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/MicrImageHostPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml.cs
