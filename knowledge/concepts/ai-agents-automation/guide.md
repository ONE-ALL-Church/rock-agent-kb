---
id: authored-ai-agents-automation
title: AI Agents And Automation
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# AI Agents And Automation

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [AI Agents And Automation index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock AI Agents are configured operational actors inside Rock RMS. They are not just chat prompts. An agent is a governed execution surface that combines instructions, enabled skills, callable tools, user/session context, Rock security, and persisted chat/session data. The most important practical rule is that an agent should only be able to see and do what the current person, API key, configured agent, enabled skill, and individual tool are permitted to see and do. Rock's developer guidance frames agents as powerful assistants that must remain understandable and safe because they operate near the organization's live ministry data ([AI Agents](https://community.rockrms.com/developer/ai-agents)).

For implementation work, treat an agent as a controlled interface over Rock operations:

- The **Agent** decides the operating persona, available skills, instructions, and usage context ([Agents](https://community.rockrms.com/developer/ai-agents/agents)).
- A **Skill** groups related tools, supplies shared domain context, and provides a security management boundary ([Skills](https://community.rockrms.com/developer/ai-agents/skills)).
- A **Tool** performs a specific lookup, read, insight, summary, or mutation action ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).
- A **Context Anchor** pins an entity such as a person or group into the session so the model has stable reference context across turns ([Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors)).
- An **AI Agent Session** stores the relationship between an agent and a person, with child records for history and anchors according to Rock source model snippets ([AIAgentSession.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSession/AIAgentSession.cs)).
- Automation extends this pattern beyond chat by letting configured events trigger actions in Rock. Rock 18.1 introduced Automations as an autonomous trigger/action pattern, and release notes identify a Chat Message automation trigger plus fallback chat notification event in the Communication module ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

The operational posture should be conservative. Give agents narrow tools, expose IdKeys instead of raw integer IDs, use lookup/list/get patterns so the model does not guess identifiers, require explicit human approval before communications or destructive changes, and verify results against live Rock state before treating a response as fact. Rock's custom tool guidance specifically warns against exposing raw Rock integer IDs to the model and emphasizes tool security before attaching tools to agents ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).

For real work, an agent should follow this sequence:

1. Identify the current task, target entity, and authority boundary.
2. Use lookup tools to translate human labels into safe identifiers.
3. Use list/get/summary/insight tools to retrieve only the minimum facts needed.
4. For writes, prepare a draft or proposed action first.
5. Require an approval gate for sensitive or irreversible work.
6. Execute through a narrow tool.
7. Re-read live state and report what changed.
8. Preserve enough evidence for audit, troubleshooting, and follow-up.

If a fact is not present in the source pack or visible through a live Rock inspection surface, this guide says what to inspect rather than inventing behavior.

## 2. Scope And Terminology

This guide covers Rock RMS AI Agents, agent skills, custom tools, lookup surfaces, prompt/tool boundaries, permissions, automation patterns, verification gates, and live operational review. It is written for agents and implementers who will perform real Rock work: reading person records, summarizing groups, finding registrations, drafting communications, inspecting configuration, triggering workflows, or building custom tools.

It intentionally connects multiple Rock areas because agent work does not live in one module. A safe agent implementation depends on Security, API Integrations, Workflows, Platform Configuration, Data Views, Reports, Operations, and Lava. These dependencies are explicit in the concept pack and are treated as part of the agent operating model.

Core terms:

**Agent**  
An agent is the configured Rock object that defines what skills and tools are available and what instructions guide the model's behavior. Rock's developer docs describe agents as the central point for AI in Rock and note that organizations may configure multiple agents for different audiences, such as internal staff and volunteers ([Agents](https://community.rockrms.com/developer/ai-agents/agents)).

**Skill**  
A skill groups related tools and supplies shared context. For example, a registration skill can explain how registration templates, instances, registrations, and registrants relate so that individual tools do not repeat that domain explanation. Skills also provide a convenient security boundary ([Skills](https://community.rockrms.com/developer/ai-agents/skills)).

**Tool**  
A tool is the action surface the agent can call. Rock supports tools written in Lava and native C#. Tools can retrieve data, summarize records, produce insights, or add/update data when designed for writes ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools), [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools), [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)).

**Lookup Tool**  
A lookup tool returns a small set of possible items needed as inputs to other tools. It usually has no filters and should return just enough fields for safe selection. Rock's Lava and native tool docs both present lookup tools as a load, format, return pattern ([Lava Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools), [Native Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)).

**List Tool**  
A list tool returns matching records, often with filters, but should not be treated as a full-detail read. It helps narrow candidates before a get/summary/detail tool is called. Rock's tool type guidance distinguishes lookup, list, get, summary, insights, available attributes, and add/update patterns ([Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)).

**Get Tool**  
A get tool retrieves detail for one known item. It should accept a safe identifier, typically an IdKey or similar, not a raw integer ID exposed directly to the model.

**Summary Tool**  
A summary tool returns a human-oriented rollup of one entity or a related collection. Use summaries for staff-facing explanations, review pages, and evidence gates.

**Insight Tool**  
An insight tool performs aggregation or analysis rather than retrieving one entity. Rock's Lava insight docs define the pattern as filter/aggregate, format, and return ([Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools)).

**AvailableAttributes Tool**  
An available attributes tool tells the agent what attribute keys or fields are valid for a target entity type before it attempts an update or filter. Rock identifies this as a recommended tool type in the native tool family and tool taxonomy ([Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)).

**AddOrUpdate Tool**  
An add/update tool changes Rock data. It must be narrow, permission checked, validation-heavy, and ideally guarded by an explicit approval step. Rock's native tool examples include guardrail attributes such as never sending a communication without explicit approval ([Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)).

**Context Window**  
The context window is the information available to the model during a request. Long instructions, verbose tool descriptions, large lookup payloads, and unbounded chat history compete for that space. Rock's instruction docs warn that instructions are included with every request and can affect processing time and cost ([Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions)).

**System Prompt / Instructions**  
The system prompt is built from multiple sources: core prompt, organization prompt, agent instructions, skill instructions, current person template, context anchors, and conversation history according to Rock's agent instruction docs ([Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions)).

**Context Anchor**  
A context anchor ties the session to a target entity so ambiguous follow-up questions continue to refer to the intended subject. Rock's example is a person anchor that helps keep “his wife” attached to the intended person rather than a recently mentioned child ([Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors)).

**Automation**  
Automation means a configured event causes actions to run without a staff member manually starting each step. Rock 18.1 documentation describes Automations as trigger-driven activities, and release notes identify chat-message-triggered automation as a communication feature ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

**Live Verification**  
Live verification is the act of confirming the current Rock state through UI, API, SQL, reports, logs, or model endpoints instead of trusting a generated statement. This guide treats live verification as mandatory for write decisions, security claims, financial/person data claims, and operational incident work.

## 3. AI Agents And Automation Mental Model

The safest mental model is not “chatbot with database access.” The safer model is “a controlled Rock operator with bounded tools, bounded memory, explicit context, and review gates.”

An agent request flows through several layers:

1. The person or external caller starts a chat, voice, MCP, or automation-triggered request.
2. Rock resolves the configured agent and current person/API authority.
3. Rock builds prompt context from core, organization, agent, skill, current-person, anchor, and history sources ([Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions)).
4. The model decides whether to answer directly or call an enabled tool.
5. The tool executes under Rock security and tool-specific validation.
6. The result is returned to the agent in a compact, structured format.
7. The agent explains, asks follow-up questions, proposes actions, or calls another tool.
8. For writes, approval and post-write verification should happen before the task is considered complete.

This stack has three separate boundaries that must not be blurred:

**The model boundary**  
The model can reason, summarize, ask clarifying questions, select tools, and compose drafts. It should not be trusted as the source of truth for live Rock state unless it just used a reliable tool and cites or reports the retrieved evidence.

**The tool boundary**  
Tools are the only way an agent should perform live retrieval or mutation. They must be named clearly, typed narrowly, and designed for least privilege. A tool that can update arbitrary Lava, run arbitrary SQL, or call arbitrary endpoints is usually too broad for a general-purpose agent.

**The human/review boundary**  
Some actions are too sensitive for autonomous execution even when technically possible: sending communications, changing security, updating giving data, changing workflow type configuration, editing person/family records at scale, deleting records, or changing public-facing content. These should be draft-first or approval-first workflows. Rock's native tool docs show this guardrail posture through communication examples that require explicit approval before sending ([Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)).

Automation fits beside agents, not underneath them. An automation trigger can start an action because something happened, such as a chat message. An agent can help decide, summarize, or draft. A workflow can carry state, assignments, approvals, and branching. A scheduled job can run time-based processing. A Data View can define the population. A report can expose evidence. Lava can render or transform. The strongest implementations use each Rock surface for what it does best instead of forcing all behavior into a single prompt.

## 4. Source Authority And How To Use This Guide

Use this guide as a synthesis, not as a replacement for official configuration screens or source inspection. The highest-authority records in the source pack are Rock developer docs, Rock documentation, release notes, model map entries, and Rock source-code snippets.

Authority order for this topic:

1. **Live Rock instance** for current configuration, exact version, installed plugins, security, data shape, and whether a feature is enabled.
2. **Rock source code** for entity relationships, generated REST endpoints, security annotations, save hooks, and model properties.
3. **Official Rock developer docs** for intended implementation patterns around agents, skills, tools, instructions, and context anchors.
4. **Official Rock documentation and release notes** for feature availability and operational changes.
5. **Rock Model Map** for identifying model families and categories.
6. **Community Q&A and podcasts** for examples, directional context, and operational caution, but not as primary authority for implementation facts.

Reviewed RockU media distillations can help route agent work to the right Rock area, but they are training context rather than implementation authority. For automation topics, use the approved public-safe RockU notes for [Automations Transcript Insight](https://community.rockrms.com/rocku/core-concepts/automations) at 00:25, [Data Automation Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/data-automation) at 00:15, and [Connection Request Status Automation Transcript Insight](https://community.rockrms.com/rocku/engagement/connection-request-status-automation) at 00:41 as routing and review cues, then verify exact behavior against official docs and the live Rock instance.

Use the source pack this way:

- For agent concepts and terminology, start with [AI Agents](https://community.rockrms.com/developer/ai-agents), [Agents](https://community.rockrms.com/developer/ai-agents/agents), [Skills](https://community.rockrms.com/developer/ai-agents/skills), and [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools).
- For prompt composition and instruction weight, use [Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions).
- For context stability, use [Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors) and source model records for `AIAgentSessionAnchor`.
- For tool categories, use [Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools).
- For Lava tool implementation, use [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools), [Lava Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools), and [Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools).
- For native C# tool implementation, use [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools), [Native Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools), [Rock Tool Helper](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper), and [Gotchas](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/gotchas).
- For generated model/API landmarks, use the Rock GitHub files listed in Section 14.
- For release caveats, use [Rock Core Release Notes](https://www.rockrms.com/releasenotes) and [Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9).

When this guide says “verify live,” inspect the live Rock instance through the relevant surface: Admin Tools, AI Agents settings, AI Skills, security dialogs, Inspect Security, Power Tools/API, model endpoints, Data Views, reports, workflow history, job history, exception logs, communication history, or direct SQL if that is part of your organization's approved read-only support process.

## 5. Core Configuration And Data Model

The core configuration starts in Rock's AI Agent settings area. Rock's tool type docs direct administrators to `Admin Tools > Settings > AI Agents > AI Skills` to inspect default tools for a skill ([Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)). In a live instance, inspect both the agent list and skill/tool configuration because the exact fields, installed defaults, and UI labels may vary by Rock version.

At minimum, inspect these configuration surfaces:

- AI Agents list.
- Individual agent detail.
- Agent instructions.
- Public vs internal usage setting.
- Chat vs MCP usage setting, if present.
- Skills attached to the agent.
- Skill security.
- Skill instructions.
- Tools attached to each skill.
- Tool type, name, description, parameters, prompt/code, and security.
- Context anchor support and current session anchors.
- Prompt templates or organization-level instructions.
- Current person template.
- Enabled mobile/voice surfaces.
- API or MCP exposure settings.
- Logs/session history retention settings, if available.

Rock's source model snippets identify several AI domain models:

- `AIAgent`
- `AIAgentSession`
- `AIAgentSessionAnchor`
- `AIAgentSessionHistory`
- `AIAgentSkill`

The Model Map source records place these in the AI category ([Model Map](https://community.rockrms.com/ModelMap)). The source snippets provide deeper operational detail:

`AIAgentSession` represents an existing chat session for a specific agent and person. The class includes an `AIAgentId`, a `PersonAliasId`, navigation to `AIAgent`, navigation to `PersonAlias`, and collections of `AIAgentSessionHistory` and `AIAgentSessionAnchor` records ([AIAgentSession.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSession/AIAgentSession.cs)). The snippet also shows `CodeGenExclude( CodeGenFeature.DefaultRestController )` and `CodeGenerateRest( DisableEntitySecurity = true )`, which means implementers should inspect the generated v2 endpoints and security annotations rather than assuming normal v1 generated controller behavior.

`AIAgentSessionHistory` represents messages associated with a session. The source excerpt shows `AIAgentSessionId`, message role, and a required relationship back to `AIAgentSession`, with cascade delete from session to history ([AIAgentSessionHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionHistory/AIAgentSessionHistory.cs)).

`AIAgentSessionAnchor` represents an anchor for additional context in a session. The class stores the session, entity type, entity ID, and additional settings. The source comment states the intent: anchor a session to an entity such as a person or group, and avoid multiple anchors on the same entity type ([AIAgentSessionAnchor.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchor.cs)). Its service includes `UpdateFromEntity`, and the excerpt shows special handling beginning with `Person`, which means anchor display/context content is not just raw entity IDs but derived from entity-specific logic ([AIAgentSessionAnchorService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchorService.cs)).

`AIAgentSkill` is the join between an agent and a skill. The source excerpt shows required `AIAgentId` and `AISkillId`, navigation to `AIAgent` and `AISkill`, and cascade delete on both relationships ([AIAgentSkill.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.cs)). Its save hook flushes the agent cache after save, which is operationally important: after adding/removing skills, the agent's cached configuration should rebuild ([AIAgentSkill.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.SaveHook.cs)).

Save hooks also set timestamps on session, anchor, and history records when added if defaults were not already set, according to the source snippets for `AIAgentSession.SaveHook`, `AIAgentSessionAnchor.SaveHook`, and `AIAgentSessionHistory.SaveHook` ([AIAgentSession.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSession/AIAgentSession.SaveHook.cs), [AIAgentSessionAnchor.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchor.SaveHook.cs), [AIAgentSessionHistory.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionHistory/AIAgentSessionHistory.SaveHook.cs)).

For live verification, inspect:

- Whether the Rock version has the AI models installed.
- Whether the tables exist and match the source branch being referenced.
- Whether generated v2 endpoints are enabled in the target environment.
- Whether the current person/API key has the required v2 model endpoint permissions.
- Whether entity security is intentionally disabled at the generated endpoint layer and replaced with controller action security, session ownership checks, or other service logic.
- Whether the organization's configured retention policy treats session history as sensitive data.

## 6. Primary Entities And Relationships

The core relationship graph is:

`AIAgent` -> many `AIAgentSkill` -> `AISkill`  
`AIAgent` -> many `AIAgentSession`  
`PersonAlias` -> many `AIAgentSession`  
`AIAgentSession` -> many `AIAgentSessionHistory`  
`AIAgentSession` -> many `AIAgentSessionAnchor`  
`AIAgentSessionAnchor` -> one `EntityType` and one target entity ID

The `AIAgentSession` source says the session is for a specific agent and person, and the `PersonAliasId` is used so one person cannot view another person's chat history ([AIAgentSession.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSession/AIAgentSession.cs)). That statement should shape every agent-history report, API integration, or admin tool. A session history viewer must not simply list all records for anyone who can hit a generated endpoint. It must preserve the intended ownership boundary or require a clearly authorized administrative role.

The `AIAgentSessionHistory` source shows a required parent session and cascade delete. If a session is deleted, history records should be expected to delete with it in the code branch represented by the source snippet ([AIAgentSessionHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionHistory/AIAgentSessionHistory.cs)). Verify this in the live database before building a cleanup job or compliance export because schema can vary by version and migration state.

The `AIAgentSessionAnchor` source shows a required parent session and an entity reference through `EntityType` plus entity ID ([AIAgentSessionAnchor.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchor.cs)). Because anchors point at arbitrary entity types, anchor handling must respect the target entity's security and sensitivity. A person anchor, group anchor, workflow anchor, financial account anchor, or registration anchor should not all be treated equally.

The `AIAgentSkill` relationship is a classic join between `AIAgent` and `AISkill`, with cascade delete on both parent relationships in the source snippet ([AIAgentSkill.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.cs)). Operationally, this means removing an agent or skill can remove join rows. It does not mean removing a skill is safe without review; it may alter what tools an agent can call and can invalidate staff workflows.

Recommended relationship checks before changing an agent:

- Count the skills attached to the agent.
- List tools under each skill.
- Record tool names, types, write capability, and security.
- Identify sessions using the agent.
- Identify whether the agent is used by docked chat, public chat, MCP, mobile voice, or automations.
- Confirm whether removing a skill affects cached configuration and whether cache flush occurs automatically.
- Confirm whether agent session history should remain after an agent is disabled or removed.

## 7. Common AI Agents And Automation Workflows

### Staff Person Research

A staff member asks: “Summarize Ted Decker's family, recent attendance, and active serving roles.”

A safe workflow:

1. Use a person lookup/list tool to identify the person by name.
2. If multiple matches exist, ask the user to choose.
3. Set or rely on a person context anchor.
4. Use get/summary tools for family, attendance, and serving.
5. Cite the live surfaces used in the response.
6. Avoid exposing sensitive fields unless the staff user has access.
7. If the user asks to change a record, switch to draft/approval mode.

The context anchor matters because follow-up questions like “What about his wife?” can otherwise drift to the wrong recently mentioned person. Rock's context anchor docs describe this exact ambiguity class ([Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors)).

### Group Lookup And Membership Insight

A staff member asks: “Which small groups have more than ten active members but no leader?”

Use the tool taxonomy:

1. Lookup group types or campuses if needed.
2. Run an insight tool that aggregates group membership by status and role.
3. Return counts and candidate group IdKeys/names.
4. Offer a get/summary tool for a selected group.
5. Do not update roles without explicit confirmation.

This is a good insight-tool use case because the question is analytic rather than “fetch one record.” Rock's insight tool pattern is specifically for filtered, aggregated output ([Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools)).

### Event Registration Support

A staff member asks: “Find people registered for Men's Retreat who still owe a balance and draft a reminder.”

A safe agent does not jump straight to communication. It should:

1. Lookup registration instances or event names.
2. List matching registrations with safe identifiers.
3. Get balance/status details through authorized finance/event tools.
4. Draft the reminder only.
5. Require explicit approval before sending.
6. Use a communication tool with a hard guardrail: no send without approval.
7. Verify the communication record after sending.

Rock's skill docs use event registration as an example of a domain where shared skill context can explain relationships among templates, instances, registrations, and registrants ([Skills](https://community.rockrms.com/developer/ai-agents/skills)). Rock's native tool docs show guardrail patterns around communications ([Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)).

### Connection Request Creation

A user asks: “Add a connection request for Ted Decker. He is interested in greeters. High importance.”

Safe flow:

1. Lookup the person.
2. Lookup connection types/opportunities, preferably through a cache-backed native lookup tool when available.
3. Confirm exact person and opportunity if ambiguous.
4. Prepare the add request.
5. Use an add/update tool that validates IdKeys and current person's authorization.
6. Return the created request's safe reference and a post-create summary.

Rock's debugging docs use a similar example when explaining how to ask an agent to explain which tools it considered ([Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)).

### Chat Message Automation

Rock release notes identify a Chat Message automation trigger and a fallback chat notification automation event in the Communication module for Rock 18.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Treat this as an automation surface, not a generic agent capability. Before using it:

- Verify the installed Rock version.
- Inspect the automation trigger type list.
- Inspect the event/action configuration.
- Confirm the chat channel, recipient population, and notification fallback rules.
- Confirm whether email/SMS fallback touches communication preferences or compliance rules.
- Test with a non-production group before broad rollout.
- Review resulting communication records and failure logs.

### Mobile Voice Agent

The mobile Voice Agent block is documented as a conversational voice assistant that opens a live audio session, streams microphone input, plays spoken responses, and can show a transcript. The docs mark it `C 19.0 S 19.0` and describe using it for questions exposed through an MCP agent ([Voice Agent](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/voice-agent)).

Operationally, voice increases the need for narrow tools and clear confirmation. A voice UI is faster and more ambiguous than typed admin work. Use it for read-only self-service or heavily guarded actions unless the live Rock configuration proves appropriate security and consent patterns.

Verify live:

- Block settings.
- Personal settings.
- Permissions.
- Whether transcript display is enabled.
- Which agent/MCP endpoint the block uses.
- Whether the user is authenticated.
- Whether the exposed tools are appropriate for a mobile audience.
- Whether audio/transcript handling meets organizational privacy policy.

## 8. Agent Tools And Lookup Surfaces Deep Dive

Rock's recommended tool taxonomy is based on verb prefixes: lookup, list, get, summary, insights, available attributes, and add/update ([Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)). Tool names matter because the model uses the name and description to decide which tool to call. A vague tool name creates routing errors. A broad tool description creates overuse. A missing tool creates guessing.

### Lookup Tools

Lookup tools are for translating human language into stable, safe inputs for other tools. A lookup should generally return all candidates when the set is small enough for context. Examples include campuses, group types, connection types, defined value sets, financial accounts visible to the user, or registration templates.

Rock's Lava lookup docs describe the pattern as loading data, formatting it, and returning it ([Lava Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools)). The native lookup docs add an important implementation preference: use cache objects when possible, and filter by active status and authorization when relevant ([Native Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)).

A good lookup result contains:

- Display name.
- Safe identifier such as IdKey.
- Optional short qualifier such as campus, status, or parent name.
- Only fields required by downstream tools.
- No raw integer IDs unless the tool documentation for the target Rock version explicitly makes that safe for the model.

A bad lookup result contains:

- Hundreds or thousands of records without filtering.
- Raw integer IDs exposed to the model.
- Sensitive fields not needed for selection.
- Large descriptions that consume context.
- Inactive or unauthorized records mixed with active authorized records.
- Ambiguous labels without enough disambiguation.

### List Tools

List tools return candidate records matching filters. Use list tools when the set is too large for a lookup or when the user supplies search criteria. A person list tool, for example, should not return every person. It should accept search terms, campus, status, or other constrained filters and return a limited candidate set.

A list tool should answer: “Which records might the user mean?” It should not answer: “Here is every detail about each record.” Follow with a get or summary tool for details.

### Get Tools

A get tool retrieves one entity by safe identifier. It should be used after lookup/list selection. It should validate the identifier, check authorization, and return a predictable shape. For sensitive records, use role-aware output. For example, a person get tool for a staff agent may include family and contact data, while a volunteer agent may only include name and public serving information.

### Summary Tools

Summary tools assemble domain-specific context. They are useful for agents because they reduce multi-tool chatter and present a coherent evidence bundle. A person summary might include household, connection requests, recent interactions, and active group membership. A workflow summary might include status, current activities, assignments, and last action date.

Do not let summary tools become unbounded data dumps. Decide what operational question the summary supports.

### Insight Tools

Insight tools aggregate. They are appropriate for questions like:

- “How many open connection requests are older than 14 days?”
- “Which groups have no active leaders?”
- “Which registration instances have unpaid balances?”
- “Which workflows are stuck in the same activity?”

Rock's Lava insight guidance frames the pattern as filtering/aggregating, formatting, and returning ([Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools)). Inputs should be filters. Outputs should be intentionally shaped metrics and candidate records.

### AvailableAttributes Tools

Use available-attributes tools before allowing an agent to update entity attributes or build attribute filters. Attribute keys are often site-specific, and the model cannot know them reliably. A tool should return the exact attribute keys, names, field types, allowed values, and whether each is writable for the current user.

Verify live:

- Entity type.
- Attribute category.
- Attribute key.
- Field type.
- Defined type/defined value dependency.
- Whether attribute values are inherited, entity-specific, or global.
- Whether security applies at the entity, attribute, category, or edit block level.

### AddOrUpdate Tools

Add/update tools are write tools. They should be narrow and high-friction by design.

A safe add/update tool requires:

- Specific operation name.
- Specific target entity type.
- Safe input identifiers.
- Strong validation.
- Authorization checks.
- Clear preview output.
- Explicit approval for sensitive changes.
- Post-write readback.
- Helpful error reporting.
- Audit trail or workflow handoff when appropriate.

Do not build a generic “run SQL” or “update any entity” agent tool for routine staff use. If such a tool exists for an internal admin agent, isolate it behind strong security, logging, and human review.

## 9. Permissions And Data Boundaries Deep Dive

Rock's custom tool guidance states that tools inherit Rock's security and that a person can only run a tool if they have access to it ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)). This is necessary but not sufficient. A safe implementation also needs data minimization, prompt minimization, output minimization, and review gates.

Security layers to verify:

- User authentication.
- Person role membership.
- Agent access.
- Skill access.
- Tool access.
- Target entity authorization.
- Attribute authorization.
- API endpoint authorization.
- Workflow type/view/edit authorization.
- Page/block authorization.
- Communication permissions.
- Data View/report permissions.
- External provider/API permissions.

Rock's Admin Hero Guide describes the broader Rock security model, including security roles, inherited permissions, elevated security levels, and the Inspect Security/Verify Security block for checking effective permissions ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)). For agent work, Inspect Security is not optional when behavior does not match expectations. Use it to verify the current person's effective permissions on the relevant entity type and entity ID.

### Public vs Internal Agents

Rock's agent docs distinguish public and internal use cases ([Agents](https://community.rockrms.com/developer/ai-agents/agents)). A public agent should be treated as hostile-environment software. It should expose only tools safe for anonymous or minimally authenticated users. An internal staff agent can have broader capabilities, but still should be segmented by role.

Public agent rules:

- No broad person search.
- No private family data.
- No financial/giving detail unless authenticated and scoped to the current person.
- No arbitrary workflow launch with user-controlled payloads.
- No raw API access.
- No unrestricted Lava/webrequest execution.
- No staff-only report data.
- No security configuration data.

Internal agent rules:

- Segment by staff role.
- Avoid all-staff access to finance, counseling, HR, security, and system administration tools.
- Keep volunteer-facing agents separate from staff agents.
- Prefer read-only tools before write tools.
- Require approval for communication and record mutation.

### Raw ID Boundary

Rock's custom tool docs warn not to expose raw Rock integer IDs to the model ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)). Use IdKeys or another safe abstraction. The operational reason is simple: a model that sees raw IDs may reuse them incorrectly, interpolate them into future calls, or mix IDs across entity types.

Safe pattern:

1. Lookup returns `name` and `idKey`.
2. List returns `displayName`, `idKey`, and disambiguators.
3. Get accepts only `idKey`.
4. Add/update accepts only `idKey` for related entities.
5. Tool internally resolves IdKey to integer ID.
6. Tool validates entity type and authorization before use.

### Sensitive Data Classes

Treat these as sensitive by default:

- Person identity and contact information.
- Children and family relationships.
- Attendance patterns.
- Giving/financial records.
- Prayer/care/counseling notes.
- Background checks.
- Security roles and elevated permissions.
- Workflow payloads.
- Communication history.
- API keys and tokens.
- Attribute values that encode private ministry, HR, medical, legal, or pastoral context.

If a tool must expose sensitive data, document:

- Why the data is needed.
- Which agent can use it.
- Which skill contains it.
- Which roles can run it.
- What fields it returns.
- What it never returns.
- Whether results are stored in session history.
- How users can audit access.

### Generated v2 Endpoint Boundary

The source snippets for AI models show generated v2 controllers with routes such as:

- `api/v2/models/aiagents`
- `api/v2/models/aiagentskills`
- `api/v2/models/aiagentsessions`
- `api/v2/models/aiagentsessionanchors`
- `api/v2/models/aiagentsessionhistories`

The generated controller snippets show authentication and `EXECUTE_UNRESTRICTED_READ` / `EXECUTE_UNRESTRICTED_WRITE` action security annotations for read/write operations, with entity security disabled in the model code generation attributes ([AIAgentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentsController.CodeGenerated.cs), [AIAgentSessionsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSessionsController.CodeGenerated.cs), [AIAgentSessionHistoriesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSessionHistoriesController.CodeGenerated.cs)). Do not expose these endpoints to integrations without verifying exact permission grants, endpoint availability, and whether the endpoint behavior enforces the ownership expectations documented in the models.

## 10. Automation Design And Workflows Deep Dive

Automation in Rock should be designed as event-driven operations with explicit scope. Rock 18.1 documentation describes Automations as trigger-driven activities ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)). Release notes mention a Chat Message trigger and fallback chat notification event in Communication ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

The reviewed RockU automation lessons reinforce the same operational posture: treat automation training as a way to identify the right Rock surface and review path, not as a substitute for live configuration checks. Use [Automations Transcript Insight](https://community.rockrms.com/rocku/core-concepts/automations) at 00:25 for general automation routing, [Data Automation Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/data-automation) at 00:15 when the automation depends on reporting or population logic, and [Connection Request Status Automation Transcript Insight](https://community.rockrms.com/rocku/engagement/connection-request-status-automation) at 00:41 when connection-process status changes or ministry follow-up workflows are involved.

A mature automation design answers:

- What event starts it?
- What entity is the event about?
- What population is in scope?
- What permissions are required?
- What data is read?
- What data is changed?
- What happens on failure?
- What evidence is retained?
- Who reviews exceptions?
- How is the automation disabled quickly?

Agents and automations should cooperate through Rock-native state where possible:

- Use **Workflows** for stateful approvals, assignments, retries, and human review.
- Use **Data Views** for population definitions.
- Use **Reports** for operational monitoring.
- Use **Lava** for rendering, formatting, and low-code tool logic.
- Use **Jobs** for scheduled background processing.
- Use **API integrations** for external systems.
- Use **AI tools** for selection, summarization, drafting, and bounded actions.

### Trigger Design

A trigger should be specific enough that downstream logic is simple. Avoid triggers that fire on every broad event and rely on the agent to decide whether anything matters. The agent should not be the primary filter for noisy or sensitive automation.

Good trigger examples:

- New chat message in a specific channel.
- Registration completed for a specific template.
- Workflow entered a specific activity.
- Connection request remains open past a threshold.
- Data View population changed, if supported by the installed version and architecture.
- Scheduled review window for stale records.

Weak trigger examples:

- Any person updated.
- Any workflow changed.
- Any communication sent.
- Any chat message anywhere.
- Any entity interaction, without filtering.

### Action Design

Actions should be idempotent where possible. If the automation reruns, it should not duplicate communications, create duplicate connection requests, or repeatedly overwrite the same value.

Use these patterns:

- Store a marker attribute or workflow action date.
- Check existing open records before creating a new one.
- Use unique keys when integrating externally.
- Log run IDs.
- Re-read after write.
- Send failures to an exception workflow or report.

### Agent-In-The-Loop Automation

A strong pattern is “automation gathers, agent drafts, human approves, tool executes.”

Example: chat support escalation.

1. Chat message trigger fires.
2. Automation gathers message, sender, channel, and recent context.
3. Agent drafts an internal summary and recommended response.
4. Workflow assigns review to a staff role.
5. Staff approves or edits.
6. Communication tool sends.
7. Automation records outcome and fallback notification status.

### Agent-As-Reviewer Automation

An agent can classify or summarize data for human review without writing to core records. This is useful for:

- Categorizing open-ended form responses.
- Summarizing care request themes.
- Drafting follow-up tasks.
- Ranking stale workflow queues.
- Explaining why a report row appears.
- Preparing weekly operational summaries.

Still verify outputs against live records. The agent's classification is a recommendation unless written and approved through a controlled workflow.

## 11. Verification And Review Gates Deep Dive

Every agent workflow should define verification gates. The correct gate depends on risk.

### Read-Only Low-Risk Gate

For low-risk reads, the agent should cite the tool result in plain language and identify ambiguity.

Examples:

- “I found two matching people. Which one do you mean?”
- “The group appears active, but I did not inspect schedule/capacity.”
- “This is based on current list results; open the record for full detail.”

### Sensitive Read Gate

For sensitive reads, verify authorization and minimize output.

Examples:

- Giving summaries.
- Care/counseling notes.
- Family relationships involving minors.
- Background check status.
- Security role membership.

The agent should say what it inspected, not dump everything it saw.

### Write Preview Gate

Before a write, show the exact proposed change:

- Target entity.
- Current value.
- New value.
- Reason.
- Tool to be used.
- Consequences.
- Whether notification will be sent.

Require explicit approval. Avoid interpreting vague approval for a different action.

### Post-Write Verification Gate

After a write:

1. Re-read the target record.
2. Confirm the field or related record changed.
3. Report created IDs as safe references, not raw IDs where possible.
4. Record any side effects.
5. Surface failures or partial success.

### Security Review Gate

Before attaching a tool to a production agent:

- Verify tool security.
- Verify skill security.
- Verify agent security.
- Test as a user with expected access.
- Test as a user without expected access.
- Test with ambiguous input.
- Test with invalid IdKey.
- Test with unauthorized target entity.
- Test with large result sets.
- Test with sensitive fields.
- Confirm session history does not leak data to unauthorized users.

Rock's Inspect Security/Verify Security block is the live tool to understand effective permissions when access is confusing ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)).

### Debugging Gate

When the agent chooses the wrong tool, Rock's debugging docs suggest adding instructions asking the model to explain which tools it considered and why it did or did not call them ([Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)). Use this in development and test contexts. Do not expose internal reasoning prompts as a routine production user feature unless your organization is comfortable with that behavior.

## 12. Related Rock Areas: Security, Api Integrations, Workflows, Platform Configuration, Data Views, Reports, Operations, Lava

### Security

Security is the first dependency. Agents do not replace Rock security; they amplify the consequences of misconfiguration. Review roles, inherited permissions, item permissions, elevated security levels, and effective access through Inspect Security ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)).

### API Integrations

AI tools and external agents may use Rock APIs, including generated v2 model endpoints. The source snippets show AI model endpoints under `api/v2/models/...` with authenticated, secured operations ([AIAgentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentsController.CodeGenerated.cs)). Verify API key permissions, endpoint security, and version-specific behavior. Rock 17.5 release notes fixed a DataView endpoint permission issue where permission checks could target the wrong entity ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)); this is a reminder to verify behavior on the installed version rather than assuming endpoint authorization is always obvious.

### Workflows

Workflows are the best place for stateful human review. Use them for approval, escalation, exception handling, retries, and assignment. Agents can draft workflow notes, summarize context, or propose next actions, but workflows should own operational state.

### Platform Configuration

Platform settings can affect prompts, organization context, enabled providers, API access, mobile blocks, security roles, and Lava availability. Inspect global AI settings, organization prompts, current person templates, and any provider credentials in the live instance. Do not infer these from source docs alone.

### Data Views

Data Views are useful for defining populations, but agents should not blindly execute DataView-driven actions. Verify Data View filters, entity type, security, and result counts. If using model DataView endpoints, account for version-specific permission behavior such as the Rock 17.5 fix noted above ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Reports

Reports are the audit surface for agent-enabled operations. Build reports for:

- Tool usage.
- Sessions by agent.
- Recent sensitive requests.
- Failed tools.
- Automation runs.
- Communications drafted/sent.
- Records changed by automation.
- Exception queues.
- Security review status.

### Operations

Operational work includes monitoring, cache behavior, exception logs, job history, retention, backup, and rollback. The `AIAgentSkill` save hook flushing the agent cache is a source-code signal that cached agent configuration exists and can matter after changes ([AIAgentSkill.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.SaveHook.cs)). If a change does not appear to take effect, verify cache behavior before assuming the tool is broken.

### Lava

Lava is a first-class way to build tools. Rock's Lava tool docs describe tools with name, description, prompt, and parameters, and note that Lava can use SQL and Entity Commands ([Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)). Lava is powerful enough to change data; treat Lava tool prompts as code, review them, and secure them accordingly.

## 13. Administration And Operational Guardrails

Recommended guardrails:

- Maintain separate agents for public, volunteer, staff, finance, system admin, and experimental work.
- Keep public agents read-only unless a specific workflow requires authenticated, narrow writes.
- Attach tools through skills, not ad hoc sprawl.
- Secure skills before adding tools.
- Use explicit tool naming and descriptions.
- Avoid raw IDs in model-visible input/output.
- Prefer IdKey-based inputs.
- Validate all tool parameters.
- Use pagination and hard result limits.
- Use cache objects for stable lookup data when available.
- Return compact structured results.
- Store enough evidence for review, but do not over-retain sensitive session content.
- Require approval for communications, deletions, security changes, financial changes, and broad updates.
- Run role-based testing before production release.
- Review release notes before upgrading AI/automation behavior.
- Maintain a rollback plan for agent configuration changes.

Operational checks:

- List all agents and classify audience.
- List all skills attached to each agent.
- Identify write-capable tools.
- Identify tools that call SQL, Entity Commands, APIs, or external services.
- Identify tools that expose sensitive data.
- Verify security for each skill/tool.
- Verify session history access.
- Verify mobile/voice exposure.
- Verify automation triggers/actions.
- Verify provider credentials and quotas.
- Review exception logs after agent tests.
- Review communication logs after communication-tool tests.
- Review workflow history for approval paths.

For live review, build an “AI Agent Inventory” report or dashboard that includes agent, audience, enabled skills, tool count, write tool count, security roles, last modified date, active sessions, and owner/reviewer.

## 14. Developer, API, Lava, And Source-Code Landmarks

### Developer Docs

Primary developer documentation:

- [AI Agents](https://community.rockrms.com/developer/ai-agents)
- [Agents](https://community.rockrms.com/developer/ai-agents/agents)
- [Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions)
- [Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors)
- [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)
- [Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)
- [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)
- [Lava Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools)
- [Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools)
- [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)
- [Native Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)
- [Rock Tool Helper](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper)
- [Native Tool Gotchas](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/gotchas)
- [Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)

### Source-Code Landmarks

Use these files as source-code anchors for model/API behavior:

- [`Rock/Model/AI/AIAgent/AIAgentService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgent/AIAgentService.cs)
- [`Rock/Model/AI/AIAgentSession/AIAgentSession.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSession/AIAgentSession.cs)
- [`Rock/Model/AI/AIAgentSession/AIAgentSession.SaveHook.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSession/AIAgentSession.SaveHook.cs)
- [`Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchor.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchor.cs)
- [`Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchorService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionAnchor/AIAgentSessionAnchorService.cs)
- [`Rock/Model/AI/AIAgentSessionHistory/AIAgentSessionHistory.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSessionHistory/AIAgentSessionHistory.cs)
- [`Rock/Model/AI/AIAgentSkill/AIAgentSkill.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.cs)
- [`Rock/Model/AI/AIAgentSkill/AIAgentSkill.SaveHook.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.SaveHook.cs)

Generated v2 REST controllers:

- [`AIAgentsController.CodeGenerated.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentsController.CodeGenerated.cs)
- [`AIAgentSkillsController.CodeGenerated.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSkillsController.CodeGenerated.cs)
- [`AIAgentSessionsController.CodeGenerated.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSessionsController.CodeGenerated.cs)
- [`AIAgentSessionAnchorsController.CodeGenerated.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSessionAnchorsController.CodeGenerated.cs)
- [`AIAgentSessionHistoriesController.CodeGenerated.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSessionHistoriesController.CodeGenerated.cs)

### Native Tool Development

Native tools inherit from `AgentSkillComponent` according to Rock's native tool docs ([Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)). Use native tools when you need compiled logic, heavier database work, external API integration, shared services, strong validation, or better testability.

Rock Tool Helper exists to standardize repetitive native-tool concerns such as validation, error collection, pagination, safe entity access, attribute handling, update methods, save methods, and summaries ([Rock Tool Helper](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper)). Use it instead of hand-rolling inconsistent error behavior.

Native tool gotcha: when projecting queryable objects in LINQ to Entities, object initialization shape must be identical when the same result type is initialized in more than one place. Rock's gotchas page calls this out because otherwise EF can throw a structurally incompatible initialization error ([Gotchas](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/gotchas)).

### Lava Tool Development

A Lava tool has name, description, prompt, and parameters. The model uses the name and description for tool selection, so those fields are part of behavior, not decoration ([Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)).

Lava tools are useful for:

- Quick lookups.
- Low-code summaries.
- SQL-backed insights.
- Formatting outputs.
- Internal admin experiments.
- Site-specific workflows where compiled deployment is too heavy.

Use native tools instead when:

- Complex authorization is required.
- The tool changes sensitive records.
- The logic is shared across agents.
- You need robust tests.
- You need external API integration with secrets.
- You need consistent pagination/errors.
- Performance matters.

## 15. Reporting, Analytics, And Model Map

The source pack includes Model Map records for AI Agent, AI Agent Session, AI Agent Session Anchor, AI Agent Session History, and AI Agent Skill, all in the AI category ([Model Map](https://community.rockrms.com/ModelMap)). Use the Model Map as a discovery layer, then verify exact columns and relationships in the live database or source branch.

Recommended reports:

**Agent Inventory**  
Agent name, audience, active status, public/internal classification, chat/MCP/mobile use, owner, reviewer, last modified.

**Skill Inventory**  
Skill name, description, instructions present, security roles, attached agents, tool count, write tool count.

**Tool Inventory**  
Tool name, type, implementation type, parameters, security, sensitive data flag, write flag, external API flag, SQL/Lava flag.

**Session Activity**  
Agent, current person/person alias, session start, last message, message count, anchor count. Confirm access rules before exposing this report.

**Sensitive Tool Usage**  
Tool calls involving finance, person data, family data, workflow payloads, security, communications, or API keys.

**Automation Outcomes**  
Trigger, action, entity, started date, completed date, result, exception, retry count.

**Post-Write Verification Failures**  
Any write tool where readback did not match expected state.

**Security Review Dashboard**  
Agents/skills/tools missing owner, missing review date, containing write tools, or exposed to broad roles.

Analytics cautions:

- Session history may contain sensitive user input and retrieved data.
- Summaries can leak sensitive data even if the original fields are secured elsewhere.
- Anchors can reveal entity interest even if the agent did not print details.
- Tool failures can include identifiers or validation details.
- Reports should apply role security and retention policy.

## 16. Version And Release Caveats

Version matters. The source pack reflects records retrieved on June 3, 2026, including Rock release pages and source snippets from the `develop` branch. Do not assume every feature exists in a production instance.

Known caveats from the pack:

- Rock release notes list Rock v19.1 as released May 20, 2026 and currently in Beta at retrieval time, with many module sections visible on the release page ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Rock release notes list Rock v18.3 as released May 20, 2026 and currently in Alpha at retrieval time ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Rock 18.1 documentation notes Automations and entity interaction tracking updates ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)).
- Rock 18.1 release notes mention the Chat Message automation trigger and Send Fallback Chat Notification automation event ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Rock 17.5 release notes fixed a DataView endpoint permission issue that could deny access even when a Person or API Key had explicit DataView permission ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- The mobile Voice Agent block is marked `C 19.0 S 19.0` in mobile docs ([Voice Agent](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/voice-agent)).
- Podcast records mention AI Agents in v19/v20 roadmap discussions, but use podcasts as directional context, not as configuration authority ([Rock Cast Ep 202](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision), [Rock Cast Ep 212](https://shows.acast.com/rock-cast/episodes/rock-cast-episode-212)).

Before implementing, verify:

- Installed Rock version.
- Whether AI Agent pages exist.
- Whether the organization has enabled the relevant provider/integration.
- Whether the AI models/tables exist.
- Whether the generated v2 endpoints are available.
- Whether mobile Voice Agent is available for the installed app/server versions.
- Whether Automation trigger/action types exist.
- Whether release-note fixes are present in the environment.

## 17. Implementation Playbooks

### Playbook: Build A Read-Only Staff Agent

1. Define audience: staff only.
2. Identify top read tasks: person lookup, group summary, connection request status, registration summary, workflow queue summary.
3. Create or select an agent.
4. Write short agent instructions: be precise, ask when ambiguous, use tools for live data, do not infer missing records.
5. Attach only read-only skills.
6. Review skill security.
7. Review each tool's returned fields.
8. Test as admin.
9. Test as ordinary staff user.
10. Test as unauthorized user.
11. Review session history output.
12. Publish with owner and review date.

### Playbook: Build A Custom Lookup Tool

1. Decide downstream tool input.
2. Return only safe identifiers and display labels.
3. Prefer cache objects in native tools when available ([Native Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)).
4. Filter inactive records unless there is a clear reason not to.
5. Filter unauthorized records.
6. Keep result count small enough for context.
7. Add disambiguators.
8. Test empty, one-result, multi-result, unauthorized, and large-result cases.
9. Confirm no raw integer IDs are visible to the model.
10. Attach to the correct skill and secure it.

### Playbook: Build A Lava Insight Tool

1. Define the operational question.
2. Define filter parameters.
3. Use SQL or entity commands as appropriate.
4. Aggregate in the query where possible.
5. Format compactly.
6. Return metrics plus a small candidate list.
7. Include caveats if the result depends on status values, date windows, or site-specific attributes.
8. Test with known records.
9. Verify performance on production-sized data.
10. Secure the skill/tool.

Rock's insight docs support the filter/aggregate/format/return pattern ([Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools)).

### Playbook: Build A Native AddOrUpdate Tool

1. Define one write operation.
2. Use `AgentSkillComponent`.
3. Use Rock Tool Helper patterns for validation and errors where possible ([Rock Tool Helper](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper)).
4. Accept IdKeys, not raw IDs.
5. Resolve and authorize every target entity.
6. Validate field values.
7. Return a preview before write if the workflow supports it.
8. Require explicit approval for sensitive actions.
9. Save through Rock services.
10. Re-read and return a concise confirmation.
11. Log or expose enough audit data for review.
12. Test invalid values and unauthorized targets.

### Playbook: Add A Skill To An Agent

1. Inspect current agent and attached skills.
2. Inspect the new skill's tools.
3. Review write tools.
4. Review skill instructions.
5. Review skill security.
6. Attach the skill.
7. Confirm cache refresh or manually clear cache if behavior indicates stale configuration. The source save hook for `AIAgentSkill` flushes agent cache on save in the referenced branch ([AIAgentSkill.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/AI/AIAgentSkill/AIAgentSkill.SaveHook.cs)).
8. Test tool availability.
9. Test unauthorized access.
10. Update inventory/reporting.

### Playbook: Configure Chat Message Automation

1. Verify Rock version supports the trigger/action.
2. Inspect Automation triggers for Chat Message.
3. Define channel/population scope.
4. Define action: notify, create workflow, summarize, assign, or fallback notification.
5. Confirm communication preferences and fallback routes.
6. Test in a limited channel.
7. Review generated workflow/communication records.
8. Add monitoring report.
9. Document disable steps.

## 18. Troubleshooting Decision Tree

### Agent Does Not Call The Expected Tool

Check:

1. Is the tool attached to a skill?
2. Is the skill attached to the agent?
3. Does the user have access to the agent, skill, and tool?
4. Is the tool name clear?
5. Does the tool description match the request?
6. Do agent or skill instructions discourage the tool?
7. Is the request ambiguous?
8. Is cached configuration stale?
9. Does a similar tool have a better name/description?
10. Use debugging instructions in a test prompt to ask what tools were considered ([Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)).

### Tool Returns No Records

Check:

1. Current person's authorization.
2. Active/inactive filters.
3. Campus/group/entity filters.
4. Date filters and timezone.
5. IdKey decoding.
6. Attribute key spelling.
7. Data View/report security.
8. Whether the record exists in live Rock.
9. Whether the tool is using stale cache.
10. Whether SQL joins accidentally exclude rows.

### Tool Returns Too Much Data

Check:

1. Missing filters.
2. Lookup used where list was needed.
3. Summary returning raw child collections.
4. Sensitive fields included unnecessarily.
5. Lack of pagination.
6. No result cap.
7. Overly broad current-person access.
8. Tool description causing overuse.

### Write Tool Fails

Check:

1. Approval was explicit.
2. IdKey resolves.
3. Target entity exists.
4. Current person has edit/write permission.
5. Required fields are present.
6. Attribute field values are valid.
7. Workflow/activity state allows the change.
8. Save validation errors.
9. ExceptionLog.
10. Post-write readback.

### Permissions Look Wrong

Check:

1. Tool security.
2. Skill security.
3. Agent security.
4. Entity security.
5. Page/block security.
6. Security role membership.
7. Elevated security levels.
8. Inherited permissions.
9. API key permissions.
10. Inspect Security / Verify Security for the person, entity type, and entity ID ([Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)).

### API Endpoint Denies Access

Check:

1. Authentication.
2. API key/person permissions.
3. Generated v2 route path.
4. Required action security such as unrestricted read/write in generated controller snippets ([AIAgentSessionsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AIAgentSessionsController.CodeGenerated.cs)).
5. Version-specific bugs or release notes.
6. DataView endpoint behavior if using DataView routes, especially around the Rock 17.5 permission fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
7. Whether endpoint behavior intentionally bypasses entity security but relies on action-level security.
8. Whether a custom controller or block action is safer than direct model endpoint use.

### Lava WebRequest Or External Call Behaves Unexpectedly

A community Q&A record describes a case where Lava `webrequest` calls appeared to fail silently even though direct API access worked ([webrequest not running??](https://community.rockrms.com/ask/developing/2708)). Treat community Q&A as example-level evidence only, but use it as a troubleshooting reminder:

- Test the endpoint outside Lava.
- Test from the Rock server.
- Confirm headers and token format.
- Check Lava command availability/security.
- Check exception logs.
- Check network/TLS/firewall behavior.
- Avoid embedding long-lived tokens directly in Lava prompts.
- Prefer native tools or secured integrations for important external API calls.

## 19. Agent Task Recipes

### Recipe: “Find The Right Person”

Use when a user gives a name, email, phone, or partial identity.

1. Search with a list tool.
2. Return limited candidates with disambiguators.
3. Ask the user to choose if more than one plausible match exists.
4. Set context anchor after selection.
5. Continue with get/summary tools.

Never assume the first name match is correct when the requested action is sensitive.

### Recipe: “Summarize This Person”

1. Confirm person anchor or selected IdKey.
2. Get authorized person summary.
3. Include only fields relevant to the request.
4. Separate verified facts from missing data.
5. Offer next safe actions.

### Recipe: “Draft A Communication”

1. Identify audience through Data View, group, registration, or list tool.
2. Count recipients.
3. Inspect communication channel constraints.
4. Draft message.
5. Present preview.
6. Require explicit approval.
7. Send through a guarded tool.
8. Verify communication record.

### Recipe: “Create A Connection Request”

1. Lookup person.
2. Lookup connection type/opportunity.
3. Confirm status/priority/comment.
4. Create through add tool.
5. Verify created request.
6. Report next owner/follow-up if available.

### Recipe: “Explain A Workflow Queue”

1. Identify workflow type.
2. Use list/insight tool for active workflows by activity/status.
3. Aggregate age and assignment.
4. Return bottlenecks.
5. Offer selected workflow summaries.
6. Do not terminate or advance workflows without approval.

### Recipe: “Audit Agent Security”

1. Inventory agents.
2. Inventory skills per agent.
3. Inventory tools per skill.
4. Mark write-capable tools.
5. Mark sensitive-read tools.
6. Verify security roles.
7. Test representative users.
8. Document findings and remediation.

### Recipe: “Build A Safe Public Agent”

1. Define anonymous/authenticated boundary.
2. Use only public-safe tools.
3. Avoid broad person search.
4. Use current-person-only data for authenticated users.
5. Avoid internal reports.
6. Avoid raw IDs.
7. Avoid write tools unless backed by a workflow with validation.
8. Test as anonymous, authenticated user, and staff.
9. Review transcripts/session history.

### Recipe: “Review An Agent Answer”

1. Identify which tool results support the answer.
2. Re-run the live lookup/get/report if needed.
3. Check date/time and version assumptions.
4. Check whether ambiguous entities were resolved.
5. Check security and sensitive-field handling.
6. If the answer included an action, verify the record changed.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `37`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | implementation_pattern | Community-hub follow-up emails and discussion prompts can serve as a backlog for future Rock workflows, content experiments, and review priorities. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| community-reviewed | operational_guidance | Short-form video should be treated as ministry content with a clear next step, not only as entertainment or social promotion. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| community-reviewed | operational_guidance | Emerging technology pilots should stay clearly labeled as experiments until output quality, data boundaries, and ministry usefulness are verified. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| community-reviewed | operational_guidance | Manual curation still matters for sermon and video libraries because view counts alone do not capture pastoral impact, ministry priority, or whether a message should be highlighted again. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) |
| community-reviewed | operational_guidance | Mobile launch and finance work should be tracked as real operational projects with explicit owners, requirements, and verification steps. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| community-reviewed | operational_guidance | AI coaching should be framed as an assisted resource-routing layer with reviewable prompts, ministry-approved categories, and clear human oversight. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | Digital content libraries work best when they connect messages, topics, and practical next steps instead of leaving users to browse isolated videos. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| community-reviewed | operational_guidance | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| community-reviewed | operational_guidance | Online next-step pathways can combine dashboards, content, and LMS when the church defines the discipleship path being supported. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | Peer learning works best when Rock teams bring action-oriented examples, not only abstract tool discussions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| community-reviewed | operational_guidance | Before adopting AI or search plugins, teams should verify data sources, answer boundaries, security behavior, and whether generated results can be reviewed or tuned. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/a0BJvYDBpz) |
| community-reviewed | operational_guidance | AI should be introduced around concrete ministry workflows and reviewable outputs, not as a broad replacement for staff judgment. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/XaBRra9Brd) |
| More |  | 25 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `9`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) | approved_for_public_distillation | 3 | media-insight:1b335b58b0acc8b1 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) | approved_for_public_distillation | 3 | media-insight:56972ff0f97e563a |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/a0BJvYDBpz) | approved_for_public_distillation | 3 | media-insight:5c9737a6d00c5149 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/XaBRra9Brd) | approved_for_public_distillation | 3 | media-insight:5dd64e1dc98b7742 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) | approved_for_public_distillation | 3 | media-insight:71525fead483ddca |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) | approved_for_public_distillation | 3 | media-insight:927b060aba73b666 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) | approved_for_public_distillation | 3 | media-insight:b4cdf69722ad5d13 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) | approved_for_public_distillation | 3 | media-insight:e81a9f6b5e5e2f8a |
| More |  | 1 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

Primary source dependencies:

- Rock AI concept and terminology: [AI Agents](https://community.rockrms.com/developer/ai-agents)
- Agent configuration and public/internal distinction: [Agents](https://community.rockrms.com/developer/ai-agents/agents)
- Prompt composition and instruction sources: [Agent Instructions](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions)
- Context stability and anchors: [Context Anchors](https://community.rockrms.com/developer/ai-agents/agents/context-anchors)
- Tool security and raw ID warning: [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)
- Tool taxonomy: [Types of Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/types-of-tools)
- Skill grouping and security boundary: [Skills](https://community.rockrms.com/developer/ai-agents/skills)
- Skill creation fields: [Creating Skills](https://community.rockrms.com/developer/ai-agents/skills/creating-skills)
- Lava implementation: [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)
- Lava lookup pattern: [Lava Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools)
- Lava insight pattern: [Insight Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/insight-tools)
- Native implementation: [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools)
- Native lookup and cache/authorization pattern: [Native Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)
- Native helper patterns: [Rock Tool Helper](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper)
- Native EF projection caveat: [Gotchas](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/gotchas)
- Tool debugging: [Debugging Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools)
- Mobile voice surface: [Voice Agent](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/voice-agent)
- General Rock security and Inspect Security: [Rock Admin Hero Guide](https://community.rockrms.com/documentation/BookContent/9)
- Release caveats: [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Model discovery: [Model Map](https://community.rockrms.com/ModelMap)
- Source repository: [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)
- RockU automation training context: [Automations Transcript Insight](https://community.rockrms.com/rocku/core-concepts/automations), especially the 00:25 approved public-safe insight for AI, automation, and responsible tool use.
- RockU data automation training context: [Data Automation Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/data-automation), especially the 00:15 approved public-safe insight for AI, automation, and responsible tool use.
- RockU connection-process training context: [Connection Request Status Automation Transcript Insight](https://community.rockrms.com/rocku/engagement/connection-request-status-automation), especially the 00:41 approved public-safe insight for AI, automation, and responsible tool use.

Topic dependencies:

- **Security** supplies effective access, inherited permissions, elevated security, and verification.
- **API Integrations** supply external and v2 model access surfaces.
- **Workflows** supply approvals, state, exceptions, and human review.
- **Platform Configuration** supplies organization prompts, providers, and global settings.
- **Data Views** supply reusable populations and report filters.
- **Reports** supply operational visibility.
- **Operations** supplies monitoring, cache, logs, versioning, and incident response.
- **Lava** supplies low-code tool implementation and formatting.

Review notes for maintainers:

- Verify the exact installed Rock version before publishing this guide as authoritative.
- Validate all source-code inferences against the target release branch, not only `develop`.
- Confirm the live UI labels for AI Agents, AI Skills, Automations, and Voice Agent settings.
- Confirm generated v2 endpoint permissions in a live test environment before documenting API access as supported.
- Add organization-specific standards for transcript retention, sensitive data handling, approval workflows, and external AI provider usage.
