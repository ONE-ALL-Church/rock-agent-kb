from __future__ import annotations

import dataclasses
from typing import Any, Callable

from ..agent_answer_pack import build_agent_answer_pack
from ..claims import build_approved_claims, validate_claim_file
from ..concepts import build_all_concepts, load_concepts, refresh_long_form_approved_claims
from ..guide_intel import build_guide_intelligence
from ..indexes import build_agent_pack, build_sqlite_index
from ..mobile_selector_audit import build_mobile_selector_audit
from ..model_map import build_model_map
from ..paths import PUBLIC_EXPORT_DIR
from ..publish import build_public_export
from ..recipes import build_recipes


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
    inputs: list[str]
    outputs: list[str]
    run: Callable[[], Any]
    depends_on: list[str] = dataclasses.field(default_factory=list)
    private: bool = False
    manual: bool = False


def _validate_claims() -> dict[str, Any]:
    errors = validate_claim_file()
    if errors:
        raise ValueError("; ".join(errors))
    return {"status": "ok", "errors": 0}


def _refresh_all_guide_claims() -> dict[str, Any]:
    return refresh_long_form_approved_claims()


def _build_all_guide_intel() -> dict[str, Any]:
    results = [build_guide_intelligence(concept.id) for concept in load_concepts()]
    return {"concept_count": len(results), "results": results}


STAGES: list[Stage] = [
    Stage(
        name="claims",
        description="Build public approved claim graph from reviewed promotions.",
        inputs=[
            "data/review/public-media-promotions/*.jsonl",
            "data/review/source-claim-reviews/*.jsonl",
            "data/review/live-claim-verifications*.jsonl",
        ],
        outputs=["claims/approved-claims.jsonl", "claims/claim-export-report.json"],
        run=build_approved_claims,
        private=True,
    ),
    Stage(
        name="claims-validate",
        description="Validate public claim graph schema, traceability, and public safety.",
        inputs=["claims/approved-claims.jsonl"],
        outputs=["claims/approved-claims.jsonl"],
        run=_validate_claims,
        depends_on=["claims"],
    ),
    Stage(
        name="concepts",
        description="Build generated concept guides, concept dependency metadata, and baseline agent entrypoints.",
        inputs=[
            "concepts/registry.yaml",
            "claims/approved-claims.jsonl",
            "agent/source-summaries.jsonl",
            "agent/source-citations.jsonl",
            "data/normalized/*.jsonl",
            "contributions/**/*.jsonl",
            "community-contributions/**/*.jsonl",
            "knowledge/model-map/**/*.jsonl",
            "agent/model-map*.json*",
        ],
        outputs=[
            "agent/concept-dependencies.jsonl",
            "agent/concept-index.jsonl",
            "knowledge/concepts/*/index.md",
        ],
        run=build_all_concepts,
        depends_on=["claims"],
        private=True,
    ),
    Stage(
        name="refresh-claims",
        description="Refresh long-form guide approved-claim and approved-media generated sections.",
        inputs=[
            "claims/approved-claims.jsonl",
            "agent/concept-dependencies.jsonl",
            "knowledge/concepts/*/guide.md",
            "data/normalized/*.media-insights.jsonl",
        ],
        outputs=[
            "knowledge/concepts/*/guide.md",
            "knowledge/concepts/*/approved-claims.md",
            "knowledge/concepts/*/approved-media.md",
        ],
        run=_refresh_all_guide_claims,
        depends_on=["claims", "concepts"],
        private=True,
    ),
    Stage(
        name="guide-intel",
        description="Build section maps, dependencies, task cards, release caveats, and guide quality metadata.",
        inputs=[
            "knowledge/concepts/*/guide.md",
            "knowledge/concepts/*/index.md",
            "agent/source-summaries.jsonl",
            "agent/source-citations.jsonl",
            "agent/concept-dependencies.jsonl",
            "claims/approved-claims.jsonl",
        ],
        outputs=[
            "knowledge/concepts/*/guide-dependencies.json",
            "knowledge/concepts/*/section-source-map.jsonl",
            "knowledge/concepts/*/open-questions.md",
        ],
        run=_build_all_guide_intel,
        depends_on=["concepts"],
        private=True,
    ),
    Stage(
        name="model-map",
        description="Build public model-map resources from authenticated Obsidian block-action stable and pre-alpha model maps.",
        inputs=["data/review/model-map/*.json", "data/review/model-map/*.jsonl"],
        outputs=[
            "knowledge/model-map/index.md",
            "knowledge/model-map/stable-models.jsonl",
            "knowledge/model-map/stable-properties.jsonl",
            "knowledge/model-map/stable-methods.jsonl",
            "knowledge/model-map/latest-models.jsonl",
            "knowledge/model-map/latest-properties.jsonl",
            "knowledge/model-map/latest-methods.jsonl",
            "knowledge/model-map/version-diff.jsonl",
            "agent/model-map-summary.json",
            "agent/model-map-entities.jsonl",
            "agent/model-map-properties.jsonl",
            "agent/model-map-methods.jsonl",
            "agent/model-map-version-diff.jsonl",
            "agent/model-map-digests.jsonl",
        ],
        run=build_model_map,
        manual=True,
    ),
    Stage(
        name="mobile-selector-audit",
        description="Build Rock Mobile selector audit resources from reviewed inventory and normalized sources.",
        inputs=[
            "knowledge/concepts/mobile/mobile-block-selector-xray.jsonl",
            "knowledge/concepts/mobile/resources/*.md",
            "data/normalized/*.jsonl",
        ],
        outputs=[
            "knowledge/concepts/mobile/mobile-block-selector-xray.jsonl",
            "knowledge/concepts/mobile/mobile-block-selector-xray-dependencies.json",
            "knowledge/concepts/mobile/resources/block-selector-image-audit.md",
        ],
        run=build_mobile_selector_audit,
        private=True,
    ),
    Stage(
        name="index",
        description="Build generated SQLite FTS index.",
        inputs=["data/normalized/*.jsonl"],
        outputs=["data/index/kb.sqlite"],
        run=build_sqlite_index,
        depends_on=["concepts"],
        private=True,
    ),
    Stage(
        name="answers",
        description="Build answer pack, live checklists, review queues, and source conflict artifacts.",
        inputs=[
            "claims/approved-claims.jsonl",
            "concepts/registry.yaml",
            "evaluations/real-world.jsonl",
            "knowledge/concepts/*/guide-dependencies.json",
            "data/review/distilled-claim-reviews*.jsonl",
        ],
        outputs=[
            "agent/answer-pack.jsonl",
            "agent/live-inspection-checklists.jsonl",
            "agent/claim-review-queue.jsonl",
            "agent/source-conflicts.jsonl",
            "agent/evaluation-set.jsonl",
            "agent/evaluation-results.jsonl",
            "agent/evaluation-report.json",
        ],
        run=build_agent_answer_pack,
        depends_on=["claims", "concepts"],
        private=True,
    ),
    Stage(
        name="recipes",
        description="Validate community recipe records and build public recipe lookup artifacts.",
        inputs=["recipes/**/*.json", "concepts/registry.yaml", "src/rock_kb/recipes.py", "src/rock_kb/schemas/recipe.py"],
        outputs=["agent/recipes.jsonl", "agent/recipe-summary.json", "knowledge/recipes/*/*.md"],
        run=build_recipes,
    ),
    Stage(
        name="agent-pack",
        description="Build agent navigation, source summaries, model-map/Lava summaries, and manifest files.",
        inputs=[
            "data/normalized/*.jsonl",
            "sources/registry.yaml",
            "concepts/registry.yaml",
            "claims/approved-claims.jsonl",
            "knowledge/concepts/**/*.md",
            "knowledge/model-map/**/*.jsonl",
            "data/review/lava-context-source/**/*",
            "src/rock_kb/lava_contexts.py",
            "agent/recipes.jsonl",
        ],
        outputs=[
            "agent/llms.txt",
            "agent/source-summaries.jsonl",
            "agent/source-citations.jsonl",
            "agent/rock-kb-manifest.json",
            "agent/lava-contexts.jsonl",
            "agent/lava-context-summary.json",
            "knowledge/concepts/lava/lava-contexts.jsonl",
            "knowledge/concepts/lava/lava-context-directory.md",
            "knowledge/concepts/lava/lava-context-dependencies.json",
        ],
        run=build_agent_pack,
        depends_on=["answers", "guide-intel", "recipes"],
        private=True,
    ),
    Stage(
        name="export",
        description="Build audited public export payload.",
        inputs=[
            "agent/**/*",
            "claims/approved-claims.jsonl",
            "knowledge/**/*.md",
            "knowledge/**/*.json",
            "knowledge/**/*.jsonl",
            "README.md",
        ],
        outputs=["data/public-export/public-export-manifest.json"],
        run=lambda: build_public_export(PUBLIC_EXPORT_DIR),
        depends_on=["agent-pack", "claims-validate"],
    ),
]


def stage_by_name(stages: list[Stage] | None = None) -> dict[str, Stage]:
    return {stage.name: stage for stage in stages or STAGES}


def topological_stages(stages: list[Stage] | None = None) -> list[Stage]:
    remaining = dict(stage_by_name(stages))
    ordered: list[Stage] = []
    seen: set[str] = set()
    while remaining:
        ready = [stage for stage in remaining.values() if all(dep in seen for dep in stage.depends_on)]
        if not ready:
            unresolved = ", ".join(sorted(remaining))
            raise ValueError(f"Cycle or unknown dependency in pipeline stages: {unresolved}")
        for stage in ready:
            ordered.append(stage)
            seen.add(stage.name)
            remaining.pop(stage.name)
    return ordered
