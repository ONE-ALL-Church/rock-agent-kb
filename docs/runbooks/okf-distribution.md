# Open Knowledge Format Distribution

Rock KB publishes a complete, read-only [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) distribution with each tagged release. OKF is a portability layer; the repository registries, JSONL records, hosted search service, and MCP server remain canonical.

## Contents

The distribution projects canonical public knowledge into typed Markdown with YAML frontmatter and normal Markdown links:

- concept guides;
- agent answers;
- approved claims;
- public contribution provenance, collapsed to one row per contribution ID;
- reviewed community recipes;
- Lava contexts;
- stable Rock model digests;
- public source summaries;
- agent task cards;
- public evidence-source policies.

Every document retains its canonical ID and structured record. Typed edges connect concepts, evidence sources, models, recipes, contributions, and Lava contexts. Directory `index.md` files provide progressive disclosure, while `relationships.jsonl` provides a compact typed-edge projection.

The distribution excludes private organization overlays, raw transcripts and media, review queues, live-instance evidence, evaluations, telemetry, and redundant generated indexes.

## Download And Inspect

Install `uv` if needed, then use the published client without permanently installing it:

```bash
uvx rock-kb okf download
uvx rock-kb okf inspect rock-agent-kb-okf-v0.6.0.zip
uvx rock-kb okf validate rock-agent-kb-okf-v0.6.0.zip
```

`download` retrieves the latest ZIP by default and verifies it against the release checksum. Use `--format tar.gz`, `--version X.Y.Z`, or `--destination <path>` when needed.

The same commands work after a permanent client install:

```bash
uv tool install rock-kb
rock-kb okf download
```

Release assets include:

- `rock-agent-kb-okf-vX.Y.Z.zip`;
- `rock-agent-kb-okf-vX.Y.Z.tar.gz`;
- `rock-agent-kb-okf-vX.Y.Z.sha256`.

## Build From The Repository

Maintainers can build and validate the distribution locally:

```bash
uv run kb publish okf
uv run kb publish okf-validate data/okf-export
```

To produce release archives:

```bash
uv run kb publish okf \
  --version X.Y.Z \
  --source-commit "$(git rev-parse HEAD)" \
  --archive-dir release-assets
```

The ignored `data/okf-export/` directory is generated output, not a contributor edit target. A manifest, per-file hashes, bundle checksums, source commit, generation time, and distribution version make each release inspectable and reproducible.

## Conformance And Safety

The exporter and client validators enforce the required OKF v0.1 `type` frontmatter, reserved-file behavior, date-only log headings, internal-link integrity, archive path safety, checksums, and public/private boundary markers. Producer validation is intentionally stricter than OKF's permissive consumer requirements.

## Import Policy

Rock KB does not import arbitrary OKF bundles into trusted knowledge. Future import support must be review-gated and route records through the existing contribution process, including identity deduplication, source authority, licensing, redaction, public-safety, and maintainer approval. Importing a bundle must never bypass those controls or merge organization-private knowledge into the public index.
