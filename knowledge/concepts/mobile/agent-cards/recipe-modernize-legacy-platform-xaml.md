---
concept_id: mobile
task_id: recipe-modernize-legacy-platform-xaml
title: Recipe: Modernize Legacy Platform XAML
generated: true
---

# Recipe: Modernize Legacy Platform XAML

The deprecation basis is the On Device Platform doc (On Device Platform).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`

## Entities And Tables

- `Device`

## Steps

1. Search XAML for legacy Rock OnDevicePlatform usage.
2. Confirm app is v6+ MAUI.
3. Replace with MAUI built-in platform extension where appropriate.
4. Verify CSS alternative if styling-only.
5. Test iOS and Android.
6. Deploy.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu
- https://community.rockrms.com/developer/mobile-docs
- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6
