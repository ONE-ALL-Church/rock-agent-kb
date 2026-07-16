# Signature Document Template Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `SignatureDocumentTemplate`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `3f9828cc-8224-4ab0-98a5-6d60001ebe32`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 55 |
| Database-marked properties | 22 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 16 |
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
| BinaryFileType |  | yes | yes |  |  | Gets or sets the type of the Binary File. |
| BinaryFileTypeId | yes | yes |  |  |  | Gets or sets the binary file type identifier. |
| CompletionSystemCommunication |  | yes | yes |  |  | The System Communication that will be used when sending the signature document completion email. |
| CompletionSystemCommunicationId | yes | yes |  |  |  | The System Communication that will be used when sending the signature document completion email. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined description or summary about the SignatureDocumentTemplate. |
| DocumentTerm | yes | yes |  |  |  | The term used to simply describe the document (wavier, release form, etc.). |
| Documents |  |  | yes |  |  | Gets or sets the documents. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InviteSystemCommunication |  | yes | yes |  |  | Gets or sets the system communication to use when a person is invited to sign a document. |
| InviteSystemCommunicationId | yes | yes |  |  |  | Gets or sets the invite system email identifier. |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is active or not. |
| IsLegacy |  |  | yes |  |  | Determines whether this instance is legacy. |
| IsValid |  |  | yes |  |  |  |
| IsValidInFuture | yes | yes |  |  |  | Determines if documents of this type should be considered valid for future eligibility needs. |
| Item |  |  | yes |  |  |  |
| LavaTemplate | yes | yes |  |  |  | The Lava template that will be used to build the signature document. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the friendly Name of the SignatureDocumentTemplate. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ProviderEntityType |  | yes | yes |  |  | Gets or sets the type of the entity. |
| ProviderEntityTypeId | yes | yes |  |  |  | Gets or sets the provider entity type identifier. |
| ProviderTemplateKey | yes | yes |  |  |  | Gets or sets the provider template key. |
| SignatureDocumentTemplateAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SignatureType | yes | yes |  |  |  | This is used to define which kind of signature is being collected from the individual. Ex: SignatureType.Drawn or SignatureType.Typed, etc. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| ValidityDurationInDays | yes | yes |  |  |  | The number of days a signed document of this type is valid once it is signed. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BinaryFileType | Gets or sets the type of the Binary File. |
| CompletionSystemCommunication | The System Communication that will be used when sending the signature document completion email. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InviteSystemCommunication | Gets or sets the system communication to use when a person is invited to sign a document. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ProviderEntityType | Gets or sets the type of the entity. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BinaryFileType | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |
| Documents | documents | c1724719-1c03-4d0c-8a66-e3545138f57f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
