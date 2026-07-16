# Person Duplicate Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `CRM`
- Model title: `PersonDuplicate`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `20b2b2b6-38c3-4302-9200-63dd4c78687b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 18 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 14 |
| Related model links | 0 |
| Method signatures | 34 |
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
| Capacity | yes | yes |  |  |  | Gets or sets the capacity. The max possible score based on what items they have values for. |
| ConfidenceScore | yes | yes |  |  |  | Gets the confidence score, which is the Geometric Mean of the "weighted score of things that are matchable"% and "weighted score of things that match"% |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DuplicatePersonAlias |  | yes | yes |  |  | Gets or sets the duplicate person alias. |
| DuplicatePersonAliasId | yes | yes |  | yes |  | Gets or sets the duplicate person alias identifier. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IgnoreUntilScoreChanges | yes | yes |  |  |  | Gets or sets a value indicating whether [ignore until score changes]. Setting this to true will hide the personduplicate record until the score changes |
| IsConfirmedAsNotDuplicate | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is confirmed as not duplicate. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the person alias identifier. |
| PersonDuplicateAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Score | yes | yes |  |  |  | Gets or sets the score. Calculated in the [spCrm_PersonDuplicateFinder] stored procedure |
| ScoreDetail | yes | yes |  |  |  | Gets or sets the score detail. |
| SupportedActions |  |  | yes |  |  |  |
| TotalCapacity | yes | yes |  |  |  | Gets or sets the total capacity. The max possible score if they had values for all matchable items |
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
| DuplicatePersonAlias | Gets or sets the duplicate person alias. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
