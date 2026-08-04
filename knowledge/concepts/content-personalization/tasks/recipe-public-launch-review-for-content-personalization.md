---
concept_id: content-personalization
task_id: recipe-public-launch-review-for-content-personalization
title: Recipe: Public launch review for content personalization
generated: true
---

# Recipe: Public launch review for content personalization

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`

## Entities And Tables

- `Person`
- `Page`

## Steps

1. Disable any Lava debug output.
2. Verify anonymous experience.
3. Verify logged-in target experiences.
4. Verify non-target experience.
5. Verify fallback content.
6. Verify assets load without authenticated sessions.
7. Verify RSS/social metadata if used.
8. Verify no private content appears in feed, page source, API output, or image URLs.
9. Verify content item delete/edit permissions.
10. Verify jobs have run.
11. Verify release notes for known content/personalization bugs.
12. Verify public repo/site hardening if publishing generated docs.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages
