---
concept_id: communications
task_id: recipe-validate-an-email-transport-and-its-event-loop
title: Recipe: Validate an email transport and its event loop
generated: true
---

# Recipe: Validate an email transport and its event loop

A bounded test proves Rock-to-provider handoff, inbox delivery and expected event return.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Confirm the active Email medium and assigned transport.
2. Review transport configuration without copying secrets into notes.
3. Confirm the sending domain and safe-sender policy.
4. Confirm provider webhooks and selected tracking events.
5. Send a uniquely named test to a bounded recipient set.
6. Confirm the Rock communication and recipient records.
7. Confirm provider acceptance.
8. Confirm real inbox delivery.
9. Generate only the approved test events, such as an open or link click.
10. Confirm those events return to the corresponding Rock record.
11. Record which events the transport does and does not provide.

## Do Not Assume

- **Stop when:** Any layer is unverified; do not interpret missing analytics as recipient disengagement until tracking is proven.

## Source Links

- https://community.rockrms.com/documentation/engagement/communications/communication-reports/email-analytics
- https://community.rockrms.com/documentation/engagement/communications/email/configure-email
