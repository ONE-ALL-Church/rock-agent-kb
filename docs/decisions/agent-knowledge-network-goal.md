# Agent Knowledge Network Goal

> **Historical status:** This goal records the architecture sequence used to
> build the current network. The Milestone 0 refactor checklist is retired and
> no longer an active task tracker. Use current audits, evaluations, freshness,
> and review queues for ongoing prioritization.

## North Star

One knowledge base for Rock RMS that combines official documentation, source-code evidence, release knowledge, and community insights — kept in clearly labeled authority tiers — that **any agent can use over the network without setup**, and that **other churches' agents can contribute to almost autonomously**: an agent submits distilled knowledge, automated gates validate it, it becomes immediately usable at a clearly-labeled community trust tier, and human review promotes it toward authoritative status.

The measure of success: a staff member at another church tells their agent "figure out why our check-in labels stopped printing," and that agent (a) queries this knowledge base first instead of web search, (b) gets source-cited, version-aware, tier-labeled answers, and (c) when it discovers something new in the process, submits that insight back — and the insight is visible to the next church's agent within the hour, labeled `community-unreviewed`, without a human in the submission loop.

## What "Almost Autonomous" Means Precisely

Full autonomy (agent-submitted content silently becoming authoritative guidance) is an anti-goal — it is how a knowledge base poisons itself. The design target is:

| Step | Actor | Gate |
|---|---|---|
| Submit a contribution | Any registered org's agent, no human | Schema validation, leak/PII checks, license attestation, size/rate limits — all automated |
| Publish at `community-unreviewed` tier | Automated (auto-merge) | All automated checks green; submission touches only the org's own intake path; org is registered |
| Serve to consuming agents | Automated | Tier label always attached; answer synthesis never blends unreviewed claims into authoritative prose |
| Promote to `community-reviewed` / `answer_pack_approved` | Human reviewer (maintainer or trusted reviewer from any org) | Existing claim-tier policy (`docs/decisions/claim-tier-policy.md`) |
| Promote to `live_verified` | Human + read-only evidence | Existing live-verification workflow |

Humans never gate *submission* or *availability*; they gate *authority*. That is the whole trick.

## Architecture Decision

**Build on the existing pipeline plus three commodity systems. Do not adopt an external knowledge platform.**

| Considered | Decision | Reason |
|---|---|---|
| Existing `rock_kb` pipeline (claims, tiers, audits, distillation) | **Keep — it is the core asset** | The claim graph with authority tiers and leak-audited public export is the differentiator; no off-the-shelf system has it |
| Git + GitHub (repos, PRs, Actions, CODEOWNERS) | **Adopt as governance machinery** | Provenance, review, identity, audit history, and automation for free; agents already speak the GitHub API |
| Cloudflare Workers + D1 + R2 | **Adopt as the serving plane** | Always-on, cheap at this corpus size, already in the maintainer's stack; first-class remote-MCP support |
| MCP (Model Context Protocol) | **Adopt as the consumption *and* contribution protocol** | The emerging standard; agents connect with one config line; tools work identically for Claude, Codex, and others |
| Wikibase | **Rejected** (re-confirmed from `claim-graph-research-notes.md`) | Right claim model, wrong platform: heavy, PHP, not git-native, not agent-first |
| Hosted RAG platforms (Onyx, etc.) | **Rejected as source of truth** | Retrieval without a review/authority model; may be layered on later as optional search |
| Vector DB as the knowledge store | **Rejected** | FTS over distilled claims/guides is sufficient at this scale; embeddings are an optional ranking enhancement, never truth |

## System Shape: Two Repos, Three Planes

```text
┌────────────────────────────────────────────────────────────────────┐
│ KNOWLEDGE PLANE (source of truth: git)                             │
│  THE REPO (public, fresh clean history): pipeline code,            │
│    registries, claims/, knowledge/, agent/, audits, service/,      │
│    intake (community-contributions/, source-suggestions/, orgs/)   │
│  private corpus repo (private): transcripts, raw source text,      │
│    private scans, review drafts, candid session logs               │
└──────────────┬────────────────────────────────▲────────────────────┘
               │ CI (same repo): kb build +     │ auto-merge after
               │ audits → deploy artifacts      │ automated gates
┌──────────────▼──────────────────┐  ┌──────────┴───────────────────┐
│ SERVICE PLANE (Cloudflare)      │  │ CONTRIBUTION PLANE (GitHub)  │
│  Remote MCP server (Worker)     │  │  Path A: PR from any agent   │
│   kb_search / kb_get_concept /  │  │   or human to the repo       │
│   kb_get_claims / kb_manifest / │  │  Path B: kb_submit MCP tool  │
│   kb_submit                     │  │   → Worker validates →       │
│  D1: FTS index   R2: artifacts  │  │   opens PR via GitHub App    │
│  HTTPS JSON + llms.txt +        │  │  Path C: rock-kb CLI submit  │
│   rock-kb consumer CLI          │  │   → same endpoint as B       │
│   (read-only)                   │  │  Actions: validate → label → │
│                                 │  │   auto-merge (unreviewed     │
│                                 │  │   tier) or hold for review   │
└─────────────────────────────────┘  └──────────────────────────────┘
```

Git remains the single source of truth — **one public repo** (born clean in Milestone 0.5) plus the private corpus repo. The service plane is a disposable, rebuildable projection of the repo's audited artifacts — if the Worker and D1 vanished, nothing would be lost. The contribution plane writes only to intake folders; nothing reaches generated artifacts except through `kb build` and the audits, which run as CI in the same repo. There is no separate distribution repo and no cross-repo import/publish machinery — that entire class of sync drift and credential plumbing is deleted by design.

**Repository visibility (decided 2026-06-11 — single public repo):**

| Repo | Visibility | Notes |
|---|---|---|
| The repo (pipeline + knowledge + intake + service) | **Public** — created fresh in Milestone 0.5 with a single curated initial commit | Fork-and-PR intake, agent read surface (clone, raw-file fetch, `llms.txt`), auditable provenance behind every claim, and a fully inspectable pipeline — transparency is part of the trust pitch to other churches |
| Existing private build repo (`ONE-ALL-Church/Rock-General-Knowledge-Base`) | **Archived, private** after migration | Its history was never audited for publication; it is never flipped public. Milestone 0 executes there; Milestone 0.5 migrates the refactored tree out |
| Private corpus repo | **Private, always** | Raw transcripts, scraped full text, private scans, review drafts, and (from Milestone 0.5) candid session logs |

Consuming agents have four read paths, all serving identical content: the remote MCP tools (query-shaped, the default for rich clients), the `rock-kb` consumer CLI (self-installable via `uvx rock-kb` — the default for terminal agents), plain HTTPS/`llms.txt` on the Worker, and the public git repo directly (bulk access and provenance verification).

## Trust and Identity Model

- **Authority tiers are the spine.** The existing vocabulary (`official`, `source-code-confirmed`, `release-note-confirmed`, `community-reviewed`, `community-unreviewed`, …) and claim tiers (`routing_context_only` → `live_verified`) are unchanged. Every served answer, claim, and search hit carries its tier. Consuming agents are told (in tool descriptions and result metadata) to treat `community-unreviewed` as "a peer church reported this" — useful lead, not ground truth.
- **Org registry.** Contributing organizations register once via PR to the repo: `orgs/<org-id>.yaml` with display name, contact, GitHub account(s) or App identity used for submissions, and standing attestation defaults. Registration is reviewed by a human (one-time, minutes). Unregistered submissions are never auto-merged.
- **Per-org sandboxing — a security boundary, not a tidiness rule.** Auto-merge applies only when a PR touches exclusively `community-contributions/<that-org-id>/**` or `source-suggestions/<that-org-id>/**`. Anything touching another org's folder, generated artifacts, code, `service/`, or `.github/` waits for human review. Because intake shares the repo with pipeline code and CI workflows, this is enforced server-side — repository rulesets restricting paths plus branch protection with required checks — never by the Actions check alone. Intake-PR validation workflows run with zero access to secrets (plain `pull_request` events, never `pull_request_target` with PR-code checkout); deploy credentials live in a GitHub Environment scoped to `main`.
- **Review ladder.** Maintainer reviews promotions today; the structure anticipates trusted reviewers from other orgs later via GitHub teams + CODEOWNERS on `contributions/`. Reviewer identity is recorded on promoted rows (existing `reviewer` fields).
- **Abuse limits.** Rate limit `kb_submit` per org token (Worker-side), cap bundle size and rows per PR (validator-side), and require the standing attestations. Repeated rejected submissions suspend an org's auto-merge (flag in `orgs/<org-id>.yaml`).
- **Both-direction privacy.** The leak checker protects this project's private corpus from leaking out, and screens *incoming* contributions for other churches' private data (person names in operational contexts, internal URLs, tokens, secrets). Ambiguous rows fail closed into the human review queue.

## Milestones

### Milestone 0 — Foundation (already specified)

Execute `docs/decisions/incremental-architecture-refactor-goal.md` in full, in the existing private repo. The parts this goal depends on hardest: the pipeline engine (`kb status`/`kb build`) for unattended rebuilds, the schema layer with the shared leak checker, the contribution state machine and standalone validator (its Phase 5), and local `kb serve` (its Phase 6), which becomes the dev-parity twin of the hosted server.

**Amendments from the single-repo decision** (also noted in that document's header): (1) in its Phase 5 Task 5.4, create the validation workflow, validator script, and CONTRIBUTING file at their real paths — `.github/workflows/validate-contributions.yml`, `scripts/validate_bundle.py`, `community-contributions/CONTRIBUTING.md` — the `templates/public-repo/` indirection is retired; (2) do not extend `publish push` or `contributions import-public` — both retire in Milestone 0.5; (3) treat `data/public-export/` as legacy: keep its audit logic, which Milestone 0.5 repurposes to audit the public tree and deploy payload directly.

**Done when:** that document's Final Verification checklist passes (as amended).

### Milestone 0.5 — Single-Repo Migration and Hardening

Collapse the planned build/distribution split into one public repo. Runs after Milestone 0 so there is exactly one history-curation event and the messy mid-refactor states stay out of public history.

**Deliverables:**

1. **Curate.** Move candid material to the private corpus repo: `docs/log/` session notes, review triage notes, anything the maintainer wouldn't sign publicly. Establish the convention going forward (dated working logs live in the corpus repo) and encode it in the repo's agent instructions (CLAUDE.md / AGENTS.md): agents never write candid notes, private data, or anything from `data/` into this repo.
2. **Vouch the tree.** The fresh repo gets a single squashed initial commit, so only the tree (not history) needs auditing: run the shared leak checker over every tracked file, a full gitleaks-style secret scan, and `kb audit all`. Fix anything found before the first push.
3. **Create and migrate.** New public repo under ONE-ALL-Church (suggested name: `rock-agent-kb`; moving to an independent GitHub org later is a governance option, not a blocker). Push the curated, refactored tree as the initial commit. Archive the old private build repo read-only — history preserved privately, never flipped public. Update local checkouts, Codex/agent workflows, and CI references.
4. **Harden before automating.** All of this is verified active *before* any intake or deploy automation lands: GitHub secret scanning + push protection; branch protection with required checks; repository rulesets restricting which paths PRs may touch (the auto-merge boundary, server-side); CODEOWNERS requiring maintainer review on everything outside intake folders; GitHub Environment (scoped to `main`) for deploy secrets; a documented local pre-commit hook running the leak checker + secret scan; and a CI tracked-tree assertion test — no file under private path prefixes is ever tracked, no tracked file matches leak patterns.
5. **Retire the split machinery.** Delete `publish push`, `contributions import-public`, and the tracked `data/public-export/` copy; `kb deploy-service` (Milestone 1) projects directly from `claims/`, `knowledge/`, and `agent/`. The export audit logic is retained as the public-surface audit run in CI. Status: tracked export removal is complete; command retirement is complete.

**Current implementation status (2026-06-12):**

- Curate: complete. Local convention is encoded in `AGENTS.md`, `data/` is ignored and untracked, and tracked private path prefixes are blocked by `scripts/audit_tracked_tree.py`.
- Vouch: complete for the public tree. The curated tree passed tracked-tree audit, bundle validation, gitleaks, `kb audit all`, full tests, fresh-clone `kb build`, and public CI checks.
- Create and migrate: complete. The public repo is `https://github.com/ONE-ALL-Church/rock-agent-kb`, created from a single curated initial commit with message `Initial public Rock agent KB`.
- Harden before automating: complete for the no-auto-merge launch state. Secret scanning, push protection, branch protection, CODEOWNERS review, required checks, an active branch ruleset, and a protected `production` environment are enabled. Proof PR #1 touched `.github/workflows/validate-contributions.yml`, remained review-required/blocked, and did not auto-merge. A throwaway push containing a dummy Slack Incoming Webhook URL was rejected server-side by GitHub push protection. GitHub rejected public-repo push rulesets with file-path restrictions (`Source public repos cannot have push rules`), so future auto-merge must not launch until a GitHub App or equivalent server-side path gate enforces the per-org intake boundary without deploy secrets.
- Retire split machinery: tracked export removal, command retirement, and public-surface audit reuse are complete.

**Done when:** the public repo exists with one clean initial commit and green CI; a test PR touching a workflow file demonstrably does not auto-merge; a push containing a planted test secret is blocked server-side; the old repo is archived; and `kb status` / `kb build` / `kb audit all` work from a fresh clone.

### Milestone 1 — Hosted Read Service

Any agent can query the knowledge base over the network with one line of MCP config and zero authentication for reads.

**Deliverables:**

1. **Worker project** in this repo under `service/` (TypeScript, wrangler config committed; secrets via wrangler secrets, never in git). Cloudflare account/IDs parameterized.
2. **Remote MCP server** on the Worker (streamable HTTP transport, using Cloudflare's MCP/agents support) exposing the same five read tools as local `kb serve` — `kb_search`, `kb_manifest`, `kb_list_concepts`, `kb_get_concept`, `kb_get_claims` — with identical result shapes, so the local stdio server and the hosted server are interchangeable. Every result row includes `authority_tier`, `claim_tier`, and source citations.
3. **Data projection.** A `kb deploy-service` CLI command that projects the public artifacts into the service stores: FTS-indexed rows into D1 (schema generated from the same data that builds the local SQLite index — one indexing code path, two targets), bulk artifacts (guides, quickstarts, manifest) into R2. Deploys are atomic: write to a versioned namespace/prefix, then flip an alias; never serve a half-deployed corpus.
4. **Plain HTTPS read surface** for non-MCP consumers: `GET /llms.txt`, `GET /manifest.json`, `GET /concepts/<id>.md`, `GET /search?q=` returning JSON. Read-only, cache-friendly.
5. **CI deploy.** A GitHub Actions workflow in the repo: on push to `main` affecting served artifacts → run audits → `kb deploy-service` → smoke-test the live endpoints. Deploy secrets come from the `main`-scoped GitHub Environment (Milestone 0.5); intake-PR validation workflows never see them. The service never serves content that did not pass `kb audit all`.

**Done when:** from a machine with no checkout, an agent added via one MCP config block answers a Rock question with tier-labeled, source-cited results; killing and redeploying the Worker from CI loses nothing.

**Current implementation status (2026-06-12):**

- Repo-side implementation is complete: `service/` contains the Cloudflare Worker, `kb deploy-service` builds D1/R2 deployment payloads from the audited public artifacts, the Worker exposes MCP-style tools plus plain HTTPS endpoints, and `.github/workflows/deploy-service.yml` runs the service build/audit/deploy path.
- Local validation passed: `kb deploy-service` produced 1,454 deployable artifacts and 4,018 search rows; TypeScript checking passed; Wrangler deploy dry-run passed.
- Live completion still requires external configuration: real Cloudflare account secrets, D1 database id, R2 bucket, production deploy approval, and a successful post-deploy `kb eval-service` run against the live URL.

### Milestone 2 — Autonomous Contribution Intake

A registered org's agent can submit knowledge and see it served within the hour, no human touch on the happy path.

**Deliverables:**

1. **Org registry** (`orgs/` in the repo): schema, example, registration runbook, and validation in CI. Registration PRs are human-reviewed.
2. **`kb_submit` MCP tool** on the Worker: accepts a contribution bundle (same `rock-kb-org-contribution-v1` rows, JSON), authenticated by per-org token issued at registration. The Worker runs the same validation the standalone validator runs (schema, vocabularies, leak/PII patterns, size caps), then opens a PR against the repo via a GitHub App, placing rows in `community-contributions/<org-id>/`, with the validation report in the PR body. Invalid bundles are rejected at the tool with row-level errors the agent can fix and retry — the feedback loop that makes agent submission actually work.
3. **Auto-merge policy**: validation green + registered org + paths confined to that org's intake folders (enforced server-side per the trust model) → auto-merge. Otherwise label for human review with the failure report.
4. **Automated rebuild-deploy loop** (same repo): on merge to intake paths (or scheduled), accepted bundle rows enter the claims pipeline as candidate/`community-unreviewed` per the Milestone 0 state machine → `kb build` → `kb audit all` → bot-commit the regenerated artifacts with pinned `ROCK_KB_GENERATED_AT` → `kb deploy-service`. Fully unattended; failures notify the maintainer and halt (never deploy on a failed audit). No cross-repo import exists.
5. **Unreviewed tier served honestly.** `kb_search` and `kb_get_claims` include `community-unreviewed` rows by default with the tier prominent; `kb_get_concept` guide prose continues to draw only on reviewed tiers per existing policy. Add a `min_tier` filter parameter to the read tools.
6. **Review queue surfaced.** `kb status` (and a generated dashboard page on the service) shows pending promotions by org and concept, so the human half of the loop has one place to look.
7. **Consumer CLI (`rock-kb`).** A thin client published to PyPI from `clients/python/` in this repo, self-installable by agents with no human setup: `uvx rock-kb search "..."`. Commands map 1:1 onto the public surface: `search [--min-tier]`, `concepts`, `get <concept-id>`, `claims <concept-id> [--tier]`, `manifest`, `validate <bundle.jsonl>` (fully offline — bundles the same parity-tested standalone validator from Milestone 0), `submit <bundle.jsonl> --org <id>` (token from `ROCK_KB_TOKEN`, hits the same endpoint as `kb_submit`), and `mcp-config` (prints the MCP registration block for rich clients). Keep it logic-free: it wraps the HTTPS API plus the bundled validator; the server stays authoritative for everything else. Released via CI on tag; the Milestone 0 parity test extends to cover the packaged CLI so its embedded vocabularies can never drift from the schema.

**Done when:** an end-to-end test (scripted as an agent) registers a test org, submits a valid bundle through `kb_submit`, sees it auto-merged, and retrieves its own claim — both via `kb_search` and via `uvx rock-kb search` — with tier `community-unreviewed` after the automated rebuild, with no human action; and a bundle containing a planted secret or another org's path is rejected at every gate.

**Current implementation status (2026-06-12):**

- Repo-side implementation is complete for reviewed intake and agent submission: `orgs/` has a reviewed-org schema/example, `scripts/validate_orgs.py` is wired into CI, the Worker validates registered-org submissions and can open GitHub PRs, and the Python `rock-kb` client can search, fetch, validate, submit, and print MCP config.
- Auto-merge is intentionally disabled (`AUTO_MERGE_INTAKE=false`) until a GitHub App or equivalent server-side path gate can enforce per-org intake boundaries while satisfying branch protection. Public GitHub push rulesets cannot enforce file-path restrictions for this repo type.
- Live completion still requires issuing real org tokens, configuring the Worker with `GITHUB_TOKEN` and org-token hashes, and proving the end-to-end registered-org submit/rebuild/serve loop.

### Milestone 3 — Network Operations

The system stays trustworthy as it grows.

**Deliverables:**

1. **Answer-quality regression gate.** The existing evaluation set (`agent/evaluation-set.jsonl`) runs in CI against the deployed service; promotions or imports that degrade scored answers fail the deploy and surface in review.
2. **Conflict handling at intake.** When a submitted claim conflicts with an official-tier claim (existing `source-conflicts` machinery), it still publishes at `community-unreviewed` but is flagged in the review queue and cross-linked from the conflicting claim, so reviewers see contradictions first.
3. **Staleness for community claims.** Rock-version applicability on community claims feeds `kb status`; claims pinned to old versions get flagged for re-verification rather than silently aging.
4. **Onboarding kit for other churches:** one doc + one example: how to point your agent at the MCP server (rich clients), how terminal agents self-install the consumer CLI (`uvx rock-kb`), how to register your org, and how to configure your agent to submit (an example agent skill/prompt that knows when and how to call `kb_submit` or `rock-kb submit`). This is the adoption surface — write it for a church IT director, not a developer.
5. **Usage telemetry (privacy-light):** Worker-side counts of tool calls, top queries with zero results (the gap-finding signal for what to ingest next), per-org submission stats. No query content retention beyond aggregates.

**Done when:** a second real church has registered, consumed, and contributed without maintainer hand-holding beyond the registration review.

**Current implementation status (2026-06-12):**

- Operational foundations are implemented: hosted-service evaluation (`kb eval-service`) runs against `agent/evaluation-set.jsonl`, service telemetry records aggregate counts without raw query retention, conflict/review artifacts are part of the deployed public surface, and `docs/community-onboarding.md` describes the consumer and contributor path for other churches.
- CI can run the service audit/deploy/eval path, but production eval is skipped until `ROCK_KB_BASE_URL` is configured.
- Live completion still requires a real second church to register, consume, submit, and have that contribution served successfully.

### Milestone 4 — Laptop-Free Private Plane

Independent of Milestones 1–3; may run any time after Milestone 0. The private corpus must not live only on the maintainer's machine, and a transcript, once produced, must never need producing again.

**Deliverables:**

1. **Cloud-canonical private corpus.** The private GitHub corpus repo becomes the canonical home for all text/JSON private artifacts (transcript JSON, sidecars, review queues, drafts, promotions, normalized records, manifests); a private R2 bucket becomes the canonical home for media binaries and prepared clips/frames. The laptop is demoted to a disposable workspace: `kb corpus sync` runs automatically after every ingest/transcription/review batch (post-command hook or wrapper, not maintainer memory), and `kb corpus restore` hydrates a fresh machine from the corpus repo + R2 manifests. Most commands exist from Milestone 0; this milestone makes sync automatic and restore first-class.
2. **Write-once transcripts.** Transcripts are keyed by media content hash; the pipeline skips transcription whenever a transcript for that hash already exists in the corpus (verify whether current behavior already guarantees this; enforce it if not). Re-transcription happens only via an explicit `--force`.
3. **Autonomous ingestion and transcription.** A scheduled job — GitHub Actions cron in the private corpus repo, or a Cloudflare Worker cron — that polls registered media sources (RSS), uploads new media to the private R2 bucket, transcribes via Workers AI Whisper (`@cf/openai/whisper-large-v3-turbo`) or the already-supported OpenAI transcribe path, writes transcript JSON + sidecars to the corpus repo, and queues review candidates. Local tools (`mlx_whisper`, Gemma enrichment) remain optional quality passes, never required steps. The maintainer's machine is needed only for review and promotion decisions.
4. **Disaster-recovery drill.** A runbook plus an actual rehearsal: on a machine that has never run the pipeline, clone the repos, `kb corpus restore`, and pass `kb corpus verify-rebuild` including the scratch public-export check.

**Cost note:** R2 ≈ $0.015/GB-month (100 GB of media ≈ $1.50/month, zero egress); Workers AI Whisper ≈ 47 neurons per audio-minute ≈ $0.03/hour of audio beyond the 10k-neurons/day free allowance; private GitHub repo free.

**Done when:** the maintainer's laptop can be wiped without losing any artifact or requiring any re-transcription, and an episode published while that laptop is off still gets transcribed and queued for review automatically.

**Current implementation status (2026-06-12):**

- Repo-side implementation is complete for the reusable path: `kb corpus autosync` and `kb corpus restore` are first-class commands, `docs/runbooks/private-corpus-cloud-runbook.md` defines the cloud-canonical private corpus flow, and `docs/templates/private-corpus-ingest.workflow.yml` provides the private-repo scheduled ingest template.
- Media transcription now reuses an existing transcript index row marked `transcribed` instead of retranscribing a completed source.
- Live completion still requires creating/configuring the private corpus repo automation, private R2 media bucket, credentials, and a documented restore drill from a fresh machine.

## Success Criteria (whole goal)

- One queryable knowledge base unifies official documentation knowledge, source-code evidence, release knowledge, and community insight — with authority tiers, never blended silently.
- Any MCP-capable agent reads it with one config line; terminal agents self-install the `rock-kb` CLI mid-session; anything else reads plain HTTPS.
- A registered church's agent can contribute end-to-end with no human in the submission loop, and the contribution is served (tier-labeled) within the hour.
- Humans gate authority promotion only — and one dashboard shows them everything awaiting judgment.
- Git remains the source of truth; the hosted service is a disposable projection; everything is rebuildable from the repos plus the private corpus.
- The maintainer's machine is not a single point of failure: the private corpus is cloud-canonical, transcripts are write-once, and new media is ingested and transcribed without the laptop.
- All existing privacy/license audits hold at every stage; no raw protected text, secrets, or private data ever reach the public surface — incoming or outgoing.

## Non-Goals

- Migrating to Wikibase, Onyx, or any external knowledge platform.
- Vector search as the source of truth (optional ranking layer later, at most).
- Auto-promotion of community content into authoritative tiers — review is the product, not overhead.
- Mirroring official documentation full-text (license posture unchanged).
- Multi-tenant private knowledge (each org's private corpus stays their problem; this network carries public-safe distilled knowledge only).
- Real-time chat/forum features — GitHub Discussions on the public repo covers human conversation.
