# Lava Agent Usage Examples

Generated from structured metadata derived from official `rock_lava_docs` records. This page is a retrieval aid for agents; use the official Lava documentation for syntax, parameters, and examples.

Related generated resources:

- Reference index: [lava-reference-index.md](lava-reference-index.md)
- Safety matrix: [lava-safety-matrix.md](lava-safety-matrix.md)
- Machine-readable rows: `lava-capabilities.jsonl` and `../../../agent/lava-capabilities.jsonl`

## Before Recommending Lava

- Identify the rendering surface: page, block, shortcode, workflow, webhook, Obsidian/Helix surface, or mobile client.
- Verify the live Rock version, enabled Lava commands, security context, current record inputs, query-string inputs, and output destination.
- Treat Lava that reads data, mutates data, launches workflows, performs external I/O, uses SQL/entity access, or affects HTTP/page output as requiring security review.
- Link to the official source page for syntax; do not copy snippets from this generated layer as implementation-ready Lava.

## Risk Triage Examples

- API or webhook answer: start from `Creating APIs Using Lava`, then verify authentication, route exposure, request inputs, output shape, and whether the endpoint exposes sensitive data.
- SQL or Entity command answer: prefer a Data View, report, block setting, API endpoint, or model-map-backed service when possible; require live review before suggesting direct Lava data access.
- Web Request command answer: verify destination, credentials, timeout behavior, retry behavior, and the exact data sent outside the page render path.
- Workflow Activate command answer: verify WorkflowType, launch path, requester, duplicate-launch behavior, and permissions before recommending the Lava command.
- Obsidian/Helix answer: check the client surface before assuming server-page Lava behavior works the same way.
- Mobile answer: verify official mobile support markers, the mobile shell/client version, and the page or block that renders the Lava output.

## Safe Answer Shape

Use this pattern for high-risk Lava guidance:

1. Name the Lava surface and link the official page.
2. State the generated risk tier from the safety matrix.
3. List the live checks needed before implementation.
4. Recommend a safer data or integration path when SQL, Entity, Web Request, webhook, or workflow launch behavior is not required.

## Selected Capability Rows

| Name | Risk | Security Review | Live Verification | Operational Prompt | Official Page |
| --- | --- | --- | --- | --- | --- |
| Creating APIs Using Lava | `high` | yes | yes | Example review question: What route exposure, authentication model, request inputs, output shape, page/block security, and data exposure are involved before enabling Creating APIs Using Lava? | [official](https://community.rockrms.com/lava/lava-api) |
| Entity | `high` | yes | yes | Example review question: Should this page use Entity, or should the data be provided by a Data View, block setting, API endpoint, or model-map-backed service instead? | [official](https://community.rockrms.com/lava/commands/entity-commands) |
| Lava With Obsidian | `high` | yes | yes | Example review question: Which rendering surface uses Lava With Obsidian, and does that surface support this Lava element? | [official](https://community.rockrms.com/lava/obsidian) |
| SQL | `high` | yes | yes | Example review question: Should this page use SQL, or should the data be provided by a Data View, block setting, API endpoint, or model-map-backed service instead? | [official](https://community.rockrms.com/lava/commands/sql-commands) |
| Web Request | `high` | yes | yes | Example review question: What destination, credentials, timeout, retry behavior, and data exposure are involved before enabling Web Request? | [official](https://community.rockrms.com/lava/commands/web-request-commands) |
| Workflow Activate | `high` | yes | yes | Example review question: Which workflow type, activity, requester, and duplicate-launch behavior will Workflow Activate touch? | [official](https://community.rockrms.com/lava/commands/workflow-activate-commands) |
