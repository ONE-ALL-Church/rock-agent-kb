# Contributor And Reviewer Workflow

This KB is intended to be community-contributed, but public output must remain source-backed, license-safe, and useful to agents. The durable unit of review is not a raw document or transcript; it is a reviewer-approved source summary, media rewrite, contribution bundle, or claim.

For the enforceable contribution boundary, lifecycle vocabulary, and end-to-end private-to-public bundle path, use [Contribution Module Runbook](contribution-module.md).

## Roles

- Contributor: suggests a source, submits a contribution bundle, or adds context that should be reviewed.
- Reviewer: checks source authority, license posture, redaction safety, concept fit, and claim usefulness.
- Maintainer: runs rebuilds, validation, public export, and merge/publish steps.
- Agent: consumes the answer pack, concept guides, source summaries, approved claims, and model-map references after rebuild.

## Source Intake

1. Add or update the source in `sources/registry.yaml` when it is a reusable public source.
2. Keep private or organization-specific material in the private review path until it is rewritten and approved.
3. Prefer canonical source URLs over direct media file URLs, HLS manifests, tokenized player URLs, screenshots with private state, or raw transcript paths.
4. Run source validation before fetch or promotion:

```bash
uv run kb sources validate
uv run kb audit licenses
```

## Media Review Path

1. Refresh the media queue:

```bash
uv run kb media report
uv run kb media queue
```

2. Transcribe a bounded batch privately:

```bash
uv run --extra media kb media batch --source rock_podcast_rss --limit 10 --tool mlx_whisper --model auto --dry-run
uv run --extra media kb media batch --source rock_podcast_rss --limit 10 --tool mlx_whisper --model auto
```

3. Generate review candidates:

```bash
uv run kb media normalize --source rock_podcast_rss
uv run kb media candidates --source rock_podcast_rss
uv run kb media review-status
```

4. Review candidates manually. Placeholder text such as `Review this timestamp...` is not publishable.
5. Write reviewer-authored rewrites under `data/review/media-rewrites/`.
6. Promote only useful, public-safe distilled claims:

```bash
uv run kb media promote \
  --source rock_podcast_rss \
  --candidate-id-file data/review/media-rewrites/<rewrite-file>.jsonl \
  --rewrite-file data/review/media-rewrites/<rewrite-file>.jsonl \
  --reviewer <reviewer-name>
```

Leave weak or mostly biographical candidates pending. Do not promote them just to clear the queue.

## Private Or Organization Contribution Path

For private docs, local repos, or organization-specific material:

```bash
uv run kb private scan --repo <path> --source-id <source-id> --org-id <org-id>
uv run kb private review-report --scan-path data/review/private-scan-docs.jsonl --source-id <source-id> --org-id <org-id>
uv run kb private distill --scan-path data/review/private-scan-docs.jsonl --source-id <source-id> --concept <concept-id> --org-id <org-id>
uv run kb contributions promote \
  --draft-path data/review/private-distill/<source-id>-<concept-id>.jsonl \
  --org-id <org-id> \
  --rewrite-file data/review/rewrites/<org-id>-<concept-id>.jsonl \
  --reviewed \
  --redaction-attestation \
  --license-attestation \
  --output contributions/<org-id>/bundle.jsonl
```

Private material must be rewritten into public-safe language before it affects public guides. Keep organization-specific IDs, person data, secret values, private URLs, and non-generalized operational details out of public bundles unless explicitly intended and safe.

## Public Community Repo Intake

For the public community repo, outside agents and other organizations should contribute under `community-contributions/<org-id>/bundle.jsonl` or add lightweight notes under `source-suggestions/<org-id>/`. The generated public surface paths (`agent/`, `knowledge/`, `claims/`, `sources/`, `concepts/`, `contributions/`, and `public-export-manifest.json`) are not contributor edit targets.

Maintainers validate accepted reviewed bundles in place:

```bash
python scripts/validate_bundle.py
uv run kb contributions check --path community-contributions
```

After accepting a public contribution PR, import or promote the reviewed rows into the canonical contribution layer, then rebuild from the pipeline rather than editing generated artifacts by hand:

```bash
uv run kb contributions validate
uv run kb status
uv run kb build
python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit public-export
```

Rows under `community-contributions/` are public intake. Rows under `contributions/` are the reviewed build input that can feed generated guides and agent artifacts.

## Claim Tier Review

Use [Claim Tier Policy](../decisions/claim-tier-policy.md) as the authority for claim eligibility:

- `routing_context_only`: can route agents to sources but should not drive answer prose.
- `source_backed`: guide-safe with caveats, but not operational proof.
- `answer_pack_approved`: may feed generated answer prose.
- `live_verified`: has concrete read-only evidence from a connected Rock instance, model map, source code, or other verified surface.

When a claim requires live evidence:

```bash
uv run kb claims live-plan
```

Retain detailed evidence in the private corpus and add public-safe promotion overlays under `data/review/live-claim-verifications.jsonl`. Do not promote a claim to `live_verified` from source text alone.

## Media Claim Distillation

Use the versioned [Media Claim Distillation Prompt](../prompts/media-claim-distillation-v1.md) for agent-authored transcript rewrites. Record the exact model, prompt ID and version, review method, and full-source input hash in `generation_provenance`. The hash must match the candidate `transcript_hash`; do not label a legacy rewrite with a newer prompt version that did not produce it.

```bash
uv run kb media promote \
  --source <source-id> \
  --candidate-id <candidate-id> \
  --rewrite-file data/review/media-rewrites/<source-id>.transcript-reviewed-rewrites.jsonl \
  --reviewer <reviewer-id> \
  --review-model <exact-model-id> \
  --prompt-id rock-kb-media-claim-distillation \
  --prompt-version 1.0.0 \
  --review-method agent_reviewed_whole_source

uv run kb claims provenance
uv run kb claims evaluation-sample --model <model-id> --sample-size 48
```

The evaluation sample is ignored/private because it may contain bounded transcript or normalized-source context. Score source fidelity, specificity, agent actionability, concept routing, temporal precision, and duplication risk before deciding whether to replace legacy claims. Do not regenerate the entire claim graph solely because a newer model is available.

## Official Document Claim Distillation

Use the versioned [Source Claim Distillation Prompt](../prompts/source-claim-distillation-v1.md) when converting API-backed Rockumentation articles into canonical claims. Generate a private candidate queue first; the command hydrates full article text from the public API and hashes the exact context reviewed by the model.

```bash
uv run kb claims document-candidates \
  --concept <concept-id> \
  --limit-per-concept 8

uv run kb claims document-promote \
  --candidate-path data/review/source-claim-candidates/official-docs.jsonl \
  --rewrite-path data/review/source-claim-rewrites/official-docs-sol-v1.jsonl \
  --output data/review/source-claim-reviews/official-docs-sol-v1.jsonl \
  --reviewer <reviewer-id> \
  --model <exact-model-id>

uv run kb build --stage claims --force
```

Start with the bounded eight-article pilot for each concept. After its claims and answer routing pass review, use a higher `--limit-per-concept` to cover the remaining eligible articles in resumable batches. Keep candidate full text and reviewer rewrite files private. A completed rewrite may use an empty `claims` array to record that a fully reviewed article added no durable, non-duplicate knowledge. The claims stage reports `private-stale` after a promotion that produces public review rows and requires the explicit `--force` rebuild shown above before those rows enter public artifacts. Public claims retain the canonical article URL, normalized source-record ID, article version, concept routing, model/prompt provenance, and source-input hash. Prefer leaf articles with operational detail; skip table-of-contents pages and duplicate knowledge.

## Source Conflict Review

`agent/source-conflicts.jsonl` is a conservative potential-contradiction report.
Rows require shared topic terms and opposing operational language, but still need
human review before changing or rejecting a claim. Review these rows when they
change materially or before a readiness pass:

- Prefer official docs, source code, release notes, RockU, stable public model-map evidence, and live verification for canonical behavior.
- Keep community-reviewed claims as implementation examples or discovery context unless they have been promoted through review and supported by stronger evidence.
- Reject or rewrite distilled claims that are broad advice, episode context, beta-version details, or community-only implementation assumptions.
- Preserve the generated conflict rows unless they become too noisy to review; hiding them can mask future source drift.

Record candid batch decisions in the private corpus, and put claim-level approvals or rejections in `data/review/distilled-claim-reviews*.jsonl`.

## Rebuild After Promotion

After media rewrites, contribution bundles, claim overlays, or source changes:

```bash
uv run kb status
uv run kb build --dry-run
ROCK_KB_GENERATED_AT=<iso timestamp> uv run kb build
uv run kb status
uv run kb audit all
```

Use targeted `uv run kb build --stage <stage>` only when you intentionally want one stale stage and its stale upstream dependencies. The pipeline stage graph owns rebuild ordering, including claim validation, concept refresh, answer pack, agent pack, and export.

After each meaningful source scrape, transcript batch, promotion, or guide synthesis, run `uv run kb status`; if guide intelligence is stale, run `uv run kb build --stage guide-intel`, then compare the regenerated open-question files for the affected concepts.

Treat open questions as a quality gate. Clear high-value `Needs Citation` rows before public export or PR review, batch `Needs Live Verification` rows through read-only evidence probes, and leave `Community-Supported Only` rows pending until stronger evidence or a reviewer-approved rewrite exists. If a previously resolved row returns after a rescrape, fix the durable source link, approved claim, source map, or guide-intel logic rather than repeating one-off cleanup.

Run tests for code or generator changes:

```bash
uv run --extra dev pytest
```

## Reviewer Checklist

- Source is allowed by `sources/registry.yaml` and license posture.
- Public text is paraphrased or reviewer-authored, not copied from raw transcripts or private docs.
- Canonical source URLs are present; direct media file URLs are not public.
- Timestamp fields are included when they help agents route evidence.
- New agent-authored rewrites include truthful `generation_provenance`; legacy rows remain explicitly unprovenanced.
- Demonstrations, partner/custom examples, current behavior, and exploratory roadmap work are labeled and worded differently.
- Concept IDs are specific enough to improve retrieval.
- Claims are durable and reusable for Rock RMS users beyond one organization.
- Operational answers use only `answer_pack_approved` or `live_verified` claims.
- `uv run kb audit readiness` passes before merge.
