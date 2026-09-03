---
concept_id: content-personalization
task_id: recipe-configure-localized-currency-display-safely
title: Recipe: Configure localized currency display safely
generated: true
---

# Recipe: Configure localized currency display safely

Numeric values display the intended currency symbol without implying conversion or silently changing gateway behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Label`

## Entities And Tables

- `Person`
- `Label`

## Steps

1. Confirm the organization’s intended transaction currency.
2. Confirm every relevant payment gateway uses the matching currency.
3. Set Organization Currency Code for the intended display symbol.
4. Use `FormatAsCurrency` for numeric currency output in Lava.
5. Test display values and payment processing as separate checks.
6. Stop if gateway currency and organization currency do not agree. (Localize Currency)
7. Identify whether the problem concerns display, entry validation, or downstream processing.
8. For dates and times, inspect server culture in System Information.
9. For phones, inspect Phone Country Code ordering, regular expressions, and formatting expressions.
10. For currency display, inspect Organization Currency Code and Lava formatting.
11. Independently confirm payment-gateway currency; a symbol change does not reconfigure it.
12. For addresses, confirm Support International Addresses and the selected country’s labels, format, and states. (Localize Dates & Times, Localize Phone Numbers, Localize Currency, Configure International Addresses)

## Do Not Assume

- Stop if gateway currency and organization currency do not agree.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments
- https://community.rockrms.com/documentation/digital-publishing/personalization
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
