---
concept_id: security-permissions
task_id: recipe-audit-person-profile-notes
title: Recipe: Audit Person Profile notes
generated: true
---

# Recipe: Audit Person Profile notes

Sensitive notes are categorized, visible, and consumed only as intended.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Workflow`
- `Page`
- `Block`

## Steps

1. Inventory the relevant Note Types and target entity contexts.
2. Map who may view, add, edit, or otherwise act on each type.
3. Inspect the Person Profile page and block surfaces.
4. Sample author, date, visibility, and lifecycle behavior without publishing private note text.
5. Identify workflows and reports that consume each type.
6. Test with authorized and unauthorized staff roles.
7. Record configuration gaps without moving or rewriting notes. Note Types,

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/rocku/content-channels/content-channel-view
- https://community.rockrms.com/rocku/individuals-in-rock/person-note-1
- https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration
- https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions
- https://community.rockrms.com/documentation/core-concepts/security/captcha/use-captcha
- https://community.rockrms.com/documentation/core-concepts/security/captcha/configure-captcha
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/documentation
