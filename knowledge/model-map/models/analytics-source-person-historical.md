# Analytics Source Person Historical Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `AnalyticsSourcePersonHistorical`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `fc84e469-7e8f-4202-89c3-f27dd41bc132`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 56 |
| Database-marked properties | 43 |
| Lava-marked properties | 49 |
| Lava-marked non-database properties | 6 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 3 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Age | yes | yes |  |  |  |  |
| AnniversaryDate | yes | yes |  |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BirthDateDim |  | yes | yes |  |  |  |
| BirthDateKey | yes | yes |  |  |  |  |
| BirthDay | yes | yes |  |  |  |  |
| BirthMonth | yes | yes |  |  |  |  |
| BirthYear | yes | yes |  |  |  |  |
| ConnectionStatusValueId | yes | yes |  |  |  | These are found in the Connection Status Defined Type. |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  |  |
| CurrentRowIndicator | yes | yes |  |  |  |  |
| EffectiveDate | yes | yes |  |  |  |  |
| Email | yes | yes |  |  |  |  |
| EmailPreference | yes | yes |  |  |  | This is a hard coded list of values defined in the code as an enumeration. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDate | yes | yes |  |  |  |  |
| FirstName | yes | yes |  |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Gender | yes | yes |  | yes |  | This is a hard coded list of values defined in the code as an enumeration. |
| GivingGroupId | yes | yes |  |  |  |  |
| GivingId | yes | yes |  |  |  |  |
| GivingLeaderId | yes | yes |  |  |  |  |
| GraduationYear | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactiveReasonNote | yes | yes |  |  |  |  |
| IsDeceased | yes | yes |  |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastName | yes | yes |  |  |  |  |
| MaritalStatusValueId | yes | yes |  |  |  | These are found in the Marital Status Defined Type. |
| MiddleName | yes | yes |  |  |  |  |
| NickName | yes | yes |  |  |  |  |
| PersonId | yes | yes |  |  |  |  |
| PhotoId | yes | yes |  |  |  |  |
| PrimaryFamilyId | yes | yes |  |  |  |  |
| RecordStatusLastModifiedDateTime | yes | yes |  |  |  |  |
| RecordStatusReasonValueId | yes | yes |  |  |  | These are found in the Inactive Record Reason Defined Type. |
| RecordStatusValueId | yes | yes |  |  |  | These are found in the Record Status Defined Type. |
| RecordTypeValueId | yes | yes |  |  |  | These are found in the Record Type Defined Type. |
| ReviewReasonNote | yes | yes |  |  |  |  |
| ReviewReasonValueId | yes | yes |  |  |  | These are found in the Review Reason Defined Type. |
| SuffixValueId | yes | yes |  |  |  | These are found in the Suffix Defined Type. |
| SystemNote | yes | yes |  |  |  |  |
| TitleValueId | yes | yes |  |  |  | These are found in the Title Defined Type. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| ViewedCount | yes | yes |  |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| BirthDateDim |  |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | MaritalStatusValueId | enum_values |
| property_changed | RecordStatusReasonValueId | enum_values |
| property_changed | RecordTypeValueId | enum_values |
