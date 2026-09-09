---
concept_id: mobile
task_id: recipe-build-personalized-content-block-output-safely
title: Recipe: Build personalized Content block output safely
generated: true
---

# Recipe: Build personalized Content block output safely

A mobile page displays current, identity-aware or entity-aware content without malformed XAML.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Page`
- `Block`

## Steps

1. Enable Dynamic Content when fresh server output or `CurrentPerson` is required.
2. Configure server-side Lava processing and only the Lava commands needed.
3. For entity context, select the entity type and define the matching page parameter.
4. Pass the entity GUID through the navigation command.
5. Handle missing authentication or context explicitly.
6. Escape all dynamic XAML text.
7. URL-encode query values.
8. Test signed-out, signed-in, missing-context and punctuation-heavy records.
9. Check whether the Content block is static; static Lava has no `CurrentPerson`.
10. Verify Dynamic Content and Process Lava on Server.
11. Inspect enabled Lava commands.
12. Confirm that the shell user is authenticated.
13. If the block uses entity context, verify the entity type, page parameter name and passed GUID.
14. Provide a safe missing-context state instead of dereferencing a null entity.

## Do Not Assume

- Static content has `CurrentPerson`
- Authentication alone establishes block entity context
- Valid Lava output is valid XAML

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms
- https://community.rockrms.com/developer/mobile-docs
- https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events
- https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance
