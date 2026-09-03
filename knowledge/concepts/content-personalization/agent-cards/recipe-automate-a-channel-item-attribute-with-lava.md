---
concept_id: content-personalization
task_id: recipe-automate-a-channel-item-attribute-with-lava
title: Recipe: Automate a channel item attribute with Lava
generated: true
---

# Recipe: Automate a channel item attribute with Lava

A scheduled job safely writes evaluated Lava output into a compatible target attribute.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Page`
- `Attribute`

## Entities And Tables

- `Schedule`
- `Page`
- `Attribute`

## Steps

1. Add a Lava-type item attribute to hold the expression.
2. Add the target item attribute with the required field type.
3. Populate and test the Lava on representative items.
4. Confirm its output is valid for the target field type.
5. Create a Content Channel Item Self Update job for the channel.
6. Set Template Key to the Lava attribute key.
7. Set Target Key to the target attribute key.
8. Run the job in a controlled test and inspect the affected item values.
9. Configure page Lava to use the target attribute.
10. Create a separate job for each additional channel. (Self Update Content Channel Items)
11. Confirm that the user has View permission on the channel; that controls whether the channel appears under `Tools > Content`.
12. Clear or adjust the status, date-range, and title filters.
13. If the item is pending, use the pending-only channel toggle to locate the channel.
14. Confirm that approvals are enabled for the channel.
15. Confirm that the user’s role has `Approve` on `Rock.Model.ContentChannelType`.
16. For missing add/delete controls, record the installed version and determine whether the Rock 19.3 fix applies. (Manage Content Items, Secure Content, Rock Core Release Notes)

## Do Not Assume

- A changed attribute default updates existing item values.
- Text that resembles a Boolean or date is valid for every target field type.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202501171949509_FixAdaptiveMessagesAttributeKey.Designer.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202501171949509_FixAdaptiveMessagesAttributeKey.cs
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content
- https://www.rockrms.com/releasenotes
