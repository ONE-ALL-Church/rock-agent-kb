---
concept_id: helix
task_id: recipe-review-a-community-recipe-before-use
title: Recipe: Review A Community Recipe Before Use
generated: true
---

# Recipe: Review A Community Recipe Before Use

Complete Review A Community Recipe Before Use with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Page`
- `Block`

## Entities And Tables

- `Group`
- `Page`
- `Block`

## Steps

1. Read the recipe as an example, not an authority.
2. Verify Rock version compatibility.
3. Replace all entity type IDs with live instance values.
4. Replace all group, role, page, block, and defined value IDs with live values.
5. Review enabled Lava Commands.
6. Review endpoint Execute permissions.
7. Run in a non-production environment.
8. Test with a low-privilege account.
9. Add observability.
10. Document rollback.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications
- https://community.rockrms.com/developer/helix/lava-applications/observability
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationList/lavaApplicationListOptionsBag.d.ts
- https://community.rockrms.com/page/3761
