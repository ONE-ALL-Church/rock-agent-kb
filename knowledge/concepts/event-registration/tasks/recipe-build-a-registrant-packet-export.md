---
concept_id: event-registration
task_id: recipe-build-a-registrant-packet-export
title: Recipe: Build A Registrant Packet Export
generated: true
---

# Recipe: Build A Registrant Packet Export

Complete Build A Registrant Packet Export with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Page`
- `Attribute`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Page`
- `Attribute`

## Steps

1. Filters by RegistrationInstanceId.
2. Excludes wait-listed registrants unless requested.
3. Joins registrant to person through PersonAlias.
4. Pulls only needed attributes.
5. Avoids exposing sensitive data broadly.
6. Sorts predictably.
7. Supports printing/page breaks if needed.
8. Uses safe parameter handling.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/rocku/event-registration/event-attributes
- https://community.rockrms.com/rocku/event-registration/event-registration-attributes
- https://www.triumph.tech/resources/github-spotlight-182025
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationInstanceSendPaymentReminderInitializationBox.cs
- https://community.rockrms.com/recipes/313
- https://community.rockrms.com/recipes/361
