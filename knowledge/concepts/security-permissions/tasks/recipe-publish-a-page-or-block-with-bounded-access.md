---
concept_id: security-permissions
task_id: recipe-publish-a-page-or-block-with-bounded-access
title: Recipe: Publish a page or block with bounded access
generated: true
---

# Recipe: Publish a page or block with bounded access

The intended audience can use the surface while unauthorized users cannot.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Page`
- `Block`

## Steps

1. Identify the site, page hierarchy, route, zone, block type, and data source.
2. Inspect inherited page security before adding direct rules.
3. Add the minimum necessary direct rule only when inheritance does not express the requirement.
4. Inspect block security and any underlying entity or endpoint.
5. Review Lava commands, query/context inputs, personalization, and detail routes.
6. Test anonymously, as the intended role, and as an administrator.
7. Verify alternate and mobile routes before publishing. Handle Permissions,
8. Resolve the exact site and route.
9. Inspect the page hierarchy and inherited page security.
10. Inspect each block’s security, block type, zone, and configuration.
11. For content channels, inspect channel, item, list block, detail block, route, and Lava template.
12. Separate personalization rules from authorization.
13. Test anonymous, intended-role, and administrator sessions.
14. Inspect alternate routes, mobile surfaces, and direct endpoints before declaring the content closed or protected. Adding Pages and Blocks,

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/rocku/content-channels/content-channel-view
- https://community.rockrms.com/rocku/individuals-in-rock/person-note-1
- https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/rocku/core-concepts/note-types
- https://community.rockrms.com/rocku/individuals-in-rock/person-profile
- https://community.rockrms.com/documentation/core-concepts/security/advanced-security/view-the-security-change-audit
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Communication/CommunicationDetail/CommunicationDetailPermissionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryAuthorizationBag.d.ts
