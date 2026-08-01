---
id: authored-workflows
title: Workflows
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "e45856216ee8b8edeba9d461f8a1889a55b05744e0d09efaaf7e5d3626ef5997"
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

## Agent Summary

Rock workflows coordinate structured processes: collect attributes, activate activities, execute ordered actions, assign responsibility, branch on conditions, communicate, and retain an inspectable workflow instance when persistence is needed. Treat the workflow type as the blueprint and each workflow instance as one process moving through that blueprint. [Official workflow overview](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-types)

For operational work, begin with the process rather than the requested screen or automation:

1. Restate the ministry problem and required outcome.
2. Identify the person or entity in context.
3. Define the process state, owner, next action, and completion condition.
4. Define attributes according to their stored formats and downstream consumers.
5. Select the least complex supported activation path.
6. Test permissions, branching, persistence, communications, retries, and final side effects.

A stakeholder’s proposed implementation is useful requirements evidence, but it should be compared with genuinely different approaches before construction. [Approved operational guidance](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=747s)

Use workflow forms for structured input, activities for stages or responsibility boundaries, actions for individual units of work, and workflow instances for operational state. Use Connections when the owning concept is a person-centered ministry follow-up process; use jobs when work must start on a schedule; and use webhooks or pipelines when an external event must initiate processing. [Official introduction](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/intro-to-workflows)

## Scope And Boundaries

This guide covers the workflow surfaces organized by Rock's
[official Workflows documentation](https://community.rockrms.com/documentation/core-concepts/workflows):

- Workflow types, attributes, activities, actions, instances, persistence, and assignment.
- Workflow activation from entry pages, URLs, person or entity contexts, grids, jobs, Lava, webhooks, SMS Pipeline, and adjacent Rock surfaces.
- Entry Forms, Form Builder, Person Entry, commands, conditional fields, and chained forms.
- Operational monitoring through workflow lists, details, logs, notes, and My Workflows.
- Connections as person-centered follow-up workflows.
- Evidence-supported examples involving attendance, preregistration, LMS completion, provider events, communications, and slow background work.

This guide does not define the full behavior of Lava, jobs, communications, security, attributes, Connections, registrations, check-in, or LMS. Those concepts own their detailed configuration. Here they are covered only where they initiate, supply data to, or receive work from a workflow.

Do not infer that an action, trigger, provider, plugin, schema element, or v19 feature is installed merely because it appears in documentation or source. Treat community contributions and recipes as reviewed implementation patterns, not official Rock behavior. Installation-specific conclusions belong under `Known Gaps And Live Verification`.

## Mental Model

A workflow type is a reusable process definition. Its attributes hold the data needed by the process; its activities represent stages of work; and its actions perform individual operations. Actions execute in configured order, so a write, assignment, communication, activation, or completion action placed earlier can affect everything that follows. [Workflow Types](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-types) and [Workflow Actions](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions)

A workflow instance is one execution of that definition. It has an initiator, status, attributes, activated activities, assignments, action completion state, and—when configured—logs and notes. An agent diagnosing an instance should inspect those layers separately rather than reducing the issue to “the workflow failed.” [Workflow instance management](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details)

Use these modeling boundaries:

- **Attribute:** data the process must collect, derive, retain, compare, or pass onward.
- **Activity:** a stage, responsibility boundary, waiting point, or branch target.
- **Action:** one ordered operation within an activity.
- **Form command:** a submission choice that can activate a particular workflow path.
- **Assignment:** the person or group responsible for an active activity.
- **Status:** human-readable workflow state; it does not replace action and activity state.
- **Persistence:** whether an instance should be retained and receive a stable database identity.
- **Trigger:** the event or interface that initiates or reprocesses a workflow.
- **Completion:** an explicit terminal state after required work and side effects have finished.

A single workflow can transfer responsibility without duplicating the entire process. For example, one activity can collect input, persist the instance, assign another activity, show a second form, and let approval or denial commands activate different terminal activities. [Define Workflow Activities](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities)

## Process Design Before Configuration

Define the process in operational language before opening Workflow Configuration:

- What real-world problem begins the process?
- What person or entity is the subject?
- What information is required at initiation, and what is derived later?
- Who owns each stage?
- Which outcomes are materially different branches?
- Which actions are reversible?
- Which actions can be retried safely?
- What constitutes completion?
- What must remain visible for audit or staff follow-up?
- Which sensitive values should not be retained or broadly exposed?

Then map the process to Rock components. Avoid using statuses for every checklist signal or duplicating whole workflows for every branch. Activities, assignments, action filters, commands, attributes, notes, and related Rock records may express the distinction more accurately. [Official activity pattern](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities)

Rock includes built-in workflows that can serve as patterns, and an existing workflow type can be copied. The built-in unattended check-in workflow carries an explicit warning against alteration unless the operator understands it. A clone is a starting point, not proof that its security, attributes, communications, or assumptions fit another process. [Built-In Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/built-in-workflows)

## Triggers And Activation

### Entry pages and direct links

`Tools > Workflows` can display configured workflow categories and launch a workflow’s first entry screen. Category and workflow security affect what the current person can see. A page containing the Workflow Entry block can launch a specific workflow type directly, allowing a public or internal page to present the process without exposing workflow terminology. [Launch a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow)

The Workflow Entry block can load an existing instance when a valid `WorkflowId` or `WorkflowGuid` is supplied. Otherwise it can create a new instance when the required workflow-type context is supplied, process it, and locate the first active form assigned to the current person. A command parameter can cause immediate form-command processing, so agents should treat command-bearing URLs as behavior-bearing inputs, not merely navigation. [Link to Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/link-to-workflows)

Query-string values can be passed into matching workflow attributes by supported workflow launch surfaces. Verify every parameter name, field type, stored-value format, and authorization boundary before using URL inputs as workflow data. [Launch from grids and routes](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow)

### Person, entity, and grid launches

A workflow can be exposed as an action from a person profile or launched for selected entities from a supported grid. The workflow must preserve the passed entity in an appropriate attribute if later actions need it. Workflow security still controls which workflow types a person can launch. [Launch a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow)

Entity triggers can launch workflows around saved or deleted records. Do not create a pre-save or immediate post-save loop in which the triggered workflow updates the same entity that is actively being saved. Confirm the trigger event, the entity passed to the workflow, and whether the workflow needs the entity to be saved before downstream processing. [Entity-trigger guidance](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow)

### Scheduled activation and background work

Rock jobs can initiate workflows on a schedule, making workflows suitable for background tasks. When the work is slow—such as rendering media or waiting for an external result—the workflow can own explicit states, retries, and completion checks instead of blocking the user interface. This orchestration pattern is community-reviewed rather than a guarantee about any particular renderer or provider. [Official background-task overview](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/intro-to-workflows) and [community-reviewed orchestration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)

A delayed or scheduled action must revalidate mutable prerequisites immediately before an irreversible effect. A reviewed community pattern for delayed payments, for example, calls for rechecking authorization, revocation, saved-account eligibility, cancellation state, and idempotency after the delay. This requires local validation before use. [Community workflow reference](https://community.rockrms.com/rocku/workflows)

### Lava `workflowactivate`

The Lava `workflowactivate` command can create a workflow, activate an activity in an existing workflow, or reprocess an existing suspended or waiting workflow. Its use depends on the Lava command being enabled for the template. The supplied immutable source shows that unrecognized command parameters are treated as potential workflow or activity attributes. [Official Lava command documentation](https://community.rockrms.com/lava/commands/workflow-activate-commands) and [immutable implementation excerpt](https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/Rock/Lava/Blocks/WorkflowActivateBlock.cs)

For `workflowactivate`, treat additional parameter names as an attribute-key contract:

- Match each parameter to the intended workflow or activity attribute key.
- Supply the value in that field type’s stored-value format.
- Remove parameters that no longer have a receiving attribute.
- Inspect the created instance before trusting downstream processing.

The approved command behavior is version-scoped from Rock v7.0, but the target installation and enabled-command configuration still require verification. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)

## Workflow Forms

### Entry Forms and Form actions

A Form action presents selected workflow or activity attributes to a person. Each field can independently be visible, editable, and required. Conditional logic can show or hide a field based on other field values. Each configured command submits the form and can activate a different workflow path, supporting choices such as approval and denial. [Understand Form Actions](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions)

Treat every field as structured process input. Before adding or changing it, document:

- Its downstream purpose.
- Its field type and stored-value format.
- Its validation and requiredness.
- Who can see or edit it.
- Whether it contains sensitive information.
- Which actions, filters, reports, or communications consume it.
- What happens when conditional logic omits it.

Do not judge downstream values by the field’s visible label. Action filters compare the attribute’s stored text representation, which can differ for Boolean, Person, single-select, Defined Value, and other field types. [Workflow action filters](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions)

### Chained forms and branching

A form command activates and processes the workflow. If processing assigns another active Form action to the current person, Rock can show that next form. Action filters can select the appropriate next form based on prior input. Persist the workflow once meaningful input should survive beyond the current interaction. [Chain Entry Forms](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/chain-entry-forms)

A Form action can notify the person assigned to the activity when it becomes active. It can also include commands in email, allowing a recipient to submit an approval or denial from the message. Verify recipient resolution, command security, and the resulting branch before using email actions operationally. [Define Workflow Activities](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities)

### Form Builder

Form Builder creates a workflow type. Its fields become workflow attributes, and each submission launches an instance of that type. The generated type begins with a Form Builder activity and action and can later be extended with additional workflow activities and actions. [Intro to the Form Builder](https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/intro-to-the-form-builder)

Person Entry can match submitted information to an existing person or create a person when needed, storing the result in a Person attribute. Its configuration includes autofill behavior, whether to hide known-person fields, record and connection status for newly created people, campus behavior, and selected person fields. Required data can cause Person Entry to remain visible even when the current person is known. [Create a Form](https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/create-a-form)

A Form Builder form also has submission review, communications, access dates, login requirements, completion behavior, analytics, and shareable-link settings. Analytics depend on the hosting Workflow Entry block logging form views and completions. Confirmation and notification communications depend on configured System Communications and their category. [Navigate the Form Builder](https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/navigate-the-form-builder)

Before editing a live form, inspect which actions consume its values and whether staff, public users, or workflow logic can see sensitive fields. This inspection path was structurally confirmed in a bounded read-only review, but no particular organization’s form configuration is implied. [Form Builder training](https://community.rockrms.com/rocku/workflows/form-builder)

### Person and family entry patterns

Requiredness must match the applicant context. A reviewed community pattern warns that self-applicants and family-member applicants may not have the same email or mobile data. Branch requiredness and communication-target validation instead of writing placeholder contact information. This is not official universal behavior and requires local testing. [Community workflow reference](https://community.rockrms.com/rocku/workflows)

For public family preregistration, community-reviewed guidance recommends testing the full path from public form through person and family record creation, check-in eligibility, and staff follow-up. The page should explain its value and avoid producing duplicate or partial records that staff must repair. Connect captured data to a defined Connection or workflow outcome. [Community-reviewed preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

## Activities, Actions, State, And Persistence

Actions are processed in order. Configure completion deliberately:

- An action normally completes when it succeeds.
- An action can complete its entire activity, preventing later actions in that activity from running.
- An action filter can limit execution based on attribute criteria.
- An activity can activate another activity or workflow.
- Explicit completion actions can end an activity or the entire workflow.

These behaviors make action order part of the process contract. [Workflow Actions](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions) and [Workflow Control](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/workflow-control)

Entry-form workflows are often initially non-persisted so merely opening and abandoning a form does not create a saved instance. A Persist action can retain the workflow after meaningful input. The `Persist Immediately` option is needed when a later action in the same processing sequence requires a saved workflow with a valid ID. [Configure Workflow Details](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/configure-workflow-details) and [Workflow Control](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/workflow-control)

Logging level determines the detail available on the instance log. Notes can be entered from workflow details, collected on forms, or created automatically by workflow actions. Use notes for human context and process history; use attributes for structured values that actions must reliably consume. [Workflow Notes](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/workflow-notes)

## Workflow Integrations

### Webhooks

Workflow webhooks are configured through Defined Values under the Workflow Webhook Defined Type. For each incoming request, Rock evaluates every configured Process Request Lava expression and launches every workflow whose expression evaluates to true. Matching rules must therefore be selective and mutually intentional. If no workflow matches, the documented endpoint returns a 404 as a security behavior. [Configure a Webhook to a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow)

Request information can be mapped into workflow attributes from values such as the URL, method, query string, raw body, headers, and cookies. Store the raw body when complex parsing is required and perform that parsing inside the workflow; the Defined Value template has practical Lava limitations. These webhook claims are official and source-backed but require live verification of the installed configuration. [Webhook documentation](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow)

Do not expose secrets in workflow names, attributes, logs, or troubleshooting output. Confirm authentication or request-validation requirements separately; the supplied evidence establishes routing and data mapping, not a universal webhook authentication design.

### SMS Pipeline

The SMS Pipeline can launch a workflow and map message context into workflow attributes by key. Workflow and pipeline attribute mappings must remain synchronized. Documentation notes that `FromPhone` is supplied automatically unless intentionally overridden and describes an Attribute Set to Initiator approach as a more flexible alternative in some workflows. [SMS Pipeline Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/sms-pipeline-workflows)

The older Text to Workflow configuration can continue to work, but the v19 documentation recommends SMS Pipeline for new work. In v19, an SMS Pipeline send action can optionally retain its response so the automated message appears in Communication History, person history, and SMS Conversations. Enable retention deliberately when auditability is needed and account for the extra retained history. [SMS Pipeline documentation](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/sms-pipeline-workflows) and [v19 release presentation](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=684s)

### Communications and provider events

Community-reviewed guidance recommends tying provider delivery and engagement events back to the Rock communication or person context that generated the message. Summarize events into operational reports that show delivery health without unnecessarily exposing raw provider data. This is an integration pattern, not proof that a given provider mapping is configured. [Community-reviewed provider-event example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5)

Rock v19 adds workflow actions for Rock Chat channel and direct messages. Confirm Rock Chat configuration, recipient resolution, workflow security, and actual delivery behavior before operational use. [v19 feature presentation](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1056s)

### Lava entity operations

In a Lava Entity command, values such as `where` must be enclosed in single quotes. If `id` is also supplied, Rock ignores `where`, `dataview`, and `dynamicparameters`. [Entity command documentation](https://community.rockrms.com/lava/commands/entity-commands)

Reviewed community patterns add several cautions that require reproduction in the target environment:

- Inspect the fully rendered Dynamic LINQ expression when a dynamic `where` clause fails.
- Check `ModifyResult.Success` after each write and stop dependent operations after failure.
- Capture the saved object’s canonical ID immediately and re-query before creating children.
- Isolate risky experiments because a failed tracked entity may affect later writes in the same render.
- Make configuration deploys idempotent and verify workflow attribute scope and action-setting IDs.

These are community observations, not official guarantees. [Lava Entity commands](https://community.rockrms.com/lava/commands/entity-commands)

## Managing Workflow Instances And Staff Work

The workflow-type management grid can filter instances by name, initiator, status, activation date, completion date, and active or completed state. Workflow details expose summary information, attributes, activities, assignments, action completion, notes, and—according to configured logging level—the log. [Viewing a Workflow Instance](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/viewing-a-workflow-instance)

`Tools > My Workflows` separates workflows initiated by the current person from active workflows assigned to that person. Assignment through a group counts when the person belongs to the assigned group. The Mini My Workflows block can filter categories and initiation or assignment relationships, and its markup can be customized with HTML and Lava. [My Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/my-workflows)

When intervening in a stuck instance, inspect before editing:

- Workflow state and status.
- Attribute values and stored formats.
- Activated and completed activities.
- Current person or group assignment.
- Action completion and last processing times.
- Action criteria.
- Workflow log and notes.
- Side effects that may already have succeeded.

Uncompleting an action can cause it to run again while its activity remains active. Before doing so, determine whether communications, group membership, connection changes, financial effects, or other writes are idempotent. [Edit Workflow Details](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details)

## Connections As Operational Workflows

Connections should be modeled as person-centered ministry follow-up. Define the person, Connection Type, Connection Opportunity, status, connector or assignee, next action, and completion outcome before adding automation or reports. Agents should inspect the person context and process state together. [Connections Overview](https://community.rockrms.com/rocku/engagement/connections-overview)

Connection Types are high-level containers for related opportunities and should represent ministry process boundaries rather than arbitrary reporting groupings. Opportunities define the specific follow-up paths inside a type. Before restructuring a type or adding, changing, or retiring an opportunity, inspect existing opportunities, active and historical requests, workflows, security, connector assignments, staff roles, ownership, and reporting dependencies. [Connection Types](https://community.rockrms.com/rocku/engagement/connections-types) and [Connection Opportunities](https://community.rockrms.com/rocku/engagement/connections-opportunities)

Use the Connections Board as a staff work queue whose visible cards depend on request status, opportunity, assignment or follow-up ownership, filters, campus, and security. Use Connections List when staff need tabular filtering and scanning across multiple requests instead of board-style movement. [Connections Board](https://community.rockrms.com/rocku/engagement/connections-board) and [Connections List](https://community.rockrms.com/rocku/engagement/connections-list-1)

Selected Rock v19 connection requests can be reassigned, moved to another status, completed, updated by state, sent to a workflow or activity, and used to initiate SMS or email. Templates, snippets, phone eligibility, and permissions still constrain these actions. [v19 Connections presentation](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=466s)

## Adjacent Operational Patterns

These patterns are evidence-supported examples, not universal configurations:

- **Rapid Attendance Entry:** Begins with a group and attendance date, with location and schedule available when supported by the group and attendance context. Configured page variants can combine attendance with family editing, new family members, notes, prayer requests, and workflow launches. Use focused variants for distinct ministry workflows rather than assuming one catch-all page. [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)
- **Event call-to-action:** A community recipe uses a workflow form reached through SMS, then routes selected responses into groups or Connection Opportunities. Evaluate its security, performance, imported references, and version assumptions before adaptation. [Community recipe](https://community.rockrms.com/recipes/445)
- **Registration-to-follow-up:** A reviewed public recipe resolves registrant and campus context, creates a native Connection Request, preserves source registration context, and verifies results without SQL writes. Its exact entities and references require target-instance validation. [Immutable community recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)
- **LMS follow-up:** Community-reviewed evidence shows LMS activities and completions can participate in group and workflow patterns for volunteer training. Training design must define learner actions and facilitator review responsibilities. [Community-reviewed LMS example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)
- **Anonymous SMS verification:** A reviewed recipe uses strict person matching, a bounded persisted challenge, server-side verification state, and final-session revalidation without exposing the matched alias to the browser. Treat this as a security-sensitive recipe requiring expert and live review. [Immutable community recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)

## Security And Governance

Workflow Types inherit security from their parent Category. Editing a workflow type requires appropriate access to Workflow Configuration and its detail block; category-level Edit access can permit management, cloning, or deletion of workflows within that category. Form Builder uses the same category structure, so category permissions also affect forms. [Secure Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/secure-workflows)

Different surfaces enforce different rights. Workflow navigation, Workflow Entry, Workflow List, Workflow Detail, and My Workflows have separate view, edit, assignment, active-form, and activity visibility conditions. Diagnose “missing workflow” reports against the specific surface instead of assuming a single permission controls all workflow access. [Secure Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/secure-workflows)

Triggered or job-run workflow Lava has no current person for authorization. The v19 Lava workflow documentation states that attribute access in that context requires `All Users - Allow View`. Do not respond by broadly exposing sensitive attributes without reviewing whether the design can use a safer value, different execution context, or narrower process. [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

Before importing or sharing a workflow, inspect the exported package. Official documentation warns that complex workflows may not export correctly and provides a Test Only import mode. Confirm categories, security, attributes, action components, communications, entity references, and plugin dependencies after import. [Workflow Import/Export](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/use-workflow-importexport)

## Version And Authority Caveats

The supplied official workflow documentation was hydrated against Rock v19.0. Confirm the installed Rock version before applying navigation paths, block settings, action options, or release-specific behavior.

Version-scoped items include:

- `workflowactivate` attribute parameters are documented from v7.0, but command enablement and target attributes require local verification. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)
- Selected connection-request bulk operations, Rock Chat workflow actions, and SMS Pipeline response retention are v19 features in the supplied release evidence. [Connections v19](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=466s) and [v19 enhancements](https://www.youtube.com/watch?v=c-wycR9HEuQ)
- The immutable `develop` source excerpt marks the legacy Activate Workflow block as deprecated in favor of Workflow Entry functionality. Source code describes that commit, not the installed block inventory. [Immutable source](https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)
- Self-hosted operators own their patch cadence. Supported dot releases may contain security fixes; confirm currently supported branches and current release notes before an upgrade. [Approved release guidance](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s)

Official documentation and approved official claims carry the most authority in this guide. RockU claims cited here were additionally supported by bounded, read-only structural reviews, but those reviews do not establish another installation’s configuration. Community-reviewed media, recipes, and contribution patterns are examples and must not be presented as core Rock guarantees.

## Troubleshooting Decision Tree

### A workflow or form is not visible

1. Identify the exact surface: Workflow navigation, direct Workflow Entry page, Workflow List, Workflow Detail, My Workflows, or Form Builder.
2. Confirm the workflow type is active and the expected category is selected in the block settings.
3. Check category and workflow-type View permissions.
4. For Workflow Entry, confirm there is an active Form action assigned to the current person and that the person can view the activity.
5. For My Workflows, confirm the activity is active, has an active form, is assigned appropriately, and the person can view it.
6. Verify login, form start/end dates, and share-link settings when using Form Builder.
7. Stop when visibility is explained; do not alter the workflow instance merely to force it onto a list. [Secure Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/secure-workflows)

### A form field is missing, unexpectedly required, or exposing data

1. Inspect the Form action or Form Builder field’s visible, editable, required, and conditional settings.
2. Check the applicant or current-person context, including Person Entry autofill and hide-if-known behavior.
3. Evaluate every conditional branch, including the case where a prior field is blank.
4. Inspect who can view the workflow, activity, form, and resulting attribute.
5. Trace downstream actions and communications that consume the field.
6. Compare the submitted stored value with the visible label.
7. Stop before changing requiredness if the communication or identity target remains ambiguous. [Understand Form Actions](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions)

### A workflow action was skipped

1. Inspect the action’s Run If criteria.
2. Read the actual submitted attribute value and its stored format.
3. Compare it with the criterion, including capitalization and Boolean text.
4. Confirm earlier actions ran in the expected order and did not change the value.
5. Determine whether `Complete Action If Criteria Unmet` marked it completed.
6. Inspect the workflow log.
7. If the form recently changed, compare current payload values with every downstream criterion. This final check is a community-reviewed troubleshooting pattern requiring local confirmation. [Workflow Actions](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions)

### A workflow is stuck or repeatedly processing

1. Inspect active activities, assignments, and action completion.
2. Find the first incomplete action in configured order.
3. Read its criteria, last processing time, and log entries.
4. Confirm whether it is intentionally configured to remain incomplete and rerun.
5. Check whether a completion action is missing after filtered branches.
6. Before uncompleting or retrying anything, inspect communications and data changes that may already have succeeded.
7. Stop if retrying could duplicate an irreversible effect. [Edit Workflow Details](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details)

### A webhook returns 404 or launches the wrong number of workflows

1. Confirm the request reached the documented webhook endpoint.
2. Enumerate every Workflow Webhook Defined Value.
3. Evaluate each Process Request Lava rule against the same request data.
4. Confirm exactly the intended rules return true.
5. Treat a no-match 404 as expected documented security behavior.
6. Store a bounded raw body in a test workflow when payload inspection is necessary.
7. Move complex parsing into the workflow rather than the Defined Value template.
8. Verify installed configuration before enabling the external sender. [Configure a Webhook to a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow)

### `workflowactivate` starts a workflow but values are blank

1. Confirm the Lava command is enabled.
2. Compare every extra parameter name with the target workflow or activity attribute key.
3. Confirm each value uses the field type’s stored-value format.
4. Inspect the created workflow and its attribute values.
5. Remove dead or misspelled parameters.
6. Verify Person-related values use the expected Person or PersonAlias representation for the receiving field.
7. Stop when the stored instance proves the contract; do not trust rendered success text alone. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)

### A connection request is missing from a board or list

1. Confirm the expected Connection Type and Opportunity.
2. Check current request status.
3. Check board or list filters.
4. Check connector or assignee ownership.
5. Check campus restrictions.
6. Check the current user’s security.
7. Compare the board with the tabular Connections List.
8. Inspect automation only after the request’s current person and process state are understood.
9. Do not change the request merely to make it visible. [Connections Board](https://community.rockrms.com/rocku/engagement/connections-board) and [Connections List](https://community.rockrms.com/rocku/engagement/connections-list-1)

### SQL or reporting cannot see a value just submitted by a form

1. Confirm the workflow has been persisted.
2. If the next action requires a valid workflow ID immediately, inspect the Persist action’s immediate-persistence setting.
3. Verify the attribute’s entity type, qualifier, workflow-type scope, and key.
4. Compare formatted and raw values.
5. Confirm the report or query reads the canonical attribute used by downstream actions.
6. Reproduce with a disposable test instance before modifying production logic.
7. Treat “persist before SQL reads submitted attributes” as a community pattern until reproduced locally. [Workflow Control](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/workflow-control)

### Lava output is blank or a parser error points at the wrong line

1. Inspect the workflow attribute’s field type and whether the template requested formatted, raw, or object output.
2. Verify the returned object shape before chaining properties.
3. Check preceding filters for an unclosed quote, missing delimiter, or incomplete argument.
4. Reduce nested conditional and assignment blocks into smaller independently previewable sections.
5. Test against a representative workflow instance.
6. Treat object-shape and downstream-error-line behavior as community troubleshooting observations requiring reproduction. [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

## Agent Task Recipes

### Recipe: Design a bounded workflow type

**Outcome:** A reviewable process model before configuration begins.

1. Restate the underlying ministry problem without naming the proposed screen or automation.
2. Generate at least three materially different approaches, including a non-workflow option when credible.
3. Select the workflow approach only if it adds useful state, assignment, branching, automation, or auditability.
4. Define the subject person or entity.
5. List initiation data, derived data, and retained data as attributes.
6. Define activities by responsibility or stage.
7. Define actions in execution order.
8. Define commands, branch criteria, completion, retries, and failure handling.
9. Define security and sensitive-data retention.
10. Define the launch surface and acceptance evidence.

**Do not assume:**

- A status is sufficient to represent every state.
- A visible label is the stored value.
- A successful final message proves every side effect.
- A documented action is installed.

**Stop when:** Each stage has an owner, entry condition, exit condition, and verified completion outcome. [Build a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow)

### Recipe: Review a workflow form change

**Outcome:** A field change that preserves validation, visibility, and downstream behavior.

1. Identify the workflow type, Form action, and attribute key.
2. Record the current field type and stored-value format.
3. Inspect visible, editable, required, and conditional settings.
4. Inspect Person Entry implications.
5. Find every action filter, Set Attribute action, communication, report, and integration that consumes the value.
6. Test every conditional branch, including omitted-field behavior.
7. Submit a disposable instance.
8. Inspect stored values and downstream outcomes.
9. Verify access as public user, staff user, assignee, and unauthorized user where applicable.

**Stop when:** The submitted value and every downstream consumer agree on the same contract. [Understand Form Actions](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions)

### Recipe: Configure a selective workflow webhook

**Outcome:** One intended request starts only the intended workflow with inspectable input.

1. Define a stable request discriminator.
2. Create or inspect the Workflow Webhook Defined Value.
3. Make Process Request Lava return true only for the intended request.
4. Compare the rule against every other webhook Defined Value.
5. Map only bounded request data into workflow attributes.
6. Store the raw body when structured parsing is needed.
7. Parse and validate inside the workflow.
8. Test no-match, one-match, and accidental-multiple-match cases.
9. Verify authentication and secret handling separately.
10. Inspect the resulting workflow instance.

**Do not assume:** Defined Values are evaluated as an exclusive first-match list.

**Stop when:** Exactly one intended workflow launches and its stored attributes match the expected request. [Configure a Webhook to a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow)

### Recipe: Diagnose an active workflow instance

**Outcome:** The first incorrect state or action is identified without unsafe replay.

1. Open Workflow Detail.
2. Record workflow state, status, initiator, and activation time.
3. Inspect attributes and raw formats where relevant.
4. Inspect activated activities and assignments.
5. Locate the first incomplete or unexpected action.
6. Inspect its criteria and prior actions.
7. Read logs and notes.
8. Verify side effects in their owning Rock records.
9. Decide whether retry is idempotent.
10. Re-run only after duplicate and irreversible effects are ruled out.

**Stop when:** The failure boundary and existing side effects are known. [Edit Workflow Details](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details)

### Recipe: Audit a connection follow-up process

**Outcome:** A Connection process is understood as both person context and operational state.

1. Identify the person and request.
2. Record Connection Type, Opportunity, status, campus, connector, assignee, and next action.
3. Inspect activity and workflow relationships.
4. Compare Board and List visibility.
5. Check filters and current-user security.
6. Identify staff ownership and completion criteria.
7. Inspect active requests before changing Type or Opportunity configuration.
8. Reconcile reporting dependencies.
9. Verify the final staff work queue after any approved change.

**Do not assume:** A missing card means the request itself is wrong.

**Stop when:** The request’s owner, state, visibility, and next action are explicit. [Connections Overview](https://community.rockrms.com/rocku/engagement/connections-overview)

### Recipe: Import or adapt a workflow safely

**Outcome:** An imported or cloned workflow is validated before activation.

1. Identify source version, required plugins, action components, and external references.
2. Use Test Only mode for import.
3. Inspect import warnings and the exported package.
4. Place the workflow in an intentional security category.
5. Verify attributes, field types, forms, activities, action order, and component settings.
6. Replace organization-specific communications, groups, campuses, pages, Defined Values, and Connection Opportunities.
7. Test with disposable instances.
8. Verify logs, assignments, communications, and side effects.
9. Connect the live trigger only after validation.

**Stop when:** No unresolved reference or unverified side effect remains. [Workflow Import/Export](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/use-workflow-importexport)

### Recipe: Design background orchestration

**Outcome:** Slow work proceeds asynchronously with explicit operational state.

1. Define queued, processing, completed, retryable-failure, and terminal-failure states.
2. Store only the identifiers needed to inspect the external work.
3. Define retry limits and duplicate suppression.
4. Define a completion check.
5. Keep the user-facing request path non-blocking.
6. Link output into public pages or apps only after completion is verified.
7. Surface concise staff status without unnecessary raw provider payloads.
8. Test timeout, duplicate callback, partial success, and final failure.

**Stop when:** Every retry is safe and publication cannot occur before verified completion. [Community-reviewed background-work pattern](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)

## Known Gaps And Live Verification

The supplied pack does not establish the following for any target installation. Verify them with bounded, read-only inspection before implementation:

- Installed Rock version, supported branch, and current dot release.
- Available workflow action components and plugin-provided actions.
- Enabled Lava commands, including `workflowactivate` and entity commands.
- Existing workflow categories and inherited security.
- Workflow Entry, My Workflows, Form Builder, Connections Board, Connections List, and Rapid Attendance Entry block settings.
- Entity-trigger timing and configured entity mappings.
- Job schedules, Workflow Launcher behavior, retry policy, and job history.
- Workflow persistence, logging, retention, and automatic completion settings.
- Form field types, attribute qualifiers, stored values, conditional logic, and sensitive-field visibility.
- Person Entry matching and record-creation behavior for the specific form.
- Webhook Defined Values, request discriminators, authentication, and overlapping match rules.
- SMS Pipeline mappings, phone eligibility, communication templates, retained history, and sender behavior.
- Rock Chat configuration and recipient resolution.
- Connection Types, Opportunities, statuses, staff ownership, active requests, security, and reporting dependencies.
- Registration-to-person, check-in, Connection, or workflow handoffs.
- LMS configuration and any group-sync or workflow actions tied to completion.
- External media, PDF, email-provider, payment, or signature integrations.
- Community-reported Lava parser, entity-tracking, persistence, attribute-scope, and deployment behaviors.
- Whether imported workflows preserve every complex action and reference correctly.
- Whether a failed scheduled workflow launch left successful earlier side effects.
- Whether delayed or retried actions remain authorized and idempotent.
- Whether v19-only capabilities apply to the installed version.

Use live evidence only to answer the bounded installation question. Do not publish raw records, organization-specific identifiers, secrets, payloads, or one organization’s configuration as universal Rock behavior.

## Source Map

### Official Rock documentation and Lava references

- [Workflows](https://community.rockrms.com/documentation/core-concepts/workflows) — documentation index and concept ownership.
- [Workflow Types](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-types) — blueprint, attributes, configuration, persistence, and retention.
- [Workflow Actions](https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions) — ordered actions, completion, filters, and stored-value criteria.
- [Define Workflow Activities](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities) — assignment, forms, branching, email commands, and completion.
- [Understand Form Actions](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions) — field visibility, editing, requiredness, conditional logic, and commands.
- [Form Builder](https://community.rockrms.com/documentation/core-concepts/workflows/form-builder) — form-based workflow construction.
- [Launch a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow) — entry pages, direct launches, people, entities, grids, and parameters.
- [Secure Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/secure-workflows) — category inheritance and surface-specific authorization.
- [Manage Workflow Instances](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances) — operational instance review.
- [Configure a Webhook to a Workflow](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow) — webhook matching and request mapping.
- [SMS Pipeline Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/sms-pipeline-workflows) — SMS context and attribute mapping.
- [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands) — Lava activation and attribute parameters.
- [Entity Commands](https://community.rockrms.com/lava/commands/entity-commands) — entity-query parameter behavior.

### RockU operational sources

- [Connections Overview](https://community.rockrms.com/rocku/engagement/connections-overview)
- [Connection Types](https://community.rockrms.com/rocku/engagement/connections-types)
- [Connection Opportunities](https://community.rockrms.com/rocku/engagement/connections-opportunities)
- [Connections Board](https://community.rockrms.com/rocku/engagement/connections-board)
- [Connections List](https://community.rockrms.com/rocku/engagement/connections-list-1)
- [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)
- [Form Builder training](https://community.rockrms.com/rocku/workflows/form-builder)

### Version and implementation evidence

- [v19 Connections presentation](https://www.youtube.com/watch?v=7rxTGLLhlrU)
- [v19 features and enhancements](https://www.youtube.com/watch?v=c-wycR9HEuQ)
- [Immutable WorkflowActivate implementation](https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/Rock/Lava/Blocks/WorkflowActivateBlock.cs)
- [Immutable deprecated Activate Workflow block](https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs)

### Community examples and reviewed patterns

- [Event Participant Call-To-Action recipe](https://community.rockrms.com/recipes/445)
- [Registration-to-Connection Request recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)
- [Workflow-Backed SMS Verification recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)
- [Background media orchestration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)
- [Family preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)
- [LMS workflow example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)
- [Provider event reporting example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5)

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `53`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Each command configured on a workflow Form submits the form and can activate a different workflow path, allowing command choices such as approval and denial to drive separate activities. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions) |
| official | behavior | In a Lava Entity command, parameter values such as `where` must be wrapped in single quotes; when `id` is also supplied, Rock ignores `where`, `dataview`, and `dynamicparameters`. | [source](https://community.rockrms.com/lava/commands/entity-commands) |
| official | behavior | In `workflowactivate`, any key and value beyond the command parameters is treated as a workflow or activity attribute value for the matching attribute key; the supplied value must use that field type's stored-value format. | [source](https://community.rockrms.com/lava/commands/workflow-activate-commands) |
| official | behavior | My Workflows can separate workflows initiated by the current person from active workflows assigned to that person, and group assignments count when the person belongs to the assigned group. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/my-workflows) |
| official | behavior | For an incoming workflow webhook, Rock evaluates every Workflow Webhook Defined Value and starts each configured workflow whose Process Request Lava evaluates to true; matching rules therefore need to be mutually intentional and sufficiently selective. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow) |
| official | configuration | The Mini My Workflows block can filter by workflow categories and initiation or assignment relationship, and its display can be customized with HTML and Lava. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/my-workflows) |
| official | configuration | A workflow Form action independently controls whether each workflow or activity attribute is visible, editable, and required, and conditional logic can show or hide a field based on other field values. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions) |
| official | configuration | A workflow Form action can notify the assigned person when it becomes active and can include form commands in email so the recipient can submit an approval or denial from the message. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities) |
| official | implementation_pattern | A webhook can pass request data such as query parameters, headers, cookies, or the raw body into workflow attributes; complex parsing is better performed inside the workflow after storing the raw body than in the Defined Value template. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow) |
| official | implementation_pattern | Workflow activities can combine assignment, entry forms, conditional action filters, activity activation, and completion commands so one workflow branches and transfers responsibility without duplicating the whole process. | [source](https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities) |
| official | operational_guidance | Before implementing a requested screen, workflow or automation, restate the underlying problem and generate several genuinely distinct approaches. A stakeholder's proposed solution may be valuable requirements evidence without being the best implementation. | [source](https://www.youtube.com/watch?v=pvgZLvcfmFQ) |
| official | release_caveat | Selected v19 connection requests can be reassigned, moved to another status, completed, updated by state, sent to a workflow or activity, and used to initiate SMS or email. Each action remains subject to configured templates, snippets, phone eligibility and user permissions. | [source](https://www.youtube.com/watch?v=7rxTGLLhlrU) |
| More |  | 41 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `19`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [BI Job Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-job) | approved_for_public_distillation | 2 | media-insight:1783ed2aacc57cc3 |
| [Components of a Workflow Transcript Insight](https://community.rockrms.com/rocku/workflows/components-of-a-workflow) | approved_for_public_distillation | 1 | media-insight:bc984ec6248f28f0 |
| [Connection Request Status Automation Transcript Insight](https://community.rockrms.com/rocku/engagement/connection-request-status-automation) | approved_for_public_distillation | 3 | media-insight:e6af71f0b72106fc |
| [Connections Overview Transcript Insight](https://community.rockrms.com/rocku/engagement/connections-overview) | approved_for_public_distillation | 2 | media-insight:f689579d363f61a6 |
| [Connections Types Transcript Insight](https://community.rockrms.com/rocku/engagement/connections-types) | approved_for_public_distillation | 2 | media-insight:fb53d5a069768847 |
| [Data Automation Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/data-automation) | approved_for_public_distillation | 3 | media-insight:e7c8cb97245bec8d |
| [Deconstructing a Sample Workflow Transcript Insight](https://community.rockrms.com/rocku/workflows/deconstructing-a-sample-workflow) | approved_for_public_distillation | 3 | media-insight:1db2ecf2b71445df |
| [Form Builder Transcript Insight](https://community.rockrms.com/rocku/workflows/form-builder) | approved_for_public_distillation | 2 | media-insight:4d696c083d2ec15d |
| More |  | 11 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->
