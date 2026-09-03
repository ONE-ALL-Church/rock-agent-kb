---
concept_id: tv-apps
task_id: recipe-add-roku-navigation-with-application-context
title: Recipe: Add Roku navigation with application context
generated: true
---

# Recipe: Add Roku navigation with application context

Selecting one control sets a context value and opens a destination page that reads it.

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

1. Choose a context key and bounded value.
2. Confirm the destination page reads that key from `Context`.
3. Place `setContext` on a supported Rock control and test it independently.
4. Place `pushPage` on a supported control and test the destination independently.
5. Combine the commands with comma-separated names.
6. Keep the context and navigation parameters on the actionable control.
7. Test a fresh application session and a session where the context is changed.
8. Add `clearContext` to the appropriate reset path.

## Do Not Assume

- Context survives after the application closes.
- Public caching is safe for context-dependent output.
- Two individually failing commands will work when chained.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs/commands/utility
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/apple-tv-docs/styling/themes
- https://community.rockrms.com/developer/roku-docs/commands
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
