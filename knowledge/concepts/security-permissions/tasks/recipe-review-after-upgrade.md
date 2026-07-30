---
concept_id: security-permissions
task_id: recipe-review-after-upgrade
title: Recipe: Review After Upgrade
generated: true
---

# Recipe: Review After Upgrade

Sources: Release Notes, GitHub Spotlight: 9/6/2024, GitHub Spotlight: 5/21/2026.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Release notes for the exact version.
2. Workflow type view changes.
3. Document type/file type changes.
4. API endpoint behavior changes.
5. Security cookie/token settings.
6. New action verbs.
7. Lava/shortcode deprecations.
8. Public-viewable warnings.
9. Custom recipes relying on old behavior.
10. AI assistant boundaries. Triumph's AI ministry discussion is useful public training context: AI can assist ministry work, but data boundaries, staff review, and live-system verification govern what an agent should see or do (AI in Digital Ministry).

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools
- https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn
- https://community.rockrms.com/rocku/groups/group-security
