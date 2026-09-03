---
id: authored-connections
title: Connections
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "eced6c635bda99cbcc9504f0e50c16c6d0c75a4d9c5874860cc0cf579bdda69a"
---

# Connections

## Agent Summary

Rock Connections is an operational pipeline for helping a person move through a relational process without losing ownership, history, or the next action. A connection type defines the overall process; opportunities represent destinations within that process; requests represent individual people moving through it. Workflows extend the pipeline, but the Connections structure remains its operational backbone. [Official v19 overview](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0)

When handling a request, distinguish these fields:

- **State** controls whether the request is active, inactive, deferred for future follow-up, or completed.
- **Status** represents the configurable stage within a connection type.
- **Activities** record individual contacts and other events; a request can have many activities.
- **Connector** identifies the person responsible for the request.
- **Opportunity** identifies the current destination.
- **Placement group** identifies the group into which the requester may be placed upon completion.

These concepts are related but not interchangeable. Changing a status does not necessarily complete, defer, transfer, or place a request. [Official v19 overview](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0)

For operational triage, start with scope: installed Rock version, connection type, opportunity, campus, state, status, connector, due-date calculation mode, enabled view, and the current user's permissions. In v19, those settings affect which requests, controls, metrics, and actions appear. [Navigate the Connections Tools](https://community.rockrms.com/documentation/engagement/connections/connection-requests/navigate-the-connections-tools?Version=v19.0), [official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=50s)

Do not treat generated AI summaries, a dashboard count, or a successful workflow launch message as proof that a person was contacted or placed. Verify the request's current state, status, connector, activities, placement data, and any required downstream result. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0)

## Scope And Boundaries

This guide covers connection types, opportunities, requests, states, statuses, list and board operation, assignment, follow-up, transfer, placement, workflows, campaigns, bulk actions, and pipeline reporting. It emphasizes the v19 documented experience because most supplied official documentation is scoped to v19.

Related concepts remain in their owning guides:

- Person and family matching belong to **People And Families**.
- Workflow construction and persistence belong to **Workflows**.
- Placement-group membership and requirements belong to **Groups**.
- SMS and email delivery behavior belongs to **Communications**.
- authorization design belongs to **Security And Permissions**.
- Data Views and external dashboards belong to **Reporting**.

Connections may invoke those systems, but a connection request is not itself proof that a person record was matched correctly, a workflow completed, a communication was delivered, a group membership was created, or an external report license was granted.

## Mental Model

| Layer | Operational meaning | Typical configuration |
| --- | --- | --- |
| Connection type | The overall organizational process | Views, states and statuses, activities, sources, request security, due-date rules, workflows |
| Connection opportunity | A specific destination inside that process | Public description, connector groups, default connectors, placement groups, opportunity workflows, transfer options |
| Connection request | One person's movement through an opportunity | Campus, connector, state, status, due date, comments, attributes, activities, placement |
| Activity | A recorded event within the relationship | Activity type, note, optional custom attributes |
| Workflow | Automation attached to a request or activity event | Trigger, workflow type, filters, workflow actions |
| Campaign | A managed source list that creates requests in batches | Data View, opportunity, assignment policy, family limit, recurrence, opt-out behavior |

This hierarchy is documented in the official Connections overview and configuration guides. A connection type can contain multiple opportunities, and each request belongs to an opportunity. Statuses and activity types are configured at the type level, while connector and placement configuration can be specific to an opportunity. [Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0), [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0)

A useful agent rule is to inspect from the outside inward:

1. Confirm the connection type and its configuration.
2. Confirm the opportunity and campus context.
3. Inspect the request's current state, status, connector, due date, and placement.
4. Review activities and workflow results.
5. Verify the downstream person, group, communication, or reporting outcome separately.

## Opportunities

A connection opportunity is a destination within a connection type. Its configuration can include an active flag, public-facing name or imagery, summary and details, opportunity-attribute values, applicable request attributes, connector groups, default connectors, placement-group options, opportunity-specific workflows, and transfer controls. [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0)

Treat the opportunity as an operational boundary, not merely a label. Before activating one, inspect:

- Whether its summary and details describe the real next step.
- Whether it should be visible through self-service discovery.
- Which campuses it serves.
- Which connector groups are responsible.
- Whether each campus has an appropriate default connector.
- Which placement groups, roles, and member statuses are valid.
- Whether completion requires a placement group.
- Which workflows apply specifically to this opportunity.
- Whether transfer should expose campus and status selection.

The official opportunity configuration supports selecting specific placement groups or using all groups of a configured group type. When multiple placement roles or group-member statuses are available, the request interface can expose those choices during placement. [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0)

Do not infer public availability from an opportunity's existence. Self-service behavior depends on the public blocks, their filters and settings, opportunity configuration, attributes, campus context, and permissions. The stock v19 documentation describes a Connection Opportunity Search flow, while a community Q&A demonstrates a customized card layout using that block; the latter is a community implementation example, not a core guarantee. [Enter New Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connection-requests/enter-new-connection-requests?Version=v19.0), [community Q&A example](https://community.rockrms.com/ask/developing/2645)

A reviewed community design pattern recommends using badges, person attributes, request attributes, requirements, or list fields for checklist-like signals before adding more statuses. Reserve statuses for genuine lifecycle stages that affect timing, ownership, or the next action. This is community guidance requiring local validation, not an official Rock rule.

## Requests And Statuses

Rock documents three core request-entry paths in v19:

1. A visitor submits through a self-service opportunity experience.
2. Staff create a request internally under `People > Connections`.
3. A workflow uses the connection-request creation action.

Request attributes can be configured as entity attributes. Public exposure can be controlled through the attribute's public flag and through included or excluded attribute categories in the signup block. [Enter New Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connection-requests/enter-new-connection-requests?Version=v19.0)

### State

The documented request states are:

- **Active:** currently being worked.
- **Inactive:** no longer in the active workload without representing successful completion.
- **Future Follow-up:** deferred until a specified date.
- **Completed:** finished through the connection process.

Future Follow-up temporarily removes a request from the connector's active workload. The official overview says the Connection Request Workflow Triggers job changes it back to Active based on the follow-up date, so a missing return-to-active transition requires job and date inspection rather than merely editing the visible list filter. [Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0)

### Status

Statuses are configurable for each connection type. They should communicate where a request is within that type's process. Rock supports manual status changes and status-automation configuration. [Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0)

When sequential status mode is enabled, requests advance only through adjacent configured statuses. Board dragging and bulk status updates cannot skip intermediate statuses, and completion becomes available after the final status. Treat an inability to jump ahead as expected behavior until sequential mode and the configured order have been inspected. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0), [official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=895s)

The supplied immutable v19-era source snapshot also exposes status configuration fields for status order, completion-note requirements, automatic inactivation, future-follow-up pause days, due-date offsets, due-soon offsets, and automations. This is implementation evidence from a specific commit, not proof that any installation has configured those values. [ConnectionStatusBag at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs)

### Due Dates

The approved official v19 evidence says due and due-soon dates can be configured at the connection type, opportunity, or status level. Inspect the selected due-date calculation mode and applicable offsets before interpreting a request as late or using overdue counts for staff accountability. [Official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=82s)

A due-date column may also be hidden by list settings. First distinguish “no calculated due date” from “the due-date field is not displayed.” [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0)

### Activities

Activities record touchpoints such as calls, messages, meetings, or other configured events. A request has one current state and one current status but can have many activities. Activity types can have their own entity attributes. [Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0), [Configure Connection Requests](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-requests?Version=v19.0)

Depending on connection-type settings, the request view may also show activities from another request for the same person. In the documented v19 presentation, styling distinguishes activities attached to the current request from activities surfaced from another request in the same type. Do not count every visible activity as belonging to the open request without checking its association. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0)

## Boards And Lists

In v19, the Connections navigation can expose list, board, grid, and operational snapshot views. Enabled views are configured on the connection type, so absence of a view does not by itself indicate a broken installation. [Navigate the Connections Tools](https://community.rockrms.com/documentation/engagement/connections/connection-requests/navigate-the-connections-tools?Version=v19.0), [official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=50s)

### List view

The v19 list supports:

- My Requests or All Requests.
- Opportunity and campus filtering.
- Quick search by requester name.
- Grouping, sorting, and column selection.
- Optional display of request source and due date.
- Selection of multiple requests for bulk actions.

The exact fields and grouping choices depend on local block settings and configured request sources. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0), [official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=247s)

Selected requests can be assigned, moved to another status, completed, changed by state, sent to a manual workflow, given an activity, or used to initiate SMS or email. Availability and success still depend on opportunity applicability, workflow trigger configuration, templates, snippets, valid phone eligibility, and user permissions. [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0), [official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=466s)

Rock reports partial applicability when a bulk action cannot operate on every selected request—for example, when a workflow is available to only one of several selected opportunities. Read the result count and inspect exceptions; do not equate the action dialog closing with complete success. [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0)

The specialized bulk-update screen for a connection type performs updates one campus at a time and can change opportunity, status, state, connector, workflow, or activity settings. Distinguish that screen from the selection toolbar embedded in the v19 list. [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0)

### Board view

The board presents requests for a selected opportunity in status columns and allows status management from the board. Opening a card exposes request detail. In sequential mode, a card can move only to the next permitted status rather than skipping multiple columns. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0)

The board should represent the lifecycle, not every piece of information staff might want to see. A reviewed community pattern recommends using badges, attributes, requirements, or list columns for visibility signals before adding more lifecycle statuses. Validate that pattern against the installed board and the team's actual operating process.

### Grid and request detail

The official documentation identifies Grid as an available v19 view but the supplied excerpt does not describe its complete behavior. Do not infer feature parity with List or Board beyond what the installed block demonstrates.

Request detail can expose other active household requests, campus, connector, request age, actions, original comments, request source, attributes, transfer, activities, status, and completion controls. Which items appear depends on connection-type, opportunity, block, and security settings. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0)

## Assignment And Follow-Up

Connector groups are configured on opportunities. Their active members form the available connector pool, and an opportunity can define default connectors by campus. [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0)

Campus is operational, not decorative. Requests are associated with a campus, and connector groups or placement groups can be partitioned by campus. For campaign assignment, a connector in an all-campus group can be available broadly, while a connector in a campus-specific group is available only for matching requests. The campaign documentation ties that matching to the requester's primary campus. [Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0), [Intro to Campaign Connectors](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-campaign-connectors?Version=v19.0)

When request security is enabled, inspect security at the request, opportunity, and type levels. Rock also documents a special allowance for the assigned connector to view or edit their requests even without broader opportunity or type access. Enabling request-level security can have a noticeable performance impact at high request volume. [Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0)

Use Future Follow-up when the next action belongs on a known future date rather than leaving the request active and overdue. Verify both the follow-up date and the job responsible for returning eligible requests to Active. Workload metrics should distinguish active work from intentionally deferred work. [Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0)

The v19 Operational Snapshot reports active, unassigned, due-soon, and overdue counts, future follow-ups, status distribution, connector activity, and completion measures. Its Care Lapse marker indicates that a connector has overdue requests; the documentation notes that the marker can remain as a historical signal after those overdue items are completed. Use it as a coaching and capacity signal, not as proof of a connector's current queue without opening the underlying requests. [Operational Snapshot](https://community.rockrms.com/documentation/engagement/connections/connection-requests/operational-snapshot?Version=v19.0)

## Placement, Completion, And Transfer

An opportunity can constrain valid placement groups, group roles, and group-member statuses. A connection type can also require a placement group before completion, which prevents the Complete action from becoming available until placement is selected. [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0), [Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0)

Before marking a request complete:

1. Confirm the request is in the intended opportunity.
2. Confirm sequential status requirements, if enabled.
3. Verify any required placement group, role, and member status.
4. Review group requirements and other configured prerequisites.
5. Enter a completion note if the status requires one.
6. Complete the request.
7. Verify the resulting group placement rather than assuming it occurred because the request left the active list.

A request can be transferred when another opportunity is a better fit. Depending on opportunity configuration, transfer can change the destination opportunity, campus, status, connector, due date, and transfer note. Connector choices can include the destination's default connector, the current connector, another eligible connector, or no connector. [Configure Connection Requests](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-requests?Version=v19.0)

After transfer, verify the destination opportunity, campus, status, connector, due date, and transfer activity. Do not treat a transfer as completion or as proof that the destination team accepted ownership.

## Workflows And Status Automation

Connection workflows can be configured at the type level for all opportunities or at an individual opportunity. The official documentation includes triggers for events such as assignment, start, transfer, future follow-up, celebration, and manual execution. Trigger behavior matters: most connection workflow triggers pass the request, but the Activity Added trigger passes the new activity. [Connection Workflows](https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows?Version=v19.0)

Rock's documented connection workflow actions include:

- Create Connection Request.
- Transfer Connection Request.
- Set Connection Request Status.
- Set Connection Request State.
- Add Connection Request Activity.

Those actions depend on correctly typed workflow attributes or explicit fallback values. A Future Follow-up state action also needs the intended follow-up date. [Connection Workflows](https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows?Version=v19.0)

Manual workflows must be configured with a Manual trigger to appear as eligible bulk actions. Opportunity-specific restrictions can cause a bulk workflow to run for only a subset of selected requests. [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0)

A reviewed community automation pattern describes status automation as a source status, destination status, and Data View. It recommends making the Data View deterministic and retry-safe: include the expected current source status, avoid accidental one-time cutoff dates, and return only requests that should still move when evaluated again. After automation, validate destination counts, request states, and job history. This pattern requires confirmation against the installed version and configuration.

A second reviewed community pattern recommends measuring time in a status from status-change History records rather than `ConnectionRequest.ModifiedDateTime`, because unrelated edits may change the latter. That is not established here as a universal core reporting contract; verify the installed history format and query behavior before adopting it.

Rock v19.3 release notes fixed a case where a workflow could not be removed from a connection type or opportunity after being triggered from a request. If removal fails on an older v19 build, inspect the exact patch level before redesigning the workflow attachment. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

## Connection Campaigns

A connection campaign builds a managed list of people and creates requests for a selected opportunity. Campaigns can support one-time or recurring outreach. The campaign configuration defines the target Data View, opportunity, connector assignment behavior, family limits, recurrence, opt-out behavior, and whether requests are created all at once or as needed. [Intro to Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-connection-campaigns?Version=v19.0), [Set Up Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/set-up-connection-campaigns?Version=v19.0)

The campaign list and the active request queue are different stages:

1. The Data View identifies eligible people.
2. The campaign job populates or updates the campaign list.
3. Assignment rules create requests from that list.
4. Connectors work ordinary connection requests.
5. Recurrence and opt-out rules determine future eligibility.

“As Needed” creation keeps a person in the campaign list until a connector is available, so request age better reflects active connector handling rather than time waiting in the source list. “All at Once” creates requests when the job runs and can create a large unassigned queue. A daily assignment limit of zero or blank stops automatic request creation and assignment, leaving requests to be created on demand. [Set Up Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/set-up-connection-campaigns?Version=v19.0)

Campaign connectors must belong to the configured connector group. Campus-specific connector membership limits which requests they can receive. Per-connector overrides can use the documented group-member attributes `CampaignDailyLimit` and `CampaignScheduleDays`; verify those keys and types in the installed version before rollout. [Intro to Campaign Connectors](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-campaign-connectors?Version=v19.0)

When a connector requests more campaign work, Rock first assigns existing unassigned requests; only when none remain does it create requests from the campaign list. [Campaign Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/campaign-connection-requests?Version=v19.0)

The official sample recipes demonstrate recurring check-ins and large emergency calling lists. They illustrate choices such as family limits, previous-connector preference, recurring intervals, and on-demand batches. Treat their settings as examples to adapt, not universal defaults. [Sample Campaign Recipes](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/sample-campaign-recipes?Version=v19.0)

## Public Intake And Cross-System Handoffs

Self-service connection intake should be tested as a complete visitor and staff journey: public discovery, request creation, person matching, campus selection, assignment, staff visibility, follow-up, transfer or placement, and completion. A request appearing in Rock does not prove that the full operating path works.

For family preregistration, reviewed community guidance recommends explaining the value to families, avoiding duplicate or partial person records, and connecting captured data to a clear workflow or connection process. Before broad launch, test the full path through family creation, check-in eligibility, and staff follow-up. The supplied read-only review confirmed that relevant feature surfaces existed in one bounded environment but explicitly did not prove that a specific preregistration flow was configured correctly. [Reviewed community preregistration source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

A reviewed community recipe demonstrates transferring registrant context into native connection requests while preserving a source registration reference and copying reviewed attributes. It is a community implementation pattern, not official Rock behavior, and still requires local workflow, identity-matching, campus, permission, and end-to-end validation. [Registration-to-Connection Request community recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)

Rock v19 introduced built-in proof-of-work CAPTCHA with organization- and block-level controls. For any exposed connection or preregistration form, confirm whether CAPTCHA is visible, invisible, or disabled and test the actual form. Do not infer protection merely from the installed Rock version. [Official v19 feature discussion](https://www.youtube.com/watch?v=edanHiYSDIM&t=195s)

## Reporting, AI, And Governance

The Operational Snapshot provides current workload and trend views, while the connection navigation can compare new and completed request counts. The supplied immutable source snapshot models daily new and completed counts and supports campus- and opportunity-filtered status or follow-up queries. These source observations explain implementation surfaces but do not establish an installation's filters, metric definitions, or data quality. [Operational Snapshot](https://community.rockrms.com/documentation/engagement/connections/connection-requests/operational-snapshot?Version=v19.0), [daily-count model at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs)

Before interpreting pipeline performance:

- Confirm campus, type, opportunity, state, status, and date filters.
- Inspect the due-date calculation mode.
- Separate campaign-list waiting time from active-request age.
- Compare new requests with completions and available connector capacity.
- Open the underlying request population before acting on a summary count.
- Treat unassigned, due-soon, overdue, future-follow-up, and completed as distinct operational populations.

Rock v19 can generate connection-request AI summaries or insights when the connection type has a prompt and an AI provider is configured. The summary can be configured for automatic loading or manual activation. Treat generated text as assistance, not authoritative person data; verify important statements against request activities and other governed records. [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0), [official AI-summary demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s)

When embedding Power BI or a similar system, pair Rock page and block security with the external platform's licensing and authorization. A Rock authorization row does not grant an external BI license, and possession of an external license does not grant access to the Rock page. This is reviewed community operational guidance; the supplied bounded read-only review confirmed Rock page, block, and authorization surfaces but did not verify external licensing. [Reviewed community analytics source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)

## Version And Authority Caveats

Most official documentation cited here identifies v19.0 as its current documented version. Confirm the installed Rock version, patch level, block generation, plugin state, and local settings before applying the guide.

The redesigned v19 Connections experience is a substantial interface change. Approved official guidance recommends showing staff the interface and providing brief training before deployment. [Official rollout guidance](https://www.youtube.com/watch?v=edanHiYSDIM&t=91s)

Relevant release distinctions include:

- Rock v18.1 added Connection Request Board improvements involving campus filtering, connector preferences, default state and status filters, workflow ordering, and request filters for applicable workflows.
- Rock v19 introduced the redesigned Connections experience described throughout this guide.
- Rock v19.3 fixed several Connections defects, including opportunity-navigation permission leakage, missing placement groups under “Use all Groups of this Type,” activity permissions, default-connector presentation, email-composer defaults, signup redirect handling, and removal of previously triggered workflows.
- The supplied release page labels v20.0 as Alpha and describes upcoming Connection Request Entry and Connections Hub additions. Do not treat those alpha features as v19 behavior or as production-ready without verifying the installed build and current release status.

[Rock Core Release Notes](https://www.rockrms.com/releasenotes)

Official documentation and release notes outrank community recipes and reviewed implementation patterns. Immutable source excerpts can clarify what a particular commit models, but they do not prove runtime configuration. Community examples may be useful starting points but require security, performance, version, and live-behavior review.

## Troubleshooting Decision Tree

### A connector cannot see an expected request

1. Confirm the request exists and inspect its type, opportunity, campus, state, status, and assigned connector.
2. Check whether the connector is looking at My Requests, All Requests, My Types, or My Opportunities.
3. Clear or deliberately set campus, opportunity, state, and status filters.
4. Check security at the request, opportunity, and type levels.
5. If campaign-generated, confirm connector-group membership and campus compatibility.
6. Inspect the installed patch level if opportunity counts or navigation visibility disagree with permissions; v19.3 includes a related fix.
7. Stop when the request is visible under the intended identity and scope, or when a specific security/configuration mismatch has been isolated.

[Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0), [Navigate the Connections Tools](https://community.rockrms.com/documentation/engagement/connections/connection-requests/navigate-the-connections-tools?Version=v19.0), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### A list field, source, grouping option, or view is missing

1. Confirm Rock v19 and the exact block being used.
2. Inspect the connection type's enabled views.
3. Open List settings and inspect selected columns, grouping, and sorting.
4. Confirm request sources are configured if the source field is expected.
5. Verify opportunity and campus filters.
6. Compare behavior using an authorized administrator and the affected connector.
7. Stop when the missing element is explained by version, block settings, source configuration, or security.

[Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0), [official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=247s)

### A request cannot skip to a later status or cannot be completed

1. Inspect whether sequential status mode is enabled.
2. Verify configured status order and the request's current status.
3. Move through the next adjacent status if sequential mode is intentional.
4. Confirm the request has reached the final status before completion.
5. Inspect whether a placement group, group requirement, or completion note is required.
6. Verify the intended placement group, role, and member status.
7. Stop when the blocking lifecycle or placement requirement is identified; do not bypass it through an unrelated state change.

[Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0), [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0)

### Due-soon or overdue counts look wrong

1. Confirm the metric's campus, type, and opportunity scope.
2. Inspect the connection type's due-date calculation mode.
3. Check opportunity- and status-level due-date or due-soon offsets.
4. Confirm whether the request has a calculated due date.
5. Separate active requests from Future Follow-up, inactive, and completed requests.
6. Open a small sample of underlying requests and reproduce the expected calculation.
7. Stop when the discrepancy is explained or a version-specific defect is reproducible.

[Official v19 demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=82s), [Operational Snapshot](https://community.rockrms.com/documentation/engagement/connections/connection-requests/operational-snapshot?Version=v19.0)

### A future follow-up request did not return to the active queue

1. Confirm the request is in Future Follow-up state.
2. Inspect the stored follow-up date.
3. Confirm the date has passed in the installation's effective time context.
4. Inspect the Connection Request Workflow Triggers job's schedule and recent results.
5. Check whether another workflow or status rule changed the request after deferral.
6. Re-open the request without restrictive list filters.
7. Stop when the job, date, state, or filter condition explains the behavior.

[Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0), [Connection Workflows](https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows?Version=v19.0)

### A campaign creates no requests or assigns them to the wrong people

1. Confirm the campaign is active and points to the intended opportunity.
2. Validate the source Data View with a bounded sample.
3. Inspect family limits and opt-out-group membership.
4. Confirm whether creation is All at Once or As Needed.
5. Check the daily limit; zero or blank prevents automatic creation and assignment.
6. Inspect the campaign-processing job and its recent result.
7. Confirm connectors belong to the configured group and match campus rules.
8. Inspect per-connector daily-limit and schedule-day overrides.
9. Distinguish people waiting in the campaign list from active connection requests.
10. Stop when eligibility, job execution, assignment capacity, or connector membership explains the result.

[Set Up Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/set-up-connection-campaigns?Version=v19.0), [Intro to Campaign Connectors](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-campaign-connectors?Version=v19.0)

### A workflow did not launch or a bulk action affected only some requests

1. Identify whether the workflow is configured on the type or opportunity.
2. Verify the trigger matches the event; bulk launch requires a Manual trigger.
3. Confirm any status, age-classification, or Data View applicability filter.
4. For Activity Added, verify the workflow expects an activity rather than a request.
5. Read the bulk-action result count and inspect excluded requests.
6. Check workflow persistence and workflow history.
7. Inspect the Rock patch level for known workflow-related fixes.
8. Stop when applicability, trigger configuration, input entity, permissions, or execution history explains the outcome.

[Connection Workflows](https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows?Version=v19.0), [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### An AI summary is unavailable or unreliable

1. Confirm the installed version and that the feature exists in the active request block.
2. Inspect the connection type's AI-summary settings.
3. Confirm a prompt is configured.
4. Confirm an AI provider is configured and available.
5. Check whether generation is manual or automatic.
6. Verify the current user's access to the request and AI surface.
7. Compare generated claims with request activities and governed person data.
8. Stop if provider access, prompt configuration, or evidence quality is insufficient; do not copy unverified generated statements into authoritative person data.

[Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0), [official AI-summary demonstration](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s)

## Agent Task Recipes

### Recipe: Configure a new connection pipeline

**Outcome:** A bounded connection type and opportunity are ready for controlled staff testing.

1. Define the real lifecycle, responsible team, completion condition, and escalation path.
2. Create or select the connection type.
3. Configure only the statuses that represent genuine lifecycle stages.
4. Choose whether sequential status mode matches the process.
5. Configure states, activities, sources, due-date rules, enabled views, and request security.
6. Create the opportunity with public summary and details.
7. Configure campus scope, connector groups, default connectors, placement groups, roles, member statuses, transfer controls, and workflows.
8. Create test requests through each intended intake path.
9. Exercise assignment, status movement, activity logging, future follow-up, transfer, placement, and completion.
10. Train connectors on the enabled v19 views before broad rollout.

**Inspect:**

- Type, opportunity, campus, status order, due rules, security, connectors, placement, workflows, and enabled views.

**Do not assume:**

- That a default connector exists for every campus.
- That a public opportunity is discoverable.
- That completion creates the intended membership without verification.

**Stop when:**

- The controlled test path passes and staff understand the interface, or a specific configuration dependency remains unresolved.

[Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0), [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0)

### Recipe: Triage an unassigned or overdue queue

**Outcome:** Every selected request has a verified owner or an explicit disposition.

1. Open the intended connection type and campus.
2. Filter to Active and Unassigned or Overdue requests.
3. Confirm due-date rules before prioritizing by lateness.
4. Group or sort by opportunity, campus, due date, or status.
5. Review connector capacity and eligibility.
6. Assign bounded batches to appropriate connectors.
7. Use Future Follow-up only when a real future date is known.
8. Transfer poor-fit requests instead of leaving them stalled.
9. Read bulk-action result counts and inspect exceptions.
10. Reopen the filtered queue and verify the remaining population.

**Do not assume:**

- That every red metric represents the same urgency.
- That assignment means contact occurred.
- That an empty visible list means the scoped queue is empty.

[Operational Snapshot](https://community.rockrms.com/documentation/engagement/connections/connection-requests/operational-snapshot?Version=v19.0), [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0)

### Recipe: Transfer and complete a request safely

**Outcome:** The request reaches the correct destination with ownership and placement preserved.

1. Review current comments, attributes, activities, campus, connector, and due date.
2. Confirm transfer is preferable to completing or inactivating the request.
3. Search for the best destination opportunity.
4. Choose the destination campus and status when those controls are enabled.
5. Select the destination's default connector, current connector, another eligible connector, or no connector deliberately.
6. Set the destination due date and add a transfer note.
7. Verify the destination request details and activity history.
8. When ready for completion, verify final status, placement group, role, member status, requirements, and required completion note.
9. Complete the request.
10. Verify the resulting placement and inactive/completed state.

[Configure Connection Requests](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-requests?Version=v19.0), [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0)

### Recipe: Launch a connection campaign

**Outcome:** An eligible audience enters a controlled, assignable follow-up queue.

1. Create or select the destination connection type and opportunity.
2. Configure the connector group and campus rules.
3. Build and validate the audience Data View.
4. Configure family limits and an opt-out group.
5. Choose All at Once or As Needed based on workload and request-age semantics.
6. Configure daily assignment limits, recurrence, and previous-connector preference where appropriate.
7. Confirm connector membership and any per-connector overrides.
8. Run a small controlled campaign cycle.
9. Compare eligible people, campaign-list entries, created requests, assignments, and exclusions.
10. Verify connector visibility and completion handling before increasing scale.

**Stop when:**

- Counts reconcile through the controlled sample, or the source, job, assignment, or campus rule causing a mismatch is identified.

[Set Up Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/set-up-connection-campaigns?Version=v19.0), [Intro to Campaign Connectors](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-campaign-connectors?Version=v19.0)

### Recipe: Connect preregistration to staff follow-up

**Outcome:** A preregistered family reaches a verified staff-owned next step without avoidable duplicate records.

1. Explain the practical value of preregistration on the public page.
2. Collect only the information required for the arrival and follow-up process.
3. Test person and family matching with representative scenarios.
4. Verify check-in eligibility and campus handling.
5. Create the intended workflow or connection request using reviewed mappings.
6. Preserve only an appropriate source reference and approved attributes.
7. Verify the request's opportunity, status, campus, comments, and assignment.
8. Complete a staff follow-up test.
9. Inspect for duplicate or partial people and family records.
10. Repeat the full path before broad publication.

**Do not assume:**

- That registration success proves person matching, check-in eligibility, or staff follow-up.
- That the presence of relevant Rock tables proves the flow is configured.

[Reviewed community preregistration source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz), [reviewed community transfer recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)

### Recipe: Validate status automation

**Outcome:** A status rule moves only currently eligible requests and can be retried safely.

1. Record the source status, destination status, Data View, job, and intended business rule.
2. Review the Data View with a bounded sample.
3. Confirm every returned request is still in the source status.
4. Remove unintended fixed cutoff dates or stale criteria.
5. If age in status matters, validate the available status-history evidence rather than assuming `ModifiedDateTime` represents the transition.
6. Run the automation through its configured job in a controlled scope.
7. Compare source and destination counts.
8. Verify request state consistency and review job history.
9. Re-evaluate the Data View to confirm moved requests no longer qualify.
10. Stop if history semantics or installed automation behavior cannot be verified.

This recipe is based on reviewed community patterns and requires live validation against the installed Rock version.

## Known Gaps And Live Verification

No live-instance review was performed while producing this guide. Some approved community claims in the evidence pack had previously received bounded read-only verification of relevant feature surfaces. Those checks did not prove that any specific connection process, preregistration path, workflow, campaign, permission model, or report is configured correctly.

The following require local verification:

- Installed Rock version, patch level, and whether legacy or Obsidian blocks are active.
- Enabled Connections views and block-level columns, filters, badges, and Lava customizations.
- Connection type, opportunity, request, and page security.
- Request-level security performance at local volume.
- Status order, sequential mode, completion requirements, and status-automation behavior.
- Due-date calculation mode and type-, opportunity-, or status-level offsets.
- Connector-group membership, campus mapping, defaults, campaign overrides, and workload capacity.
- Future-follow-up dates and the Connection Request Workflow Triggers job.
- Workflow trigger applicability, persistence, input entity, and downstream outcome.
- Placement-group requirements and actual membership creation.
- Public-form person matching, duplicate prevention, CAPTCHA mode, and end-to-end staff follow-up.
- Communication templates, snippets, phone eligibility, sender configuration, permissions, and delivery.
- AI provider access, prompt configuration, generated-summary quality, and governance.
- External dashboard licensing and authorization in addition to Rock page security.
- Community recommendations concerning status-age history, retry-safe Data Views, board-signal design, and registration-to-request workflows.
- Current v20 release status and whether any alpha feature described in release notes has changed before production use.

Where evidence is insufficient, mark the result as unverified rather than inferring behavior from a field name, model, source branch, dashboard label, or successful UI action.

## Source Map

### Official documentation

- [Connections documentation index](https://community.rockrms.com/documentation/engagement/connections?Version=v19.0) — v19 documentation structure.
- [Intro to Connections](https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections?Version=v19.0) — hierarchy, state, status, activities, campus, and profile visibility.
- [Navigate the Connections Tools](https://community.rockrms.com/documentation/engagement/connections/connection-requests/navigate-the-connections-tools?Version=v19.0) — navigation, filters, enabled views, and quick metrics.
- [Connections Views](https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views?Version=v19.0) — list, board, request detail, bulk selection, sequential movement, AI summaries, activities, and placement.
- [Enter New Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connection-requests/enter-new-connection-requests?Version=v19.0) — self-service, staff, and workflow entry.
- [Operational Snapshot](https://community.rockrms.com/documentation/engagement/connections/connection-requests/operational-snapshot?Version=v19.0) — workload, follow-up, status, connector, and completion metrics.
- [Configure Connection Types](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types?Version=v19.0) — enabled views, security, due dates, activities, statuses, sources, and automations.
- [Configure Connection Opportunities](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities?Version=v19.0) — connector groups, default connectors, placement groups, workflows, and transfer controls.
- [Configure Connection Requests](https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-requests?Version=v19.0) — activities, transfers, and badges.
- [Connection Workflows](https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows?Version=v19.0) — triggers, workflow inputs, and connection workflow actions.
- [Bulk Update Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests?Version=v19.0) — specialized and list-based bulk operations.
- [Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns?Version=v19.0) — campaign documentation index.
- [Set Up Connection Campaigns](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/set-up-connection-campaigns?Version=v19.0) — audience, request creation, limits, recurrence, and opt-out behavior.
- [Campaign Connection Requests](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/campaign-connection-requests?Version=v19.0) — on-demand request allocation.
- [Intro to Campaign Connectors](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-campaign-connectors?Version=v19.0) — group membership, campus, and connector overrides.
- [Sample Campaign Recipes](https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/sample-campaign-recipes?Version=v19.0) — official examples, not universal defaults.

### Official release and demonstration evidence

- [Connections Helps Prevent Your People from Falling Through the Cracks](https://www.youtube.com/watch?v=7rxTGLLhlrU) — approved v19 evidence for metrics, due-date configuration, list options, bulk actions, AI summaries, and sequential statuses.
- [3 Underrated Features Churches Are Overlooking](https://www.youtube.com/watch?v=edanHiYSDIM) — approved v19 rollout-training and CAPTCHA evidence.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — v18.1, v19.3, and supplied v20 Alpha distinctions.

### Immutable implementation evidence

- [Connection type enabled-view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionTypeSummaryBag.cs) — commit-scoped list, board, grid, snapshot, and celebration flags.
- [Connection status configuration model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusBag.cs) — commit-scoped status fields and automation collection.
- [Daily request-count model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Connection/ConnectionOpportunityNavigation/ConnectionRequestCountsPerDayBag.cs) — commit-scoped new and completed daily count structure.
- [Connection Opportunity reporting filter](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs) — commit-scoped reporting implementation.

### Community-reviewed guidance and examples

- [Family preregistration and follow-up discussion](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) — reviewed operational guidance for data quality and end-to-end testing.
- [Analytics and embedded reporting discussion](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) — reviewed guidance for Rock security and external licensing.
- [Registration-to-Connection Request Transfer Workflow](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request) — reviewed community recipe requiring local validation.
- [Connection Request Add from Profile Workflow](https://community.rockrms.com/recipes/57) — older community recipe, explicitly not core-reviewed or endorsed.
- [Connection Opportunity Search customization](https://community.rockrms.com/ask/developing/2645) — community Q&A example, not official behavior.