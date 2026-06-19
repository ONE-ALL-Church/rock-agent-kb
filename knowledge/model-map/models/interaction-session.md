# Interaction Session Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `InteractionSession`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `338025de-c16f-47bb-ba31-6de0c59e59aa`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 19 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 15 |
| Related model links | 3 |
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
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DeviceType |  | yes | yes |  |  | Gets or sets the device type. |
| DeviceTypeId | yes | yes |  |  |  | Gets or sets the Id of the Interaction Device Type device type that that is associated with this Session. |
| DurationLastCalculatedDateTime | yes |  |  |  |  | Gets or sets the last date and time when this was calculated. |
| DurationSeconds | yes | yes |  |  |  | Gets or set the duration in seconds. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractionChannel |  |  | yes |  |  | Gets or sets the interaction channel. |
| InteractionChannelId | yes | yes |  |  |  | Gets or sets the interaction channel identifier. |
| InteractionCount | yes | yes |  |  |  | Gets or sets the Interaction Count. |
| InteractionMode | yes | yes |  |  |  | Gets or sets the interaction mode. |
| InteractionSessionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractionSessionLocation |  | yes | yes |  |  | Gets or sets the interaction session location. |
| InteractionSessionLocationId | yes | yes |  |  |  | Gets or sets the Id of the Interaction Session Location Session Location that that is associated with this Interaction Session. |
| Interactions |  | yes | yes |  |  | Gets or sets the Interactions for this session. |
| IpAddress | yes | yes |  |  |  | Gets or sets the IP address of the request. |
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
| SessionData | yes | yes |  |  |  | Gets or sets the interaction session data. |
| SessionStartDateKey | yes | yes |  |  |  | Gets or sets the session start date key which is the form YYYYMMDD. |
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
| DeviceType | Gets or sets the device type. |
| EntityStringValue |  |
| IdKey |  |
| InteractionSessionLocation | Gets or sets the interaction session location. |
| Interactions | Gets or sets the Interactions for this session. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DeviceTypeId | [Interaction Device Type](interaction-device-type.md) | c1a24534-c77f-41a8-bca9-73aba57348e3 |
| InteractionSessionLocationId | [Interaction Session Location](interaction-session-location.md) | 790ec7ac-7443-466c-a07e-f702d86b9e1b |
| Interactions | Interactions | 3bb4b095-2de4-4009-8fa2-705bf284f7b7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
