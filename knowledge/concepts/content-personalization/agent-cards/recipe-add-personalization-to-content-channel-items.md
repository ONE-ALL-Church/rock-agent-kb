---
concept_id: content-personalization
task_id: recipe-add-personalization-to-content-channel-items
title: Recipe: Add personalization to Content Channel Items
generated: true
---

# Recipe: Add personalization to Content Channel Items

Matching visitors receive the intended filtered or prioritized content without cross-visitor cache leakage.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`
- `Group`
- `Block`

## Entities And Tables

- `Person`
- `DataView`
- `Group`
- `Block`

## Steps

1. Enable personalization on the exact site.
2. Enable Visitor Tracking if activity-based or anonymous continuity is required.
3. Create or validate the Personalization Segments and Request Filters.
4. For Person Filters, confirm the backing data views are persisted.
5. Enable personalization on the Content Channel.
6. Assign segments and/or Request Filters to each target item.
7. Remember that multiple segments are OR within their group, multiple Request Filters are OR within their group, and using both groups requires one match from each.
8. Configure the Content Channel View block as Ignore, Prioritize, or Filter.
9. Disable output caching.
10. Run Update Personalization Data when segment membership has changed.
11. Test a matching identified person, a nonmatching person, and an anonymous or request-filter context. (Personalize Content Channel Items, Troubleshoot Personalization)

## Do Not Assume

- Personalization grants permission.
- Segment membership updates in real time.
- A channel setting controls how the block applies matches.
- One browser session is enough to prove audience isolation.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/localization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages
