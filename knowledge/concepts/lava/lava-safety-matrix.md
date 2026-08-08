# Lava Safety Matrix

Generated from structured metadata derived from official Rock Lava pages plus maintainer-authored operational guidance.

## Agent Rules

- Do not treat this matrix as syntax documentation; link to the official Rock page for syntax.
- High-risk rows require live-instance verification before recommending operational changes.
- Any row that reads data, mutates data, performs external I/O, uses SQL/entity access, launches workflows, or affects page/HTTP output should trigger security review in public or staff-facing surfaces.
- Lava command rows usually require explicit command enablement in the rendering context.

## High-Risk Rows

| Name | Category | Why It Is Sensitive | Live Verification Prompt | Official Page |
| --- | --- | --- | --- | --- |
| Adaptive Message | `command` | reads data, page/HTTP output, requires command enablement | Before recommending Adaptive Message operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/adaptivemessage-commands) |
| Cache | `command` | page/HTTP output, requires command enablement | Before recommending Cache operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/cache-commands) |
| Calendar Events | `command` | reads data, SQL/entity access, requires command enablement | Before recommending Calendar Events operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/calendar-events) |
| Entity | `command` | reads data, SQL/entity access, requires command enablement | Before recommending Entity operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/entity-commands) |
| Event Scheduled Instance | `command` | reads data, SQL/entity access, requires command enablement | Before recommending Event Scheduled Instance operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/event-scheduled-instance) |
| Interaction Content Channel Item Write | `command` | mutates data, requires command enablement | Before recommending Interaction Content Channel Item Write operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write) |
| Interaction Intent Write | `command` | reads data, mutates data, requires command enablement | Before recommending Interaction Intent Write operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/interaction-intent-write) |
| Interaction Write | `command` | mutates data, requires command enablement | Before recommending Interaction Write operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/interaction-write) |
| JavaScript | `command` | page/HTTP output, requires command enablement | Before recommending JavaScript operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/javascript-commands) |
| Personalize | `command` | reads data, page/HTTP output, requires command enablement | Before recommending Personalize operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/personalize-commands) |
| Print ZPL | `command` | external I/O, requires command enablement | Before recommending Print ZPL operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/print-zpl) |
| Search | `command` | reads data, requires command enablement | Before recommending Search operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/search-commands) |
| SQL | `command` | reads data, mutates data, SQL/entity access, requires command enablement | Before recommending SQL operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/sql-commands) |
| Stylesheet | `command` | page/HTTP output, requires command enablement | Before recommending Stylesheet operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/stylesheet-commands) |
| Web Request | `command` | external I/O, requires command enablement | Before recommending Web Request operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/web-request-commands) |
| Workflow Activate | `command` | mutates data, workflow launch, requires command enablement | Before recommending Workflow Activate operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/commands/workflow-activate-commands) |
| CreateEntitySet | `filter` | mutates data, SQL/entity access | Before recommending CreateEntitySet operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| CreateShortLink | `filter` | mutates data | Before recommending CreateShortLink operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| DeleteUserPreference | `filter` | mutates data | Before recommending DeleteUserPreference operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/person-filters) |
| EntityFromCachedObject | `filter` | reads data, SQL/entity access | Before recommending EntityFromCachedObject operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| IsInDataView | `filter` | reads data, SQL/entity access | Before recommending IsInDataView operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PageRedirect | `filter` | page/HTTP output | Before recommending PageRedirect operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PersonImpersonationToken | `filter` | reads data, page/HTTP output | Before recommending PersonImpersonationToken operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonTokenCreate | `filter` | reads data, page/HTTP output | Before recommending PersonTokenCreate operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonTokenRead | `filter` | reads data | Before recommending PersonTokenRead operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Postback | `filter` | page/HTTP output | Before recommending Postback operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| RockInstanceConfig | `filter` | reads data | Before recommending RockInstanceConfig operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| RunLava | `filter` | page/HTTP output | Before recommending RunLava operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SetUserPreference | `filter` | mutates data | Before recommending SetUserPreference operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/person-filters) |
| UpdatePersistedDataset | `filter` | mutates data | Before recommending UpdatePersistedDataset operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| UploadBinaryFile | `filter` | mutates data | Before recommending UploadBinaryFile operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| WriteCookie | `filter` | mutates data, page/HTTP output | Before recommending WriteCookie operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Creating APIs Using Lava | `lava_api` | reads data, mutates data, external I/O, page/HTTP output | Before recommending Creating APIs Using Lava operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/lava-api) |
| Using Lava Remotely | `remote_lava` | reads data, mutates data, external I/O, page/HTTP output | Before recommending Using Lava Remotely operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/remote-lava) |
| Lava With Obsidian | `obsidian` | reads data, page/HTTP output | Before recommending Lava With Obsidian operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/obsidian) |
| Workflows and Lava | `workflow` | reads data, mutates data, workflow launch | Before recommending Workflows and Lava operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance. | [official](https://community.rockrms.com/lava/workflows) |

## Medium-Risk Rows

| Name | Category | Safety Notes | Official Page |
| --- | --- | --- | --- |
| DB Transaction | `command` | requires command enablement | [official](https://community.rockrms.com/lava/commands/db-transaction) |
| Delete Entity | `command` | reads data, requires command enablement | [official](https://community.rockrms.com/lava/commands/delete-entity) |
| Execute | `command` | requires command enablement | [official](https://community.rockrms.com/lava/commands/execute-commands) |
| Getting Started | `command` | requires command enablement | [official](https://community.rockrms.com/lava/commands/getting-started) |
| HTTP Response | `command` | requires command enablement | [official](https://community.rockrms.com/lava/commands/http-response) |
| Modify Entity | `command` | reads data, requires command enablement | [official](https://community.rockrms.com/lava/commands/modify-entity) |
| Observe | `command` | requires command enablement | [official](https://community.rockrms.com/lava/commands/observe) |
| Render Lava Endpoint | `command` | requires command enablement | [official](https://community.rockrms.com/lava/commands/render-lava-endpoint) |
| Set Culture | `command` | page/HTTP output, requires command enablement | [official](https://community.rockrms.com/lava/commands/setculture-commands) |
| Tag List | `command` | reads data | [official](https://community.rockrms.com/lava/commands/taglist-commands) |
| AddCssLink | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddLinkTagToHead | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddMetaTagToHead | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddResponseHeader | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddScriptLink | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddSegment | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| AppendFollowing | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AppendSegments | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AppendWatches | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Attributes | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/attribute-filters) |
| Campus | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Children | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Client | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Debug | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Decrypt | `filter` | rendering/context dependent | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Encrypt | `filter` | rendering/context dependent | [official](https://community.rockrms.com/lava/filters/text-filters) |
| FamilySalutation | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| FilterFollowed | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FilterUnfollowed | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FromCache | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FromIdHash | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| GeofencingGroupMembers | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GeofencingGroups | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GetPersonAlternateId | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GetUserPreference | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Group | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GroupByGuid | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| GroupById | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Groups | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GroupsAttended | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GuidToId | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| HasRightsTo | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| HasSignedDocument | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| HeadOfHousehold | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| HtmlDecode | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ImageUrl | `filter` | reads data, page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| IsFollowed | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| IsInSecurityRole | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| LastAttendedGroupOfType | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| NearestCampus | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| NearestGroup | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| NearestGroups | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Notes | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Page | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PageParameter | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PageRoute | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Parents | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersistedDataset | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PersonActionIdentifier | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonalizationItems | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByAliasGuid | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByAliasId | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByGuid | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonById | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByPersonActionIdentifier | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByPersonAlternateId | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PhoneNumber | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Property | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PropertyToKeyValue | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ReadCookie | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| RenderStructuredContentAsHtml | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ResolveRockUrl | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SetPageTitle | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SetUrlParameter | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SortByAttribute | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Spouse | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Steps | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| StripHtml | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ToCssClass | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ToIdHash | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Url | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| XamlWrap | `filter` | page/HTTP output | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ZebraPhoto | `filter` | reads data | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Include | `tag` | rendering/context dependent | [official](https://community.rockrms.com/lava/tags/include-tags) |
| Return | `tag` | page/HTTP output | [official](https://community.rockrms.com/lava/tags/return-tags) |
| Authoring Shortcodes | `shortcode` | page/HTTP output | [official](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes) |
| Intro to Shortcodes | `shortcode` | page/HTTP output | [official](https://community.rockrms.com/lava/shortcodes/intro-to-shortcodes) |
| The Power of Shortcode Blocks | `shortcode` | page/HTTP output | [official](https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks) |
| Types of Shortcodes | `shortcode` | page/HTTP output | [official](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes) |

## Flag Matrix

| Name | Reads | Mutates | External I/O | HTTP/Page Output | Workflow | SQL/Entity | Enablement | Official Page |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Adaptive Message | yes | no | no | yes | no | no | yes | [official](https://community.rockrms.com/lava/commands/adaptivemessage-commands) |
| Cache | no | no | no | yes | no | no | yes | [official](https://community.rockrms.com/lava/commands/cache-commands) |
| Calendar Events | yes | no | no | no | no | yes | yes | [official](https://community.rockrms.com/lava/commands/calendar-events) |
| DB Transaction | no | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/db-transaction) |
| Delete Entity | yes | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/delete-entity) |
| Entity | yes | no | no | no | no | yes | yes | [official](https://community.rockrms.com/lava/commands/entity-commands) |
| Event Scheduled Instance | yes | no | no | no | no | yes | yes | [official](https://community.rockrms.com/lava/commands/event-scheduled-instance) |
| Execute | no | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/execute-commands) |
| Getting Started | no | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/getting-started) |
| HTTP Response | no | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/http-response) |
| Interaction Content Channel Item Write | no | yes | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write) |
| Interaction Intent Write | yes | yes | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/interaction-intent-write) |
| Interaction Write | no | yes | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/interaction-write) |
| JavaScript | no | no | no | yes | no | no | yes | [official](https://community.rockrms.com/lava/commands/javascript-commands) |
| Modify Entity | yes | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/modify-entity) |
| Observe | no | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/observe) |
| Personalize | yes | no | no | yes | no | no | yes | [official](https://community.rockrms.com/lava/commands/personalize-commands) |
| Print ZPL | no | no | yes | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/print-zpl) |
| Render Lava Endpoint | no | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/render-lava-endpoint) |
| Search | yes | no | no | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/search-commands) |
| Set Culture | no | no | no | yes | no | no | yes | [official](https://community.rockrms.com/lava/commands/setculture-commands) |
| SQL | yes | yes | no | no | no | yes | yes | [official](https://community.rockrms.com/lava/commands/sql-commands) |
| Stylesheet | no | no | no | yes | no | no | yes | [official](https://community.rockrms.com/lava/commands/stylesheet-commands) |
| Tag List | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/commands/taglist-commands) |
| Web Request | no | no | yes | no | no | no | yes | [official](https://community.rockrms.com/lava/commands/web-request-commands) |
| Workflow Activate | no | yes | no | no | yes | no | yes | [official](https://community.rockrms.com/lava/commands/workflow-activate-commands) |
| Abs | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| AddCssLink | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddLinkTagToHead | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddMetaTagToHead | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddResponseHeader | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Address | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| AddScriptLink | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AddSegment | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| AddToArray | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| AddToDictionary | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| AddToMergeFields | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AdjustHue | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| AllKeysFromDictionary | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Append | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| AppendFollowing | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AppendSegments | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AppendWatches | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsBoolean | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsDateTime | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsDateTimeUtc | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| AsDecimal | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsDictionary | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| AsDouble | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsEnum | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| AsGuid | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsInteger | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AsString | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| AtLeast | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| AtMost | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Attributes | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/attribute-filters) |
| Base64Encode | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Campus | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Capitalize | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Ceiling | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Children | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Client | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Compact | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Concat | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Contains | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| CreateEntitySet | no | yes | no | no | no | yes | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| CreateShortLink | no | yes | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Darken | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Date | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DateAdd | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DateDiff | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DateRangeFromSlidingFormat | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DatesFromICal | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DaysFromNow | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DaysInMonth | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DaysSince | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| DaysUntil | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| Debug | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Decrypt | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Default | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| DeleteUserPreference | no | yes | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Desaturate | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Distinct | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| DividedBy | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Downcase | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Encrypt | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| EntityFromCachedObject | yes | no | no | no | no | yes | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Escape | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| EscapeDataString (aka UrlEncode) | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| EscapeOnce | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| FadeIn | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| FadeOut | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| FamilySalutation | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| FilterFollowed | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FilterUnfollowed | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| First | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Floor | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Format | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| FormatAsCurrency | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| FromBase64 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FromCache | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FromIdHash | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FromJSON | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| FromMarkdown | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| GeofencingGroupMembers | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GeofencingGroups | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GetPersonAlternateId | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GetUserPreference | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Grayscale | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Group | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GroupBy | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| GroupByGuid | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| GroupById | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Groups | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GroupsAttended | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| GuidToId | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| HasRightsTo | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| HasSignedDocument | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| HeadOfHousehold | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| HmacSha1 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| HmacSha256 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| HtmlDecode | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Humanize | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| HumanizeDateTime | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| HumanizeTimeSpan | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| ImageUrl | yes | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Index | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Indexer | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| IsDateBetween | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| IsFollowed | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| IsInDataView | yes | no | no | no | no | yes | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| IsInSecurityRole | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Join | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Last | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| LastAttendedGroupOfType | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Lighten | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Linkify | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Map | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Md5 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| MetersToMiles | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| MilesToMeters | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Minus | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Mix | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Modulo | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| NearestCampus | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| NearestGroup | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| NearestGroups | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| NewlineToBr | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| NextDayOfTheWeek | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| Notes | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| NumberToOrdinal | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| NumberToOrdinalWords | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| NumberToRomanNumerals | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| NumberToWords | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| ObfuscateEmail | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Object | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| OrderBy | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Page | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PageParameter | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PageRedirect | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PageRoute | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Parents | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersistedDataset | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PersonActionIdentifier | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonalizationItems | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByAliasGuid | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByAliasId | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByGuid | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonById | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByPersonActionIdentifier | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonByPersonAlternateId | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonImpersonationToken | yes | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonTokenCreate | yes | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PersonTokenRead | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| PhoneNumber | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Pluralize | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| PluralizeForQuantity | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Plus | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Possessive | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Postback | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Prepend | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Property | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| PropertyToKeyValue | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| RandomNumber | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| ReadCookie | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ReadTime | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RegExMatch | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RegExMatchValue | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RegExMatchValues | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RegExReplace | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Remove | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RemoveFirst | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RemoveFromArray | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| RemoveFromDictionary | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| RenderStructuredContentAsHtml | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Replace | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ReplaceFirst | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ReplaceLast | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ResolveRockUrl | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Reverse | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Right | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| RockInstanceConfig | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Round | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| RunLava | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SanitizeSql | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Saturate | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Select | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| SentenceCase | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| SetPageTitle | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SetUrlParameter | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| SetUserPreference | no | yes | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Sha1 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Sha256 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Shade | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| Shuffle | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Singularize | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Size | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Size | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Slice | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Slice (arrays) | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Sort | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| SortByAttribute | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| SortNatural | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| Split | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Spouse | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Steps | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| StripHtml | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| StripNewlines | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Sum | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| SundayDate | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| TimeOfDay | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| Times | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Tint | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/color-filters) |
| TitleCase | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ToBase64 | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ToCssClass | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ToIdHash | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ToJSON | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ToMarkdown | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ToMidnight | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/date-filters) |
| ToPascal | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| ToQuantity | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| ToString | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/numeric-filters) |
| Trim | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| TrimEnd | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| TrimStart | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Truncate | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| TruncateWords | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| UnescapeDataString (aka UrlDecode) | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Uniq | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| UniqueIdentifier | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Upcase | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| UpdatePersistedDataset | no | yes | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| UploadBinaryFile | no | yes | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Url | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| Where | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| WithFallback | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/text-filters) |
| Working With Arrays | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/array-filters) |
| WriteCookie | no | yes | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| XamlWrap | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/filters/other-filters) |
| ZebraPhoto | yes | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/filters/person-filters) |
| Assign and Capture Tags | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/variable-tags) |
| Case | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/case-tags) |
| Comment | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/comment-tags) |
| Cycle | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/cycle-tags) |
| For | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/for-tags) |
| If / Else | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/if-else-tags) |
| Include | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/include-tags) |
| Lava | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/lava-tags) |
| Observe | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/observe) |
| Raw | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/raw-tags) |
| Return | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/tags/return-tags) |
| Unless | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/tags/unless-tags) |
| Authoring Shortcodes | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes) |
| Intro to Shortcodes | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/shortcodes/intro-to-shortcodes) |
| Passing in Objects | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/shortcodes/passing-in-objects) |
| The Power of Shortcode Blocks | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks) |
| Types of Shortcodes | no | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes) |
| Creating APIs Using Lava | yes | yes | yes | yes | no | no | no | [official](https://community.rockrms.com/lava/lava-api) |
| Using Lava Remotely | yes | yes | yes | yes | no | no | no | [official](https://community.rockrms.com/lava/remote-lava) |
| Lava With Obsidian | yes | no | no | yes | no | no | no | [official](https://community.rockrms.com/lava/obsidian) |
| Fluid Differences | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/fluid/differences) |
| Workflows and Lava | yes | yes | no | no | yes | no | no | [official](https://community.rockrms.com/lava/workflows) |
| Lava Style Guide | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/style) |
| About Lava Fluid | no | no | no | no | no | no | no | [official](https://community.rockrms.com/lava/fluid) |
