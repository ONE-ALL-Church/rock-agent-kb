# Financial Pledge Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialPledge`
- EntityType GUID: `ce8060e6-21e7-49f5-bfbe-f632c816c232`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 18 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 18 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  | Gets or sets the FinancialAccount or account that the pledge is being directed toward. |
| AccountId | yes | yes |  |  |  | Gets or sets the AccountId of the FinancialAccount that the pledge is directed toward. |
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
| EndDate | yes | yes |  |  |  | Gets or sets the end date of the pledge period. |
| EndDateKey | yes | yes |  |  |  | Gets the end date key. |
| EndSourceDate |  | yes | yes |  |  | Gets or sets the end source date. |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialPledgeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | If a person belongs to one or more groups a particular type (i.e. Family), this field is used to distinguish which group the pledge should be associated with. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| PledgeFrequencyValue |  | yes | yes |  |  | Gets or sets the pledge frequency DefinedValue. This is how often the Person who is making the pledge promises to give the TotalAmount |
| PledgeFrequencyValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the pledge frequency DefinedValue representing how often the pledgor is promising to give a portion of the pledge amount. These are found in the "Recurring Transaction Frequency" Defined Type. |
| StartDate | yes | yes |  |  |  | Gets or sets the start date of the pledge period. |
| StartDateKey | yes | yes |  |  |  | Gets the start date key. |
| StartSourceDate |  | yes | yes |  |  | Gets or sets the start source date. |
| SupportedActions |  |  | yes |  |  |  |
| TotalAmount | yes | yes |  |  |  | Gets or sets the pledge amount that is promised to be given. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Account | Gets or sets the FinancialAccount or account that the pledge is being directed toward. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EndSourceDate | Gets or sets the end source date. |
| EntityStringValue |  |
| Group | Gets or sets the Group. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the PersonAlias. |
| PledgeFrequencyValue | Gets or sets the pledge frequency DefinedValue. This is how often the Person who is making the pledge promises to give the TotalAmount |
| StartSourceDate | Gets or sets the start source date. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Account | [FinancialAccount](financial-account.md) |  |
| AccountId | [FinancialAccount](financial-account.md) |  |
| Group | [Group](group.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PledgeFrequencyValue | [DefinedValue](defined-value.md) |  |
| PledgeFrequencyValue | [Person](person.md) |  |
| PledgeFrequencyValueId | [DefinedValue](defined-value.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
