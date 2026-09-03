---
concept_id: roku
task_id: recipe-configure-a-remote-login-journey
title: Recipe: Configure A Remote Login Journey
generated: true
---

# Recipe: Configure A Remote Login Journey

A Roku login page displays a verification code and routes correctly on success or timeout.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Label`
- `Page`

## Entities And Tables

- `Person`
- `Label`
- `Page`

## Steps

1. Confirm that the application has a website authentication page.
2. Create or identify the Roku page that will display login information.
3. Add SceneGraph elements with IDs `lgnQrPoster` and `lgnCodeLabel`.
4. Configure the login control’s login-page, timeout-page, and success-page identifiers.
5. Review the timeout duration and polling interval.
6. Decide whether successful login should clear the navigation stack.
7. Test anonymous start, QR display, successful authentication, timeout, and Back behavior.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/PersonalizationSegmentDetail/pageViewSegmentFilterBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/SettingsPage.xaml
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/BatchItemDetailPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/MicrImageHostPage.xaml
