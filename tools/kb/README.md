# kb CLI

The project CLI is exposed as the `kb` console script from the Python package.

Use it through `uv` for reproducible local execution:

```bash
uv run kb sources validate
uv run kb fetch --source rock_core_release_notes --dry-run
uv run kb probe-endpoints
uv run kb discover-community --source rock_lava_docs --max-pages 180
uv run kb normalize --source rock_core_release_notes
uv run kb refresh --source rock_api_docs --skip-discovery --skip-probe --skip-indexes
uv run kb build-agent-pack
uv run kb build-concepts
uv run kb concepts stale
uv run kb hydrate-concept --concept groups --limit 80
uv run kb synthesize-concept --concept groups --profile comprehensive --hydrate-sources --model gpt-5.5
uv run kb synthesize-concept --concept workflows --hydrate-sources --include-contributions --model gpt-5.5
uv run kb hydrate-concept --concept workflows --include-private-drafts --private-draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl
uv run kb build-guide-intel --concept groups
uv run kb audit-guide --concept groups
uv run kb audit-public-export
uv run kb public-export
uv run kb media-discover --source rock_podcast_rss
uv run kb media-doctor
uv run kb media-transcribe --source rock_podcast_rss --dry-run
uv run kb private-scan --repo /Users/briand/Documents/GitHub/RockProduction/docs --source-id rockproduction_docs_private_candidates --org-id oneall
uv run kb private-review-report --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --org-id oneall
uv run kb distill-private --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --concept workflows --org-id oneall
uv run kb contribution-promote --draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl --org-id oneall
uv run kb contribution-promote --draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl --org-id oneall --rewrite-file data/review/rewrites/oneall-workflows.jsonl --reviewed --redaction-attestation --license-attestation --output contributions/oneall/bundle.jsonl
uv run kb private-stale --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --concept workflows
uv run kb private-impact --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --org-id oneall
uv run kb contribution-new --org-id <org-key> --org-display-name "Example Church"
uv run kb contribution-check --path contributions/<org-key>
uv run kb contribution-validate
```

Comprehensive synthesis builds its required outline from `concepts/registry.yaml`, including each concept's subguides and dependency topics, so new concepts do not inherit a stale hard-coded guide structure.

Approved public contribution bundles are included in concept synthesis by default through `--include-contributions`. Use `--no-include-contributions` to exclude them. Private draft contribution rows are excluded unless `--include-private-drafts` and one or more `--private-draft-path` values are passed to `hydrate-concept` or to `synthesize-concept --hydrate-sources`; private draft packs stay under `data/review/concept-synthesis/` and are not public export material.

## Private Media Workflow

Media discovery and transcription are private processing steps for RockU lessons, ROCK Cast podcast episodes, and community hub media pages. Raw transcripts are private corpus material, not public export material.

```bash
uv sync --extra media
uv run kb media-discover --source rock_podcast_rss
uv run kb media-discover --source rock_rocku --limit 25 --include-empty
uv run kb media-discover --source rock_community_hubs --include-empty
uv run kb media-doctor
uv run kb media-transcribe --source rock_podcast_rss --dry-run
uv run --extra media kb media-transcribe --source rock_podcast_rss --tool mlx_whisper --model auto
uv run --extra media kb media-transcribe --source rock_podcast_rss --tool parakeet --model auto
uv run kb media-transcribe --source rock_podcast_rss --tool openai --model gpt-4o-mini-transcribe
uv run kb media-transcribe --source rock_podcast_rss --tool whisper --model base
uv run kb media-normalize --source rock_podcast_rss
uv run kb media-public-candidates --all-sources
uv run kb media-review-status
uv run kb guide-refresh-plan
uv run kb build-index
```

Generated media manifests, downloads, and transcript rows live under `data/media/`, which is ignored and treated as private raw working data by public export audits.

`--tool mlx_whisper --model auto` is the recommended local default on this Apple Silicon machine and maps to `mlx-community/whisper-large-v3-turbo`. `--tool parakeet` is available as an experimental high-throughput local path after a compatible `parakeet` CLI is installed. `--tool openai` uses the bundled Codex `transcribe` skill script and requires `OPENAI_API_KEY`; the Codex login by itself does not expose an audio transcription model to the repo CLI. Video/HLS sources use `yt-dlp` when installed, or `uvx --from yt-dlp yt-dlp` when `uvx` is available.

`media-normalize` distills completed private transcript rows into `data/normalized/<source>.media-insights.jsonl`. Those records include summaries, source URLs, media IDs, transcript hashes, and review flags; they do not include the raw transcript field. `media-public-candidates` writes textless review prompts under `data/review/public-summary-candidates/`; run it per source or with `--all-sources` for every transcribed media source. Generated placeholders are blocked from promotion until `media-public-promote --rewrite-file <jsonl>` receives reviewer-written public-safe summaries and insights. Promotion records explicit approvals under `data/review/public-media-promotions/` and replaces the matching local insight row summary/key insights so future concept/public-export rebuilds may use only the rewritten claims. Reviewer rewrites may include `timestamp`, `timestamp_seconds`, and `source_timestamp_url` fields for public citation routing, but should use source page URLs rather than direct media, HLS, or tokenized player URLs.

`media-review-status` reports transcribed, candidate, approved, pending, rejected, and affected-concept coverage across media sources. `guide-refresh-plan` distinguishes generated concept `index.md` rebuilds from long-form `guide.md` refreshes by comparing approved media insight hashes against current dependency metadata. Raw transcript completion alone should not change public guides; approved public distillations should trigger generated-layer rebuilds, and long-form guides should be refreshed only when the plan flags approved media dependency drift.

This directory exists as the stable home for future CLI helper scripts, templates, and source-specific adapters.

## Private And Org Contributions

`private-scan` creates private review manifests from owner or outside-org docs. `private-review-report` summarizes a private scan by classification, candidate concept, risk flag, and distillation eligibility without exposing private paths or raw content. `distill-private` turns eligible `generalizable_pattern` rows into private draft contribution rows under `data/review/private-distill/` and dependency rows under `data/review/private-dependencies/`. `contribution-promote` turns private draft rows into either private staging skeletons or reviewed public bundles. Reviewed promotion requires `--rewrite-file`, `--reviewed`, `--redaction-attestation`, and `--license-attestation`; without those flags it writes a private staging file under `data/review/contribution-promotion/`. Reviewed promotion writes private public-artifact dependency maps under `data/review/private-promotion-dependencies/`. `private-impact` compares those maps to the latest private scan and reports which public concepts and contribution bundle paths need rebuild without exposing private paths or raw content. `concepts stale` also reads this local private impact data when present. `private-stale` compares private dependency hashes to the latest scan and reports stale drafts without exposing private paths or raw content. `contribution-new` creates a non-public `bundle.example.jsonl` starter template, `contribution-check` runs the contributor-facing bundle audit and summary, and `contribution-validate` validates public JSONL bundles under `contributions/` while rejecting unreviewed rows, private metadata, sensitive-looking values, private paths, and missing source traceability.

Reviewer rewrite files are JSONL keyed by the private draft `contribution_id`:

```json
{"contribution_id":"private-distill:abc","public_contribution_id":"oneall:workflow-intake-review","title":"Workflow intake patterns need launch review","distilled_summary":"Newly written public-safe guidance with source support and no copied private text.","source_urls":["https://community.rockrms.com/documentation"],"source_record_ids":[],"confidence":"medium","needs_live_verification":true}
```
