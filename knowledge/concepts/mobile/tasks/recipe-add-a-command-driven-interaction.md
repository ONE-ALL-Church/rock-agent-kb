---
concept_id: mobile
task_id: recipe-add-a-command-driven-interaction
title: Recipe: Add a command-driven interaction
generated: true
---

# Recipe: Add a command-driven interaction

A control executes a supported command with a validated parameter.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Check the command’s `M` and `C` requirements.
2. Confirm whether it needs block or page context.
3. Start with a minimal button or equivalent control.
4. Supply the simplest supported parameter form.
5. If the parameter is structured, use the documented typed object.
6. If nested controls lose the binding, reference the parent binding context explicitly.
7. Test the action and its cancellation or failure path.
8. Move the working command into the final gesture, menu or behavior.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/developer/mobile-docs/essentials/commands
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/engagement
- https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/saveFamilyOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/savedKioskConfigurationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/editFamilyResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskAvailabilityBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/addIndividualOptionsBag.d.ts
