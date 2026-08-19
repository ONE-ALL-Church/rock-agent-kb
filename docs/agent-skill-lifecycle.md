# Rock KB Agent Skill Lifecycle

The Rock KB skill is a versioned instruction package. A copied `SKILL.md` does
not update itself, so the installer that created the copy should remain
responsible for checking and applying updates.

## Recommended Installation

Use the Rock KB client for Codex, Claude Code, Cursor, or OpenCode. It installs
the skill and the matching hosted MCP configuration together:

```bash
uvx rock-kb install-agent --dry-run
uvx rock-kb install-agent
```

The installer validates the hosted service and skill SHA-256, adds source
provenance to the installed skill, preserves unrelated configuration, creates
timestamped backups, and records private owner-only lifecycle state.

## Check And Update

Run a check that does not change the installed skill or agent configuration:

```bash
uvx rock-kb skill check
```

Apply stale skill content:

```bash
uvx rock-kb skill update
```

Preview and apply an MCP endpoint or anonymous telemetry-header configuration
change:

```bash
uvx rock-kb install-agent --dry-run
uvx rock-kb install-agent
```

Checks report skill content and managed MCP configuration independently:

| Status | Meaning | Command |
| --- | --- | --- |
| `skill_update_available` | Only the reviewed skill content is stale. | `uvx rock-kb skill update` |
| `agent_config_update_available` | Only the managed MCP entry is stale. | `uvx rock-kb install-agent` |
| `skill_and_agent_config_update_available` | Both components are stale. | `uvx rock-kb skill update` |
| `pinned_skill_update_available` | New skill content exists, but the installed version is intentionally pinned. | None unless the human chooses `skill update --unpin`. |
| `pinned_skill_and_agent_config_update_available` | The pinned skill and managed MCP entry are both stale. | Review `install-agent --dry-run`; unpin only if the human also approves the skill update. |

`skill update` does not apply configuration-only drift. It exits with
`agent_config_update_available` and points to `install-agent`, so repeatedly
refreshing an already-current skill cannot be mistaken for a configuration
repair. When skill content and configuration are both stale, one approved
`skill update` keeps the two managed components aligned.

The installer compares parsed TOML or JSON values, not formatting. For example,
Codex's nested `[mcp_servers.rock-kb.http_headers]` table and the equivalent
inline `http_headers = { ... }` form are both current. Reports expose bounded
`config_update_reasons` values such as `mcp_endpoint`, `telemetry_headers`, or
`managed_entry`; they never expose private header values.

Inspect stable local state for scripting or agent use:

```bash
uvx rock-kb skill status --format json
```

`skill check --if-due` skips the network request when the most recent
successful check is less than 24 hours old. Its status is `not_due`, its
recommended action is `none`, and it cannot produce an update notice from
cached local state. Ordinary hosted CLI use performs the same bounded passive
check no more than once per day when managed state exists. The check records
its timestamp and result in private lifecycle state. A failed passive check
never blocks the requested Rock KB operation.

Restart or reload the agent only when an update reports
`restart_required: true`.

## Update Policies

The default policy is `notify`. Set the policy only after the human chooses how
future updates should be handled:

```bash
uvx rock-kb skill policy notify
uvx rock-kb skill policy auto
uvx rock-kb skill policy pinned
```

- `notify` reports an update and waits for explicit approval.
- `auto` applies trusted skill or managed MCP configuration updates during the
  daily check. It is available only for user-scoped installations.
- `pinned` records the installed version and prevents `skill update` from
  changing it. Use `skill update --unpin` to deliberately return to the current
  reviewed version. Configuration-only drift remains separately visible because
  pinning the skill does not make the MCP endpoint or consented headers current.

The decision is stored in private local state, not sent to the hosted service.
Agents should ask the human once before choosing `auto`, and should not infer
permission from unrelated feedback or contribution consent.

## Project Scope

Project-scoped installations are written into the selected repository:

```bash
uvx rock-kb install-agent --scope project --project-dir /path/to/repo
uvx rock-kb skill update --scope project --project-dir /path/to/repo
```

Automatic updates are rejected at project scope. Review the resulting Git diff
and use the repository's normal pull-request process before sharing the change.

## Hosted Manifest

The current release contract is available at:

```text
https://rock-agent-kb.oneandall.church/skill/manifest.json
```

MCP-capable agents can call `kb_skill_manifest`. The response includes stable
keys for the skill version, exact served source SHA-256, source URL, publication
time, minimum client version, restart behavior, supported agents, default
policy, and update interval.

## Other Skill Managers

The canonical package also lives at `skills/rock-kb-agent/`, which makes it
discoverable by source-aware cross-agent managers:

```bash
npx skills add ONE-ALL-Church/rock-agent-kb --skill rock-kb-agent
gh skill install ONE-ALL-Church/rock-agent-kb rock-kb-agent --scope user
```

Those managers should update the skill through their own provenance and hash
tracking:

```bash
npx skills update rock-kb-agent
gh skill update rock-kb-agent
```

These alternate routes install the skill only. They do not configure the Rock
KB MCP endpoint. The Rock KB installer remains the recommended one-step path
for a complete integration.
