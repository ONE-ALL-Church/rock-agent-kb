# Private Corpus Cloud Runbook

The public repo must be disposable. Raw transcripts, sidecars, review queues, normalized private rows, and media restore pointers live in a private corpus repo. Large binaries live in private object storage such as R2.

## Bootstrap

```bash
uv run kb corpus init --path /path/to/private-corpus
uv run kb corpus validate --path /path/to/private-corpus
```

The private corpus checkout contains:

- `data/raw-manifests/`
- `data/normalized/`
- `data/review/`
- `data/media/`
- `data/index/`
- `large-media-restore-manifest.json`
- `private-corpus-manifest.json`

## Sync After Private Work

After ingest, transcription, media review, private scans, claim promotion review, or normalization:

```bash
uv run kb corpus autosync --path /path/to/private-corpus --commit
```

`autosync` copies ignored text/JSON artifacts into the private corpus, refreshes the large-media restore manifest, and optionally commits in the private corpus repo. It does not copy large media binaries into git.

## Restore On A New Machine

```bash
git clone https://github.com/ONE-ALL-Church/rock-agent-kb.git
git clone <private-corpus-repo-url> private-corpus
cd rock-agent-kb
uv run kb corpus restore --path ../private-corpus
uv run kb corpus verify-rebuild --path ../private-corpus --public-export-destination /tmp/rock-kb-public-export
```

Use `--overwrite` only when intentionally replacing local ignored artifacts from the private corpus.

## Write-Once Transcript Rule

Transcript rows are keyed by media id in `data/media/<source>.transcripts.jsonl`. `kb media transcribe` reuses an existing `transcribed` transcript row instead of re-running ASR when a restored transcript exists. Re-transcription should require an explicit future force path and should preserve the old transcript row or raw payload for audit.

## Scheduled Private Ingest

Run scheduled ingest in the private corpus repo or another private automation context, not in the public repo:

1. Check out `rock-agent-kb` and the private corpus repo.
2. Restore text artifacts with `kb corpus restore`.
3. Run source refresh/media discovery/transcription commands for the target source.
4. Run `kb media sidecars`, `kb media candidates`, and review queue generation.
5. Run `kb corpus autosync --commit`.
6. Upload large media files listed in `large-media-restore-manifest.json` to private R2.

Workers AI Whisper can be used by a private Worker/cron if desired, but local `mlx_whisper`, OpenAI transcription, and Gemma enrichment remain optional private processors. Public artifacts should receive only reviewer-authored distilled claims and source links.

## Required Secrets For Private Automation

- Private corpus repo write token.
- Private R2 bucket credentials.
- Optional ASR provider key if using hosted transcription.
- Optional `OPENAI_API_KEY` for the existing OpenAI transcription path.

Never put these secrets in the public repo, public Actions, public Worker vars, or org registry files.
