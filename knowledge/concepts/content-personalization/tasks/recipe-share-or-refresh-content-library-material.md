---
concept_id: content-personalization
task_id: recipe-share-or-refresh-content-library-material
title: Recipe: Share or refresh Content Library material
generated: true
---

# Recipe: Share or refresh Content Library material

An item is uploaded or downloaded with its license and overwrite behavior understood.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`
- `Location`
- `Device`
- `Block`

## Entities And Tables

- `Person`
- `DataView`
- `Location`
- `Device`
- `Block`

## Steps

1. Enable Content Library features on the source or destination channel as appropriate.
2. For upload, confirm the channel license and populate the item’s Experience Level and Topic.
3. Upload only the selected item.
4. For download, start from the destination channel’s **Download from Library** action.
5. Select and download the library item.
6. Before downloading it again, identify any local edits.
7. Refresh only when overwriting those local edits is acceptable.
8. Preserve the license and required attribution in downstream presentation. (Set Up The Content Library, Library Viewer)
9. Confirm **Enable Personalization** on the exact site.
10. If browsing activity is required, confirm Enable Visitor Tracking on that site.
11. Confirm the item’s channel has personalization enabled.
12. Evaluate every segment filter area and its internal Any or All logic.
13. Refresh the persisted data view when person data has changed.
14. Run Update Personalization Data.
15. Allow for or inspect the `ROCK_SEGMENT_FILTERS` cookie affinity interval.
16. Evaluate Request Filters against the current site, device, query, cookie, IP, location, day, and time.
17. Confirm the rendering block is not set to Ignore.
18. Disable output caching for personalized output and retest in isolated sessions. (Configure Site for Personalization, Troubleshoot Personalization, Configure Content Components)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/content-management/content-library
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components
