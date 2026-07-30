---
concept_id: tv-apps
task_id: recipe-validate-remote-auth-in-data
title: Recipe: Validate Remote Auth In Data
generated: true
---

# Recipe: Validate Remote Auth In Data

Complete Validate Remote Auth In Data with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Device`
- `Page`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Device`
- `Page`

## Steps

1. `RemoteAuthenticationSession` rows created during a test.
2. `Code`.
3. `DeviceUniqueIdentifier`.
4. `ClientIpAddress`.
5. `AuthenticationIpAddress`.
6. `SessionStartDateTime`.
7. `SessionEndDateTime`.
8. `SiteId`.
9. `AuthorizedPersonAliasId`.
10. New session row appears when TV login starts.
11. Code matches displayed code.
12. Authorized alias is empty before web authorization.
13. Authorized alias is populated after successful web authorization.
14. Session remains active within lifetime.
15. Shell detects success and navigates to success page.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/apple-tv-docs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/lava/lava-api
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Client/CodeGenerated/RemoteAuthenticationSession.cs
