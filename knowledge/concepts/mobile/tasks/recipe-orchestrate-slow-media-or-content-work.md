---
concept_id: mobile
task_id: recipe-orchestrate-slow-media-or-content-work
title: Recipe: Orchestrate slow media or content work
generated: true
---

# Recipe: Orchestrate slow media or content work

Slow processing completes asynchronously and only verified output reaches public mobile content.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Workflow`
- `Person`
- `Page`
- `Block`

## Steps

1. Define explicit queued, processing, retry, failed and completed states.
2. Start the work through a workflow rather than holding the mobile interface open.
3. Record bounded retry behavior and a terminal failure state.
4. Poll or receive the provider’s completion result.
5. Validate the resulting asset.
6. Link it into mobile or web content only after completion.
7. Surface failure or review-needed status to an operator.
8. Check whether the Content block is static; static Lava has no `CurrentPerson`.
9. Verify Dynamic Content and Process Lava on Server.
10. Inspect enabled Lava commands.
11. Confirm that the shell user is authenticated.
12. If the block uses entity context, verify the entity type, page parameter name and passed GUID.
13. Provide a safe missing-context state instead of dereferencing a null entity.

## Do Not Assume

- A provider accepted the job because a request returned successfully
- A generated URL points to a complete, public-safe asset
- Workflow completion automatically publishes content

## Source Links

- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
