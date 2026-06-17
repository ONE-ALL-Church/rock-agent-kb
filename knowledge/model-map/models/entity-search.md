# Entity Search Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `EntitySearch`
- EntityType GUID: `080374b4-c765-4f90-8b85-bc2635164275`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 23 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 13 |
| Related model links | 1 |
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
| Description | yes | yes |  |  |  | Gets or sets the text that describes the purpose of this search. |
| EncryptedKey |  |  | yes |  |  |  |
| EntitySearchAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type that will be queried by this search. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Entity Type that will be targeted by this search. This property is required. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupByExpression | yes | yes |  |  |  | Gets or sets the expression that will be used to group the results. This is processed after WhereExpression. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludePaths | yes | yes |  |  |  | Gets or sets the property paths to be included by Entity Framework. This is only valid when IsEntitySecurityEnabled is true. Example: GroupType,Members.Person |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this search is active. |
| IsEntitySecurityEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this search will enforce entity security. Entity security has a pretty heafty performance hit and should only be used when it is actually needed. |
| IsRefinementAllowed | yes | yes |  |  |  | Gets or sets a value indicating whether search query will allow custom refinement options in the form of an additional user query. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  | yes |  | Gets or sets the key of this search. This is used to identify this search item through the API and Lava. This value must be unique for a given EntityTypeId. This property is required. |
| MaximumResultsPerQuery | yes | yes |  |  |  | Gets or sets the maximum number of results per query. More data can be retrieved by subsequent queries that skip the first n items. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the search query. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SelectExpression | yes | yes |  |  |  | Gets or sets the expression that will be used to define the structure of the resulting items. This is processed after GroupByExpression. |
| SelectManyExpression | yes | yes |  |  |  | Gets or sets the expression that will be used to define the structure of the resulting items. This is processed after GroupByExpression and instead of SelectExpression. |
| SortExpression | yes | yes |  |  |  | Gets or sets the expression that will be used to sort the results. This is processed after SelectExpression. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WhereExpression | yes | yes |  |  |  | Gets or sets the expression that will be used to filter the query. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type that will be queried by this search. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
