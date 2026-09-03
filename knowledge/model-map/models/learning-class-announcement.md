# Learning Class Announcement Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `LMS`
- Model title: `LearningClassAnnouncement`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `d2ce59d3-55e1-4275-9ea1-38c18a05a32b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 17 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
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
| CommunicationMode | yes | yes |  |  |  | The communication mode used for the announcement. This is a hard coded list of values defined in the code as an enumeration. |
| CommunicationSent | yes | yes |  |  |  | Gets or sets a value indicating whether the communication has been sent. This will always be false when the 'None' CommunicationMode is specified. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description for the announcement. |
| DetailsUrl | yes | yes |  |  |  | Gets or sets the url where more details can be found (if any). |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningClass |  | yes | yes |  |  | Gets or sets the related Learning Class. |
| LearningClassAnnouncementAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningClassId | yes | yes |  |  |  | Gets or sets the id of the Learning Class the announcement belongs to. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PublishDateTime | yes | yes |  |  |  | Gets or sets the date the announcement should be published/visible. |
| Summary | yes | yes |  |  |  | Gets or sets the summary text of the announcement. |
| SupportedActions |  |  | yes |  |  |  |
| Title | yes | yes |  | yes |  | Gets or sets the title of the announcement. |
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
| LearningClass | Gets or sets the related Learning Class. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| LearningClass | [Learning Class](learning-class.md) | eb41e4e1-64b1-4aa1-8f66-f0dfd81557d9 |
| LearningClassId | [Learning Class](learning-class.md) | eb41e4e1-64b1-4aa1-8f66-f0dfd81557d9 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
