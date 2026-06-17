---
id: authored-connections
title: Connections
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Connections

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Connections index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Connections is Rock RMS's engagement pipeline system. Use it when a person has expressed interest, needs follow-up, is being routed toward a ministry outcome, or must be tracked through a repeatable relational process. A Connection Request is not just a note, task, workflow, or group member record. It is a structured pipeline item tied to a person, a Connection Type, a Connection Opportunity, a status, a state, activities, assignments, campus context, and optional automation.

The fastest working mental model is:

- **Connection Type**: the broad pipeline, such as serving, care, next steps, membership, baptism, new guest follow-up, or ministry onboarding.
- **Connection Opportunity**: the specific destination or ministry option inside that type, such as Kids Team, Production Team, Small Groups, Prayer Team, or a care ministry.
- **Connection Request**: the individual person's active or historical request inside that opportunity.
- **Connection Status**: the configurable stage label, such as New, Contacted, Assigned, In Progress, Waiting, Follow-Up, Connected, or Not Interested.
- **Connection State**: the broader lifecycle bucket used by Rock behavior and filtering. Common operational buckets include active work, future follow-up, inactive/closed, and connected/completed behavior. Always verify the available state values in the live instance.
- **Connector**: the person assigned to follow up on the request.
- **Activities**: the logged touches, notes, communications, status movements, and follow-up actions that make the request auditable.

For agents doing real Rock work, start with the request row or opportunity row, then walk outward. A Connections problem is usually one of five things:

1. The request exists but is hidden by state/status/campus/opportunity filters.
2. The request is assigned to the wrong connector or no connector.
3. The status automation, workflow, or future follow-up behavior moved it somewhere the user did not expect.
4. The opportunity is inactive, misconfigured, missing a connector group, or using the wrong attributes/security.
5. The UI block, mobile block, board/list view, or Lava template is filtering differently than the admin expects.

Official Engagement documentation places Connections under `People > Connections` and describes it as the operational page for reviewing requests grouped by Connection Opportunity and Connection Type, with card and list experiences for individual requests ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). RockU has dedicated training pages for Connections Overview, Connection Types, Connection Opportunities, request status automation, list, and board experiences, but the source excerpts for several 2026 pages are mostly metadata and should be treated as pointers unless the live video/page is reviewed ([Connections Overview](https://community.rockrms.com/rocku/engagement/overview), [Connection Types](https://community.rockrms.com/rocku/engagement/connection-types), [Connection Opportunities](https://community.rockrms.com/rocku/engagement/connection-opportunities), [Connection Request Status Automation](https://community.rockrms.com/rocku/engagement/connection-request-status-automation), [Connections List](https://community.rockrms.com/rocku/engagement/connections-list-1), [Connections Board](https://community.rockrms.com/rocku/engagement/connections-board)).

Version caveat: Connections changed materially over time. Rock v10 added existing Connections chapters and capability around request signup attributes and campaigns in the Engagement documentation change log; Rock v12 removed the old need for a separate request detail page when using the board-style request detail experience; Rock v17.2 fixed inherited request attributes in the Connection Opportunity Signup block; Rock v18.1 improved the Connection Request Board with default state/status filters, campus filtering, connector preferences, and workflow filtering/reordering; Rock v18.3 fixed multiple board/list/detail display issues ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39), [release notes](https://www.rockrms.com/releasenotes)).

## 2. Scope And Terminology

This guide covers the Connections concept area: connection types, opportunities, requests, statuses, states, boards, lists, assignments, connector follow-up, reporting, mobile blocks, API/source-code landmarks, and operational troubleshooting.

It depends on six related Rock domains:

- **People**: every request belongs to a person or requester context. Person profile visibility and record source behavior can affect how staff interpret the request.
- **Workflows**: connection statuses and opportunities can trigger or filter workflows, and workflows are often used to create requests, assign connectors, send reminders, or close loops.
- **Groups**: opportunities often map to placement groups, serving teams, connector groups, or ministry groups.
- **Communications**: activities and follow-up often involve email/SMS, and communication permission/compliance can affect automation.
- **Security**: the board, list, opportunity detail, API endpoints, group placement, and attributes all have permissions that can hide or expose data.
- **Reporting**: request pipelines are usually monitored through data views, reports, dashboards, board/list filters, and operational snapshots.

Terms used in this guide:

**Connection Type**  
A high-level container for a family of related opportunities and statuses. It defines much of the administrative behavior for the pipeline: statuses, enabled views, idle thresholds, request detail behavior, future follow-up behavior, attributes, and other settings. The official docs describe settings such as days until idle, request detail page behavior for older versions, future follow-up, and connection type attributes ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

**Connection Opportunity**  
A specific destination inside a Connection Type. Model Map identifies Connection Opportunity as an Engagement model ([Model Map](https://community.rockrms.com/ModelMap)). Source-code and mobile docs show that opportunities are commonly selected by Connection Type and are ordered by configured order and name in reporting components ([Connection Opportunity filter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs), [Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list)).

**Connection Request**  
The person-specific instance of interest or follow-up. A request carries state/status, opportunity, requester/person, campus, connector assignment, activity history, attributes, and possibly placement context. The mobile Connection Request List block is specifically designed to show not-yet-completed requests for one opportunity and excludes requests in a Connected state ([Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

**Connection Status**  
A configurable stage within a Connection Type. Source-code view models expose status fields such as name, description, highlight color, active/default flags, note-required-on-completion, auto-inactivate behavior, due-date offsets, due-soon offsets, future-follow-up pause days, and automations ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs), [TypeScript status bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusBag.d.ts)).

**Connection State**  
A lifecycle bucket separate from the configured status label. States are used by blocks and boards for filtering and behavior. Do not assume every instance uses the same displayed labels. Inspect the Connection Type, board/list block settings, and request rows in the live Rock instance. Release notes for v18.1 specifically mention new default Connection State and Status filter settings and that the board's State filter became required ([release notes](https://www.rockrms.com/releasenotes)).

**Connector**  
The assigned follow-up person. Connector options often come from configured groups. Source-code for the Connection Opportunity Detail view model shows a default connector options request accepting group GUIDs to fetch group members ([DefaultConnectorOptionsRequestBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionOpportunityDetail/DefaultConnectorOptionsRequestBag.cs)). The v2 API has a controller for Connection Opportunity Connector Groups, indicating connector group relationships are first-class API-addressable records with authenticated read/write endpoints controlled by security actions ([ConnectionOpportunityConnectorGroupsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)).

**Activity**  
An interaction or logged event on the request. Activities are central to auditability: who contacted the person, what happened, when status changed, what follow-up was scheduled, and whether the request is idle. Engagement documentation includes Activities as a core Connections section ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

**Board View, List View, Grid View, Snapshot View**  
Connection Type summary source-code exposes enabled view flags and convenience booleans for list, board, grid, and snapshot views ([ConnectionTypeSummaryBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs)). Treat view availability as configuration, not a universal guarantee.

## 3. Connections Mental Model

Connections sits between raw interest and completed ministry action. It is a pipeline, but it is not only a sales-style board. It is a relational operations system. The design assumes a person may enter through many channels, be triaged into a specific opportunity, be assigned to a connector, receive touches over time, move between statuses, be paused for future follow-up, and eventually be connected, transferred, inactivated, or left for reporting.

A practical model for agents:

1. **Entry**  
   A person enters the system through staff entry, self-service signup, mobile app, website form, workflow, API, import, event follow-up, or a manual request from the person's profile. The Engagement documentation includes "Entering New Requests", "Self-Service", and "Staff Entry" as official topics ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). Mobile docs provide an Add Connection Request block that creates a new connection request and can be constrained by connection type or opportunity page parameters ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request)).

2. **Routing**  
   The request is tied to a Connection Type and Opportunity. If only the type is known, the user or workflow may choose an opportunity later. If the opportunity is known up front, the UI can lock the form to that opportunity.

3. **Assignment**  
   A connector is assigned. Some organizations auto-assign by opportunity, campus, connector group, demographic fit, ministry area, workload, or staff rotation. Community recipes show real-world patterns such as a connector availability workflow and report, but those are community-contributed and should be validated before use ([connector report recipe](https://community.rockrms.com/recipes/446)).

4. **Follow-Up**  
   Connectors log activities, send communications, change status, schedule future follow-up, and possibly transfer the request. Rock's v18 documentation mentions future follow-up and a generated "Future Follow-up Complete" action when a request reaches its follow-up date ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

5. **Completion Or Closure**  
   A request may be completed as connected, closed as inactive, transferred to another opportunity, or placed into a follow-up state. The exact state/status semantics are instance configuration. Source-code for statuses includes automation fields that can auto-inactivate or auto-pause a request for future follow-up when a status is selected ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)).

6. **Measurement**  
   Managers inspect open volume, idle volume, due/due-soon requests, status distribution, new/completed trend, connector workload, campus mix, and opportunity health. Source-code exposes request counts per day, status distribution, and upcoming follow-up windows as queryable view-model/DTO concepts ([ConnectionRequestCountsPerDayBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs), [ConnectionRequestStatusDistribution source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestStatusDistribution.cs), [ConnectionRequestUpcomingFollowUpWindow source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestUpcomingFollowUpWindow.cs)).

The highest-yield diagnostic question is: "Which layer is wrong: the request, the opportunity, the type, the connector assignment, the view filter, or the automation?"

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. **Live Rock instance**  
   For operational questions, inspect the live record. Connection configuration is heavily instance-specific. Do not assume status names, state labels, connector groups, campus behavior, board filters, block settings, or workflow actions.

2. **Official Rock documentation**  
   The Engagement book is the main official conceptual source for Connections. It lists Connections sections such as State, Status, Activities, campus, request work, Lava, list view, bulk update, request detail, activity entry, transfer, badges, new requests, self-service, request attributes, and staff entry ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

3. **RockU**  
   RockU provides training coverage for Connections Overview, Connection Types, Connection Opportunities, Connection Request Status Automation, Connections List, Connections Board, and newer 2026 Connections videos. The source pack includes titles, presenters, and durations, but several hydrated excerpts show page errors rather than full training content, so use these as discovery/citation pointers unless you review the videos directly ([RockU Engagement Overview](https://community.rockrms.com/rocku/engagement/overview), [new RockU videos](https://community.rockrms.com/rocku/new)).

4. **Release notes**  
   Use release notes for version-specific behavior. The v18.1 and v18.3 Connection notes are especially relevant for board/list/detail behavior, default filters, connector preferences, workflow filtering, and display fixes ([release notes](https://www.rockrms.com/releasenotes)).

5. **Model Map and source code**  
   Use Model Map for model identity and source code for implementation landmarks. The source snippets show reporting filters, Obsidian view-model bags, REST controller paths, and fields exposed to the UI/API ([Model Map](https://community.rockrms.com/ModelMap), [Rock source repository](https://github.com/SparkDevNetwork/Rock)).

6. **Developer/mobile docs**  
   Use these for mobile app blocks, page parameters, query parameters, template merge fields, and block behavior. The source pack includes Connection Type List, Opportunity List, Add Request, Request List, and Request Detail references under the mobile Connection block family ([Connection mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection)).

7. **Community Q&A and recipes**  
   Use only as examples. A Q&A answer recommends the Connection Opportunity Search block and demonstrates a card layout using opportunity fields such as public name, summary, public attribute, and photo URL, but it is not official product documentation ([community Q&A](https://community.rockrms.com/ask/developing/2645)). A recipe for connector reporting and unavailability workflow is explicitly community-contributed and should be reviewed for fit, performance, and security before production use ([connector report recipe](https://community.rockrms.com/recipes/446)).

## 5. Core Configuration And Data Model

### Configuration Surfaces

The core administrative surfaces are:

- **Connection Type Detail**
- **Connection Opportunity Detail**
- **Connection Request Board**
- **Connection Request List**
- **Connection Request Detail**
- **Connection Opportunity Signup or Search**
- **Mobile Connection blocks**
- **Workflow actions and status automations**
- **Reports/Data Views for Connection Request**
- **Security settings on blocks, pages, attributes, groups, and REST/API endpoints**

Official documentation identifies `People > Connections` as the normal staff access point for request work and describes overview grouping by Connection Opportunity and Connection Type ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Connection Type Configuration

A Connection Type is the parent configuration for a pipeline. Verify these fields and child settings in the live instance:

- Name
- Description
- Icon CSS class
- Display order
- Active state
- Enabled views: list, board, grid, snapshot
- Connection statuses
- Default status
- Days until request considered idle
- Request detail page behavior
- Future follow-up setting
- Type-level request attributes
- Type-level workflows or automations, if configured
- Security
- Campus behavior
- Any status automation rules

Source-code shows a `ConnectionTypeSummaryBag` with icon CSS class, name, enabled view flags, and booleans for list, board, grid, and snapshot view availability ([ConnectionTypeSummaryBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs)). The documentation excerpt identifies "Days Until Request Considered Idle", "Connection Request Detail Page", "Enable Future Follow-up", and "Connection Type Attributes" as settings to consider ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

Agent check: if a user says "the board/list is missing", verify the type's enabled views and the page/block settings before assuming a data problem.

### Connection Status Configuration

Connection statuses are configured under the type. Source-code exposes these status properties:

- `Guid`
- `Name`
- `Description`
- `HighlightColor`
- `IsActive`
- `IsDefault`
- `IsNoteRequiredOnCompletion`
- `AutoInactivateState`
- `RequestStatusDueDateOffsetInDays`
- `RequestStatusDueSoonOffsetInDays`
- `AutoFutureFollowUpPauseInDays`
- `Automations`

These fields appear in the Obsidian view model for Connection Type Detail ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs), [TypeScript status bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusBag.d.ts)). Status automation bags include an automation name, data view, and group requirement filtering concepts ([ConnectionStatusAutomationBag TypeScript source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusAutomationBag.d.ts)).

Operationally, a status can be more than a label. It may:

- Become the default status for new requests.
- Require a note before completion.
- Move a request to inactive state.
- Pause a request into future follow-up.
- Affect due dates and due-soon indicators.
- Trigger or constrain automation.
- Carry display color in boards/lists.

Agent check: when a request "moved itself", inspect status automation first, then workflow history, then request history/activity.

### Connection Opportunity Configuration

Connection Opportunities are the specific routes inside a type. Verify:

- Connection Type
- Name and public name
- Summary/details
- Active state
- Display order
- Campus availability
- Connector groups
- Default connector
- Placement group, group type, or related group behavior
- Request attributes inherited from type and defined on opportunity
- Signup/self-service visibility
- Show/connect/complete behavior
- Workflows attached to the opportunity
- Security
- Advanced settings that hide or expose options while working requests

The Engagement docs mention advanced settings on Connection Opportunity configuration added in newer versions, allowing certain options to be hidden when working with requests ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). Release notes for v18.1 say workflows on the Connection Opportunity block can be reordered by drag-and-drop and filtered by age classification and include/exclude data views ([release notes](https://www.rockrms.com/releasenotes)).

Source-code for the reporting opportunity filter queries active opportunities by Connection Type and orders them by order then name ([ConnectionOpportunityFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs)). This is a useful implementation clue: if a report filter does not show an opportunity, check whether it is inactive, in the wrong type, or inaccessible.

### Connection Request Data

A request normally ties together:

- Requester/person
- Connection Opportunity
- Connection Type through the opportunity
- Status
- State
- Campus
- Connector person alias/person
- Created date
- Modified date
- Follow-up date
- Activities
- Attribute values
- Workflows/history
- Placement or group membership outcome, if relevant

Exact table column names and relationships should be verified in the live schema before writing SQL, because Rock versions and local customizations can differ.

Useful inspection approach:

- Start with `ConnectionRequest`.
- Join to `ConnectionOpportunity`.
- Join to `ConnectionType`.
- Join to `ConnectionStatus`.
- Join to `PersonAlias`/`Person` for requester and connector where applicable.
- Join to `Campus` if campus behavior matters.
- Inspect attribute values by entity type if custom request/opportunity/type attributes are involved.
- Check request history and activities if status/state changed unexpectedly.

Do not invent state/status mapping. Inspect the live request row, the configured status, and the board/list filters.

## 6. Primary Entities And Relationships

### Entity Relationship Map

At a concept level:

```text
ConnectionType
  has many ConnectionStatus
  has many ConnectionOpportunity
  has type-level Attributes
  configures enabled views and follow-up behavior

ConnectionOpportunity
  belongs to ConnectionType
  has many ConnectionRequest
  can have connector groups
  can have opportunity-level Attributes
  can have workflows and placement/group behavior

ConnectionRequest
  belongs to ConnectionOpportunity
  indirectly belongs to ConnectionType
  belongs to a Person/Requester
  may belong to a Campus
  may be assigned to a Connector
  has one current Status
  has one current State
  has many Activities
  has AttributeValues
  may trigger workflows

ConnectionStatus
  belongs to ConnectionType
  has display and automation behavior
  can affect due dates, inactive state, note requirement, future follow-up, and status automation

ConnectionOpportunityConnectorGroup
  links opportunities to groups that provide possible connectors
```

### ConnectionType

`ConnectionType` is the main administrative container. Reporting source-code uses `ConnectionTypeCache.All()` and orders types by `Order` then `Name` for filter definitions ([ConnectionTypeFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs)). That matters for agents because report dropdown order can reflect configured order, not alphabetical-only behavior.

### ConnectionOpportunity

`ConnectionOpportunity` is an Engagement model in Model Map ([Model Map](https://community.rockrms.com/ModelMap)). Opportunities are often the user-visible "thing someone wants to connect with." In public-serving websites, opportunity fields may be used to render cards or sign-up links. Community Q&A shows a practical Lava pattern using a Connection Opportunity Search block and opportunity fields, but agents should prefer official blocks when possible and treat the recipe as an example rather than a standard ([community Q&A](https://community.rockrms.com/ask/developing/2645)).

### ConnectionRequest

`ConnectionRequest` is the item staff work. Developer mobile docs say the mobile Connection Request List block lists requests for a single opportunity and does not pull down requests already in a Connected state because the block's purpose is to manage unfinished requests ([Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)). That exclusion is critical when debugging "missing" mobile requests.

### ConnectionStatus

`ConnectionStatus` is both display and behavior. The view model includes request-count and limited request-list concepts for status-based display ([ConnectionStatusViewModel source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionRequest/ConnectionStatusViewModel.cs)). In boards, statuses commonly act like columns or grouping units, but the exact UI depends on version and block.

### ConnectionOpportunityConnectorGroup

The generated REST v2 controller exposes authenticated CRUD-like endpoints under `api/v2/models/connectionopportunityconnectorgroups`, with read endpoints secured separately from write endpoints ([ConnectionOpportunityConnectorGroupsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)). This confirms connector group relationships can be managed as model records, but agents should use the UI unless explicitly asked to automate API writes.

## 7. Common Connections Workflows

### Staff Creates A Request

A staff-created request typically starts from a person profile or Connections area. Verify:

1. Person record is correct.
2. Connection Type is correct.
3. Opportunity is correct.
4. Campus is correct.
5. Status defaults as expected.
6. Connector assignment occurs or remains intentionally blank.
7. Request attributes are captured.
8. Activities or notes document the source.

The Engagement documentation includes "Staff Entry" as an official Connections topic ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Person Self-Service Signup

Self-service lets a person create a request through a website, mobile app, or sign-up block. Verify:

1. The user is authenticated or requester is identified.
2. The block is constrained to the expected Connection Type/Opportunity.
3. Public opportunities are active and visible.
4. Request attributes inherited from type and opportunity appear.
5. The post-save action sends the person somewhere sensible.
6. New person creation and record source behavior are expected.
7. Security does not expose staff-only opportunities.

The Add Connection Request mobile block can be configured with allowed Connection Types and post-save/post-cancel actions. It accepts page parameters such as `RequesterId`, `ConnectionTypeId`, and `ConnectionOpportunityId`; when type or opportunity parameters are provided, the selection can be locked or narrowed ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request)).

Version caveat: Rock v17.2 fixed an issue where the Connection Opportunity Signup block only showed opportunity-defined request attributes instead of including attributes inherited from the Connection Type ([release notes](https://www.rockrms.com/releasenotes)). If an inherited request attribute is missing on signup, verify Rock version and block behavior.

### Connector Works The Request

A connector usually:

1. Opens board/list/detail.
2. Filters to assigned requests.
3. Reviews the person's context.
4. Adds an activity.
5. Sends a communication or logs a touch.
6. Changes status or state.
7. Schedules future follow-up if needed.
8. Completes/connects the request or transfers it.

The Engagement docs include "Connection Request Detail", "Adding Activities", "Transferring a Request", and "Displaying Badges" as official areas ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Manager Reviews Pipeline

A manager checks:

- Open requests by type/opportunity
- Idle requests
- Due or due-soon requests
- Future follow-up volume
- Status distribution
- New vs completed trend
- Connector workload
- Campus distribution
- Opportunities with no connector groups
- Automation failures
- Requests stuck in legacy or hidden states

Source-code exposes status distribution query options that can filter by campus and opportunity ([ConnectionRequestStatusDistributionQueryOptions source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/Options/ConnectionRequestStatusDistributionQueryOptions.cs)). Upcoming follow-up query options also accept campus and opportunity filters ([ConnectionRequestUpcomingFollowUpWindowQueryOptions source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/Options/ConnectionRequestUpcomingFollowUpWindowQueryOptions.cs)).

### Workflow Automation Runs

Common automation:

- Create a request from a form or workflow.
- Auto-assign connector.
- Change status after time elapsed.
- Send reminders.
- Add activity records.
- Move to future follow-up.
- Close stale requests.
- Notify supervisors.
- Sync placement into a group.

RockU has a specific "Connection Request Status Automation" training page ([RockU status automation](https://community.rockrms.com/rocku/engagement/connection-request-status-automation)). Source-code confirms connection status automation is modeled in the Connection Type Detail view model ([ConnectionStatusAutomationBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusAutomationBag.cs)).

## 8. Opportunities Deep Dive

### What Opportunities Are For

Use a Connection Opportunity when the organization needs a distinct destination inside a broader pipeline. Examples:

- Serving > Worship
- Serving > Kids
- Serving > Production
- Care > Benevolence
- Care > Hospital Visit
- Next Steps > Baptism
- Next Steps > Membership
- Groups > Small Group Interest
- Guest Follow-Up > First-Time Guest
- Prayer > Prayer Team Follow-Up

Opportunities are useful because they provide routing, ownership, reporting, and configuration boundaries. If every request in a type follows the same owners, workflows, and reporting, one opportunity may be enough. If different ministries own different responses, separate opportunities are usually cleaner.

### Key Opportunity Settings To Inspect

For an opportunity, inspect:

- **Active**: inactive opportunities may disappear from selection/report filters.
- **Connection Type**: wrong type means wrong statuses and wrong board context.
- **Name/Public Name**: internal and public labels may differ.
- **Summary/Details**: used by public listings or staff context.
- **Photo/Image**: often used by public opportunity cards.
- **Order**: affects display order in selectors and filters.
- **Campus**: determines routing and filtering if campus-aware.
- **Connector Groups**: determines who can be assigned.
- **Default Connector**: may prefill or automate assignment.
- **Placement Groups**: if opportunity results in group membership.
- **Attributes**: distinguish request attributes, opportunity attributes, and type-level inherited attributes.
- **Workflows**: request lifecycle automation.
- **Security**: who can view, edit, assign, or administer.

Source-code for default connector options takes group GUIDs and fetches associated group members, which reinforces that connector assignment is often group-backed ([DefaultConnectorOptionsRequestBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionOpportunityDetail/DefaultConnectorOptionsRequestBag.cs)).

### Opportunity Lists And Public Discovery

For mobile, the Connection Opportunity List block displays opportunities for a single Connection Type. The docs explain that the block needs the Connection Type context, often by obtaining the type GUID and using query parameters or block settings. The page includes header and opportunity templates, merge fields, no-request content, detail page behavior, and styling sections ([Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list)).

For web/Lava, prefer built-in Connection Opportunity Search/List/Signup blocks where possible. Community Q&A shows an example where the Connection Opportunity Search block is used to render opportunity cards, including filtering on a public attribute and using opportunity summary/public name/photo URL in Lava ([community Q&A](https://community.rockrms.com/ask/developing/2645)). Treat that as a pattern to adapt, not a canonical implementation.

### Opportunity Workflow Configuration

Release notes for v18.1 add two important capabilities:

- Workflows on the Connection Opportunity block can be reordered with drag-and-drop.
- Workflows can be filtered so they apply only to requests matching age classification and/or include/exclude data views ([release notes](https://www.rockrms.com/releasenotes)).

Agent checks:

- If a workflow did not run, inspect workflow filter criteria on the opportunity.
- If workflows ran in the wrong order, inspect the configured workflow order.
- If a workflow applies to children/adults differently, inspect age classification.
- If a data-view filter is involved, test the person against the data view directly.
- If a data view changed recently, re-check cached results or persisted values if applicable in that instance.

## 9. Requests And Statuses Deep Dive

### Request Lifecycle

A request normally moves through:

1. New/intake status.
2. Assignment.
3. First contact.
4. In progress.
5. Waiting/future follow-up.
6. Completed/connected or inactive/closed.
7. Reporting/history.

Do not hard-code those names. Statuses are configured per Connection Type. The official docs include separate sections for State and Status, implying they are distinct concepts ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Status Vs State

Use this distinction carefully:

- **Status** is usually ministry-configured and human-readable.
- **State** is a lifecycle category used by Rock views and behavior.

A status can cause a state change. Source-code exposes `AutoInactivateState` and `AutoFutureFollowUpPauseInDays` on statuses, which means selecting a status can change more than the displayed label ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)).

Agent rule: never say "status X means closed" unless you inspected the live Connection Type's status configuration.

### Note Required On Completion

The status model includes `IsNoteRequiredOnCompletion` ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)). If a connector cannot complete a request, check whether the chosen status requires a note and whether the UI is surfacing validation clearly.

### Due Dates And Due-Soon Behavior

Status configuration can include:

- Due date offset in days.
- Due-soon offset in days.

These fields appear in the status view model ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)). In practice, due indicators depend on request date, status date, current date, and block/report logic. Verify exact calculations in the live version before writing automation.

### Future Follow-Up

Future follow-up is a major Connections behavior. The Engagement docs identify "Enable Future Follow-up" on Connection Type and mention a generated future follow-up action when requests reach their follow-up date in newer versions ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). Source-code includes an upcoming follow-up window DTO with `ConnectionTypeId`, start/end offsets, and count, plus query options for campus and opportunity filters ([ConnectionRequestUpcomingFollowUpWindow source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestUpcomingFollowUpWindow.cs), [query options source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/Options/ConnectionRequestUpcomingFollowUpWindowQueryOptions.cs)).

Troubleshooting future follow-up:

- Confirm the Connection Type has future follow-up enabled.
- Confirm the selected status can auto-pause to future follow-up if expected.
- Inspect the request's follow-up date.
- Check whether the board/list filter includes future follow-up state.
- Verify scheduled jobs or status automation if automatic return did not occur.
- Inspect request history and activities.
- Check release notes for known version issues. The release excerpt references fixes around future follow-up date behavior in Connection Request workflows in the v17.5 area, but the provided snippet is truncated, so verify details in full release notes ([release notes](https://www.rockrms.com/releasenotes)).

### Status Automation

Status automation is configured at the Connection Type/status layer. RockU has a dedicated training page for it ([RockU status automation](https://community.rockrms.com/rocku/engagement/connection-request-status-automation)). Source-code shows a status can have a list of automation bags and that automation may include a data view and group requirement filter concept ([ConnectionStatusAutomationBag TypeScript source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusAutomationBag.d.ts)).

When diagnosing automation:

1. Identify the current status.
2. Inspect automations on that status.
3. Inspect any data view filter.
4. Inspect group requirement filter.
5. Check whether the request's person qualifies now and qualified when the automation ran.
6. Check workflow history if automation launches workflows.
7. Check job history if a scheduled job mediates the automation.
8. Confirm security context if automation depends on actions requiring permissions.

## 10. Boards And Lists Deep Dive

### Board View

The Connection Request Board is the staff operational surface for managing requests visually. Release notes for v18.1 specifically mention improvements to the board:

- Campus filtering updates.
- Connector preferences.
- Workflow configuration updates.
- New default Connection State and Status filter settings.
- Required State filter setting.
- Opportunity workflow ordering and request applicability filters ([release notes](https://www.rockrms.com/releasenotes)).

Agent implications:

- A missing request may be filtered out by default state/status settings.
- A campus filter may hide requests.
- Connector preferences may affect what a user sees by default.
- A required state filter may force an explicit lifecycle subset.
- Workflow buttons/actions may be filtered per request.

### List View

List view is better for scanning, sorting, bulk work, and reporting-like inspection. Engagement documentation includes List View and Connection Request Bulk Update topics ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). Release notes for v18.3 fixed sorting by date in the Connection Request List block, which matters if staff report "the list order is wrong" ([release notes](https://www.rockrms.com/releasenotes)).

Agent checks:

- Confirm the list block version and settings.
- Confirm sort column and sort direction.
- Check if a version-specific bug applies.
- Check whether state/status/campus/opportunity filters match the user's expectation.
- Compare list view against board view and direct database/API query.

### Grid And Snapshot Views

Source-code includes enabled flags for grid and snapshot views along with list and board ([ConnectionTypeSummaryBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs)). If a user expects snapshot analytics and does not see them, inspect enabled view flags, block settings, security, and Rock version.

### Mobile Views

Mobile docs include the Connection block family and specific pages for Add Connection Request, Connection Opportunity List, and Connection Request List ([Connection mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection)). Key mobile behaviors from the source pack:

- Opportunity List displays opportunities for a single Connection Type ([Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list)).
- Add Request can constrain available Connection Types, and page parameters can lock type/opportunity/requester context ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request)).
- Request List is opportunity-specific and excludes requests in Connected state ([Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

## 11. Assignment And Follow-Up Deep Dive

### Connector Assignment

Connector assignment is the operational handoff. A request without an owner is a leakage point.

Inspect:

- Opportunity connector groups.
- Default connector.
- Connector group membership.
- Group member active status.
- Connector campus.
- Person record status.
- Security.
- Auto-assignment workflow.
- Manual reassignment history.
- Connector workload.

Source-code for default connector options indicates group GUIDs are used to fetch group members for selecting a default connector ([DefaultConnectorOptionsRequestBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionOpportunityDetail/DefaultConnectorOptionsRequestBag.cs)). REST v2 exposes Connection Opportunity Connector Group records with authenticated read and secured write behavior ([ConnectionOpportunityConnectorGroupsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)).

### Follow-Up Activities

Activities are the audit trail. Require connectors to log:

- Contact attempt.
- Successful conversation.
- Email/SMS sent.
- Voicemail.
- No response.
- Status change rationale.
- Future follow-up date.
- Transfer reason.
- Completion note.

If activities are missing, the request may be operationally incomplete even if the status is correct. Engagement docs include Activities and Adding Activities as core Connections topics ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Connector Availability And Workload

A community recipe describes using connector groups, workflow, and reports to manage connector assignments, availability, leave, workload, and matching by ministry/demographic fit ([connector report recipe](https://community.rockrms.com/recipes/446)). Because recipes are community-contributed and explicitly not core-reviewed, validate:

- Security of reports and workflows.
- SQL performance.
- Whether it assumes local group structures.
- Whether it writes attributes or workflow state.
- Whether connector availability should be modeled as group membership, person attribute, schedule, workflow entry, or a custom table.
- Whether the report respects campus and ministry boundaries.

### Future Follow-Up Discipline

Future follow-up is useful, but it can also become a hiding place for stalled requests. Operational guardrails:

- Require a future follow-up date and reason.
- Dashboard requests coming due in the next 7/14/30 days.
- Dashboard overdue future follow-ups separately.
- Monitor requests that repeatedly move to future follow-up.
- Train connectors to close requests when appropriate instead of indefinite pauses.

Source-code upcoming follow-up windows count requests in offset windows by type and optionally campus/opportunity, which is a useful model for operational reporting ([ConnectionRequestUpcomingFollowUpWindow source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestUpcomingFollowUpWindow.cs)).

## 12. Related Rock Areas: People, Workflows, Groups, Communications, Security, Reporting

### People

Connections is person-centered. Always verify the correct person:

- Duplicate records can split connection history.
- A person may have multiple requests across opportunities.
- Record status can affect whether a person appears in selectors.
- Person profile blocks may show only selected states.
- v18.1 CRM release notes added a "Serving Connection" record source and updated the Connection Opportunity Signup block to assign that source when new individuals are added through a sign-up ([release notes](https://www.rockrms.com/releasenotes)).

Agent check: if a request was created from signup for a new person, inspect record source and duplicate records.

### Workflows

Workflows can create, update, assign, close, and communicate about requests. Opportunity workflows received v18.1 configuration improvements for ordering and filters ([release notes](https://www.rockrms.com/releasenotes)).

Inspect:

- Workflow type.
- Trigger source.
- Entity type and entity id.
- Request attributes passed to workflow.
- Person aliases.
- Current activity state.
- Exceptions.
- Whether the workflow is tied to type, opportunity, status automation, page block, or external form.

### Groups

Groups are commonly involved in:

- Connector groups.
- Serving teams.
- Placement groups.
- Campus teams.
- Ministry ownership.
- Group requirements.

The status automation TypeScript source references group requirement filtering concepts ([ConnectionStatusAutomationBag TypeScript source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusAutomationBag.d.ts)). A Triumph Tech GitHub spotlight excerpt mentions a bug where group requirement for the selected placement group disappeared from the Connection Request Board modal; use release notes/GitHub issue details if troubleshooting older v17.x/v18 pre-alpha builds ([Triumph Tech GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-422025)).

### Communications

Connections commonly uses communications for follow-up. Check:

- Person communication preferences.
- SMS opt-in/opt-out.
- Email deliverability.
- Communication templates.
- Connector permissions.
- Whether a communication was sent, queued, failed, or only logged as an activity.

Release notes mention SMS compliance changes in v18.1 CRM, which can matter if connection workflows send SMS through system phone numbers ([release notes](https://www.rockrms.com/releasenotes)).

### Security

Security can affect:

- Page access.
- Block access.
- Connection Type edit/view.
- Opportunity edit/view.
- Request detail access.
- Connector groups.
- Attribute visibility/editability.
- REST endpoints.
- Workflow actions.
- Reports and data views.

The REST v2 connector group controller secures read and write with distinct authorization actions ([ConnectionOpportunityConnectorGroupsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)). Do not assume a user who can see a request can edit connector group configuration.

### Reporting

Reporting uses Connection Request filters by Connection Type and Opportunity. Source-code provides official reporting filter components:

- `ConnectionTypeFilter` applies to `Rock.Model.ConnectionRequest` and lists connection types ordered by configured order/name ([ConnectionTypeFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs)).
- `ConnectionOpportunityFilter` applies to `Rock.Model.ConnectionRequest` and builds opportunity options from active opportunities within each type ([ConnectionOpportunityFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs)).

When reports disagree with the board, compare:

- Filter state/status.
- Campus.
- Active-only opportunity behavior.
- Date basis.
- Security trimming.
- Whether connected/completed requests are included.
- Whether future follow-up is included.
- Whether a report uses request created date, modified date, activity date, or completion date.

## 13. Administration And Operational Guardrails

### Minimum Viable Governance

Every Connection Type should have an owner. Every Opportunity should have an owner or ministry team. Every open request should have a connector or a documented unassigned triage queue.

Suggested governance fields:

- Owner ministry/team.
- Backup owner.
- SLA for first contact.
- Idle threshold.
- Completion definition.
- Transfer rules.
- Future follow-up policy.
- Reporting cadence.
- Data retention/cleanup expectations.
- Security group responsible for administration.

### Configuration Review Checklist

For each Connection Type:

- Name and description are clear.
- Enabled views match staff workflow.
- Statuses are active, ordered, and meaningful.
- Exactly one intended default status exists.
- Completion/inactivation behavior is intentional.
- Due offsets and due-soon offsets are documented.
- Future follow-up is enabled only if staff use it.
- Type attributes are still needed and secured.
- Request detail behavior matches Rock version.
- Idle threshold is appropriate.

For each Opportunity:

- Active state is correct.
- Public name/details are safe for public display if used externally.
- Campus routing is correct.
- Connector groups are populated.
- Default connector is valid.
- Workflows are ordered and filtered intentionally.
- Request attributes appear on signup/detail as expected.
- Security is scoped to ministry owners.
- Placement/group settings are still valid.

For boards/lists:

- Default state/status filters are intentional.
- Campus filter behavior is documented.
- Connector preference defaults are understood.
- Bulk update is restricted to trained staff.
- Version-specific known bugs are reviewed.

### Operational Metrics

Track:

- New requests by week/month.
- Completed requests by week/month.
- Open requests by type/opportunity.
- Open requests by connector.
- Requests idle past threshold.
- Requests due soon.
- Requests overdue.
- Future follow-up counts by window.
- Status distribution.
- Requests with no connector.
- Requests with no activity after creation.
- Requests transferred more than once.
- Requests reopened or repeatedly paused.

Source-code models support several of these ideas: new/completed request counts per day, status distribution, and upcoming follow-up windows ([ConnectionRequestCountsPerDayBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs), [ConnectionRequestStatusDistribution source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestStatusDistribution.cs), [ConnectionRequestUpcomingFollowUpWindow source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestUpcomingFollowUpWindow.cs)).

## 14. Developer, API, Lava, And Source-Code Landmarks

### Mobile Blocks

The mobile Connection block family is documented under Mobile Docs > Essentials > Blocks > Connection ([Connection mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection)).

Key pages:

- Add Connection Request: creates a request and supports block configuration/page parameters ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request)).
- Connection Opportunity List: displays opportunities for a single Connection Type and supports templates/detail page behavior ([Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list)).
- Connection Request List: displays unfinished requests for a single opportunity and excludes Connected-state requests ([Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

### Query/Page Parameter Landmarks

From the mobile docs:

- Opportunity list needs Connection Type context, commonly by GUID.
- Request list looks for an opportunity context, including `connectionOpportunityGuid` behavior.
- Add request can use `RequesterId`, `ConnectionTypeId`, and `ConnectionOpportunityId` page parameters to preselect or lock choices ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request), [Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

When implementing mobile navigation, verify whether a parameter expects an integer id, id key, or GUID. The source pack excerpts include mixed parameter naming across docs; inspect the live block settings and current docs for the target Rock/mobile version.

### Lava

For public opportunity listings, prefer a supported Connection Opportunity block when possible. If Lava is required:

- Use block-provided merge fields rather than direct SQL when possible.
- Filter to active/public opportunities.
- Respect security and campus.
- Use public-facing names/details.
- Avoid exposing internal connector or request data.
- Link to a supported signup/detail page with the expected parameter.
- Include empty-state handling.

Community Q&A shows a Lava card pattern using an Opportunity collection from the Connection Opportunity Search block, public attribute filtering, summary display, and optional `PhotoUrl` use ([community Q&A](https://community.rockrms.com/ask/developing/2645)). Adapt carefully.

### REST/API

The source pack includes a generated REST v2 controller for `ConnectionOpportunityConnectorGroup` under `api/v2/models/connectionopportunityconnectorgroups`, with authenticated read and write endpoints secured by read/write authorization actions ([ConnectionOpportunityConnectorGroupsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)).

API rules for agents:

- Prefer read operations unless explicitly asked to write.
- Use GUID/IdKey where supported to avoid environment-specific integer ids.
- Confirm security context.
- Confirm model version.
- For writes, capture before/after state and rollback plan.
- Do not create connector group records without confirming group GUIDs and opportunity GUIDs.

### Source-Code Landmarks

Useful files from the source pack:

- Connection Type summary view model: enabled views and labels  
  [ConnectionTypeSummaryBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs)

- New/completed request counts per day  
  [ConnectionRequestCountsPerDayBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs)

- Status distribution DTO and query options  
  [ConnectionRequestStatusDistribution.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestStatusDistribution.cs)  
  [ConnectionRequestStatusDistributionQueryOptions.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/Options/ConnectionRequestStatusDistributionQueryOptions.cs)

- Upcoming follow-up windows and query options  
  [ConnectionRequestUpcomingFollowUpWindow.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestUpcomingFollowUpWindow.cs)  
  [ConnectionRequestUpcomingFollowUpWindowQueryOptions.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/Options/ConnectionRequestUpcomingFollowUpWindowQueryOptions.cs)

- Connection status view models  
  [ConnectionStatusBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)  
  [ConnectionStatusAutomationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusAutomationBag.cs)  
  [ConnectionStatusViewModel.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionRequest/ConnectionStatusViewModel.cs)

- Reporting filters  
  [ConnectionTypeFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs)  
  [ConnectionOpportunityFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs)

- Connector group API  
  [ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)

## 15. Reporting, Analytics, And Model Map

### Model Map

Model Map identifies Connection Opportunity as an Engagement model ([Model Map](https://community.rockrms.com/ModelMap)). Use Model Map to orient entity categories, but use live schema/source code for exact field relationships.

### Built-In Reporting Filters

Rock includes Connection Request reporting filters by type and opportunity. The source-code filters apply to `Rock.Model.ConnectionRequest`, not directly to Person, Group, or Opportunity ([ConnectionTypeFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs), [ConnectionOpportunityFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs)).

This means a data view/report needs to be based on Connection Request if you want native type/opportunity filters. If the report is person-based, you may need a related entity filter, custom SQL, or a persisted data view.

### Analytics Dimensions

Useful dimensions:

- Connection Type
- Connection Opportunity
- Request State
- Request Status
- Campus
- Connector
- Created date
- Completion date
- Last activity date
- Follow-up date
- Source channel
- Person age classification
- Placement group
- Request attributes
- Opportunity attributes
- Workflow outcome

### Analytics Measures

Useful measures:

- Count of open requests.
- Count of connected/completed requests.
- Count of inactive requests.
- Count created per period.
- Count completed per period.
- Median time to first activity.
- Median time to completion.
- Idle request count.
- Requests due soon.
- Requests overdue.
- Upcoming future follow-up count.
- Connector assignment load.
- No-activity-after-creation count.
- Transfer count.
- Conversion rate by opportunity.

Source-code `ConnectionRequestCountsPerDayBag` explicitly models new and completed counts by day ([ConnectionRequestCountsPerDayBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs)). `ConnectionRequestStatusDistribution` models status count segments with color and status name ([ConnectionRequestStatusDistribution source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestStatusDistribution.cs)). These are good clues for the metrics Rock itself considers useful.

## 16. Version And Release Caveats

### Rock v10

The Engagement documentation change log says v10 added existing Connections chapters, request signup attribute entry capability, Connection Campaigns, and related updates ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). If supporting older instances, verify whether request signup attributes and campaigns exist and behave the same.

### Rock v12

The docs note that older versions used a Connection Request Detail Page setting, but as of Rock v12, the Connection Request Board no longer needed that separate page for viewing request details ([Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39)). If an older instance opens details on a separate page, inspect that setting.

### Mobile v3.0 / Core v13.3

The mobile Connection Opportunity List and Connection Request List docs identify mobile/core version availability around M v3.0 and C v13.3 ([Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list), [Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

### Mobile v5.0 / Core v16.1

The Add Connection Request mobile docs identify availability around M v5.0 and C v16.1 ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request)).

### Rock v17.2

Release notes fixed inherited request attributes in the Connection Opportunity Signup block so type-level request attributes appear correctly with opportunity-level attributes ([release notes](https://www.rockrms.com/releasenotes)).

### Rock v18.1

Release notes describe major Connection improvements:

- Connection Request Board campus filtering.
- Connector preferences.
- Workflow configuration.
- Default Connection State and Status block filters.
- Required State filter.
- Connection Opportunity workflow drag-and-drop ordering.
- Workflow applicability filters by age classification and include/exclude data views.
- Serving Connection record source behavior for new individuals added through signup in CRM notes ([release notes](https://www.rockrms.com/releasenotes)).

### Rock v18.3

Release notes list several Connection fixes:

- Date sorting consistency in Connection Request List.
- Activity Status values ordering in detail edit view.
- Activity list showing nickname instead of first name.
- Detail edit view status display when Show Connect Button is disabled ([release notes](https://www.rockrms.com/releasenotes)).

### Rock v19.1 / Current Release Notes

The hydrated release notes page shows Rock v19.1 beta and v18.3 alpha headings as of the retrieval date, but the provided Connection-specific excerpt focuses on v18.3 and v18.1. For v19.1 Connection behavior, inspect the live release notes directly before asserting changes ([release notes](https://www.rockrms.com/releasenotes)).

## 17. Implementation Playbooks

### Playbook: Create A New Serving Pipeline

1. Define the Connection Type: "Serving" or equivalent.
2. Define statuses: New, Contacted, Interviewing, Background Check, Training, Placed, Not A Fit, Future Follow-Up. Use local language.
3. Decide which statuses inactivate, complete, require notes, or pause follow-up.
4. Define opportunities for each ministry team.
5. Add connector groups per opportunity.
6. Add default connectors only where ownership is stable.
7. Add request attributes: preferred campus, availability, experience, role interest, restrictions.
8. Add opportunity workflows: notify ministry lead, create background check workflow, add group placement, send training info.
9. Configure board/list filters.
10. Configure self-service signup.
11. Test with a known person.
12. Verify request appears on board and list.
13. Verify connector assignment.
14. Verify inherited request attributes appear in signup/detail, especially on v17.2 or earlier.
15. Verify reporting filters by type/opportunity.

### Playbook: Public Opportunity Cards

1. Use a built-in Connection Opportunity block if possible.
2. Scope to one Connection Type.
3. Show only active/public opportunities.
4. Use public-safe name, summary, and image.
5. Link to signup with opportunity context.
6. Confirm mobile/desktop display.
7. Confirm inactive opportunities disappear.
8. Confirm security does not reveal internal opportunities.
9. Confirm request is created with correct type/opportunity/status.
10. Confirm post-save action.

Mobile docs describe the Opportunity List block and its need for Connection Type context ([Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list)). Community Q&A provides a non-authoritative Lava card example ([community Q&A](https://community.rockrms.com/ask/developing/2645)).

### Playbook: Add Status Automation

1. Identify the status that should trigger automation.
2. Define the desired outcome.
3. Decide whether automation is immediate, scheduled, workflow-based, or filter-based.
4. Add or update status automation on the Connection Type.
5. If using data views, test the person manually against the data view.
6. If using group requirements, test requirement state.
7. Confirm workflow order and filters on opportunities if relevant.
8. Test on a non-production request.
9. Review request history/activity.
10. Add report/dashboard coverage for failures.

RockU includes a status automation training page, and source-code exposes status automation bags in Connection Type Detail ([RockU status automation](https://community.rockrms.com/rocku/engagement/connection-request-status-automation), [ConnectionStatusAutomationBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusAutomationBag.cs)).

### Playbook: Build A Manager Dashboard

Include:

- Open requests by Connection Type/Opportunity.
- Open requests by status.
- Idle requests.
- Due soon/overdue requests.
- Future follow-up windows.
- Requests with no connector.
- New/completed trend.
- Connector workload.
- Campus distribution.

Base reports on `ConnectionRequest` when using native type/opportunity filters ([ConnectionTypeFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs), [ConnectionOpportunityFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs)).

## 18. Troubleshooting Decision Tree

### Request Missing From Board

1. Confirm the request exists.
2. Confirm the request's Connection Type and Opportunity.
3. Confirm the opportunity is active.
4. Confirm board is scoped to the same type/opportunity.
5. Check board State filter.
6. Check board Status filter.
7. Check campus filter.
8. Check connector preference filter.
9. Check user security.
10. Check Rock version for board bugs/fixes.
11. Compare against list view and direct query.

Relevant v18.1 release notes: default state/status filters, campus filtering, connector preferences, and required state filter ([release notes](https://www.rockrms.com/releasenotes)).

### Request Missing From Mobile Request List

1. Confirm the block has the correct opportunity context.
2. Confirm query/page parameter name and value.
3. Confirm the request is not in Connected state, because the mobile Request List block excludes Connected-state requests.
4. Confirm mobile app version supports the block.
5. Confirm user security.
6. Confirm API/network errors.

Source: mobile Request List behavior ([Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

### Opportunity Missing From Selector Or Report

1. Confirm opportunity is active.
2. Confirm opportunity belongs to the expected Connection Type.
3. Confirm report filter is based on Connection Request if using native filters.
4. Confirm security.
5. Confirm display order/name.
6. Confirm cache refresh if recently changed.

Source-code reports active opportunities by type for the opportunity filter ([ConnectionOpportunityFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs)).

### Request Did Not Auto-Assign

1. Check connector groups on the opportunity.
2. Check default connector.
3. Check connector group membership.
4. Check campus compatibility.
5. Check workflow/automation.
6. Check person/group security.
7. Check inactive group members.
8. Check whether assignment is manual by design.

Source: connector group/default connector source-code landmarks ([DefaultConnectorOptionsRequestBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionOpportunityDetail/DefaultConnectorOptionsRequestBag.cs), [ConnectionOpportunityConnectorGroupsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs)).

### Status Change Did Something Unexpected

1. Inspect the selected status configuration.
2. Check auto-inactivate.
3. Check auto future follow-up pause.
4. Check note-required-on-completion.
5. Check due offsets.
6. Check status automations.
7. Check workflow history.
8. Check request history.

Source: status fields in view model ([ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)).

### Signup Missing Attributes

1. Determine whether missing attributes are type-level or opportunity-level.
2. Verify attribute security.
3. Verify block settings.
4. Verify Rock version.
5. Check v17.2 fix for inherited request attributes.
6. Test in staff and public contexts.

Source: v17.2 release note ([release notes](https://www.rockrms.com/releasenotes)).

### List Sorting Looks Wrong

1. Confirm sort field and direction.
2. Confirm date basis.
3. Compare board/list/direct query.
4. Check v18.3 fix for date sorting.
5. Verify timezone/date display.

Source: v18.3 release note ([release notes](https://www.rockrms.com/releasenotes)).

## 19. Agent Task Recipes

### Recipe: Audit One Connection Type

Return:

- Type name/id/guid.
- Active state.
- Enabled views.
- Statuses with order/default/active/auto behavior.
- Opportunities with active state, order, campus, connector groups, default connector.
- Open request counts by status/state.
- Idle request count.
- Future follow-up count.
- Requests missing connector.
- Workflows and automation summary.
- Security concerns.
- Version caveats.

Use official/source concepts: enabled views from `ConnectionTypeSummaryBag`, status fields from `ConnectionStatusBag`, and reporting filters by Connection Request ([ConnectionTypeSummaryBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs), [ConnectionStatusBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs), [ConnectionTypeFilter source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs)).

### Recipe: Explain Why A Request Is Hidden

Return:

- Request id/guid/idkey.
- Person.
- Type/opportunity.
- Current state/status.
- Campus.
- Connector.
- Board/list filters checked.
- Security checked.
- Whether request is connected/completed.
- Whether mobile block excludes it.
- Final reason.

Cite mobile connected-state exclusion if relevant ([Connection Request List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)).

### Recipe: Validate Signup Flow

Return:

- Entry page/block.
- Allowed Connection Types.
- Locked Connection Type/Opportunity parameters.
- Requester identity behavior.
- Attributes shown.
- Post-save/post-cancel actions.
- Created request fields.
- New person record source behavior.
- Version caveats.

Cite Add Request mobile docs for parameter behavior and v17.2/v18.1 release notes for attributes/record source if applicable ([Add Connection Request mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request), [release notes](https://www.rockrms.com/releasenotes)).

### Recipe: Build Opportunity Cards

Return:

- Connection Type source.
- Opportunity filter criteria.
- Public/private field mapping.
- Image field.
- Signup/detail link.
- Empty state.
- Security review.
- Test request result.

Use the official Opportunity List block where possible; only use community Lava patterns as examples ([Connection Opportunity List mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list), [community Q&A](https://community.rockrms.com/ask/developing/2645)).

### Recipe: Investigate Connector Workload

Return:

- Connector group membership by opportunity.
- Open request count by connector.
- Requests with no connector.
- Idle requests by connector.
- Future follow-up by connector.
- Availability/leave process.
- Suggested assignment correction.

Community recipe provides one real-world pattern for connector availability reporting, but validate before adopting ([connector report recipe](https://community.rockrms.com/recipes/446)).
























<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `37`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | implementation_pattern | Before launching preregistration broadly, teams should test the full path from public form through family record creation, check-in eligibility, and staff follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | implementation_pattern | New-family preregistration should be connected to a clear follow-up workflow or connection process so the data captured before arrival leads to ministry action. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | operational_guidance | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Family preregistration is useful when it reduces first-visit friction and improves the quality of people, family, and child data before check-in. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | operational_guidance | A public preregistration page should explain the value to families and avoid creating duplicate or partial records that staff later need to clean manually. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | implementation_pattern | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| community-reviewed | operational_guidance | Long-form training or strategy material should be broken into actionable sections with a way to measure whether leaders and teams are adopting the recommendations. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |
| community-reviewed | operational_guidance | Campus dashboards should help leaders compare current year-to-date values against both goals and prior-year context, while leaving deeper campus-specific measures available without crowding the organization-wide dashboard. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Communication teams often feel siloed, so content and campaign strategy should be tied to ministry ownership, shared goals, and a visible next-step path in Rock. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |
| community-reviewed | operational_guidance | A mature reporting suite can separate executive dashboards, campus or ministry dashboards, and functional operational dashboards so each audience sees the level of detail needed for its decisions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Functional dashboards such as connection-request views may justify live database connections when leaders need up-to-date queues, while slower-changing attendance or giving dashboards can usually use scheduled refreshes. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| More |  | 25 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->











































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `8`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) | approved_for_public_distillation | 4 | media-insight:1f90493258b0b21b |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) | approved_for_public_distillation | 6 | media-insight:392aedce4cf2d99c |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/OLmW03olAp) | approved_for_public_distillation | 3 | media-insight:4b01eb5056bab0e5 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) | approved_for_public_distillation | 3 | media-insight:7e8c9d47198de3f9 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) | approved_for_public_distillation | 3 | media-insight:a0960ff639b6ffaf |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) | approved_for_public_distillation | 3 | media-insight:a8361b8714eb62ff |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) | approved_for_public_distillation | 3 | media-insight:e81a9f6b5e5e2f8a |
| [Rock's Future Anchored in Vision \| Ep 202 Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) | approved_for_public_distillation | 4 | media-insight:00a8a57d7db012dc |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->
























## 20. Source Map And Dependency Notes

### Official Documentation

- [Engagement documentation](https://community.rockrms.com/documentation/bookcontent/39): primary official source for Connections concepts, request work, state/status, activities, campus, list/detail/bulk update, self-service, staff entry, type settings, and version notes.
- [Release notes](https://www.rockrms.com/releasenotes): version-specific behavior, especially v17.2, v18.1, and v18.3 Connection changes.

### RockU Training

- [Connections Overview](https://community.rockrms.com/rocku/engagement/overview)
- [Connection Types](https://community.rockrms.com/rocku/engagement/connection-types)
- [Connection Opportunities](https://community.rockrms.com/rocku/engagement/connection-opportunities)
- [Connection Request Status Automation](https://community.rockrms.com/rocku/engagement/connection-request-status-automation)
- [Connections List](https://community.rockrms.com/rocku/engagement/connections-list-1)
- [Connections Board](https://community.rockrms.com/rocku/engagement/connections-board)
- [New RockU Videos](https://community.rockrms.com/rocku/new)

The hydrated RockU excerpts mostly provide metadata, durations, and page pointers. Review the live videos for detailed procedural claims.

### Developer And Mobile Docs

- [Connection mobile docs](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection)
- [Add Connection Request](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request)
- [Connection Opportunity List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list)
- [Connection Request List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list)

Use these for mobile block behavior, configuration, templates, and navigation parameters.

### Model Map And Source Code

- [Model Map](https://community.rockrms.com/ModelMap): confirms Connection Opportunity as an Engagement model.
- [Rock repository](https://github.com/SparkDevNetwork/Rock): source repository.
- [ConnectionTypeSummaryBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs): enabled views and type summary.
- [ConnectionRequestCountsPerDayBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs): new/completed trend data.
- [ConnectionRequestStatusDistribution](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestStatusDistribution.cs): status distribution metrics.
- [ConnectionRequestUpcomingFollowUpWindow](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Connection/ConnectionType/DTO/ConnectionRequestUpcomingFollowUpWindow.cs): follow-up window metrics.
- [ConnectionStatusBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs): status configuration fields.
- [ConnectionStatusAutomationBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusAutomationBag.cs): status automation model.
- [ConnectionTypeFilter](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs): reporting filter by Connection Type.
- [ConnectionOpportunityFilter](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs): reporting filter by Connection Opportunity.
- [ConnectionOpportunityConnectorGroupsController](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs): REST v2 connector group endpoint.

### Community Examples

- [Connection Type Q&A](https://community.rockrms.com/ask/developing/2645): example of using Connection Opportunity Search and Lava for public cards.
- [Connector Report With Unavailability Workflow recipe](https://community.rockrms.com/recipes/446): example of workload/availability reporting and workflow, not core-reviewed.

### Live Verification Required

Before taking operational action, inspect the live Rock instance for:

- Actual status names and order.
- Actual state values and filters.
- Board/list block settings.
- Enabled views per Connection Type.
- Opportunity active state and connector groups.
- Default connector behavior.
- Campus behavior.
- Workflow order and filters.
- Attribute inheritance and security.
- Person duplicate/record-source behavior.
- Version-specific release behavior.
- Security permissions for the acting user.
