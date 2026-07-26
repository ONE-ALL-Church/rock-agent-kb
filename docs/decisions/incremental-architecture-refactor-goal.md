# Architecture Refactor Goal (Clean-Break, Test-Guarded)

> **Status: retired 2026-07-26.** This checklist is preserved as historical
> design context. Its architecture, pipeline, contribution validation, hosted
> service, and public-audit outcomes are implemented; unchecked boxes no longer
> represent active work. Use `docs/decisions/project-goal.md`, current readiness
> audits, source freshness, evaluation results, and maintainer review queues to
> select new work.

> **For agentic workers (Codex):** Execute this plan phase by phase, task by task, in order. Steps use checkbox (`- [ ]`) syntax for tracking. Every task ends with the full test suite passing and a commit. Never leave the repo in a state where `uv run --extra dev pytest` fails at a commit boundary.

> **Amendment (2026-06-11, single-public-repo decision):** `docs/decisions/agent-knowledge-network-goal.md` (Milestone 0.5) amends this plan. When executing: (1) in Phase 5 Task 5.4, create `.github/workflows/validate-contributions.yml`, `scripts/validate_bundle.py`, and `community-contributions/CONTRIBUTING.md` at those real paths — the `templates/public-repo/` indirection is retired; (2) do not extend `publish push` or `contributions import-public` beyond renaming — both retire in Milestone 0.5; (3) `data/public-export/` is legacy: keep its audit logic, which Milestone 0.5 repurposes to audit the public tree and deploy payload directly. Read that document's Milestone 0 amendments before starting Phase 5.

**Goal:** Rebuild the Rock RMS General Knowledge Base's *surface* — CLI grammar, module boundaries, workflow encoding, validation, and serving — into the architecture you would design from scratch, while keeping the proven pipeline logic, data formats, tests, and privacy audits. End state: a ~50-command grouped CLI (down from 77 flat commands), focused modules, a staleness engine where `kb status` answers "what needs doing?" and `kb build` does it, write-time schemas where privacy is a type, a hardened community contribution lifecycle, and an MCP server (`kb serve`).

**Context that shapes this plan:** This project is **not in production**. There are no external consumers of the CLI. The only callers are the maintainer, the runbooks in `docs/`, the CI workflow `.github/workflows/refresh.yml`, and agent sessions — all of which this plan updates in lockstep. Therefore: **no backward-compatibility aliases, no deprecation shims, no frozen command names.** Commands are renamed, merged, or deleted outright, and every reference is updated in the same commit. The safety net is the test suite and the audit gates, not name stability.

**Why not from scratch:** The ~19,600 lines under `src/rock_kb/` embed tested, hard-won logic — source-specific crawlers, transcription tool integration, leak-detection patterns, claim building, model-map scraping — and 24 test modules that encode expected behavior. The data design (registry-driven sources, JSONL records, claims as the durable unit, audited public export) is sound. The problems are at the surface. A clean-break refactor reaches the from-scratch end state without re-deriving the hard parts or regressing the privacy gates. Do not rewrite working pipeline internals; restructure and re-expose them.

**Tech Stack:** Python ≥3.11 (bumped in Phase 0), Typer, uv/hatchling, pytest, PyYAML, httpx. New dependencies: `pydantic>=2` (Phase 4), `mcp` (Phase 6, optional extra).

---

## Hard Invariants (apply to every task)

1. **Test gate at every commit.** `uv run --extra dev pytest` passes before every commit. When a task renames or deletes a command, the same commit updates every test, runbook, README mention, and CI reference. Tests asserting on removed behavior are updated to assert on the replacement, never simply deleted.
2. **Audit gate after any task touching generated artifacts, validation, or publish code.** Run `uv run kb audit public-export && uv run kb audit licenses && uv run kb audit source-policy && uv run kb audit readiness` (post-Phase-3: the `kb audit *` forms). `audit-readiness` may report `incomplete` (expected while private ingestion is partial) but must not report new `fail` checks relative to the Phase 0 baseline.
3. **Coherence at every commit.** No commit may leave README, runbooks, or `.github/workflows/refresh.yml` referencing a command that no longer exists.
4. **Privacy boundary is untouchable.** Never commit anything from `data/media/`, `data/normalized/`, `data/review/`, `data/raw-manifests/`, or `data/index/`. Never weaken a leak check, license check, or public-export audit. Validation logic may be *moved* (Phase 4) but the moved code must reject everything the old code rejected — proven by tests.
5. **Deliberate regeneration only.** Do not regenerate files under `agent/`, `knowledge/`, or `claims/` unless a task requires it. `data/public-export/` is legacy ignored scratch output in Milestone 0.5. When rebuilding, pin `ROCK_KB_GENERATED_AT` to a fixed ISO timestamp so `generated_at` metadata does not churn.
6. **One task, one commit** (or a small number of coherent commits per task). Imperative commit messages consistent with repo history, e.g. `Split media module into package`, `Re-cut CLI to grouped grammar`.
7. **Behavior preservation for pipeline logic.** Renaming, regrouping, and re-validating are in scope; changing what any pipeline stage computes or emits is not. Artifact formats stay byte-compatible (verify with pinned-timestamp rebuild diffs where a task touches a writer).

---

## Phase 0 — Baseline and Toolchain

### Task 0.1: Record the baseline

**Files:**
- Historical: `docs/log/refactor-baseline.md` was created during the private build phase and is now retired to the private corpus.

- [ ] **Step 1:** Run and record a private baseline note under headings `## Test Baseline`, `## Audit Baseline`, `## Command Inventory`:

```bash
uv run --extra dev pytest 2>&1 | tail -5
uv run kb audit readiness 2>&1 | tail -20
uv run kb --help
```

This file is the reference for "no new failures" for the rest of the plan.

- [ ] **Step 2: Commit.** `Record refactor baseline`

### Task 0.2: Bump Python floor

**Files:**
- Modify: `pyproject.toml` (`requires-python = ">=3.11"`)

- [ ] **Step 1:** Set `requires-python = ">=3.11"` (the MCP SDK in Phase 6 needs ≥3.10; 3.11 is the sensible floor). Run `uv sync --extra dev && uv run --extra dev pytest`. If any dependency fails to resolve on 3.11, fall back to `>=3.10` and note it in the private baseline record.
- [ ] **Step 2: Commit.** `Raise Python floor to 3.11`

---

## Phase 1 — Split the God Modules

Pure structural refactor: no command names change in this phase, no logic changes. `cli.py` stays monolithic until Phase 3 (so the CLI is restructured exactly once, after the pipeline engine exists).

### Task 1.1: Split `media.py` (2,686 lines) into a `media/` package

**Files:**
- Create: `src/rock_kb/media/__init__.py`, `discover.py`, `transcribe.py`, `queue.py`, `sidecars.py`, `review.py`, `promote.py`, `understanding.py`, `report.py`, `_shared.py`
- Delete: `src/rock_kb/media.py`
- Tests: existing `tests/test_media.py` must pass unchanged.

- [ ] **Step 1: Map the split before moving anything.** Read `src/rock_kb/media.py` top to bottom and assign every function/constant to exactly one target file by responsibility: media URL discovery → `discover.py`; transcription tools and batch runs → `transcribe.py`; priority queue → `queue.py`; sidecar/index writing → `sidecars.py`; public candidates, review status, draft rewrites → `review.py`; promotion of reviewed candidates → `promote.py`; Gemma/understanding benchmark → `understanding.py`; report/doctor → `report.py`; constants, path helpers, JSONL helpers used by 2+ submodules → `_shared.py`.
- [ ] **Step 2: Move mechanically, then re-export.** `__init__.py` re-exports every public name `media.py` previously exposed:

```python
from .discover import *      # noqa: F401,F403
from .transcribe import *    # noqa: F401,F403
from .queue import *         # noqa: F401,F403
from .sidecars import *      # noqa: F401,F403
from .review import *        # noqa: F401,F403
from .promote import *       # noqa: F401,F403
from .understanding import * # noqa: F401,F403
from .report import *        # noqa: F401,F403
```

Verify external usage with `grep -rn "from rock_kb.media import\|from rock_kb import media\|rock_kb\.media\." src/ tests/`.

- [ ] **Step 3: Verify.** `uv run --extra dev pytest` full pass; `uv run kb media report` runs.
- [ ] **Step 4: Commit.** `Split media module into focused package`

### Task 1.2: Split `concepts.py` (2,220 lines) into a `concepts/` package

**Files:**
- Create: `src/rock_kb/concepts/__init__.py`, `registry.py` (registry load/validate/list/stale), `build.py` (concept artifact builds), `synthesize.py` (LLM synthesis + hydration), `_shared.py`
- Delete: `src/rock_kb/concepts.py`

Same mechanical procedure as Task 1.1: map every symbol to one file, move, wildcard re-export from `__init__.py`, grep for external imports (`tests/test_cli_prompt.py` imports `get_concept` from `rock_kb.concepts` — must keep working), full pytest. Commit: `Split concepts module into focused package`

### Task 1.3: Split `guide_intel.py` (1,748 lines) into a `guide_intel/` package

**Files:**
- Create: `src/rock_kb/guide_intel/__init__.py` plus submodules split by responsibility (suggested: `sections.py`, `citations.py`, `open_questions.py`, `dependencies.py`, `_shared.py` — adjust to the actual seams found while reading the file)
- Delete: `src/rock_kb/guide_intel.py`

Same procedure. Commit: `Split guide-intel module into focused package`

---

## Phase 2 — Pipeline Engine: `kb status` and `kb build`

The rebuild order currently lives in `docs/runbooks/source-rebuild-orchestration-runbook.md` and human memory. This phase encodes it as a declarative stage graph with hash-based staleness. In Phase 3, the engine *replaces* the standalone `build-*` commands entirely.

### Task 2.1: Stage graph and build-state store

**Files:**
- Create: `src/rock_kb/pipeline/__init__.py`, `src/rock_kb/pipeline/stages.py`, `src/rock_kb/pipeline/state.py`
- Test: `tests/test_pipeline.py`

- [ ] **Step 1: Define the model in `stages.py`:**

```python
from __future__ import annotations

import dataclasses
from typing import Callable, List


@dataclasses.dataclass(frozen=True)
class Stage:
    """One rebuildable step in the KB pipeline.

    inputs/outputs are repo-relative glob patterns. A stage is stale when
    the combined hash of files matching its inputs differs from the hash
    recorded at its last successful run, or when any upstream stage is
    stale, or when any output file is missing.
    """
    name: str
    description: str
    inputs: List[str]
    outputs: List[str]
    run: Callable[[], None]
    depends_on: List[str] = dataclasses.field(default_factory=list)
    private: bool = False   # touches only private data
    manual: bool = False    # requires human review; never auto-run
```

- [ ] **Step 2: Register the rebuild graph.** Define `STAGES: list[Stage]` covering the deterministic rebuild chain. Derive exact membership, ordering, inputs, and outputs from `docs/runbooks/source-rebuild-orchestration-runbook.md` and the existing command implementations — the runbook is authoritative for order; the code is authoritative for inputs/outputs. The expected automatic stages (verify, don't trust this list blindly):

```text
claims          (inputs: data/review/** promotions, contributions/**)        ← build-claims
claims-validate (depends_on: claims)                                         ← validate-claims
concepts        (inputs: concepts/registry.yaml, claims/, data/normalized/**) ← build-concepts / build-concept
refresh-claims  (depends_on: claims, concepts)                               ← refresh-guide-claims
guide-intel     (depends_on: concepts)                                       ← build-guide-intel
model-map       (inputs: model-map scrape inputs; manual=True if scrape-gated) ← build-model-map
mobile-selector-audit (inputs: knowledge/concepts/mobile/*.jsonl)            ← build-mobile-selector-audit
index           (depends_on: concepts)                                       ← build-index
answers         (depends_on: claims, concepts)                               ← build-answer-pack
agent-pack      (depends_on: answers, guide-intel)                           ← build-agent-pack
export          (depends_on: agent-pack, claims-validate)                    ← public-export
```

Each `run` callable wraps the same internal function the corresponding CLI command calls today (import the function; never shell out). Stages that take flags in normal operation get the all-sources/all-concepts defaults the runbook prescribes.

Transcription, review, promotion, synthesis, source refresh (network ingest), and publish-push are **not** stages or are `manual=True`; they surface in `kb status` as gates, never auto-run.

- [ ] **Step 3: Implement `state.py`.** `load_state()` / `save_state()` over `data/index/build-state.json` (already a gitignored directory). State maps stage name → `{"input_hash": str, "completed_at": iso}`. Hash = SHA-256 over sorted (path, file-sha256) pairs of all files matching the stage's input globs. Implement `stage_status(stage, state) -> "fresh" | "stale" | "missing-outputs" | "manual"`.
- [ ] **Step 4: Tests** in `tests/test_pipeline.py` with `tmp_path` fixtures and a two-stage toy graph: fresh after run; stale after an input changes; downstream stale when upstream stale; missing outputs detected; hash stable across runs with unchanged files. Never test against real repo data.
- [ ] **Step 5: Verify and commit.** `Add pipeline stage graph with hash-based staleness`

### Task 2.2: `kb status`

**Files:**
- Modify: `src/rock_kb/cli.py` (register `status` top-level; the CLI re-cut comes in Phase 3)
- Create: `src/rock_kb/pipeline/status.py`
- Test: `tests/test_pipeline.py` (extend)

- [ ] **Step 1: Implement.** Output, in order:
  1. **Pipeline table**: one row per stage — name, status, and for stale stages the first 3 changed input paths.
  2. **Review queues** (reuse existing report functions; do not reimplement): pending media review counts (the `media-review-status` internals), claim review queue size (`agent/claim-review-queue.jsonl` row count), per-concept guide refresh needs (the `guide-refresh-plan` internals), concept staleness (the `concepts stale` internals), mobile selector audit status (the `mobile-selector-audit-status` internals).
  3. **Suggested next commands**: for each stale automatic stage in topological order, `uv run kb build --stage <name>`; for manual gates, the runbook command.

  `kb status` absorbs `guide-refresh-plan`, `rebuild-plan`, `concepts stale`, and `mobile-selector-audit-status` — their logic is called from here, and their standalone commands are deleted in Phase 3.
- [ ] **Step 2: Test** with the toy graph via `CliRunner` (monkeypatch the stage registry). Verify by hand: `uv run kb status` on the real repo completes in under ~30 seconds.
- [ ] **Step 3: Commit.** `Add kb status workflow overview`

### Task 2.3: `kb build`

**Files:**
- Modify: `src/rock_kb/cli.py`
- Create: `src/rock_kb/pipeline/build.py`
- Test: `tests/test_pipeline.py` (extend)

- [ ] **Step 1: Implement `kb build [--stage NAME] [--dry-run] [--force]`.** Default: run all stale automatic stages in topological order, updating state after each success. `--stage`: one stage plus stale upstreams (unless `--force`). `--dry-run`: print the plan. Manual stages never auto-run; if one blocks downstream, print the gate and stop. Respect `ROCK_KB_GENERATED_AT` exactly as the wrapped functions do.
- [ ] **Step 2: Tests** on the toy graph: dry-run ordering; state updated; manual gate blocks; `--force` re-runs a fresh stage.
- [ ] **Step 3: Real-repo smoke test:** `ROCK_KB_GENERATED_AT=2026-06-11T00:00:00Z uv run kb build --dry-run` prints a plan without executing. If `kb status` shows genuinely stale stages, run the real build, then the four audits and `git diff --stat` — all diffs must be explainable.
- [ ] **Step 4: Commit.** `Add kb build incremental pipeline runner`

---

## Phase 3 — Clean-Break CLI Re-Cut, README, and Docs Triage

One decisive change: the flat 77-command surface becomes the final grammar below. **No aliases, no deprecation period.** Old names die in this phase; every runbook, README mention, CI reference, and test updates in the same task.

### Task 3.1: Re-cut `cli.py` into a `cli/` package with the final grammar

**Files:**
- Create: `src/rock_kb/cli/__init__.py` plus one module per group: `sources_cmds.py`, `extract_cmds.py`, `media_cmds.py`, `claims_cmds.py`, `corpus_cmds.py`, `private_cmds.py`, `contribution_cmds.py`, `concepts_cmds.py`, `modelmap_cmds.py`, `audit_cmds.py`, `publish_cmds.py`, `report_cmds.py`, `tools_cmds.py`, `workflow_cmds.py` (status/build from Phase 2), `_shared.py`
- Delete: `src/rock_kb/cli.py`
- Modify: `tests/test_cli_prompt.py` (helpers `candidate_ids_from_file`, `comprehensive_required_sections` move to `cli/_shared.py`; update imports)
- Create: `tests/test_cli_surface.py`
- Modify: `.github/workflows/refresh.yml`, every runbook under `docs/` that names a command

**The final command surface.** This is the complete disposition of all 77 current commands. Three dispositions: **rename** (same behavior, new name), **absorb** (functionality now reached through `kb build`/`kb status`; standalone command deleted), **merge** (two commands become one).

Top-level workflow verbs: `kb status`, `kb build` (from Phase 2), and later `kb serve` (Phase 6).

| Current command | Disposition → new form |
|---|---|
| `sources list` / `sources validate` | unchanged |
| `discover` | rename → `sources discover` |
| `discover-community` | rename → `sources discover-community` |
| `fetch` | rename → `sources fetch` |
| `normalize` | rename → `sources normalize` |
| `summarize` | rename → `sources summarize` |
| `refresh` | rename → `sources refresh` |
| `probe-endpoints` | rename → `sources probe-endpoints` |
| `source-scan` | rename → `sources scan` |
| `extract-markdown` | rename → `extract markdown` |
| `extractor-doctor` | rename → `extract doctor` |
| `media-discover` | rename → `media discover` |
| `media-transcribe` | rename → `media transcribe` |
| `media-batch` | rename → `media batch` |
| `media-doctor` | rename → `media doctor` |
| `media-report` | rename → `media report` |
| `media-queue` | rename → `media queue` |
| `media-normalize` | rename → `media normalize` |
| `media-sidecars` | rename → `media sidecars` |
| `media-prune-dry-runs` | rename → `media prune-dry-runs` |
| `media-public-candidates` | rename → `media candidates` |
| `media-review-status` | rename → `media review-status` |
| `media-public-draft-rewrites` | rename → `media draft-rewrites` |
| `media-public-promote` | rename → `media promote` |
| `media-understanding-benchmark` | rename → `media understand-benchmark` |
| `media-understanding-prepare` | rename → `media understand-prepare` |
| `media-understanding-run-ollama` | rename → `media understand-run` |
| `build-claims` | **absorb** → `kb build --stage claims` |
| `validate-claims` | rename → `claims validate` |
| `live-verification-plan` | rename → `claims live-plan` |
| `private-corpus-init` | rename → `corpus init` |
| `private-corpus-validate` | rename → `corpus validate` |
| `private-corpus-report` | rename → `corpus report` |
| `private-corpus-sync` | rename → `corpus sync` |
| `private-corpus-media-manifest` | rename → `corpus media-manifest` |
| `private-corpus-audit` | rename → `corpus audit` |
| `private-corpus-verify-rebuild` | rename → `corpus verify-rebuild` |
| `private-scan` | rename → `private scan` |
| `private-ingest` | rename → `private ingest` |
| `private-review-report` | rename → `private review-report` |
| `distill-private` | rename → `private distill` |
| `private-stale` | rename → `private stale` |
| `private-impact` | rename → `private impact` |
| `contribution-new` | rename → `contributions new` |
| `contribution-check` | rename → `contributions check` |
| `contribution-validate` | rename → `contributions validate` |
| `contribution-promote` | rename → `contributions promote` |
| `contribution-import-public` | retired by single-public-repo Milestone 0.5 |
| `concepts list` | unchanged |
| `concepts stale` | **absorb** → `kb status` |
| `build-concept` + `build-concepts` | **merge + absorb** → `kb build --stage concepts` (stage builds all; per-concept debugging via the stage function's existing `--concept` path if cheap, else not exposed) |
| `synthesize-concept` | rename → `concepts synthesize` |
| `hydrate-concept` | rename → `concepts hydrate` |
| `build-guide-intel` | **absorb** → `kb build --stage guide-intel` |
| `refresh-guide-claims` | **absorb** → `kb build --stage refresh-claims` |
| `guide-refresh-plan` | **absorb** → `kb status` |
| `build-model-map` | rename → `modelmap build` |
| `stamp-model-map-scrape-version` | rename → `modelmap stamp` |
| `diff-model-map-scrapes` | rename → `modelmap diff` |
| `build-index` | **absorb** → `kb build --stage index` |
| `build-answer-pack` | **absorb** → `kb build --stage answers` |
| `build-agent-pack` | **absorb** → `kb build --stage agent-pack` |
| `build-mobile-selector-audit` | **absorb** → `kb build --stage mobile-selector-audit` |
| `mobile-selector-audit-status` | **absorb** → `kb status` |
| `audit-guide` | rename → `audit guide` |
| `audit-licenses` | rename → `audit licenses` |
| `audit-source-policy` | rename → `audit source-policy` |
| `audit-public-export` | rename → `audit public-export` |
| `audit-readiness` | rename → `audit readiness` |
| *(new)* | `audit all` — runs licenses, source-policy, public-export, readiness in sequence, fails on first failure |
| `public-export` | rename → `publish export` (also reachable as `kb build --stage export`) |
| `publish-public` | retired by single-public-repo Milestone 0.5 |
| `report-refresh` | rename → `report refresh` |
| `refresh-dashboard` | rename → `report dashboard` |
| `rebuild-plan` | **absorb** → `kb status` / `kb build --dry-run` |
| `repo-pack` | rename → `tools repo-pack` |

- [x] **Step 1: Build the package.** Move command functions into their group modules (cut/paste, no logic edits beyond renames and deletions per the table). Absorbed commands: delete the Typer command function; keep the underlying implementation function (it is now called by a pipeline stage or by `kb status`). Shared CLI helpers go to `cli/_shared.py`, re-exported from `cli/__init__.py`.
- [x] **Step 2: Assemble the root app:**

```python
import typer

from . import (
    audit_cmds, claims_cmds, concepts_cmds, contribution_cmds, corpus_cmds,
    extract_cmds, media_cmds, modelmap_cmds, private_cmds, publish_cmds,
    report_cmds, sources_cmds, tools_cmds, workflow_cmds,
)
from ._shared import candidate_ids_from_file, comprehensive_required_sections

app = typer.Typer(help="Rock RMS knowledge base tooling.")
workflow_cmds.register(app)   # kb status, kb build (top-level)
app.add_typer(sources_cmds.app, name="sources")
app.add_typer(extract_cmds.app, name="extract")
app.add_typer(media_cmds.app, name="media")
app.add_typer(claims_cmds.app, name="claims")
app.add_typer(corpus_cmds.app, name="corpus")
app.add_typer(private_cmds.app, name="private")
app.add_typer(contribution_cmds.app, name="contributions")
app.add_typer(concepts_cmds.app, name="concepts")
app.add_typer(modelmap_cmds.app, name="modelmap")
app.add_typer(audit_cmds.app, name="audit")
app.add_typer(publish_cmds.app, name="publish")
app.add_typer(report_cmds.app, name="report")
app.add_typer(tools_cmds.app, name="tools")
```

- [x] **Step 3: Surface test.** `tests/test_cli_surface.py`: every command in the final grammar resolves with `--help` (use `CliRunner`, enumerate the full new surface as a literal list); a sample of five dead names (`build-claims`, `media-public-promote`, `guide-refresh-plan`, `private-corpus-sync`, `rebuild-plan`) exits non-zero.
- [x] **Step 4: Update every caller in the same commit.**
  - `grep -o 'kb [a-z-]*' .github/workflows/refresh.yml | sort -u` — rewrite each invocation to the new grammar (e.g. `kb refresh` → `kb sources refresh`, `kb report refresh` → `kb report refresh`, any `build-*` → `kb build --stage ...`).
  - `grep -rn 'uv run kb ' README.md docs/ --include='*.md' -l` — update every command mention in every doc.
  - Update any test that invokes commands by old names.
- [x] **Step 5: Verify.** Full pytest; `uv run kb --help` fits on one screen; `uv run kb audit all` works; spot-run `uv run kb media report` and `uv run kb status`.
- [x] **Step 6: Commit.** `Re-cut CLI to grouped grammar without compatibility aliases`

### Task 3.2: Rewrite `README.md` as a one-page map

**Files:**
- Modify: `README.md`
- Create: `docs/runbooks/cli-reference.md` (full command reference in the new grammar, including the disposition table above for anyone holding old muscle memory)
- Create: `docs/runbooks/pipeline-overview.md` (the prose currently in README lines ~148–175: sidecar rules, claim layers, private corpus, answer pack, media queue, Gemma enrichment, source summaries, readiness audit — moved and updated to new command names, not rewritten)

- [x] **Step 1: Write the new README** with exactly these sections and nothing more:
  - **Identity** (3 sentences): what the project is, the two-tier public/private posture, the conservative default.
  - **Quick Start** (≤6 commands): `uv sync --extra dev`, `uv run kb status`, `uv run kb build --dry-run`, `uv run kb audit all`, `uv run --extra dev pytest`.
  - **Layout**: the existing directory table, one line per directory.
  - **Command groups**: one line each for `status`/`build` and the 13 groups, pointing to `docs/runbooks/cli-reference.md`.
  - **Where to go next**: `docs/decisions/project-goal.md` (decisions), the runbooks directory, `agent/rock-kb-manifest.json` as the agent entrypoint.
  - One short paragraph on reproducibility (`ROCK_KB_GENERATED_AT`, `SOURCE_DATE_EPOCH`).
- [x] **Step 2: Move, don't delete** — every removed README paragraph lands in a runbook. No information loss.
- [x] **Step 3:** Every relative link resolves. Commit: `Rewrite README as one-page map with runbook pointers`

### Task 3.3: Triage `docs/` into runbooks, decisions, and log

**Files:**
- Create: `docs/decisions/` (`docs/runbooks/` exists from Task 3.2). Historical `docs/log/` point-in-time notes were later retired to the private corpus by the single-public-repo cleanup.
- Create: `docs/README.md` (index)

- [x] **Step 1: Classify and `git mv` every file in `docs/`:**
  - **`docs/runbooks/`** (how to operate, durable): `model-map-rebuild-runbook.md`, `contributor-reviewer-workflow.md`, `public-publish-runbook.md`, `source-rebuild-orchestration-runbook.md`, `local-transcription.md`, plus the two from Task 3.2.
  - **`docs/decisions/`** (why it is this way, durable): `project-goal.md`, `public-private-knowledge-system-goal.md`, `claim-graph-refactor-goal.md`, `claim-graph-research-notes.md`, `claim-tier-policy.md`, `data-organization-decision.md`, `current-tooling-research.md`, `public-export-policy.md`, `topic-split-rules.md`, `private-and-org-data-integration-plan.md`, `org-data-implementation-roadmap.md`, this file.
  - **Private corpus logs** (dated point-in-time records, not public repo content): `thin-concept-coverage-review-2026-06-09.md`, `high-value-guide-spot-check-2026-06-09.md`, `high-value-guide-spot-check-2026-06-11.md`, `answer-pack-queue-triage-2026-06-10.md`, `media-transcription-next-batch-2026-06-09.md`, `source-conflict-review-2026-06-10.md`, `v1-release-checkpoint.md`, `topic-expansion-review.md`, `topic-gap-report.md`, `agent-handoff.md`, `implementation-plan.md`, `open-questions-live-verification.md`, `retrieval-qa-media-priority.md`, `refactor-baseline.md`.
  - `public-repo-readme.md`: `grep -rn "public-repo-readme" src/` first — if code references it, leave it in place and note that in `docs/README.md`; otherwise move to `docs/runbooks/`.
- [x] **Step 2: Fix every inbound link.** `grep -rn "docs/" README.md docs/ src/ knowledge/ agent/ --include="*.md" --include="*.py" -l` and update paths — check `src/rock_kb/publish.py` and `src/rock_kb/readiness.py` especially (readiness checks may assert on doc paths).
- [x] **Step 3:** Write `docs/README.md` — three sections, one line per file. Full pytest + `uv run kb audit readiness` (no new failures). Commit: `Triage docs into runbooks, decisions, and log`
- [x] **Step 4: Update the runbooks to the engine.** `docs/runbooks/source-rebuild-orchestration-runbook.md` and `contributor-reviewer-workflow.md` currently prescribe long command sequences; replace the mechanical sequences with `kb status` / `kb build`, keep the manual-gate documentation (review, rewrite, promotion steps stay human). Commit: `Encode rebuild sequences as status/build in runbooks`

---

## Phase 4 — Schema Layer (write-time validation, privacy as a type)

### Task 4.1: Pydantic base and claim model

**Files:**
- Modify: `pyproject.toml` (add `pydantic>=2.0` to `[project.dependencies]`)
- Create: `src/rock_kb/schemas/__init__.py`, `src/rock_kb/schemas/base.py`, `src/rock_kb/schemas/claim.py`
- Test: `tests/test_schemas.py`

- [x] **Step 1:** Add the dependency; `uv sync --extra dev`.
- [x] **Step 2: `base.py`:**

```python
from typing import Any, Dict

from pydantic import BaseModel


def Private(**kwargs):
    """Marker for fields that must never appear in public artifacts."""
    from pydantic import Field
    extra = kwargs.pop("json_schema_extra", {}) or {}
    extra["visibility"] = "private"
    return Field(json_schema_extra=extra, **kwargs)


class KBRecord(BaseModel):
    """Base for all KB JSONL record types."""

    model_config = {"extra": "forbid"}

    def public_dump(self) -> Dict[str, Any]:
        """Serialize excluding every field marked Private."""
        private = {
            name
            for name, field in type(self).model_fields.items()
            if (field.json_schema_extra or {}).get("visibility") == "private"
        }
        return self.model_dump(exclude=private, exclude_none=True)
```

- [x] **Step 3: `claim.py`.** Model the approved-claim row **exactly as currently emitted** into `claims/approved-claims.jsonl` — derive fields from `src/rock_kb/claims.py` and `docs/decisions/claim-tier-policy.md`, not memory. `Literal` types for `authority_tier`, `claim_tier`, `review_status` using the exact vocabularies. Private-only fields (private corpus pointers, evidence paths) use `Private()`.
- [x] **Step 4: Tests:** every row of the real `claims/approved-claims.jsonl` round-trips with zero errors; `public_dump()` excludes a `Private()` field; unknown fields rejected.
- [x] **Step 5: Commit.** `Add pydantic schema layer with privacy-marked claim model`

### Task 4.2: Shared leak checker, and claims validation through the schema

**Files:**
- Create: `src/rock_kb/private_leakage.py`
- Modify: `src/rock_kb/claims.py`
- Test: `tests/test_private_leakage.py` (new), `tests/test_claims.py` (extend)

- [x] **Step 1: Extract, don't invent.** `claims validate` already blocks direct media URLs, transcript fields, secrets, and private-only data. Move those predicates into `private_leakage.py` with one entry point — `find_leaks(row: dict) -> list[str]` (human-readable violations) — adding path-prefix checks for `data/review/`, `data/media/`, `data/normalized/` and tokenized/HLS URL patterns if not already present. `claims validate` now calls the shared checker; everything the old inline code rejected must still be rejected (port the existing tests, add cases).
- [x] **Step 2: Validate through the model.** The claims build path constructs `Claim` models and serializes via `public_dump()` with today's key order (verify byte-stability with a pinned-timestamp rebuild diff). `claims validate` = schema validation + `find_leaks` + the existing traceability checks.
- [x] **Step 3: Verify:** full pytest; `uv run kb claims validate` passes on the real graph; `uv run kb audit public-export` unchanged.
- [x] **Step 4: Commit.** `Validate claims through schema layer with shared leak checker`

---

## Phase 5 — Community Contribution Module Hardening

**Depends on Phase 4** (uses `KBRecord`, `Private()`, and `private_leakage.py`). Independent of Phase 6.

**Current state (verify, don't assume):** the contribution system already exists — `src/rock_kb/contributions.py` (~783 lines), `src/rock_kb/contribution_sources.py`, `src/rock_kb/private_scan.py`, the `rock-kb-org-contribution-v1` JSONL bundle schema (examples in `contributions/example-org/bundle.example.jsonl` and `community-contributions/example-org/bundle.example.jsonl`), intake folders (`contributions/`, `community-contributions/`, `source-suggestions/`), the CLI verbs (`contributions new/check/validate/promote`), and the prose workflow in `docs/runbooks/contributor-reviewer-workflow.md`. This phase does **not** redesign that flow. It makes the rules *enforceable* instead of *documented*: typed bundle schema, an explicit review-status state machine, the shared leak checker applied to bundles, and self-serve validation for outside contributors. Example bundles must remain valid throughout.

**The private→public contribution boundary (the design contract for every task in this phase):**

| Stage | Artifact | Location | Visibility |
|---|---|---|---|
| 1. Scan | raw scan rows from a private repo (`kb private scan`) | `data/review/private-scan-*.jsonl` | **Private** — gitignored, may contain raw private text |
| 2. Distill | concept-routed draft candidates (`kb private distill`) | `data/review/private-distill/*.jsonl` | **Private** — still private wording |
| 3. Rewrite | reviewer-authored public-safe rewrites | `data/review/rewrites/*.jsonl` | **Private** — input to promotion |
| 4. Promote | attested bundle rows (`kb contributions promote --reviewed --redaction-attestation --license-attestation`) | `contributions/<org-id>/bundle.jsonl` | **Public** (build repo) — first public artifact in the chain |
| 5. Outside-org intake | bundles submitted by other orgs via PR to the public repo | `community-contributions/<org-id>/bundle.jsonl`, `source-suggestions/<org-id>/` | **Public, untrusted** — candidate status, never auto-trusted |
| 6. Validate | accepted public bundles validated in the single public repo before maintainer promotion | `community-contributions/<org-id>/`, `source-suggestions/<org-id>/` | **Public, untrusted** — candidate material until reviewed |
| 7. Build | contribution rows become claims (`kb build --stage claims`) → guides → agent pack → public surface | `claims/`, `knowledge/`, `agent/`, `concepts/`, `sources/` | **Public** — community authority tier preserved, never relabeled as official |

The rule the whole phase enforces: **nothing crosses from row 3 to row 4 without an approved review status plus both attestations, and no public row may carry private paths, raw transcript text, secrets, tokenized/HLS URLs, or non-generalized org-internal details.**

### Task 5.1: Write the canonical contribution-module runbook

**Files:**
- Create: `docs/runbooks/contribution-module.md`
- Modify: `docs/runbooks/contributor-reviewer-workflow.md` (add a pointer; remove nothing)

- [x] **Step 1:** Write `docs/runbooks/contribution-module.md`: the boundary table above (corrected against actual code paths if any differ); the lifecycle vocabulary from Task 5.3; one worked end-to-end example using the real command sequence (private scan → distill → rewrite → promote → `kb build` → export); and a "what contributors may touch" section — in the public repo only `community-contributions/<org-id>/` and `source-suggestions/<org-id>/` are contributor edit targets.
- [x] **Step 2:** Verify every path and command named in the doc exists. Commit: `Add canonical contribution-module runbook`

### Task 5.2: Typed bundle schema

**Files:**
- Create: `src/rock_kb/schemas/contribution.py`
- Modify: `src/rock_kb/schemas/__init__.py` (export `ContributionRow`)
- Modify: `src/rock_kb/contributions.py` (`contributions validate` validates rows through the model in addition to existing checks)
- Test: `tests/test_schemas.py` (extend), `tests/fixtures/` (valid/invalid bundle fixtures)

- [x] **Step 1: Derive the model from reality.** Read the validation logic in `contributions.py` and the example bundles. Observed field set for `schema: rock-kb-org-contribution-v1`: `schema`, `contribution_id`, `org_id`, `org_display_name`, `contribution_type`, `concept_ids`, `distilled_summary`, `source_urls`, `source_record_ids`, `confidence`, `review_status`, `needs_live_verification`, `license_attestation`, `redaction_attestation`. The code is authoritative. `Literal` vocabularies for `contribution_type` (observed: `task_card`, `troubleshooting_pattern`, `release_caveat`, `entity_note`, `guide_section`, `source_link`, `open_question` — extract the complete list from code), `review_status`, and `confidence`.
- [x] **Step 2: Round-trip test:** both example bundles parse with zero errors; unknown field rejected; bad `contribution_type` rejected with a message naming allowed values.
- [x] **Step 3:** Wire into `contributions validate` additively — schema failures report file, row index, pydantic message. Must still pass on the repo as-is.
- [x] **Step 4:** Full pytest. Commit: `Add typed contribution bundle schema and wire into validation`

### Task 5.3: Review-status state machine and promotion gate

**Files:**
- Modify: `src/rock_kb/schemas/contribution.py` (transitions table)
- Modify: `src/rock_kb/contributions.py` (promotion enforces the gate)
- Test: `tests/test_contributions_lifecycle.py` (new)

- [x] **Step 1: Extract the real status vocabulary** from `contributions.py` (examples show `draft_private`; find the full set including the statuses the promote path writes).
- [x] **Step 2: Encode transitions** as data next to the model:

```python
# Allowed review_status transitions. Promotion to a public bundle is only
# legal from a status marked promotable, and only with reviewed +
# redaction_attestation + license_attestation all true.
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    # fill from the actual vocabulary found in Step 1
}
PROMOTABLE_STATUSES: frozenset[str] = frozenset({...})  # from Step 1
```

- [x] **Step 3: Enforce at the only door.** In `contributions promote`, before any row is written to a public bundle: status in `PROMOTABLE_STATUSES` (or the call performs a legal transition into one), and all three flags present. On failure, exit non-zero naming the row, its status, and which gate failed. Where existing flag checks already cover part of this, route them through the new table — one source of truth.
- [x] **Step 4: Tests:** promoting `draft_private` without attestations fails naming the gate; legal promotion succeeds and the emitted row validates as `ContributionRow`; illegal transition rejected. Also apply `find_leaks` (Phase 4) to every promoted row — a row with a `data/review/...` path or transcript field is a hard failure.
- [x] **Step 5:** Full pytest. Commit: `Enforce contribution review-status state machine at promotion`

### Task 5.4: Self-serve validation for outside contributors

Outside orgs submit via PR to the **public repo**, which contains only the export — not this package. They need validation that runs there without installing the build repo.

**Files:**
- Create: `scripts/validate_bundle.py` (stdlib-only, single file)
- Create: `.github/workflows/validate-contributions.yml`
- Create: `community-contributions/CONTRIBUTING.md`
- Modify: `docs/runbooks/contribution-module.md` (install instructions)
- Modify: `src/rock_kb/contributions.py` — only if Step 4 finds import-time validation missing
- Test: `tests/test_validate_bundle_script.py` (new)

- [x] **Step 1: Standalone validator.** `validate_bundle.py` uses only the standard library (json, sys, pathlib, re, urllib.parse). Validates every `community-contributions/*/bundle*.jsonl` row: parseable JSON per line, `schema == "rock-kb-org-contribution-v1"`, required fields, vocabulary membership, and the same leak patterns as `private_leakage.py`. Exit non-zero with per-row messages. Embed vocabularies as constants with a comment naming `src/rock_kb/schemas/contribution.py` as the source of truth.
- [x] **Step 2: Parity test.** `tests/test_validate_bundle_script.py` runs the script (subprocess, `sys.executable`) against the same valid/invalid fixtures as Tasks 5.2–5.3 and asserts it accepts and rejects exactly what `ContributionRow` + `find_leaks` do. This keeps the stdlib copy honest — vocabulary drift fails this test.
- [x] **Step 3: Workflow + contributor docs.** `validate-contributions.yml` triggers on PRs touching `community-contributions/**` or `source-suggestions/**`, runs `python scripts/validate_bundle.py`. `CONTRIBUTING.md`: what a bundle is, field reference, submissions are candidates subject to maintainer review and stay community-tier after acceptance, contributors must hold rights to what they submit. One page, plain language.
- [x] **Step 4: Close the import loop.** The former split-repo `contributions import-public` path validated bundles before import; single-public-repo Milestone 0.5 retired the command so public intake is validated in place before maintainer promotion.
- [x] **Step 5: Document installation.** The validator, workflow, and contribution guide live at their real single-repo paths. The runbook documents how contributors and CI use them directly; no `templates/public-repo/` install step remains.
- [x] **Step 6:** Full pytest. Commit: `Add self-serve bundle validation for public-repo contributors`

---

## Phase 6 — `kb serve`: MCP Server over the Knowledge Base

Independent of Phases 2–5 (needs only Phase 0's Python bump); may be executed earlier if retrieval value is the priority. Read-only MCP stdio server so agents query the KB without knowing the repo layout.

### Task 6.1: Retrieval functions

**Files:**
- Create: `src/rock_kb/serve/__init__.py`, `src/rock_kb/serve/retrieval.py`
- Test: `tests/test_serve.py`

- [x] **Step 1: Inspect the existing index.** Read `src/rock_kb/indexes.py` for the SQLite/FTS database path under `data/index/` and its table schema. Reuse it; do not invent a second index.
- [x] **Step 2: Pure retrieval functions** (no MCP imports here):
  - `search(query: str, limit: int = 10) -> list[dict]` — FTS query; hits return title, path/URL, snippet, concept, citation fields available in the index.
  - `get_manifest() -> dict` — parsed `agent/rock-kb-manifest.json`.
  - `list_concepts() -> list[dict]` — from `agent/concept-index.jsonl`.
  - `get_concept(concept_id: str) -> dict` — quickstart + answers + task cards + release caveats for one concept, from `knowledge/concepts/<id>/` and `agent/`.
  - `get_claims(concept_id: str, tier: str | None = None) -> list[dict]` — filtered rows from `claims/approved-claims.jsonl`.
  - Every function works from **public artifacts only** (never `data/media/`, `data/review/`, `data/normalized/`). If the FTS index contains private rows, filter by the index's public/private marker; if none exists, restrict `search` to rows whose source path is under `knowledge/`, `agent/`, or `claims/`.
- [x] **Step 3: Tests** with `tmp_path` fixtures: tiny FTS DB + fixture JSONL; search returns the seeded row; concept assembly works; claims filter by tier; a private-pathed row never surfaces.
- [x] **Step 4: Commit.** `Add public-only retrieval functions for KB serving`

### Task 6.2: MCP server and `kb serve` command

**Files:**
- Modify: `pyproject.toml` (optional extra: `serve = ["mcp>=1.0"]`)
- Create: `src/rock_kb/serve/server.py`
- Modify: `src/rock_kb/cli/workflow_cmds.py` — or `src/rock_kb/cli.py` if this phase is executed before the Phase 3 re-cut (top-level `serve`; import `mcp` lazily so the base install works without the extra)
- Test: extend `tests/test_serve.py`

- [x] **Step 1: Implement** with the official `mcp` Python SDK (`FastMCP`), stdio transport, five read-only tools mapping 1:1 onto retrieval functions: `kb_search`, `kb_manifest`, `kb_list_concepts`, `kb_get_concept`, `kb_get_claims`. Tool descriptions tell an agent when to use each (`kb_search`: "Full-text search across the Rock RMS knowledge base. Start here for any Rock question; results cite sources.").
- [x] **Step 2: `kb serve`** runs the stdio server; without the extra installed, exit with: `kb serve requires the serve extra: uv sync --extra serve`.
- [x] **Step 3: Tests:** five tools registered with correct names (SDK in-memory client if available; else assert on `build_server()` registrations).
- [x] **Step 4: Manual smoke test** (note the result in the commit message): `uv sync --extra serve && timeout 5 uv run kb serve` starts cleanly. Document client registration in `docs/runbooks/agent-serving.md`:

```json
{ "mcpServers": { "rock-kb": { "command": "uv", "args": ["run", "--directory", "/path/to/Rock General Knowledge Base", "kb", "serve"] } } }
```

- [x] **Step 5: Commit.** `Add kb serve MCP server over public KB artifacts`

---

## Final Verification (after all phases)

- [x] `uv run --extra dev pytest` — full pass, zero skips introduced by this work. Verified 2026-06-12: 336 passed.
- [x] `uv run kb audit all` — no new failures vs the private baseline record. Verified 2026-06-12: exits 0; readiness remains `incomplete` with 12 pass / 2 warn / 0 fail for stale concept and guide refresh warnings.
- [x] `uv run kb --help` fits on one screen; every command in `tests/test_cli_surface.py` resolves; the five sampled dead names fail. Verified 2026-06-12: help is 34 lines and full pytest passes `tests/test_cli_surface.py`.
- [x] `uv run kb status` gives an actionable overview; `ROCK_KB_GENERATED_AT=<pin> uv run kb build --dry-run` prints a coherent plan. Verified 2026-06-12 with `ROCK_KB_GENERATED_AT=2026-06-11T00:00:00Z`.
- [x] `grep -rn 'uv run kb ' README.md docs/ .github/ --include='*.md' --include='*.yml'` — every invocation uses the new grammar. Verified 2026-06-12: no removed flat-command grammar hits.
- [x] `uv run kb contributions validate` passes, and `scripts/validate_bundle.py` agrees with the schema validator (parity test green). Verified 2026-06-12: `uv run kb contributions validate`, `python3 scripts/validate_bundle.py`, direct `scripts/validate_bundle.py`, and `tests/test_validate_bundle_script.py` pass.
- [x] README quickstart is ≤6 commands; every relative link resolves. Verified 2026-06-12: 5 commands, no README relative-link errors.
- [x] `git log --oneline` shows one coherent commit per task. Verified 2026-06-12 against the recent refactor series.

## Out of Scope (do not do)

- Rewriting pipeline internals (crawlers, transcription, normalization, claim building, model-map scraping) — restructure and re-expose only.
- Changing any generated artifact format, claim vocabulary, source policy, or audit rule.
- Deploying the MCP server to Cloudflare Workers (future goal; keep `retrieval.py` free of gratuitous local-FS assumptions, but do not build it).
- Adding vector search, embeddings, or hosted services.
- Refactoring modules this plan doesn't name (`model_map.py`, `agent_answer_pack.py`, `community.py`, etc. stay as-is).
- Touching `data/` private directories or committing anything from them.
