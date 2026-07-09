# Local Transcription Decision

## Recommendation

Use `mlx-whisper` with `mlx-community/whisper-large-v3-turbo` as the default local transcription path on this Mac.

This machine is an Apple M1 Pro with 16 GB RAM, so MLX is the best fit among easy-to-operate local options. It avoids API keys, keeps private media private, and integrates cleanly with the repo's `uv` workflow.

The newest high-throughput open model to track is NVIDIA Parakeet TDT. The repo now supports `--tool parakeet` as an experimental local path, but it is not the default because the current Mac setup already has MLX Whisper working and Parakeet's official stack is heavier. Use Parakeet for speed/accuracy experiments after installing a compatible local CLI.

## Repo Commands

```bash
uv sync --extra media
uv run --extra media kb media doctor
uv run --extra media kb media transcribe --source rock_podcast_rss --tool mlx_whisper --model auto
uv run --extra media kb media batch --source rock_podcast_rss --limit 3 --tool mlx_whisper --model auto --dry-run
uv run --extra media kb media batch --source rock_podcast_rss --limit 3 --tool mlx_whisper --model auto
uv run kb media transcribe --source rock_podcast_rss --tool cloudflare --model auto
uv run --extra media kb media transcribe --source rock_podcast_rss --tool parakeet --model auto
uv run kb media normalize --source rock_podcast_rss
uv run kb media sidecars --source rock_podcast_rss
uv run kb media candidates --source rock_podcast_rss
uv run kb media review-status
uv run kb media understand-benchmark --tool gemma4-12b
uv run kb media understand-prepare --tool gemma4-12b
uv run kb media understand-run --model gemma4:12b
uv run kb build --stage index
```

The official Rock YouTube feed is registered as `rock_youtube`. Target one
known video by stable media ID so a higher-priority unrelated item cannot take
its place:

```bash
uv run kb media discover --source rock_youtube
uv run --extra media kb media batch --source rock_youtube --media-id media:<id> --limit 1 --tool mlx_whisper --model auto --dry-run
uv run --extra media kb media batch --source rock_youtube --media-id media:<id> --limit 1 --tool mlx_whisper --model auto
uv run kb media candidates --source rock_youtube
```

Official videos and Community Blog articles are useful for product direction,
demonstrations, rollout lessons, and discovering claims that written docs may
not yet cover. Reviewer distillations must label demonstrations and exploratory
roadmap items explicitly. Current documentation, release notes, public source
code, and live configuration remain the authority for implementation details
and actual availability.

Use the tiny model only for quick smoke tests:

```bash
mkdir -p data/media/smoke
say -o data/media/smoke/rock-kb-smoke.aiff "Rock RMS knowledge base local transcription smoke test."
uv run --extra media mlx_whisper data/media/smoke/rock-kb-smoke.aiff --model mlx-community/whisper-tiny --output-dir data/media/smoke --output-format txt --verbose False
uv run --extra media kb media transcribe --source rock_podcast_rss --tool mlx_whisper --model tiny --limit 1
uv run --extra media kb media batch --source rock_podcast_rss --tool mlx_whisper --model tiny --limit 1
uv run kb media sidecars --source rock_podcast_rss
```

Install and prepare the experimental Parakeet path separately:

```bash
brew install lucataco/tap/parakeet-cli
parakeet download
uv run --extra media kb media transcribe --source rock_podcast_rss --tool parakeet --model auto --limit 1
```

The default Parakeet download is INT8 model weights. The CLI also supports `parakeet download --fp16` for larger/faster FP16 weights on Apple Silicon.

Local validation on 2026-06-02:

- `brew install lucataco/tap/parakeet-cli` installed `parakeet-cli` 0.1.3.
- `parakeet download` downloaded the INT8 Parakeet TDT 0.6B v3 weights under `~/Library/Application Support/parakeet/models/`.
- A generated smoke WAV transcribed successfully with `parakeet transcribe ... --format json`.
- `uv run --extra media kb media transcribe --source rock_podcast_rss --tool mlx_whisper --model tiny --limit 1` completed one real local podcast transcription.
- The first podcast transcript produced a private transcript row and sidecar with about 49k transcript characters. `kb media normalize` then produced one non-verbatim `media-insight` row with transcript hash, source URL, detected themes, and `needs_review: true`.
- `kb media batch` is the preferred operator command for ongoing corpus fill. It selects the next pending rows, runs transcription, rebuilds private media insights, and refreshes sidecars. Use `--dry-run` first to preview the batch without writing transcript rows.
- Gemma 4 12B is a second-pass audio/video understanding step, not the baseline transcript generator. After the normal transcription/normalization/sidecar/candidate flow, run `kb media understand-benchmark --tool gemma4-12b`, `kb media understand-prepare --tool gemma4-12b`, then `kb media understand-run --model gemma4:12b`. The prepare step writes a private clip/frame manifest under `data/tmp/gemma-benchmark/`, and the Ollama runner sends compressed MP3 payloads generated from prepared clips, adds video frames when available, and uses transcript excerpts only as comparison grounding.

## Model Options

| Option | Best Use | Notes |
| --- | --- | --- |
| `mlx-whisper` + Whisper Large v3 Turbo | Default for this Apple Silicon Mac | Local, simple, good quality, no API key. |
| `parakeet` CLI + NVIDIA Parakeet TDT 0.6B v3 | Experimental high-throughput local path | Newer open model family with strong leaderboard speed; may require WAV conversion and extra install steps. |
| `whisper.cpp` + Metal | Alternative local Mac runtime | Strong fallback if Python/MLX gets awkward. |
| Cloudflare Workers AI Whisper Large v3 Turbo | Hosted scheduled-ingest default | Uses `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`; aligns with private R2 automation. |
| NVIDIA Canary / Canary-Qwen | Accuracy experiments | Strong leaderboard quality, but operationally heavier for this repo workflow. |
| Cohere Transcribe 03-2026 | Accuracy experiment | Apache-2.0 model family to watch; not yet wired into the repo CLI. |
| fal.ai Wizper | Low-ops hosted fallback | Useful for batch bursts, but hosted and pricing should be checked live before bulk use. |
| OpenAI transcription API | API fallback | Already supported via the Codex transcribe skill, but requires `OPENAI_API_KEY`. |

## Sidecars And Indexes

After transcription, run `kb media sidecars` for each media source. It writes:

- `data/media/sidecars/<source>/*.media.md`: private Markdown sidecars that may contain raw transcripts.
- `data/media/index/<source>.media-index.jsonl`: per-source routing rows without transcript text.
- `data/media/index/media-index.jsonl`: combined private routing index for local agents.
- `data/media/index/transcription-priority-queue.jsonl`: private ranked transcription work queue.
- `data/media/index/transcription-priority-report.json`: private queue summary and top-item report.

Agents should use the index to locate relevant media and the sidecar for private synthesis. `kb media normalize` insight rows are private retrieval inputs until they receive an explicit public review status such as `redaction_reviewed`. Public output should use source URLs, source hashes, and reviewed distilled claims; it should not copy transcript text from sidecars.

Before running a larger transcription pass, rebuild the priority queue:

```bash
uv run kb media queue
```

The queue is ranked from private media manifests using source authority, media type, item-level title/source URL signals, release/developer/operations/security/reporting terms, and duration. It intentionally avoids broad source-level tags and direct media URL query strings so a Vimeo `oauth2_token` or a word like `training` does not falsely boost every item. `kb media batch` and `kb media transcribe` use the same priority ordering within the selected source.

Normalized media insights must be distilled, not transcript excerpts. The safe shape is a source-linked signal summary such as detected themes, transcript scale, tool/model, transcript hash, and review status. Raw transcript language belongs only in `data/media/sidecars/` and transcript payload files. Public agent indexes exclude private-derived rows while `needs_review` is true.

Public concept guides use the same review gate. Transcript-derived `media-insight:*` rows must be promoted before they can affect `agent/concept-dependencies.jsonl`, authored synthesis packs, public source summaries, or the public surface.

Transcripts should preserve timestamps whenever the transcription tool provides them. The private transcript row stores `transcript_segments`, `transcript_segment_count`, `timestamped_transcript_available`, and a `raw_transcript_payload_path` that points to the ASR tool's original JSON. The KB row is written separately as `*.row.json` so future runs do not overwrite segment-level ASR output.

Public podcast material should be episode notes, not transcripts. Run:

```bash
uv run kb media candidates --source rock_podcast_rss
uv run kb media candidates --all-sources
uv run kb media review-status
```

This writes `data/review/public-summary-candidates/<source>.media-public-candidates.jsonl`. Each candidate contains source links, transcript hashes, topics, timestamped insight slots when segment data exists, and review notes. It intentionally omits raw transcript text. These rows are review prompts, not public claims; placeholder summaries or `Review this timestamp...` insights cannot be promoted without a reviewer rewrite.

For audio/video enrichment, run the Gemma private review step before deciding which candidates deserve reviewer-authored public rewrites:

```bash
uv run kb media understand-benchmark --tool gemma4-12b
uv run kb media understand-prepare --tool gemma4-12b
uv run kb media understand-run --model gemma4:12b
```

`media-understanding-prepare` writes private clips, frames, and `data/tmp/gemma-benchmark/clip-manifest.json`. `media-understanding-run-ollama` reads that manifest and writes private results under `data/review/media-understanding-benchmarks/`. Use those results to identify stronger durable claims, visual context, transcript disagreements, and low-confidence media that needs a better transcript or human review. Do not promote Gemma output directly into public artifacts; rewrite claims in reviewer-authored public-safe language and cite canonical source page URLs.

Create a JSONL rewrite file keyed by `candidate_id`:

```json
{"candidate_id":"media-public-candidate:<id>","summary":"Public-safe durable claim written by the reviewer, with no transcript excerpt text.","key_insights":[{"topic":"workflows","insight":"Specific public-safe insight that can feed a concept guide.","source_url":"https://example.org/source","source_timestamp_url":"https://example.org/source","timestamp":"01:23","timestamp_seconds":83,"contains_verbatim_transcript":false}],"concept_ids":["workflows"]}
```

Promote reviewed candidates explicitly:

```bash
uv run kb media promote --source rock_podcast_rss --candidate-id media-public-candidate:<id> --rewrite-file data/review/media-rewrites/rock_podcast_rss.jsonl --review-status approved_for_public_distillation --concept-id workflows
uv run kb build --stage claims
uv run kb build --stage concepts
uv run kb build --stage refresh-claims
uv run kb build --stage agent-pack
uv run kb publish export
```

`kb media promote` writes an approval row under `data/review/public-media-promotions/` and updates the matching local normalized `media-insight:*` row with the rewritten `summary`, `key_insights`, `review_status`, `review_origin`, and `needs_review: false`. The promotion row and public artifacts remain textless with respect to raw transcripts. Reviewer rewrites may keep timestamp metadata for source routing, but should cite the canonical source page and should not include direct media file URLs, HLS manifests, or tokenized player URLs.

After promotion, rebuild generated public layers with `uv run kb build --stage claims`, `uv run kb build --stage concepts`, `uv run kb build --stage refresh-claims`, `uv run kb build --stage agent-pack`, and `uv run kb publish export`. Set `ROCK_KB_GENERATED_AT=<iso timestamp>` for this rebuild when you want generated metadata to stay stable across repeated runs. Then run `uv run kb status`. Generated concept `index.md` files should follow approved media promotions automatically, and `kb build --stage refresh-claims` inserts bounded approved-claim and approved-media summaries into long-form `guide.md` files while writing the full per-concept tables to `knowledge/concepts/<concept>/approved-claims.md` and `knowledge/concepts/<concept>/approved-media.md`. If the plan still flags a long-form guide, refresh the authored guide body, run `uv run kb build --stage guide-intel --concept <concept>`, then rebuild the agent pack and public export.

Non-media sources should also have public summaries and key insights, but not necessarily standalone pages. `uv run kb build --stage agent-pack` writes `agent/source-summaries.jsonl` for public-agent-eligible records. These rows are public-safe routing notes for agents; authoritative concept guides should be reserved for source clusters where synthesis adds operational value.

## Why Not fal.ai As The Default?

`fal-ai/wizper` is a good hosted option and worth keeping as a fallback provider, especially if local transcription becomes too slow. It is not the default because the KB's private layer should remain local-first and not rely on a hosted scraping or AI service as the only rebuild path.

Before using fal.ai for a bulk corpus run, verify current model pricing on the fal model page or pricing API.

## Sources Checked

- [Hugging Face Open ASR Leaderboard results](https://huggingface.co/datasets/hf-audio/open-asr-leaderboard-results)
- [MLX Whisper examples](https://github.com/ml-explore/mlx-examples/blob/main/whisper/README.md)
- [NVIDIA Parakeet TDT 0.6B v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
- [NVIDIA NeMo](https://github.com/NVIDIA-NeMo/NeMo)
- [parakeet-cli](https://github.com/lucataco/parakeet-cli)
- [fal.ai Wizper](https://fal.ai/models/fal-ai/wizper)
- [fal.ai speech-to-text docs](https://fal.ai/docs/examples/audio-speech/convert-speech-to-text)
- [fal.ai pricing docs](https://fal.ai/docs/documentation/model-apis/pricing)
- [Open ASR Leaderboard paper](https://arxiv.org/abs/2510.06961)
- [Canary / Parakeet paper](https://arxiv.org/abs/2509.14128)
