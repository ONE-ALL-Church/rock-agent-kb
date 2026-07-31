from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .extract import sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REPO_ROOT
from .schemas import (
    EvidenceLink,
    GenerationActivity,
    KnowledgeRelationship,
    KnowledgeUnit,
    ReviewedCrossSourceArtifact,
    ReviewedCrossSourceManifest,
    SourceSnapshot,
    SourceUnit,
)


REVIEWED_CROSS_SOURCE_RELATIVE_DIR = Path("canonical/cross-source/v1")
REVIEW_DECISIONS_NAME = "review-decisions.jsonl"
PROMOTED_FILES = (
    REVIEW_DECISIONS_NAME,
    "source-snapshots.jsonl",
    "source-units.jsonl",
    "generation-activities.jsonl",
    "knowledge-units.jsonl",
    "evidence-links.jsonl",
    "relationships.jsonl",
    "evaluation-set.jsonl",
)


def promote_reviewed_cross_source(
    *,
    input_path: Path,
    destination: Path,
) -> dict[str, Any]:
    """Compile reviewed multi-source decisions into the canonical envelope."""

    reviewed = [
        ReviewedCrossSourceArtifact.model_validate(row)
        for row in read_jsonl(input_path)
    ]
    if not reviewed:
        raise ValueError("reviewed cross-source input cannot be empty")

    snapshots: dict[str, SourceSnapshot] = {}
    units: dict[str, SourceUnit] = {}
    activities: dict[str, GenerationActivity] = {}
    knowledge: dict[str, KnowledgeUnit] = {}
    evidence_links: dict[str, EvidenceLink] = {}
    relationships: dict[str, KnowledgeRelationship] = {}
    evaluations: dict[str, dict[str, Any]] = {}

    for artifact in reviewed:
        if artifact.knowledge_unit_id in knowledge:
            raise ValueError(
                "duplicate reviewed cross-source knowledge unit: "
                f"{artifact.knowledge_unit_id}"
            )
        source_work_ids: set[str] = set()
        source_unit_ids: list[str] = []
        source_snapshot_ids: set[str] = set()
        authority_tiers: set[str] = set()

        for evidence in artifact.source_evidence:
            snapshot = evidence.source_snapshot
            unit = evidence.source_unit
            _store_unique(
                snapshots,
                snapshot.source_snapshot_id,
                snapshot,
                "source snapshot",
            )
            _store_unique(
                units,
                unit.source_unit_id,
                unit,
                "source unit",
            )
            source_snapshot_ids.add(snapshot.source_snapshot_id)
            source_unit_ids.append(unit.source_unit_id)
            authority_tiers.add(evidence.authority_tier)
            if snapshot.source_work_id:
                source_work_ids.add(snapshot.source_work_id)

        source_input_hash = sha256_text(
            json.dumps(
                [
                    {
                        "source_snapshot_id": row.source_snapshot.source_snapshot_id,
                        "source_unit_id": row.source_unit.source_unit_id,
                        "normalized_content_hash": (
                            row.source_unit.normalized_content_hash
                        ),
                        "relation": row.relation,
                    }
                    for row in artifact.source_evidence
                ],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        activity_id = "generation:" + sha256_text(
            f"{artifact.knowledge_unit_id}:{source_input_hash}:"
            f"{artifact.generation_prompt_id}:"
            f"{artifact.generation_prompt_version}:"
            f"{artifact.generation_model}"
        )[:24]
        activity = GenerationActivity(
            schema="rock-kb-generation-activity-v1",
            generation_activity_id=activity_id,
            activity_type="maintainer_review",
            model=artifact.generation_model,
            prompt_id=artifact.generation_prompt_id,
            prompt_version=artifact.generation_prompt_version,
            source_snapshot_ids=sorted(source_snapshot_ids),
            source_unit_ids=sorted(source_unit_ids),
            source_input_hash=source_input_hash,
            created_at=artifact.reviewed_at,
            review_method="public_evidence_cross_source_synthesis",
            parameters={
                "reviewer": artifact.reviewer,
                "public_retrieval_changed": False,
                "source_count": len(source_snapshot_ids),
            },
        )
        activities[activity_id] = activity

        payload = {
            "schema": "rock-kb-cross-source-artifact-payload-v1",
            "temporal_status": artifact.temporal_status,
            "review": {
                "reviewer": artifact.reviewer,
                "reviewed_at": artifact.reviewed_at,
                "rationale": artifact.review_rationale,
            },
            **artifact.payload,
        }
        content_hash = sha256_text(
            json.dumps(
                {
                    "knowledge_type": artifact.knowledge_type,
                    "title": artifact.title,
                    "retrieval_text": artifact.retrieval_text,
                    "concept_ids": artifact.concept_ids,
                    "topic_ids": artifact.topic_ids,
                    "rock_versions": artifact.rock_versions,
                    "version_scope_status": artifact.version_scope_status,
                    "source_unit_ids": sorted(source_unit_ids),
                    "payload": payload,
                },
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        knowledge_unit = KnowledgeUnit(
            schema="rock-kb-knowledge-unit-v1",
            knowledge_unit_id=artifact.knowledge_unit_id,
            knowledge_type=artifact.knowledge_type,
            title=artifact.title,
            retrieval_text=artifact.retrieval_text,
            concept_facets=sorted(artifact.concept_ids),
            topic_facets=sorted(artifact.topic_ids),
            authority_tiers=sorted(authority_tiers),
            claim_tier=artifact.claim_tier,
            review_state=artifact.review_state,
            rock_versions=artifact.rock_versions,
            version_scope_status=artifact.version_scope_status,
            source_unit_ids=sorted(source_unit_ids),
            source_work_ids=sorted(source_work_ids),
            generation_activity_ids=[activity_id],
            reviewed_at=artifact.reviewed_at,
            payload_schema="rock-kb-cross-source-artifact-payload-v1",
            payload=payload,
            content_hash=content_hash,
        )
        knowledge[artifact.knowledge_unit_id] = knowledge_unit

        for evidence in artifact.source_evidence:
            unit_id = evidence.source_unit.source_unit_id
            evidence_id = "evidence:" + sha256_text(
                f"{artifact.knowledge_unit_id}:{unit_id}:{evidence.relation}"
            )[:24]
            evidence_links[evidence_id] = EvidenceLink(
                schema="rock-kb-evidence-link-v1",
                evidence_link_id=evidence_id,
                knowledge_unit_id=artifact.knowledge_unit_id,
                source_unit_id=unit_id,
                relation=evidence.relation,
                evidence_summary=evidence.evidence_summary,
                authority_tier=evidence.authority_tier,
                confidence=evidence.confidence,
                independence_group=evidence.independence_group,
                needs_review=evidence.needs_review,
            )

        for relationship in artifact.relationships:
            relationship_id = "relationship:" + sha256_text(
                f"{artifact.knowledge_unit_id}:{relationship.relation}:"
                f"{relationship.target_id}"
            )[:24]
            relationships[relationship_id] = KnowledgeRelationship(
                schema="rock-kb-knowledge-relationship-v1",
                relationship_id=relationship_id,
                from_id=artifact.knowledge_unit_id,
                to_id=relationship.target_id,
                relation=relationship.relation,
                decision="accept",
                confidence=relationship.confidence,
                rationale=relationship.rationale,
                evidence_source_unit_ids=(
                    relationship.evidence_source_unit_ids
                ),
                reviewed_at=artifact.reviewed_at,
            )

        for evaluation in artifact.evaluations:
            evaluation_id = f"cross-source:{evaluation.evaluation_id}"
            if evaluation_id in evaluations:
                raise ValueError(
                    f"duplicate cross-source evaluation: {evaluation_id}"
                )
            evaluations[evaluation_id] = {
                "schema": "rock-kb-service-evaluation-case-v1",
                "id": evaluation_id,
                "question": evaluation.question,
                "query_type": evaluation.query_type,
                "concept_id": evaluation.concept_id,
                "source": "reviewed_cross_source",
                "evaluation_mode": "retrieval",
                "expected_result_ids": [artifact.knowledge_unit_id],
                "expected_result_kinds": [artifact.knowledge_type],
                "required_authority_tiers": (
                    evaluation.required_authority_tiers
                ),
                "required_terms": evaluation.required_terms,
                "max_allowed_rank": evaluation.max_rank,
            }

    destination.mkdir(parents=True, exist_ok=True)
    if input_path.resolve() != (destination / REVIEW_DECISIONS_NAME).resolve():
        write_jsonl(
            destination / REVIEW_DECISIONS_NAME,
            [
                row.model_dump(
                    by_alias=True,
                    exclude_none=True,
                )
                for row in reviewed
            ],
        )
    write_jsonl(
        destination / "source-snapshots.jsonl",
        [
            row.public_dump()
            for row in sorted(
                snapshots.values(),
                key=lambda item: item.source_snapshot_id,
            )
        ],
    )
    write_jsonl(
        destination / "source-units.jsonl",
        [
            row.public_dump()
            for row in sorted(
                units.values(),
                key=lambda item: item.source_unit_id,
            )
        ],
    )
    write_jsonl(
        destination / "generation-activities.jsonl",
        [
            row.public_dump()
            for row in sorted(
                activities.values(),
                key=lambda item: item.generation_activity_id,
            )
        ],
    )
    write_jsonl(
        destination / "knowledge-units.jsonl",
        [
            row.public_dump()
            for row in sorted(
                knowledge.values(),
                key=lambda item: item.knowledge_unit_id,
            )
        ],
    )
    write_jsonl(
        destination / "evidence-links.jsonl",
        [
            row.public_dump()
            for row in sorted(
                evidence_links.values(),
                key=lambda item: item.evidence_link_id,
            )
        ],
    )
    write_jsonl(
        destination / "relationships.jsonl",
        [
            row.public_dump()
            for row in sorted(
                relationships.values(),
                key=lambda item: item.relationship_id,
            )
        ],
    )
    write_jsonl(
        destination / "evaluation-set.jsonl",
        [evaluations[key] for key in sorted(evaluations)],
    )
    manifest = ReviewedCrossSourceManifest(
        schema="rock-kb-reviewed-cross-source-manifest-v1",
        artifact_count=len(knowledge),
        source_snapshot_count=len(snapshots),
        source_unit_count=len(units),
        generation_activity_count=len(activities),
        evidence_link_count=len(evidence_links),
        relationship_count=len(relationships),
        evaluation_case_count=len(evaluations),
        file_hashes={
            name: sha256_file(destination / name)
            for name in PROMOTED_FILES
        },
        notes=[
            "The bundle remains canonical shadow input; default public retrieval remains legacy and any canary access requires a separate opt-in release.",
            "Mutable issue reports are separated from official release and immutable source-code evidence.",
            "Reported affected versions and officially fixed versions retain distinct evidence relations.",
        ],
    )
    (destination / "manifest.json").write_text(
        json.dumps(
            manifest.model_dump(by_alias=True, exclude_none=True),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-reviewed-cross-source-promotion-v1",
        "status": "ok",
        "destination": str(destination),
        **manifest.model_dump(by_alias=True, exclude_none=True),
    }


def load_reviewed_cross_source(
    repo_root: Path = REPO_ROOT,
) -> dict[str, list[Any]]:
    directory = repo_root / REVIEWED_CROSS_SOURCE_RELATIVE_DIR
    if not directory.exists():
        return {
            "source_snapshots": [],
            "source_units": [],
            "generation_activities": [],
            "knowledge_units": [],
            "evidence_links": [],
            "relationships": [],
        }
    manifest = ReviewedCrossSourceManifest.model_validate(
        json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    )
    for name, expected_hash in manifest.file_hashes.items():
        path = directory / name
        if not path.exists() or sha256_file(path) != expected_hash:
            raise ValueError(
                f"reviewed cross-source manifest hash mismatch: {name}"
            )
    return {
        "source_snapshots": [
            SourceSnapshot.model_validate(row)
            for row in read_jsonl(directory / "source-snapshots.jsonl")
        ],
        "source_units": [
            SourceUnit.model_validate(row)
            for row in read_jsonl(directory / "source-units.jsonl")
        ],
        "generation_activities": [
            GenerationActivity.model_validate(row)
            for row in read_jsonl(directory / "generation-activities.jsonl")
        ],
        "knowledge_units": [
            KnowledgeUnit.model_validate(row)
            for row in read_jsonl(directory / "knowledge-units.jsonl")
        ],
        "evidence_links": [
            EvidenceLink.model_validate(row)
            for row in read_jsonl(directory / "evidence-links.jsonl")
        ],
        "relationships": [
            KnowledgeRelationship.model_validate(row)
            for row in read_jsonl(directory / "relationships.jsonl")
        ],
    }


def reviewed_cross_source_evaluation_rows(
    repo_root: Path = REPO_ROOT,
) -> list[dict[str, Any]]:
    return list(
        read_jsonl(
            repo_root
            / REVIEWED_CROSS_SOURCE_RELATIVE_DIR
            / "evaluation-set.jsonl"
        )
    )


def _store_unique(
    target: dict[str, Any],
    key: str,
    value: Any,
    label: str,
) -> None:
    existing = target.get(key)
    if existing is not None and existing != value:
        raise ValueError(f"conflicting reviewed cross-source {label}: {key}")
    target[key] = value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
