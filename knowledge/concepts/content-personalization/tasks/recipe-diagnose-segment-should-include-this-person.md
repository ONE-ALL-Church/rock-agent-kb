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

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/content-management
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component
- https://community.rockrms.com/lava/commands/interaction-content-channel-item-write
- https://community.rockrms.com/recipes/128
- https://community.rockrms.com/documentation/digital-publishing/personalization/localization
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes
