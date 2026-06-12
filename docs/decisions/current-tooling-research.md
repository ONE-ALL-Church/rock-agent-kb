# Current Tooling Research

Last checked: 2026-06-02.

## Decisions

- Keep Crawl4AI as the primary local advanced crawler. It remains active, local-first, Python-friendly, and suitable for JavaScript-rendered or Markdown-oriented extraction.
- Keep Cloudflare Browser Run Markdown extraction as an optional hosted fallback for hard pages. It is useful for one-off URL/HTML-to-Markdown extraction and bounded crawler experiments, but free quota is limited and it must not become the only rebuild path.
- Keep Firecrawl optional. Its 2026 `/monitor`, Highlights, and Question formats are valuable for low-token change detection and targeted evidence extraction, but hosted cost/API-key use and AGPL self-hosting keep it out of the default path.
- Keep Docling as the preferred document converter. Its v2 CLI and Python API support Markdown/JSON output and broad document conversion, which fits private source packs and future PDF/Office ingestion.
- Keep `mlx-whisper` with `mlx-community/whisper-large-v3-turbo` as the default local transcription path on this Apple Silicon Mac.
- Track Parakeet CLI/NVIDIA NeMo as the newest high-throughput local transcription candidate. The repo supports `kb media transcribe --tool parakeet`, but this is experimental until a repeatable local install and corpus benchmark are captured.
- Treat Canary-Qwen, Cohere Transcribe, fal.ai Wizper, and OpenAI transcription as optional experiments or hosted fallbacks, not the default private corpus path.
- Adopt the Framedex-style media sidecar/index pattern for Rock media, but not Framedex itself as a hard dependency. The useful idea is durable local sidecars plus textless indexes; this repo should keep its own source policy, citations, and public/private audits.

## Why This Matters For Rock KB

The KB should not just gather pages. It should maintain source-aware, concept-aware distilled guides. That means the highest-leverage tooling is:

- reliable source discovery,
- source hash/change detection,
- clean Markdown/JSON extraction,
- private raw transcript/document processing,
- public distilled outputs with citations,
- repeatable audits that prevent raw copyrighted/private content from leaking.

The best current pattern is still a hybrid system:

- `sources/registry.yaml` describes authoritative inputs and licensing.
- `data/raw-manifests/` and `data/normalized/` track fetched and normalized records.
- `data/media/` and hydrated packs remain private.
- `data/media/sidecars/` stores private per-media Markdown records; `data/media/index/` stores routing indexes without raw transcript text.
- `knowledge/concepts/**` contains authored, rebuilt, citation-backed concept guides.
- `agent/**` contains compact routing/search artifacts for agents.

## Research Notes

- The Hugging Face Open ASR Leaderboard currently shows NVIDIA Canary-Qwen and Parakeet families as strong open ASR candidates. Parakeet TDT 0.6B v3 is especially interesting for high throughput and a permissive CC BY 4.0 model license.
- NVIDIA's own model card says Parakeet TDT 0.6B v3 supports punctuation/capitalization, timestamps, and long audio, but official NeMo usage is heavier than this repo's existing `uv`/MLX path.
- `parakeet-cli` exposes a simple `parakeet transcribe <FILE> --format json` surface, which is why the repo can support it without adopting NeMo as a hard dependency.
- Firecrawl's May 2026 changes make it more attractive for scheduled source monitoring and targeted excerpts, not bulk source-of-truth storage.
- Cloudflare Browser Run exposes a REST `/markdown` Quick Action and `/crawl` endpoint. The repo wraps `/markdown` behind `kb extract markdown --tool cloudflare`; use `kb extract doctor` to check credentials.
- Docling v2 remains the best local-first document conversion candidate because it can emit Markdown and JSON through both CLI and Python APIs.
- Simbastack's Framedex demonstrates the right media archive shape for this project: metadata extraction, transcription, structured AI notes, Markdown sidecars, and JSON rollups. For Rock KB, skip face embeddings by default and treat video frame analysis as a future private-only enhancement for RockU/community hub videos.

## Sources

- [Hugging Face Open ASR Leaderboard results](https://huggingface.co/datasets/hf-audio/open-asr-leaderboard-results)
- [NVIDIA Parakeet TDT 0.6B v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
- [NVIDIA NeMo](https://github.com/NVIDIA-NeMo/NeMo)
- [parakeet-cli](https://github.com/lucataco/parakeet-cli)
- [Firecrawl changelog](https://www.firecrawl.dev/changelog)
- [Cloudflare Browser Run Markdown endpoint](https://developers.cloudflare.com/browser-rendering/rest-api/markdown-endpoint/)
- [Cloudflare Browser Run pricing](https://developers.cloudflare.com/browser-rendering/pricing/)
- [Crawl4AI releases](https://github.com/unclecode/crawl4ai/releases)
- [Docling](https://www.docling.ai/)
- [Docling v2 docs](https://docling-project.github.io/docling/v2/)
- [Framedex](https://github.com/Simbastack-hq/framedex)
- [SimbaStack local video indexing write-up](https://blog.simbastack.com/indexed-a-year-of-video-locally/)
