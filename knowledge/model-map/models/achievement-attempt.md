# Achievement Attempt Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `AchievementAttempt`
- EntityType GUID: `5c144b51-3d2e-4bc2-b6c7-7e4cb890e15f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 16 |
| Lava-marked properties | 29 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AchievementAttemptAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AchievementAttemptEndDateTime | yes | yes |  |  |  | Gets or sets the achievement attempt end date time. |
| AchievementAttemptStartDateTime | yes | yes |  | yes |  | Gets or sets the achievement attempt start date time. |
| AchievementType |  | yes | yes |  |  | Gets or sets the Achievement Type of this attempt. |
| AchievementTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Achievement Type to which this attempt belongs. This property is required. |
| AchieverEntityId | yes | yes |  | yes |  | Gets or sets the achiever entity identifier. The type of AchieverEntity is determined by AchievementType.AchieverEntityTypeId. NOTE: In the case of a Person achievement, this could either by PersonAliasId or PersonId (but probably PersonAliasId) depending on AchievementType.AchievementEntityType |
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
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsClosed | yes | yes |  |  |  | Gets or sets a value indicating whether this attempt is closed. |
| IsSuccessful | yes | yes |  |  |  | Gets or sets a value indicating whether this attempt was a success. |
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
| Progress | yes | yes |  |  |  | Gets or sets the progress. This is a percentage so .25 is 25% and 1 is 100%. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AchievementType | Gets or sets the Achievement Type of this attempt. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
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
| AchievementType | [Achievement Type](achievement-type.md) | 0e99356c-0dea-4f24-944e-21cd5fa83b9e |
| AchievementTypeId | [Achievement Type](achievement-type.md) | 0e99356c-0dea-4f24-944e-21cd5fa83b9e |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
