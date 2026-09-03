---
concept_id: event-registration
task_id: recipe-promote-a-wait-listed-person-to-full-registration
title: Recipe: Promote a wait-listed person to full registration
generated: true
---

# Recipe: Promote a wait-listed person to full registration

The person becomes a complete, paid-as-required registrant with the intended group membership.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Attribute`

## Entities And Tables

- `Person`
- `Group`
- `Attribute`

## Steps

1. Confirm available capacity and identify the exact wait-listed registrant.
2. Move that registrant from the Wait List tab.
3. Send the completion email unless a reviewed alternative follow-up is in place.
4. Confirm the person opens the correct registration.
5. Collect any payment and questions omitted during wait-list entry.
6. Verify the full-registration status.
7. Verify configured group membership and any required Group Member Attributes.
8. Reconcile capacity and the remaining wait-list order.
9. Stop when the registrant is complete across status, data, finance, and group placement.
10. Confirm the registrant is now marked as a full registrant.
11. Confirm that configured group placement occurred.
12. Verify whether the move email was sent.
13. Open its completion link as a test recipient and confirm it requests payment and fields omitted during wait-list entry.
14. Check whether the person completed that follow-up flow.
15. If payment completion fails, compare the installed version with the supplied v19.3 fix.
16. Stop when status, required data, payment, and group placement all reconcile.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/group-placement
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations
- https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-content-channel-items
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementConfigBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementBag.cs
- https://community.rockrms.com/rocku/event-registration/event-attributes
- https://community.rockrms.com/rocku/event-registration/event-registration-attributes
