---
concept_id: developer-resources
task_id: recipe-verify-a-save-or-rock-managed-file-deployment
title: Recipe: Verify a save or Rock-managed file deployment
generated: true
---

# Recipe: Verify a save or Rock-managed file deployment

Confirm that the intended state persisted at the exact target.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Identify the actual owning save or file-content surface.
2. Read the current object, file, or content hash.
3. Record the exact target and expected change.
4. Perform the authorized save through that owning surface.
5. Read the value back independently through Edit, Preview, refreshed initialization, a normal API read, exact file readback, or bounded read-only verification.
6. Compare normalized saved state or content hash with the intended artifact.
7. Test the live route that consumes the state.
8. If they differ, investigate normalization, defaults, ignored fields, caching, routing, or a wrong target.

## Do Not Assume

- A success response proves every submitted field persisted.
- A successful upload proves the live route reads that file.
- Read-only SQL is the correct mutation path.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders
- https://community.rockrms.com/lava/obsidian
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in
- https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes
- https://community.rockrms.com/developer/quickstart-tutorials/blocks
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events
- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security
