# Analytics Dim Person Historical Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Reporting`
- Model title: `AnalyticsDimPersonHistorical`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `050aaa2b-43ea-4952-936c-70638d3bcc0d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 94 |
| Database-marked properties | 81 |
| Lava-marked properties | 87 |
| Lava-marked non-database properties | 6 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

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
| CampusId | yes | yes |  |  |  |  |
| CampusName | yes | yes |  |  |  |  |
| CampusShortCode | yes | yes |  |  |  |  |
| ConnectionStatus | yes | yes |  |  |  |  |
| ConnectionStatusValueId | yes | yes |  |  |  | These are found in the Connection Status Defined Type. |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  |  |
| CurrentRowIndicator | yes | yes |  |  |  |  |
| EffectiveDate | yes | yes |  |  |  |  |
| Email | yes | yes |  |  |  |  |
| EmailPreference | yes | yes |  |  |  | This is a hard coded list of values defined in the code as an enumeration. |
| EmailPreferenceText | yes | yes |  |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDate | yes | yes |  |  |  |  |
| FirstName | yes | yes |  |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Gender | yes | yes |  | yes |  | This is a hard coded list of values defined in the code as an enumeration. |
| GenderText | yes | yes |  |  |  |  |
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
| MailingAddressCity | yes | yes |  |  |  |  |
| MailingAddressCountry | yes | yes |  |  |  |  |
| MailingAddressCounty | yes | yes |  |  |  |  |
| MailingAddressFull | yes | yes |  |  |  |  |
| MailingAddressGeoFence | yes | yes |  |  |  |  |
| MailingAddressGeoPoint | yes | yes |  |  |  |  |
| MailingAddressLatitude | yes | yes |  |  |  |  |
| MailingAddressLongitude | yes | yes |  |  |  |  |
| MailingAddressPostalCode | yes | yes |  |  |  |  |
| MailingAddressState | yes | yes |  |  |  |  |
| MailingAddressStreet1 | yes | yes |  |  |  |  |
| MailingAddressStreet2 | yes | yes |  |  |  |  |
| MappedAddressCity | yes | yes |  |  |  |  |
| MappedAddressCountry | yes | yes |  |  |  |  |
| MappedAddressCounty | yes | yes |  |  |  |  |
| MappedAddressFull | yes | yes |  |  |  |  |
| MappedAddressGeoFence | yes | yes |  |  |  |  |
| MappedAddressGeoPoint | yes | yes |  |  |  |  |
| MappedAddressLatitude | yes | yes |  |  |  |  |
| MappedAddressLongitude | yes | yes |  |  |  |  |
| MappedAddressPostalCode | yes | yes |  |  |  |  |
| MappedAddressState | yes | yes |  |  |  |  |
| MappedAddressStreet1 | yes | yes |  |  |  |  |
| MappedAddressStreet2 | yes | yes |  |  |  |  |
| MaritalStatus | yes | yes |  |  |  |  |
| MaritalStatusValueId | yes | yes |  |  |  | These are found in the Marital Status Defined Type. |
| MiddleName | yes | yes |  |  |  |  |
| NickName | yes | yes |  |  |  |  |
| PersonId | yes | yes |  |  |  |  |
| PhotoId | yes | yes |  |  |  |  |
| PrimaryFamilyId | yes | yes |  |  |  |  |
| PrimaryFamilyKey | yes | yes |  |  |  |  |
| RecordStatus | yes | yes |  |  |  |  |
| RecordStatusLastModifiedDateTime | yes | yes |  |  |  |  |
| RecordStatusReason | yes | yes |  |  |  |  |
| RecordStatusReasonValueId | yes | yes |  |  |  | These are found in the Inactive Record Reason Defined Type. |
| RecordStatusValueId | yes | yes |  |  |  | These are found in the Record Status Defined Type. |
| RecordType | yes | yes |  |  |  |  |
| RecordTypeValueId | yes | yes |  |  |  | These are found in the Record Type Defined Type. |
| ReviewReason | yes | yes |  |  |  |  |
| ReviewReasonNote | yes | yes |  |  |  |  |
| ReviewReasonValueId | yes | yes |  |  |  | These are found in the Review Reason Defined Type. |
| Suffix | yes | yes |  |  |  |  |
| SuffixValueId | yes | yes |  |  |  | These are found in the Suffix Defined Type. |
| SystemNote | yes | yes |  |  |  |  |
| Title | yes | yes |  |  |  |  |
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

No stable-to-pre-alpha changes were detected for this model.
