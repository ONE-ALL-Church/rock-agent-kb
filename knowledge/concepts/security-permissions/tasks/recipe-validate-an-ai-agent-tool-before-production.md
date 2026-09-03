---
concept_id: security-permissions
task_id: recipe-validate-an-ai-agent-tool-before-production
title: Recipe: Validate an AI agent tool before production
generated: true
---

# Recipe: Validate an AI agent tool before production

A bounded tool whose availability, authorization, input handling, and output have been demonstrated.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Identify agent, skill, tool, current-person context, and Chat or MCP exposure.
2. Confirm whether the feature is released in the installed Rock version.
3. Define explicit parameters and a bounded result shape.
4. Expose only the minimum operation; separate drafting from sending and omit destructive tools unless required.
5. Route data access through managed Rock code.
6. Enforce Rock permission checks for the authenticated person.
7. Sanitize inputs and avoid arbitrary model-generated SQL execution.
8. Test allowed and denied users.
9. Inspect built-in tool logs for calls, inputs, results, and failures.
10. Test OAuth scope and revocation for MCP clients.
11. Stop before production use if any permission behavior remains inferred. AI Summit,

## Do Not Assume

- Sanitize inputs and avoid arbitrary model-generated SQL execution.

## Source Links

- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/rocku/individuals-in-rock/person-note-1
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/rocku/core-concepts/note-types
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/individuals-in-rock/person-profile
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/rocku/content-channels/content-channel-view
- https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions
- https://community.rockrms.com/documentation/core-concepts/security/advanced-security/view-the-security-change-audit
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.1/202504091716317_AddPersonalDeviceLocationPermissionStatus.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.1/202504091716317_AddPersonalDeviceLocationPermissionStatus.Designer.cs
