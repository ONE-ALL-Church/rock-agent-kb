# Open Knowledge Format Distribution

Rock KB publishes `full` and `core` read-only [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) distributions with each tagged release. OKF is a portability layer; the repository registries, JSONL records, hosted search service, and MCP server remain canonical. Rock-specific extensions are versioned in the [Rock KB OKF profile](../specs/rock-kb-okf-profile-v1.md).

## When To Use OKF

For ordinary online retrieval, use hosted MCP from an MCP-capable agent or the
`rock-kb` CLI from a terminal agent. These are co-primary interfaces to the same
current hosted projection; MCP is preferable only when native typed tools fit
the client better.

Use OKF when the consumer needs one or more of these properties:

- offline or disconnected operation;
- a version-pinned, reproducible public snapshot;
- bulk analysis or a locally managed search/vector index;
- archival and provenance inspection;
- interchange with another OKF-aware knowledge system.

Do not download an OKF bundle merely to answer an ordinary online question. An
OKF consumer is responsible for indexing, bounded retrieval, and checking the
bundle version for staleness; it should not place the complete corpus into one
model context.

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
- public Rock issue routing metadata and nested reviewed enrichments in the full profile;
- public evidence-source policies.

Every document retains its canonical ID and links to a lossless JSON structured record. Typed edges connect concepts, evidence sources, models, recipes, contributions, and Lava contexts. Bounded, sharded directory `index.md` files provide progressive disclosure, while `relationships.jsonl` provides a compact typed-edge projection.

The `full` profile includes every public canonical row. The smaller `core`
profile omits routing-only claims, source summaries, and contribution
provenance, excludes Rock issue routing records, and uses compact model digests.
Canonical IDs remain the same.

The distribution excludes private organization overlays, raw transcripts and media, review queues, live-instance evidence, evaluations, telemetry, and redundant generated indexes.

## Download And Inspect

Install `uv` if needed, then use the published client without permanently installing it:

```bash
uvx rock-kb okf download
uvx rock-kb okf inspect rock-agent-kb-okf-vX.Y.Z.zip
uvx rock-kb okf conformance third-party-okf.zip
uvx rock-kb okf verify rock-agent-kb-okf-vX.Y.Z.zip
uvx rock-kb okf download --profile core
```

`download` retrieves the latest full ZIP by default and requires a matching release checksum or GitHub asset digest. Prefer `--profile core` for a smaller local agent index; use `full` when the consumer needs Rock issue records, routing-only claims, source summaries, and contribution provenance. Use `--format tar.gz`, `--version X.Y.Z`, or `--destination <path>` when needed. `conformance` applies generic OKF rules and reports unresolved links or unknown versions as warnings. `verify` applies the stricter Rock profile, integrity, licensing, structured-record, and public-safety rules. `validate` remains an alias for `verify` for older agents.

The same commands work after a permanent client install:

```bash
uv tool install rock-kb
rock-kb okf download
```

Release assets include:

- `rock-agent-kb-okf-vX.Y.Z.zip`;
- `rock-agent-kb-okf-vX.Y.Z.tar.gz`;
- `rock-agent-kb-okf-vX.Y.Z.sha256`.
- `rock-agent-kb-okf-core-vX.Y.Z.zip`;
- `rock-agent-kb-okf-core-vX.Y.Z.tar.gz`;
- `rock-agent-kb-okf-core-vX.Y.Z.sha256`.

## Build From The Repository

Maintainers can build and validate the distribution locally:

```bash
uv run kb publish okf
uv run kb publish okf --profile core --destination data/okf-export-core
uv run kb publish okf-validate data/okf-export
uv run kb publish okf-validate data/okf-export-core
```

To produce release archives:

```bash
uv run kb publish okf \
  --version X.Y.Z \
  --source-commit "$(git rev-parse HEAD)" \
  --archive-dir release-assets
```

The ignored export directories are generated output, not contributor edit targets. Set `SOURCE_DATE_EPOCH` to the source commit time for byte-reproducible archives. Manifests include source commit, generation time, profile, upstream spec pin, licensing, content hashes, and a meaningful delta against the previous release. Release archives also receive GitHub artifact attestations.

## Conformance And Safety

Generic conformance enforces the required OKF v0.1 `type` frontmatter while tolerating broken links and unknown versions as the upstream specification recommends. Strict Rock verification additionally enforces reserved-file behavior, date-only logs, complete checksums, exact structured-record links, archive entry/size/compression limits, duplicate-path rejection, licensing, and public/private boundaries. The release workflow runs Google's pinned reference parser against the core profile, and a weekly monitor fails when the upstream specification changes.

## Import Policy

Rock KB does not import arbitrary OKF bundles into trusted knowledge. Future import support must be review-gated and route records through the existing contribution process, including identity deduplication, source authority, licensing, redaction, public-safety, and maintainer approval. Importing a bundle must never bypass those controls or merge organization-private knowledge into the public index.
