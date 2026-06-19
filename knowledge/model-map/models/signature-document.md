# Signature Document Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `SignatureDocument`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `c1724719-1c03-4d0c-8a66-e3545138f57f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 31 |
| Lava-marked properties | 49 |
| Lava-marked non-database properties | 18 |
| Related model links | 3 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AppliesToPersonAlias |  | yes | yes |  |  | Gets or sets the applies to person alias. |
| AppliesToPersonAliasId | yes | yes |  |  |  | Gets or sets the applies to person alias identifier. |
| AssignedToPersonAlias |  | yes | yes |  |  | Gets or sets the assigned to person alias. |
| AssignedToPersonAliasId | yes | yes |  |  |  | Gets or sets the assigned to person alias identifier. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFile |  | yes | yes |  |  | Gets or sets the binary file. |
| BinaryFileId | yes | yes |  |  |  | Gets or sets the binary file identifier. |
| CompletionEmailSentDateTime | yes | yes |  |  |  | The date and time the document completion email was sent. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DocumentKey | yes | yes |  |  |  | Gets or sets the document key. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | The ID of the entity to which the document is related. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | The EntityType that this document is related to (example Rock.Model.Registration) |
| EntityTypeId | yes | yes |  |  |  | The EntityType that this document is related to (example Rock.Model.Registration) |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InviteCount | yes | yes |  |  |  | Gets or sets the invite count. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastInviteDate | yes | yes |  |  |  | Gets or sets the request date. |
| LastStatusDate | yes | yes |  |  |  | Gets or sets the last status date. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for this SignatureDocument instance. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SignatureData |  |  | yes |  |  | The data that was collected during a drawn signature type. This is an img data url. Example: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAngAAABkCAYAAAAVH... This is stored as SignatureDataEncrypted. |
| SignatureDataEncrypted | yes | yes |  |  |  | The encrypted data that was collected during a drawn signature type. Use SignatureData to set this from the unencrypted drawn signature. |
| SignatureDocumentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SignatureDocumentTemplate |  | yes | yes |  |  | Gets or sets the Signature Document Template that is being executed in this persisted SignatureDocument instance. |
| SignatureDocumentTemplateId | yes | yes |  |  |  | Gets or sets the SignatureDocumentTemplateId of the Signature Document Template that this SignatureDocument instance is executing. |
| SignatureVerificationHash | yes | yes |  |  |  | The computed SHA1 hash for the SignedDocumentText, SignedClientIP address, SignedClientUserAgent, SignedDateTime, SignedByPersonAliasId, SignatureData, and SignedName. This hash can be used to prove the authenticity of the unaltered signature document. This is only calculated once during the pre-save event when the SignedDateTime was originally null/empty but now has a value. |
| SignedByEmail | yes | yes |  |  |  | The email address that was used to send the completion receipt. |
| SignedByPersonAlias |  | yes | yes |  |  | Gets or sets the signed by person alias. |
| SignedByPersonAliasId | yes | yes |  |  |  | Gets or sets the signed by person alias identifier. |
| SignedClientIp | yes | yes |  |  |  | The observed IP address of the client system of the individual who signed the document. |
| SignedClientUserAgent | yes | yes |  |  |  | The observed 'user agent' of the client system of the individual who signed the document. |
| SignedDateTime | yes | yes |  |  |  | The date and time the document was signed. |
| SignedDocumentText | yes | yes |  |  |  | The resulting text/document using the Lava template from the Signature Document Template at the time the document was signed. Does not include the signature data. It would be what they saw just prior to signing. |
| SignedName | yes | yes |  |  |  | The name of the individual who signed the document. |
| Status | yes | yes |  |  |  | Gets or sets the status. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AppliesToPersonAlias | Gets or sets the applies to person alias. |
| AssignedToPersonAlias | Gets or sets the assigned to person alias. |
| AttributeValues |  |
| Attributes |  |
| BinaryFile | Gets or sets the binary file. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | The EntityType that this document is related to (example Rock.Model.Registration) |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SignatureDocumentTemplate | Gets or sets the Signature Document Template that is being executed in this persisted SignatureDocument instance. |
| SignedByPersonAlias | Gets or sets the signed by person alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| SignatureDocumentTemplate | [Signature Document Template](signature-document-template.md) | 3f9828cc-8224-4ab0-98a5-6d60001ebe32 |
| SignatureDocumentTemplateId | [Signature Document Template](signature-document-template.md) | 3f9828cc-8224-4ab0-98a5-6d60001ebe32 |
| SignedDocumentText | [Signature Document Template](signature-document-template.md) | 3f9828cc-8224-4ab0-98a5-6d60001ebe32 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
