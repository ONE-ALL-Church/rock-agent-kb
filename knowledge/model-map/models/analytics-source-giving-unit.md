# Analytics Source Giving Unit Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `AnalyticsSourceGivingUnit`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `05103bcb-b164-4591-9129-f949a58c04b1`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 33 |
| Database-marked properties | 21 |
| Lava-marked properties | 26 |
| Lava-marked non-database properties | 5 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Frequency | yes | yes |  |  |  | The frequency that this person typically has given in the past 12 months. FinancialGivingAnalyticsFrequencyLabel Possible values include: Weekly, Bi-Weekly, Monthly, Quarterly, Erratic, Variable |
| GiftAmountIqr | yes | yes |  |  |  | The gift amount interquartile range calculated from the past 12 months of giving. |
| GiftAmountMedian | yes | yes |  |  |  | The median gift amount given in the past 12 months. |
| GiftFrequencyMean | yes | yes |  |  |  | The mean days between gifts given in the past 12 months. |
| GiftFrequencyStandardDeviation | yes | yes |  |  |  | The standard deviation for the number of days between gifts given in the past 12 months. |
| GivingBin | yes | yes |  |  |  | The bin that this person's giving habits fall within. The logic for this is in GivingAutomation |
| GivingId | yes | yes |  |  |  | See Person.GivingId. |
| GivingLeaderPersonId | yes | yes |  |  |  | See Person.GivingLeaderId. |
| GivingPercentile | yes | yes |  |  |  | Giving Percentile - Number - This will be rounded to the nearest percent and stored as a whole number (15 vs .15) |
| GivingSalutation | yes | yes |  |  |  | See Group.GroupSalutation |
| GivingSalutationFull | yes | yes |  |  |  | See Group.GroupSalutationFull |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| PercentGiftsScheduled | yes | yes |  |  |  | The percent of gifts in the past 12 months that have been part of a scheduled transaction. Note that this is stored as an integer. Ex: 15% is stored as 15. |
| PreferredCurrency | yes | yes |  |  |  | The most used means of giving that this person employed in the past 12 months. This would be the DefinedValue.Value of PreferredCurrencyValueId |
| PreferredCurrencyValueId | yes | yes |  |  |  | The DefinedValueId of PreferredCurrency |
| PreferredSource | yes | yes |  |  |  | The most used giving source (kiosk, app, web) that this person employed in the past 12 months. This would be the DefinedValue.Value of PreferredSourceValueId |
| PreferredSourceValueId | yes | yes |  |  |  | The DefinedValueId of PreferredSource |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
