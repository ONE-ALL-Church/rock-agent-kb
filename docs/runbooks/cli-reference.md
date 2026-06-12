# CLI Reference

The `kb` CLI is the stable interface for imports, review queues, generated artifacts, audits, and local rebuilds. Run `uv run kb --help` for the current grouped surface.

## Quick Commands

```bash
uv run kb --help
uv run kb status
uv run kb build --dry-run
uv run kb audit all
uv run --extra dev pytest
```

## Source And Extraction Commands

```bash
uv run kb sources validate
uv run kb sources list
uv run kb sources fetch --source rock_core_release_notes --dry-run
uv run kb sources probe-endpoints
uv run kb sources discover --source rock_mobile_docs
uv run kb sources discover-community --source rock_recipes --max-pages 120 --id-sweep
uv run kb sources normalize --source rock_developer
uv run kb sources summarize --source rock_podcast_rss --model gpt-4.1-mini
uv run kb sources refresh
uv run kb sources refresh --source rock_api_docs --skip-discovery --skip-probe --skip-indexes
uv run kb sources scan --output-dir data/review/source-scan
uv run kb extract doctor
uv run kb extract markdown --tool local --url https://www.triumph.tech/resources/github-spotlight-5212026
uv run kb extract markdown --tool cloudflare --url https://www.triumph.tech/resources/github-spotlight-5212026 --wait-until networkidle
```

## Media Commands

```bash
uv run kb media discover --source rock_podcast_rss
uv run kb media discover --source rock_rocku --include-empty
uv run kb media discover --source rock_community_hubs --include-empty
uv run kb media doctor
uv run kb media report
uv run kb media queue
uv run kb media sidecars --source rock_podcast_rss
uv run kb media transcribe --source rock_podcast_rss --dry-run
uv run --extra media kb media transcribe --source rock_podcast_rss --tool mlx_whisper --model auto
uv run --extra media kb media batch --source rock_podcast_rss --limit 3 --tool mlx_whisper --model auto --dry-run
uv run --extra media kb media batch --source rock_podcast_rss --limit 3 --tool mlx_whisper --model auto
uv run --extra media kb media transcribe --source rock_podcast_rss --tool parakeet --model auto
uv run kb media transcribe --source rock_podcast_rss --tool openai --model gpt-4o-mini-transcribe
uv run kb media transcribe --source rock_podcast_rss --tool whisper --model base
uv run kb media normalize --source rock_podcast_rss
uv run kb media candidates --all-sources
uv run kb media review-status
uv run kb media promote --source rock_podcast_rss --candidate-id media-public-candidate:<id> --rewrite-file data/review/media-rewrites/rock_podcast_rss.jsonl --review-status approved_for_public_distillation --concept-id workflows
uv run kb media understand-benchmark --tool gemma4-12b
uv run kb media understand-prepare --tool gemma4-12b
uv run kb media understand-run --model gemma4:12b
```

## Build, Claims, Concepts, And Model Map

```bash
uv run kb build --stage claims
uv run kb claims validate
uv run kb claims live-plan
uv run kb build --stage concepts
uv run kb build --stage refresh-claims
uv run kb build --stage guide-intel
uv run kb build --stage answers
uv run kb build --stage agent-pack
uv run kb build --stage index
uv run kb build --stage mobile-selector-audit
uv run kb build --stage export
uv run kb concepts list
uv run kb concepts synthesize --concept check-in --model gpt-5.5
uv run kb concepts synthesize --concept workflows --hydrate-sources --include-contributions --model gpt-5.5
uv run kb concepts hydrate --concept workflows --include-private-drafts --private-draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl
uv run kb modelmap build
uv run kb modelmap stamp
uv run kb modelmap diff
```

## Corpus, Private, And Contribution Commands

```bash
uv run kb corpus init --path /path/to/private-rock-kb-corpus
uv run kb corpus validate --path /path/to/private-rock-kb-corpus
uv run kb corpus report
uv run kb corpus sync --path /path/to/private-rock-kb-corpus --dry-run
uv run kb corpus media-manifest --path /path/to/private-rock-kb-corpus
uv run kb corpus audit --path /path/to/private-rock-kb-corpus
uv run kb corpus verify-rebuild --path /path/to/private-rock-kb-corpus --public-export-destination data/tmp/private-corpus-public-export-check
uv run kb private scan --repo /path/to/private-rock-docs --source-id rockproduction_docs_private_candidates --org-id oneall
uv run kb private review-report --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --org-id oneall
uv run kb private distill --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --concept workflows --org-id oneall
uv run kb private stale --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --concept workflows
uv run kb private impact --scan-path data/review/private-scan-docs.jsonl --source-id rockproduction_docs_private_candidates --org-id oneall
uv run kb contributions new --org-id <org-key> --org-display-name "Example Church"
uv run kb contributions check --path contributions/<org-key>
uv run kb contributions validate
uv run kb contributions validate --path contributions/<org-key>/bundle.jsonl
uv run kb contributions promote --draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl --org-id oneall --rewrite-file data/review/rewrites/oneall-workflows.jsonl --reviewed --redaction-attestation --license-attestation --output contributions/oneall/bundle.jsonl
```

## Audit, Publish, Report, And Tools

```bash
uv run kb audit guide --concept check-in
uv run kb audit licenses
uv run kb audit source-policy
uv run kb audit public-export
uv run kb audit readiness
uv run kb audit all
uv run kb publish export
uv run kb report refresh
uv run kb report dashboard
uv run kb tools repo-pack --repo https://github.com/SparkDevNetwork/Rock
```

`kb contributions import-public` and `kb publish push` are retired split-repo transition commands. The single-public-repo path validates `community-contributions/` and `source-suggestions/` in place and treats `kb publish export` as ignored scratch/audit output.

## Command Groups

| Group | Purpose |
|---|---|
| `kb status` / `kb build` | Pipeline freshness, dry-run planning, and deterministic rebuild execution. |
| `kb sources ...` | Source registry, discovery, fetch, normalize, summarize, refresh, endpoint probing, and source scans. |
| `kb extract ...` | Targeted Markdown extraction and extractor diagnostics. |
| `kb media ...` | Private media discovery, transcription, sidecars, review candidates, promotion, and Gemma enrichment. |
| `kb claims ...` | Claim graph validation and live-verification planning. |
| `kb corpus ...` | Private corpus portability, sync, audit, and rebuild verification. |
| `kb private ...` | Private-source scanning, distillation, review reporting, staleness, and impact checks. |
| `kb contributions ...` | Contribution bundle creation, validation, promotion, and import. |
| `kb concepts ...` | Concept listing, authored synthesis, and hydration. |
| `kb modelmap ...` | Stable/latest Rock model-map build, stamping, and diffs. |
| `kb audit ...` | Guide, license, source-policy, public-export, readiness, and all-in-one audits. |
| `kb publish ...` | Public export and legacy public-repo push commands. |
| `kb report ...` | Refresh reports and maintainer dashboards. |
| `kb tools ...` | Developer utility commands. |

## Old Command Disposition

The Phase 3 CLI re-cut intentionally removed flat compatibility aliases. Use the new grouped forms below.

| Old command | New form |
|---|---|
| `sources list` | `sources list` |
| `sources validate` | `sources validate` |
| `discover` | `sources discover` |
| `discover-community` | `sources discover-community` |
| `fetch` | `sources fetch` |
| `normalize` | `sources normalize` |
| `summarize` | `sources summarize` |
| `refresh` | `sources refresh` |
| `probe-endpoints` | `sources probe-endpoints` |
| `source-scan` | `sources scan` |
| `extract-markdown` | `extract markdown` |
| `extractor-doctor` | `extract doctor` |
| `media-discover` | `media discover` |
| `media-transcribe` | `media transcribe` |
| `media-batch` | `media batch` |
| `media-doctor` | `media doctor` |
| `media-report` | `media report` |
| `media-queue` | `media queue` |
| `media-normalize` | `media normalize` |
| `media-sidecars` | `media sidecars` |
| `media-prune-dry-runs` | `media prune-dry-runs` |
| `media-public-candidates` | `media candidates` |
| `media-review-status` | `media review-status` |
| `media-public-draft-rewrites` | `media draft-rewrites` |
| `media-public-promote` | `media promote` |
| `media-understanding-benchmark` | `media understand-benchmark` |
| `media-understanding-prepare` | `media understand-prepare` |
| `media-understanding-run-ollama` | `media understand-run` |
| `build-claims` | `build --stage claims` |
| `validate-claims` | `claims validate` |
| `live-verification-plan` | `claims live-plan` |
| `private-corpus-init` | `corpus init` |
| `private-corpus-validate` | `corpus validate` |
| `private-corpus-report` | `corpus report` |
| `private-corpus-sync` | `corpus sync` |
| `private-corpus-media-manifest` | `corpus media-manifest` |
| `private-corpus-audit` | `corpus audit` |
| `private-corpus-verify-rebuild` | `corpus verify-rebuild` |
| `private-scan` | `private scan` |
| `private-ingest` | `private ingest` |
| `private-review-report` | `private review-report` |
| `distill-private` | `private distill` |
| `private-stale` | `private stale` |
| `private-impact` | `private impact` |
| `contribution-new` | `contributions new` |
| `contribution-check` | `contributions check` |
| `contribution-validate` | `contributions validate` |
| `contribution-promote` | `contributions promote` |
| `contribution-import-public` | retired split-repo transition command |
| `concepts list` | `concepts list` |
| `concepts stale` | `status` |
| `synthesize-concept` | `concepts synthesize` |
| `hydrate-concept` | `concepts hydrate` |
| `build-concepts` | `build --stage concepts` |
| `build-concept` | `build --stage concepts` |
| `refresh-guide-claims` | `build --stage refresh-claims` |
| `build-guide-intel` | `build --stage guide-intel` |
| `build-model-map` | `modelmap build` |
| `stamp-model-map-scrape-version` | `modelmap stamp` |
| `diff-model-map-scrapes` | `modelmap diff` |
| `build-mobile-selector-audit` | `build --stage mobile-selector-audit` |
| `mobile-selector-audit-status` | `status` |
| `build-index` | `build --stage index` |
| `build-answer-pack` | `build --stage answers` |
| `build-agent-pack` | `build --stage agent-pack` |
| `guide-refresh-plan` | `status` |
| `audit-guide` | `audit guide` |
| `audit-licenses` | `audit licenses` |
| `audit-source-policy` | `audit source-policy` |
| `audit-public-export` | `audit public-export` |
| `audit-readiness` | `audit readiness` |
| `public-export` | `publish export` |
| `publish-public` | retired split-repo transition command |
| `report-refresh` | `report refresh` |
| `refresh-dashboard` | `report dashboard` |
| `rebuild-plan` | `status` plus `build --dry-run` |
| `repo-pack` | `tools repo-pack` |
