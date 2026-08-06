---
concept_id: communications
task_id: recipe-explain-why-a-person-did-not-get-sms
title: Recipe: Explain why a person did not get SMS
generated: true
---

# Recipe: Explain why a person did not get SMS

Complete Explain why a person did not get SMS with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`
- `Person`

## Entities And Tables

- `Block`
- `Person`

## Steps

1. mobile phone exists
2. SMS enabled
3. opt-out state
4. phone type
5. cleaned number
6. shared number
7. recipient row
8. status note
9. From system phone number
10. provider send log
11. pipeline only if inbound/reply issue
12. Check recipient `CommunicationRecipient` status and status note.
13. Check person's phone record.
14. Confirm mobile phone type.
15. Confirm SMS enabled state.
16. Confirm opt-out state.
17. Confirm bad-number provider errors.
18. Confirm From number and provider send logs.
19. Check whether the UI only appeared to send. Community experience shows staff can miss pending/failure state without stronger UI warnings (Disabled SMS Mobile Phone Warning).
20. Check v19.1 bad-number vs opt-out fix if relevant (Rock Release Notes).

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-view
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardRecipientBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateDetailBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateListItemBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryGetRecipientsRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateList/communicationTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowInstanceMessageMetrics/recipientMetricsBag.d.ts
- https://community.rockrms.com/recipes/438
- https://www.rockrms.com/releasenotes
