# Communication Response Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Communication`
- Model title: `CommunicationResponse`
- EntityType GUID: `db449144-6045-4b11-aa55-ecf286b117a9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 19 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 13 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attachments |  | yes | yes |  |  | Gets or sets the attachments. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CommunicationResponseAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
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
| FromPersonAlias |  |  | yes |  |  | Gets or sets from person alias. |
| FromPersonAliasId | yes | yes |  |  |  | Gets or sets from person alias identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsRead | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is read. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MessageKey | yes | yes |  | yes |  | This is the address of the sender communication medium. e.g. A phone number or email address. It is used when an incoming message cannot be identified with a person, this can be used to link it up later. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RelatedCommunication |  |  | yes |  |  | Gets or sets the related communication. |
| RelatedCommunicationId | yes | yes |  |  |  | Gets or sets the related communication identifier. |
| RelatedMedium |  |  | yes |  |  | Gets or sets the related medium. |
| RelatedMediumEntityTypeId | yes | yes |  |  |  | Gets or sets the related medium entity type identifier. |
| RelatedSmsFromDefinedValueId | yes | yes |  |  |  | [Obsoleted in v15] Use RelatedSmsFromSystemPhoneNumberId instead. Gets or sets the related SMS from defined value identifier. |
| RelatedSmsFromSystemPhoneNumber |  |  | yes |  |  | Gets or sets the related SMS system phone number this response was received on. |
| RelatedSmsFromSystemPhoneNumberId | yes | yes |  |  |  | Gets or sets the related SMS system phone number identifier this response was received on. |
| RelatedTransport |  |  | yes |  |  | Gets or sets the related transport. |
| RelatedTransportEntityTypeId | yes | yes |  |  |  | Gets or sets the related transport entity type identifier. |
| Response | yes | yes |  |  |  | Gets or sets the response. |
| SupportedActions |  |  | yes |  |  |  |
| ToPersonAlias |  |  | yes |  |  | Gets or sets to person alias. |
| ToPersonAliasId | yes | yes |  |  |  | Gets or sets to person alias identifier. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Attachments | Gets or sets the attachments. |
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

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | RelatedSmsFromDefinedValueId |  |
