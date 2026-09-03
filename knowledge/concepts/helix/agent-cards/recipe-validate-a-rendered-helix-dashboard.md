---
concept_id: helix
task_id: recipe-validate-a-rendered-helix-dashboard
title: Recipe: Validate a rendered Helix dashboard
generated: true
---

# Recipe: Validate a rendered Helix dashboard

Evidence that source targeting, authorization, data semantics, interaction behavior, and responsive layout all work in the actual page context.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Label`
- `Page`
- `Block`

## Entities And Tables

- `Label`
- `Page`
- `Block`

## Steps

1. Confirm the saved application, endpoint, and Content block source matches the intended source.
2. Open the rendered page as an unauthorized visitor.
3. Test as the intended role.
4. Test as an administrator, but record that result separately.
5. Assert known totals or invariants and representative rows.
6. Exercise each filter, sort, refresh, and empty state.
7. Inspect visible errors, hidden Lava error surfaces, network failures, and console errors.
8. Test narrow and wide layouts for clipped labels, unintended internal scrolling, and unbounded horizontal overflow.
9. Inspect endpoint traces for representative requests.

## Do Not Assume

- Source equality proves rendered behavior.
- Administrator access proves intended-role access.
- A successful HTTP response proves correct data semantics.
- Desktop rendering proves responsive readiness.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/developer/helix/overview/security
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationList/lavaApplicationListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard
