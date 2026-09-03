---
concept_id: api-integrations
task_id: recipe-build-a-provider-event-health-report
title: Recipe: Build A Provider Event Health Report
generated: true
---

# Recipe: Build A Provider Event Health Report

Staff can understand delivery health in Rock context without seeing unnecessary raw provider data.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`

## Entities And Tables

- `Person`
- `DataView`

## Steps

1. List the provider event types with operational meaning.
2. Define the configured authenticity check for callbacks.
3. Define how each valid event correlates to a Rock communication, recipient, or person context.
4. Separate matched, unmatched, invalid, and processing-failed events.
5. Map events to concise operational states.
6. Build a bounded report or data view using the Rock-side communication fields needed by staff.
7. Exclude credentials, signatures, full raw bodies, and unrelated provider metadata.
8. Test a known event through receipt, correlation, state update, and report display.
9. Define an exception-review process for unmatched events.
10. Verify that the callback passed the provider’s configured authenticity check.
11. Determine whether it correlates to a Rock communication, recipient, or person context.
12. Separate matched events from invalid or unmatched events.
13. Map only operationally meaningful status into staff reporting.
14. Keep unnecessary raw payload fields out of routine reports.
15. For Mailgun on applicable versions, verify that the HTTP webhook signing key is distinct from the API key. (Media Watch; Rock release notes)

## Do Not Assume

- Receipt means authenticity.
- Provider status has already been tied to the correct Rock record.
- Raw detail is more useful than a bounded operational summary.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/security/person-tokens/configure-person-tokens
- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5
- https://www.rockrms.com/releasenotes
