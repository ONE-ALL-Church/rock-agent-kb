---
concept_id: serving-volunteer-ops
task_id: recipe-safely-customize-a-volunteer-facing-page
title: Recipe: Safely Customize A Volunteer-Facing Page
generated: true
---

# Recipe: Safely Customize A Volunteer-Facing Page

The external schedule recipe demonstrates why copied pages may be necessary when serving teams share a toolbox with other group categories (View Serving Schedule on External Page).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Schedule`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Group`
- `Schedule`
- `Page`
- `Block`

## Steps

1. Identify whether the page is shared.
2. Copy shared pages when customization is serving-specific.
3. Limit page data to current person or authorized group.
4. Avoid exposing private contact fields.
5. Use safe parameters.
6. Test with non-admin account.
7. Document page ids and block settings.
8. Keep Lava and SQL in source control where possible.

## Do Not Assume

- Avoid exposing private contact fields.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/rocku/groups/group-types
- https://community.rockrms.com/rocku/groups/group-scheduling-overview
- https://community.rockrms.com/recipes/459
- https://community.rockrms.com/rocku/groups/group-details
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
- https://community.rockrms.com/rocku/groups/group-requirements
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/recipes/530/dynamic-sender-for-group-scheduling-confirmations-coordinator-fallback
