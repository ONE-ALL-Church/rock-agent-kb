---
concept_id: lava
task_id: recipe-build-a-read-only-helix-active-search-page
title: Recipe: Build a read-only Helix active-search page
generated: true
---

# Recipe: Build a read-only Helix active-search page

A server-rendered page enhanced with bounded HTMX filtering.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Page`
- `Block`

## Steps

1. Render a useful first result set through the Lava Application Content block.
2. Keep the filter shell, target and loading state in the host response.
3. Use a caret route for the results endpoint.
4. Allowlist filters, sort columns, direction and page size.
5. Parameterize text search and bound the query.
6. Return only inner rows or cards from the partial endpoint.
7. Carry filter, sort and pagination state through one request contract.
8. Test anonymous, intended-role and administrator access.
9. Test first render, swaps, empty results, pagination and browser navigation.
10. Inspect console errors and responsive overflow.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://community.rockrms.com/developer/helix/overview
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupPlacement/PersonFiltersBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupPlacement/personFiltersBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersResponseBag.d.ts
