---
concept_id: helix
task_id: recipe-inspect-an-existing-helix-application-before-changing-it
title: Recipe: Inspect an existing Helix application before changing it
generated: true
---

# Recipe: Inspect an existing Helix application before changing it

A bounded map of the current application flow and its security-sensitive surfaces.

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

1. Record the installed Rock version and whether Helix is core- or plugin-provided.
2. Inspect the Lava Application’s name, description, slug, configuration rigging, activity state, and security.
3. Identify every linked Lava Application Content block.
4. Inventory the application’s endpoints by name, slug, method, and activity state.
5. For each endpoint, record security mode, enabled commands, caching, code-template purpose, and any exposed rate-limit or CSRF setting.
6. Trace each page action to its endpoint and target element.
7. Identify which endpoints read, mutate, delete, or launch other work.
8. Review representative observability activities before altering behavior.

## Do Not Assume

- Page security protects the endpoint.
- Administrator success proves role access.
- A staff-session route is suitable for public use.
- Settings observed in another installation exist here.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/developer/helix/lava-applications
- https://community.rockrms.com/developer/helix/lava-applications/observability
- https://community.rockrms.com/developer/helix/lava-applications/endpoints
- https://community.rockrms.com/developer/helix/overview/security
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationList/lavaApplicationListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs
