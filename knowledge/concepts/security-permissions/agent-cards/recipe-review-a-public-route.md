---
concept_id: security-permissions
task_id: recipe-review-a-public-route
title: Recipe: Review A Public Route
generated: true
---

# Recipe: Review A Public Route

Sources: IdKey guidance, Helix security, and remote Lava warnings (Rock Security, Helix Security, Using Lava Remotely).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Route parameters.
2. Raw IDs vs IdKeys/GUIDs.
3. Page View.
4. Block View.
5. Entity-specific authorization.
6. Lava commands.
7. API calls in browser.
8. File/document links.
9. Query string manipulation.
10. Anonymous test.
11. Low-privilege authenticated test.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks
- https://community.rockrms.com/recipes/441
- https://community.rockrms.com/developer/303---blast-off/rock-security
- https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-auth0
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-entra
- https://community.rockrms.com/developer/developer-codex/coding-standards/rock-architecture
- https://community.rockrms.com/developer/helix/overview/security
