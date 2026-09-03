---
concept_id: prayer-care
task_id: recipe-validate-outreach-toolbox-for-prayer-touchpoints
title: Recipe: Validate Outreach Toolbox for prayer touchpoints
generated: true
---

# Recipe: Validate Outreach Toolbox for prayer touchpoints

A signed-in mobile user can see, complete, and receive reminders for an assigned prayer touchpoint.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`
- `Page`
- `Group`
- `Block`

## Entities And Tables

- `Device`
- `Page`
- `Group`
- `Block`

## Steps

1. Confirm the target server and mobile versions.
2. Confirm the Outreach Toolbox page is placed in the mobile shell.
3. Verify authentication and permissions for a pilot user.
4. Complete onboarding with known assignment days and reminder preferences.
5. Configure a test contact and prayer cadence.
6. Verify the dashboard shows the due action.
7. Complete the touchpoint and inspect its history.
8. Configure and run the applicable reminder job.
9. Verify the push notification on the target device.
10. Review who can see contact details, history, and pulse updates.
11. Confirm the request saved successfully.
12. Inspect whether it is approved. If automatic approval is disabled, approve it through the administrative request list.
13. Confirm it is active and inspect its expiration date.
14. Check whether the team block is scoped to a different category.
15. Check whether Public Only is enabled while the request is non-public.
16. Inspect its flag count and whether the configured threshold unapproved it.
17. Determine whether it is group-associated. A normal session without `GroupGuid` excludes group requests.
18. Inspect the block’s maximum-results and ordering settings.
19. Test the page using the affected team member’s exact permissions.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts
- https://www.youtube.com/shorts/c6T9Ha13jKE
- https://www.youtube.com/watch?v=LNcx8t0mlQ4
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests
