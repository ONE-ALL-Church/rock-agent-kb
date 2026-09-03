---
concept_id: communications
task_id: recipe-preflight-a-broad-email-communication
title: Recipe: Preflight a broad email communication
generated: true
---

# Recipe: Preflight a broad email communication

A reviewed draft whose audience, sender, classification, content, consent and delivery path are ready for the organization’s approval process.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`
- `Group`

## Entities And Tables

- `Person`
- `DataView`
- `Group`

## Steps

1. Record the installed Rock version, editor surface and intended send time.
2. Identify the authoritative audience source and calculate its current result.
3. Refresh any synchronized communication-list group through its approved mechanism.
4. Compare source count, group count and final eligible-recipient count.
5. Investigate exclusions rather than adding people manually to force count alignment.
6. Confirm personal-versus-bulk classification.
7. Confirm From, Reply-To, sender domain, topic and template.
8. Preview representative personalization cases and every important call-to-action.
9. Send bounded tests to representative mailbox providers.
10. Confirm the transport, tracking and unsubscribe behavior.
11. Save as draft or submit for approval.
12. After authorization and sending, verify Communication History and recipient outcomes.

## Do Not Assume

- A Data View reruns when an old communication is duplicated.
- Every selected person is eligible.
- A preview proves provider delivery.
- Counts do not reconcile.

## Source Links

- https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics
- https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
