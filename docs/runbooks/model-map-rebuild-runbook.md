# Rock Model Map Rebuild Runbook

This runbook covers the generated model-map layer used by concept indexes, long-form guide pointers, agent rows, and the public export.

## Policy

- Treat the generic stable demo scrape as the default public model-map authority.
- Treat the generic latest/pre-alpha scrape as a comparison layer only.
- Prefer stable model and property rows in concept guides, agent retrieval, and model detail pages.
- Call out latest/pre-alpha differences only when a model or property differs from stable.
- Do not publish local instance SQL schema snapshots or organization-specific plugin/custom model rows as the public model-map authority.
- Keep the raw scrape artifacts under `data/review/model-map-scrape/`; generated public artifacts are under `knowledge/model-map/` and `agent/model-map-*.jsonl`.

Current checked-in tracks from the last accepted scrape:

| Track | Source | Checked-in Rock Version | Scrape Artifact |
| --- | --- | --- | --- |
| Stable | `https://rocksolidchurchdemo.com/admin/power-tools/model-map` | `19.1.8` | `data/review/model-map-scrape/demo-model-map-full-scrape.json` |
| Latest/pre-alpha | `https://rockrmslatest.com/admin/power-tools/model-map` | `20.0.4` | `data/review/model-map-scrape/latest-model-map-full-scrape.json` |

Do not assume those versions are still live. `uv run kb status` probes the stable and latest Rock version endpoints and reports `model-map versions` as stale when either site has advanced.

## Prerequisites

The scraper is a Node/Playwright script:

```bash
npm install --prefix /tmp/rock-model-map-scrape playwright
```

Run the scraper with `NODE_PATH` pointed at that temporary install unless Playwright is already available to Node in the repo.

The public demo credentials used for the generic demo sites are `admin` / `admin`.

## Refresh The Scrapes

Refresh stable:

```bash
NODE_PATH=/tmp/rock-model-map-scrape/node_modules \
  node tools/model_map_obsidian_scrape.js \
  --url https://rocksolidchurchdemo.com/admin/power-tools/model-map \
  --output data/review/model-map-scrape/demo-model-map-full-scrape.json \
  --username admin \
  --password admin
```

Refresh latest/pre-alpha:

```bash
NODE_PATH=/tmp/rock-model-map-scrape/node_modules \
  node tools/model_map_obsidian_scrape.js \
  --url https://rockrmslatest.com/admin/power-tools/model-map \
  --output data/review/model-map-scrape/latest-model-map-full-scrape.json \
  --username admin \
  --password admin
```

Stamp the raw scrapes from the matching Utility endpoints after scraping:

```bash
uv run kb modelmap stamp
uv run kb modelmap stamp \
  --scrape-path data/review/model-map-scrape/latest-model-map-full-scrape.json \
  --endpoint-url https://rockrmslatest.com/api/Utility/GetRockSemanticVersionNumber
```

## Rebuild Generated Artifacts

Generate the review diff:

```bash
uv run kb modelmap diff
```

Rebuild the public model-map layer:

```bash
uv run kb modelmap build
```

The default build compares the local scrape versions to the live stable/latest endpoints and exits nonzero if either scrape is stale. Use `--skip-live-version-check` only for an explicit offline/custom-path rebuild, and call that out in the PR.

Expected generated outputs include:

- `knowledge/model-map/index.md`
- `knowledge/model-map/stable-models.jsonl`
- `knowledge/model-map/stable-properties.jsonl`
- `knowledge/model-map/latest-models.jsonl`
- `knowledge/model-map/latest-properties.jsonl`
- `knowledge/model-map/version-diff.json`
- `knowledge/model-map/version-diff.jsonl`
- `knowledge/model-map/models/*.md`
- `knowledge/model-map/concept-slices/*.md`
- `agent/model-map-summary.json`
- `agent/model-map-entities.jsonl`
- `agent/model-map-properties.jsonl`
- `agent/model-map-version-diff.jsonl`

## Rebuild Dependent Layers

After the model-map layer changes, rebuild dependent concept and agent artifacts:

```bash
uv run kb build --stage concepts
uv run kb build --stage agent-pack
uv run kb publish export
```

Use `ROCK_KB_GENERATED_AT=<iso timestamp>` for intentional rebuilds that should not change generated metadata on every run. `build-agent-pack` refreshes the generated model-map pointer block in long-form concept guides.

In CI, raw scrape artifacts under `data/review/model-map-scrape/` may be absent because that directory is review/private working state. In that case `uv run kb build --stage agent-pack` reuses the committed generated model-map layer under `knowledge/model-map/` and `agent/model-map-*.jsonl`. Run `uv run kb modelmap build` only after intentionally refreshing the stable/latest raw scrapes.

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
rg -n "Generated Model Map Pointer|Data Model Landmarks|Pre-alpha" knowledge/concepts/groups knowledge/concepts/workflows knowledge/concepts/security-permissions
```

## Review Notes

- A large generated diff is normal because `knowledge/model-map/`, concept indexes, long-form guide pointer blocks, and agent rows all depend on the same generated model-map layer. If you regenerate the ignored scratch export, review it as a local audit artifact only.
- Review generated model pages for obvious scrape noise before publishing. Pay attention to rows that look like enum option values or action payload artifacts rather than model properties.
- If latest/pre-alpha differs from stable, the stable row should remain the default reference and the latest difference should be a callout, not a replacement.
- If the stable demo version changes, update the expected version table in this runbook and review the generated diff as a version upgrade.
