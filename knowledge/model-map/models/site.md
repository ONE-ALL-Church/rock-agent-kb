# Site Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CMS`
- Model title: `Site`
- EntityType GUID: `7244c10b-5d87-467b-a7f5-12dc29910ca8`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 107 |
| Database-marked properties | 54 |
| Lava-marked properties | 88 |
| Lava-marked non-database properties | 34 |
| Related model links | 16 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettings | yes | yes |  |  |  | Gets or sets the additional settings. |
| AllowIndexing | yes | yes |  |  |  | Gets or sets a value indicating whether [allow indexing]. |
| AllowedFrameDomains | yes | yes |  |  |  | The Allowed Frame Domains designates which external domains/sites are allowed to embed iframes of this site. It controls what is put into the Content-Security-Policy HTTP response header. This is in accordance with the Content Security Policy described here http://w3c.github.io/webappsec-csp/#csp-header and here https://www.owasp.org/index.php/Content_Security_Policy_Cheat_Sheet |
| AllowsInteractiveBulkIndexing |  |  | yes |  |  | Gets a value indicating whether [allows interactive bulk indexing]. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Blocks |  | yes | yes |  |  | Gets or sets the collection of Blocks that are used on the site. |
| BotGuardianLevel | yes | yes |  |  |  | Gets or sets the Bot Guardian Level for the Site. This is a hard coded list of values defined in the code as an enumeration. |
| ChangePasswordPage |  | yes | yes |  |  | Gets or sets the change password page. |
| ChangePasswordPageId | yes | yes |  |  |  | Gets or sets the change password page identifier. |
| ChangePasswordPageRoute |  | yes | yes |  |  | Gets or sets the change password page route. |
| ChangePasswordPageRouteId | yes | yes |  |  |  | Gets or sets the change password page route identifier. |
| CommunicationPage |  | yes | yes |  |  | Gets or sets the communication page. |
| CommunicationPageId | yes | yes |  |  |  | Gets or sets the communication page identifier. |
| CommunicationPageRoute |  | yes | yes |  |  | Gets or sets the communication page route. |
| CommunicationPageRouteId | yes | yes |  |  |  | Gets or sets the communication page route identifier. |
| ConfigurationMobilePhoneBinaryFile |  | yes | yes |  |  | Gets or sets the configuration mobile phone binary file. |
| ConfigurationMobilePhoneBinaryFileId | yes | yes |  |  |  | Gets or sets the configuration mobile phone binary file identifier. |
| ConfigurationMobilePhoneFileUrl |  |  | yes |  |  | Gets or sets the configuration mobile file path. |
| ConfigurationMobileTabletBinaryFile |  | yes | yes |  |  | Gets or sets the configuration tablet phone binary file. |
| ConfigurationMobileTabletBinaryFileId | yes | yes |  |  |  | Gets or sets the configuration tablet binary file identifier. |
| ConfigurationTabletFileUrl |  |  | yes |  |  | Gets or sets the configuration tablet file path. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultDomainUri |  | yes | yes |  |  | Gets the default domain URI. |
| DefaultPage |  | yes | yes |  |  | Gets or sets the default Page page for the site. |
| DefaultPageId | yes | yes |  |  |  | Gets or sets the Id of the Site's default Page. |
| DefaultPageRoute |  | yes | yes |  |  | Gets or sets the default PageRoute page route for this site. If this value is null, the DefaultPage will be used |
| DefaultPageRouteId | yes | yes |  |  |  | Gets or sets the default page route unique identifier. If this has a value (and the PageRoute can be found) use this instead of the DefaultPageId |
| Description | yes | yes |  |  |  | Gets or sets a user defined description/summary of the Site. |
| DisablePredictableIds | yes | yes |  |  |  | Gets or sets whether predictable Ids are disabled. |
| EnableExclusiveRoutes | yes | yes |  |  |  | Enabling this feature will prevent other sites from using this sites routes and prevent routes from other sites from working on this site. |
| EnableMobileRedirect | yes | yes |  |  |  | Gets or sets a value indicating whether [enable mobile redirect]. |
| EnablePageViewGeoTracking | yes | yes |  |  |  | [Obsoleted in v0] Geolocation lookups are now performed on all interactions, regardless of this setting. Gets or sets a value indicating whether geo-location lookups should be performed on interactions. |
| EnablePageViews | yes | yes |  |  |  | Gets or sets a value indicating whether to log Page Views into the Interaction tables for pages in this site |
| EnablePersonalization | yes | yes |  |  |  | Gets or sets a value indicating whether [enable personalization]. |
| EnableVisitorTracking | yes | yes |  |  |  | Gets or sets a value indicating whether /[enable visitor tracking]. |
| EnabledForShortening | yes | yes |  |  |  | Gets or sets a value indicating whether this site should be available to be used for shortlinks (the shortlink can still reference the URL of other sites). |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ErrorPage | yes | yes |  |  |  | Gets or sets the path to the error page. |
| ExternalUrl | yes | yes |  |  |  | Gets or sets the external URL. |
| FavIconBinaryFile |  | yes | yes |  |  | Gets or sets the favicon binary file. |
| FavIconBinaryFileId | yes | yes |  |  |  | Gets or sets the favicon binary file identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GoogleAnalyticsCode | yes | yes |  |  |  | Gets or sets the Google analytics code. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IndexStartingLocation | yes | yes |  |  |  | Gets or sets the index starting location. |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsIndexEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is index enabled. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Site was created by and is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LatestVersionDateTime | yes | yes |  |  |  | Gets or sets the latest version date time. |
| Layouts |  | yes | yes |  |  | Gets or sets a collection of Layout entities that are a part of the Site. |
| LoginPage |  | yes | yes |  |  | Gets or sets the login Page page for the site. |
| LoginPageId | yes | yes |  |  |  | Gets or sets the Id of the Site's log in Page |
| LoginPageRoute |  | yes | yes |  |  | Gets or sets the login PageRoute page route for this site. If this value is null, the LoginPage will be used |
| LoginPageRouteId | yes | yes |  |  |  | Gets or sets the login page route unique identifier. If this has a value (and the PageRoute can be found) use this instead of the LoginPageId |
| MobilePage |  | yes | yes |  |  | Gets or sets the mobile page. |
| MobilePageId | yes | yes |  |  |  | Gets or sets the mobile page identifier. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Site. This property is required. |
| PageHeaderContent | yes | yes |  |  |  | Gets or sets the content of the page header. |
| PageNotFoundPage |  | yes | yes |  |  | Gets or sets the 404 Page page for the site. |
| PageNotFoundPageId | yes | yes |  |  |  | Gets or sets the Id of the 404 Page |
| PageNotFoundPageRoute |  | yes | yes |  |  | Gets or sets the 404 PageRoute page route for this site. |
| PageNotFoundPageRouteId | yes | yes |  |  |  | Gets or sets the 404 page route unique identifier. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RedirectTablets | yes | yes |  |  |  | Gets or sets a value indicating whether [redirect tablets]. |
| RegistrationPage |  | yes | yes |  |  | Gets or sets the registration Page page for the site. |
| RegistrationPageId | yes | yes |  |  |  | Gets or sets the Id of the Site's registration Page |
| RegistrationPageRoute |  | yes | yes |  |  | Gets or sets the registration PageRoute page route for this site. If this value is null, the RegistrationPage will be used |
| RegistrationPageRouteId | yes | yes |  |  |  | Gets or sets the registration page route unique identifier. If this has a value (and the PageRoute can be found) use this instead of the RegistrationPageId |
| RequiresEncryption | yes | yes |  |  |  | Gets or sets a value indicating whether [requires encryption]. |
| SiteAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SiteDomains |  | yes | yes |  |  | Gets or sets the collection of SiteDomain entities that reference the Site. |
| SiteLogoBinaryFile |  | yes | yes |  |  | Gets or sets the site logo binary file. |
| SiteLogoBinaryFileId | yes | yes |  |  |  | Gets or sets the site logo binary file identifier. |
| SiteType | yes | yes |  |  |  | Gets or sets the type of the site. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| Theme | yes | yes |  |  |  | Gets or sets the name of the Theme that is used on the Site. |
| ThumbnailBinaryFile |  | yes | yes |  |  | Gets or sets the thumbnail binary file. |
| ThumbnailBinaryFileId | yes | yes |  |  |  | Gets or sets the thumbnail binary file identifier. |
| ThumbnailFileUrl |  |  | yes |  |  | Gets the thumbnail file URL. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Blocks | Gets or sets the collection of Blocks that are used on the site. |
| ChangePasswordPage | Gets or sets the change password page. |
| ChangePasswordPageRoute | Gets or sets the change password page route. |
| CommunicationPage | Gets or sets the communication page. |
| CommunicationPageRoute | Gets or sets the communication page route. |
| ConfigurationMobilePhoneBinaryFile | Gets or sets the configuration mobile phone binary file. |
| ConfigurationMobileTabletBinaryFile | Gets or sets the configuration tablet phone binary file. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefaultDomainUri | Gets the default domain URI. |
| DefaultPage | Gets or sets the default Page page for the site. |
| DefaultPageRoute | Gets or sets the default PageRoute page route for this site. If this value is null, the DefaultPage will be used |
| EntityStringValue |  |
| FavIconBinaryFile | Gets or sets the favicon binary file. |
| IdKey |  |
| Layouts | Gets or sets a collection of Layout entities that are a part of the Site. |
| LoginPage | Gets or sets the login Page page for the site. |
| LoginPageRoute | Gets or sets the login PageRoute page route for this site. If this value is null, the LoginPage will be used |
| MobilePage | Gets or sets the mobile page. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PageNotFoundPage | Gets or sets the 404 Page page for the site. |
| PageNotFoundPageRoute | Gets or sets the 404 PageRoute page route for this site. |
| RegistrationPage | Gets or sets the registration Page page for the site. |
| RegistrationPageRoute | Gets or sets the registration PageRoute page route for this site. If this value is null, the RegistrationPage will be used |
| SiteDomains | Gets or sets the collection of SiteDomain entities that reference the Site. |
| SiteLogoBinaryFile | Gets or sets the site logo binary file. |
| ThumbnailBinaryFile | Gets or sets the thumbnail binary file. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Blocks | Blocks |  |
| DefaultPage | [Page](page.md) |  |
| DefaultPageId | [Page](page.md) |  |
| DefaultPageRoute | [PageRoute](page-route.md) |  |
| Layouts | [Layout](layout.md) |  |
| LoginPage | [Page](page.md) |  |
| LoginPageId | [Page](page.md) |  |
| LoginPageRoute | [PageRoute](page-route.md) |  |
| PageNotFoundPage | [Page](page.md) |  |
| PageNotFoundPageId | [Page](page.md) |  |
| PageNotFoundPageRoute | [PageRoute](page-route.md) |  |
| RegistrationPage | [Page](page.md) |  |
| RegistrationPageId | [Page](page.md) |  |
| RegistrationPageRoute | [PageRoute](page-route.md) |  |
| SiteDomains | [SiteDomain](site-domain.md) |  |
| SupportedActions | Dictionary`2 |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | EnablePageViewGeoTracking | description, is_obsolete |
| property_changed | SupportedActions | related_entity_links |
