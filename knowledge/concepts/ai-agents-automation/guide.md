---
id: authored-ai-agents-automation
title: AI Agents And Automation
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "64b2e1db8957c92d8f372d114b1f3429595acc04e963636e99778bcc612788cd"
---

# AI Agents And Automation

## Agent Summary

Rock’s agent framework separates responsibility across three layers:

- An **agent** defines the audience, interaction mode, instructions, available skills and access.
- A **skill** groups related tools and supplies shared usage context and security.
- A **tool** performs one bounded unit of work, such as looking up an entity, retrieving details, calculating a summary or making a specific change.

Treat those layers as independent controls. An agent being available does not imply that every attached skill or tool is authorized, and a tool being visible does not replace entity-level permission checks. Only expose tools appropriate for the agent’s audience and the authenticated person using it. Public agents require especially narrow tools because they must be safe for untrusted use. [AI Agents](https://community.rockrms.com/developer/ai-agents) and [Agents](https://community.rockrms.com/developer/ai-agents/agents)

Use tools to constrain the model’s choices:

1. Resolve natural-language names through lookup or list tools.
2. Pass `IdKey` values between tools instead of exposing raw integer IDs.
3. Retrieve only the fields needed for the current decision.
4. Require prerequisites and confirmation before outbound, destructive or security-sensitive actions.
5. Return a structured success, no-data or error result.
6. Read the changed record or resulting state back before calling the task complete.

Never give an AI integration unrestricted database access or an open-ended facility for generating and executing SQL. Route operational access through reviewed Rock code that applies authorization and business rules. A narrowly secured tool containing reviewed, static SQL is different from arbitrary model-generated SQL, but it still requires parameter sanitation, bounded output and authorization design. [Approved claims `claim:a181b9ddd5b0e689895b` and `claim:c3921cb1d8b61e06c713`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s)

No Rock instance was inspected for this guide. Installed version, AI provider, agent configuration, permissions, enabled tools, workflow settings and actual side effects remain live-verification requirements.

## Scope And Boundaries

This guide covers:

- Agent, skill and tool responsibilities.
- Chat, MCP, Internal and Public boundaries.
- Tool naming, parameters, lookup surfaces and result shapes.
- Lava and native-tool design.
- Least privilege, data minimization and SQL boundaries.
- Prompt layering and conversation context.
- Workflow-oriented automation and durable handoffs.
- Approval, read-back and operational review gates.
- Troubleshooting and live-verification practices.

Detailed administration of Rock security, APIs, workflows, reports, Data Views, Lava or provider configuration belongs in those concepts. This guide covers how an agent should interact with those surfaces without replacing their owning documentation.

Current developer documentation describes the framework for developers comfortable with Lava, SQL or C#, and emphasizes that building agent capabilities carries responsibility for both safety and clarity. [AI Agents](https://community.rockrms.com/developer/ai-agents)

The evidence pack contains current developer-documentation excerpts, official media guidance, release notes and selected source-code excerpts at an immutable commit. Source-code observations describe that commit’s implementation; they do not prove that the same feature is installed, configured or enabled in a particular Rock instance.

## Mental Model

### Agent, skill and tool

An agent is the orchestration boundary. It selects the persona, instructions, skills and tools available for a particular use. Separate agents can therefore serve different risk profiles: a staff agent may have broad internal read access, a volunteer agent may have fewer or non-mutating tools, and a public agent should expose only capabilities safe for any visitor. [Agents](https://community.rockrms.com/developer/ai-agents/agents)

A skill is a coherent group of tools with shared usage context. Skills reduce repeated instructions and provide a security-management boundary. Avoid adding overlapping skills merely because a local term differs from Rock terminology; existing tools plus concise organization instructions may already cover the use case. Too many skills and tools increase context size, cost and tool-selection ambiguity. [Skills](https://community.rockrms.com/developer/ai-agents/skills)

A tool is one bounded operation. A request that sounds like one task may require several tool calls—for example, locating a person, resolving a group and then adding the person to that group. Treat each call as its own authorization and validation boundary. [AI Agents](https://community.rockrms.com/developer/ai-agents)

### Control stack

A production decision should pass through all applicable controls:

1. **Agent availability:** May this person use this agent?
2. **Audience and channel:** Is it Internal or Public, and Chat or MCP?
3. **Skill availability:** Is the capability group attached and authorized?
4. **Tool availability:** Is this exact operation exposed?
5. **Entity authorization:** May the current person view or modify the target?
6. **Business rules:** Is the operation valid in the target’s current state?
7. **Human approval:** Has a required outbound, destructive or sensitive action been confirmed?
8. **Read-back:** Does the authoritative Rock state show the intended result?

Rock’s pre-release design was described as applying permissions as the authenticated person using the agent, including through MCP, rather than giving the agent unrestricted administrative access. That statement remains release-sensitive: verify the shipped version and every enabled tool’s authorization behavior. [Approved claim `claim:2a7ef23854b5dd315c7d`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s)

### Chat, MCP, Internal and Public are separate choices

Chat agents operate inside Rock and can receive context anchors from the chat host. MCP agents expose tools to an external client and do not support Rock chat context anchors. Internal versus Public determines the intended audience and can affect which fields a tool returns; it does not replace skill, tool or entity security. [Agents](https://community.rockrms.com/developer/ai-agents/agents)

Context anchors help keep a Chat conversation focused on a particular entity, such as the person whose profile is open. They are hints, not guarantees, and only one anchor per entity type can be present. Tool code does not establish anchors; the chat host does. [Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors) and [Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions)

## Agent Tools And Lookup Surfaces

### Shape tools around intent

Use clear `VerbNoun` names such as `LookupConnectionTypes`, `ListGroups`, `GetGroup`, `GetConnectionRequestSummary`, `GetPersonAvailableAttributes`, `AddOrUpdateGroup` or `SendCommunication`. Names, parameter descriptions, prerequisites and return descriptions help the model choose the correct operation. [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools) and [Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)

The recommended types have different jobs:

- **Lookup:** Returns a bounded reference set used as input to other tools. It commonly returns `IdKey`, name and only the metadata needed to select correctly.
- **List:** Returns filtered matching records. Large sets should be paginated.
- **Get:** Returns one identified record with the details needed for the task.
- **Summary:** Returns aggregate information, often grouped by a defined dimension.
- **Insights:** Returns an opinionated analysis over filtered or aggregated data rather than individual records.
- **AvailableAttributes:** Returns attribute definitions and value-format information, not the entity’s attribute values.
- **AddOrUpdate:** Creates a new record when no target key is provided or updates an identified record when one is provided.
- **Action:** Performs a stateful operation such as launching a workflow or sending a communication. Prerequisites and guardrails should describe required state and confirmation.

Delete operations belong in the taxonomy but should be omitted entirely when the agent does not need them. Tool-level controls are intended to allow capabilities such as drafting while withholding sending. [Approved claim `claim:903c8ff9b5d2590fd616`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)

### Use lookup, list and get as a sequence

Lookup and list tools should help the model resolve the target without flooding its context. A lookup generally returns the reference set needed by another tool; a list accepts meaningful filters; a get retrieves the selected record’s fuller representation. This division lets a list remain compact while a get supplies details only when needed. [Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools), [List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/list-tools) and [Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/get-tools)

Do not return every entity property by default. Return enough information to distinguish candidates and make the next decision. Large descriptions, unused fields and full result objects stored repeatedly in conversation history consume context and may be summarized away later. Native Get-tool guidance recommends storing a compact reference in history and calling the Get tool again if full details are needed. [Native Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/get-tools)

### Design parameters for a model caller

Native-tool parameters should be flat, top-level method arguments rather than nested parameter objects. Use explicit names such as `personIdKey` or `communicationIdKey`, not a context-free `idKey`. Required and optional behavior should be expressed clearly through the parameter signature and descriptions; truly optional nullable inputs should default to `null`. [Tool Parameters](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/tool-parameters)

Never expose a raw Rock integer `Id` to the model. Accept and return `IdKey` values, converting internally when Rock code needs an integer identifier. [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)

AvailableAttributes tools are important when qualifiers determine which attributes apply. For an existing entity, load that entity. For a new entity, create an in-memory representation and set the qualifying values before retrieving definitions. The result should identify attribute keys, field types and formatting expectations needed by the later AddOrUpdate call. [AvailableAttributes Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools)

The supplied immutable source excerpts show this pattern across workflows, connection requests, content-channel items, CMS blocks and pages: an existing entity key can be used for edits, while creation paths use a parent type or other qualifier to construct the applicable attribute surface. This is implementation evidence from commit [`471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills), not proof of an installation’s available tools.

### Choose Lava or native code deliberately

Lava supports low-code tools inside Rock. The documented Lava tool types are:

- **AI Prompt:** Supplies stored instructions to the agent.
- **Execute Lava:** Runs Lava and returns a shaped result.

An Execute Lava tool has a name, description, prompt and parameters. Its response should use the agent-tool filters to distinguish `Success`, `NoData` and `Error`, attach private instructions, compact or suppress history content, add metadata and supply secured Rock reference routes. `NoData` represents a successful operation with no returned items; it is not an error. [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)

Native tools use compiled C# and Rock infrastructure for more complex logic, external integrations or heavier data work. Native methods should return `AgentToolResult`, use intentionally shaped result objects and provide actionable error results. Native metadata can describe purpose, usage, guardrails, prerequisites, examples, return shape and chat preamble. A method without an `AgentToolGuid` is not registered as a tool. [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)

Use cache objects when available and entity services or commands when they better preserve Rock behavior. The SQL examples in the summit were intentionally simplified teaching examples; they should not be copied into production without authorization, business-rule and query-cost analysis. [Approved claim `claim:725a3342f3dc657cc546`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=1490s)

### Paginate according to authorization behavior

For large Lava list results, paginate and use the conventional `pageNumber` parameter where applicable. Sanitize every string interpolated into SQL with `SanitizeSql`; prompt instructions do not prevent a user from supplying malicious input. [Lava List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/list-tools)

Native list tools that apply per-item authorization should use cursor pagination. Page-number offsets can become incorrect or increasingly expensive when unauthorized items are filtered out while walking earlier pages. Page-number pagination is appropriate only when an offset can be trusted without per-item security filtering. [Native List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools)

## Permissions And Data Boundaries

### Apply least privilege at every layer

Configure security before attaching a tool to an agent. Rock’s documentation says new agents default to the `RSR - Rock Administrator` security role and remain locked down until access is explicitly granted. A staff-facing agent may begin with an appropriate staff role, but each organization must decide the actual access boundary. [Agents](https://community.rockrms.com/developer/ai-agents/agents)

Skill security keeps related tools consistent, but individual tool review remains necessary. A skill that includes both read and write capabilities may be too broad for a public, volunteer or drafting-only agent. Tool availability and Rock authorization must both pass; neither substitutes for the other. [Skills](https://community.rockrms.com/developer/ai-agents/skills) and [approved claim `claim:903c8ff9b5d2590fd616`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)

For a Public agent:

- Include only tools safe for an unknown, potentially hostile user.
- Review every returned field for public suitability.
- Do not assume that the Public designation automatically removes every field your organization considers sensitive.
- Test both normal and adversarial prompts.
- Exclude write, send, delete and administrative tools unless a separately reviewed public use case truly requires them.

Rock documents that tools may omit or substitute properties according to audience—for example, returning a public-safe representation instead of an internal one—but the organization remains responsible for configuring security on the agent, skills and tools. [Agents](https://community.rockrms.com/developer/ai-agents/agents)

### Keep database access behind Rock controls

Do not give the model a general API key with unrestricted data access, direct database credentials or an arbitrary SQL executor. Managed Rock code should validate identifiers, apply permissions, preserve business rules and restrict both inputs and outputs. [Approved claim `claim:a181b9ddd5b0e689895b`](https://www.youtube.com/watch?v=mYTaGxYMyyQ&t=557s)

Static SQL inside a reviewed Lava tool is still code. It must:

- Accept explicit, bounded parameters.
- Convert `IdKey` values internally.
- Sanitize string inputs.
- Select only required columns.
- Limit and paginate large result sets.
- Enforce the applicable authorization boundary.
- Avoid bypassing entity business logic for updates.
- Return a structured `AgentToolResult`.

The summit explicitly distinguished such reviewed, narrow SQL from model-generated SQL executed at runtime, which was strongly discouraged because it bypasses Rock security and business logic. [Approved claims `claim:c3921cb1d8b61e06c713` and `claim:4b7b8d0b0379ceb7587f`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s)

### Treat authorization changes as high-risk mutations

The supplied v20-alpha source excerpt includes tools for listing supported authorization actions, listing direct and inherited rules, adding or updating a rule and deleting a rule. Those implementations require administrative access to the secured entity, attach guardrails to mutations and refuse changes that would remove the caller’s own administrative access through the tool. They also recommend reading the ordered rule list back after a change. [Immutable source excerpt](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills)

Because that is source-code evidence from a particular commit, do not infer that these tools are installed, enabled or attached to an agent. If present, keep them off general-purpose agents and require an explicit review of entity, action, subject, allow/deny choice and rule order before mutation.

### Bound MCP authentication

Rock’s planned MCP flow was described as using OAuth so that the external harness—not the language model—holds and renews the access token, avoiding exposure of a general Rock API key to the model. Administrators must verify the released implementation’s client authorization, scopes, expiry and revocation behavior. [Approved claim `claim:2a2a9fc94666d58b0e4f`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s)

Do not treat OAuth as sufficient by itself. The authenticated identity, agent configuration, skill and tool exposure, entity permissions and tool implementation still determine what an MCP client can do.

## Prompt And Tool Boundaries

Rock’s prompt context is layered across the core prompt, organization prompt, agent instructions, skill instructions and current-person context. Context anchors and conversation history add further request context. Keep each layer concise because repeated instructions consume tokens on every request. Add instructions when testing demonstrates a need, and place each rule at the narrowest layer that owns it. [Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions) and [approved claim `claim:57e32b4d554a759231a1`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s)

Use the layers this way:

- **Organization prompt:** Stable organization-wide terminology or policy.
- **Agent instructions:** Persona, audience behavior and general ambiguity handling.
- **Skill instructions:** Relationships and conventions shared by a related tool set.
- **Tool schema and annotations:** Exact purpose, parameters, prerequisites, result shape and safety guardrails.
- **Current-person context:** The authenticated user information needed for the request.
- **Context anchor:** The primary entity supplied by a Chat host.
- **Conversation history:** Prior turns that may help continuity but may later be summarized.

Instructions do not enforce authorization. A sentence such as “only show permitted records” is not a substitute for filtering records in Rock code. Likewise, a prompt that says “never send without approval” should be reinforced by omitting the send tool from drafting agents or by enforcing a confirmation prerequisite at the action boundary.

Rock-side skills and tools provide capabilities. An external harness may also contain organization-specific skills or business rules that guide how those capabilities are used. Govern and version both layers; do not assume MCP tool definitions contain the organization’s full operating policy. [Approved claim `claim:538f1a4e0ad7c90f7c5a`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=909s)

## Automation Design And Workflows

### Separate reasoning, drafting and execution

A safe automation normally has distinct stages:

1. Gather bounded, authorized data.
2. Resolve ambiguous entities.
3. Produce a proposed result or draft.
4. Validate prerequisites and current state.
5. Obtain approval where required.
6. Invoke the narrow action tool.
7. Read the result back from Rock.
8. Produce a durable handoff or audit artifact when the work must outlive the conversation.

This pattern allows an organization to automate research and drafting without automatically enabling outbound or destructive actions. It follows Rock’s per-tool control model and native-tool support for purpose, prerequisite and guardrail annotations. [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools) and [approved claim `claim:903c8ff9b5d2590fd616`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)

When work must survive the chat, create a durable file or handoff artifact rather than leaving the result only in transient conversation history. [Approved claim `claim:679a38216f2b07097624`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=713s)

### Use Rock workflows as bounded action surfaces

The supplied source excerpt at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` shows a `LaunchWorkflow` tool that:

- Resolves a workflow type with a security check.
- Can restrict launches to workflow types configured on the agent’s Workflow skill.
- Applies supplied attribute values through helper logic.
- Returns a configuration-specific error when the workflow exists but is not launchable by that agent.

That is a useful implementation pattern: combine the current person’s Rock access with an agent-specific allowlist rather than treating view access as universal permission to launch every workflow. [LaunchWorkflow source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.LaunchWorkflow.cs)

The same commit includes a Get tool that retrieves a workflow’s current state, attributes, activities and actions after applying security. Use a read operation like this for post-launch verification rather than relying only on the action tool’s success message. [GetWorkflow source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflow.cs)

Rock v20.0 release notes, dated September 2, 2026 and marked Alpha in the supplied pack, describe a Workflow Builder AI skill that can discover installed action components and create, edit or remove workflow definitions and related structures. That capability is administrative and release-sensitive; verify version, packaging, configuration and tool exposure before use. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Connect event-driven automation carefully

Rock 18.1 release notes describe a Chat Message Automation Trigger and a Send Fallback Chat Notification Automation Event for alternate notification methods when a person lacks an active personal device or has notifications disabled. Treat this as a version-specific communication automation surface, not evidence that any particular instance has configured a trigger or fallback path. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

For event-driven automation, verify:

- The installed Rock version contains the trigger and event.
- The trigger is active and scoped to the intended messages.
- The fallback channel is configured.
- Recipient selection and consent rules are correct.
- Duplicate or recursive triggering is prevented.
- Test events produce the expected workflow or notification records.

### Treat generated summaries as assistance

Connection-request AI summaries and insights require both a configured prompt on the connection type and a configured AI provider. Their output is generated assistance, not authoritative person data. [Approved claim `claim:069aa7a39db4563841a2`](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s)

Do not write a generated inference back as verified person data without a separate, authorized workflow and human review. When a summary affects pastoral follow-up or another consequential decision, inspect the underlying Rock records and identify uncertainty.

### Include training in the rollout

AI automation is partly an operational adoption problem. Staff who do not understand the intended Rock workflow are more likely to create disconnected shadow processes that fragment data and accountability. [Approved claim `claim:4b083dda9f0d9ccc4aff`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2042s)

Rock’s LMS can assign role-specific curricula and track completion, subject to installed-version configuration and permissions. Train staff before expecting them to train volunteers; staff-first sequencing creates training multipliers and reduces inconsistent data practices. [Approved claims `claim:91be2ad338eb6b1cdaed` and `claim:c8c3a60f71790dd3616d`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1983s)

When an upgrade changes an agent or Rock interface, prepare and distribute a short targeted video before staff encounter the change. [Approved claim `claim:c9c1fa08cb4d501e6`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1714s)

## Verification And Review Gates

Use evidence appropriate to the claim being made:

- **Tool schema or configuration:** Inspect the installed agent, skill, tool and parameters.
- **Authorization:** Test with representative identities, including an allowed user and a denied user.
- **Read behavior:** Compare the tool’s returned records and fields with authorized Rock views.
- **Mutation:** Use a controlled target, obtain required approval and read the target back afterward.
- **Outbound action:** Confirm the created draft, recipient and content before sending; verify delivery state separately.
- **Workflow launch:** Verify that the workflow exists, is active and has the intended attribute values and activities.
- **Generated summary:** Inspect the configured prompt and provider, then compare the output with its underlying records.
- **MCP:** Verify client authorization, authenticated person, token scope, tool discovery and revocation.
- **Public agent:** Test adversarial prompts and confirm that sensitive fields and dangerous tools remain inaccessible.
- **Performance:** Exercise pagination, large result sets and expensive filters without assuming a small test dataset represents production.

A successful tool response proves only what that response states. It does not by itself prove that an outbound message was delivered, a scheduled process will continue running, a public user cannot discover another path or a workflow completed all downstream work.

Use built-in tool logs during debugging to inspect calls, inputs and results. Temporary debugging prompts can ask the model which tools it considered and why it did or did not call them, but model-reported reasoning is diagnostic context, not proof that authorization or execution succeeded. [Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools) and [approved claim `claim:4b7b8d0b0379ceb7587f`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s)

## Version And Authority Caveats

- The developer-documentation excerpts in this pack identify documentation version `1.0.0`. Confirm the documentation applicable to the installed Rock release.
- Rock v20.0 was listed as Alpha on September 2, 2026 in the supplied release-note snapshot. Its Workflow Builder, Core Administration and Community Knowledge Base AI skills should be treated as pre-production until the organization verifies a supported release and installed behavior. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Summit and Rock Cast statements about MCP, OAuth, authenticated-person permissions and tool controls were pre-release guidance. They describe intended design, not guaranteed behavior in every released or installed version. [RockIQ Rapid Fire Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM)
- The supplied source-code excerpts all reference immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They can clarify implementation at that revision but cannot establish an instance’s schema, plugins, configuration or deployment state.
- Rock 17.5 release notes describe a fix for permission checks on a model’s `./DataView/{id}` endpoint. If an agent integration uses that surface on an older release, confirm version applicability before diagnosing authorization solely as bad configuration. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- A historical community question about Lava `webrequest` behavior is not sufficient authority for current agent-tool troubleshooting and should not be generalized to modern Rock versions.
- Community sessions and partner material in the pack provide implementation context and examples, not universal Rock behavior.
- No reviewed live-instance evidence was supplied.

## Troubleshooting Decision Tree

### The agent does not show a tool

1. Confirm the installed Rock version and packaging include the tool.
2. Confirm the method or Lava tool is registered; native methods require an `AgentToolGuid`.
3. Confirm the skill is attached to the intended agent.
4. Confirm the tool is enabled within that skill.
5. Confirm the current person can use the agent, skill and tool.
6. Confirm the agent type is correct; Chat and MCP are separate configurations.
7. For an external client, refresh tool discovery after authorization or configuration changes.
8. Inspect tool logs before changing the prompt. [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)

### The agent chooses the wrong tool

1. Check whether tool names follow a clear verb-and-entity pattern.
2. Compare overlapping tool purposes and remove redundant capabilities.
3. Inspect parameter names, descriptions, prerequisites and return descriptions.
4. Verify that lookup, list and get responsibilities are distinct.
5. Temporarily ask the model to explain which tools it considered.
6. Shorten or relocate conflicting organization, agent or skill instructions.
7. Retest with representative phrasing and ambiguous phrasing. [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools) and [Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)

### The agent acts on the wrong person or entity

1. Inspect the current Chat context anchor, if applicable.
2. Remember that MCP agents do not receive Rock context anchors.
3. Resolve the target through a lookup or list operation.
4. If multiple candidates remain, stop and ask for clarification.
5. Pass the selected `IdKey`, never a raw integer ID.
6. Use Get to read the selected entity before mutation.
7. Read the entity back after mutation. [Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors)

### The tool returns unauthorized or sensitive data

1. Disable the tool on the affected agent if exposure may continue.
2. Confirm whether the agent is Internal or Public.
3. Inspect agent, skill, tool and entity permissions separately.
4. Review the result object for fields that should be omitted or replaced for Public use.
5. Confirm authorization filtering occurs in code rather than only in instructions.
6. Test with a least-privileged identity and an anonymous or public path where applicable.
7. Review logs for prior calls and follow the organization’s incident process if data was exposed. [Agents](https://community.rockrms.com/developer/ai-agents/agents)

### A list is incomplete, repeats items or becomes slow on later pages

1. Identify whether per-item authorization is applied.
2. If it is, verify that the native tool uses cursor pagination.
3. If it is not, confirm page-number ordering is deterministic.
4. Check that filters and cursor or page values are returned as metadata.
5. Confirm the result set is bounded and returns only required fields.
6. Inspect query cost on production-like volume.
7. Do not solve context pressure by removing authorization checks. [Native List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools)

### A Lava tool errors or returns unexpected no-data

1. Inspect tool logs for the supplied parameters and status.
2. Confirm the tool accepted `IdKey` and converted it internally.
3. Sanitize every string used in SQL.
4. Distinguish `NoData` from `Error`.
5. Confirm the selected fields and joins match the requested result.
6. Verify authorization rather than assuming a valid identifier implies visibility.
7. Replace raw SQL with cache objects or entity commands when that better preserves Rock behavior. [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)

### A mutation was refused or changed the wrong state

1. Stop additional write calls.
2. Read the target’s current state.
3. Confirm the target `IdKey`, current person and agent.
4. Check required lookup and Get prerequisites.
5. Confirm the person has both tool access and entity-level authorization.
6. Verify the action is allowed in the entity’s current state.
7. Review tool parameters, especially nullable fields and add-versus-update behavior.
8. Require a fresh confirmation before retrying.
9. Read the result back after any retry. [AddOrUpdate Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/addorupdate-tools)

### A connection-request AI summary is missing

1. Confirm the connection type has an AI prompt configured.
2. Confirm an AI provider is configured and available.
3. Confirm the installed version supports the feature.
4. Check permissions and logs for the requesting person.
5. Retest with a suitable connection request.
6. Treat any generated result as assistance rather than authoritative person data. [Approved claim `claim:069aa7a39db4563841a2`](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s)

### An MCP client cannot authenticate or discovers unexpected tools

1. Confirm the installed MCP implementation and supported Rock version.
2. Verify the external client registration and authorization.
3. Confirm the authenticated Rock person.
4. Inspect scopes, token expiry and revocation behavior.
5. Confirm the intended MCP agent is selected.
6. Review its attached skills and tools.
7. Test an allowed and denied operation.
8. Revoke the client if the discovered capability exceeds the intended boundary. [Approved claims `claim:2a2a9fc94666d58b0e4f` and `claim:2a7ef23854b5dd315c7d`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s)

### A workflow does not launch

1. Confirm the workflow type exists and is active.
2. Confirm the current person is authorized for it.
3. Confirm the Workflow skill is attached to the agent.
4. Check whether the agent’s configuration limits launchable workflow types.
5. Retrieve AvailableAttributes for the workflow type before supplying values.
6. Inspect the action result and logs for validation errors.
7. Read the workflow back to verify activation and supplied values.
8. Do not infer downstream completion merely because launch succeeded. [LaunchWorkflow source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.LaunchWorkflow.cs)

## Agent Task Recipes

### Recipe: Design a safe read-only lookup surface

**Outcome:** The agent can resolve a natural-language reference to an authorized Rock entity without receiving unnecessary data.

1. Identify the downstream tool and the exact identifier it needs.
2. Determine the smallest useful selection fields, normally an `IdKey`, name and limited disambiguating metadata.
3. Use a cache object when available; otherwise use a secured entity query.
4. Filter out inactive or unauthorized entries when required.
5. Return structured results through `AgentToolResult`.
6. Store a compact history representation.
7. Test no matches, one match, multiple matches and a denied record.

**Inspect:**

- Audience-specific fields.
- Entity authorization.
- Maximum result size.
- Whether a List tool with filters is more appropriate.

**Do not assume:**

- A small development dataset will stay small.
- A Public agent designation automatically sanitizes every field.
- Prompt instructions enforce data access.

**Stop when:**

- The target cannot be identified uniquely.
- Required authorization cannot be enforced.
- The result set cannot be bounded. [Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)

### Recipe: Build a bounded List and Get pair

**Outcome:** The agent can search a large entity set and retrieve details only for the selected item.

1. Define a `List<Entity>` tool with explicit filters and deterministic ordering.
2. Use cursor pagination when per-item authorization is required.
3. Return only the fields needed to distinguish candidates.
4. Define a `Get<Entity>` tool accepting the selected `IdKey`.
5. Enforce security while loading the entity.
6. Shape and sanitize the full result.
7. Keep only a compact reference in conversation history.
8. Test pagination, invalid keys, denied entities and repeated retrieval.

**Inspect:**

- Query cost.
- Per-item authorization.
- Cursor or page metadata.
- Public versus Internal result shapes.

**Do not assume:**

- Page-number pagination is safe with per-item filtering.
- Every entity property belongs in the agent context. [Native List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools) and [Native Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/get-tools)

### Recipe: Add a controlled AddOrUpdate capability

**Outcome:** An authorized user can create or edit one entity through a validated, auditable tool.

1. Decide whether the same tool should support both create and update.
2. Accept an optional entity `IdKey`; treat its presence as update and absence as create.
3. Add explicit qualifier keys required for creation.
4. Retrieve available attributes before accepting attribute values.
5. Load existing entities with security checks or create through Rock’s managed entity infrastructure.
6. Validate required fields and state-dependent rules.
7. Apply attributes through reviewed helper or entity logic.
8. Save only when no validation errors remain.
9. Return a bounded full result with a compact history reference.
10. Read the entity back independently before reporting completion.

**Inspect:**

- Add and edit permissions.
- Attribute visibility and editability.
- Null, set and clear semantics.
- Downstream workflows or side effects.

**Stop when:**

- The target is ambiguous.
- A required qualifier is missing.
- Approval is required but absent.
- The read-back differs from the requested state. [AddOrUpdate Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/addorupdate-tools)

### Recipe: Configure a drafting agent without send authority

**Outcome:** Staff can research and compose a communication while sending remains a separate approved action.

1. Create or select an Internal agent for the intended staff group.
2. Attach only the read tools needed to resolve recipients and context.
3. Attach a compose or draft tool.
4. Omit send and delete tools from the agent.
5. If a separate send agent is required, restrict it to a smaller role and add an explicit confirmation prerequisite.
6. Test that drafting succeeds for an authorized user.
7. Test that direct and indirect requests to send are refused.
8. Review returned recipient data for least privilege.

**Do not assume:**

- An instruction saying “do not send” is equivalent to withholding the send tool.
- Draft creation proves delivery.
- Recipient identity may be inferred safely. [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools) and [approved claim `claim:903c8ff9b5d2590fd616`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)

### Recipe: Launch a workflow through an agent

**Outcome:** The agent launches one permitted workflow with valid attribute values and verifies the resulting record.

1. Lookup the permitted workflow types.
2. Resolve the requested type to an `IdKey`.
3. Retrieve its available attributes and formatting requirements.
4. Gather missing required values from the user.
5. Confirm any consequential side effects.
6. Call the launch action once.
7. Capture the returned workflow reference.
8. Retrieve the workflow and verify activation, status and supplied values.
9. Produce a durable handoff when another person or process must continue the work.

**Inspect:**

- Agent-specific launchable workflow configuration.
- Current-person authorization.
- Workflow activation state.
- Downstream activities that remain pending.

**Stop when:**

- The type is not allowlisted for the agent.
- Required values cannot be validated.
- Launch succeeded but read-back is unavailable. [LaunchWorkflow source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.LaunchWorkflow.cs)

### Recipe: Review a Public agent before launch

**Outcome:** The public surface exposes only reviewed, non-sensitive and non-destructive capabilities.

1. Inventory every attached skill and tool.
2. Remove all capabilities not required by the public use case.
3. Review each tool’s parameters, return fields and reference routes.
4. Confirm that entity authorization and audience sanitization occur in code.
5. Test anonymous and least-privileged access.
6. Test prompt injection, identifier guessing, broad listing and requests for internal data.
7. Confirm write, send, delete and administration operations are absent.
8. Review logs and remediate every unexpected call or field.
9. Repeat the review after version, plugin, tool or prompt changes.

**Do not assume:**

- Friendly agent instructions prevent hostile requests.
- Public mode alone establishes the organization’s privacy policy.
- A successful normal-path test covers adversarial use. [Agents](https://community.rockrms.com/developer/ai-agents/agents)

### Recipe: Diagnose incorrect tool selection

**Outcome:** The model consistently chooses the intended tool for representative requests.

1. Capture a minimal failing prompt.
2. Inspect the agent’s available skills and tools.
3. Compare names, purposes, prerequisites, parameter descriptions and return descriptions.
4. Remove overlapping or unused tools from the test agent.
5. Add temporary debugging instructions asking which tools were considered.
6. Adjust the narrowest responsible instruction or schema description.
7. Retest the failing prompt, close variations and an intentionally ambiguous request.
8. Remove temporary debugging instructions before production use.
9. Review tool logs to confirm actual calls.

**Stop when:**

- Correct selection depends on information the user did not provide; ask for clarification instead.
- A prompt change would attempt to compensate for missing authorization or validation code. [Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)

### Recipe: Roll out an agent-assisted process to staff

**Outcome:** Staff understand the approved use case, review boundary and authoritative Rock workflow before volunteer rollout.

1. Document the approved tasks and prohibited actions.
2. Assign role-specific training through the configured LMS where available.
3. Demonstrate how to verify generated output against Rock records.
4. Provide a short video before any interface change.
5. Require staff completion before expanding access.
6. Pilot with a small staff group and review tool logs and data quality.
7. Correct the process and training.
8. Train volunteers only after staff can support the workflow consistently.

**Inspect:**

- LMS configuration and permissions.
- Completion reporting.
- Shadow tools or duplicate data processes.
- Support questions after the interface change. [Approved claims `claim:91be2ad338eb6b1cdaed`, `claim:c8c3a60f71790dd3616d` and `claim:c9c1fa08cb4d501e6`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1983s)

## Known Gaps And Live Verification

No live-instance review was supplied. Before production use, verify:

- Installed Rock version and release channel.
- Whether AI Agents are included in the installed package.
- Configured AI provider, model and provider permissions.
- Agent type: Chat or MCP.
- Audience type: Internal or Public.
- Agent, skill and individual tool authorization.
- Entity-level view, edit, administer and specialized actions.
- Which tools are actually attached and discoverable.
- Whether destructive, outbound or authorization-management tools are absent from general agents.
- Prompt layers and their effective combined content.
- Context-anchor behavior in the actual Chat host.
- MCP client registration, authenticated identity, token scopes, expiry and revocation.
- Tool result sanitation for Internal and Public audiences.
- Raw integer ID exposure in parameters, results, history content and logs.
- SQL sanitation, query cost, authorization filtering and business-rule coverage.
- Pagination behavior on production-scale data.
- AvailableAttributes behavior for installed schema, qualifiers, plugins and custom attributes.
- Workflow allowlists, launch behavior and post-launch read-back.
- Connection-type prompt and AI-provider configuration for generated summaries.
- Chat automation triggers and fallback-notification configuration.
- Tool logging, retention and access.
- Staff training assignments and completion tracking.
- Durable handoff requirements for work that must survive a conversation.

Evidence gaps remain for provider-specific behavior, model-specific tool-selection limits, exact production availability of pre-release capabilities, upgrade paths, licensing and packaging, usage-cost controls, log-retention defaults and the complete released MCP authorization model. Do not fill these gaps from names, roadmap statements or source-tree presence.

## Source Map

### Official developer documentation

- [AI Agents](https://community.rockrms.com/developer/ai-agents): Agent, skill, tool, context-window and system-prompt concepts.
- [Agents](https://community.rockrms.com/developer/ai-agents/agents): Public versus Internal, Chat versus MCP and default agent security.
- [Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions): Prompt layers, context anchors and conversation history.
- [Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors): Chat-only entity anchoring and ambiguity limits.
- [Skills](https://community.rockrms.com/developer/ai-agents/skills): Skill grouping, shared context, security and context-size considerations.
- [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools): Tool security, naming and `IdKey` boundary.
- [Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools): Lookup, List, Get, Summary, Insights, AvailableAttributes, AddOrUpdate and Action patterns.
- [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools): Execute Lava result statuses, filters, metadata, history and reference routes.
- [Lava Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools): Minimal lookup results and `IdKey` conversion.
- [Lava List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/list-tools): Filtering, pagination, minimum fields and `SanitizeSql`.
- [Lava Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/get-tools): Single-record result and error handling.
- [Lava Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools): Filtered aggregate analysis.
- [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools): Native annotations, structured results, guardrails and error handling.
- [Native List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools): Page-number versus cursor pagination.
- [Native Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/get-tools): Secured entity retrieval, sanitation and compact history.
- [AddOrUpdate Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/addorupdate-tools): Create/update branching, validation and save behavior.
- [AvailableAttributes Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools): Attribute definitions for existing and not-yet-created entities.
- [Tool Parameters](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/tool-parameters): Flat, explicit and nullable parameter design.
- [Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools): Tool-selection diagnostics.

### Official release and media evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): Version-specific AI, workflow, API and automation changes.
- [AI Summit: The Community’s First Look at Rock’s AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8): Approved operational claims about architecture, prompts, Lava tools, SQL boundaries and logging.
- [RockIQ Rapid Fire Q&A from the AI Summit](https://www.youtube.com/watch?v=dpYJiOAiJYM): Release-sensitive claims about MCP, OAuth, authenticated-person permissions, tool controls and local business-rule layers.
- [AI Voice Models & the Hidden Costs of Untrained Staff](https://www.youtube.com/watch?v=bu5nPeAVCAo): Durable artifacts, staff training, LMS assignments and change management.
- [Connections Helps Prevent Your People from Falling Through the Cracks](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s): Connection-request AI summary prerequisites and authority caveat.
- [Ladies and Gentlemen, Your RX26 Keynote Speaker](https://www.youtube.com/watch?v=mYTaGxYMyyQ&t=557s): Direct-database-access warning.

### Immutable implementation evidence

Selected source excerpts were supplied from [`SparkDevNetwork/Rock` commit `471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills). They illustrate Data View cursor paging, AvailableAttributes implementations, workflow read and launch tools and authorization-management guardrails. They are implementation evidence for that commit, not evidence of any organization’s installed configuration.