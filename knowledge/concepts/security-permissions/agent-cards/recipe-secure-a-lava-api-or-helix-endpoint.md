---
concept_id: security-permissions
task_id: recipe-secure-a-lava-api-or-helix-endpoint
title: Recipe: Secure a Lava API or Helix endpoint
generated: true
---

# Recipe: Secure a Lava API or Helix endpoint

A directly callable endpoint with explicit identity, authorization, validation, and bounded output.

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

1. Enumerate the endpoint URL, method, parent application, page, and block.
2. Define authenticated and anonymous behavior explicitly.
3. Enforce the caller’s required View or Edit permission.
4. Validate and sanitize every query and body value.
5. Use non-GET methods for mutations.
6. Enable only required Lava commands.
7. Review CSRF and rate-limit settings.
8. Return only approved fields.
9. Test direct calls without the front end.
10. Test unauthorized, intended-role, and administrator contexts.
11. Verify resulting data or mutations independently. Helix Security,
12. Confirm page and block access for the intended role.
13. Inspect the endpoint’s security mode.
14. Inspect direct endpoint authorization.
15. Where application-level security applies, inspect the parent Lava Application.
16. Inspect enabled commands, input validation, CSRF, and rate-limit settings.
17. Check whether the installed version predates the relevant v19.5 fix.
18. Retest as anonymous, intended role, and administrator; do not treat admin override as role proof. Helix Security,

## Do Not Assume

- Retest as anonymous, intended role, and administrator; do not treat admin override as role proof.

## Source Links

- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/rocku/content-channels/content-channel-view
- https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Communication/CommunicationDetail/CommunicationDetailPermissionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryAuthorizationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/communicationDetailPermissionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/AuthClaims/authClaimBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Administration/Security/securityRoleActionItemBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/AuthClaims/authClaimsOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Administration/Security/addRoleRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/AuthClaims/authClaimRequestBag.d.ts
- https://community.rockrms.com/developer/helix/overview/security
- https://www.rockrms.com/releasenotes
