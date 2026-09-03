---
concept_id: content-personalization
task_id: recipe-build-and-refresh-a-content-collection
title: Recipe: Build and refresh a Content Collection
generated: true
---

# Recipe: Build and refresh a Content Collection

Multiple channels or calendars are searchable together with deliberate filtering, ranking, and security boundaries.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Block`
- `Attribute`

## Steps

1. Confirm an active Universal Search index component.
2. Create or select the collection under `Admin Tools > CMS Configuration > Content Collections`.
3. Add the required content channels and calendars.
4. Select the source attributes that should be indexed.
5. Enable and arrange the collection’s search filters.
6. Configure trending only if interaction logging exists on the item-viewing surfaces.
7. Configure segment and Request Filter evaluation if personalized ranking is required.
8. Rebuild the index.
9. Configure a Content Collection View block with the collection, result count, search behavior, filters, templates, sort orders, and personalization boost.
10. Verify that each visible filter is enabled in both the collection and block.
11. Audit every source for restricted content before public display. (Set Up Content Collections, Content Collection View)
12. Confirm the expected channel or calendar is a source in the collection.
13. Confirm the needed item attributes were selected for indexing.
14. Run `Index Content Collections` or use Rebuild Index after same-day changes.
15. Confirm filters are enabled both in the collection and in the Content Collection View block.
16. Recheck the block’s selected collection, search-on-load behavior, result count, and templates.
17. If personalization is involved, verify site personalization and the block’s boost configuration.
18. Stop before exposing the collection if it contains restricted items; individual item security is not enforced by the collection. (Troubleshoot Content Collections, Content Collection View)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections
