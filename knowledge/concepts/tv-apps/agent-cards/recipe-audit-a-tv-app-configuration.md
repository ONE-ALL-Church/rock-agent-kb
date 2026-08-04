---
concept_id: tv-apps
task_id: recipe-audit-a-tv-app-configuration
title: Recipe: Audit A TV App Configuration
generated: true
---

# Recipe: Audit A TV App Configuration

Complete Audit A TV App Configuration with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Platform: Apple TV or Roku.
2. Rock version.
3. Application record name, GUID/ID if available.
4. API key ID/person.
5. Page-view enabled flag.
6. Retention days.
7. Authentication page.
8. Root/start page.
9. Global styles/components.
10. All page GUIDs referenced by commands.
11. Cache settings for each page.
12. Media URL sources.
13. Remote auth block page and attributes.
14. Configuration summary.
15. Security concerns.
16. Cache concerns.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs
- https://community.rockrms.com/developer/roku-docs/commands/media
- https://community.rockrms.com/lava/lava-api
