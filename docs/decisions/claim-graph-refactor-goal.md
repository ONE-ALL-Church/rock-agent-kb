# Claim Graph And Private Corpus Refactor Goal

## Short Goal

Refactor the Rock RMS General Knowledge Base into a three-layer, agent-first knowledge system: a public distilled repo, a portable private corpus, and optional private object storage for large media. Keep this public repo as the source of public-safe generated knowledge, but make the durable unit of knowledge an approved, source-backed claim. Add a private corpus strategy so transcripts, sidecars, review candidates, normalized private records, source manifests, and other non-public processing artifacts are not trapped on one laptop forever. Do not publish raw transcripts, downloaded media, private source text, tokenized media URLs, secrets, internal URLs, or copied protected material. Do not rebuild from scratch or migrate wholesale to Wikibase, Onyx, OpenDocuments, Docmancer, or another platform. Instead, evolve the current repo and borrow the strongest Wikibase idea: claims/statements with references, review state, confidence, authority tier, and provenance.

## Why

The project should be more than a documentation mirror or a generic RAG index. It should become an agent-first Rock implementation intelligence base that combines official sources, source-code evidence, and reviewed community experience without blurring their authority. At the same time, the private working corpus should be durable and portable for the owner. Raw transcripts and private review data should remain private, but they should be recoverable from another trusted machine through a private repo or encrypted storage strategy.

## Repository And Storage Shape

Use three layers:

1. **Public repo**
   - This repo remains the public project.
   - It contains public-safe distilled guides, concept indexes, source summaries, citations, claim exports, contribution schemas, task cards, agent packs, source maps, dependency metadata, and public audit tooling.
   - It must never contain raw transcripts, downloaded media files, private repo scans, private review notes, copied protected source text, secrets, internal URLs, or tokenized media URLs.

2. **Private corpus repo**
   - A separate private GitHub repo or equivalent private git remote stores portable private processing artifacts.
   - It should preserve the same local paths where practical, such as `data/media/`, `data/normalized/`, `data/review/`, `data/raw-manifests/`, and `data/index/`.
   - It may include transcript JSON, transcript sidecars, media indexes, review candidates, reviewer rewrites, private promotions, private normalized records, benchmark results, source manifests, private dependency maps, and rebuild state.
   - Access should be limited to the owner and trusted maintainers.

3. **Private object storage for large binaries**
   - Large `.mp3`, `.mp4`, `.wav`, downloaded video, frame, and clip files should not be stored in normal git.
   - Use Git LFS, DVC, rclone/restic, S3/R2/Backblaze, or another private encrypted object store.
   - The private corpus repo should track manifests, hashes, and restore pointers for these objects.

The public repo should be rebuildable when the private corpus is mounted locally, but it should remain safe to publish when the private corpus is absent.

## Target Claim Model

Add a first-class `claim` data contract. A claim should be a short durable statement, not a copied source excerpt. Each claim should include:

- stable `claim_id`
- `claim`
- `claim_type`
- `concept_ids`
- `source_refs`
- `source_record_ids`
- `authority_tier`
- `confidence`
- `review_status`
- `license_status`
- `public_publish_mode`
- `rock_versions`
- optional `timestamp`, `timestamp_seconds`, `source_timestamp_url`
- optional private corpus pointer or evidence hash when safe
- `needs_live_verification`
- `created_at` and `updated_at`

Authority tiers should distinguish at least:

- `official`
- `source-code-confirmed`
- `release-note-confirmed`
- `community-reviewed`
- `community-unreviewed`
- `agent-inference`
- `private-draft`
- `needs-live-verification`

## Pipeline

The desired pipeline is:

```text
sources/registry.yaml
  -> raw/private ingest
  -> private corpus artifacts
  -> normalized evidence records
  -> claim candidates
  -> review/rewrite/promotion
  -> approved claim graph
  -> concept dependency graph
  -> guide.md, index.md, task cards, agent cards, source maps, public export
```

Raw transcripts, private source text, downloaded media, private repo scans, and reviewer notes stay in the private corpus. Public artifacts may contain only reviewed distilled claims, source URLs, source hashes, timestamps where safe, and short summaries within source policy.

## Existing Code To Preserve

Do not discard the current implementation. Preserve and evolve:

- `sources/registry.yaml`
- `concepts/registry.yaml`
- normalized records under `data/normalized/`
- public/private checks
- media discovery, transcription, sidecars, candidates, and promotions
- contribution bundle validation
- concept guide builds
- agent pack builds
- public export
- audit readiness tests

Existing contribution rows and media promotions are close to claims. Migrate or adapt them into the claim model instead of creating a parallel system.

## Private Corpus Tooling Goal

Add CLI support for private corpus portability:

- initialize or validate a private corpus checkout
- report which local ignored files are private corpus artifacts
- sync or copy private text/JSON artifacts into the private corpus
- write restore manifests for large media objects
- verify that public export can be rebuilt from the mounted private corpus
- audit that no private corpus files leak into the public repo
- document how a second machine should clone the public repo, clone the private corpus repo, restore large media if needed, and run the KB pipeline

The private corpus workflow should not require publishing private data to the public repo. It should also not require every machine to restore large media files unless transcription or visual reprocessing is needed.

## Community Contribution Goal

Community members and their agents should be able to submit source-backed knowledge through GitHub PRs. A submission should be accepted as a candidate, not automatically trusted. A valid public contribution should identify the source URL or source record, the distilled claim, relevant concepts, confidence, review status, license/redaction attestations, and whether live verification is needed.

The contribution path should support:

- community recipes
- public GitHub projects related to Rock RMS
- plugin examples
- blog posts
- conference talks
- community hub media
- operational patterns from churches or consultants

The system should mark community material as community-derived even after review. Reviewed community claims may inform guides, but guides should label them separately from official behavior and source-code-confirmed behavior.

## Guide Generation Goal

Guides should become rebuildable views over approved claims. A guide should be able to include:

- official documented behavior
- source-code-confirmed implementation details
- release/version caveats
- community-reviewed patterns
- examples and recipes
- risks and gotchas
- related GitHub projects
- open questions
- source bibliography

When new sources or claims are added, the tooling should identify affected concepts, compare claim hashes against dependency metadata, and report whether generated indexes, agent packs, or long-form `guide.md` files need refresh.

## External Systems Decision

Do not adopt a full external replacement at this stage. Wikibase has the best conceptual model for claims with references, but it is not agent-first, Markdown/git-first, or tailored to Rock source ingestion, media processing, private corpus sync, and public/private publication rules. Onyx, OpenDocuments, and Docmancer are useful retrieval systems, but they do not replace the need for a reviewed claim graph. They may be used later as optional retrieval/search layers over the public repo and private corpus.

The comparison frame and design lessons from adjacent open-source systems are documented in [Claim Graph Research Notes](claim-graph-research-notes.md).

## Success Criteria

This refactor is successful when:

- approved claims are the central public knowledge unit
- every public claim traces to evidence
- private transcripts and review artifacts are portable through a private corpus repo or private storage
- large media can be restored from private object storage when needed
- community submissions can be validated and reviewed
- guides can be rebuilt from approved claims
- official, source-code, and community authority are clearly separated
- public export audits prevent raw/private leakage
- source changes identify stale claims and guides
- agent packs expose compact, source-backed, concept-routed knowledge
- a new trusted machine can clone the public repo, attach the private corpus, and continue processing without relying on the original laptop
