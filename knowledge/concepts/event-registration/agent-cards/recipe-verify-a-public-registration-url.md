---
concept_id: event-registration
task_id: recipe-verify-a-public-registration-url
title: Recipe: Verify A Public Registration URL
generated: true
---

# Recipe: Verify A Public Registration URL

Return whether the URL targets the intended registration and why it is open, closed, full, wait-listing, or broken.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Label`
- `Block`
- `Page`

## Entities And Tables

- `Label`
- `Block`
- `Page`

## Steps

1. URL route and parameters.
2. Event occurrence linkage.
3. Registration Instance Id.
4. Slug/public name.
5. Registration Entry block settings.
6. Instance active/date/capacity.
7. Rendered status label.
8. Mobile equivalent if applicable.
9. Anonymous access.
10. Instance Active.
11. Registration Starts.
12. Registration Ends.
13. Current server time/time zone.
14. Capacity/spots.
15. Wait list enabled.
16. Linkage points to correct instance.
17. Public page block resolves correct instance.
18. Template is valid.
19. Version-specific status label behavior.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationInstanceSendPaymentReminderInitializationBox.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceFeeList/RegistrationInstanceFeeListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/ResolvePreviewResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstancePaymentList/RegistrationInstancePaymentListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/ResolvePreviewRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationBalanceBag.cs
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/resolvePreviewRequestBag.d.ts
