# Rock Ideas Intelligence

Rock Community Ideas are indexed as bounded metadata for finding known feature gaps and tracking community roadmap states.

## Trust Boundary

- An idea is a community request, not an approved product claim.
- `Planned`, `Started`, and `Complete` are roadmap labels. Confirm actual release availability through official documentation, release notes, source code, and local read-only checks.
- The public KB does not republish proposal bodies, comments, submitter identities, organization identities, or staff response text.

## Agent Use

1. Search Ideas only when the question is explicitly about a feature request, known product gap, or roadmap state.
2. Use typed relationships to route to concepts, exact multiword models, explicitly linked issues, and corroborating official records.
3. Treat `references_issue` as an explicit link only. It does not prove the issue implements the Idea; `implemented_by_issue` requires official release-note evidence.
4. If the idea has a planned version or completed state, corroborate it with official release evidence before saying the feature is available.
5. Treat open and not-planned ideas as research leads, not proof that no workaround or newer capability exists.
6. Use the verification queue to prioritize lifecycle claims. A queue state or private candidate count is not public evidence; only reviewed or deterministic official relationships can corroborate availability.

Current generated catalog: 1091 metadata rows. See [`agent/rock-ideas.jsonl`](../../agent/rock-ideas.jsonl), [`agent/rock-idea-relationships.jsonl`](../../agent/rock-idea-relationships.jsonl), [`agent/rock-idea-verification-queue.jsonl`](../../agent/rock-idea-verification-queue.jsonl), and [`agent/rock-idea-summary.json`](../../agent/rock-idea-summary.json).
