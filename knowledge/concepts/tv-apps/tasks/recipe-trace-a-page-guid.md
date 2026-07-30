---
concept_id: tv-apps
task_id: recipe-trace-a-page-guid
title: Recipe: Trace A Page GUID
generated: true
---

# Recipe: Trace A Page GUID

Complete Trace A Page GUID with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`
- `Page`

## Entities And Tables

- `Device`
- `Page`

## Steps

1. Search TV page records for the GUID.
2. Confirm platform and parent application.
3. Render the page with relevant query parameters.
4. Inspect final XML.
5. Check merge fields used.
6. Check page cache settings.
7. Check page security.
8. Check commands pointing out from the page.
9. Check whether page writes interactions.
10. Test device navigation.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/apple-tv-docs
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/lava/lava-api
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs
