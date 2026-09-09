---
concept_id: developer-resources
task_id: recipe-inspect-page-content-with-a-rock-ai-agent
title: Recipe: Inspect page content with a Rock AI agent
generated: true
---

# Recipe: Inspect page content with a Rock AI agent

Determine what blocks and settings contribute to a page, when the installed agent tools support it.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Page`
- `Block`
- `Attribute`

## Steps

1. Verify that the applicable AI-agent feature and CMS skill are installed and authorized.
2. Resolve the page identifier.
3. List blocks at page, layout, and site scope.
4. Resolve the block type for each relevant block.
5. Inspect available and current block attributes.
6. Separate inherited layout/site behavior from page-local behavior.
7. Report identifiers without exposing secrets or private content.
8. Treat the result as an inspection, not authorization to modify the page.

## Do Not Assume

- Alpha release-note features exist in the target instance.
- Page-level blocks are the only blocks rendered.
- A tool’s presence grants access to every entity.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders
- https://community.rockrms.com/lava/obsidian
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in
- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes
- https://community.rockrms.com/developer/quickstart-tutorials/blocks
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events
- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
