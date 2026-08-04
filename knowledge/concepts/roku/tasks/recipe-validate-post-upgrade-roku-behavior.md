---
concept_id: roku
task_id: recipe-validate-post-upgrade-roku-behavior
title: Recipe: Validate Post-Upgrade Roku Behavior
generated: true
---

# Recipe: Validate Post-Upgrade Roku Behavior

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

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

1. Confirm Roku pages render.
2. Confirm Lava engine behavior.
3. Check attribute access changes.
4. Check enabled Lava commands.
5. Verify login QR flow.
6. Verify media playback.
7. Verify interactions and watch maps.
8. Verify cache behavior.
9. Review release notes for Roku, Lava, API, CMS, media, and security changes.
10. Update internal docs with changed behavior.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/lava/commands/interaction-write
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/developer/roku-docs/resources/controls/button
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/RockCloudPrint/Rock.CloudPrint.Desktop/Pages/DashboardPage.xaml.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/CheckScannerUtility/CheckScannerUtility/LoginPage.xaml
