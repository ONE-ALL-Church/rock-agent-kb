---
concept_id: helix
task_id: recipe-add-observability-to-a-complex-endpoint
title: Recipe: Add Observability To A Complex Endpoint
generated: true
---

# Recipe: Add Observability To A Complex Endpoint

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Find the slow logical block.
2. Wrap only that block with `{% observe %}`.
3. Use a stable name.
4. Add organization-prefixed tags.
5. Escape tag values if dynamic.
6. Compare traces before/after.
7. Remove noisy instrumentation if it does not help.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications
- https://community.rockrms.com/developer/helix/lava-applications/observability
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationList/lavaApplicationListOptionsBag.d.ts
