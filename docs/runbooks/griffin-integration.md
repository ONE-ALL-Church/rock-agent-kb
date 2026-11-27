# Use Griffin With The Rock Agent KB

Griffin is Rock's official Community Knowledge Base. Use it first for most
product questions. The Rock Agent KB adds precise lookup tools and reviewed
community experience. A Rock instance MCP connector answers questions about a
specific installation under that instance's permissions.

## Connect Both Services

1. Sign in to Rock Community and open your organization's page.
2. Copy the Community Knowledge Base MCP URL from that page.
3. Add it to your agent host as a private, user-level HTTP MCP connection.
   Use a distinct name, such as `rock-community-knowledge`.
4. Keep your existing `rock-kb` connection. To add it, preview
   `uvx rock-kb install-agent --dry-run`, then run `uvx rock-kb install-agent`.
5. Reload the host. Check that it lists Griffin's `search_knowledge` and the
   community KB's `kb_search` as separate tools.

Keep the organization URL out of repositories, shared settings, logs, and
contribution bundles. Use the host's private configuration to store it.
The agent calls each service directly. This KB does not need the Griffin URL
or credentials. For live operations, follow
[Rock's separate instance MCP setup](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/ai/set-up-an-mcp-agent#connect-the-external-tool).

## Choose A Tool

| Question | Start here | Check before answering |
| --- | --- | --- |
| How do I configure a Rock feature? | Griffin `search_knowledge` with the target major version. Try `filter_source: "Core Documentation"` and a matching domain. | Read the result chunk and cite its original article. Search by the setup stage when the first query is broad. |
| What is a Lava command, workflow action, REST endpoint, or database field? | Griffin's matching topic tool, then `get_article` with a key from the table of contents or a child article. | Follow content offsets. Topic entries require browsing. |
| What does Rock actually do in a given release line? | Griffin `search_code` or `grep_code` with the major version, then `get_code_lines`. | Check the exact patch or commit for patch-sensitive behavior. |
| What shipped, and which release is supported today? | [Rock Release Timeline](https://community.rockrms.com/release-timeline), then the exact release notes and technical bulletins. | Check the full version and release state. A similar version string can rank higher. |
| Which merge fields exist in this Check-In label, workflow, or block? | Community KB `kb_get_lava_context` or `kb_list_lava_contexts`. | Check the surface, render phase, and observed versions. Verify a missing build against code or the instance. |
| Is a model property exposed to Lava? What changed across snapshots? | Community KB `kb_get_model` with `property` or selected `fields`. | Check the sampled build. Use Griffin's schema topic for a particular major and its code tools for behavioral details. |
| How did another church implement this? | Community KB `kb_get_recipe` or `kb_list_recipes`. | Verify the pinned source, compatibility, adaptation steps, and required local tests. |
| Does a reported issue affect my Rock version? Is the requested feature available? | Community KB `kb_get_rock_issue`, `kb_assess_rock_issues`, or `kb_get_rock_idea`. | Check `kb_get_freshness`. Consult upstream when the catalog lags. Confirm applicability or availability with release evidence and local read-only checks. |
| What is configured at my church? | The authorized instance connector or a local read-only check. | Share only general public questions with either knowledge service. |
| Can I index or audit a pinned snapshot offline? | The community KB's read-only OKF exports. | Use the release manifest and source provenance. |

When Griffin is unavailable, search the community KB and follow citations to
Rock's current documentation. Treat search misses as coverage or retrieval
gaps. Keep official evidence and community implementation experience attributed
to their respective sources.

## Test The Setup

1. Ask for Rock v19 Check-In setup guidance across areas, groups, and kiosks.
   Expect Griffin to return Rock documentation. Check that the answer cites it.
2. Ask for `PersonAttendance` on a Person Dynamic Text label at Rock `19.2.0`.
   Expect `kb_get_lava_context` for `check-in-label-person-dynamic-text`. Check
   the observed version, roots, and source commit.
3. Ask about that surface at a build absent from `available_versions`.
   Check that the agent reports the coverage limit and seeks direct evidence.

For the comparison and maintenance direction, see the
[Griffin adoption decision](../decisions/griffin-adoption-2026-11-27.md).
