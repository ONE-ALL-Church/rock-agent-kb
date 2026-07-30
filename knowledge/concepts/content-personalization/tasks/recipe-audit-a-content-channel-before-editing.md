---
concept_id: content-personalization
task_id: recipe-audit-a-content-channel-before-editing
title: Recipe: Audit a content channel before editing
generated: true
---

# Recipe: Audit a content channel before editing

Do not change anything until you know which pages and workflows depend on the channel.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Channel name, ID/GUID, type, and purpose.
2. Channel item count by status.
3. Item attributes and required fields.
4. Channel attributes.
5. Personalization enabled state.
6. RSS enabled state.
7. Content Library enabled state.
8. Security rules for view/edit/approve/delete/admin.
9. Blocks/pages that render it.
10. Collection memberships.
11. Jobs/workflows that update it.
12. Recent release caveats relevant to the deployed version.

## Do Not Assume

- Do not change anything until you know which pages and workflows depend on the channel.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/content-management
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels
- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component
- https://community.rockrms.com/lava/commands/interaction-content-channel-item-write
- https://community.rockrms.com/recipes/128
- https://community.rockrms.com/documentation/digital-publishing/personalization/localization
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
