---
concept_id: event-registration
task_id: recipe-investigate-api-registration-url-issues
title: Recipe: Investigate API Registration URL Issues
generated: true
---

# Recipe: Investigate API Registration URL Issues

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

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

1. EventItemOccurrence.
2. Linkage record.
3. RegistrationInstanceId.
4. Slug/public name fields.
5. Page route.
6. Registration Entry block.
7. Mobile Registration URL setting.
8. Custom Lava.
9. Current API response shape.

## Do Not Assume

- Do not assume expanded Linkages contain a complete public URL.

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
