# Griffin Adoption

Date: 2026-11-27

Use Griffin as the default for official Rock product knowledge. Maintain this
project as a companion for community implementation and structured operational
references. Let the agent host choose between the two MCP servers.

## Evidence

The organization endpoint supplied for review initialized as `griffin` and
listed 22 tools. It offers knowledge search, topic browsing, and versioned code
search with line retrieval. The server advertises roughly 5,000 knowledge
documents and 56,000 code files. The live tool list includes schema topics
for Rock 17 through 21, Lava, REST, workflow, and coding references.

We submitted 12 matched public questions to both hosted services and inspected
their first three hits. We used Griffin's advertised source and domain filters
where relevant. We then tested exact recipe, issue, Idea, Lava context, and
Model Map lookup alongside Griffin's topic and code paths. This sample
compares the intended retrieval paths. It does not estimate answer accuracy or
complete catalog coverage.

| Probe | Observed result | Decision |
| --- | --- | --- |
| Check-In, workflow entry forms, MCP setup | Filtered Griffin searches exposed the official setup text. A broad unfiltered Check-In query surfaced podcast chunks. The community KB supplied useful checklists and procedure fragments. | Use official documentation first. Narrow weak searches by source and domain. |
| Release status and retirement | Griffin found retirement references. Its `19.9` release search ranked `1.9.4` first and described `19.9` as unreleased. Rock's live timeline listed the November 25 release. | Verify current status on the live timeline and match the complete version. |
| Group model | Griffin's v19 schema topic reached the exact Group article with columns and computed properties. The community KB could filter directly to `Members` and exposes snapshot differences. | Use Griffin for versioned schema. Keep the compact Model Map views where they save work. |
| Check-In label Lava | Griffin returned Label Designer documentation, Label Types, and related v19 source files. The community KB returned seven `PersonAttendance` paths for the exact Person Dynamic Text surface at `19.2.0`. It reported `version_not_observed` for `19.9`. | Keep the exact context directory and its build boundaries. Use upstream evidence for newer or uncovered builds. |
| Issue #6916 and Idea #2280 | The community KB returned exact typed records. Griffin returned related documentation and releases without those records in the first three hits. | Keep issue applicability, verification guidance, and Idea lifecycle metadata. |
| Registration-to-Connection Request recipe | Griffin found documentation for the standard Connection workflow action. The community KB returned the reviewed organization recipe with an immutable source pin and adaptation points. | Keep recipes and reviewed contributions. Use Griffin to confirm current product behavior. |
| Rockcast and plugin discovery | Griffin found episode 225 transcript chunks. Its Rock Shop results were in the right source but did not confirm the named Zapier integration. | Use Griffin's curated sources with result-level verification. Prioritize original community learnings and timestamped evidence that add something to official coverage. |

## Maintenance Direction

- Defer broad re-distillation of official manuals, developer docs, release
  notes, and recent podcasts. Use deterministic metadata feeds where they
  power a distinct feature, such as release-to-issue links or freshness.
- Prioritize reviewed recipes and contributions, exact Lava contexts, issue
  applicability, and Ideas with explicit evidence. Retain Model Map property
  lookup and comparisons while checking where Griffin's schema covers it.
- Keep the published MCP, CLI, and OKF contracts available to existing
  consumers. Preserve citations, review metadata, and stable result IDs.
- Keep the two services connected at the agent host. The community service
  does not proxy Griffin, store organization URLs, or index Griffin responses.
  This keeps the upstream access boundary independent of community hosting.
- Address publication lag for the differentiating catalogs before expanding
  content. On November 27, the live freshness report showed 6,098 checked
  issues versus 5,985 served, and 1,119 checked Ideas versus 1,106 served.
  Review the issue draft and rebuild Ideas in isolation. Confirm counts and
  hashes after deployment. Preserve unrelated release data.
- Before pruning an overlapping source family, test fresh client tasks and
  offline consumers. Require stable exact IDs, recoverable citations, and
  compatible CLI, MCP, and OKF behavior. Measure actual tool calls and maintainer
  effort before adopting an automated router or retiring a retrieval path.

Evidence sources: [Rock Release Timeline](https://community.rockrms.com/release-timeline),
[Rock MCP setup](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/ai/set-up-an-mcp-agent),
[community KB freshness](https://rock-agent-kb.oneandall.church/operations/freshness),
and [issue refresh draft](https://github.com/ONE-ALL-Church/rock-agent-kb/pull/186).
