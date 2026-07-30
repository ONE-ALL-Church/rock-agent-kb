---
concept_id: api-integrations
task_id: recipe-build-a-safe-agent-tool
title: Recipe: Build A Safe Agent Tool
generated: true
---

# Recipe: Build A Safe Agent Tool

See Writing Custom Tools, Get Tools, and List Tools.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Attribute`

## Entities And Tables

- `Person`
- `Attribute`

## Steps

1. Define tool purpose and allowed user roles.
2. Use IdKey for all entity identifiers.
3. Use helper methods to resolve and check security.
4. Return narrow result objects.
5. Sanitize attribute values.
6. Use pagination.
7. Add explicit guardrails for writes.
8. Test with unauthorized current person.
9. Test missing/invalid IdKey.
10. Document terms and date/time assumptions.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail/check-scanning
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/303---blast-off/extending-communication-transports
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/developer/303---blast-off/rock-security
