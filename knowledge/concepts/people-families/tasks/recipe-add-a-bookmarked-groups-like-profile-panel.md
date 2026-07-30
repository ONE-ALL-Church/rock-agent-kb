---
concept_id: people-families
task_id: recipe-add-a-bookmarked-groups-like-profile-panel
title: Recipe: Add A Bookmarked Groups-Like Profile Panel
generated: true
---

# Recipe: Add A Bookmarked Groups-Like Profile Panel

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`

## Entities And Tables

- `Person`
- `Group`

## Steps

1. Verify group following entity type ids in live Rock.
2. Respect group security.
3. Filter by current person.
4. Filter by context person.
5. Limit output.
6. Test as users with different group access.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/rocku/individuals-in-rock
- https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members
