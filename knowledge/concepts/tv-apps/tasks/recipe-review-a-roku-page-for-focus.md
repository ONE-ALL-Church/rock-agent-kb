---
concept_id: tv-apps
task_id: recipe-review-a-roku-page-for-focus
title: Recipe: Review A Roku Page For Focus
generated: true
---

# Recipe: Review A Roku Page For Focus

Complete Review A Roku Page For Focus with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Label`
- `Page`

## Entities And Tables

- `Group`
- `Label`
- `Page`

## Steps

1. `Rock:Page` exists as page root.
2. `initialFocus` references an actual control ID.
3. Horizontal controls are grouped.
4. Vertical controls are grouped.
5. IDs are unique.
6. Buttons have enough width for labels.
7. RowList has valid content hierarchy.
8. Back navigation path is clear.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/apple-tv-docs
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rocklabel
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/lava/lava-api
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs
