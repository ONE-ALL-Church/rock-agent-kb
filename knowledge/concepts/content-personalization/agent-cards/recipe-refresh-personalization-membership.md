---
concept_id: content-personalization
task_id: recipe-refresh-personalization-membership
title: Recipe: Refresh personalization membership
generated: true
---

# Recipe: Refresh personalization membership

A persisted segment and its browser-facing membership state reflect current person data.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`

## Entities And Tables

- `Person`
- `DataView`

## Steps

1. Identify the segment and each persisted data view used by its Person Filter.
2. Refresh the underlying persisted data view.
3. Run Update Personalization Data.
4. Inspect the segment’s current person list.
5. Account for the `ROCK_SEGMENT_FILTERS` cookie affinity duration.
6. Retest with the intended person and site.
7. If the result remains wrong, evaluate every filter area and its Any or All logic. (Update Personalization Job, Troubleshoot Personalization)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
