# Registration Registrant Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `RegistrationRegistrant`
- EntityType GUID: `8a25e5ce-1b4f-4825-bcea-216167836305`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 56 |
| Database-marked properties | 17 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 22 |
| Related model links | 11 |
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
| Cost | yes | yes |  |  |  | Gets or sets the cost. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DiscountApplies | yes | yes |  |  |  | Gets or sets a flag indicating if the registration's discount code applies to this registrant. |
| Email |  | yes | yes |  |  | Gets the email. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| Fees |  | yes | yes |  |  | Gets or sets the fees. |
| FirstName |  | yes | yes |  |  | Gets the first name. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupMember |  | yes | yes |  |  | Gets or sets the GroupMember. |
| GroupMemberId | yes | yes |  |  |  | Gets or sets the GroupMember identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastName |  | yes | yes |  |  | Gets the last name. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NickName |  | yes | yes |  |  | Gets the name of the nick. |
| OnWaitList | yes | yes |  |  |  | Gets or sets a value indicating whether registrant is on a wait list. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Person |  | yes | yes |  |  | Gets the Person. |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAlias identifier. |
| PersonId |  |  | yes |  |  | Gets the Person identifier. |
| Registration |  | yes | yes |  |  | Gets or sets the Registration. |
| RegistrationId | yes | yes |  |  |  | Gets or sets the Registration identifier. |
| RegistrationRegistrantAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationTemplateId | yes | yes |  | yes |  | Gets or sets the RegistrationTemplate identifier. |
| SignatureDocument |  |  | yes |  |  | Gets or sets the optional SignatureDocument that may be associated with the Registrant. |
| SignatureDocumentId | yes | yes |  |  |  | Gets or sets the id of the optional SignatureDocument that may be associated with the Registrant. |
| SupportedActions |  |  | yes |  |  |  |
| TotalCost |  | yes | yes |  |  | Gets the cost with fees. |
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
| Email | Gets the email. |
| EntityStringValue |  |
| Fees | Gets or sets the fees. |
| FirstName | Gets the first name. |
| GroupMember | Gets or sets the GroupMember. |
| IdKey |  |
| LastName | Gets the last name. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NickName | Gets the name of the nick. |
| Person | Gets the Person. |
| PersonAlias | Gets or sets the PersonAlias. |
| Registration | Gets or sets the Registration. |
| TotalCost | Gets the cost with fees. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| GroupMember | [GroupMember](group-member.md) |  |
| GroupMemberId | [GroupMember](group-member.md) |  |
| Person | [Person](person.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PersonAliasId | [PersonAlias](person-alias.md) |  |
| PersonId | [Person](person.md) |  |
| Registration | [Registration](registration.md) |  |
| RegistrationId | [Registration](registration.md) |  |
| RegistrationTemplateId | [RegistrationTemplate](registration-template.md) |  |
| SignatureDocument | [SignatureDocument](signature-document.md) |  |
| SignatureDocumentId | [SignatureDocument](signature-document.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
