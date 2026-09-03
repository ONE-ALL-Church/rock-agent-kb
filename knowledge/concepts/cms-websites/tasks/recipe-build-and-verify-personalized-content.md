---
concept_id: cms-websites
task_id: recipe-build-and-verify-personalized-content
title: Recipe: Build and verify personalized content
generated: true
---

# Recipe: Build and verify personalized content

Each target audience receives the intended content while authorization remains independently enforced.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`
- `Group`
- `Campus`

## Entities And Tables

- `Person`
- `Page`
- `Block`
- `Group`
- `Campus`

## Steps

1. Define the intended audience and fallback.
2. Identify the exact person or visitor data used by the rule.
3. Confirm site personalization and any required tracking settings.
4. Configure targeted and fallback content.
5. Inspect page, block, and entity authorization.
6. Configure caching so audience or context differences are preserved.
7. Test anonymous, matching, nonmatching, incomplete-data, and administrator cases.
8. Record the actor state and route used for each test.
9. Stop if targeting is the only thing preventing access to sensitive content.
10. Record the exact route, parameters, login state, person, campus, or group used in the test.
11. Confirm the site has the required personalization setting enabled.
12. Inspect the audience rule and source person data.
13. Inspect context entity type and the parameter or setter that establishes it.
14. Check fallback content.
15. Disable or vary caching in a controlled test.
16. Inspect page, block, and entity authorization separately.
17. Retest with representative actors. Personalization,

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/html-block-context
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/documentation
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
