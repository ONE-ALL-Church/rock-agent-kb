# Exception Log Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `ExceptionLog`
- EntityType GUID: `f61a9f8a-6da5-49c6-bc8e-5545c5eeda21`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 23 |
| Lava-marked properties | 37 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
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
| Cookies | yes | yes |  |  |  | Gets or sets a table containing the session cookies from the client when the exception occurred. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a message that describes the exception. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExceptionLogAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ExceptionType | yes | yes |  |  |  | Gets or sets the type (exception class) of the exception that occurred. i.e. System.Data.SqlClient.SqlException |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Form | yes | yes |  |  |  | Gets or sets a table containing all the form items from the page request where the exception occurred. |
| Guid | yes | yes |  |  |  |  |
| HasInnerException | yes | yes |  |  |  | Gets or sets a flag indicating if this exception has a child/inner exception. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Page |  | yes | yes |  |  | Gets or sets the Page that the exception occurred on. |
| PageId | yes | yes |  |  |  | Gets or sets the Id of the Page that the exception occurred on. |
| PageUrl | yes | yes |  |  |  | Gets or sets the relative URL of the page that the exception occurred on. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentId | yes | yes |  |  |  | Gets or sets the Id of the parent/outer ExceptionLog entity (if it exists). ExceptionLog entities are hierarchical. |
| QueryString | yes | yes |  |  |  | Gets or sets the full query string from the page that the exception occurred on. |
| ServerVariables | yes | yes |  |  |  | Gets or sets a table of the ServerVariables at the time that the exception occurred. |
| Site |  | yes | yes |  |  | Gets or sets the Site that the exception occurred on. |
| SiteId | yes | yes |  |  |  | Gets or sets the Id of the Site that the exception occurred on. If this did not occur on a site (i.e. a job) this value will be null. |
| Source | yes | yes |  |  |  | Gets or sets the name of the application or the object that causes the error. |
| StackTrace | yes | yes |  |  |  | Gets a string representation of the immediate frames on the call stack. |
| StatusCode | yes | yes |  |  |  | Gets or sets the StatusCode that was returned and describes the type of error. |
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
| Page | Gets or sets the Page that the exception occurred on. |
| Site | Gets or sets the Site that the exception occurred on. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Page | [Page](page.md) |  |
| PageId | [Page](page.md) |  |
| Site | [Site](site.md) |  |
| SiteId | [Site](site.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
