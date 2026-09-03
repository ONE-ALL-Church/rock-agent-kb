---
concept_id: security-permissions
task_id: recipe-explain-an-effective-permission-result
title: Recipe: Explain an effective permission result
generated: true
---

# Recipe: Explain an effective permission result

A sourced explanation of why one person is allowed or denied one action.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Block`

## Entities And Tables

- `Person`
- `Block`

## Steps

1. Record the person, entity type, entity ID or GUID, and requested action.
2. Run the equivalent of an Inspect Security review.
3. Capture the matching direct or inherited rule and its position.
4. Identify the parent when the rule is inherited.
5. Check relevant role membership separately.
6. State the effective result, matching rule, inheritance source, and any unverified adjacent boundary.

## Do Not Assume

- A role name proves membership.
- A visible route proves block or entity access.
- An administrator result represents the user’s result.

## Source Links

- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/individuals-in-rock/person-note-1
- https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/rocku/content-channels/content-channel-view
- https://community.rockrms.com/rocku/core-concepts/note-types
- https://community.rockrms.com/rocku/individuals-in-rock/person-profile
- https://community.rockrms.com/documentation/core-concepts/security/advanced-security/inspect-security
- https://community.rockrms.com/documentation/core-concepts/security/advanced-security/view-the-security-change-audit
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Communication/CommunicationDetail/CommunicationDetailPermissionsBag.cs
