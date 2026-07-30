---
concept_id: communications
task_id: recipe-investigate-sms-conversation-access
title: Recipe: Investigate SMS conversation access
generated: true
---

# Recipe: Investigate SMS conversation access

Complete Investigate SMS conversation access with evidence-backed checks and a verifiable outcome.

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

1. system phone number
2. assigned person
3. block allowed numbers
4. "show only personal" setting
5. "hide personal" setting
6. page security
7. block security
8. conversation age setting
9. database timeout
10. pipeline action
11. inbound provider logs

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardRecipientBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateDetailBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateListItemBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryGetRecipientsRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateList/communicationTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowInstanceMessageMetrics/recipientMetricsBag.d.ts
