---
concept_id: prayer-care
task_id: recipe-create-and-verify-a-group-prayer-route
title: Recipe: Create and verify a group prayer route
generated: true
---

# Recipe: Create and verify a group prayer route

New requests are permanently associated with the correct group and appear only through that group’s prayer route.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Page`

## Entities And Tables

- `Group`
- `Page`

## Steps

1. Resolve the intended group’s GUID through an authorized administrative method.
2. Construct the Prayer Request Entry URL with `GroupGuid`.
3. Verify the target group before distributing the URL.
4. Submit a non-sensitive test request.
5. Confirm the group association in administrative request details.
6. Open the Prayer Session or Prayer Card View route with the same parameter.
7. Confirm the test request appears.
8. Remove the parameter and confirm the group request is excluded.
9. Test surrounding page security with member, nonmember, and anonymous accounts.
10. Confirm the request was created with the intended `GroupGuid`.
11. Inspect the request’s group from its administrative details.
12. Remember that the association cannot be changed or removed after creation.
13. Confirm the prayer page URL carries the same `GroupGuid`.
14. Confirm the page uses Prayer Session or Prayer Card View.
15. Test as an intended group member.
16. Test as a signed-in nonmember and anonymous visitor to validate the surrounding access controls.

## Do Not Assume

- The entry page will visibly identify the group.
- An incorrect group association can be edited later.
- Possession of the GUID alone is an adequate authorization design.
- The request is associated with the wrong group; do not continue creating production requests through that URL.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts
