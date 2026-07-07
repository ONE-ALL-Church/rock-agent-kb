# Check In Label Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Check-in`
- Model title: `CheckInLabel`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `8b651eb1-492f-46d0-821b-ca7355c6e6e7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 18 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 12 |
| Related model links | 2 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CheckInLabelAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Content | yes | yes |  |  |  | The content that describes how to generate the final label content that will be sent to the printer. The format of this value depends on LabelFormat. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | The text that describes the purpose of the label and what kind of information it shows. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | A flag indicating if this Check In Label is active. An in-active label will still be shown in the list of existing labels to be printed, but will not be available when adding a new label to be printed to a group. In-active labels will not be printed. |
| IsSystem | yes | yes |  | yes |  | A flag indicating if this Check In Label is part of the Rock core system/framework. System labels cannot be edited or deleted. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LabelFormat | yes | yes |  |  |  | The format that the Content is stored in. This determines what UI is displayed for editing the label as well as how the label is printed. This is a hard coded list of values defined in the code as an enumeration. |
| LabelType | yes | yes |  |  |  | The type of label. Label types are used to determine what kind of data is available to the label and also how many instances of the label are generated. This is a hard coded list of values defined in the code as an enumeration. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | The name of the check-in label that will be displayed in the UI. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PreviewImage | yes | yes |  |  |  | The image data that will be used to generate a preview of the label in the UI. This should be in PNG or JPG format. |
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
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| IsActive | [Check In Label](check-in-label.md) | 8b651eb1-492f-46d0-821b-ca7355c6e6e7 |
| IsSystem | [Check In Label](check-in-label.md) | 8b651eb1-492f-46d0-821b-ca7355c6e6e7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
