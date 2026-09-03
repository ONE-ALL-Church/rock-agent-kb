---
concept_id: mobile
task_id: recipe-migrate-a-page-from-shell-v5-to-v6
title: Recipe: Migrate a page from Shell v5 to v6+
generated: true
---

# Recipe: Migrate a page from Shell v5 to v6+

The page renders correctly on .NET MAUI without silently breaking retained older clients.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Record the current and target shell versions.
2. Inventory migration-sensitive layouts, controls, effects and extensions.
3. Separate layout, scrolling, sizing, control and styling changes.
4. Replace deprecated controls only where the target shell supports the replacement.
5. If both generations must remain active, render only markup compatible with the requesting shell.
6. Verify the actual shell-version value used by the target environment before writing a version gate.
7. Deploy the shared content.
8. Test an old-shell client and a v6+ client separately.
9. Visually inspect phone and tablet layouts.
10. Identify the original shell and confirm the target is v6 or later.
11. Inventory `StackLayout`, expansion options, scrolling containers, hard size requests, `Zone`, `Frame`, `StyledView`, safe-area effects and legacy platform extensions.
12. Replace only the pattern being tested; do not apply an undifferentiated search-and-replace.
13. Use constrained grid regions where scrolling or expansion requires them.
14. Use a v6-compatible border control where appropriate.
15. Render and visually inspect every affected page on representative phone and tablet layouts.

## Do Not Assume

- Removing an expansion suffix preserves expansion
- A text replacement proves visual compatibility
- A marketing version string matches the runtime shell-version format
- Replace only the pattern being tested; do not apply an undifferentiated search-and-replace.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6
- https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
