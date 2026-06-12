# Topic Split Rules

Use these rules when deciding whether a source, guide section, task card, or approved media distillation should live in an existing concept or justify a new first-class concept.

## General Rule

Create a first-class concept when all three are true:

1. The topic has repeated source evidence across at least three source families or a clear official source family.
2. Agents need a distinct operational starting point for real support or implementation questions.
3. Keeping the material inside existing guides causes duplicated checklists, unclear routing, or mixed authority levels.

Keep the topic as a subguide or dependency note when it is mostly a technique, implementation detail, or narrow source family.

## Connections Versus Workflows

Use **Connections** when the question is about:

- Connection types.
- Connection opportunities.
- Connection requests.
- Connection statuses or placements.
- Connections Board or Connections List behavior.
- Assignment, follow-up, or ministry-owner review of people in a connection process.
- Reporting on connection pipeline state.

Use **Workflows** when the question is about:

- Workflow types, activities, actions, triggers, or forms.
- Automation behind a connection process.
- Workflow Entry blocks.
- Workflow failures, activation, persistence, or action configuration.

If a workflow exists only to implement a connection process, route the operational guide to Connections and cite Workflows for the automation mechanics.

## System Administration Versus Security, Data Views, And Workflows

Use **System Administration And Operations** when the question is about:

- Service jobs and job history.
- Exception logs.
- Cache behavior.
- Cleanup/data-integrity jobs.
- Indexing/search health.
- Global/system settings.
- Operational diagnostics and health checks.
- "Rock is slow", "Rock is broken", or "something changed after upgrade" starting points.

Use **Security And Permissions** when the core question is access control, authorization, roles, inherited security, API keys, or public exposure.

Use **Data Views And Reports** when the core question is query logic, data view filters, report output, BI grain, or analytics.

Use **Workflows** when the core question is automation design or a specific workflow execution path.

## Platform Configuration Versus Existing Concepts

Use **Platform Configuration** when the question is about configuration primitives that shape many Rock areas:

- Attributes and attribute values.
- Defined types and defined values.
- Categories.
- Entity types.
- Campuses.
- Global attributes.
- System settings.
- Inheritance or configuration patterns that cut across pages, groups, workflows, finance, and people.

Keep content in the domain guide when the configuration primitive is only meaningful inside that domain. For example:

- Financial account attributes belong in Giving And Finance.
- Check-in label settings belong in Check-In.
- Content channel attributes belong in CMS And Websites.
- Workflow attributes belong in Workflows.

Platform Configuration should explain the primitive and cross-domain risks; domain guides should explain local usage.

## Serving Versus Groups, Scheduling, Check-In, And Communications

Use **Serving And Volunteer Operations** when the question is about the end-to-end volunteer lifecycle:

- Serving teams.
- Volunteer onboarding.
- Requirements.
- Team scheduling and confirmations.
- Service attendance.
- Volunteer communication.
- Follow-up and health of serving pipelines.

Use **Groups** for group type/member/role mechanics.

Use **Scheduling And Locations** for rooms, resources, schedules, calendars, and reservations.

Use **Check-In** for attendance capture, labels, kiosks, room availability, and check-in eligibility.

Use **Communications** for email/SMS delivery, templates, segments, and deliverability.

## AI Agents Versus API, Security, And Workflows

Use **AI Agents And Automation** when the question is about:

- Rock AI agents.
- Custom agent tools.
- Tool permissions and data boundaries.
- Prompt/tool design.
- Staff review requirements.
- Agent access to live Rock data.
- Agentic workflows that can inspect or act in Rock.

Use **API And Integrations** for REST, API v1/v2, OData, webhooks, external systems, and endpoint behavior.

Use **Security And Permissions** for authorization, roles, API key access, public exposure, and least privilege.

Use **Workflows** for Rock workflow automation that does not involve AI-agent tool selection or prompt/tool boundaries.

AI-agent guidance should always cite security and API sources, but it should own the review workflow for what an agent is allowed to see or do.

## Learning, LMS, And Engagement

Do not add this as a first-class concept until there is clearer official source coverage or repeated operational requests.

For now:

- Put learning/LMS implementation mechanics under the closest domain guide.
- Put metrics and engagement scoring under Data Views And Reports unless the question is specifically about learner experience.
- Put communication around courses or engagement under Communications.

## Migration And Data Import

Keep this as a task cluster unless migration work becomes frequent.

Use **Migration And Data Import** only when the source/question is about:

- Slingshot.
- Legacy-system import.
- CSV import strategy.
- Data migration helper methods.
- Idempotent import design.
- Reconciliation after import.

Otherwise:

- Use API And Integrations for import APIs.
- Use Data Views And Reports for validation/reporting.
- Use People And Families, Giving And Finance, or Groups for domain-specific record cleanup.

## Plugins And Extensions

Keep the current topic-page approach unless plugin work becomes a common support surface.

Use a first-class **Plugins And Extensions** concept only if the KB needs recurring guidance for:

- Rock Shop plugin evaluation.
- Plugin install/upgrade risk.
- Custom plugin development.
- Obsidian/classic block packaging.
- Third-party plugin security and maintenance review.

Until then, route plugin development to API And Integrations, CMS And Websites, Mobile, Lava, or Security And Permissions depending on the primary surface.
