---
concept_id: prayer-care
task_id: recipe-enable-prayer-comment-digests
title: Recipe: Enable prayer-comment digests
generated: true
---

# Recipe: Enable prayer-comment digests

Allowed comments are delivered to request-specific email addresses within the intended category scope.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Schedule`

## Entities And Tables

- `Person`
- `Schedule`

## Steps

1. Configure a scheduled job using the Send Prayer Comments job type.
2. Select the Prayer Request Comments Digest system communication.
3. For all categories, leave Prayer Categories blank and enable Include Child Categories.
4. For a narrower scope, select categories and explicitly choose child inclusion.
5. Decide whether sent communications should be saved.
6. Confirm test requests have Allow Comments enabled.
7. Add a non-sensitive test comment.
8. Run the job in a controlled test.
9. Verify the digest includes the original request and expected comments.
10. Verify delivery to the email stored on the request.
11. Run the job again after adding another comment and confirm it sends only comments added since the prior run.
12. Confirm the Send Prayer Comments job exists, is configured, and has run successfully.
13. Confirm the request has Allow Comments enabled.
14. Inspect the job’s category selection and Include Child Categories setting.
15. Inspect the email stored on the prayer request rather than relying on the person’s current profile email.
16. Confirm that a new comment exists within the job’s unsent window.
17. Inspect the configured system communication and outbound communication provider.
18. Determine whether Save Communications is enabled before expecting a saved communication record.
19. Perform a bounded test with non-sensitive content and verify receipt.

## Do Not Assume

- The person profile’s current email is the destination.
- Comment permission and digest eligibility are the same control.
- An unsaved communication was not sent.

## Source Links

- https://www.youtube.com/watch?v=LNcx8t0mlQ4
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestDetailAddPersonResponseBag.d.ts
- https://www.youtube.com/shorts/c6T9Ha13jKE
- https://community.rockrms.com/recipes/72
