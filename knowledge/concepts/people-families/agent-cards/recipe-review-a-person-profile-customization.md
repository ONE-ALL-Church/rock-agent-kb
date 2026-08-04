---
concept_id: people-families
task_id: recipe-review-a-person-profile-customization
title: Recipe: Review A Person Profile Customization
generated: true
---

# Recipe: Review A Person Profile Customization

Complete Review A Person Profile Customization with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Identify page route and context person parameter.
2. List all blocks on the page.
3. Check inherited and explicit security.
4. Check Lava commands enabled.
5. Check SQL commands enabled.
6. Review query filters.
7. Review whether data is registration, giving, workflow, minors, background check, or attributes.
8. Test unauthorized access.
9. Document the customization.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person
- https://community.rockrms.com/developer/202---ignition/advanced-entity-guide
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs
- https://community.rockrms.com/lava/filters/attribute-filters
- https://community.rockrms.com/lava/commands/entity-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search
- https://community.rockrms.com/lava/filters/person-filters
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/checkInFamilyRegistrationSettingsBag.d.ts
