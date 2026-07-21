from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Literal

from pydantic import Field, model_validator

from .base import KBRecord
from .claim import AuthorityTier, ClaimTier, Confidence


IssueValidationState = Literal["reported", "confirmed", "rejected", "withdrawn"]
IssueComponent = Literal["rock_core", "mobile_shell"]
VersionRelationship = Literal[
    "reported_affected",
    "known_affected",
    "first_affected",
    "last_affected",
    "targeted",
    "fixed",
    "first_fixed",
    "known_not_affected",
    "under_investigation",
]
ApplicabilityStatus = Literal[
    "affected",
    "fixed",
    "not_affected",
    "under_investigation",
    "unknown",
]
IssueRiskLevel = Literal["critical", "high", "medium", "low"]

READ_ONLY_SQL_START_PATTERN = re.compile(r"^(?:SELECT|WITH)\b", re.IGNORECASE)
SQL_WRITE_PATTERN = re.compile(
    r"\b(?:INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|TRUNCATE|EXEC(?:UTE)?|CREATE|GRANT|REVOKE|INTO)\b",
    re.IGNORECASE,
)


class RockIssueConceptRoute(KBRecord):
    concept_id: str
    basis: Literal["github_topic_label", "structured_field", "title_keyword", "body_keyword", "repository_default"]
    signal: str


class RockIssueVersionEvidence(KBRecord):
    component: IssueComponent
    relationship: VersionRelationship
    version: str
    normalized_version: str
    version_line: str
    version_scheme: Literal["rock_release", "rock_runtime", "git", "unknown"] = "rock_release"
    validity: Literal["valid", "wildcard", "sentinel", "invalid"] = "valid"
    source_kind: Literal[
        "issue_form",
        "github_label",
        "github_milestone",
        "timeline",
        "release_note",
        "reviewed_enrichment",
    ]
    source_ref: str
    authority_tier: AuthorityTier
    confidence: Confidence
    observed_at: str | None = None


class RockIssueLabel(KBRecord):
    github_node_id: str
    name: str


class RockIssueEvent(KBRecord):
    event_id: str
    event_type: Literal[
        "closed",
        "reopened",
        "labeled",
        "unlabeled",
        "milestoned",
        "demilestoned",
        "referenced",
        "cross_referenced",
        "marked_as_duplicate",
        "transferred",
        "other",
    ]
    occurred_at: str | None = None
    label_github_node_id: str | None = None
    label_name: str | None = None
    milestone_title: str | None = None
    commit_sha: str | None = None
    target_issue_id: str | None = None


class RockIssueMilestone(KBRecord):
    title: str
    state: Literal["open", "closed"]
    url: str


class RockIssueTimelineRelation(KBRecord):
    relation: Literal["references_commit", "closed_by_commit", "cross_references_issue", "duplicate_of"]
    target: str
    occurred_at: str | None = None


class RockIssueReleaseNoteRef(KBRecord):
    record_id: str
    source_id: Literal["rock_core_release_notes", "rock_mobile_release_notes"]
    url: str
    version: str
    module: str | None = None
    summary: str
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class RockIssue(KBRecord):
    schema_: Literal["rock-kb-rock-issue-v1"] = Field(alias="schema")
    issue_id: str
    github_node_id: str
    identity_key: str
    location_id: str
    location_aliases: list[str] = Field(default_factory=list)
    source_id: str
    repository: Literal["SparkDevNetwork/Rock", "SparkDevNetwork/Rock.Mobile-Issues"]
    component: IssueComponent
    number: int = Field(gt=0)
    title: str
    url: str
    state: Literal["open", "closed"]
    state_reason: str | None = None
    validation_state: IssueValidationState
    created_at: str
    updated_at: str
    closed_at: str | None = None
    locked: bool = False
    comment_count: int = Field(default=0, ge=0)
    labels: list[str] = Field(default_factory=list)
    label_count: int = Field(default=0, ge=0)
    labels_truncated: bool = False
    label_records: list[RockIssueLabel] = Field(default_factory=list)
    type_labels: list[str] = Field(default_factory=list)
    status_labels: list[str] = Field(default_factory=list)
    priority_labels: list[str] = Field(default_factory=list)
    topic_labels: list[str] = Field(default_factory=list)
    milestone: RockIssueMilestone | None = None
    native_issue_type: str | None = None
    issue_type: str | None = None
    frequency: str | None = None
    platforms: list[str] = Field(default_factory=list)
    concept_ids: list[str] = Field(min_length=1)
    concept_routes: list[RockIssueConceptRoute] = Field(min_length=1)
    model_map_links: list[str] = Field(default_factory=list)
    version_evidence: list[RockIssueVersionEvidence] = Field(default_factory=list)
    release_note_refs: list[RockIssueReleaseNoteRef] = Field(default_factory=list)
    timeline_relations: list[RockIssueTimelineRelation] = Field(default_factory=list)
    events: list[RockIssueEvent] = Field(default_factory=list)
    timeline_status: Literal["not_fetched", "complete"] = "not_fetched"
    timeline_updated_through: str | None = None
    related_issue_ids: list[str] = Field(default_factory=list)
    linked_commit_shas: list[str] = Field(default_factory=list)
    remediation_state: Literal["none_recorded", "candidate_fix_linked", "fixed_release_recorded"]
    evidence_state: Literal["report_only", "maintainer_triaged", "commit_linked", "fixed_release_recorded"]
    body_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    timeline_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    source_content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    raw_content_policy: Literal["untrusted_not_republished"] = "untrusted_not_republished"
    generation_method: Literal["deterministic_github_api_normalization"] = "deterministic_github_api_normalization"
    authority_tier: AuthorityTier
    claim_tier: ClaimTier = "routing_context_only"
    confidence: Confidence
    needs_live_verification: bool = True

    @model_validator(mode="after")
    def validate_identity_and_routes(self) -> "RockIssue":
        if not self.github_node_id.strip():
            raise ValueError("github_node_id must not be empty")
        expected = f"rock_issue:{self.repository}#{self.number}"
        if self.issue_id != expected:
            raise ValueError(f"issue_id must be {expected}")
        if self.location_id != f"{self.repository}#{self.number}":
            raise ValueError("location_id must match repository and number")
        if self.identity_key != f"github:{self.github_node_id}":
            raise ValueError("identity_key must be based on github_node_id")
        routed = {route.concept_id for route in self.concept_routes}
        if set(self.concept_ids) != routed:
            raise ValueError("concept_ids must exactly match concept_routes")
        if self.location_id in self.location_aliases:
            raise ValueError("location_aliases must not include the current location")
        if len(self.location_aliases) != len(set(self.location_aliases)):
            raise ValueError("location_aliases must be unique")
        if self.label_count < len(self.label_records):
            raise ValueError("label_count must be at least the number of retained label records")
        if self.labels_truncated != (self.label_count > len(self.label_records)):
            raise ValueError("labels_truncated must match label_count and retained label records")
        return self


class RockIssueRangeEvent(KBRecord):
    introduced: str | None = None
    fixed: str | None = None
    last_affected: str | None = None
    limit: str | None = None

    @model_validator(mode="after")
    def require_one_event(self) -> "RockIssueRangeEvent":
        values = [self.introduced, self.fixed, self.last_affected, self.limit]
        if sum(value is not None for value in values) != 1:
            raise ValueError("range event must set exactly one boundary")
        return self


class RockIssueVersionRange(KBRecord):
    events: list[RockIssueRangeEvent] = Field(min_length=1)


class RockIssueApplicabilityAssertion(KBRecord):
    assertion_id: str
    component: IssueComponent
    version_scheme: Literal["rock_release", "rock_runtime", "git"]
    release_track: str | None = None
    context: dict[str, str] = Field(default_factory=dict)
    versions: list[str] = Field(default_factory=list)
    ranges: list[RockIssueVersionRange] = Field(default_factory=list)
    status: ApplicabilityStatus
    justification_code: str | None = None
    justification: str | None = None
    fix_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(min_length=1)
    authority_tier: AuthorityTier
    claim_tier: ClaimTier
    confidence: Confidence
    assessed_at: str
    review_due_at: str | None = None

    @model_validator(mode="after")
    def validate_status_evidence(self) -> "RockIssueApplicabilityAssertion":
        if not self.versions and not self.ranges:
            raise ValueError("applicability assertion requires versions or ranges")
        if self.status == "not_affected" and not (self.justification_code and self.justification):
            raise ValueError("not_affected assertion requires a coded justification")
        if self.status == "fixed" and not self.fix_refs:
            raise ValueError("fixed assertion requires a fix reference")
        return self


class RockIssueProfileRequirement(KBRecord):
    field: Literal["platforms", "capabilities", "configurations"]
    operator: Literal["contains_any", "contains_all", "contains_none"]
    values: list[str] = Field(min_length=1, max_length=20)

    @model_validator(mode="after")
    def validate_values(self) -> "RockIssueProfileRequirement":
        normalized = []
        for value in self.values:
            value = value.strip()
            if not value or len(value) > 80 or not re.fullmatch(r"[A-Za-z0-9._ -]+", value):
                raise ValueError("profile requirement values must be bounded public identifiers")
            normalized.append(value.lower())
        if len(normalized) != len(set(normalized)):
            raise ValueError("profile requirement values must be unique")
        return self


class RockIssueRiskAssessment(KBRecord):
    level: IssueRiskLevel
    rationale: str = Field(min_length=1, max_length=700)
    evidence_refs: list[str] = Field(min_length=1, max_length=20)
    assessed_at: str

    @model_validator(mode="after")
    def validate_assessed_at(self) -> "RockIssueRiskAssessment":
        try:
            parsed = datetime.fromisoformat(self.assessed_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("risk assessed_at must be an RFC 3339 timestamp") from exc
        if parsed.tzinfo is None:
            raise ValueError("risk assessed_at must include a timezone")
        if parsed.astimezone(timezone.utc) > datetime.now(timezone.utc) + timedelta(minutes=5):
            raise ValueError("risk assessed_at cannot be in the future")
        if any(len(value) > 500 for value in self.evidence_refs):
            raise ValueError("risk evidence references must be at most 500 characters")
        return self


class RockIssueVerificationStep(KBRecord):
    step_id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]{0,79}$")
    title: str = Field(min_length=1, max_length=160)
    method: Literal[
        "version_check",
        "source_revision_check",
        "configuration_check",
        "read_only_sql",
        "read_only_api",
        "ui_observation",
        "log_review",
    ]
    instructions: str = Field(min_length=1, max_length=1000)
    probe: str | None = Field(default=None, max_length=2000)
    expected_if_affected: str = Field(min_length=1, max_length=700)
    expected_if_unaffected: str = Field(min_length=1, max_length=700)
    evidence_to_record: list[str] = Field(default_factory=list, max_length=10)
    requires_privileged_access: bool = False
    mutation_risk: Literal["none"] = "none"

    @model_validator(mode="after")
    def enforce_read_only_probe(self) -> "RockIssueVerificationStep":
        if any(len(value) > 160 for value in self.evidence_to_record):
            raise ValueError("verification evidence labels must be at most 160 characters")

        if self.method == "read_only_sql":
            if not self.probe:
                raise ValueError("read_only_sql verification steps require a probe")
            sql = self.probe.strip()
            if not READ_ONLY_SQL_START_PATTERN.match(sql):
                raise ValueError("read_only_sql probes must begin with SELECT or WITH")
            if SQL_WRITE_PATTERN.search(sql):
                raise ValueError("read_only_sql probes may not contain write-capable SQL")
            if ";" in sql.rstrip(";"):
                raise ValueError("read_only_sql probes must contain exactly one statement")

        return self


class RockIssueVerificationPlaybook(KBRecord):
    goal: str = Field(min_length=1, max_length=700)
    prerequisites: list[str] = Field(default_factory=list, max_length=10)
    steps: list[RockIssueVerificationStep] = Field(min_length=1, max_length=12)
    limitations: list[str] = Field(default_factory=list, max_length=10)
    production_safe: Literal[True] = True

    @model_validator(mode="after")
    def validate_bounded_guidance(self) -> "RockIssueVerificationPlaybook":
        if any(len(value) > 500 for value in self.prerequisites):
            raise ValueError("verification prerequisites must be at most 500 characters")
        if any(len(value) > 700 for value in self.limitations):
            raise ValueError("verification limitations must be at most 700 characters")
        step_ids = [step.step_id for step in self.steps]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("verification step IDs must be unique within a playbook")
        return self


class RockIssueReviewedEnrichment(KBRecord):
    schema_: Literal["rock-kb-rock-issue-enrichment-v1"] = Field(alias="schema")
    enrichment_id: str = Field(pattern=r"^rock_issue_enrichment:[A-Za-z0-9._:/#-]+$", max_length=240)
    issue_id: str = Field(pattern=r"^rock_issue:SparkDevNetwork/Rock(?:\.Mobile-Issues)?#\d+$", max_length=160)
    diagnosis_status: Literal["hypothesis", "source_supported", "maintainer_confirmed"]
    diagnosis_summary: str = Field(min_length=1, max_length=1200)
    workaround_summaries: list[str] = Field(default_factory=list, max_length=20)
    verification_playbook: RockIssueVerificationPlaybook | None = None
    applicability: list[RockIssueApplicabilityAssertion] = Field(default_factory=list)
    applicability_requirements: list[RockIssueProfileRequirement] = Field(default_factory=list, max_length=20)
    risk: RockIssueRiskAssessment | None = None
    source_refs: list[str] = Field(min_length=1, max_length=30)
    agent_run_ids: list[str] = Field(default_factory=list, max_length=20)
    authority_tier: AuthorityTier = "community-reviewed"
    claim_tier: ClaimTier
    confidence: Confidence
    review_status: Literal["redaction_reviewed", "approved_for_public_distillation"]
    reviewer: str = Field(min_length=1, max_length=120)
    issue_updated_at: str
    reviewed_at: str
    redaction_attestation: Literal[True]
    license_attestation: Literal[True]
    source_path: str | None = None

    @model_validator(mode="after")
    def validate_bounded_public_text(self) -> "RockIssueReviewedEnrichment":
        timestamps: dict[str, datetime] = {}
        for field_name in ("issue_updated_at", "reviewed_at"):
            raw = getattr(self, field_name)
            try:
                parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"{field_name} must be an RFC 3339 timestamp") from exc
            if parsed.tzinfo is None:
                raise ValueError(f"{field_name} must include a timezone")
            timestamps[field_name] = parsed.astimezone(timezone.utc)
        if timestamps["issue_updated_at"] > timestamps["reviewed_at"]:
            raise ValueError("issue_updated_at cannot be later than reviewed_at")
        if timestamps["reviewed_at"] > datetime.now(timezone.utc) + timedelta(minutes=5):
            raise ValueError("reviewed_at cannot be in the future")
        if any(len(value) > 800 for value in self.workaround_summaries):
            raise ValueError("workaround summaries must be at most 800 characters")
        if any(len(value) > 500 for value in self.source_refs):
            raise ValueError("source references must be at most 500 characters")
        if any(len(value) > 160 for value in self.agent_run_ids):
            raise ValueError("agent run IDs must be at most 160 characters")
        requirement_identities = [
            (
                requirement.field,
                requirement.operator,
                tuple(sorted(value.strip().lower() for value in requirement.values)),
            )
            for requirement in self.applicability_requirements
        ]
        if len(requirement_identities) != len(set(requirement_identities)):
            raise ValueError("applicability requirements must be unique")
        if self.risk:
            if any(reference not in self.source_refs for reference in self.risk.evidence_refs):
                raise ValueError("risk evidence references must also appear in source_refs")
            risk_assessed_at = datetime.fromisoformat(self.risk.assessed_at.replace("Z", "+00:00")).astimezone(timezone.utc)
            if risk_assessed_at > timestamps["reviewed_at"]:
                raise ValueError("risk assessed_at cannot be later than reviewed_at")
        if self.diagnosis_status == "hypothesis" and self.claim_tier != "routing_context_only":
            raise ValueError("hypothesis enrichments must remain routing_context_only")
        if self.diagnosis_status != "hypothesis" and self.claim_tier == "routing_context_only":
            raise ValueError("supported enrichments must use a source-backed claim tier")
        return self


class RockIssueWorkerFinding(KBRecord):
    statement: str = Field(min_length=1, max_length=600)
    classification: Literal[
        "reporter_observation",
        "official_metadata",
        "source_supported",
        "live_observation",
        "hypothesis",
    ]
    evidence_refs: list[str] = Field(min_length=1, max_length=20)
    confidence: Confidence


class RockIssueWorkerTest(KBRecord):
    name: str = Field(min_length=1, max_length=160)
    outcome: Literal["pass", "fail", "inconclusive", "not_run"]
    evidence_ref: str | None = Field(default=None, max_length=500)
    notes: str = Field(default="", max_length=600)


class RockIssueProposedApplicability(KBRecord):
    component: IssueComponent
    versions: list[str] = Field(min_length=1, max_length=20)
    status: ApplicabilityStatus
    evidence_refs: list[str] = Field(min_length=1, max_length=20)
    confidence: Confidence


class RockIssueProposedWorkaround(KBRecord):
    summary: str = Field(min_length=1, max_length=600)
    evidence_refs: list[str] = Field(min_length=1, max_length=20)
    risk: Literal["low", "medium", "high", "unknown"] = "unknown"
    requires_write: bool = False


class RockIssueWorkerResult(KBRecord):
    schema_: Literal["rock-kb-rock-issue-worker-result-v1"] = Field(alias="schema")
    run_id: str = Field(min_length=1, max_length=160)
    issue_id: str
    issue_updated_at: str
    task_id: str
    status: Literal["complete", "needs_input", "blocked", "no_op"]
    findings: list[RockIssueWorkerFinding] = Field(default_factory=list, max_length=50)
    tests: list[RockIssueWorkerTest] = Field(default_factory=list, max_length=30)
    proposed_applicability: list[RockIssueProposedApplicability] = Field(default_factory=list, max_length=30)
    proposed_workarounds: list[RockIssueProposedWorkaround] = Field(default_factory=list, max_length=20)
    open_questions: list[str] = Field(default_factory=list, max_length=30)
    confidence: Confidence
    private_output_refs: list[str] = Field(default_factory=list, max_length=20)
