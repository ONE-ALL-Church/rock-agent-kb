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

## Entities And Tables

- `Block`

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

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardRecipientBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateDetailBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateListItemBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryGetRecipientsRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateList/communicationTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowInstanceMessageMetrics/recipientMetricsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts
