---
concept_id: mobile
task_id: recipe-validate-push-notifications
title: Recipe: Validate push notifications
generated: true
---

# Recipe: Validate push notifications

A real target device receives and opens a notification through the intended route.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`
- `Page`

## Entities And Tables

- `Device`
- `Page`

## Steps

1. Verify publishing-time notification configuration.
2. Confirm the Rock transport, medium and provider configuration.
3. Request notification permission through the intended app experience.
4. Confirm the device reports notifications enabled.
5. Send to a bounded test recipient.
6. Verify receipt while signed in.
7. Where required, verify receipt while signed out.
8. Open the notification and confirm the mobile-page or detail action.
9. Test both platforms before broad release.
10. Confirm the app has been through notification-capable publishing configuration.
11. Verify the Rock communication transport and push medium.
12. Confirm the provider service-account configuration is current without exposing it.
13. Check whether the device was asked for permission and whether permission is currently enabled.
14. Verify the recipient scope and the mobile-page destination.
15. If using the updated service integration, confirm the applicable Rock Core requirement and provider coordination.
16. Test actual delivery on both target platforms; a queued communication is not proof of device receipt.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-type
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform
- https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color
- https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements
- https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
