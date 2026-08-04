---
concept_id: content-personalization
task_id: recipe-verify-content-interactions
title: Recipe: Verify content interactions
generated: true
---

# Recipe: Verify content interactions

Complete Verify content interactions with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Block`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Block`

## Steps

1. Is the item rendered by a block that logs views?
2. Is a Lava command logging interactions manually?
3. Does the command specify `contentchannelitemid`?
4. Are operation and summary within documented limits?
5. Is the current person/person alias resolved?
6. Is the Rock version patched for content channel item entity type logging?
7. Are interactions visible in `Tools > Interactions`?

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages
