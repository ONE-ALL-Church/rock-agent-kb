---
concept_id: communications
task_id: recipe-determine-whether-a-workflow-email-supports-analytics
title: Recipe: Determine whether a workflow email supports analytics
generated: true
---

# Recipe: Determine whether a workflow email supports analytics

Do not promise analytics for workflow emails unless confirmed in the live instance. The source pack includes an unanswered community question showing this can differ by path (Mailgun Tracking Q&A).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. workflow action type
2. whether a `Communication` record is created
3. whether recipients are `CommunicationRecipient` rows
4. selected medium/transport
5. tracking setting
6. provider tracking/webhook state
7. comparison send through wizard
8. recipient engagement rows

## Do Not Assume

- Do not promise analytics for workflow emails unless confirmed in the live instance.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/8
- https://community.rockrms.com/recipes/435
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-view
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateList/communicationTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockEmailMessageRecipient.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockSMSMessageRecipient.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql
