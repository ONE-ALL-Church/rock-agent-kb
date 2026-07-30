---
concept_id: developer-resources
task_id: recipe-diagnose-works-for-admin-but-not-staff
title: Recipe: Diagnose "Works for admin but not staff"
generated: true
---

# Recipe: Diagnose "Works for admin but not staff"

References: 303 security, Helix security, release notes (Rock Security, Helix Security, Release Notes).

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

1. Check page security.
2. Check block security.
3. Check block action security.
4. Check entity security.
5. Check endpoint security mode.
6. Check workflow type view/execute permissions.
7. Check API key/user permissions.
8. Check parent authority inheritance.
9. Check release-note security hardening.
10. Verify with the affected user/person.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer
- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders
- https://community.rockrms.com/lava/obsidian
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/quickstart-tutorials/blocks
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events
