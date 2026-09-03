---
concept_id: helix
task_id: recipe-build-a-read-only-htmx-result-fragment
title: Recipe: Build a read-only HTMX result fragment
generated: true
---

# Recipe: Build a read-only HTMX result fragment

A page-hosted query interaction that returns only authorized display content.

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

1. Create or select a Lava Application with a documented name, description, and slug.
2. Add a GET endpoint for the result fragment.
3. Configure its security mode for the intended audience.
4. Enable only the Lava commands required to read and render the result.
5. Validate and allowlist all query values.
6. Check the caller’s right to view each protected entity.
7. Add a Lava Application Content block and link it to the application.
8. Render useful initial content.
9. Add the HTMX request using a caret route and an explicit target.
10. Test empty, invalid, unauthorized, and representative result states.
11. Inspect endpoint traces and database calls.

## Do Not Assume

- IdKeys or GUIDs provide authorization.
- Read-only behavior makes private fields safe to expose.
- A default cache policy is appropriate for person-specific output.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/developer/helix/overview/security
- https://community.rockrms.com/developer/helix/lava-applications/observability
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationList/lavaApplicationListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs
