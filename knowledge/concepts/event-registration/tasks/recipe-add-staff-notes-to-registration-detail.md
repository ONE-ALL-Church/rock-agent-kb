---
concept_id: event-registration
task_id: recipe-add-staff-notes-to-registration-detail
title: Recipe: Add Staff Notes To Registration Detail
generated: true
---

# Recipe: Add Staff Notes To Registration Detail

Complete Add Staff Notes To Registration Detail with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Create a Note Type.
2. Add a Notes block to the appropriate internal registration detail page.
3. Scope note permissions.
4. Decide whether notes attach to registration, registrant, or another entity.
5. Test retention when registrants are removed or changed.
6. Train staff on note standards.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/resolvePreviewRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/registrationInstanceSendPaymentReminderInitializationBox.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/resolvePreviewResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceFeeList/RegistrationInstanceFeeListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/ResolvePreviewResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstancePaymentList/RegistrationInstancePaymentListOptionsBag.cs
