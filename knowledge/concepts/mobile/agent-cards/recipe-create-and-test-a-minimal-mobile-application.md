---
concept_id: mobile
task_id: recipe-create-and-test-a-minimal-mobile-application
title: Recipe: Create and test a minimal mobile application
generated: true
---

# Recipe: Create and test a minimal mobile application

A deployed application opens in the Rock Mobile Core test shell.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`
- `Page`
- `Block`

## Entities And Tables

- `Device`
- `Page`
- `Block`

## Steps

1. Create the application under Mobile Applications.
2. Select Flyout or Tabbed navigation unless the use case specifically requires Blank.
3. Configure an organization-specific alphanumeric API key.
4. Create or open the homepage.
5. Add one Content block with minimal valid XAML.
6. Deploy the application.
7. Connect the test shell using the Application ID, public API URL and API key.
8. Launch on at least one target device.

## Do Not Assume

- Saving automatically deploys
- A localhost server is reachable
- The Rock application name becomes the store name

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-type
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/engagement
- https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements
- https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page
- https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app
- https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs
