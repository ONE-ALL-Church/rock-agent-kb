# Rock Model Map Rebuild Runbook

This runbook covers the generated model-map layer used by concept indexes, long-form guide pointers, agent rows, and the public export.

## Policy

- Treat the generic stable demo Obsidian block-action export as the default public model-map authority.
- Treat the generic latest/pre-alpha export as a comparison layer only.
- Prefer stable model and property rows in concept guides, agent retrieval, and model detail pages.
- Call out latest/pre-alpha differences only when a model or property differs from stable.
- Do not publish local instance SQL schema snapshots or organization-specific plugin/custom model rows as the public model-map authority.
- Keep the raw fetch artifacts under `data/review/model-map-scrape/`; generated public artifacts are under `knowledge/model-map/` and `agent/model-map-*.jsonl`.

Current checked-in tracks from the last accepted scrape:

| Track | Source | Checked-in Rock Version | Raw Artifact |
| --- | --- | --- | --- |
| Stable | `https://rocksolidchurchdemo.com/admin/power-tools/model-map` | `19.2.0` | `data/review/model-map-scrape/demo-model-map-full-scrape.json` |
| Latest/pre-alpha | `https://rockrmslatest.com/admin/power-tools/model-map` | `20.0.6` | `data/review/model-map-scrape/latest-model-map-full-scrape.json` |

Do not assume those versions are still live. `uv run kb status` probes the stable and latest Rock version endpoints and reports `model-map versions` as stale when either site has advanced.

If a live demo reports an older version than the last reviewed artifact, do not
silently downgrade the checked-in track. Preserve the live response as ignored
review evidence, restore the last accepted artifact from the private corpus,
and document the source anomaly. Resume normal promotion only after the demo
advances to the accepted version or a maintainer reviews and explicitly accepts
the downgrade. On 2026-07-30 the stable demo reported `19.1.8`, behind the
accepted `19.2.0` artifact, so this policy was applied while latest advanced to
`20.0.6`.

## Prerequisites

The fetcher uses Node/Playwright for authentication, then calls Obsidian block
actions directly:

- `RefreshObsidianBlockInitialization` for category/model routing.
- `GetModelDetails` for each model detail payload.

It records collection method, block GUIDs, initialization/detail endpoints,
table names, obsolete flags, enum/DefinedValue flags, and method signatures so
freshness and routing can be checked from generated artifacts.

```bash
npm install --prefix /tmp/rock-model-map-scrape playwright
npx --prefix /tmp/rock-model-map-scrape playwright install chromium
```

`uv run kb modelmap fetch` automatically adds `/tmp/rock-model-map-scrape/node_modules` to `NODE_PATH` when that directory exists. Both the Node package and its Chromium runtime are required on a fresh machine.

The public demo credentials used for the generic demo sites are `admin` / `admin`.

## Refresh The Raw Artifacts

Refresh both stable and latest/pre-alpha:

```bash
uv run kb modelmap fetch --track both --concurrency 16
```

Refresh a single track only when intentionally debugging or limiting scope:

```bash
uv run kb modelmap fetch --track stable
uv run kb modelmap fetch --track latest
```

The older `stamp` command remains available for legacy raw artifacts, but the
current fetch path already probes and records the live Rock semantic version for
each track.

## Rebuild Generated Artifacts

Generate the review diff:

```bash
uv run kb modelmap diff
```

Rebuild the public model-map layer:

```bash
uv run kb modelmap build
```

The default build compares the local raw artifact versions to the live stable/latest endpoints and exits nonzero if either artifact is stale. Use `--skip-live-version-check` only for an explicit offline/custom-path rebuild, and call that out in the PR.

Expected generated outputs include:

- `knowledge/model-map/index.md`
- `knowledge/model-map/stable-models.jsonl`
- `knowledge/model-map/stable-properties.jsonl`
- `knowledge/model-map/stable-methods.jsonl`
- `knowledge/model-map/latest-models.jsonl`
- `knowledge/model-map/latest-properties.jsonl`
- `knowledge/model-map/latest-methods.jsonl`
- `knowledge/model-map/version-diff.json`
- `knowledge/model-map/version-diff.jsonl`
- `knowledge/model-map/models/*.md`
- `knowledge/model-map/concept-slices/*.md`
- `agent/model-map-summary.json`
- `agent/model-map-entities.jsonl`
- `agent/model-map-properties.jsonl`
- `agent/model-map-methods.jsonl`
- `agent/model-map-version-diff.jsonl`
- `agent/model-map-digests.jsonl`

Property and method rows use stable `model_slug + property_slug/signature`
identities. Release-wide Rock versions remain in the summary and model rows;
transient Obsidian row IDs, row indexes, and repeated member-level version
values are intentionally excluded. A routine refresh should therefore show
added, removed, or semantically changed members instead of rewriting every row
when the demo version or block response ordering changes.

## Rebuild Dependent Layers

After the model-map layer changes, rebuild dependent concept and agent artifacts:

```bash
uv run kb build --stage concepts
uv run kb build --stage agent-pack
uv run kb publish export
```

Use `ROCK_KB_GENERATED_AT=<iso timestamp>` for intentional rebuilds that should not change generated metadata on every run. `build-agent-pack` refreshes the generated model-map pointer block in long-form concept guides.

Raw fetch artifacts under `data/review/model-map-scrape/` are ignored review/private working state. `uv run kb build --stage agent-pack` always reuses the committed generated model-map layer under `knowledge/model-map/` and `agent/model-map-*.jsonl`; it must not regenerate the model-map from ignored raw artifacts. Run `uv run kb modelmap build` only after intentionally refreshing and reviewing the stable/latest raw artifacts.

## Validation

Run these checks before packaging a model-map update:

```bash
uv run --extra dev pytest
uv run kb sources validate
uv run kb claims validate
uv run kb audit licenses
uv run kb audit source-policy
uv run kb audit public-export
uv run kb audit readiness
```

Then spot-check:

```bash
head -40 agent/model-map-summary.json
sed -n '1,120p' knowledge/model-map/index.md
sed -n '1,160p' knowledge/model-map/models/group-member.md
uv run --project clients/python rock-kb --url https://rock-agent-kb.oneandall.church model-map list
uv run --project clients/python rock-kb --url https://rock-agent-kb.oneandall.church model group --fields identity,required,relationships,diffs
rg -n "Generated Model Map Pointer|Data Model Landmarks|Pre-alpha" knowledge/concepts/groups knowledge/concepts/workflows knowledge/concepts/security-permissions
```

## Review Notes

- The one-time stable-identity migration can produce a large diff. Later refreshes should not rewrite unchanged property or method rows; investigate broad churn before publishing it.
- Review generated model pages for obvious collection noise before publishing. Pay attention to rows that look like enum option values or action payload artifacts rather than model properties.
- If latest/pre-alpha differs from stable, the stable row should remain the default reference and the latest difference should be a callout, not a replacement.
- If the stable demo version changes, update the expected version table in this runbook and review the generated diff as a version upgrade.
