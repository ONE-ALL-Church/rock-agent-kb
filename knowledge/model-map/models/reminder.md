# Reminder Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `Reminder`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `38`
- Obsolete methods: `4`
- EntityType GUID: `46cc0d74-be46-4d5d-a6f1-0811645721ac`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 21 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 14 |
| Related model links | 0 |
| Method signatures | 38 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the entity identifier. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HasFutureOccurrences | yes |  |  |  |  | Gets a value indicating whether this reminder has future occurrences. Returns false if the reminder is non-renewing. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes |  |  |  |  | Gets a value indicating whether this reminder is active. |
| IsComplete | yes | yes |  |  |  | Gets or sets a value indicating whether this reminder is complete. |
| IsRenewing | yes |  |  |  |  | Gets a value indicating whether this is a renewing reminder. If a reminder has a null value in RenewMaxCount it is perpetually renewing. A reminder must also have a non-null, non-zero value in RenewPeriodDays to be renewing. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| ReminderAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ReminderDate | yes | yes |  |  |  | Gets or sets the reminder date. |
| ReminderType |  | yes | yes |  |  | Gets or sets the type of the reminder. |
| ReminderTypeId | yes | yes |  |  |  | Gets or sets the reminder type identifier. |
| RenewCurrentCount | yes | yes |  |  |  | Gets or sets renew current count. |
| RenewMaxCount | yes | yes |  |  |  | Gets or sets the renew max count. |
| RenewPeriodDays | yes | yes |  |  |  | Gets or sets the renew period days. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias. |
| ReminderType | Gets or sets the type of the reminder. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
