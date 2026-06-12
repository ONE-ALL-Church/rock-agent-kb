# Claim Graph Research Notes

## Purpose

These notes frame the claim graph and private corpus refactor against adjacent open-source systems. The conclusion is not that this project should be replaced. The conclusion is that this repo should stay the source of truth, while borrowing proven ideas from structured knowledge systems, RAG/search systems, and agent-oriented local wikis.

The target is a Rock-specific, agent-first knowledge base that is:

- source-backed
- community-contributable
- public/private aware
- Markdown and JSONL friendly
- rebuildable from source evidence
- portable across trusted machines
- safe to publish publicly

## Current Repo Fit

This repo already has many of the required primitives:

- source registry and source policy in `sources/registry.yaml`
- concept registry in `concepts/registry.yaml`
- normalized records
- source summaries and citation maps
- media discovery, transcription, sidecars, candidates, and promotions
- private/public audit boundaries
- contribution bundle scaffolding
- concept guide builds
- agent packs
- public export
- readiness tests

The missing center is a first-class `claim` model. Existing media promotions and contribution rows are close to claims, but the project should converge them into one explicit evidence-backed claim graph.

## Open-Source Systems Reviewed

### Wikibase / Wikidata

Wikibase is the strongest conceptual reference. Its core model is close to the desired shape: entities have statements, statements contain claims, and claims can carry references. It also has a mature mental model for community editing, provenance, identifiers, and linked open data.

Lessons to borrow:

- represent durable claims separately from prose pages
- attach references directly to claims
- use stable IDs for entities, properties, statements, and sources
- allow claims to have qualifiers such as version, time, scope, or applicability
- preserve provenance even when multiple sources support or conflict with a claim
- support community contribution without treating every contribution as equally authoritative

Reasons not to migrate wholesale:

- not Markdown/git-first
- not agent-first by default
- heavier operationally than this project needs today
- not tailored to private media transcripts and public distilled exports
- does not directly solve Rock-specific ingestion, guide generation, or private/public corpus separation

Design implication: make this repo internally more Wikibase-like, but keep the implementation local, file-based, and Rock-specific.

### Semantic MediaWiki

Semantic MediaWiki shows another mature approach to structured assertions inside a wiki. Its reference/provenance datatype is especially relevant because it associates a value with provenance metadata.

Lessons to borrow:

- structured annotations can coexist with human-readable pages
- provenance should be queryable, not buried in prose
- semantic properties need clear constraints and predictable display

Reasons not to migrate wholesale:

- wiki-page authoring model is not ideal for generated agent packs
- MediaWiki operations and extension complexity are unnecessary for the current repo
- the current project already has better source-ingestion and public/private controls for this use case

### Onyx

Onyx is useful as a reference for source connectors and enterprise search. It focuses on syncing external systems, grounding answers in documents, and respecting permissions in enterprise contexts.

Lessons to borrow:

- connector abstraction for external source families
- metadata and permission signals matter for answer quality
- retrieval UI can be separate from the canonical knowledge model

Reasons not to use as source of truth:

- primarily search/chat over documents, not a reviewed claim graph
- does not produce source-controlled public guide artifacts
- does not replace contribution review, redaction, or guide rebuild logic

Potential role later: optional retrieval/search layer over the public repo and private corpus.

### OpenDocuments

OpenDocuments is a self-hosted RAG platform with connectors for GitHub, Notion, Google Drive, Confluence, local files, web sources, Swagger/OpenAPI, and many file formats. It supports hybrid retrieval and cited answers.

Lessons to borrow:

- broad connector coverage
- hybrid keyword/vector retrieval
- MCP/tool access for agents
- source metadata, citations, and security controls

Reasons not to use as source of truth:

- standard RAG architecture does not create reviewed durable claims
- query-time synthesis is not the same as rebuildable guides
- less suited to publishing a public distilled repo with audit gates

Potential role later: private or self-hosted search service for the corpus.

### Docmancer

Docmancer is a local-first retrieval engine for coding agents. It is especially relevant because it is agent-oriented, local-first, and returns compact source-attributed context packs.

Lessons to borrow:

- local-first indexing can be enough for strong agent use
- agents benefit from compact context packs with file paths and URLs
- explainable retrieval signals are useful for debugging source selection

Reasons not to use as source of truth:

- retrieval engine, not a claim review or publication system
- does not model community contributions or public/private publishing rules
- does not replace deterministic guide and agent artifact generation

Potential role later: local query tool over checked-out public and private corpora.

### Synthadoc

Synthadoc is directionally close because it compiles raw documents into a structured local wiki and emphasizes contradiction detection, graph links, source hashes, and audit logs.

Lessons to borrow:

- precompiled knowledge can be better than pure query-time RAG
- contradiction detection should happen during ingest/review, not only at answer time
- source hashes, job history, and audit logs are first-class artifacts
- local wiki output should be human-readable and agent-readable

Reasons not to replace this repo:

- younger/general-purpose system
- not Rock-specific
- may publish full transcript-style pages in ways that do not match this project's public/private policy
- current repo already has source family parsers, media review, and Rock concepts

Potential role later: compare design patterns or borrow contradiction/lint ideas.

### SwarmVault / Agent Wikis

Agent-wiki projects are relevant because they optimize for local graph building, Markdown output, and agent context.

Lessons to borrow:

- local graph inspection is useful
- agent context packs should be explicit artifacts
- Markdown remains a durable interface for humans and agents

Reasons not to replace this repo:

- generic memory/wiki orientation
- less focus on source authority, licensing, public export, and Rock-specific source ingestion

### BookStack / Outline

BookStack and Outline are strong human-facing knowledge bases. They provide editing, permissions, collaboration, APIs, and search.

Lessons to borrow:

- good human editing and review UX matters
- permissions and audit logs matter for collaborative knowledge
- public sharing and private editing can be separate

Reasons not to use as source of truth:

- page-centric rather than claim-centric
- not designed around source-backed guide rebuilds
- not ideal for git-based public exports and agent packs

Potential role later: optional human-facing publication or editor surface, not canonical data.

### Open Semantic Search

Open Semantic Search is relevant for broad-source indexing, OCR, metadata enrichment, RDF/SKOS, watchlists, and search over many content types.

Lessons to borrow:

- source monitoring and change alerts are valuable
- OCR/image/media-derived text can be part of a private corpus
- metadata taxonomies improve discoverability

Reasons not to use as source of truth:

- primarily search/indexing infrastructure
- does not solve claim review and guide generation

## Architectural Conclusion

The best path is a hybrid:

1. Keep this repo as the canonical public source of truth.
2. Add a portable private corpus for raw/private processing artifacts.
3. Add private object storage for large media binaries.
4. Refactor existing candidates/promotions/contributions into a first-class claim graph.
5. Borrow Wikibase's claim/reference mental model.
6. Borrow RAG/search systems' connector and retrieval ideas.
7. Borrow agent-wiki systems' local-first, Markdown/graph, audit-log ideas.
8. Keep public outputs deterministic, auditable, source-linked, and safe to publish.

## Design Principles For Implementation

- **Claims over prose:** prose guides are generated or reviewed outputs; approved claims are the durable public knowledge units.
- **Evidence before synthesis:** every public claim must trace to a source URL, source record, commit, timestamp, or reviewed private evidence hash.
- **Authority is visible:** official, source-code-confirmed, release-note-confirmed, and community-reviewed claims must remain distinguishable.
- **Private stays portable:** transcripts and private review data should be private, but not laptop-bound.
- **Public stays clean:** public export must fail when raw transcripts, direct media URLs, secrets, private paths, or copied protected source text leak.
- **Community input is candidate input:** community submissions enter review queues and become guide material only after promotion.
- **Guides are rebuildable views:** changed sources and claims should identify stale concept guides, task cards, source maps, and agent packs.
- **Use external systems as satellites:** retrieval/search tools may index this repo and private corpus, but should not replace the claim graph as source of truth.

## Candidate External Roles

- **Wikibase export:** future optional export for structured linked data if the community claim layer grows.
- **JSON-LD/RDF export:** future interoperability format for claims, sources, concepts, and authority tiers.
- **Onyx/OpenDocuments:** optional hosted/self-hosted search UI over public and private corpora.
- **Docmancer:** optional local agent retrieval over checked-out docs and private corpus.
- **BookStack/Outline:** optional human-facing documentation surface generated from public artifacts.

None of these should be prerequisites for the core repo workflow.
