---
concept_id: content-personalization
task_id: recipe-configure-a-content-component-template
title: Recipe: Configure a Content Component template
generated: true
---

# Recipe: Configure a Content Component template

Editors can change structured content without editing presentation markup.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`
- `Attribute`

## Entities And Tables

- `Block`
- `Attribute`

## Steps

1. In Rock 19.0, open `Admin Tools > CMS Configuration > Content Component Templates`.
2. Copy a suitable existing template as a starting point when appropriate.
3. Build Display Lava using related content items and component settings.
4. Temporarily use `{{ 'Lava' | Debug }}` to inspect available context.
5. Remove debug output.
6. Create Content Channel Item attribute categories whose names exactly match each target template.
7. Add item attributes to the applicable categories; leave Categories blank only when the attribute should appear for every template.
8. Configure the block’s template, filters, item multiplicity, and presentation values.
9. Avoid output caching if any rendered value varies by visitor.
10. Test editing and rendering without requiring the editor to modify HTML. (Create Content Component Templates, Add Content Component Item Attributes)

## Do Not Assume

- Avoid output caching if any rendered value varies by visitor.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Cms/StructuredContent/BlockTypes/ImageDataFile.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/LinkedMediaElementBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202501171949509_FixAdaptiveMessagesAttributeKey.Designer.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/getLinkedMediaElementsResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/getLinkedMediaElementsRequestBag.d.ts
