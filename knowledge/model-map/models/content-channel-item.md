# Content Channel Item Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CMS`
- Model title: `ContentChannelItem`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `41`
- Obsolete methods: `4`
- EntityType GUID: `bf12ae64-21fb-433b-a8a4-e40e8c426dda`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 71 |
| Database-marked properties | 31 |
| Lava-marked properties | 52 |
| Lava-marked non-database properties | 21 |
| Related model links | 3 |
| Method signatures | 41 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AllowsInteractiveBulkIndexing |  |  | yes |  |  | Gets a value indicating whether [allows interactive bulk indexing]. |
| ApprovedByPersonAlias |  | yes | yes |  |  | Gets or sets the approved by person alias. |
| ApprovedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId of the Person who either approved or declined the ContentItem. If no approval action has been performed on this item, this value will be null. |
| ApprovedDateTime | yes | yes |  |  |  | Gets or sets the approved date. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChildItems |  | yes | yes |  |  | Gets or sets the child items. |
| Content | yes | yes |  |  |  | Gets or sets the content. |
| ContentChannel |  | yes | yes |  |  | Gets or sets the content channel. |
| ContentChannelId | yes | yes |  |  |  | Gets or sets the content channel identifier. |
| ContentChannelItemAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContentChannelItemSlugs |  | yes | yes |  |  | Gets or sets the content channel item slugs. |
| ContentChannelType |  | yes | yes |  |  | Gets or sets the type of the content channel. |
| ContentChannelTypeId | yes | yes |  |  |  | Gets or sets the content channel type identifier. |
| ContentLibraryContentTopicId | yes | yes |  |  |  | Gets the content library content topic identifier. |
| ContentLibraryLicenseTypeValueId | yes | yes |  |  |  | Gets the content library license type defined value identifier. |
| ContentLibrarySourceIdentifier | yes | yes |  |  |  | Gets the content library source identifier. |
| ContentLibraryUploadedByPersonAlias |  | yes | yes |  |  | Gets or sets the content library uploaded by person alias. |
| ContentLibraryUploadedByPersonAliasId | yes | yes |  |  |  | Gets or sets the content library uploaded by person alias identifier. |
| ContentLibraryUploadedByPersonName |  | yes | yes |  |  | Gets the name of the content library uploaded by person. |
| ContentLibraryUploadedDateTime | yes | yes |  |  |  | Gets or sets the content library uploaded date time. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EventItemOccurrences |  |  | yes |  |  | Gets or sets the event item occurrence channel items. |
| ExperienceLevel | yes | yes |  |  |  | Gets or sets the experience level. This is a hard coded list of values defined in the code as an enumeration. |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the expire date time. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsContentLibraryOwner | yes | yes |  |  |  | Gets or sets a value indicating whether this item is an owned content library item. |
| IsDownloadedFromContentLibrary |  |  | yes |  |  | Gets a value indicating whether this instance is downloaded from content library. |
| IsUploadedToContentLibrary |  |  | yes |  |  | Gets a value indicating whether this instance is uploaded to content library. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ItemGlobalKey | yes | yes |  |  |  | Gets or sets the item global key. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentItems |  | yes | yes |  |  | Gets or sets the parent items. |
| Permalink | yes | yes |  |  |  | Gets or sets the permalink. |
| PrimarySlug |  | yes | yes |  |  | Gets the primary slug. The first occurence of IsPrimary otherwise the first. |
| Priority | yes | yes |  |  |  | Gets or sets the priority of this ContentItem. The lower the number, the higher the priority. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the start date time. |
| Status | yes | yes |  |  |  | Gets or sets the ContentChannelItemStatus (status) of this ContentItem. This is a hard coded list of values defined in the code as an enumeration. |
| StructuredContent | yes | yes |  |  |  | Gets or sets the structured content. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| Title | yes | yes |  |  |  | Gets or sets the title. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ApprovedByPersonAlias | Gets or sets the approved by person alias. |
| AttributeValues |  |
| Attributes |  |
| ChildItems | Gets or sets the child items. |
| ContentChannel | Gets or sets the content channel. |
| ContentChannelItemSlugs | Gets or sets the content channel item slugs. |
| ContentChannelType | Gets or sets the type of the content channel. |
| ContentLibraryUploadedByPersonAlias | Gets or sets the content library uploaded by person alias. |
| ContentLibraryUploadedByPersonName | Gets the name of the content library uploaded by person. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentItems | Gets or sets the parent items. |
| PrimarySlug | Gets the primary slug. The first occurence of IsPrimary otherwise the first. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ApprovedByPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| ChildItems | child items | 7c86eed3-c3f9-4b25-887b-f732fe3c35f0 |
| EventItemOccurrences | event item occurrence channel items | 378a9559-bd86-45a8-b218-2c5d4cf3d770 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
