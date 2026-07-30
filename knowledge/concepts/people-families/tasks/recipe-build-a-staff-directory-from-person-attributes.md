---
concept_id: people-families
task_id: recipe-build-a-staff-directory-from-person-attributes
title: Recipe: Build A Staff Directory From Person Attributes
generated: true
---

# Recipe: Build A Staff Directory From Person Attributes

Complete Build A Staff Directory From Person Attributes with evidence-backed checks and a verifiable outcome.

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

1. Create person attributes for staff hire date and title if not already present.
2. Set security to HR/staff admins as appropriate.
3. Use a report or Dynamic Data page only in secure internal context.
4. Join person attribute values by attribute id/key.
5. Exclude former staff using a clear status or attribute, not a magic date if avoidable.
6. Review community examples critically (Internal Staff Directory).

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/commands/entity-commands
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://community.rockrms.com/rocku/individuals-in-rock
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
