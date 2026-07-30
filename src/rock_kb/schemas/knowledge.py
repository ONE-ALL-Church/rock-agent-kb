from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from .base import KBRecord, Private


PublicHandling = Literal[
    "public",
    "cite_and_summarize_only",
    "private_evidence_only",
    "metadata_only",
    "existing_public_artifact",
    "manual_review_required",
]
SourceUnitKind = Literal[
    "document",
    "document_section",
    "media_segment",
    "source_code_span",
    "issue_observation",
    "idea_observation",
    "model_map_observation",
    "recipe_release",
    "contribution_record",
    "existing_knowledge_projection",
    "other",
]
KnowledgeType = Literal[
    "claim",
    "concept",
    "answer",
    "task_card",
    "troubleshooting_node",
    "recipe",
    "lava_context",
    "rock_issue",
    "rock_idea",
    "model_map",
    "community_contribution",
    "source_summary",
    "other",
]
EvidenceRelation = Literal["supports", "qualifies", "contradicts", "supersedes", "derived_from"]
RelationshipType = Literal[
    "related_to",
    "corroborates",
    "mirrors",
    "contradicts",
    "qualifies",
    "supersedes",
    "implements",
    "affects",
    "references",
]
RelationshipDecision = Literal["accept", "reject", "replace", "needs_review"]
Confidence = Literal["low", "medium", "high", "needs_review"]
IdentityBasis = Literal[
    "content_fallback",
    "legacy_anchor",
    "source_identity",
    "registry_alias",
    "registry_merge",
]
IdentityMigrationType = Literal[
    "content_addressed_to_registry",
    "identity_merge",
    "identity_reassignment",
]
PublicAliasSource = Literal[
    "existing_public_result_id",
    "existing_public_legacy_id",
]


class SourceLocator(KBRecord):
    kind: Literal[
        "record",
        "section",
        "timestamp",
        "source_code_span",
        "issue",
        "idea",
        "model",
        "property",
        "recipe",
        "other",
    ]
    value: str = Field(min_length=1, max_length=500)
    url: str | None = Field(default=None, max_length=2000)
    path: str | None = Field(default=None, max_length=500)
    symbol: str | None = Field(default=None, max_length=300)
    timestamp_seconds: float | None = Field(default=None, ge=0)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)

    @field_validator("url")
    @classmethod
    def validate_public_url(cls, value: str | None) -> str | None:
        if value and not value.startswith("https://"):
            raise ValueError("source locator URLs must use https")
        return value

    @field_validator("path")
    @classmethod
    def validate_public_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.replace("\\", "/").strip()
        if normalized.startswith("/") or ".." in normalized.split("/"):
            raise ValueError("source locator paths must be public-safe relative paths")
        return normalized

    @model_validator(mode="after")
    def validate_line_range(self) -> "SourceLocator":
        if self.line_end is not None and self.line_start is None:
            raise ValueError("line_end requires line_start")
        if self.line_start is not None and self.line_end is not None and self.line_end < self.line_start:
            raise ValueError("line_end must be greater than or equal to line_start")
        return self


class SourceSnapshot(KBRecord):
    schema_: Literal["rock-kb-source-snapshot-v1"] = Field(alias="schema")
    source_snapshot_id: str = Field(min_length=3, max_length=240)
    source_id: str = Field(min_length=1, max_length=160)
    source_record_id: str | None = Field(default=None, max_length=240)
    source_work_id: str | None = Field(default=None, max_length=240)
    canonical_url: str | None = Field(default=None, max_length=2000)
    title: str | None = Field(default=None, max_length=500)
    observed_at: str | None = Field(default=None, max_length=80)
    content_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    immutable: bool = False
    authority_tier: str = Field(min_length=1, max_length=80)
    public_policy: PublicHandling
    derivation: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
    location_aliases: list[str] = Field(default_factory=list, max_length=5000)

    @field_validator("canonical_url")
    @classmethod
    def validate_canonical_url(cls, value: str | None) -> str | None:
        if value and not value.startswith("https://"):
            raise ValueError("source snapshot URLs must use https")
        return value

    @model_validator(mode="after")
    def require_locator(self) -> "SourceSnapshot":
        if not self.source_record_id and not self.canonical_url:
            raise ValueError("source snapshot requires source_record_id or canonical_url")
        return self


class SourceUnit(KBRecord):
    schema_: Literal["rock-kb-source-unit-v1"] = Field(alias="schema")
    source_unit_id: str = Field(min_length=3, max_length=240)
    source_snapshot_id: str = Field(min_length=3, max_length=240)
    unit_kind: SourceUnitKind
    locator: SourceLocator
    context: str = Field(default="", max_length=1000)
    text: str | None = Private(default=None)
    public_summary: str | None = Field(default=None, max_length=1500)
    normalized_content_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    required_public_handling: PublicHandling


class EvidenceLink(KBRecord):
    schema_: Literal["rock-kb-evidence-link-v1"] = Field(alias="schema")
    evidence_link_id: str = Field(min_length=3, max_length=240)
    knowledge_unit_id: str = Field(min_length=3, max_length=240)
    source_unit_id: str = Field(min_length=3, max_length=240)
    relation: EvidenceRelation = "supports"
    evidence_summary: str = Field(min_length=1, max_length=1500)
    authority_tier: str = Field(min_length=1, max_length=80)
    confidence: Confidence = "medium"
    independence_group: str | None = Field(default=None, max_length=240)
    needs_review: bool = False


class KnowledgeUnit(KBRecord):
    schema_: Literal["rock-kb-knowledge-unit-v1"] = Field(alias="schema")
    knowledge_unit_id: str = Field(min_length=3, max_length=240)
    knowledge_type: KnowledgeType
    title: str = Field(min_length=1, max_length=500)
    retrieval_text: str = Field(min_length=1, max_length=100_000)
    concept_facets: list[str] = Field(default_factory=list, max_length=100)
    topic_facets: list[str] = Field(default_factory=list, max_length=100)
    authority_tiers: list[str] = Field(default_factory=list, max_length=30)
    claim_tier: str | None = Field(default=None, max_length=80)
    review_state: str | None = Field(default=None, max_length=100)
    rock_versions: list[str] = Field(default_factory=list, max_length=100)
    version_scope_status: str | None = Field(default=None, max_length=80)
    source_unit_ids: list[str] = Field(default_factory=list, max_length=500)
    source_work_ids: list[str] = Field(default_factory=list, max_length=100)
    legacy_ids: list[str] = Field(default_factory=list, max_length=500)
    payload_schema: str | None = Field(default=None, max_length=160)
    payload: dict[str, Any]
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_unique_facets_and_references(self) -> "KnowledgeUnit":
        for field_name in (
            "concept_facets",
            "topic_facets",
            "authority_tiers",
            "rock_versions",
            "source_unit_ids",
            "source_work_ids",
            "legacy_ids",
        ):
            values = getattr(self, field_name)
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} values must be unique")
        if self.knowledge_unit_id in self.legacy_ids:
            raise ValueError("legacy_ids must not include knowledge_unit_id")
        return self


class KnowledgeIdentity(KBRecord):
    schema_: Literal["rock-kb-knowledge-identity-v1"] = Field(alias="schema")
    knowledge_unit_id: str = Field(min_length=3, max_length=240)
    knowledge_type: KnowledgeType
    identity_key: str = Field(min_length=3, max_length=500)
    identity_basis: IdentityBasis
    aliases: list[str] = Field(default_factory=list, max_length=1000)
    content_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_aliases(self) -> "KnowledgeIdentity":
        if len(self.aliases) != len(set(self.aliases)):
            raise ValueError("identity aliases must be unique")
        if self.knowledge_unit_id in self.aliases:
            raise ValueError("identity aliases must not include knowledge_unit_id")
        return self


class KnowledgeIdentityMigration(KBRecord):
    schema_: Literal["rock-kb-knowledge-identity-migration-v1"] = Field(alias="schema")
    migration_id: str = Field(min_length=3, max_length=240)
    from_knowledge_unit_id: str = Field(min_length=3, max_length=240)
    to_knowledge_unit_id: str = Field(min_length=3, max_length=240)
    migration_type: IdentityMigrationType
    reason: str = Field(min_length=1, max_length=1500)
    matched_aliases: list[str] = Field(default_factory=list, max_length=1000)
    review_state: Literal["generated_needs_reviewer_approval", "reviewer_approved"] = (
        "generated_needs_reviewer_approval"
    )

    @model_validator(mode="after")
    def validate_migration(self) -> "KnowledgeIdentityMigration":
        if self.from_knowledge_unit_id == self.to_knowledge_unit_id:
            raise ValueError("identity migrations must change the knowledge unit ID")
        if len(self.matched_aliases) != len(set(self.matched_aliases)):
            raise ValueError("matched_aliases values must be unique")
        return self


class PublicResultAlias(KBRecord):
    schema_: Literal["rock-kb-public-result-alias-v1"] = Field(alias="schema")
    alias_id: str = Field(min_length=3, max_length=500)
    canonical_knowledge_unit_id: str = Field(min_length=3, max_length=240)
    knowledge_type: KnowledgeType
    source: PublicAliasSource
    compatibility_status: Literal["required"] = "required"

    @model_validator(mode="after")
    def validate_alias(self) -> "PublicResultAlias":
        if self.alias_id == self.canonical_knowledge_unit_id:
            raise ValueError("public result aliases must change the result ID")
        return self


class CanonicalIdentityBaselineManifest(KBRecord):
    schema_: Literal["rock-kb-canonical-identity-baseline-manifest-v1"] = Field(
        alias="schema"
    )
    baseline_version: Literal["v1"] = "v1"
    status: Literal["shadow_only"] = "shadow_only"
    public_retrieval_changed: Literal[False] = False
    identity_registry_path: str = Field(min_length=1, max_length=500)
    public_result_aliases_path: str = Field(min_length=1, max_length=500)
    identity_count: int = Field(ge=0)
    public_alias_count: int = Field(ge=0)
    existing_result_id_alias_count: int = Field(ge=0)
    existing_legacy_id_alias_count: int = Field(ge=0)
    canonical_ids_already_public_count: int = Field(ge=0)
    knowledge_type_counts: dict[str, int] = Field(default_factory=dict)
    identity_registry_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    public_result_aliases_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    public_search_projection_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    unpublished_pilot_migrations_included: Literal[False] = False

    @model_validator(mode="after")
    def validate_counts(self) -> "CanonicalIdentityBaselineManifest":
        if (
            self.existing_result_id_alias_count
            + self.existing_legacy_id_alias_count
            != self.public_alias_count
        ):
            raise ValueError("public alias source counts must equal public_alias_count")
        if sum(self.knowledge_type_counts.values()) != self.identity_count:
            raise ValueError("knowledge type counts must equal identity_count")
        return self


class KnowledgeRelationship(KBRecord):
    schema_: Literal["rock-kb-knowledge-relationship-v1"] = Field(alias="schema")
    relationship_id: str = Field(min_length=3, max_length=240)
    from_id: str = Field(min_length=3, max_length=240)
    to_id: str = Field(min_length=3, max_length=240)
    relation: RelationshipType
    decision: RelationshipDecision
    confidence: Confidence
    rationale: str = Field(min_length=1, max_length=1500)
    evidence_source_unit_ids: list[str] = Field(default_factory=list, max_length=100)
    replacement_relation: RelationshipType | None = None
    reviewed_at: str | None = Field(default=None, max_length=80)

    @model_validator(mode="after")
    def validate_decision(self) -> "KnowledgeRelationship":
        if self.from_id == self.to_id:
            raise ValueError("knowledge relationships cannot be self-referential")
        if self.decision == "replace" and self.replacement_relation is None:
            raise ValueError("replace decisions require replacement_relation")
        if self.decision != "replace" and self.replacement_relation is not None:
            raise ValueError("replacement_relation is only valid for replace decisions")
        if len(self.evidence_source_unit_ids) != len(set(self.evidence_source_unit_ids)):
            raise ValueError("evidence_source_unit_ids values must be unique")
        return self


class CanonicalKnowledgeBundle(KBRecord):
    schema_: Literal["rock-kb-canonical-knowledge-bundle-v1"] = Field(alias="schema")
    source_snapshots: list[SourceSnapshot] = Field(default_factory=list)
    source_units: list[SourceUnit] = Field(default_factory=list)
    knowledge_units: list[KnowledgeUnit] = Field(default_factory=list)
    identities: list[KnowledgeIdentity] = Field(default_factory=list)
    identity_migrations: list[KnowledgeIdentityMigration] = Field(default_factory=list)
    evidence_links: list[EvidenceLink] = Field(default_factory=list)
    relationships: list[KnowledgeRelationship] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_references(self) -> "CanonicalKnowledgeBundle":
        snapshots = _unique_by_id(self.source_snapshots, "source_snapshot_id")
        units = _unique_by_id(self.source_units, "source_unit_id")
        knowledge = _unique_by_id(self.knowledge_units, "knowledge_unit_id")
        identities = _unique_by_id(self.identities, "knowledge_unit_id")
        _unique_by_id(self.identity_migrations, "migration_id")
        _unique_by_id(self.evidence_links, "evidence_link_id")
        _unique_by_id(self.relationships, "relationship_id")

        if identities and set(identities) != set(knowledge):
            missing = sorted(set(knowledge) - set(identities))
            unknown = sorted(set(identities) - set(knowledge))
            raise ValueError(
                "identity registry must cover exactly the knowledge units "
                f"(missing={missing[:3]}, unknown={unknown[:3]})"
            )

        identity_keys: dict[str, str] = {}
        identity_aliases: dict[str, str] = {}
        for identity in self.identities:
            existing_id = identity_keys.get(identity.identity_key)
            if existing_id and existing_id != identity.knowledge_unit_id:
                raise ValueError(
                    f"identity key maps to multiple knowledge units: {identity.identity_key}"
                )
            identity_keys[identity.identity_key] = identity.knowledge_unit_id
            for alias in identity.aliases:
                existing_id = identity_aliases.get(alias)
                if existing_id and existing_id != identity.knowledge_unit_id:
                    raise ValueError(
                        f"identity alias maps to multiple knowledge units: {alias}"
                    )
                identity_aliases[alias] = identity.knowledge_unit_id

        historical_ids = {
            migration.from_knowledge_unit_id for migration in self.identity_migrations
        }
        migration_targets: dict[str, str] = {}
        for migration in self.identity_migrations:
            if (
                migration.to_knowledge_unit_id not in knowledge
                and migration.to_knowledge_unit_id not in historical_ids
            ):
                raise ValueError(
                    f"identity migration references unknown target: {migration.migration_id}"
                )
            existing_target = migration_targets.get(
                migration.from_knowledge_unit_id
            )
            if (
                existing_target
                and existing_target != migration.to_knowledge_unit_id
            ):
                raise ValueError(
                    "identity migration source has multiple targets: "
                    f"{migration.from_knowledge_unit_id}"
                )
            migration_targets[migration.from_knowledge_unit_id] = (
                migration.to_knowledge_unit_id
            )
        for historical_id in migration_targets:
            visited: set[str] = set()
            target = historical_id
            while target in migration_targets:
                if target in visited:
                    raise ValueError(
                        f"identity migration cycle detected: {historical_id}"
                    )
                visited.add(target)
                target = migration_targets[target]
            if target not in knowledge:
                raise ValueError(
                    f"identity migration does not resolve to a current unit: {historical_id}"
                )

        for unit in self.source_units:
            if unit.source_snapshot_id not in snapshots:
                raise ValueError(f"source unit references unknown snapshot: {unit.source_snapshot_id}")

        for link in self.evidence_links:
            if link.knowledge_unit_id not in knowledge:
                raise ValueError(f"evidence link references unknown knowledge unit: {link.knowledge_unit_id}")
            source_unit = units.get(link.source_unit_id)
            if source_unit is None:
                raise ValueError(f"evidence link references unknown source unit: {link.source_unit_id}")
            if source_unit.unit_kind == "existing_knowledge_projection":
                raise ValueError("existing knowledge projections cannot be used as primary evidence")

        for item in self.knowledge_units:
            missing = sorted(set(item.source_unit_ids) - set(units))
            if missing:
                raise ValueError(f"knowledge unit references unknown source units: {', '.join(missing)}")

        valid_endpoints = set(snapshots) | set(units) | set(knowledge)
        for relationship in self.relationships:
            if relationship.from_id not in valid_endpoints or relationship.to_id not in valid_endpoints:
                raise ValueError(f"relationship references unknown endpoint: {relationship.relationship_id}")
            missing = sorted(set(relationship.evidence_source_unit_ids) - set(units))
            if missing:
                raise ValueError(f"relationship references unknown evidence units: {', '.join(missing)}")
        return self


def _unique_by_id(rows: list[Any], field_name: str) -> dict[str, Any]:
    by_id: dict[str, Any] = {}
    for row in rows:
        value = str(getattr(row, field_name))
        if value in by_id:
            raise ValueError(f"duplicate {field_name}: {value}")
        by_id[value] = row
    return by_id
