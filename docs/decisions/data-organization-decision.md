# Data Organization Decision

## Decision

Use a Karpathy-style LLM wiki as the core knowledge shape, strengthened with explicit provenance, license gates, and generated agent indexes.

This means the repo is not just an Obsidian vault and not just a vector database. It is a hybrid structure:

- `sources/` defines what can be collected, how often, with what tool, and under what license posture.
- `data/raw-manifests/` records fetch metadata, source hashes, discovered URLs, and extraction details.
- `data/normalized/` stores structured JSONL records that agents and scripts can process predictably.
- `knowledge/` stores curated Markdown organized by Rock domain.
- `agent/` stores generated navigation such as `llms.txt`, topic indexes, release indexes, and citation maps.
- `data/index/` stores generated local search artifacts such as SQLite FTS.

## Why This Shape

Recent AI knowledge-base patterns have converged around Markdown-first systems that agents can read and maintain directly. Andrej Karpathy's 2026 LLM knowledge-base pattern emphasizes compact, interlinked Markdown maintained by agents instead of treating RAG/vector retrieval as the primary memory layer. The broader ecosystem is moving in the same direction with AI-readable files such as `llms.txt`, generated codebase wikis, and source-grounded agent navigation.

For Rock RMS, this is especially important because source trust matters:

- Official Rock docs and release notes should be cited clearly.
- Community recipes and Q&A should be useful but labeled as community-contributed.
- Code repositories have mixed licenses and should be license-gated.
- Private repo material must stay behind review and sanitization.
- Version-specific behavior matters, especially for release notes and mobile docs.

## Practical Rule

Markdown is the working knowledge layer. JSONL manifests are the audit and automation layer. SQLite/vector indexes are access layers only.

