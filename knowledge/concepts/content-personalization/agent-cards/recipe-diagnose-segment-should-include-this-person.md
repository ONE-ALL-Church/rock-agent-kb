---
concept_id: content-personalization
task_id: recipe-diagnose-segment-should-include-this-person
title: Recipe: Diagnose “segment should include this person”
generated: true
---

# Recipe: Diagnose “segment should include this person”

Complete Diagnose “segment should include this person” with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Group`
- `Page`
- `Attribute`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Group`
- `Page`
- `Attribute`

## Steps

1. Person record demographics and attributes.
2. Group/registration/connection data used by the segment.
3. Whether the segment is person-data based or browsing-history based.
4. Visitor tracking if browsing history is involved.
5. Segment active state.
6. `Update Personalization Data` last run.
7. Current membership list from the Personalization Segments page.
8. `PersonAliasPersonalization` only if safe and appropriate to inspect.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages
