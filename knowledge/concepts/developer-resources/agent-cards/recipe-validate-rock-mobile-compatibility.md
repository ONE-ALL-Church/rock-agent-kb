---
concept_id: developer-resources
task_id: recipe-validate-rock-mobile-compatibility
title: Recipe: Validate Rock Mobile compatibility
generated: true
---

# Recipe: Validate Rock Mobile compatibility

Determine whether a feature is supported by the exact Core/Shell pair.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`

## Entities And Tables

- `Device`

## Steps

1. Record the target feature.
2. Read its minimum `C` requirement.
3. Read its minimum `M` requirement.
4. Record the installed Rock Core version.
5. Record the actual Mobile Shell version on the test device.
6. Compare both dimensions.
7. If upgrading from V5 or earlier to V6 or later, identify XAML affected by the Xamarin Forms to .NET MAUI transition.
8. Test the affected layouts and controls on the supported devices.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer
