---
concept_id: roku
task_id: recipe-review-a-roku-related-lava-endpoint
title: Recipe: Review A Roku-Related Lava Endpoint
generated: true
---

# Recipe: Review A Roku-Related Lava Endpoint

A public-safe inventory of the endpoint’s exposure, template, and enabled capabilities.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Identify whether the Roku flow actually uses a custom Lava webhook.
2. Record its route and purpose without exposing secrets.
3. Inspect how requests are authenticated or constrained.
4. Review the response template for sensitive data.
5. Inventory enabled Lava commands.
6. Confirm whether the endpoint relies on any organization-specific configuration.
7. Report unprotected or over-capable exposure as a security risk.
8. Stop before enabling commands, changing security, rotating keys, or editing the template unless explicitly authorized.

## Do Not Assume

- The Roku application API key protects the Lava webhook.
- Page security automatically applies to the webhook.
- Another installation shares the inspected configuration.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/lava/lava-api
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/SettingsPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/MicrImageHostPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml
