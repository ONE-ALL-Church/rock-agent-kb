---
concept_id: tv-apps
task_id: recipe-decide-cache-policy
title: Recipe: Decide Cache Policy
generated: true
---

# Recipe: Decide Cache Policy

Verify actual headers and CDN behavior in the live environment.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Campus`
- `Page`

## Entities And Tables

- `Person`
- `Campus`
- `Page`

## Steps

1. Page is anonymous.
2. Content is identical for all users.
3. No person/campus-sensitive data is included.
4. Stale content is acceptable for the configured duration.
5. Page uses `CurrentPerson`.
6. Page uses person-specific watch progress.
7. Page contains private media.
8. Page uses auth state.
9. Page uses context that should not leak across viewers.
10. Page changes frequently.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs
- https://community.rockrms.com/developer/roku-docs/commands/media
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
