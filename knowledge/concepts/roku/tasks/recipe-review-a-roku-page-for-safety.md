---
concept_id: roku
task_id: recipe-review-a-roku-page-for-safety
title: Recipe: Review A Roku Page For Safety
generated: true
---

# Recipe: Review A Roku Page For Safety

Report findings by severity: security/cache leaks first, broken rendering second, analytics inaccuracies third, maintainability last.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Attribute`

## Entities And Tables

- `Person`
- `Page`
- `Attribute`

## Steps

1. XML validity after Lava render.
2. `Rock:Page` root.
3. `initialFocus`.
4. `rockCommand` names.
5. Page GUID references.
6. Media URL sources.
7. Cache settings.
8. Lava command usage.
9. Attribute security bypasses.
10. SQL usage.
11. Current-person data.
12. Interaction suppression.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/lava/commands/interaction-write
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/lava/commands/personalize-commands
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/lava/commands/adaptivemessage-commands
