---
concept_id: communications
task_id: recipe-create-a-communication-flow-without-over-messaging
title: Recipe: Create a communication flow without over-messaging
generated: true
---

# Recipe: Create a communication flow without over-messaging

A version-appropriate flow with a current audience, measurable goal and explicit exit behavior.

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

1. Choose recurring, on-demand or one-time behavior.
2. Define the authoritative audience or activation event.
3. Define a measurable conversion goal supported by Rock.
4. Set the goal window and target.
5. Add only evidence-supported email, SMS or push messages.
6. Define the buffer and send time for each message.
7. Choose when recipients exit.
8. Verify consent and channel eligibility for each medium.
9. Test representative recipients and conversion paths.
10. Activate only after audience, timing and exit behavior are approved.
11. Monitor recipient logs, conversion and unsubscribe results.
12. Pause the flow if targeting or timing is wrong.

## Do Not Assume

- Flow templates and system-wide Communication Templates are interchangeable.

## Source Links

- https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-flows
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts
