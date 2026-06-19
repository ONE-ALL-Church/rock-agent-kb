---
id: authored-workflows
title: Workflows
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Workflows

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Workflows index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock workflows are configurable process engines. They collect data, evaluate conditions, call actions, show forms, create or update Rock records, send communications, wait for later processing, and connect ministry processes to pages, triggers, Lava, jobs, integrations, and reporting. They are one of Rock's most powerful extension points because they let administrators automate work without writing compiled plugins, while still giving developers and agents hooks through Lava, REST, webhooks, attributes, and source-level model behavior.

Treat every workflow as two related things:

1. A **Workflow Type** is the definition: attributes, activities, actions, forms, templates, status labels, persistence behavior, and security.
2. A **Workflow** is a running or completed instance of that definition, with concrete attribute values, activities, actions, status, errors, and history.

The official workflow manual, [Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12), is the primary authority for concepts, configuration, entity triggers, form behavior, version notes, and administrative screens. RockU provides short training modules for practical learning paths such as [What is a Workflow](https://community.rockrms.com/rocku/workflows/what-is-a-workflow), [Components of a Workflow](https://community.rockrms.com/rocku/workflows/components-of-a-workflow), [Workflow Entry](https://community.rockrms.com/rocku/workflows/workflow-entry), [Persisted Workflows](https://community.rockrms.com/rocku/workflows/persisted-workflows), [Workflow Performance Tips](https://community.rockrms.com/rocku/workflows/workflow-performance-tips), [Workflow Person Entry](https://community.rockrms.com/rocku/workflows/workflow-person-entry), [Electronic Signatures](https://community.rockrms.com/rocku/workflows/electronic-signatures-1), and [Form Builder](https://community.rockrms.com/rocku/workflows/form-builder). Use source code and migrations for exact field behavior when the docs are thin; for example, Person Entry options are represented by `Hide`, `Optional`, and `Required` in the `WorkflowActionFormPersonEntryOption` enum in Rock's source ([C# enum](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Workflow/WorkflowActionFormPersonEntryOption.cs), [Obsidian enum](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Workflow/workflowActionFormPersonEntryOption.ts)).

For operational work, start from these questions:

1. **How is the workflow launched?** Check Workflow Entry blocks, entity triggers, connection or step triggers, grid actions, Lava `workflowactivate`, webhooks, jobs, and any external integration. Community examples show common "where used" audits across blocks, triggers, and Lava references ([Workflow Finder](https://community.rockrms.com/recipes/457)).
2. **Is it persisted?** If a workflow waits, delays, suspends, or needs later processing, inspect active instances and the Process Workflows job. Community health recipes emphasize that stuck active workflows can keep reprocessing and should be monitored ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).
3. **Which attributes carry state?** Workflow attributes are the input and state contract. Before changing a workflow, list attribute names, keys, field types, default values, and whether they are set by forms, query string parameters, Lava, triggers, webhooks, or helper workflows.
4. **Which person is involved?** Person Entry can create or update people without manually creating workflow attributes for every person field, but it still stores selected people through configured person-related attributes and processor logic. Verify how your version maps the form's Person, Spouse, campus, address, email, phone, and SMS opt-in settings.
5. **What completes the workflow?** A workflow that never reaches a completion action can remain active indefinitely unless controlled by maximum age, completion logic, manual intervention, or operational cleanup.
6. **What security boundary is involved?** Workflow launch permissions, block security, Lava command enablement, SQL-enabled HTML blocks, external forms, webhooks, and administrative screens must be checked separately.

Do not assume that a workflow definition explains every launch path. In real Rock instances, a Workflow Type can be used by a visible Workflow Entry page, a hidden modal page, a grid action, a workflow trigger, a connection process, a step process, a webhook endpoint, a Lava command in an HTML block, a helper workflow, or a third-party integration. When a workflow is being retired or changed, perform a "where used" review before editing production behavior.

## 2. Scope And Terminology

This guide covers Rock RMS workflows as a concept area: Workflow Types, workflow instances, activities, actions, forms, Person Entry, triggers, activation paths, integrations, jobs, operational monitoring, reporting, and developer landmarks. It also covers related dependencies: Lava, jobs, communications, security, attributes, model-map concepts, source-code behavior, and community implementation patterns.

This guide does not replace a live-instance audit. Rock is highly configurable, and many production workflows depend on local IDs, GUIDs, custom attributes, custom pages, plugins, SQL, Lava snippets, custom REST endpoints, external webhooks, or ministry-specific conventions. When a detail depends on local configuration, this guide says what to inspect.

Key terms:

**Workflow Type**
The reusable process definition. It contains attributes, activity types, action types, form configuration, status options, templates, completion behavior, and security. In the official docs, the distinction between Workflow Types and Workflows is foundational ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

**Workflow**
A specific running or completed instance of a Workflow Type. It has a name, status, state, attributes, activities, actions, and audit metadata. Agents should treat a workflow instance as evidence, not merely a definition.

**Activity Type**
A configured phase or branch in the workflow definition. It groups action types. Activities can be activated by workflow processing, Lava, actions, or triggers depending on configuration.

**Activity**
A concrete instance of an Activity Type inside a workflow instance.

**Action Type**
A configured step within an Activity Type. Examples include showing a form, setting attributes, running Lava, sending communications, activating activities, completing workflows, delaying, logging errors, requesting background checks, and many other action components documented across the workflow manual and version notes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

**Action**
A concrete execution record for an Action Type in a workflow instance.

**Workflow Attribute**
A typed data field defined for the Workflow Type. Attributes hold submitted form values, intermediate state, entity references, integration payloads, routing decisions, comments, selected people, and external IDs. Attributes are central to both no-code workflows and developer-driven workflows.

**Workflow Form**
A workflow action that displays fields to a user. The form can expose workflow attributes, organize fields into sections, apply conditional logic in newer Rock versions, and optionally include Person Entry. The Model Map lists workflow form-related models such as [Workflow Action Form](https://community.rockrms.com/ModelMap), [Workflow Action Form Attribute](https://community.rockrms.com/ModelMap), and [Workflow Action Form Section](https://community.rockrms.com/ModelMap).

**Person Entry**
A workflow form feature that gathers individual and spouse information without requiring separate workflow attributes for every person field. Rock source and migrations show it stores many configuration options on `WorkflowActionForm`, including campus, spouse, email, mobile phone, birthdate, address, marital status, gender, record status, connection status, and related person attributes ([Person Entry migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs), [gender option migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011171742444_WorkflowActionFormPersonEntryGenderOption.cs)).

**Persisted Workflow**
A workflow that is saved to the database for later processing, review, waiting, delay, or completion. RockU calls out persisted workflows as a distinct training topic ([Persisted Workflows](https://community.rockrms.com/rocku/workflows/persisted-workflows)). Operationally, persisted workflows are where agents most often find stuck processes, repeated errors, and job-related delays.

**Trigger**
A configuration that launches or activates a workflow when some event happens, such as an entity change. The official documentation locates entity trigger configuration under Admin Tools > General Settings > Workflow Triggers ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

**Workflow Entry Block**
A page block that lets users start or continue workflow entry. Source code indicates the older `Activate Workflow` block is deprecated because the Workflow Entry block now supports the relevant activation and query-string attribute behavior ([ActivateWorkflow.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)).

**Form Builder**
A user-facing form-building experience backed by workflows. Community examples emphasize that Form Builder forms are workflows and often need clear entry URLs, preview links, and submission reporting for staff adoption ([Form Builder - Helpful Links](https://community.rockrms.com/recipes/347)).

## 3. Workflows Mental Model

Think of a workflow as a stateful process graph backed by Rock entities and attributes.

A simple workflow might do this:

1. Show an external form.
2. Store submitted values in workflow attributes.
3. Attach a person using Person Entry.
4. Route the request based on a selected topic.
5. Send a communication.
6. Create a connection request.
7. Mark itself complete.

A more complex workflow might:

1. Start from a webhook.
2. Store raw JSON in a text attribute.
3. Run Lava to parse fields.
4. Activate a loop activity once per item.
5. Call helper workflows for reusable operations.
6. Persist and wait for staff review.
7. Resume when a person submits an electronic signature.
8. Complete after all required downstream objects are created.

The mental model has five layers.

**Definition Layer**
The Workflow Type defines allowed attributes, activity types, action types, forms, statuses, templates, and rules. It is the blueprint.

**Instance Layer**
Each Workflow instance carries real state. It may be active, complete, canceled, errored, waiting, or otherwise labeled according to configuration and Rock behavior. Agents should inspect actual workflow rows when troubleshooting because definition settings alone do not prove current state.

**Execution Layer**
Activities and actions execute in order and may activate other activities. Some actions are immediate. Others persist state, delay, show forms, wait on user input, or rely on jobs. A workflow can run synchronously from a page request or asynchronously through later processing depending on how it was launched and configured.

**Data Layer**
Workflow attributes are the process memory. They also form the integration contract between forms, Lava, actions, helper workflows, and external systems. Attribute values may store raw text, person aliases, group IDs, GUIDs, files, JSON, selected defined values, connection opportunities, comments, or other typed data.

**Activation Layer**
Workflows can be launched from many surfaces. Official and community sources show at least these patterns:

- Workflow Entry pages and Form Builder entry pages ([Workflow Entry](https://community.rockrms.com/rocku/workflows/workflow-entry), [Form Builder](https://community.rockrms.com/rocku/workflows/form-builder)).
- Entity triggers configured under Workflow Triggers ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).
- Lava `workflowactivate`, available when the command is enabled ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)).
- Grid launches and custom grid actions ([Launch Workflow From Grid](https://community.rockrms.com/rocku/workflows/launch-workflow-from-grid), [Launching a workflow from a Grid](https://community.rockrms.com/recipes/300)).
- Webhook-to-workflow patterns ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473), [Send Workflow Info To Zapier](https://community.rockrms.com/recipes/211)).
- Connection, group requirement, and step-related triggers in local configuration, as shown by community "where used" audit patterns ([Workflow Finder](https://community.rockrms.com/recipes/457)).
- Helper workflows activated by a parent workflow ([Helper Workflow Starter Pack](https://community.rockrms.com/recipes/258)).

Agents should never ask "where is the workflow page?" as the only launch-path question. Ask "what can create or reactivate this Workflow Type?"

## 4. Source Authority And How To Use This Guide

Use sources in this order.

**1. Official Rock documentation**
The workflow manual, [Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12), is the first place to verify supported concepts, UI paths, action documentation, version notes, triggers, Workflow Entry, forms, and configuration screens.

**2. Rock source code and migrations**
Use source code when exact behavior matters, especially for fields introduced by migrations, Lava command behavior, deprecation warnings, internal APIs, and tests. Examples:

- `workflowactivate` behavior and security are documented in source and integration tests ([WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs), [WorkflowActivateTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Commands/WorkflowActivateTests.cs)).
- Person Entry fields and options are visible in migrations and view models ([WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs), [FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs), [FormPersonEntryViewModel.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/WorkFlow/FormBuilder/FormPersonEntryViewModel.cs)).
- Obsidian TypeScript definitions describe client-facing bags for Person Entry configuration and values ([personEntryConfigurationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryConfigurationBag.d.ts), [personEntryValuesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryValuesBag.d.ts)).

**3. RockU training**
RockU is useful for onboarding and for understanding how Rock's authors frame workflows operationally. The [Workflows RockU section](https://community.rockrms.com/rocku/workflows) includes modules on components, entry, persistence, performance, styling, sample workflows, grid launching, Person Entry, electronic signatures, and Form Builder.

**4. Model Map**
The [Model Map](https://community.rockrms.com/ModelMap) is useful for identifying relevant model families, but it is not a complete operational manual. In the source pack it confirms workflow-form models in the Workflow category: Workflow Action Form, Workflow Action Form Attribute, and Workflow Action Form Section.

**5. Release notes and spotlight records**
Use release notes to detect version caveats. The official manual has version update notes through Rock 18.1 for workflow changes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)), and official Rock release notes should be checked for later workflow, form, security, and automation changes before production decisions ([Release Notes](https://www.rockrms.com/releasenotes)). The Triumph GitHub spotlight notes a v16.7 change: workflow form Person Entry campus selection gained an option to filter inactive campuses, aligning workflow form action behavior with Form Builder behavior ([GitHub Spotlight: 10/18/2024](https://www.triumph.tech/resources/github-spotlight-10182024)). For production decisions, verify the exact Rock version and confirm behavior in the installed codebase.

**6. Community recipes**
Recipes are useful examples, not primary authority. The Rock community recipe pages themselves warn that recipes are contributed and not necessarily reviewed or endorsed. Use them as implementation patterns and prompts for verification, especially around reports, modals, helper workflows, webhooks, and where-used utilities.

## 5. Core Configuration And Data Model

### Workflow Type Configuration

A Workflow Type is configured under the workflow administration area. The official documentation references General Settings > Workflow Configuration and describes sections such as workflow attributes, activities, actions, status, and templates ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). In practice, agents should capture the following for any Workflow Type audit:

- Name.
- Id and Guid.
- Category or organizational grouping.
- Description and purpose.
- Active/inactive state, if visible.
- Security permissions.
- Workflow attributes: name, key, field type, default value, visibility, required state, and any configured values.
- Activity types: order, name, activation/completion behavior, and conditions.
- Action types: component/action type, order, configuration, conditional criteria, persistence behavior, and error handling.
- Form actions: fields, sections, Person Entry, pre/post HTML, submit button text, completion text, and conditional display rules.
- Status values used by the workflow.
- Templates: entry, detail, summary, or any display templates available in the installed version.
- Maximum age or auto-completion settings if available in the installed version.
- Change log or notes if present.

The official docs note that workflow summary templates can be customized per workflow type and generally do not need changes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). If an agent sees unexpected workflow detail rendering, inspect the Workflow Type templates before assuming a block issue.

### Workflow Attributes

Workflow attributes are the main contract between users, actions, integrations, and reporting. They are configured at the Workflow Type level and populated on workflow instances. Attributes can represent:

- Submitted form fields.
- Person or Person Alias references.
- Group, campus, connection opportunity, or defined value choices.
- Raw integration payloads.
- Derived values created by Lava.
- Counters and loop state.
- Routing values such as topic, department, or assigned worker.
- Files or signature-related artifacts.
- Status flags.
- External system IDs.
- Error or response messages.

Operationally, attribute keys matter more than display names. Lava, actions, integrations, imported workflows, helper workflows, and reports often reference keys. Community examples show administrators adding helper HTML or reports to display workflow attribute keys without editing each attribute ([View Workflow Attributes Without Editing Workflow](https://community.rockrms.com/recipes/203), [Finding People from Workflows](https://community.rockrms.com/recipes/437)).

Agent checklist for workflow attributes:

1. Export or list all attributes with keys and field types.
2. Identify which attributes are filled by the first form.
3. Identify which are set by query string, webhook body, Lava, trigger context, helper workflow parameters, or staff action.
4. Identify which attributes are used only for internal state.
5. Identify Person-related attributes and whether they store a Person Alias Guid, Person Id, text, or another format.
6. Identify stale or unused attributes before cleanup.
7. Before renaming keys, search every action, Lava snippet, communication template, block configuration, SQL report, and integration that could reference them.

### Activities And Actions

A workflow's activity types organize action types into process phases. A common pattern is:

- Start activity: collect input and initialize values.
- Routing activity: evaluate selections and assign staff.
- Worker activity: show staff form or send notifications.
- Integration activity: create/update external or Rock records.
- Completion activity: send final communication and mark complete.
- Error activity: log or notify on failure.

Actions are where work happens. Depending on installed components, actions may show forms, set attributes, activate activities, run Lava, send communications, persist workflow state, complete/cancel workflows, delay processing, create entities, request background checks, log errors, and call integrations. The official manual's version notes mention additions such as Delay, Background Check Request, Log Error, and Persist Workflow behavior across earlier versions ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

Agents should document action order. A workflow bug often comes from an action executing before an attribute is set, an activity being reactivated unexpectedly, a condition allowing both branches, or a completion action ending the workflow before later actions can run.

### Workflow Forms

Workflow forms are configured as action forms. The Model Map identifies workflow form models in the Workflow category, including [Workflow Action Form](https://community.rockrms.com/ModelMap), [Workflow Action Form Attribute](https://community.rockrms.com/ModelMap), and [Workflow Action Form Section](https://community.rockrms.com/ModelMap). A form action generally includes:

- Form title and instructions.
- Attribute fields exposed to the user.
- Field order.
- Sections.
- Required fields.
- Visibility or conditional logic, depending on version.
- Person Entry settings.
- HTML before and after fields.
- CSS classes or styling hooks.
- Submit behavior.
- Success or completion messaging.

For exact fields available in your instance, inspect the Workflow Type form action configuration and the `WorkflowActionForm` schema in the database or source version. Source migrations show that Person Entry configuration is stored on `WorkflowActionForm` and evolved over versions ([WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs), [WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2016.0/Version%201.16.0/202308242352371_WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs)).

### Persistence And Processing

A workflow that completes immediately may not need long-term active state. A workflow that waits on users, delays, or background processing must persist. RockU separates [Persisted Workflows](https://community.rockrms.com/rocku/workflows/persisted-workflows) and [Workflow Performance Tips](https://community.rockrms.com/rocku/workflows/workflow-performance-tips), which reflects a real operational distinction: persisted active workflows become ongoing workload.

Inspect:

- Whether the workflow uses a Persist Workflow action.
- Whether actions delay, wait, suspend, or require external response.
- Whether the Process Workflows job is running and healthy.
- Number of active workflow instances by type and status.
- Oldest active workflow instance.
- Error counts.
- Last processed timestamps if available.
- Whether maximum workflow age is configured in your version. The official docs note Rock 13 added a Maximum Workflow Age setting to automatically complete old workflows ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

### Status

Status is both a user-facing label and an operational signal. The official docs include Status as a core workflow component ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). In live systems, agents should not assume status strings are standardized. Many churches define local statuses like New, Pending Staff Review, Waiting for Signature, Follow Up Complete, Canceled, Duplicate, Error, or Imported.

For reporting, normalize status by asking:

- Which statuses mean "active and expected"?
- Which mean "waiting on someone"?
- Which mean "complete"?
- Which mean "failed"?
- Which are legacy?
- Are there workflows marked complete but still carrying error states?
- Are there active workflows with terminal status labels?

## 6. Primary Entities And Relationships

This section describes the common conceptual relationships. Verify exact table and column names in the installed Rock version before writing SQL or API code.

**WorkflowType -> Workflow**
One Workflow Type can have many Workflow instances. The type defines the process. Instances store execution state.

**WorkflowType -> Attribute -> AttributeValue**
Workflow Types define attributes. Workflow instances carry values for those attributes. Attribute values are often the most important troubleshooting evidence.

**WorkflowType -> WorkflowActivityType -> WorkflowActionType**
Activity Types belong to a Workflow Type. Action Types belong to Activity Types. They define the executable process graph.

**Workflow -> WorkflowActivity -> WorkflowAction**
Workflow instances create concrete activities and actions as processing occurs. These records represent what actually happened.

**WorkflowActionType -> WorkflowActionForm**
A form action has form-specific configuration. The Model Map lists Workflow Action Form as a workflow model ([Model Map](https://community.rockrms.com/ModelMap)). Source migrations show `WorkflowActionForm` contains Person Entry configuration fields ([WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs)).

**WorkflowActionForm -> WorkflowActionFormSection -> WorkflowActionFormAttribute**
Forms can have sections and attribute field configurations. The Model Map identifies both Workflow Action Form Section and Workflow Action Form Attribute as workflow models ([Model Map](https://community.rockrms.com/ModelMap)).

**WorkflowActionForm -> Person Entry settings**
Person Entry is stored as configuration associated with the form. Source files show settings for autofill, hide-if-current-person-known behavior, campus, campus status, connection status, record status, person attributes, spouse label, and visibility options for person fields ([FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs), [FormPersonEntryViewModel.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/WorkFlow/FormBuilder/FormPersonEntryViewModel.cs)).

**Person Entry values -> Person and PersonAlias**
Person Entry processing may use or create person records and store person alias values into workflow attributes. Integration tests demonstrate processor behavior around logged-in person and spouse matching, and then reading person alias GUIDs from workflow attributes ([WorkflowPersonEntryProcessorTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Workflow/WorkflowPersonEntryProcessorTests.cs)). In a live instance, inspect the configured Person and Spouse attributes and their stored raw values.

**WorkflowTrigger -> EntityType/WorkflowType**
Entity triggers connect database events to workflow activation. The official manual describes entity triggers under Admin Tools > General Settings > Workflow Triggers ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). Inspect the trigger type, entity type, workflow type, conditions, and any attributes populated from the triggering entity.

**Page/Block -> WorkflowType**
Workflow Entry blocks, Form Builder pages, modal pages, and custom pages may reference Workflow Types directly. Community "where used" patterns include page blocks with Workflow Entry configuration and HTML/Lava references ([Workflow Finder](https://community.rockrms.com/recipes/457)).

**Lava -> WorkflowType/Workflow/ActivityType**
The `workflowactivate` Lava command can create workflows, activate activities, set workflow names, pass attributes, and re-activate existing waiting workflows when enabled ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands), [WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs)).

**External system -> Webhook -> Workflow**
Webhook integrations can launch workflows and pass payloads into attributes. Community examples show raw body attributes and response attributes used in webhook-to-workflow patterns ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)).

## 7. Common Workflows Workflows

### Request Intake Workflow

Use for contact forms, facility requests, benevolence requests, IT support, pastoral care, prayer, or ministry operations.

Core pattern:

1. User submits a Workflow Entry or Form Builder form.
2. Form stores submitted fields as workflow attributes.
3. Person Entry identifies or creates the person if needed.
4. Workflow routes based on campus, ministry, topic, or urgency.
5. Staff receive communication or assignment.
6. Staff complete a worker form.
7. Workflow creates follow-up records or marks complete.

Operational checks:

- Confirm external form page and Workflow Entry block settings.
- Confirm unauthenticated users can access only the intended page and form.
- Confirm required fields match ministry requirements.
- Confirm routing attribute values match current departments or staff.
- Confirm completion happens after staff response.
- Confirm old requests are not active forever.

Community examples include topic-based assignment using groups and member attributes to avoid editing workflow logic when staff assignments change ([Workflow Assignment by Topic](https://community.rockrms.com/recipes/164)).

### Event Call-To-Action Workflow

Use for events where attendees receive a text link and choose next steps, groups, or follow-up actions.

Core pattern:

1. Event participation or check-in identifies attendees.
2. Communication sends a workflow form link.
3. Attendee chooses a call-to-action response.
4. Workflow adds them to a group, creates a connection request, sends a communication, or tags them for follow-up.
5. Staff report on response groups or connection queues.

A community implementation describes event attendees receiving a text link to a workflow form, selecting next steps, and being placed into follow-up groups or connection mechanisms ([Event Participant Call-To-Action Using a Workflow Form](https://community.rockrms.com/recipes/445)). Use this as a pattern, not as a drop-in production design.

Verify live:

- SMS phone number configuration.
- Consent and SMS compliance posture.
- Event attendance source.
- Group IDs and connection opportunity IDs.
- Duplicate handling if the same person submits multiple times.
- Whether the form should require login, use Person Entry, or accept anonymous submission.

### Staff Approval Workflow

Use for reimbursements, communication requests, facility approvals, purchase requests, content review, or ministry sign-offs.

Core pattern:

1. Requester submits a form.
2. Workflow determines approver.
3. Approver receives email or dashboard task.
4. Approver submits a staff-only workflow form.
5. Workflow branches on approve, reject, need more information, or cancel.
6. Final communication is sent.
7. Workflow completes or persists for follow-up.

Design considerations:

- Put approver assignment in data when possible. A group-member-attribute model can let ministry leaders update assignments without changing workflow action conditions ([Workflow Assignment by Topic](https://community.rockrms.com/recipes/164)).
- Store approval decision, approver, timestamp, and comments in workflow attributes.
- Use security to protect staff-only forms.
- If approval creates financial, HR, or access records, log enough context for audit.

### Helper Workflow

A helper workflow performs one reusable task and is called by parent workflows. Community examples compare helper workflows to functions or subroutines and show use cases like setting SMS enabled, creating connection requests, creating people, adding steps, adding group members with attributes, and sending SMS ([Helper Workflow Starter Pack](https://community.rockrms.com/recipes/258)).

Good helper workflow traits:

- Single responsibility.
- Clear attribute contract.
- No direct user entry page unless needed for testing.
- Predictable completion.
- Error attribute or status.
- Idempotency when possible.
- Versioned name if behavior changes.

Use helper workflows when:

- Multiple workflows need the same operation.
- Looping is easier in Lava than in action configuration.
- You need one tested process for creating a specific Rock object.
- You want parent workflows to stay readable.

Avoid helper workflows when:

- A built-in action is simpler and used only once.
- The helper hides important side effects.
- Debugging would require jumping through too many nested workflows.
- It creates large volumes of persisted child workflows without cleanup.

### Grid-Launched Workflow

Grid-launched workflows let staff select rows in Rock grids and run a workflow against those records. RockU includes [Custom Grid Actions](https://community.rockrms.com/rocku/workflows/custom-grid-actions) and [Launch Workflow From Grid](https://community.rockrms.com/rocku/workflows/launch-workflow-from-grid). A community recipe notes that different grids pass different entity contexts, so template workflows may need Lava that understands whether the row represents a person, group member, or another entity ([Launching a workflow from a Grid](https://community.rockrms.com/recipes/300)).

Agent checks:

- Which page and grid defines the custom action?
- What entity type does the grid pass?
- What identifier is passed to the workflow?
- Does the workflow expect PersonAlias Guid, Person Id, GroupMember Id, or another value?
- Can staff accidentally launch it for too many rows?
- Is the workflow idempotent?
- Does security restrict who can launch it?

### Webhook-To-Workflow Integration

Use when external systems need to send payloads into Rock and launch a workflow.

Patterns:

- Zapier catches or sends webhooks and a workflow sends data outward ([Send Workflow Info To Zapier](https://community.rockrms.com/recipes/211)).
- Clearstream or another external tool pushes to Rock and launches a workflow immediately rather than waiting on a scheduled job ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)).
- Workflow attributes store raw request body, parsed fields, and response content.

Agent checks:

- Endpoint path and authentication.
- Workflow Type configured for webhook launch.
- Attribute that stores raw body.
- Attribute used for response body if applicable. The Clearstream recipe references `WebhookResponse` as a key used in the webhook handler path ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)).
- JSON parsing logic.
- Error response behavior.
- Duplicate prevention.
- Rate limits and replay behavior.
- Logs and exception handling.

### Form Builder Workflow

Form Builder gives staff a form-building experience backed by workflow infrastructure. RockU has a dedicated [Form Builder](https://community.rockrms.com/rocku/workflows/form-builder) module, and the official docs note recent improvements such as Rock 18.1 support for easier link sharing with a link icon, block setting, and slug field ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

Agent checks:

- Where Form Builder appears in the page tree.
- Which Workflow Type each form creates.
- Entry URL pattern.
- Submission reporting page.
- Security model for form editors versus form submitters.
- Whether staff know how to preview and share the form.
- Whether Person Entry is enabled and configured appropriately.
- Whether submissions can be communicated with or exported.

A community helper-links recipe argues that staff may not understand that Form Builder forms are workflows and may need obvious preview, URL, and submission links ([Form Builder - Helpful Links](https://community.rockrms.com/recipes/347)).

### Electronic Signature Workflow

Electronic signature workflows commonly combine forms, group requirements, signature documents, communications, and follow-up. RockU includes [Electronic Signatures](https://community.rockrms.com/rocku/workflows/electronic-signatures-1). A community group requirement helper workflow describes a pattern where requirement workflows are tied to signature documents and may need resend or remediation behavior when a person does not complete the signature flow ([Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482)).

Agent checks:

- Signature document template.
- Requirement SQL or criteria.
- "Does Not Meet Requirement" workflow.
- Auto-initiate setting.
- Trigger that sends the workflow.
- Whether incomplete requirement workflows can be resent through UI.
- Email deliverability and spam issues.
- Whether old requirement workflows block new ones.
- Completion conditions for the requirement.

### Bulk Creation Workflow

Workflows can generate multiple Rock records from a schedule or list. A community recipe uses a workflow to create multiple sign-up opportunities from schedule parameters, with a form for inputs, Lava to generate date lists, loop counters, activity activation, duplicate checks, and per-date creation ([Create Multiple Sign-Up Opportunities From Schedule](https://community.rockrms.com/recipes/479)).

Agent checks:

- Loop counter attributes.
- Maximum expected iterations.
- Duplicate detection.
- Performance impact.
- Whether the workflow persists between iterations.
- What happens if the workflow fails halfway.
- Whether created records can be rolled back or safely rerun.

### Finance Or Contribution Workflow

Workflows can support finance-adjacent processes such as non-cash gifts or handoff to accounting systems. A community non-cash contribution recipe combines workflow and connection types and stores item information and pictures as connection request attributes ([Non-Cash Contribution Workflow](https://community.rockrms.com/recipes/253)). A Zapier recipe describes sending workflow information to external services such as QuickBooks through Zapier ([Send Workflow Info To Zapier](https://community.rockrms.com/recipes/211)).

For finance workflows, verify:

- Permissions.
- Audit trail.
- Data retention.
- PII and donor privacy.
- Approval requirements.
- External accounting integration behavior.
- Error handling and reconciliation.
- Whether workflow data should become a formal financial transaction, connection request, note, document, or attachment.

## 8. Triggers And Activation Deep Dive

### Workflow Entry Activation

The Workflow Entry block is the standard page-based entry path. It can start a workflow and show configured forms. Source code for the deprecated Activate Workflow block states that the Workflow Entry block now supports setting attribute values from query string parameters and makes the older Activate Workflow block unnecessary ([ActivateWorkflow.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)).

Inspect:

- Page route.
- Block type and block settings.
- Workflow Type selection or parameter binding.
- Whether workflow type is static or supplied by route/query string.
- Attribute values accepted from query string.
- Security on page, block, and workflow type.
- Whether the entry page is internal or external.
- Whether anonymous users can submit.
- Whether the page is embedded in a modal or iframe.

### Entity Triggers

Entity triggers can launch workflows when Rock entities change. The official manual places them under Admin Tools > General Settings > Workflow Triggers and describes selecting a trigger type ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

Agent trigger audit:

1. Open Workflow Triggers.
2. Filter by Workflow Type if possible.
3. Record trigger type.
4. Record entity type.
5. Record qualifiers or conditions.
6. Record whether the trigger fires on add, update, delete, pre-save, post-save, or another local option.
7. Record which workflow attributes are populated from the entity.
8. Confirm whether the trigger is active.
9. Test on a non-production entity when possible.

Do not assume a trigger fires just because it is configured. Verify by checking recent workflow instances after a known entity change.

### Lava `workflowactivate`

The `workflowactivate` Lava command can launch a new workflow or activate an activity on an existing workflow. Official Lava docs list parameters for workflow type, workflow id, workflow name, and activity type ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)). Source code confirms important behavior:

- The command is a secured Lava block and must be enabled in the Lava render context ([WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs)).
- Workflow Type can be supplied as an integer, string integer, or GUID in source examples ([WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs)).
- Workflow Id can refer to an existing workflow.
- Activity Type is required when activating an activity in an existing workflow.
- Unrecognized parameters can be treated as workflow or activity attributes.
- The command exposes `Workflow`, `Activity`, and `Error` variables inside the block.
- Integration tests verify that the command returns a configuration error when not enabled and creates workflows when enabled ([WorkflowActivateTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Commands/WorkflowActivateTests.cs)).

Operational implications:

- Search HTML Content blocks, block pre/post HTML, communication templates, Lava files, and theme assets for `workflowactivate`.
- Confirm the Lava command is enabled only where needed.
- Prefer GUIDs over integer IDs for portable snippets.
- Validate attribute keys exactly.
- Handle `Error` output in user-facing or integration-facing Lava.
- Avoid launching unbounded workflows inside loops unless volume is controlled.

Minimal pattern:

```liquid
{% workflowactivate workflowtype:'WORKFLOW-TYPE-GUID' workflowname:'Readable Name' Person:'PERSON-ALIAS-GUID' %}
  {{ Workflow.Id }}
{% endworkflowactivate %}
```

This example is intentionally generic. In production, verify the expected raw value format for each attribute.

### Webhook Activation

Webhook-to-workflow patterns let external systems initiate workflows. A community Clearstream example distinguishes scheduled "Push to Rock RMS > Launch Workflow" behavior from an immediate webhook approach and describes RawBody and WebhookResponse attributes ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)).

Agent checks:

- Is the endpoint native Rock webhook-to-workflow, a custom handler, or a plugin endpoint?
- Does it launch instantly or depend on Process Workflows?
- Which Workflow Type is configured?
- What authentication/signature validation exists?
- Is raw payload stored?
- Is the response body controlled by a workflow attribute?
- Does the workflow complete immediately?
- What happens on errors?
- Is sensitive payload data retained longer than needed?

### Grid Activation

Grid activation is powerful because it lets staff run workflows against selected records. RockU includes grid-related training modules ([Custom Grid Actions](https://community.rockrms.com/rocku/workflows/custom-grid-actions), [Launch Workflow From Grid](https://community.rockrms.com/rocku/workflows/launch-workflow-from-grid)). Community guidance notes that the Lava or setup needed to extract a person can vary by grid because different grids pass different row entities ([Launching a workflow from a Grid](https://community.rockrms.com/recipes/300)).

Agent checks:

- Which block/grid has the action.
- Whether single-row or bulk selection is allowed.
- What object is passed.
- Whether the workflow action can be run twice.
- Whether the action respects security.
- Whether staff have confirmation before mass changes.
- Whether logs show who launched it.

### Connection, Step, Group, And Requirement Activation

Workflow triggers can also be embedded in other Rock areas. The Workflow Finder recipe lists connection type/opportunity triggers and step type/program triggers as usage locations it checks, and community examples show group requirement workflows tied to signature documents ([Workflow Finder](https://community.rockrms.com/recipes/457), [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482)).

When a workflow appears to launch "from nowhere," inspect:

- Connection Types and Opportunities.
- Step Programs and Step Types.
- Group Types.
- Group Requirements.
- Registration templates and events.
- Communication responses.
- Check-in or attendance workflows.
- Plugins and custom jobs.

## 9. Workflow Forms Deep Dive

### Form Design Principles

A workflow form should be designed around the process, not merely the data fields. For each form, define:

- Who fills it out?
- Are they authenticated?
- What decision or handoff happens after submission?
- Which fields are required for the next action?
- Which fields are for reporting only?
- Which fields should be hidden because they can be inferred?
- What should happen on duplicate submission?
- How will staff find and act on submissions?

Use the official workflow manual and Form Builder training as the baseline for form behavior, then inspect the live Workflow Action/Form Builder configuration for version-specific fields and validation ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12), [Form Builder](https://community.rockrms.com/rocku/workflows/form-builder)).

Use forms for human input. Use actions for derived values. Do not ask users to provide values Rock can already infer, such as current person, campus from context, event from route, or group from the launch path, unless there is a real operational reason.

### Form Fields And Sections

The Model Map identifies `Workflow Action Form Attribute` and `Workflow Action Form Section`, which reflects the distinction between a workflow attribute and its presentation on a specific form ([Model Map](https://community.rockrms.com/ModelMap)). The same workflow attribute can be internal-only, shown on one form, hidden on another, or set by an action.

Agent checks:

- Is every displayed field backed by the expected workflow attribute?
- Are required flags on the form aligned with downstream action requirements?
- Are field types appropriate?
- Are section headings useful?
- Are internal state attributes hidden?
- Are sensitive fields protected from public display?
- Are field keys stable?

### Conditional Logic

The official workflow manual notes that workflow form fields can have conditional logic in version update notes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). Because conditional UI behavior can vary by version and block implementation, inspect the specific form action in the live Rock instance.

Operational cautions:

- Hidden required fields can block submission if configured incorrectly.
- Conditional fields may not be populated when hidden.
- Downstream actions should not assume optional conditional values exist.
- Reports should distinguish "not asked" from "asked but blank" when the distinction matters.

### Person Entry

Person Entry lets a workflow form gather person and spouse information without making administrators define every person field as a workflow attribute. The official docs describe Person Entry as a way to gather individual and spouse information from a workflow form without manually creating workflow attributes for those questions ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). Source files show the configuration is extensive.

Important fields and concepts from source:

- Enable/allow Person Entry is stored on `WorkflowActionForm` ([WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs)).
- Pre and post HTML can be configured for the Person Entry section.
- Campus visibility and autofill behavior are configurable.
- Person Entry can hide if the current person is known.
- Spouse, email, mobile phone, birthdate, address, marital status, and gender use hide/optional/required-style options across versioned fields ([WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs), [WorkflowActionFormPersonEntryGenderOption.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011171742444_WorkflowActionFormPersonEntryGenderOption.cs)).
- SMS opt-in was added as a Person Entry form option in a Rock 16 migration ([WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2016.0/Version%201.16.0/202308242352371_WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs)).
- Form Builder source settings include campus visibility, inactive campus inclusion, campus status, connection status, record status, gender, email, mobile phone, SMS opt-in, birthdate, and address-related settings ([FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs), [FormPersonEntryViewModel.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/WorkFlow/FormBuilder/FormPersonEntryViewModel.cs)).
- Obsidian client configuration includes options for address, birthdate, campus list, email, ethnicity, gender, campus visibility, SMS opt-in visibility, marital status, mobile phone, race, spouse, pre/post HTML, and section CSS class ([personEntryConfigurationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryConfigurationBag.d.ts)).

Person Entry audit:

1. Confirm Person Entry is enabled.
2. Identify whether current person autofill is enabled.
3. Identify whether the section hides when current person is known.
4. Confirm which fields are hidden, optional, or required.
5. Confirm campus visibility and inactive campus behavior.
6. Confirm record status and connection status applied to new people.
7. Confirm address type and location behavior.
8. Confirm which workflow attributes receive Person and Spouse references.
9. Submit a test as anonymous, logged-in known person, and logged-in person with spouse if the workflow supports those cases.
10. Verify the stored raw values and created/updated person records.

### Campus Selection And Inactive Campuses

Source-level and release-note records indicate campus selection behavior has changed over time. The Form Person Entry settings default inactive campus inclusion to true as existing behavior before the option was introduced ([FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs)). A release spotlight notes that v16.7 added an option to filter inactive campuses in workflow form Person Entry, aligning workflow form action behavior with Form Builder ([GitHub Spotlight: 10/18/2024](https://www.triumph.tech/resources/github-spotlight-10182024)).

In a live instance, inspect:

- Rock version.
- Whether the form action exposes "include inactive campuses" or equivalent.
- Whether inactive campuses appear on public forms.
- Whether campus status filters are configured.
- Whether campus is required when shown.

### Form Styling

RockU includes [Form Styling](https://community.rockrms.com/rocku/workflows/form-styling). Styling can be done through form settings, CSS classes, theme CSS, pre/post HTML, or page layout. Avoid embedding brittle styling directly into workflow actions unless there is no better site-level or block-level mechanism.

Agent checks:

- Does the form render correctly on mobile?
- Does the external site theme style workflow controls consistently?
- Are required markers visible?
- Are validation messages clear?
- Is custom HTML accessible?
- Is any embedded CSS tied to old Bootstrap or theme classes?
- Does a modal iframe inherit the correct styling?

### Modal Workflow Entry

A community recipe demonstrates embedding a Workflow Entry page in a modal using an iframe and notes the need to configure allowed frame domains ([Modal Dialog for Workflow Entry](https://community.rockrms.com/recipes/141)). Treat this as a pattern requiring security review.

Verify:

- Allowed frame domains.
- Clickjacking protections.
- Same-site cookies and authentication behavior.
- Public/private page boundaries.
- Mobile behavior.
- Whether the modal traps focus and is accessible.
- Whether form completion closes the modal or leaves a blank embedded page.

## 10. Workflow Integrations Deep Dive

### Outbound Webhooks And Zapier

Workflows can send data outward to tools such as Zapier. A community recipe shows using a workflow action to send attributes to a Zapier catch hook and mentions use cases such as sending financial workflow data onward to accounting tools ([Send Workflow Info To Zapier](https://community.rockrms.com/recipes/211)).

Design checklist:

- Define the outbound payload schema.
- Use stable attribute keys.
- Include a Rock workflow ID and workflow type GUID.
- Avoid sending unnecessary PII.
- Store external response or failure details.
- Decide retry behavior.
- Add test and production endpoint separation.
- Document who owns the external Zap.

### Inbound Webhooks

Inbound webhook workflows should be designed like API endpoints, not just forms without UI.

Minimum contract:

- Endpoint URL.
- Authentication method.
- Expected HTTP method.
- Payload format.
- Required fields.
- Idempotency key or duplicate detection.
- Workflow Type.
- Raw payload attribute.
- Parsed attributes.
- Response attribute if supported.
- Error response behavior.
- Monitoring location.

The Clearstream recipe uses a RawBody attribute to preserve incoming body and a WebhookResponse attribute to send a response back in its pattern ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)). Verify the exact handler behavior in the installed Rock version or custom plugin before relying on that key.

### Lava As Integration Glue

Lava is often the glue between workflows and Rock data. It can:

- Read workflow attributes.
- Parse strings or JSON-like payloads.
- Build communication content.
- Call workflowactivate.
- Loop through collections.
- Render dynamic HTML.
- Build comments for connection requests.
- Transform registration, group, or person data before activating helper workflows.

The `workflowactivate` command is especially important for integration-style workflows because it can pass attribute values into child workflows ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)). Source code confirms unrecognized parameters are treated as possible workflow or activity attributes ([WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs)).

Security notes:

- Lava commands must be enabled explicitly in many contexts.
- SQL-enabled Lava in HTML blocks is powerful and risky.
- Workflow activation from public pages can create spam or database load if not protected.
- Never expose sensitive attributes in rendered Lava output.
- Validate assumptions about raw attribute values.

### Communications

Workflows commonly send emails and SMS. They may also create communication records, group communications, or connection requests that later generate communications. Event CTA and helper workflow recipes use communications as follow-up mechanisms ([Event Participant Call-To-Action Using a Workflow Form](https://community.rockrms.com/recipes/445), [Helper Workflow Starter Pack](https://community.rockrms.com/recipes/258)).

Agent checks:

- Which action sends the communication?
- Which template or Lava content is used?
- Who is recipient: submitter, assigned worker, group members, connection connector, requester?
- Does the recipient field use Person, PersonAlias, email text, phone text, or group?
- Are unsubscribe/SMS compliance rules respected?
- Are failures logged?
- Does the workflow continue if send fails?
- Are communications duplicated on reprocessing?

### Connections

Connection requests pair well with workflows because they create staff-owned follow-up queues. Community examples include call-to-action forms creating connection requests and non-cash contribution workflows using connection types as part of the process ([Event Participant Call-To-Action Using a Workflow Form](https://community.rockrms.com/recipes/445), [Non-Cash Contribution Workflow](https://community.rockrms.com/recipes/253)).

Use connections when:

- A person needs follow-up by a connector.
- Status and activity history matter.
- Staff need queues and dashboards.
- The process may outlive the initial workflow.
- Multiple staff roles are involved.

Do not keep all follow-up solely in workflow instances if Rock's connection system is the better operational home.

### Groups And Group Member Attributes

Workflows can add people to groups, set group member attributes, or use group data for assignment. A topic-assignment recipe recommends using a group with group member attributes to map topics to responsible workers so staff assignments can change without workflow edits ([Workflow Assignment by Topic](https://community.rockrms.com/recipes/164)). Helper workflow examples include adding people to groups with member attributes ([Helper Workflow Starter Pack](https://community.rockrms.com/recipes/258)).

Agent checks:

- Group type.
- Group role.
- Group member status.
- Duplicate group member behavior.
- Group member attributes.
- Whether inactive group members should be reactivated or duplicated.
- Security on group membership.
- Whether group membership is the correct long-term record.

## 11. Related Rock Areas: Lava, Jobs, Communications, Security, Attributes

### Lava

Lava appears in workflows as content, logic, activation, and integration glue. The dedicated workflow activation Lava command is documented separately from the workflow manual ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)). Source tests confirm it must be enabled and has explicit output when not configured ([WorkflowActivateTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Commands/WorkflowActivateTests.cs)).

Agent Lava search targets:

- Workflow action settings.
- Form pre/post HTML.
- Workflow templates.
- Communication templates.
- HTML Content blocks.
- Block pre/post HTML.
- Theme Lava files.
- Webhook handler templates.
- Dynamic Data blocks.
- Shortcodes.

### Jobs

Workflows that persist, wait, delay, or are launched by some integrations may depend on background jobs. The community Clearstream recipe specifically calls out that one launch path depends on the Rock Process Workflows job and therefore may not be immediate ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)). Health recipes also focus on active workflows that reprocess over time ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).

Agent job checks:

- Is Process Workflows enabled?
- When did it last run?
- Did it complete successfully?
- What is its schedule?
- Does the workflow type have many active instances?
- Are there error messages in job history or exception logs?
- Did a recent deployment disable jobs?
- Are long-running workflows causing repeated work?

### Communications

Workflow communications often look like email bugs when they are actually workflow state bugs. Verify:

- Communication action executed.
- Recipient attribute was populated before send.
- Person has email/SMS data.
- Communication medium is configured.
- Message was not suppressed by communication preferences.
- Workflow did not reprocess and send duplicates.
- Errors were not swallowed.

### Security

Security exists at multiple levels:

- Workflow Type security controls who can view, edit, launch, or manage workflows.
- Page security controls who can access Workflow Entry forms.
- Block security controls who can use configured blocks.
- Lava command enablement controls dangerous command execution.
- SQL-enabled blocks can expose data.
- Webhook endpoints must be protected.
- Person Entry can create or update person data.
- Form Builder may empower staff to create public forms.

The official docs note that workflow security is considered when building workflow lists in relevant settings ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). In practice, agents should verify the actual page, block, and workflow permissions because a secure workflow type can still be exposed through a misconfigured page, and a secure page can still launch a workflow from server-side triggers.

### Attributes

Attributes are both configuration and data. Workflow attributes are part of a larger Rock attribute system. When troubleshooting, distinguish:

- Workflow Type attributes.
- Workflow instance attribute values.
- Person attributes.
- Group attributes.
- Group member attributes.
- Connection request attributes.
- Registration attributes.
- Block attributes.
- System settings.

Community recipes often use attributes as local contracts: RawBody and WebhookResponse for webhooks, topic attributes for assignment, item fields for non-cash gifts, or person attributes for reporting ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473), [Workflow Assignment by Topic](https://community.rockrms.com/recipes/164), [Non-Cash Contribution Workflow](https://community.rockrms.com/recipes/253), [Finding People from Workflows](https://community.rockrms.com/recipes/437)).

## 12. Administration And Operational Guardrails

### Naming Standards

Use names that communicate owner, purpose, and lifecycle.

Recommended pattern:

- `Ministry - Process - Purpose`
- `Finance - Non-Cash Gift Intake`
- `Groups - Requirement Signature Request`
- `Care - Contact Us Routing`
- `System Helper - Create Connection Request`
- `Events - CTA Response - Spring Retreat 2026`

Avoid:

- `New Workflow`
- `Test`
- `Form`
- `Copy of Copy`
- Names tied to a staff person rather than a process.

For helper workflows, prefix clearly so they are not launched directly by staff.

### Change Management

Before editing a workflow:

1. Record Workflow Type Id and Guid.
2. Export or copy configuration if your instance supports it.
3. Screenshot or document attributes, activities, and actions.
4. Check active instances.
5. Check where the Workflow Type is used.
6. Identify external links and integrations.
7. Test changes in a sandbox.
8. Communicate expected behavior change.
9. Monitor active and new instances after deployment.

The official docs note a Change Log/Notes block was added to the Workflow Configuration page in version notes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). Use it if available. If not, maintain a local change log elsewhere.

### Where-Used Audits

A where-used audit should check:

- Workflow Entry blocks.
- Form Builder links.
- HTML Content blocks.
- Block pre/post HTML.
- Lava files.
- Workflow triggers.
- Connection type and opportunity triggers.
- Step type and program triggers.
- Group requirements.
- Grid actions.
- Webhook configuration.
- External tools.
- Communications linking to form pages.
- QR codes and printed materials.

The community Workflow Finder recipe provides a useful pattern by checking page blocks, `workflowactivate` Lava, general workflow triggers, connection triggers, and step triggers ([Workflow Finder](https://community.rockrms.com/recipes/457)). Treat its list as a starting point, not an exhaustive guarantee.

### Active Workflow Hygiene

Monitor:

- Count of active workflows by type.
- Count of completed workflows by type.
- Count by status.
- Oldest active instance.
- Active instances modified by former staff.
- Error counts.
- Workflows reprocessing for weeks or months.
- Process Workflows job health.

The Track Workflow Statistics and Health recipe describes adding statistics to the Workflow Configuration page and creating a broader active workflow health page ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)). Even if you do not implement that recipe, use the same operational questions.

### Maximum Age And Auto-Completion

Rock 13 version notes mention a Maximum Workflow Age setting that can automatically complete workflows older than a configured number of days ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). Use cautiously.

Before setting maximum age:

- Confirm old active workflows are safe to complete.
- Determine whether completion should send communications or merely mark complete.
- Exclude workflows that represent long-term cases if needed.
- Report counts before and after.
- Verify no active integrations depend on those workflow instances.

### Error Handling

Every production workflow should have an error posture:

- What happens if a required attribute is blank?
- What happens if a person cannot be found?
- What happens if a webhook payload is malformed?
- What happens if a communication fails?
- What happens if a duplicate record exists?
- What happens if an external system is down?
- Who is notified?
- Is the workflow completed, suspended, or left active?
- Is the error visible on a dashboard?

Use explicit Log Error or error notification actions when available in your version. The workflow manual's version notes mention Log Error as an action added in earlier Rock versions ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

### Public Form Guardrails

For external workflow forms:

- Use only necessary fields.
- Protect against spam.
- Avoid exposing internal IDs.
- Use GUIDs or slugs in URLs where available.
- Confirm page security.
- Confirm CAPTCHA or equivalent if appropriate.
- Confirm Person Entry does not create bad duplicate data.
- Confirm completion text does not reveal private information.
- Confirm uploaded files are restricted by type and size.
- Confirm form URLs in communications point to the correct site.

Rock 18.1 version notes mention Form Builder link sharing with a link icon, block setting, and slug field ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)). In versions with slugs, prefer stable friendly URLs over exposing implementation details, but still verify routing and security.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Lava Command Source

`WorkflowActivateBlock.cs` is the main source landmark for the `workflowactivate` Lava command ([WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs)). It describes use cases:

- Start a new workflow.
- Activate an activity in an existing workflow.
- Pass workflow or activity attribute values.
- Reactivate an existing waiting workflow.

The integration test file validates important behavior, including command enablement and workflow creation ([WorkflowActivateTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Commands/WorkflowActivateTests.cs)).

### Deprecated Activate Workflow Block

The WebForms `Activate Workflow` block is marked deprecated in source. Its description says the Workflow Entry block now supports the same functionality, and source notification text says administrators should update links to point directly to Workflow Entry pages ([ActivateWorkflow.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)). If a live instance still uses this block, plan migration.

### Person Entry Source

Key source landmarks:

- `WorkflowActionFormPersonEntryOption` enum: Hide, Optional, Required ([C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Workflow/WorkflowActionFormPersonEntryOption.cs), [TypeScript](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Workflow/workflowActionFormPersonEntryOption.ts)).
- `WorkflowActionFormAllowPersonEntry` migration: adds many Person Entry fields to `WorkflowActionForm` ([migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs)).
- Gender option migration: adds gender option field ([migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011171742444_WorkflowActionFormPersonEntryGenderOption.cs)).
- SMS opt-in migration: adds `PersonEntrySmsOptInEntryOption` ([migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2016.0/Version%201.16.0/202308242352371_WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs)).
- `FormPersonEntrySettings`: server-side settings class with an internal API warning ([FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs)).
- `FormPersonEntryViewModel`: Form Builder view model for Person Entry settings ([FormPersonEntryViewModel.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/WorkFlow/FormBuilder/FormPersonEntryViewModel.cs)).
- Obsidian bags: client-facing configuration and submitted values ([personEntryConfigurationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryConfigurationBag.d.ts), [personEntryValuesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryValuesBag.d.ts)).
- Processor tests: verify matching and attribute outcomes for logged-in person and spouse scenarios ([WorkflowPersonEntryProcessorTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Workflow/WorkflowPersonEntryProcessorTests.cs)).

### API And Data Access

For API work, verify the installed Rock REST endpoints and security. The source pack does not include complete endpoint documentation for workflow REST APIs, so do not invent endpoint behavior. Inspect in a live instance:

- `/api/WorkflowTypes` availability and permissions.
- `/api/Workflows` availability and permissions.
- Attribute value endpoints or entity attribute loading behavior.
- Whether Obsidian block APIs are used for Form Builder or Workflow Entry in your version.
- Whether custom plugins expose workflow endpoints.
- API user permissions.

Use Rock's REST/API documentation and v2 API patterns for authentication/authorization expectations, but treat workflow-specific endpoint shape as live-instance evidence until verified ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns)).

When in doubt, use read-only API calls first and compare returned fields to the live UI.

### Internal API Warning

`FormPersonEntrySettings` is marked as an internal API not subject to public compatibility guarantees ([FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs)). Plugin developers should avoid depending on internal classes unless they accept upgrade risk. Prefer public APIs, documented configuration, or stable entity models where available.

## 14. Reporting, Analytics, And Model Map

### What To Report

Workflow reporting should answer operational questions:

- How many workflows were started by type?
- How many are active?
- How many completed?
- How many errored?
- How old are active workflows?
- Which statuses are most common?
- Which staff member owns or last modified active work?
- Which form submissions include people who need communication?
- Which launch path created the workflow?
- Which external payloads failed parsing?
- Which workflows are stuck waiting on signatures or approvals?

Community recipes illustrate three reporting needs:

- Workflow health and statistics by status and active/completed counts ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).
- Finding people attached to workflow attributes so staff can view profiles or communicate with submitters ([Finding People from Workflows](https://community.rockrms.com/recipes/437)).
- Displaying workflow attribute keys for administrators without editing every attribute ([View Workflow Attributes Without Editing Workflow](https://community.rockrms.com/recipes/203)).

### Model Map Use

The Model Map confirms workflow form-related models in the Workflow category:

- [Workflow Action Form](https://community.rockrms.com/ModelMap)
- [Workflow Action Form Attribute](https://community.rockrms.com/ModelMap)
- [Workflow Action Form Section](https://community.rockrms.com/ModelMap)

Use these model names to orient schema exploration. For exact fields, inspect your installed database schema or Rock source for your version.

### Reporting Caveats

Workflow reporting is often hard because important values are stored as attributes. Field types can store raw values differently:

- Person fields may store Person Alias GUIDs.
- Multi-select fields may store delimited values.
- Entity fields may store GUIDs or IDs depending on field type.
- File fields may store binary file GUIDs or IDs.
- Defined value fields may store GUIDs.
- Text fields may contain JSON, HTML, or comments.

Community reporting examples for workflows reinforce this risk: useful reports often need workflow attributes, person links, active/completed state, and health status, not just the Workflow row itself ([Finding People from Workflows](https://community.rockrms.com/recipes/437), [Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).

Before writing a report, inspect a sample of actual `AttributeValue` raw values for the Workflow Type. Do not assume the formatted value in the UI matches the raw value needed for joins.

### Health Metrics

Recommended metrics:

- Active workflow count by Workflow Type and status.
- Completed workflow count by Workflow Type and status.
- Active workflows older than 7, 30, 90, and 365 days.
- Active workflows with last processed or modified date older than threshold.
- Workflows with error status or exception text.
- Workflow Types with no starts in the last year.
- Workflow Types with active instances but no current launch path.
- Workflow Types launched by public pages.
- Workflow Types using SQL-enabled Lava or webhook endpoints.
- Workflow Types with deprecated Activate Workflow block usage.

The workflow health recipe is a community implementation pattern for active/completed counts and dashboard-style monitoring; use it as a checklist idea, then verify against live workflow types, statuses, launch paths, and Process Workflows job behavior ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257), [Persisted Workflows](https://community.rockrms.com/rocku/workflows/persisted-workflows)).

## 15. Version And Release Caveats

Version matters. The official workflow manual includes update notes across Rock versions and should be checked for the installed version before making assumptions ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

Known caveats from source pack:

- Rock 2.0 docs added workflow actions such as Delay, Add/Remove Person to/from Organization Tag, Background Check Request, and Log Error in the manual's version notes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).
- Rock 3.0 docs added a Persist Immediately option on Persist Workflow in the manual's version notes ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).
- Rock 12-related source migrations added Person Entry fields to `WorkflowActionForm`, including spouse, email, mobile phone, birthdate, address, marital status, and related person-entry settings ([WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs)).
- A later Rock 12 migration added gender option support for Person Entry ([WorkflowActionFormPersonEntryGenderOption.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011171742444_WorkflowActionFormPersonEntryGenderOption.cs)).
- Rock 13 documentation notes a Maximum Workflow Age setting and bulk delete ability from Workflow List ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).
- Rock 16 source migration added SMS opt-in entry option to workflow entry form Person Entry ([WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2016.0/Version%201.16.0/202308242352371_WorkflowEntryForm-PersonEntrySmsOptInEntryOption.cs)).
- A v16.7 spotlight notes inactive campus filtering for workflow form Person Entry ([GitHub Spotlight: 10/18/2024](https://www.triumph.tech/resources/github-spotlight-10182024)).
- RockU marks Text to Workflow modules as legacy and says Text to Workflow functionality has been replaced by SMS Pipeline features ([Text to Workflow](https://community.rockrms.com/rocku/workflows/text-to-workflow), [Text to Workflow Performance](https://community.rockrms.com/rocku/workflows/text-to-workflow-performance)).
- Rock 18.1 documentation notes Form Builder link sharing improvements with a link icon, block setting, and slug field ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).
- The Activate Workflow block is deprecated in source and should be replaced by direct Workflow Entry block usage ([ActivateWorkflow.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)).

For any version-sensitive task, inspect:

- Rock version.
- Installed migrations.
- Block type in use: WebForms vs Obsidian where applicable.
- Form Builder feature availability.
- Person Entry field availability.
- Workflow action component availability.
- Release notes between source version and production version.

## 16. Implementation Playbooks

### Playbook: Build A Public Intake Workflow

1. Define the outcome: request, connection, group add, communication, or record update.
2. Create a Workflow Type with a clear name and owner.
3. Add workflow attributes for submitted values and internal state.
4. Add a Start activity.
5. Add a form action.
6. Enable Person Entry if the submitter must be matched or created.
7. Configure required fields.
8. Add routing action or Lava if needed.
9. Add follow-up action: communication, connection request, group add, or staff assignment.
10. Add completion action.
11. Create external Workflow Entry page.
12. Configure page route and block settings.
13. Set page and workflow security.
14. Submit test as anonymous user and logged-in user.
15. Verify workflow attributes, person matching, communication, and completion.
16. Add monitoring report or saved filter for active submissions.

Base this playbook on Workflow Entry, Form Builder, and Person Entry training, then verify public page security and duplicate-handling behavior in the target version ([Workflow Entry](https://community.rockrms.com/rocku/workflows/workflow-entry), [Form Builder](https://community.rockrms.com/rocku/workflows/form-builder), [Workflow Person Entry](https://community.rockrms.com/rocku/workflows/workflow-person-entry)).

### Playbook: Add A Workflow To A Grid

1. Identify the grid and entity type.
2. Confirm selected rows pass the expected identifier.
3. Create or copy a workflow template that accepts the row context.
4. Add an attribute for the incoming entity or Person Alias.
5. Use Lava or actions to resolve the actual person or record.
6. Add guardrails for missing or unsupported row types.
7. Add the grid action.
8. Restrict security.
9. Test one row.
10. Test multiple rows if bulk launch is enabled.
11. Verify duplicate behavior.
12. Monitor active workflows after launch.

Use RockU grid modules and community grid-launch patterns as reference points ([Custom Grid Actions](https://community.rockrms.com/rocku/workflows/custom-grid-actions), [Launch Workflow From Grid](https://community.rockrms.com/rocku/workflows/launch-workflow-from-grid), [Launching a workflow from a Grid](https://community.rockrms.com/recipes/300)).

### Playbook: Create A Helper Workflow

1. Name it with a helper prefix.
2. Define one responsibility.
3. Add only input attributes required for that task.
4. Add an output status or result attribute if parent workflows need it.
5. Make it complete deterministically.
6. Add error logging.
7. Test it directly with known values.
8. Call it from parent workflows using `workflowactivate` or an appropriate action.
9. Pass attributes using stable keys.
10. Monitor volume if called inside loops.

Reference helper workflow patterns from the community starter pack ([Helper Workflow Starter Pack](https://community.rockrms.com/recipes/258)).

### Playbook: Replace Deprecated Activate Workflow Block

1. Search pages for Activate Workflow block usage.
2. Record linked Workflow Entry page.
3. Confirm query string parameters currently passed.
4. Configure Workflow Entry block to accept the same workflow and attributes.
5. Update links to point directly to the Workflow Entry page.
6. Test all old link patterns.
7. Remove deprecated block after verification.
8. Monitor administrator notifications.

Source confirms this block is deprecated and that Workflow Entry now supports the key behavior ([ActivateWorkflow.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)).

### Playbook: Build Webhook-To-Workflow

1. Define external payload schema.
2. Create Workflow Type.
3. Add RawBody text attribute.
4. Add parsed field attributes.
5. Add response attribute if handler supports it.
6. Configure webhook endpoint.
7. Add authentication or shared secret validation if available.
8. Add Lava parsing and validation.
9. Add duplicate detection.
10. Add success and failure response behavior.
11. Test with a known payload.
12. Test malformed payload.
13. Test duplicate payload.
14. Monitor exceptions and active workflows.

Use webhook examples as patterns, but verify exact handler behavior in the live Rock version ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473), [Send Workflow Info To Zapier](https://community.rockrms.com/recipes/211)).

### Playbook: Audit A Workflow Before Editing

1. Record Workflow Type Id and Guid.
2. List active workflows by status and age.
3. List attributes and keys.
4. List activities and actions.
5. List forms and Person Entry settings.
6. Search where used.
7. Check triggers.
8. Check pages and blocks.
9. Check Lava `workflowactivate`.
10. Check webhooks.
11. Check connection, step, group, and requirement references.
12. Check communications and QR/printed links.
13. Check job dependency.
14. Make change in test first.
15. Verify new and existing instances.

Use the Workflow Finder recipe as the audit-category prompt for where-used review, and pair it with persisted-workflow health checks before changing active production processes ([Workflow Finder](https://community.rockrms.com/recipes/457), [Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).

## 17. Troubleshooting Decision Tree

### Workflow Did Not Start

Check launch path.

- If page form: inspect Workflow Entry block settings, page security, Workflow Type security, route, required parameters, and validation.
- If entity trigger: inspect Workflow Triggers, entity type, trigger type, active state, and whether the entity change actually occurred.
- If Lava: confirm `workflowactivate` command is enabled and the Workflow Type ID/GUID is valid. Source tests show disabled command returns a configuration error ([WorkflowActivateTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Commands/WorkflowActivateTests.cs)).
- If webhook: inspect endpoint, authentication, payload, raw body attribute, and exception logs.
- If grid: confirm the grid action is configured and passes expected entity data.
- If connection/step/group requirement: inspect that subsystem's trigger configuration.

### Workflow Started But Form Did Not Show

Check:

- Workflow Entry block points to correct Workflow Type.
- Start activity includes a form action.
- The form action is active.
- Action conditions allow it to execute.
- Workflow did not immediately complete before rendering.
- Required query string values are present.
- Page security allows access.
- Person Entry configuration is not hiding everything unexpectedly.
- Form fields have valid attributes.

### Form Submission Fails

Check:

- Required fields.
- Hidden conditional required fields.
- Person Entry required fields.
- Invalid campus or inactive campus selection.
- File type and size limits.
- Validation messages.
- Exception log.
- Whether the workflow action has already completed and cannot accept another submission.
- Whether the user is authenticated if required.

### Person Entry Creates Duplicates

Check:

- Autofill current person setting.
- Hide-if-current-person-known setting.
- Matching fields available: name, email, phone, birthdate.
- Whether anonymous submissions lack enough identifiers.
- Record status and connection status for new people.
- Person and spouse attribute configuration.
- Test behavior with logged-in and anonymous users.
- Processor behavior in your version. Source tests show Person Entry has explicit logic for logged-in person and spouse scenarios ([WorkflowPersonEntryProcessorTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Workflow/WorkflowPersonEntryProcessorTests.cs)).

### Workflow Is Stuck Active

Check:

- Current status.
- Active activities.
- Last action executed.
- Waiting or delay actions.
- Persist Workflow usage.
- Process Workflows job.
- Old errors.
- Missing completion action.
- Branch conditions that never match.
- External signature or approval dependency.
- Maximum age setting.

Community health patterns focus specifically on active workflows that never complete and continue reprocessing ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).

### Workflow Sends Duplicate Communications

Check:

- Workflow reprocessing.
- Communication action inside a repeatedly activated activity.
- Missing completion after send.
- Retry behavior.
- Multiple triggers.
- Multiple form submissions.
- Helper workflow launched in loop.
- Attribute flag that should mark "sent" but is not set.
- Parent workflow and child workflow both sending.

### Workflow Does Not Send Communication

Check:

- Recipient attribute populated before send action.
- Recipient is correct raw value type.
- Communication medium configured.
- Person has valid email or phone.
- SMS opt-in where required.
- Send action condition.
- Exception log.
- Communication history.
- Whether workflow completed before send action.

### Webhook Workflow Is Slow

Check:

- Whether launch path depends on Process Workflows job.
- Job schedule.
- Payload parsing cost.
- External calls inside workflow.
- Workflow persistence.
- Volume and rate.
- Whether an immediate webhook path is available and safe. Community Clearstream guidance was motivated by job-dependent launch delay ([Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473)).

### Workflow Attribute Value Looks Wrong

Check:

- Attribute field type.
- Raw value versus formatted value.
- Whether form stores GUID, ID, text, or delimited list.
- Whether a Lava action overwrote it.
- Whether query string set initial value.
- Whether helper workflow parameter key matches.
- Whether attribute key was renamed.
- Whether multiple attributes have similar names.

### Form Builder Staff Cannot Find The Form Link

Check:

- Rock version and Form Builder link-sharing features.
- Page route for form entry.
- Workflow Entry page.
- Form Builder page helper links.
- Slug configuration if available.
- Security.
- Whether the form is active.

Community examples show staff may need explicit preview and copy-link helpers because Form Builder forms are backed by workflows ([Form Builder - Helpful Links](https://community.rockrms.com/recipes/347)). Rock 18.1 adds official link-sharing improvements ([Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12)).

## 18. Agent Task Recipes

### Recipe: Find Every Launch Path For A Workflow Type

Inputs:

- Workflow Type Id.
- Workflow Type Guid.
- Workflow Type name.

Inspect:

1. Workflow Entry blocks.
2. Form Builder references.
3. HTML Content blocks.
4. Block pre/post HTML.
5. Lava files and shortcodes.
6. `workflowactivate` usage.
7. Workflow Triggers.
8. Connection Type and Opportunity triggers.
9. Step Type and Program triggers.
10. Group Requirements.
11. Grid actions.
12. Webhook configuration.
13. External tools and documented URLs.
14. Communications containing entry links.

Use the Workflow Finder recipe as a pattern for categories to search ([Workflow Finder](https://community.rockrms.com/recipes/457)).

### Recipe: Explain A Workflow To A Staff Owner

Deliver:

- Purpose.
- Who can start it.
- Where it starts.
- What information it collects.
- Who it assigns.
- What records it creates or changes.
- What communications it sends.
- How it completes.
- What can go wrong.
- Where staff can report on it.

Avoid describing internal actions unless they affect staff behavior.

### Recipe: Diagnose A Missing Submission

1. Ask for submitter, time, form URL, and expected workflow.
2. Check whether a Workflow instance exists near that time.
3. If none, check page access, trigger, webhook, or Lava launch path.
4. If instance exists, inspect attributes.
5. Check Person Entry match/create behavior.
6. Check active activities and errors.
7. Check communications or downstream records.
8. Determine whether the issue is launch, form submit, processing, integration, or reporting.

### Recipe: Safely Retire A Workflow

1. Confirm no current launch paths.
2. Remove public links or redirect pages.
3. Disable triggers.
4. Remove grid actions.
5. Disable webhooks.
6. Stop external tools from posting.
7. Let active workflows complete or bulk-complete according to policy.
8. Preserve historical data as needed.
9. Mark Workflow Type inactive or move to archive category.
10. Document replacement.

### Recipe: Build A Workflow Health Dashboard

Include:

- Active by Workflow Type.
- Active by status.
- Completed by status.
- Old active instances.
- Error counts.
- Last Process Workflows job result.
- Workflow Types with high active counts.
- Workflow Types with no recent activity.
- Public workflow forms.

The Track Workflow Statistics and Health recipe shows one community approach using Dynamic Data blocks and a broader health page ([Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257)).

### Recipe: Validate Person Entry Configuration

1. Open the workflow form action.
2. Confirm Person Entry enabled.
3. Record field visibility for spouse, gender, email, phone, SMS opt-in, birthdate, address, marital status, race, ethnicity, and campus where available.
4. Confirm campus inactive filtering.
5. Confirm new person record and connection statuses.
6. Confirm Person and Spouse workflow attributes.
7. Test anonymous submission.
8. Test logged-in person submission.
9. Test logged-in spouse/family scenario if relevant.
10. Inspect resulting Person, PersonAlias, and workflow attribute values.

Use source fields as a checklist, but verify installed UI because fields vary by version ([FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs), [personEntryConfigurationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryConfigurationBag.d.ts)).

### Recipe: Audit `workflowactivate` Lava

Search for:

- `workflowactivate`
- Workflow Type Id.
- Workflow Type Guid.
- Attribute keys passed as parameters.
- Activity Type Id or Guid.

For each usage:

- Confirm the command is enabled in that context.
- Confirm IDs or GUIDs still refer to the intended workflow.
- Confirm passed attributes still exist.
- Confirm loops are bounded.
- Confirm error output is handled.
- Confirm user input is sanitized.

Official Lava docs and source both describe the command's parameters and exposed variables ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands), [WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `1340`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | configuration | Connection Types are high-level containers for related connection opportunities; they should match ministry process boundaries rather than arbitrary reporting groupings. | [source](https://community.rockrms.com/rocku/engagement/connections-types) |
| rocku-confirmed | configuration | Rapid Attendance Entry is configurable enough to support multiple page variants, so teams can create focused versions for different ministry workflows instead of using one catch-all setup everywhere. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | configuration | Connection Opportunities define the specific follow-up paths available inside a connection type; changing an opportunity can affect request routing, staff ownership, and reporting. | [source](https://community.rockrms.com/rocku/engagement/connections-opportunities) |
| rocku-confirmed | implementation_pattern | For list discrepancies, compare the list filters, connection type/opportunity, status, assignee, campus, and current user security against the expected request set. | [source](https://community.rockrms.com/rocku/engagement/connections-list-1) |
| rocku-confirmed | implementation_pattern | When a connection request appears missing from a board, inspect opportunity filters, status, campus or connector assignment, and security before changing the request itself. | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| rocku-confirmed | implementation_pattern | Before restructuring connection types, review existing opportunities, request history, workflows, security, and staff ownership because type changes can alter process visibility and reporting. | [source](https://community.rockrms.com/rocku/engagement/connections-types) |
| rocku-confirmed | implementation_pattern | Before changing a workflow form, inspect which actions consume the submitted values and whether staff, public users, or workflow logic can see sensitive fields. | [source](https://community.rockrms.com/rocku/workflows/form-builder) |
| rocku-confirmed | implementation_pattern | Agents should inspect connection types, opportunities, statuses, activities, workflows, and staff ownership together because a connection request is both a person record and a process state. | [source](https://community.rockrms.com/rocku/engagement/overview) |
| rocku-confirmed | implementation_pattern | Form Builder should be used to collect structured workflow input intentionally: name each field by its downstream purpose, validation needs, visibility, and storage sensitivity. | [source](https://community.rockrms.com/rocku/workflows/form-builder) |
| rocku-confirmed | implementation_pattern | When troubleshooting connections, identify whether the problem is person context, request status, opportunity configuration, staff assignment, or automation rather than treating it as one generic workflow issue. | [source](https://community.rockrms.com/rocku/engagement/connections-overview) |
| rocku-confirmed | implementation_pattern | Before adding or retiring a connection opportunity, inspect active requests, workflows, staff roles, connector assignments, and reporting dependencies. | [source](https://community.rockrms.com/rocku/engagement/connections-opportunities) |
| rocku-confirmed | operational_guidance | Connections Board should be treated as a staff work queue for connection requests; board behavior depends on request status, opportunity, assignment, and follow-up ownership. | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| More |  | 1328 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `78`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Assign Statement Transcript Insight](https://community.rockrms.com/rocku/lava/assign-statement) | approved_for_public_distillation | 1 | media-insight:446c751591a992b1 |
| [Attendance Analytics Transcript Insight](https://community.rockrms.com/rocku/check-in/attendance-analytics) | approved_for_public_distillation | 3 | media-insight:e066ef3153b2cc3d |
| [Automations Transcript Insight](https://community.rockrms.com/rocku/core-concepts/automations) | approved_for_public_distillation | 3 | media-insight:7f62014ede8ae0e5 |
| [BI Financial Transaction Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report) | approved_for_public_distillation | 3 | media-insight:a815728575995f92 |
| [BI Job Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-job) | approved_for_public_distillation | 2 | media-insight:1783ed2aacc57cc3 |
| [BI Template Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template) | approved_for_public_distillation | 3 | media-insight:22fb0ca5319b94a9 |
| [Businesses Transcript Insight](https://community.rockrms.com/rocku/finance/businesses) | approved_for_public_distillation | 3 | media-insight:f84cdc67d1626107 |
| [Calendar Overview Transcript Insight](https://community.rockrms.com/rocku/event-registration/calendar-overview) | approved_for_public_distillation | 1 | media-insight:b7cb6e0f0354451c |
| More |  | 70 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

Primary sources:

- [Blasting Off With Workflows](https://community.rockrms.com/documentation/BookContent/12): official workflow manual, configuration concepts, version notes, triggers, forms, Person Entry, and administrative guidance.
- [RockU Workflows](https://community.rockrms.com/rocku/workflows): training map covering workflow concepts, components, entry, persistence, performance, styling, sample workflows, legacy text-to-workflow, grid actions, Person Entry, electronic signatures, and Form Builder.
- [Workflow Activate Lava command](https://community.rockrms.com/lava/commands/workflow-activate-commands): official Lava command documentation for launching workflows and activities.
- [WorkflowActivateBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WorkflowActivateBlock.cs): source behavior for the Lava command.
- [WorkflowActivateTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Commands/WorkflowActivateTests.cs): integration tests for command enablement and activation behavior.
- [ActivateWorkflow.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs): source evidence that the Activate Workflow block is deprecated.
- [WorkflowActionFormAllowPersonEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.0/202011052358368_WorkflowActionFormAllowPersonEntry.cs): migration evidence for Person Entry configuration fields.
- [WorkflowActionFormPersonEntryOption.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Workflow/WorkflowActionFormPersonEntryOption.cs): enum values for Person Entry visibility requirements.
- [FormPersonEntrySettings.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/FormBuilder/FormPersonEntrySettings.cs): Form Builder Person Entry settings and internal API warning.
- [FormPersonEntryViewModel.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/WorkFlow/FormBuilder/FormPersonEntryViewModel.cs): view model for Form Builder Person Entry settings.
- [personEntryConfigurationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryConfigurationBag.d.ts): Obsidian client configuration shape for Person Entry.
- [personEntryValuesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Workflow/personEntryValuesBag.d.ts): submitted values shape for Person Entry.
- [WorkflowPersonEntryProcessorTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Workflow/WorkflowPersonEntryProcessorTests.cs): processor behavior tests for logged-in person and spouse scenarios.
- [Model Map](https://community.rockrms.com/ModelMap): model-category confirmation for workflow form models.

Community examples used as patterns:

- [Workflow Finder](https://community.rockrms.com/recipes/457): where-used audit categories.
- [Track Workflow Statistics and Health](https://community.rockrms.com/recipes/257): operational health dashboard pattern.
- [Event Participant Call-To-Action Using a Workflow Form](https://community.rockrms.com/recipes/445): event CTA workflow pattern.
- [Modal Dialog for Workflow Entry](https://community.rockrms.com/recipes/141): iframe/modal entry pattern and allowed frame domain caveat.
- [Workflow Assignment by Topic](https://community.rockrms.com/recipes/164): group/member-attribute assignment pattern.
- [Clearstream - Launch Rock Workflows Instantly With Webhooks](https://community.rockrms.com/recipes/473): immediate webhook launch pattern.
- [Finding People from Workflows](https://community.rockrms.com/recipes/437): reporting on person attributes in workflow submissions.
- [Create Multiple Sign-Up Opportunities From Schedule](https://community.rockrms.com/recipes/479): loop and bulk creation pattern.
- [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482): group requirement and signature document helper pattern.
- [View Workflow Attributes Without Editing Workflow](https://community.rockrms.com/recipes/203): administrator attribute-key visibility pattern.
- [Launching a workflow from a Grid](https://community.rockrms.com/recipes/300): grid launch context pattern.
- [Form Builder - Helpful Links](https://community.rockrms.com/recipes/347): staff usability pattern for Form Builder links.
- [Send Workflow Info To Zapier](https://community.rockrms.com/recipes/211): outbound integration pattern.
- [Helper Workflow Starter Pack](https://community.rockrms.com/recipes/258): helper workflow pattern.
- [Non-Cash Contribution Workflow](https://community.rockrms.com/recipes/253): workflow plus connection process pattern.

Dependencies:

- **Lava** is required for dynamic workflow activation, template rendering, logic, loops, payload transformation, and many community patterns.
- **Jobs** are required for delayed, persisted, or scheduled workflow processing. Always inspect Process Workflows job health when active workflows are stuck or delayed.
- **Communications** are often downstream effects of workflow actions and should be audited separately for deliverability, duplication, and recipient correctness.
- **Security** must be checked at workflow, page, block, Lava command, webhook, and SQL-enabled block levels.
- **Attributes** are the workflow data contract. Every agent workflow audit should start by listing attribute keys and raw values.
- **Live Rock verification** is required for exact installed action components, schema columns, REST endpoints, block settings, trigger conditions, plugin behavior, and local launch paths.
