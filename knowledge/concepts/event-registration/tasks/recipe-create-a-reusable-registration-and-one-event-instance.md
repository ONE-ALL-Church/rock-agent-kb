---
concept_id: event-registration
task_id: recipe-create-a-reusable-registration-and-one-event-instance
title: Recipe: Create a reusable registration and one event instance
generated: true
---

# Recipe: Create a reusable registration and one event instance

A configured but not yet broadly launched instance with explicit ownership of shared and event-specific settings.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Campus`
- `Workflow`
- `Block`

## Entities And Tables

- `Person`
- `Group`
- `Campus`
- `Workflow`
- `Block`

## Steps

1. Define the registrant population, registrar model, required fields, cost model, capacity, group destination, communications, and follow-up owner.
2. Reuse an appropriate template or create one with authorized template administration.
3. Put reusable form, eligibility, finance, communication, workflow, signature, and placement settings on the template.
4. Create the instance and set its registration dates, contact, capacity, payment deadline, and any instance-owned finance settings.
5. Create or select the operational group if the event requires a roster or check-in.
6. Create or select the event item and occurrence.
7. Add the registration, group, campus, public name, and URL slug linkage as required.
8. Leave the instance inactive when the workflow requires review before publication.
9. Test representative free or paid, single- or multi-person, eligible and ineligible paths.
10. Activate only after public routing, communications, payments, placement, and permissions pass.

## Do Not Assume

- Wizard completion equals launch readiness
- A calendar event automatically has a registration
- An instance automatically places people into a group
- A selected gateway supports payment plans

## Source Links

- https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/group-placement
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementConfigBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementBag.cs
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations
- https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-content-channel-items
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/event-wizard
- https://www.rockrms.com/releasenotes
