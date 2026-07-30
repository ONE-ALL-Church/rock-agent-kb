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

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels
- https://community.rockrms.com/documentation/digital-publishing/content-management
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component
- https://community.rockrms.com/lava/commands/interaction-content-channel-item-write
- https://community.rockrms.com/recipes/128
- https://community.rockrms.com/documentation/digital-publishing/personalization/localization
- https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization
