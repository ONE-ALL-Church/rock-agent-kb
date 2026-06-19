# Financial Pledge Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Finance`
- Model title: `FinancialPledge`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
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
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  | Gets or sets the Financial Account or account that the pledge is being directed toward. |
| AccountId | yes | yes |  |  |  | Gets or sets the AccountId of the Financial Account that the pledge is directed toward. |
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
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| PledgeFrequencyValue |  | yes | yes |  |  | Gets or sets the pledge frequency Defined Value. This is how often the Person who is making the pledge promises to give the TotalAmount |
| PledgeFrequencyValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the pledge frequency Defined Value representing how often the pledgor is promising to give a portion of the pledge amount. These are found in the Recurring Transaction Frequency Defined Type. |
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
| Account | Gets or sets the Financial Account or account that the pledge is being directed toward. |
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
| PersonAlias | Gets or sets the Person Alias. |
| PledgeFrequencyValue | Gets or sets the pledge frequency Defined Value. This is how often the Person who is making the pledge promises to give the TotalAmount |
| StartSourceDate | Gets or sets the start source date. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Account | [Financial Account](financial-account.md) | 798bce48-6aa7-4983-9214-f9bcefb4521d |
| AccountId | [Financial Account](financial-account.md) | 798bce48-6aa7-4983-9214-f9bcefb4521d |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PledgeFrequencyValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| PledgeFrequencyValue | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PledgeFrequencyValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | PledgeFrequencyValueId | enum_values |
