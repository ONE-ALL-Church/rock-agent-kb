from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from itertools import combinations
from pathlib import Path
from typing import Any

from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .media.identity import infer_source_work_id
from .paths import REPO_ROOT, REVIEW_DIR
from .reviewed_cross_source import load_reviewed_cross_source
from .schemas import (
    CanonicalIdentityBaselineManifest,
    CanonicalKnowledgeBundle,
    Claim,
    EvidenceLink,
    GenerationActivity,
    KnowledgeIdentity,
    KnowledgeIdentityMigration,
    KnowledgeRelationship,
    KnowledgeUnit,
    PublicResultAlias,
    SourceLocator,
    SourceSnapshot,
    SourceUnit,
)
from .service_projection import build_search_rows
from .source_family_contracts import (
    source_family_contract,
    source_family_contract_summary,
)
from .source_native import (
    canonical_records_for_source_native_artifacts,
    load_source_native_pilot,
)
from .source_native_migration import (
    LegacyMigrationIndex,
    SourceNativeArtifactMigrationIndex,
)
from .source_native_verification import verification_resolutions_by_artifact

SHADOW_DIR = REVIEW_DIR / "canonical-knowledge-pilot"
CANONICAL_IDENTITY_BASELINE_RELATIVE_DIR = Path("canonical/identity/v1")
CANONICAL_IDENTITY_REGISTRY_NAME = "identity-registry.jsonl"
CANONICAL_RETIRED_IDENTITY_MIGRATIONS_NAME = "retired-identity-migrations.jsonl"
CANONICAL_PUBLIC_ALIASES_NAME = "public-result-aliases.jsonl"
CANONICAL_IDENTITY_MANIFEST_NAME = "manifest.json"
SUPPORTED_SEARCH_KINDS = {
    "claim",
    "community_contribution",
    "recipe",
    "source_summary",
    "model_map",
    "lava_context",
    "rock_issue",
    "rock_idea",
}
VOLATILE_SOURCE_SUMMARY_FIELDS = {"retrieved_at"}
CLAIM_TIER_RANK = {
    "routing_context_only": 0,
    "source_backed": 1,
    "answer_pack_approved": 2,
    "live_verified": 3,
}
REVIEW_STATE_RANK = {
    "generated_needs_reviewer_approval": 0,
    "community_unreviewed": 0,
    "routing_context_only": 0,
    "redaction_reviewed": 1,
    "community_reviewed": 2,
    "reviewer_approved": 3,
    "approved_for_answer_pack": 3,
    "approved_for_public_distillation": 3,
    "public_reviewed": 3,
}
PRIVATE_VALUE_PATTERNS = (
    re.compile(r"(?:^|[\"'\s])/(?:Users|home|private|var/folders)/"),
    re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{12,}\b"),
)
FORBIDDEN_PAYLOAD_KEYS = {
    "private_corpus_pointer",
    "raw_transcript",
    "raw_transcript_text",
    "transcript",
    "secret",
    "access_token",
    "api_key",
}


def build_canonical_knowledge_bundle(
    *,
    search_rows: Iterable[dict[str, Any]] | None = None,
    distilled_claims: Iterable[dict[str, Any]] | None = None,
    identity_registry: Iterable[dict[str, Any]] | None = None,
    identity_migrations: Iterable[dict[str, Any]] | None = None,
    previous_knowledge_units: Iterable[dict[str, Any]] | None = None,
    include_source_native_pilot: bool | None = None,
    include_legacy_migrations: bool | None = None,
    include_reviewed_cross_source: bool | None = None,
    repo_root: Path = REPO_ROOT,
) -> tuple[CanonicalKnowledgeBundle, dict[str, Any]]:
    """Project current public artifacts into the shared architecture without publishing it."""

    use_source_native_pilot = (
        search_rows is None and distilled_claims is None
        if include_source_native_pilot is None
        else include_source_native_pilot
    )
    use_reviewed_cross_source = (
        search_rows is None and distilled_claims is None
        if include_reviewed_cross_source is None
        else include_reviewed_cross_source
    )
    use_legacy_migrations = (
        use_source_native_pilot
        if include_legacy_migrations is None
        else include_legacy_migrations
    )
    all_search_rows = list(search_rows) if search_rows is not None else build_search_rows()
    supported_rows = [row for row in all_search_rows if str(row.get("kind") or "") in SUPPORTED_SEARCH_KINDS]
    distilled_rows = (
        list(distilled_claims)
        if distilled_claims is not None
        else list(read_jsonl(repo_root / "agent" / "distilled-claims.jsonl"))
    )
    resolver = _IdentityResolver(
        identity_registry=identity_registry or [],
        identity_migrations=identity_migrations or [],
        previous_knowledge_units=previous_knowledge_units or [],
    )
    builder = _ProjectionBuilder(resolver)

    source_native = (
        load_source_native_pilot(repo_root)
        if use_source_native_pilot
        else {
            "source_snapshots": [],
            "source_units": [],
            "generation_activities": [],
            "reviewed_artifacts": [],
            "relationships": [],
            "verification_queue": [],
            "verification_resolutions": [],
            "legacy_migrations": [],
            "artifact_migrations": [],
        }
    )
    legacy_migration_index = LegacyMigrationIndex(
        source_native.get("legacy_migrations") or []
        if use_legacy_migrations
        else []
    )
    artifact_migration_index = SourceNativeArtifactMigrationIndex(
        source_native.get("artifact_migrations") or []
        if use_legacy_migrations
        else []
    )

    claim_rows = [row for row in supported_rows if row.get("kind") == "claim"]
    for group in canonical_claim_groups(claim_rows, distilled_rows):
        migration = legacy_migration_index.match(
            result_ids=claim_group_aliases(
                group["claim_rows"],
                group["distilled_rows"],
            ),
            knowledge_type="claim",
            ingestion_mode="legacy_reviewed_claim_projection",
            content_hash=claim_group_content_hash(group),
            source_record_ids=claim_group_source_record_ids(group),
        )
        if migration is not None:
            continue
        builder.add_claim_group(group)

    for row in supported_rows:
        if row.get("kind") == "claim":
            continue
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        kind = str(row.get("kind") or "other")
        contract = source_family_contract(kind, payload)
        migration = legacy_migration_index.match(
            result_ids=[str(row.get("id") or ""), *(row.get("legacy_ids") or [])],
            knowledge_type=kind,
            ingestion_mode=contract.ingestion_mode,
            content_hash=search_row_payload_content_hash(kind, payload),
            source_record_ids=search_row_source_record_ids(row),
        )
        if migration is not None:
            continue
        builder.add_search_row(row)

    legacy_migration_index.assert_all_applied()

    reviewed_cross_source = (
        load_reviewed_cross_source(repo_root)
        if use_reviewed_cross_source
        else {
            "source_snapshots": [],
            "source_units": [],
            "generation_activities": [],
            "knowledge_units": [],
            "evidence_links": [],
            "relationships": [],
        }
    )
    builder.add_reviewed_cross_source(reviewed_cross_source)
    builder.add_source_native_pilot(
        source_native,
        legacy_migration_index=legacy_migration_index,
        artifact_migration_index=artifact_migration_index,
    )
    builder.add_mirror_relationships()
    bundle = builder.bundle()
    summary = projection_summary(
        bundle,
        all_search_rows=all_search_rows,
        supported_rows=supported_rows,
        claim_rows=claim_rows,
        distilled_rows=distilled_rows,
        source_native_artifact_count=len(source_native["reviewed_artifacts"]),
        legacy_migration_count=len(source_native.get("legacy_migrations") or []),
        artifact_migration_count=len(
            source_native.get("artifact_migrations") or []
        ),
        reviewed_cross_source_artifact_count=len(
            reviewed_cross_source["knowledge_units"]
        ),
    )
    return bundle, summary


def write_canonical_knowledge_shadow(
    destination: Path = SHADOW_DIR,
    *,
    search_rows: Iterable[dict[str, Any]] | None = None,
    distilled_claims: Iterable[dict[str, Any]] | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    previous_knowledge_units = list(read_jsonl(destination / "knowledge-units.jsonl"))
    local_identity_registry = list(
        read_jsonl(destination / CANONICAL_IDENTITY_REGISTRY_NAME)
    )
    use_repository_projection = search_rows is None and distilled_claims is None
    persistent_identity_registry = (
        list(
            read_jsonl(
                repo_root
                / CANONICAL_IDENTITY_BASELINE_RELATIVE_DIR
                / CANONICAL_IDENTITY_REGISTRY_NAME
            )
        )
        if use_repository_projection
        else []
    )
    reviewed_alias_transfers = (
        source_native_reviewed_alias_transfers(
            load_source_native_pilot(repo_root)
        )
        if use_repository_projection
        else {}
    )
    identity_registry = merge_identity_registry_rows(
        persistent_identity_registry,
        local_identity_registry,
        reviewed_alias_transfers=reviewed_alias_transfers,
    )
    identity_migrations = list(read_jsonl(destination / "identity-migrations.jsonl"))
    retired_identity_migrations = list(
        read_jsonl(
            destination / CANONICAL_RETIRED_IDENTITY_MIGRATIONS_NAME
        )
    )
    bundle, summary = build_canonical_knowledge_bundle(
        search_rows=search_rows,
        distilled_claims=distilled_claims,
        identity_registry=identity_registry,
        identity_migrations=identity_migrations,
        previous_knowledge_units=previous_knowledge_units,
        repo_root=repo_root,
    )
    active_migration_ids = {
        row.migration_id for row in bundle.identity_migrations
    }
    retired_by_id: dict[str, KnowledgeIdentityMigration] = {}
    for raw in [*retired_identity_migrations, *identity_migrations]:
        migration = KnowledgeIdentityMigration.model_validate(raw)
        if migration.migration_id in active_migration_ids:
            continue
        existing = retired_by_id.get(migration.migration_id)
        if existing is not None and existing != migration:
            raise ValueError(
                "retired identity migration history conflicts for "
                f"{migration.migration_id}"
            )
        retired_by_id[migration.migration_id] = migration
    retired_rows = sorted(
        retired_by_id.values(),
        key=lambda row: row.migration_id,
    )
    summary["output"]["retired_identity_migrations"] = len(retired_rows)
    destination.mkdir(parents=True, exist_ok=True)
    write_jsonl(
        destination / "source-snapshots.jsonl",
        [row.public_dump() for row in bundle.source_snapshots],
    )
    write_jsonl(
        destination / "source-units.jsonl",
        [row.public_dump() for row in bundle.source_units],
    )
    write_jsonl(
        destination / "generation-activities.jsonl",
        [row.public_dump() for row in bundle.generation_activities],
    )
    write_jsonl(
        destination / "knowledge-units.jsonl",
        [row.public_dump() for row in bundle.knowledge_units],
    )
    write_jsonl(
        destination / "identity-registry.jsonl",
        [row.public_dump() for row in bundle.identities],
    )
    write_jsonl(
        destination / "identity-migrations.jsonl",
        [row.public_dump() for row in bundle.identity_migrations],
    )
    write_jsonl(
        destination / CANONICAL_RETIRED_IDENTITY_MIGRATIONS_NAME,
        [row.public_dump() for row in retired_rows],
    )
    write_jsonl(
        destination / "evidence-links.jsonl",
        [row.public_dump() for row in bundle.evidence_links],
    )
    write_jsonl(
        destination / "relationships.jsonl",
        [row.public_dump() for row in bundle.relationships],
    )
    (destination / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {**summary, "destination": str(destination)}


def write_canonical_identity_baseline(
    destination: Path | None = None,
    *,
    shadow_destination: Path = SHADOW_DIR,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Persist public-safe canonical identities without publishing pilot migrations."""

    write_canonical_knowledge_shadow(
        shadow_destination,
        repo_root=repo_root,
    )
    identities = [
        KnowledgeIdentity.model_validate(row)
        for row in read_jsonl(
            shadow_destination / CANONICAL_IDENTITY_REGISTRY_NAME
        )
    ]
    knowledge_units = [
        KnowledgeUnit.model_validate(row)
        for row in read_jsonl(shadow_destination / "knowledge-units.jsonl")
    ]
    source_native = load_source_native_pilot(repo_root)
    historical_public_result_ids = sorted(
        row.prior_artifact_id
        for row in source_native.get("artifact_migrations") or []
    )
    public_rows = build_search_rows()
    registry, aliases, metadata = build_public_identity_baseline(
        identities=identities,
        knowledge_units=knowledge_units,
        public_search_rows=public_rows,
        historical_public_result_ids=historical_public_result_ids,
    )
    baseline_dir = (
        destination
        if destination is not None
        else repo_root / CANONICAL_IDENTITY_BASELINE_RELATIVE_DIR
    )
    baseline_dir.mkdir(parents=True, exist_ok=True)
    registry_path = baseline_dir / CANONICAL_IDENTITY_REGISTRY_NAME
    aliases_path = baseline_dir / CANONICAL_PUBLIC_ALIASES_NAME
    manifest_path = baseline_dir / CANONICAL_IDENTITY_MANIFEST_NAME
    write_jsonl(
        registry_path,
        [row.public_dump() for row in registry],
    )
    write_jsonl(
        aliases_path,
        [row.public_dump() for row in aliases],
    )
    manifest = CanonicalIdentityBaselineManifest(
        schema="rock-kb-canonical-identity-baseline-manifest-v1",
        identity_registry_path=repository_relative_or_name(
            registry_path,
            repo_root,
        ),
        public_result_aliases_path=repository_relative_or_name(
            aliases_path,
            repo_root,
        ),
        identity_count=len(registry),
        public_alias_count=len(aliases),
        existing_result_id_alias_count=metadata[
            "existing_result_id_alias_count"
        ],
        existing_legacy_id_alias_count=metadata[
            "existing_legacy_id_alias_count"
        ],
        canonical_ids_already_public_count=metadata[
            "canonical_ids_already_public_count"
        ],
        knowledge_type_counts=metadata["knowledge_type_counts"],
        identity_registry_sha256=sha256_file(registry_path),
        public_result_aliases_sha256=sha256_file(aliases_path),
        public_search_projection_sha256=metadata[
            "public_search_projection_sha256"
        ],
    )
    manifest_path.write_text(
        json.dumps(
            manifest.public_dump(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        **manifest.public_dump(),
        "manifest_path": str(manifest_path),
        "private_migration_audit_count": sum(
            1
            for _row in read_jsonl(
                shadow_destination / "identity-migrations.jsonl"
            )
        ),
    }


def build_public_identity_baseline(
    *,
    identities: Iterable[KnowledgeIdentity],
    knowledge_units: Iterable[KnowledgeUnit],
    public_search_rows: Iterable[dict[str, Any]],
    historical_public_result_ids: Iterable[str] = (),
) -> tuple[
    list[KnowledgeIdentity],
    list[PublicResultAlias],
    dict[str, Any],
]:
    identity_rows = sorted(
        identities,
        key=lambda row: row.knowledge_unit_id,
    )
    units_by_id = {
        row.knowledge_unit_id: row
        for row in knowledge_units
    }
    if {row.knowledge_unit_id for row in identity_rows} != set(units_by_id):
        raise ValueError(
            "identity baseline requires exact identity and knowledge-unit coverage"
        )
    supported_rows = sorted(
        (
            dict(row)
            for row in public_search_rows
            if str(row.get("kind") or "") in SUPPORTED_SEARCH_KINDS
        ),
        key=lambda row: str(row.get("id") or ""),
    )
    public_alias_sources: dict[str, str] = {}
    public_result_ids: set[str] = set()
    reviewed_historical_ids = sorted(
        {
            str(value).strip()
            for value in historical_public_result_ids
            if str(value).strip()
        }
    )
    for result_id in reviewed_historical_ids:
        public_result_ids.add(result_id)
        public_alias_sources[result_id] = "existing_public_result_id"
    for row in supported_rows:
        row_id = str(row.get("id") or "").strip()
        if not row_id:
            raise ValueError("public search rows require IDs")
        public_result_ids.add(row_id)
        public_alias_sources[row_id] = "existing_public_result_id"
        for raw_alias in row.get("legacy_ids") or []:
            alias = str(raw_alias).strip()
            if alias and alias not in public_alias_sources:
                public_alias_sources[alias] = "existing_public_legacy_id"

    sanitized_registry: list[KnowledgeIdentity] = []
    alias_owners: dict[str, str] = {}
    for identity in identity_rows:
        public_aliases = sorted(
            alias
            for alias in identity.aliases
            if alias in public_alias_sources
        )
        sanitized = KnowledgeIdentity.model_validate(
            identity.model_copy(
                update={"aliases": public_aliases}
            ).model_dump(by_alias=True)
        )
        sanitized_registry.append(sanitized)
        for alias in public_aliases:
            existing = alias_owners.get(alias)
            if existing and existing != identity.knowledge_unit_id:
                raise ValueError(
                    f"public identity alias has multiple owners: {alias}"
                )
            alias_owners[alias] = identity.knowledge_unit_id

    canonical_ids = {
        row.knowledge_unit_id for row in sanitized_registry
    }
    unresolved = sorted(
        alias
        for alias in public_alias_sources
        if alias not in canonical_ids and alias not in alias_owners
    )
    if unresolved:
        raise ValueError(
            "public result IDs are missing from the identity baseline: "
            + ", ".join(unresolved[:10])
        )
    public_aliases = [
        PublicResultAlias(
            schema="rock-kb-public-result-alias-v1",
            alias_id=alias,
            canonical_knowledge_unit_id=canonical_id,
            knowledge_type=units_by_id[canonical_id].knowledge_type,
            source=public_alias_sources[alias],
        )
        for alias, canonical_id in sorted(alias_owners.items())
        if alias != canonical_id
    ]
    alias_source_counts = Counter(row.source for row in public_aliases)
    knowledge_type_counts = Counter(
        row.knowledge_type for row in sanitized_registry
    )
    public_projection = {
        "active_rows": [
            {
                "id": str(row.get("id") or ""),
                "kind": str(row.get("kind") or ""),
                "legacy_ids": sorted(
                    str(value) for value in row.get("legacy_ids") or []
                ),
            }
            for row in supported_rows
        ],
        "reviewed_historical_result_ids": reviewed_historical_ids,
    }
    return sanitized_registry, public_aliases, {
        "existing_result_id_alias_count": alias_source_counts[
            "existing_public_result_id"
        ],
        "existing_legacy_id_alias_count": alias_source_counts[
            "existing_public_legacy_id"
        ],
        "canonical_ids_already_public_count": len(
            canonical_ids & public_result_ids
        ),
        "knowledge_type_counts": dict(sorted(knowledge_type_counts.items())),
        "public_search_projection_sha256": sha256_text(
            json.dumps(
                public_projection,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        ),
    }


def merge_identity_registry_rows(
    *registries: Iterable[dict[str, Any]],
    reviewed_alias_transfers: dict[str, tuple[str, str]] | None = None,
) -> list[dict[str, Any]]:
    """Merge identity history, allowing only reviewed alias ownership transfers."""

    merged: dict[str, KnowledgeIdentity] = {}
    for registry in registries:
        for raw in registry:
            candidate = KnowledgeIdentity.model_validate(raw)
            existing = merged.get(candidate.knowledge_unit_id)
            if existing is None:
                merged[candidate.knowledge_unit_id] = candidate
                continue
            if (
                existing.knowledge_type != candidate.knowledge_type
                or existing.identity_key != candidate.identity_key
            ):
                raise ValueError(
                    "persistent and local identity registries disagree for "
                    f"{candidate.knowledge_unit_id}"
                )
            merged[candidate.knowledge_unit_id] = KnowledgeIdentity.model_validate(
                candidate.model_copy(
                    update={
                        "aliases": sorted(
                            {*existing.aliases, *candidate.aliases}
                        )
                    }
                ).model_dump(by_alias=True)
            )
    aliases_by_owner = {
        identity.knowledge_unit_id: set(identity.aliases)
        for identity in merged.values()
    }
    owners_by_alias: dict[str, set[str]] = defaultdict(set)
    for identity in merged.values():
        for alias in identity.aliases:
            owners_by_alias[alias].add(identity.knowledge_unit_id)
    allowed_transfers = reviewed_alias_transfers or {}
    for alias, owners in owners_by_alias.items():
        if len(owners) <= 1:
            continue
        transfer = allowed_transfers.get(alias)
        if transfer is None or owners != set(transfer):
            raise ValueError(
                f"identity registry alias has multiple owners: {alias}"
            )
        from_id, to_id = transfer
        if from_id not in merged or to_id not in merged:
            raise ValueError(
                f"reviewed identity alias transfer is incompatible: {alias}"
            )
        aliases_by_owner[from_id].discard(alias)

    normalized: list[KnowledgeIdentity] = []
    alias_owners: dict[str, str] = {}
    for identity in merged.values():
        updated = KnowledgeIdentity.model_validate(
            identity.model_copy(
                update={"aliases": sorted(aliases_by_owner[identity.knowledge_unit_id])}
            ).model_dump(by_alias=True)
        )
        for alias in updated.aliases:
            owner = alias_owners.get(alias)
            if owner and owner != updated.knowledge_unit_id:
                raise ValueError(
                    f"identity registry alias has multiple owners: {alias}"
                )
            alias_owners[alias] = updated.knowledge_unit_id
        normalized.append(updated)
    return [
        row.public_dump()
        for row in sorted(
            normalized,
            key=lambda row: row.knowledge_unit_id,
        )
    ]


def source_native_reviewed_alias_transfers(
    source_native: dict[str, list[Any]],
) -> dict[str, tuple[str, str]]:
    """Return exact alias reassignments authorized by reviewed migrations."""

    transfers: dict[str, tuple[str, str]] = {}
    migration_rows = [
        *source_native.get("legacy_migrations", []),
        *source_native.get("artifact_migrations", []),
    ]
    for migration in migration_rows:
        if hasattr(migration, "legacy_knowledge_unit_id"):
            from_id = migration.legacy_knowledge_unit_id
            aliases = {
                from_id,
                *migration.legacy_result_ids,
            }
        else:
            from_id = migration.prior_artifact_id
            aliases = {from_id}
        to_id = migration.replacement_artifact_id
        for alias in aliases:
            transfer = (from_id, to_id)
            existing = transfers.get(alias)
            if existing is not None and existing != transfer:
                raise ValueError(
                    f"reviewed migrations assign an alias to multiple targets: {alias}"
                )
            transfers[alias] = transfer
    return transfers


def repository_relative_or_name(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.name


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_claim_groups(
    claim_rows: Iterable[dict[str, Any]],
    distilled_rows: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for row in claim_rows:
        payload = public_claim_payload(row.get("payload") or {})
        statement = str(row.get("body") or payload.get("claim") or "").strip()
        claim_type = str(payload.get("claim_type") or "other")
        if not statement:
            continue
        key = canonical_claim_fingerprint(statement, claim_type)
        group = groups.setdefault(
            key,
            {
                "fingerprint": key,
                "statement": statement,
                "claim_type": claim_type,
                "claim_rows": [],
                "distilled_rows": [],
            },
        )
        group["claim_rows"].append({**row, "payload": payload})

    for raw in distilled_rows:
        row = dict(raw)
        statement = str(row.get("distilled_claim") or row.get("generated_distilled_claim") or "").strip()
        claim_type = str(row.get("claim_type") or "other")
        if not statement:
            continue
        key = canonical_claim_fingerprint(statement, claim_type)
        group = groups.setdefault(
            key,
            {
                "fingerprint": key,
                "statement": statement,
                "claim_type": claim_type,
                "claim_rows": [],
                "distilled_rows": [],
            },
        )
        group["distilled_rows"].append(row)

    return sorted(groups.values(), key=lambda row: row["fingerprint"])


def canonical_claim_fingerprint(statement: str, claim_type: str) -> str:
    normalized = normalize_statement(statement)
    return sha256_text(f"{claim_type.strip().lower()}:{normalized}")


def claim_group_aliases(
    claim_rows: Iterable[dict[str, Any]],
    distilled_rows: Iterable[dict[str, Any]],
) -> list[str]:
    aliases: set[str] = set()
    for row in claim_rows:
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        aliases.update(
            str(value)
            for value in [
                row.get("id"),
                payload.get("claim_id"),
                *(row.get("legacy_ids") or []),
            ]
            if value
        )
    for row in distilled_rows:
        aliases.update(
            str(value)
            for value in [
                row.get("id"),
                row.get("distilled_claim_id"),
            ]
            if value
        )
    return sorted(aliases)


def claim_group_payload(group: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "rock-kb-canonical-claim-payload-v1",
        "claim_type": group["claim_type"],
        "approved_claims": sorted(
            [row.get("payload") or {} for row in group["claim_rows"]],
            key=lambda row: str(row.get("claim_id") or ""),
        ),
        "distillations": sorted(
            group["distilled_rows"],
            key=lambda row: str(row.get("id") or ""),
        ),
    }


def claim_group_content_hash(group: dict[str, Any]) -> str:
    payload = claim_group_payload(group)
    assert_public_safe(payload)
    return sha256_text(canonical_json(payload))


def search_row_payload_content_hash(kind: str, payload: dict[str, Any]) -> str:
    """Hash answer-bearing payload content without source-check timestamps."""

    stable_payload = dict(payload)
    if kind == "source_summary":
        for field in VOLATILE_SOURCE_SUMMARY_FIELDS:
            stable_payload.pop(field, None)
    return sha256_text(canonical_json(stable_payload))


def claim_group_source_record_ids(group: dict[str, Any]) -> list[str]:
    return sorted(
        {
            str(value)
            for row in group["claim_rows"]
            for value in (row.get("payload") or {}).get("source_record_ids") or []
            if value
        }
        | {
            str(value)
            for row in group["distilled_rows"]
            for value in row.get("source_record_ids") or []
            if value
        }
    )


def search_row_source_record_ids(row: dict[str, Any]) -> list[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values = {
        str(value)
        for value in payload.get("source_record_ids") or []
        if value
    }
    source_record_id = search_row_source_record_id(row)
    if source_record_id:
        values.add(source_record_id)
    return sorted(values)


def claim_identity_anchor(
    claim_rows: Iterable[dict[str, Any]],
    distilled_rows: Iterable[dict[str, Any]],
) -> str:
    approved_claim_ids = sorted(
        {
            str(payload.get("claim_id"))
            for row in claim_rows
            for payload in [row.get("payload") if isinstance(row.get("payload"), dict) else {}]
            if payload.get("claim_id")
        }
    )
    if approved_claim_ids:
        return approved_claim_ids[0]
    distilled_ids = sorted(
        {
            str(row.get("id") or row.get("distilled_claim_id"))
            for row in distilled_rows
            if row.get("id") or row.get("distilled_claim_id")
        }
    )
    if distilled_ids:
        return distilled_ids[0]
    supporting_claim_ids = sorted(
        {
            str(value)
            for row in distilled_rows
            for value in row.get("supporting_claim_ids") or []
            if value
        }
    )
    if supporting_claim_ids:
        return supporting_claim_ids[0]
    row_ids = sorted(
        {
            str(value)
            for row in claim_rows
            for value in [row.get("id")]
            if value
        }
    )
    return row_ids[0] if row_ids else ""


def normalize_statement(value: str) -> str:
    normalized = str(value or "").replace("\u2019", "'").replace("\u2018", "'")
    normalized = normalized.replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", normalized).strip().lower()


class _IdentityResolver:
    def __init__(
        self,
        *,
        identity_registry: Iterable[dict[str, Any]],
        identity_migrations: Iterable[dict[str, Any]],
        previous_knowledge_units: Iterable[dict[str, Any]],
    ) -> None:
        self.registry = {
            row.knowledge_unit_id: row
            for raw in identity_registry
            for row in [KnowledgeIdentity.model_validate(raw)]
        }
        self.alias_index: dict[str, set[str]] = defaultdict(set)
        for row in self.registry.values():
            for alias in row.aliases:
                self.alias_index[alias].add(row.knowledge_unit_id)
        self.previous_units = {
            row.knowledge_unit_id: row
            for raw in previous_knowledge_units
            for row in [KnowledgeUnit.model_validate(raw)]
        }
        self.previous_alias_index: dict[str, set[str]] = defaultdict(set)
        for row in self.previous_units.values():
            for alias in [row.knowledge_unit_id, *row.legacy_ids]:
                self.previous_alias_index[alias].add(row.knowledge_unit_id)
        self.identities: dict[str, KnowledgeIdentity] = {}
        self.migrations = {
            row.migration_id: row
            for raw in identity_migrations
            for row in [KnowledgeIdentityMigration.model_validate(raw)]
        }

    def resolve(
        self,
        *,
        knowledge_type: str,
        aliases: Iterable[str],
        content_fingerprint: str,
        default_identity_key: str,
        default_knowledge_unit_id: str,
        default_basis: str,
        preferred_registry_id: str | None = None,
        merge_reason: str | None = None,
        merge_review_state: str = "generated_needs_reviewer_approval",
    ) -> KnowledgeIdentity:
        current_aliases = {str(value).strip() for value in aliases if str(value).strip()}
        matched_registry_ids = {
            registry_id
            for alias in current_aliases
            for registry_id in self.alias_index.get(alias, set())
        }
        if matched_registry_ids:
            if preferred_registry_id:
                survivor_id = preferred_registry_id
            else:
                survivor_id = min(matched_registry_ids)
            survivor = self.registry.get(survivor_id)
            identity_key = (
                survivor.identity_key if survivor else default_identity_key
            )
            basis = (
                "registry_merge"
                if len(matched_registry_ids) > 1
                or survivor_id not in matched_registry_ids
                else survivor.identity_basis
            )
            for registry_id in sorted(matched_registry_ids):
                current_aliases.update(self.registry[registry_id].aliases)
                if registry_id != survivor_id:
                    self.add_migration(
                        from_id=registry_id,
                        to_id=survivor_id,
                        migration_type="identity_merge",
                        reason=merge_reason
                        or (
                            "Previously distinct registry identities now share an explicit "
                            "source or legacy alias; the selected identity survives."
                        ),
                        matched_aliases=sorted(
                            set(self.registry[registry_id].aliases) & current_aliases
                        ),
                        review_state=merge_review_state,
                    )
        else:
            survivor_id = default_knowledge_unit_id
            identity_key = default_identity_key
            basis = default_basis

        if survivor_id in self.identities:
            raise ValueError(
                "one persistent identity matched multiple current knowledge units: "
                f"{survivor_id}"
            )

        prior_ids = {
            prior_id
            for alias in current_aliases
            for prior_id in self.previous_alias_index.get(alias, set())
        }
        for prior_id in sorted(prior_ids):
            if prior_id == survivor_id:
                continue
            prior = self.previous_units[prior_id]
            current_aliases.add(prior_id)
            self.add_migration(
                from_id=prior_id,
                to_id=survivor_id,
                migration_type=(
                    "content_addressed_to_registry"
                    if prior.knowledge_type == "claim"
                    else "identity_reassignment"
                ),
                reason=(
                    "The prior shadow identity was derived from mutable content. "
                    "The replacement is anchored in the persistent identity registry."
                ),
                matched_aliases=sorted(
                    set(prior.legacy_ids) & current_aliases
                ),
            )

        current_aliases.discard(survivor_id)
        identity = KnowledgeIdentity(
            schema="rock-kb-knowledge-identity-v1",
            knowledge_unit_id=survivor_id,
            knowledge_type=knowledge_type,
            identity_key=identity_key,
            identity_basis=basis,
            aliases=sorted(current_aliases),
            content_fingerprint=content_fingerprint,
        )
        self.identities[survivor_id] = identity
        return identity

    def add_migration(
        self,
        *,
        from_id: str,
        to_id: str,
        migration_type: str,
        reason: str,
        matched_aliases: list[str],
        review_state: str = "generated_needs_reviewer_approval",
    ) -> None:
        migration_id = "identity-migration:" + sha256_text(
            f"{from_id}:{to_id}:{migration_type}"
        )[:24]
        self.migrations[migration_id] = KnowledgeIdentityMigration(
            schema="rock-kb-knowledge-identity-migration-v1",
            migration_id=migration_id,
            from_knowledge_unit_id=from_id,
            to_knowledge_unit_id=to_id,
            migration_type=migration_type,
            reason=reason,
            matched_aliases=matched_aliases,
            review_state=review_state,
        )

    def migrations_resolving_to(
        self, current_knowledge_unit_ids: set[str]
    ) -> list[KnowledgeIdentityMigration]:
        migrations_by_source: dict[str, KnowledgeIdentityMigration] = {}
        for migration in self.migrations.values():
            existing = migrations_by_source.get(migration.from_knowledge_unit_id)
            if (
                existing is not None
                and existing.to_knowledge_unit_id
                != migration.to_knowledge_unit_id
            ):
                raise ValueError(
                    "identity migration source has multiple targets: "
                    f"{migration.from_knowledge_unit_id}"
                )
            migrations_by_source[migration.from_knowledge_unit_id] = migration

        active_sources: set[str] = set()
        for source_id in migrations_by_source:
            visited: set[str] = set()
            target = source_id
            path: list[str] = []
            while target in migrations_by_source:
                if target in visited:
                    raise ValueError(f"identity migration cycle detected: {source_id}")
                visited.add(target)
                path.append(target)
                target = migrations_by_source[target].to_knowledge_unit_id
            if target in current_knowledge_unit_ids:
                active_sources.update(path)

        return [
            migration
            for source_id, migration in migrations_by_source.items()
            if source_id in active_sources
        ]


class _ProjectionBuilder:
    def __init__(self, identity_resolver: _IdentityResolver) -> None:
        self.snapshots: dict[str, SourceSnapshot] = {}
        self.units: dict[str, SourceUnit] = {}
        self.activities: dict[str, GenerationActivity] = {}
        self.knowledge: dict[str, KnowledgeUnit] = {}
        self.links: dict[str, EvidenceLink] = {}
        self.relationships: dict[str, KnowledgeRelationship] = {}
        self.identity_resolver = identity_resolver

    def add_reviewed_cross_source(
        self,
        records: dict[str, list[Any]],
    ) -> None:
        for snapshot in records.get("source_snapshots") or []:
            self.store_snapshot(snapshot)
        for unit in records.get("source_units") or []:
            existing = self.units.get(unit.source_unit_id)
            if existing and existing != unit:
                raise ValueError(
                    "reviewed cross-source unit conflicts with an existing "
                    f"source unit: {unit.source_unit_id}"
                )
            self.units[unit.source_unit_id] = unit
        for activity in records.get("generation_activities") or []:
            existing = self.activities.get(activity.generation_activity_id)
            if existing and existing != activity:
                raise ValueError(
                    "reviewed cross-source generation activity conflicts with "
                    f"an existing activity: {activity.generation_activity_id}"
                )
            self.activities[activity.generation_activity_id] = activity

        canonical_ids: dict[str, str] = {}
        for item in records.get("knowledge_units") or []:
            identity = self.identity_resolver.resolve(
                knowledge_type=item.knowledge_type,
                aliases=[
                    item.knowledge_unit_id,
                    *item.legacy_ids,
                ],
                content_fingerprint=item.content_hash,
                default_identity_key=(
                    f"reviewed_cross_source:{item.knowledge_unit_id}"
                ),
                default_knowledge_unit_id=item.knowledge_unit_id,
                default_basis="source_identity",
            )
            canonical_ids[item.knowledge_unit_id] = (
                identity.knowledge_unit_id
            )
            updated = item.model_copy(
                update={
                    "knowledge_unit_id": identity.knowledge_unit_id,
                    "ingestion_mode": "reviewed_cross_source_synthesis",
                    "legacy_ids": identity.aliases,
                }
            )
            self.knowledge[identity.knowledge_unit_id] = (
                KnowledgeUnit.model_validate(
                    updated.model_dump(by_alias=True)
                )
            )

        for link in records.get("evidence_links") or []:
            knowledge_unit_id = canonical_ids.get(
                link.knowledge_unit_id,
                link.knowledge_unit_id,
            )
            updated = link.model_copy(
                update={
                    "knowledge_unit_id": knowledge_unit_id,
                    "evidence_link_id": "evidence:"
                    + sha256_text(
                        f"{knowledge_unit_id}:{link.source_unit_id}:"
                        f"{link.relation}"
                    )[:24],
                }
            )
            self.links[updated.evidence_link_id] = (
                EvidenceLink.model_validate(
                    updated.model_dump(by_alias=True)
                )
            )

        endpoint_aliases = {
            alias: identity.knowledge_unit_id
            for identity in self.identity_resolver.identities.values()
            for alias in (
                identity.knowledge_unit_id,
                *identity.aliases,
            )
        }
        for relationship in records.get("relationships") or []:
            from_id = canonical_ids.get(
                relationship.from_id,
                endpoint_aliases.get(
                    relationship.from_id,
                    relationship.from_id,
                ),
            )
            to_id = canonical_ids.get(
                relationship.to_id,
                endpoint_aliases.get(
                    relationship.to_id,
                    relationship.to_id,
                ),
            )
            updated = relationship.model_copy(
                update={
                    "relationship_id": "relationship:"
                    + sha256_text(
                        f"{from_id}:{relationship.relation}:{to_id}"
                    )[:24],
                    "from_id": from_id,
                    "to_id": to_id,
                }
            )
            self.relationships[updated.relationship_id] = (
                KnowledgeRelationship.model_validate(
                    updated.model_dump(by_alias=True)
                )
            )

    def add_source_native_pilot(
        self,
        records: dict[str, list[Any]],
        *,
        legacy_migration_index: LegacyMigrationIndex | None = None,
        artifact_migration_index: SourceNativeArtifactMigrationIndex | None = None,
    ) -> None:
        for snapshot in records.get("source_snapshots") or []:
            self.store_snapshot(snapshot)
        for unit in records.get("source_units") or []:
            existing = self.units.get(unit.source_unit_id)
            if existing and existing != unit:
                raise ValueError(
                    "source-native unit conflicts with an existing source unit: "
                    f"{unit.source_unit_id}"
                )
            self.units[unit.source_unit_id] = unit
        for activity in records.get("generation_activities") or []:
            existing = self.activities.get(activity.generation_activity_id)
            if existing and existing != activity:
                raise ValueError(
                    "source-native generation activity conflicts with an existing "
                    f"activity: {activity.generation_activity_id}"
                )
            self.activities[activity.generation_activity_id] = activity

        verification_by_artifact = verification_resolutions_by_artifact(
            queue_rows=[
                row.public_dump()
                for row in records.get("verification_queue") or []
            ],
            resolution_rows=[
                row.public_dump()
                for row in records.get("verification_resolutions") or []
            ],
        )
        knowledge_units, evidence_links = canonical_records_for_source_native_artifacts(
            records.get("reviewed_artifacts") or [],
            verification_by_artifact=verification_by_artifact,
        )
        migration_aliases = (
            legacy_migration_index.aliases_by_replacement()
            if legacy_migration_index
            else {}
        )
        artifact_migration_aliases = (
            artifact_migration_index.aliases_by_replacement()
            if artifact_migration_index
            else {}
        )
        migrations_by_replacement = (
            legacy_migration_index.migrations_by_replacement()
            if legacy_migration_index
            else {}
        )
        artifact_migrations_by_replacement = (
            artifact_migration_index.migrations_by_replacement()
            if artifact_migration_index
            else {}
        )
        canonical_ids: dict[str, str] = {}
        for item in knowledge_units:
            replacement_migrations = migrations_by_replacement.get(
                item.knowledge_unit_id,
                [],
            )
            artifact_replacement_migrations = (
                artifact_migrations_by_replacement.get(
                    item.knowledge_unit_id,
                    [],
                )
            )
            updated_payload = (
                {
                    **item.payload,
                    **(
                        {
                            "legacy_migrations": [
                                {
                                    "migration_id": row.migration_id,
                                    "legacy_knowledge_unit_id": (
                                        row.legacy_knowledge_unit_id
                                    ),
                                    "coverage": row.coverage,
                                    "review_state": row.review_state,
                                    "reviewed_at": row.reviewed_at,
                                }
                                for row in replacement_migrations
                            ]
                        }
                        if replacement_migrations
                        else {}
                    ),
                    **(
                        {
                            "source_native_artifact_migrations": [
                                {
                                    "migration_id": row.migration_id,
                                    "prior_artifact_id": row.prior_artifact_id,
                                    "review_state": row.review_state,
                                    "reviewed_at": row.reviewed_at,
                                }
                                for row in artifact_replacement_migrations
                            ]
                        }
                        if artifact_replacement_migrations
                        else {}
                    ),
                }
                if replacement_migrations or artifact_replacement_migrations
                else item.payload
            )
            updated_content_hash = sha256_text(canonical_json(updated_payload))
            identity = self.identity_resolver.resolve(
                knowledge_type=item.knowledge_type,
                aliases=[
                    item.knowledge_unit_id,
                    *migration_aliases.get(item.knowledge_unit_id, []),
                    *artifact_migration_aliases.get(
                        item.knowledge_unit_id,
                        [],
                    ),
                ],
                content_fingerprint=updated_content_hash,
                default_identity_key=(
                    f"source_native_artifact:{item.knowledge_unit_id}"
                ),
                default_knowledge_unit_id=item.knowledge_unit_id,
                default_basis="source_identity",
                preferred_registry_id=(
                    item.knowledge_unit_id
                    if replacement_migrations or artifact_replacement_migrations
                    else None
                ),
                merge_reason=(
                    "A reviewer-approved, hash-bound source-native migration "
                    "replaced an earlier projection while preserving its public IDs."
                    if replacement_migrations or artifact_replacement_migrations
                    else None
                ),
                merge_review_state=(
                    "reviewer_approved"
                    if replacement_migrations or artifact_replacement_migrations
                    else "generated_needs_reviewer_approval"
                ),
            )
            canonical_ids[item.knowledge_unit_id] = identity.knowledge_unit_id
            source_work_ids = sorted(
                {
                    str(snapshot.source_work_id)
                    for source_unit_id in item.source_unit_ids
                    if (source_unit := self.units.get(source_unit_id))
                    and (
                        snapshot := self.snapshots.get(
                            source_unit.source_snapshot_id
                        )
                    )
                    and snapshot.source_work_id
                }
            )
            updated = item.model_copy(
                update={
                    "knowledge_unit_id": identity.knowledge_unit_id,
                    "ingestion_mode": "source_native_distillation",
                    "source_work_ids": source_work_ids,
                    "legacy_ids": identity.aliases,
                    "payload": updated_payload,
                    "content_hash": updated_content_hash,
                }
            )
            self.knowledge[identity.knowledge_unit_id] = KnowledgeUnit.model_validate(
                updated.model_dump(by_alias=True)
            )
        for link in evidence_links:
            knowledge_unit_id = canonical_ids.get(
                link.knowledge_unit_id,
                link.knowledge_unit_id,
            )
            updated = link.model_copy(
                update={
                    "knowledge_unit_id": knowledge_unit_id,
                    "evidence_link_id": "evidence:"
                    + sha256_text(
                        f"{knowledge_unit_id}:{link.source_unit_id}:"
                        f"{link.relation}"
                    )[:24],
                }
            )
            self.links[updated.evidence_link_id] = EvidenceLink.model_validate(
                updated.model_dump(by_alias=True)
            )
        alias_to_canonical = {
            alias: identity.knowledge_unit_id
            for identity in self.identity_resolver.identities.values()
            for alias in identity.aliases
        }
        for relationship in records.get("relationships") or []:
            from_id = canonical_ids.get(
                relationship.from_id,
                alias_to_canonical.get(
                    relationship.from_id,
                    relationship.from_id,
                ),
            )
            to_id = canonical_ids.get(
                relationship.to_id,
                alias_to_canonical.get(
                    relationship.to_id,
                    relationship.to_id,
                ),
            )
            if from_id == to_id:
                continue
            updated = relationship.model_copy(
                update={
                    "relationship_id": "relationship:"
                    + sha256_text(
                        f"{from_id}:{relationship.relation}:{to_id}"
                    )[:24],
                    "from_id": from_id,
                    "to_id": to_id,
                }
            )
            self.relationships[updated.relationship_id] = (
                KnowledgeRelationship.model_validate(
                    updated.model_dump(by_alias=True)
                )
            )
        required_replacement_ids = set(migrations_by_replacement)
        required_replacement_ids.update(artifact_migrations_by_replacement)
        required_replacement_ids.update(
            row.artifact_id
            for migrations in migrations_by_replacement.values()
            for migration in migrations
            for row in migration.supporting_replacement_artifacts
        )
        missing_replacements = sorted(
            required_replacement_ids - set(canonical_ids)
        )
        if missing_replacements:
            raise ValueError(
                "reviewed source-native migrations reference artifacts that are not "
                "active canonical knowledge: "
                + ", ".join(missing_replacements[:3])
            )
        for migrations in migrations_by_replacement.values():
            for migration in migrations:
                from_id = canonical_ids[migration.replacement_artifact_id]
                for supporting in migration.supporting_replacement_artifacts:
                    to_id = canonical_ids[supporting.artifact_id]
                    if from_id == to_id:
                        continue
                    relationship_id = "relationship:" + sha256_text(
                        f"{from_id}:references:{to_id}"
                    )[:24]
                    self.relationships.setdefault(
                        relationship_id,
                        KnowledgeRelationship(
                        schema="rock-kb-knowledge-relationship-v1",
                        relationship_id=relationship_id,
                        from_id=from_id,
                        to_id=to_id,
                        relation="references",
                        decision="accept",
                        confidence="high",
                        rationale=(
                            "A reviewer-approved legacy source-summary migration "
                            "identified this typed artifact as part of the replacement "
                            "coverage."
                        ),
                        reviewed_at=migration.reviewed_at,
                        ),
                    )

    def add_claim_group(self, group: dict[str, Any]) -> None:
        statement = str(group["statement"])
        fingerprint = str(group["fingerprint"])
        claim_rows = list(group["claim_rows"])
        distilled_rows = list(group["distilled_rows"])
        legacy_ids = claim_group_aliases(claim_rows, distilled_rows)
        anchor = claim_identity_anchor(claim_rows, distilled_rows)
        identity_key = f"claim_alias:{anchor}" if anchor else f"claim_content:{fingerprint}"
        identity = self.identity_resolver.resolve(
            knowledge_type="claim",
            aliases=legacy_ids,
            content_fingerprint=fingerprint,
            default_identity_key=identity_key,
            default_knowledge_unit_id=(
                "knowledge:claim:" + sha256_text(identity_key)[:24]
            ),
            default_basis="legacy_anchor" if anchor else "content_fallback",
        )
        prior_content_addressed_id = f"knowledge:claim:{fingerprint[:24]}"
        if prior_content_addressed_id != identity.knowledge_unit_id:
            identity = identity.model_copy(
                update={
                    "aliases": sorted(
                        {*identity.aliases, prior_content_addressed_id}
                    )
                }
            )
            identity = KnowledgeIdentity.model_validate(
                identity.model_dump(by_alias=True)
            )
            self.identity_resolver.identities[identity.knowledge_unit_id] = identity
            self.identity_resolver.add_migration(
                from_id=prior_content_addressed_id,
                to_id=identity.knowledge_unit_id,
                migration_type="content_addressed_to_registry",
                reason=(
                    "The initial canonical pilot derived this claim identity from mutable "
                    "claim wording. The registry-backed identity survives wording changes "
                    "while an explicit alias preserves the prior lookup."
                ),
                matched_aliases=[],
            )
        knowledge_unit_id = identity.knowledge_unit_id
        concepts = sorted(
            {
                str(value)
                for row in claim_rows
                for value in row.get("concepts") or []
                if value
            }
            | {
                str(row.get("concept_id"))
                for row in distilled_rows
                if row.get("concept_id")
            }
        )
        authorities = sorted(
            {
                str(row.get("authority_tier"))
                for row in claim_rows
                if row.get("authority_tier")
            }
            | {
                str(value)
                for row in distilled_rows
                for value in row.get("authority_tiers") or []
                if value
            }
        )
        legacy_ids = identity.aliases
        rock_versions = sorted(
            {
                str(value)
                for row in claim_rows
                for value in (row.get("payload") or {}).get("rock_versions") or []
                if value
            }
        )
        claim_tier = highest_ranked(
            [str(row.get("claim_tier") or "") for row in claim_rows],
            CLAIM_TIER_RANK,
        )
        review_state = highest_ranked(
            [
                str((row.get("payload") or {}).get("review_status") or "")
                for row in claim_rows
            ]
            + [str(row.get("distillation_status") or "") for row in distilled_rows],
            REVIEW_STATE_RANK,
        )
        source_unit_ids: list[str] = []
        source_work_ids: list[str] = []
        evidence_rows = []
        for row in claim_rows:
            payload = row.get("payload") or {}
            refs = payload.get("source_refs") or []
            if not refs and row.get("url"):
                refs = [{"source_id": row.get("source_id"), "url": row.get("url"), "title": row.get("title")}]
            for ref in refs:
                if not isinstance(ref, dict):
                    continue
                unit_id, work_id, authority = self.add_source_for_claim(
                    payload=payload,
                    ref=ref,
                    statement=statement,
                )
                source_unit_ids.append(unit_id)
                source_work_ids.append(work_id)
                evidence_rows.append((unit_id, work_id, authority))

        if not evidence_rows:
            for row in distilled_rows:
                for ref in row.get("source_refs") or []:
                    if not isinstance(ref, dict):
                        continue
                    unit_id, work_id, authority = self.add_source_for_claim(
                        payload=row,
                        ref=ref,
                        statement=statement,
                    )
                    source_unit_ids.append(unit_id)
                    source_work_ids.append(work_id)
                    evidence_rows.append((unit_id, work_id, authority))

        payload = claim_group_payload(group)
        assert_public_safe(payload)
        item = KnowledgeUnit(
            schema="rock-kb-knowledge-unit-v1",
            knowledge_unit_id=knowledge_unit_id,
            knowledge_type="claim",
            ingestion_mode="legacy_reviewed_claim_projection",
            title=statement[:500],
            retrieval_text=statement,
            concept_facets=concepts,
            authority_tiers=authorities,
            claim_tier=claim_tier or None,
            review_state=review_state or None,
            rock_versions=rock_versions,
            version_scope_status="scoped" if rock_versions else claim_version_scope(claim_rows),
            source_unit_ids=sorted(set(source_unit_ids)),
            source_work_ids=sorted(set(source_work_ids)),
            legacy_ids=legacy_ids,
            payload_schema="rock-kb-canonical-claim-payload-v1",
            payload=payload,
            content_hash=sha256_text(canonical_json(payload)),
        )
        self.knowledge[item.knowledge_unit_id] = item
        for source_unit_id, work_id, authority in sorted(set(evidence_rows)):
            link_id = "evidence:" + sha256_text(f"{knowledge_unit_id}:{source_unit_id}:supports")[:24]
            self.links[link_id] = EvidenceLink(
                schema="rock-kb-evidence-link-v1",
                evidence_link_id=link_id,
                knowledge_unit_id=knowledge_unit_id,
                source_unit_id=source_unit_id,
                relation="supports",
                evidence_summary=f"The reviewed source unit supports this claim: {statement}"[:1500],
                authority_tier=authority,
                confidence="high" if review_state in {"reviewer_approved", "approved_for_answer_pack"} else "medium",
                independence_group=work_id,
                needs_review=not bool(review_state),
            )

    def add_search_row(self, raw: dict[str, Any]) -> None:
        row = dict(raw)
        kind = str(row.get("kind") or "other")
        payload = dict(row.get("payload") or {})
        contract = source_family_contract(kind, payload)
        assert_public_safe(payload)
        row_id = str(row.get("id") or "")
        title = str(row.get("title") or row_id)
        retrieval_text = str(row.get("body") or title).strip()
        content_fingerprint = sha256_text(
            canonical_json(
                {
                    "title": title,
                    "retrieval_text": retrieval_text,
                    "payload": payload,
                }
            )
        )
        identity = self.identity_resolver.resolve(
            knowledge_type=kind if kind in SUPPORTED_SEARCH_KINDS else "other",
            aliases=[row_id, *(row.get("legacy_ids") or [])],
            content_fingerprint=content_fingerprint,
            default_identity_key=f"search_row:{kind}:{row_id}",
            default_knowledge_unit_id=row_id,
            default_basis="source_identity",
        )
        prior_hashed_id = f"knowledge:{kind}:{sha256_text(row_id)[:24]}"
        if prior_hashed_id != identity.knowledge_unit_id:
            identity = identity.model_copy(
                update={"aliases": sorted({*identity.aliases, prior_hashed_id})}
            )
            identity = KnowledgeIdentity.model_validate(
                identity.model_dump(by_alias=True)
            )
            self.identity_resolver.identities[identity.knowledge_unit_id] = identity
            self.identity_resolver.add_migration(
                from_id=prior_hashed_id,
                to_id=identity.knowledge_unit_id,
                migration_type="identity_reassignment",
                reason=(
                    "The initial canonical pilot wrapped an already stable, namespaced "
                    "source artifact ID in an opaque hash. The source identity is now "
                    "canonical and the pilot hash remains an explicit alias."
                ),
                matched_aliases=[],
            )
        knowledge_unit_id = identity.knowledge_unit_id
        source_unit_ids: list[str] = []
        source_work_ids: list[str] = []
        evidence_rows = []
        refs = source_refs_for_search_row(row)
        for ref in refs:
            unit_id, work_id = self.add_source_for_search_row(row, ref)
            source_unit_ids.append(unit_id)
            source_work_ids.append(work_id)
            evidence_rows.append((unit_id, work_id))

        item = KnowledgeUnit(
            schema="rock-kb-knowledge-unit-v1",
            knowledge_unit_id=knowledge_unit_id,
            knowledge_type=kind if kind in SUPPORTED_SEARCH_KINDS else "other",
            ingestion_mode=contract.ingestion_mode,
            title=title,
            retrieval_text=retrieval_text,
            concept_facets=sorted({str(value) for value in row.get("concepts") or [] if value}),
            topic_facets=sorted({str(value) for value in row.get("topics") or [] if value}),
            authority_tiers=sorted({str(row.get("authority_tier"))} if row.get("authority_tier") else set()),
            claim_tier=str(row.get("claim_tier") or "") or None,
            review_state=search_row_review_state(payload),
            rock_versions=search_row_versions(payload),
            version_scope_status=search_row_version_scope(payload),
            source_unit_ids=sorted(set(source_unit_ids)),
            source_work_ids=sorted(set(source_work_ids)),
            legacy_ids=identity.aliases,
            payload_schema=str(payload.get("schema") or "") or None,
            payload=payload,
            content_hash=search_row_payload_content_hash(kind, payload),
        )
        self.knowledge[item.knowledge_unit_id] = item
        for source_unit_id, work_id in sorted(set(evidence_rows)):
            link_id = "evidence:" + sha256_text(f"{knowledge_unit_id}:{source_unit_id}:supports")[:24]
            self.links[link_id] = EvidenceLink(
                schema="rock-kb-evidence-link-v1",
                evidence_link_id=link_id,
                knowledge_unit_id=knowledge_unit_id,
                source_unit_id=source_unit_id,
                relation="supports",
                evidence_summary=f"The source record supports the routed {kind} artifact: {title}"[:1500],
                authority_tier=str(row.get("authority_tier") or "unknown"),
                confidence="medium",
                independence_group=work_id,
                needs_review=bool(payload.get("needs_review") or payload.get("needs_live_verification")),
            )

    def add_source_for_claim(
        self,
        *,
        payload: dict[str, Any],
        ref: dict[str, Any],
        statement: str,
    ) -> tuple[str, str, str]:
        source_id = str(ref.get("source_id") or payload.get("source_id") or "unknown")
        url = https_url(ref.get("url") or ref.get("source_timestamp_url"))
        source_record_id = matching_source_record_id(source_id, payload.get("source_record_ids") or [])
        source_work_id = infer_source_work_id(
            source_id=source_id,
            source_title=str(ref.get("title") or ""),
            source_record_id=source_record_id,
            source_url=url or "",
        )
        snapshot_id = source_snapshot_id(source_id, source_record_id, url, None)
        authority = str(payload.get("authority_tier") or "unknown")
        self.store_snapshot(
            SourceSnapshot(
                schema="rock-kb-source-snapshot-v1",
                source_snapshot_id=snapshot_id,
                source_id=source_id,
                source_record_id=source_record_id or None,
                source_work_id=source_work_id,
                canonical_url=url,
                title=str(ref.get("title") or "") or None,
                observed_at=first_value(payload, "updated_at", "created_at", "reviewed_at"),
                content_hash=None,
                immutable=False,
                authority_tier=authority,
                public_policy=public_handling(payload),
                derivation={"artifact_kind": "claim"},
            )
        )
        locator = claim_source_locator(ref, source_record_id, url)
        unit_id = source_unit_id(snapshot_id, locator)
        safe_hash = valid_sha256(payload.get("safe_evidence_hash"))
        self.units.setdefault(
            unit_id,
            SourceUnit(
                schema="rock-kb-source-unit-v1",
                source_unit_id=unit_id,
                source_snapshot_id=snapshot_id,
                unit_kind="media_segment" if locator.kind == "timestamp" else "document_section",
                locator=locator,
                context=str(ref.get("title") or "")[:1000],
                public_summary=statement[:1500],
                normalized_content_hash=safe_hash,
                required_public_handling=public_handling(payload),
            ),
        )
        return unit_id, source_work_id, authority

    def add_source_for_search_row(
        self,
        row: dict[str, Any],
        ref: dict[str, Any],
    ) -> tuple[str, str]:
        payload = row.get("payload") or {}
        kind = str(row.get("kind") or "other")
        source_id = str(ref.get("source_id") or row.get("source_id") or "unknown")
        url = https_url(ref.get("url") or row.get("url"))
        source_record_id = str(ref.get("source_record_id") or search_row_source_record_id(row))
        source_work_id = infer_source_work_id(
            source_id=source_id,
            source_title=str(ref.get("title") or row.get("title") or ""),
            source_record_id=source_record_id,
            source_url=url or "",
            existing=str(payload.get("source_work_id") or "") or None,
        )
        content_hash = search_row_source_hash(payload)
        snapshot_id = source_snapshot_id(source_id, source_record_id, url, content_hash)
        authority = str(row.get("authority_tier") or "unknown")
        self.store_snapshot(
            SourceSnapshot(
                schema="rock-kb-source-snapshot-v1",
                source_snapshot_id=snapshot_id,
                source_id=source_id,
                source_record_id=source_record_id or None,
                source_work_id=source_work_id,
                canonical_url=url,
                title=str(ref.get("title") or row.get("title") or "") or None,
                observed_at=first_value(payload, "updated_at", "retrieved_at", "created_at", "source_commit_date"),
                content_hash=content_hash,
                immutable=search_row_is_immutable(kind, payload, url),
                authority_tier=authority,
                public_policy=public_handling(payload),
                derivation={"artifact_kind": kind, "payload_schema": str(payload.get("schema") or "") or None},
            )
        )
        locator = search_row_locator(row, ref, source_record_id, url)
        unit_id = source_unit_id(snapshot_id, locator)
        self.units.setdefault(
            unit_id,
            SourceUnit(
                schema="rock-kb-source-unit-v1",
                source_unit_id=unit_id,
                source_snapshot_id=snapshot_id,
                unit_kind=source_unit_kind(kind, locator),
                locator=locator,
                context=str(row.get("title") or "")[:1000],
                public_summary=str(row.get("body") or row.get("title") or "")[:1500],
                normalized_content_hash=content_hash,
                required_public_handling=public_handling(payload),
            ),
        )
        return unit_id, source_work_id

    def store_snapshot(self, candidate: SourceSnapshot) -> None:
        existing = self.snapshots.get(candidate.source_snapshot_id)
        if existing is None:
            self.snapshots[candidate.source_snapshot_id] = candidate
            return
        record_ids = [
            value
            for value in (existing.source_record_id, candidate.source_record_id)
            if value
        ]
        preferred_record_id = max(record_ids, key=source_record_quality) if record_ids else None
        aliases = sorted(
            set(existing.location_aliases)
            | set(candidate.location_aliases)
            | {value for value in record_ids if value != preferred_record_id}
        )
        policy_rank = {
            "public": 0,
            "metadata_only": 1,
            "cite_and_summarize_only": 2,
            "manual_review_required": 3,
            "private_evidence_only": 4,
            "existing_public_artifact": 0,
        }
        public_policy = max(
            [existing.public_policy, candidate.public_policy],
            key=lambda value: policy_rank.get(value, 0),
        )
        merged = existing.model_copy(
            update={
                "source_record_id": preferred_record_id,
                "source_work_id": existing.source_work_id or candidate.source_work_id,
                "canonical_url": existing.canonical_url or candidate.canonical_url,
                "title": existing.title or candidate.title,
                "observed_at": max(
                    [value for value in (existing.observed_at, candidate.observed_at) if value],
                    default=None,
                ),
                "content_hash": existing.content_hash or candidate.content_hash,
                "immutable": existing.immutable or candidate.immutable,
                "public_policy": public_policy,
                "location_aliases": aliases,
            }
        )
        self.snapshots[candidate.source_snapshot_id] = (
            SourceSnapshot.model_validate(merged.model_dump(by_alias=True))
        )

    def add_mirror_relationships(self) -> None:
        by_work: dict[str, list[SourceSnapshot]] = defaultdict(list)
        for snapshot in self.snapshots.values():
            if snapshot.source_work_id:
                by_work[snapshot.source_work_id].append(snapshot)
        for source_work_id, snapshots in sorted(by_work.items()):
            distinct_sources = {row.source_id for row in snapshots}
            if len(distinct_sources) < 2:
                continue
            for left, right in combinations(sorted(snapshots, key=lambda row: row.source_snapshot_id), 2):
                if left.source_id == right.source_id:
                    continue
                relationship_id = "relationship:" + sha256_text(
                    f"mirrors:{left.source_snapshot_id}:{right.source_snapshot_id}"
                )[:24]
                self.relationships[relationship_id] = KnowledgeRelationship(
                    schema="rock-kb-knowledge-relationship-v1",
                    relationship_id=relationship_id,
                    from_id=left.source_snapshot_id,
                    to_id=right.source_snapshot_id,
                    relation="mirrors",
                    decision="accept",
                    confidence="high",
                    rationale=(
                        f"Both locators identify the same source work ({source_work_id}); "
                        "they are alternate distributions, not independent corroboration."
                    ),
                )

    def bundle(self) -> CanonicalKnowledgeBundle:
        return CanonicalKnowledgeBundle(
            schema="rock-kb-canonical-knowledge-bundle-v1",
            source_snapshots=sorted(self.snapshots.values(), key=lambda row: row.source_snapshot_id),
            source_units=sorted(self.units.values(), key=lambda row: row.source_unit_id),
            generation_activities=sorted(
                self.activities.values(),
                key=lambda row: row.generation_activity_id,
            ),
            knowledge_units=sorted(self.knowledge.values(), key=lambda row: row.knowledge_unit_id),
            identities=sorted(
                self.identity_resolver.identities.values(),
                key=lambda row: row.knowledge_unit_id,
            ),
            identity_migrations=sorted(
                self.identity_resolver.migrations_resolving_to(
                    set(self.knowledge)
                ),
                key=lambda row: row.migration_id,
            ),
            evidence_links=sorted(self.links.values(), key=lambda row: row.evidence_link_id),
            relationships=sorted(self.relationships.values(), key=lambda row: row.relationship_id),
        )


def projection_summary(
    bundle: CanonicalKnowledgeBundle,
    *,
    all_search_rows: list[dict[str, Any]],
    supported_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    distilled_rows: list[dict[str, Any]],
    source_native_artifact_count: int = 0,
    legacy_migration_count: int = 0,
    artifact_migration_count: int = 0,
    reviewed_cross_source_artifact_count: int = 0,
) -> dict[str, Any]:
    distilled_groups = defaultdict(list)
    for row in distilled_rows:
        statement = str(row.get("distilled_claim") or row.get("generated_distilled_claim") or "")
        if statement:
            distilled_groups[canonical_claim_fingerprint(statement, str(row.get("claim_type") or "other"))].append(row)
    knowledge_kind_counts = Counter(row.knowledge_type for row in bundle.knowledge_units)
    ingestion_mode_counts = Counter(row.ingestion_mode for row in bundle.knowledge_units)
    direct_database_units = [
        row
        for row in bundle.knowledge_units
        if row.knowledge_type == "claim"
        and "unrestricted direct database access" in row.retrieval_text.lower()
    ]
    regression = {}
    if direct_database_units:
        item = direct_database_units[0]
        legacy_distilled = [value for value in item.legacy_ids if value.startswith("distilled-claim:")]
        payload = item.payload if isinstance(item.payload, dict) else {}
        regression = {
            "knowledge_unit_id": item.knowledge_unit_id,
            "canonical_unit_count": len(direct_database_units),
            "legacy_distilled_claim_count": len(legacy_distilled),
            "approved_claim_count": len(payload.get("approved_claims") or []),
            "concept_facets": item.concept_facets,
            "source_unit_count": len(item.source_unit_ids),
            "source_work_ids": item.source_work_ids,
            "independent_source_work_count": len(item.source_work_ids),
        }
    return {
        "schema": "rock-kb-canonical-knowledge-shadow-summary-v1",
        "generated_at": generated_at_iso(),
        "mode": "shadow_only",
        "public_retrieval_changed": False,
        "input": {
            "all_search_rows": len(all_search_rows),
            "supported_search_rows": len(supported_rows),
            "approved_claim_rows": len(claim_rows),
            "distilled_claim_rows": len(distilled_rows),
            "distilled_claim_groups": len(distilled_groups),
            "distilled_duplicate_rows_removed": len(distilled_rows) - len(distilled_groups),
            "source_native_reviewed_artifacts": source_native_artifact_count,
            "reviewed_legacy_migrations": legacy_migration_count,
            "reviewed_source_native_artifact_migrations": (
                artifact_migration_count
            ),
            "reviewed_cross_source_artifacts": (
                reviewed_cross_source_artifact_count
            ),
        },
        "output": {
            "source_snapshots": len(bundle.source_snapshots),
            "source_units": len(bundle.source_units),
            "generation_activities": len(bundle.generation_activities),
            "knowledge_units": len(bundle.knowledge_units),
            "identity_registry_rows": len(bundle.identities),
            "identity_migrations": len(bundle.identity_migrations),
            "identity_migration_types": dict(
                sorted(
                    Counter(
                        row.migration_type
                        for row in bundle.identity_migrations
                    ).items()
                )
            ),
            "content_fallback_identities": sum(
                1 for row in bundle.identities if row.identity_basis == "content_fallback"
            ),
            "evidence_links": len(bundle.evidence_links),
            "relationships": len(bundle.relationships),
            "knowledge_types": dict(sorted(knowledge_kind_counts.items())),
            "ingestion_modes": dict(sorted(ingestion_mode_counts.items())),
            "source_family_contracts": source_family_contract_summary(
                [
                    row
                    for row in supported_rows
                    if str(row.get("kind") or "") != "claim"
                ]
            ),
            "mirror_relationships": sum(1 for row in bundle.relationships if row.relation == "mirrors"),
        },
        "regressions": {
            "direct_database_access": regression,
        },
    }


def public_claim_payload(raw: dict[str, Any]) -> dict[str, Any]:
    return Claim.model_validate(raw).public_dump()


def source_refs_for_search_row(row: dict[str, Any]) -> list[dict[str, Any]]:
    payload = row.get("payload") or {}
    refs = [dict(ref) for ref in payload.get("source_refs") or [] if isinstance(ref, dict)]
    if refs:
        return refs
    url = https_url(row.get("url"))
    if not url and not row.get("source_id"):
        return []
    return [
        {
            "source_id": row.get("source_id"),
            "source_record_id": search_row_source_record_id(row),
            "url": url,
            "title": row.get("title"),
        }
    ]


def search_row_source_record_id(row: dict[str, Any]) -> str:
    payload = row.get("payload") or {}
    for key in (
        "source_record_id",
        "issue_id",
        "idea_id",
        "recipe_id",
        "contribution_id",
        "id",
    ):
        if payload.get(key):
            return str(payload[key])
    return str(row.get("id") or "")


def claim_source_locator(ref: dict[str, Any], source_record_id: str, url: str | None) -> SourceLocator:
    timestamp_seconds = numeric_value(ref.get("timestamp_seconds"))
    timestamp = str(ref.get("timestamp") or "").strip()
    if timestamp_seconds is not None or timestamp:
        return SourceLocator(
            kind="timestamp",
            value=timestamp or format_seconds(timestamp_seconds or 0),
            url=https_url(ref.get("source_timestamp_url")) or url,
            timestamp_seconds=timestamp_seconds,
        )
    return SourceLocator(
        kind="record",
        value=source_record_id or url or "source-record",
        url=url,
    )


def search_row_locator(
    row: dict[str, Any],
    ref: dict[str, Any],
    source_record_id: str,
    url: str | None,
) -> SourceLocator:
    payload = row.get("payload") or {}
    kind = str(row.get("kind") or "")
    if kind == "lava_context" and payload.get("source_file"):
        return SourceLocator(
            kind="source_code_span",
            value=str(payload.get("source_ref") or payload.get("source_symbol") or source_record_id),
            url=url,
            path=str(payload.get("source_file")),
            symbol=str(payload.get("source_symbol") or "") or None,
            line_start=integer_value(payload.get("source_line_start")),
            line_end=integer_value(payload.get("source_line_end")),
        )
    if kind == "rock_issue":
        return SourceLocator(kind="issue", value=str(payload.get("location_id") or source_record_id), url=url)
    if kind == "rock_idea":
        return SourceLocator(kind="idea", value=str(payload.get("idea_id") or source_record_id), url=url)
    if kind == "model_map":
        identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
        return SourceLocator(kind="model", value=str(identity.get("model_slug") or source_record_id), url=url)
    if kind == "recipe":
        return SourceLocator(kind="recipe", value=str(payload.get("recipe_id") or source_record_id), url=url)
    return SourceLocator(kind="record", value=source_record_id or url or "source-record", url=url)


def source_unit_kind(kind: str, locator: SourceLocator) -> str:
    if locator.kind == "source_code_span":
        return "source_code_span"
    return {
        "rock_issue": "issue_observation",
        "rock_idea": "idea_observation",
        "model_map": "model_map_observation",
        "recipe": "recipe_release",
        "community_contribution": "contribution_record",
        "source_summary": "document",
        "lava_context": "source_code_span",
    }.get(kind, "other")


def source_snapshot_id(source_id: str, source_record_id: str, url: str | None, content_hash: str | None) -> str:
    del content_hash
    seed = canonical_json(
        {
            "source_id": source_id,
            "source_locator": url or source_record_id,
        }
    )
    return "snapshot:" + sha256_text(seed)[:24]


def source_unit_id(snapshot_id: str, locator: SourceLocator) -> str:
    seed = canonical_json({"snapshot_id": snapshot_id, "locator": locator.model_dump(exclude_none=True)})
    return "unit:" + sha256_text(seed)[:24]


def matching_source_record_id(source_id: str, values: Iterable[Any]) -> str:
    candidates = [str(value) for value in values if value]
    for value in candidates:
        if source_id and value.startswith(f"{source_id}:"):
            return value
    return candidates[0] if len(candidates) == 1 else ""


def source_record_quality(value: str) -> tuple[int, int, str]:
    return (
        0 if value.startswith("media-insight:") else 1,
        1 if ":" in value else 0,
        value,
    )


def public_handling(payload: dict[str, Any]) -> str:
    mode = str(payload.get("public_publish_mode") or "")
    if mode == "public_cite_and_summarize_only":
        return "cite_and_summarize_only"
    if mode == "manual_review_required":
        return "manual_review_required"
    if mode == "private_only":
        return "private_evidence_only"
    license_status = str(payload.get("license_status") or "")
    if license_status == "cite_and_summarize_only":
        return "cite_and_summarize_only"
    if license_status in {"manual_review_required", "unknown"}:
        return "manual_review_required"
    if payload.get("raw_content_policy") == "untrusted_not_republished":
        return "metadata_only"
    return "public"


def search_row_is_immutable(kind: str, payload: dict[str, Any], url: str | None) -> bool:
    if kind == "recipe":
        implementation = payload.get("implementation") if isinstance(payload.get("implementation"), dict) else {}
        return bool(re.fullmatch(r"[0-9a-f]{40}", str(implementation.get("commit_sha") or "")))
    if re.fullmatch(r"[0-9a-f]{40}", str(payload.get("source_commit") or "")):
        return True
    return bool(url and re.search(r"/(?:blob|tree)/[0-9a-f]{40}/", url))


def search_row_source_hash(payload: dict[str, Any]) -> str | None:
    for key in ("source_content_hash", "content_hash", "body_sha256"):
        value = valid_sha256(payload.get(key))
        if value:
            return value
    return None


def search_row_review_state(payload: dict[str, Any]) -> str | None:
    for key in ("review_status", "validation_state", "verification_state", "evidence_state"):
        if payload.get(key):
            return str(payload[key])
    return None


def search_row_versions(payload: dict[str, Any]) -> list[str]:
    values = []
    for key in ("rock_versions", "versions", "tested_rock_versions"):
        value = payload.get(key)
        values.extend(value if isinstance(value, list) else [value] if value else [])
    compatibility = payload.get("compatibility") if isinstance(payload.get("compatibility"), dict) else {}
    tested = compatibility.get("tested_rock_versions")
    values.extend(tested if isinstance(tested, list) else [tested] if tested else [])
    return sorted({str(value) for value in values if value})


def search_row_version_scope(payload: dict[str, Any]) -> str | None:
    versions = search_row_versions(payload)
    if versions:
        return "scoped"
    return str(payload.get("version_scope_status") or "") or None


def claim_version_scope(claim_rows: list[dict[str, Any]]) -> str:
    values = {
        str((row.get("payload") or {}).get("version_scope_status") or "unprocessed")
        for row in claim_rows
    }
    return "version_independent" if values == {"version_independent"} else "unprocessed"


def highest_ranked(values: Iterable[str], ranks: dict[str, int]) -> str:
    filtered = [value for value in values if value]
    return max(filtered, key=lambda value: (ranks.get(value, -1), value)) if filtered else ""


def assert_public_safe(value: Any, path: str = "payload") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_PAYLOAD_KEYS and item not in (None, "", [], {}):
                raise ValueError(f"{path}.{key} contains private or secret material")
            assert_public_safe(item, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            assert_public_safe(item, f"{path}[{index}]")
        return
    if isinstance(value, str) and any(pattern.search(value) for pattern in PRIVATE_VALUE_PATTERNS):
        raise ValueError(f"{path} contains a private path or credential-like value")


def valid_sha256(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    return text if re.fullmatch(r"[0-9a-f]{64}", text) else None


def https_url(value: Any) -> str | None:
    text = str(value or "").strip()
    return text if text.startswith("https://") else None


def first_value(payload: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        if payload.get(key):
            return str(payload[key])
    return None


def numeric_value(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip()) if str(value or "").strip() else None
    except ValueError:
        return None


def integer_value(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def format_seconds(value: float) -> str:
    seconds = max(0, int(value))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
