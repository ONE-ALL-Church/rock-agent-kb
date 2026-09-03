---
concept_id: roku
task_id: recipe-prepare-a-roku-development-readiness-review
title: Recipe: Prepare A Roku Development Readiness Review
generated: true
---

# Recipe: Prepare A Roku Development Readiness Review

A bounded determination of whether page development can begin.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Confirm the target Rock version.
2. Verify that Roku support is applicable to that version.
3. Confirm whether a development application was requested from the Rock Core team.
4. Inspect the application record for API-key presence, authentication page, page-view tracking, and retention duration.
5. Record missing prerequisites without displaying secrets.
6. Stop before requesting credentials, changing configuration, or submitting an external request unless authorized.

## Do Not Assume

- An upgrade provisions a Roku development application.
- A populated API-key field proves connectivity.
- A selected authentication page proves QR login.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/developer/roku-docs/getting-started
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/SettingsPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/MicrImageHostPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml.cs
