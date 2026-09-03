---
concept_id: content-personalization
task_id: recipe-publish-a-governed-content-channel-item
title: Recipe: Publish a governed Content Channel Item
generated: true
---

# Recipe: Publish a governed Content Channel Item

An item is structurally complete, correctly scheduled, reviewable, and eligible for display.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Schedule`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Schedule`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Identify the destination channel and inspect its channel type, item attributes, date mode, approval requirement, and personalization setting.
2. Enter the item through `Tools > Content` unless channel administration is required.
3. Populate the required fields and structured item attributes.
4. Set Start and optional Expire dates according to the channel type.
5. Add or create child items only after confirming the allowed child channels.
6. If the channel requires approval, leave or move the item into the appropriate review state and have a user with Approval permission complete approval.
7. Inspect the exact rendering block’s channel, status, filters, ordering, and template.
8. Verify the public result in both pre-start or expired and active conditions as applicable. (Add Content Items, Manage Content Items)
9. Confirm that the expected page uses the intended Content Channel View or Content Channel Item View block and the intended channel.
10. Check the item’s approval status and whether the channel requires approval.
11. Check Start and Expire dates using the date model defined by the channel type.
12. Inspect block status filters, item filters, context filters, route parameters, and ordering.
13. If the item contains Lava, verify that the item-view block processes `Item.Content` with `RunLava`.
14. If personalization is enabled, inspect the channel setting, item assignments, and the block’s Ignore, Prioritize, or Filter choice.
15. Check View and Interact permissions separately.
16. If the content is being rendered through RSS, test without current-person or page-context assumptions. (Add a Content Channel Item, Content Channel View Block, Personalize Content Channel Items)

## Do Not Assume

- Saving means approved.
- Approval means in date.
- In-date means permitted.
- A valid item means the page block selects it.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item
