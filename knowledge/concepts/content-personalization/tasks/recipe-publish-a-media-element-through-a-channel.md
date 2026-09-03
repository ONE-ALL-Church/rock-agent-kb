---
concept_id: content-personalization
task_id: recipe-publish-a-media-element-through-a-channel
title: Recipe: Publish a Media Element through a channel
generated: true
---

# Recipe: Publish a Media Element through a channel

A media item appears through normal content tools with the intended player behavior and analytics.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Attribute`

## Entities And Tables

- `Page`
- `Attribute`

## Steps

1. Confirm the Media Account and provider plugin, or identify that the Local Media Account is being maintained manually.
2. Add a Media Element item attribute to the target Content Channel.
3. Either link the Media Element manually or enable channel synchronization on the Media Folder.
4. Confirm that a newly added element creates the expected item when synchronization is used.
5. In the display Lava, read the Media Element attribute’s raw value.
6. Pass the GUID to the Media Player shortcode’s `media` parameter.
7. Configure auto-resume and play-combination windows deliberately.
8. Play the media from the published page and inspect the resulting analytics.
9. If a direct variant is needed instead, select its URL from Media Files and use `src`, recognizing that this is a different integration pattern. (Publishing Media, Use With Content Channel Items)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media
- https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202501171949509_FixAdaptiveMessagesAttributeKey.Designer.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202501171949509_FixAdaptiveMessagesAttributeKey.cs
