from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .concepts import concept_source_records
from .extract import sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REPO_ROOT
from .schemas.source_native_orchestrator import SourceNativeArticleReview
from .source_native import (
    SOURCE_NATIVE_PILOT_DIR,
    SOURCE_NATIVE_PROMPT_ID,
    SOURCE_NATIVE_PROMPT_PATH,
    SOURCE_NATIVE_PROMPT_VERSION,
    SOURCE_NATIVE_SCHEMA_PATH,
    build_source_native_document_candidates,
    sha256_file,
)
from .source_native_migration import (
    SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_ID,
    SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_PATH,
    SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION,
    build_source_native_legacy_migration_inputs,
    merge_source_native_legacy_migration_outputs,
    promote_source_native_legacy_migration,
    write_source_native_legacy_migration_prompt,
    write_source_native_legacy_migration_schema,
)
from .source_native_priority import (
    SOURCE_NATIVE_MIGRATION_PRIORITY_ALGORITHM,
    SOURCE_NATIVE_MIGRATION_PRIORITY_SCHEMA,
    build_source_native_migration_priority_report,
    parse_utc,
)
from .source_native_priority import (
    canonical_json as priority_canonical_json,
)

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised on Windows.
    fcntl = None  # type: ignore[assignment]

BATCH_STATE_SCHEMA = "rock-kb-source-native-migration-batch-state-v1"
BATCH_REVIEW_SCHEMA = "rock-kb-source-native-article-review-v1"
BATCH_COMPARISON_SCHEMA = "rock-kb-migration-batch-comparison-v1"
BATCH_MANIFEST_SCHEMA = "rock-kb-source-native-migration-batch-manifest-v1"
BATCH_REVIEW_VALIDATION_MANIFEST_SCHEMA = (
    "rock-kb-source-native-review-validation-manifest-v1"
)
BATCH_POLICY_VERSION = "1"
RISK_POLICY_VERSION = "3"
RISK_ORDER = {"low": 0, "standard": 1, "high": 2}
HIGH_RISK_TERMS = {
    "authentication",
    "authorization",
    "credential",
    "delete entity",
    "deployment",
    "encryption",
    "execute",
    "financial",
    "firewall",
    "giving",
    "hosting",
    "http response",
    "install",
    "modify entity",
    "password",
    "payment",
    "permission",
    "save",
    "security",
    "server",
    "sql",
    "token",
    "transaction",
    "web request",
    "workflow",
    "write",
}
STANDARD_RISK_TERMS = {
    "branch",
    "debug",
    "legacy",
    "logging",
    "migration",
    "pre-alpha",
    "slingshot",
    "v13",
    "v14",
}
HIGH_RISK_CONCEPTS = {
    "api-integrations",
    "giving-finance",
    "hosting-infrastructure",
    "security-permissions",
    "system-admin-ops",
    "workflows",
}
HYDRATED_HIGH_RISK_TERMS = {
    "authentication",
    "authorization",
    "credential",
    "db transaction",
    "delete entity",
    "execute sql",
    "firewall",
    "http response",
    "modify entity",
    "password",
    "payment",
    "private key",
    "rockinternal",
    "save changes",
    "savechanges",
    "secret",
    "security",
    "web request",
}
HYDRATED_STANDARD_RISK_PATTERNS = (
    (
        "hydrated_internal_api",
        "internal API compatibility warning",
        r"\binternal\s+api\b",
    ),
    (
        "hydrated_near_term_change_warning",
        "near-term change warning",
        (
            r"\bmay\s+(?:be\s+)?change\w*(?:\s+\w+){0,8}\s+"
            r"(?:in\s+)?(?:the\s+)?near[\s-]+term\b"
        ),
    ),
    (
        "hydrated_change_without_notice_warning",
        "change or removal without notice warning",
        r"\b(?:changed|removed)(?:\s+\w+){0,6}\s+without\s+notice\b",
    ),
    (
        "hydrated_compatibility_warning",
        "reduced compatibility guarantee",
        r"\bnot\s+subject(?:\s+\w+){0,8}\s+compatibility\s+standards\b",
    ),
    (
        "hydrated_mutable_release_status",
        "mutable or provisional release status",
        (
            r"\b(?:pre[\s-]?alpha|early[\s-]+access|preview(?:\s+release)?|"
            r"deprecated\s+soon|not\s+(?:yet|currently)\s+"
            r"(?:available|released|supported)|no\s+longer\s+supported|unsupported)\b"
        ),
    ),
)
HYDRATED_POSITIVE_STATUS_PATTERN = (
    r"\b(?:is|are|was|were)\s+(?:now\s+|currently\s+)?"
    r"(?:available|released|supported)\b|\bhas\s+been\s+released\b"
)
HYDRATED_NEGATIVE_STATUS_PATTERN = (
    r"\b(?:is|are|was|were)\s+(?:not|no\s+longer)\s+"
    r"(?:currently\s+)?(?:available|released|supported)\b|"
    r"\b(?:not\s+(?:yet|currently)\s+(?:available|released|supported)|"
    r"no\s+longer\s+supported|unsupported)\b"
)
EPISODE_NUMBER_PATTERN = re.compile(
    r"\bep(?:isode)?\.?[\s:#-]*(\d{1,4})\b",
    re.IGNORECASE,
)
SOURCE_BINDING_STOP_WORDS = {
    "and",
    "article",
    "documentation",
    "developer",
    "for",
    "from",
    "into",
    "rock",
    "that",
    "the",
    "this",
    "with",
}
STABLE_LIST_KEYS = (
    "artifact_key",
    "source_unit_id",
    "legacy_knowledge_unit_id",
    "existing_artifact_id",
    "recommendation_id",
    "verification_request_key",
    "target_artifact_key",
    "label",
    "step_id",
    "order",
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected a JSON object: {path}")
    return value


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _cleanup_runtime_residue(batch_dir: Path) -> None:
    for name in (
        ".batch-state.json.tmp",
        ".comparison-report.json.tmp",
        ".review-validation-manifest.json.tmp",
    ):
        (batch_dir / name).unlink(missing_ok=True)


def _require_review_destination(destination: Path, repo_root: Path) -> Path:
    review_root = (repo_root / "data" / "review").resolve()
    resolved = destination.resolve()
    if not resolved.is_relative_to(review_root):
        raise ValueError(
            "migration batches must be written under the ignored data/review directory"
        )
    return resolved


def _require_review_input(path: Path, repo_root: Path) -> Path:
    resolved = path.resolve()
    review_root = (repo_root / "data" / "review").resolve()
    if not resolved.is_relative_to(review_root):
        raise ValueError(f"private migration input must be under data/review: {path}")
    return resolved


def _git_output(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_state(repo_root: Path, *, require_clean: bool) -> dict[str, Any]:
    commit = _git_output(repo_root, "rev-parse", "HEAD")
    branch = _git_output(repo_root, "branch", "--show-current")
    dirty = _git_output(
        repo_root,
        "status",
        "--porcelain",
        "--untracked-files=no",
    )
    if require_clean and dirty:
        raise ValueError("migration batch preparation requires a clean tracked tree")
    return {
        "base_commit": commit,
        "branch": branch,
        "tracked_tree_clean": not bool(dirty),
    }


@contextmanager
def _batch_lock(repo_root: Path) -> Iterator[None]:
    lock_path = repo_root / "data" / "review" / ".source-native-migration.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        if fcntl is not None:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ValueError(
                    "another source-native migration batch owns the lock"
                ) from exc
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return

        import msvcrt  # pragma: no cover - Windows-only fallback.

        handle.seek(0)
        if not handle.read(1):
            handle.write(b"\0")
            handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise ValueError(
                "another source-native migration batch owns the lock"
            ) from exc
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def _validate_priority_report(report: dict[str, Any]) -> None:
    if report.get("schema") != SOURCE_NATIVE_MIGRATION_PRIORITY_SCHEMA:
        raise ValueError("unsupported source-native migration priority schema")
    if str(report.get("algorithm_version") or "") != (
        SOURCE_NATIVE_MIGRATION_PRIORITY_ALGORITHM
    ):
        raise ValueError("unsupported source-native migration priority algorithm")
    if report.get("status") != "ok":
        raise ValueError("source-native migration priority report is not healthy")
    rows = report.get("rows")
    counts = report.get("counts") or {}
    if not isinstance(rows, list):
        raise TypeError("source-native migration priority rows are missing")
    actionable_count = int(counts.get("actionable_source_count") or 0)
    if actionable_count < 1 or len(rows) != actionable_count:
        raise ValueError(
            "source-native migration priority report is truncated; rebuild it "
            "with a limit covering every actionable record"
        )
    if int(counts.get("unresolved_source_identity_count") or 0):
        raise ValueError("source-native migration priority has unresolved identities")
    if len({str(row.get("source_record_id") or "") for row in rows}) != len(rows):
        raise ValueError("source-native migration priority contains duplicate records")
    if not str(report.get("input_hash") or ""):
        raise ValueError("source-native migration priority input hash is missing")
    if parse_utc(report.get("as_of")) is None:
        raise ValueError("source-native migration priority as_of is invalid")
    hash_payload = {
        "algorithm_version": report.get("algorithm_version"),
        "as_of": report.get("as_of"),
        "score_weights": report.get("score_weights") or {},
        "rows": rows,
        "reviewed_retained": report.get("reviewed_retained_source_record_ids") or [],
        "unresolved_records": [
            str(row.get("source_record_id") or "")
            for row in report.get("unresolved_source_records") or []
        ],
        "source_record_aliases": report.get("source_record_aliases") or [],
        "external_signals": report.get("bounded_external_signals") or [],
    }
    expected_input_hash = sha256_text(priority_canonical_json(hash_payload))
    if report.get("input_hash") != expected_input_hash:
        raise ValueError("source-native migration priority input hash is invalid")


def _risk_text(row: dict[str, Any], record: dict[str, Any]) -> str:
    values = [
        row.get("source_title"),
        row.get("documentation_path"),
        *(row.get("documentation_branches") or []),
        *(row.get("concept_ids") or []),
        record.get("source_title"),
        record.get("canonical_path"),
        record.get("summary"),
        record.get("excerpt"),
    ]
    return " ".join(str(value or "").lower() for value in values)


def _concept_routing_provenance(row: dict[str, Any]) -> tuple[str, bool]:
    routing = row.get("concept_routing")
    if not isinstance(routing, dict):
        return "", False
    confidence = str(routing.get("confidence") or "").lower()
    concept_ids = [str(value) for value in row.get("concept_ids") or []]
    routed_concept_ids = [str(value) for value in routing.get("concept_ids") or []]
    routes = routing.get("routes")
    route_concept_ids = [
        str(route.get("concept_id") or "")
        for route in routes or []
        if isinstance(route, dict) and str(route.get("method") or "")
    ]
    complete = (
        confidence in {"high", "medium", "low"}
        and isinstance(routes, list)
        and len(route_concept_ids) == len(routes)
        and len(route_concept_ids) == len(set(route_concept_ids))
        and sorted(routed_concept_ids) == sorted(concept_ids)
        and sorted(route_concept_ids) == sorted(concept_ids)
    )
    return confidence, complete


def classify_migration_risk(
    row: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    reasons: list[str] = []
    reason_codes: list[str] = []
    level = "low"

    def raise_to(value: str, code: str, reason: str) -> None:
        nonlocal level
        if RISK_ORDER[value] > RISK_ORDER[level]:
            level = value
        reason_codes.append(code)
        reasons.append(reason)

    freshness = str((row.get("freshness") or {}).get("status") or "missing")
    if not row.get("migration_ready"):
        raise_to("high", "priority_not_migration_ready", "priority action is not migration-ready")
    if freshness != "current":
        raise_to("high", "source_not_current", f"source freshness is {freshness}")
    if int(row.get("verification_debt_count") or 0):
        raise_to(
            "high",
            "legacy_verification_debt",
            "legacy projection has verification debt",
        )
    if int(row.get("existing_source_native_artifact_count") or 0):
        raise_to(
            "high",
            "existing_source_native_identity",
            "existing source-native identities require adjudication",
        )
    if int(row.get("legacy_claim_count") or 0):
        raise_to(
            "standard",
            "legacy_claim_semantic_review",
            "legacy claims require semantic replacement review",
        )
    if not row.get("concept_ids"):
        raise_to("high", "concept_routing_missing", "concept routing is missing")
    routing_confidence, routing_provenance_complete = _concept_routing_provenance(row)
    if row.get("concept_ids") and not routing_provenance_complete:
        raise_to(
            "high",
            "concept_routing_provenance_missing",
            "concept routing provenance is missing or invalid",
        )
    elif row.get("concept_ids") and routing_confidence != "high":
        raise_to(
            "standard",
            "concept_routing_not_high_confidence",
            f"concept routing confidence is {routing_confidence}",
        )
    if not str(row.get("source_content_hash") or ""):
        raise_to(
            "high",
            "normalized_source_hash_missing",
            "normalized source hash is missing",
        )
    if {str(value) for value in row.get("authority_tiers") or []} != {"official"}:
        raise_to(
            "high",
            "source_authority_not_official",
            "source authority is not exclusively official",
        )
    if str(row.get("source_id") or record.get("source_id") or "") == (
        "rock_community_blog"
    ):
        raise_to(
            "standard",
            "editorial_community_blog",
            "editorial rock_community_blog sources require standard review",
        )

    matched_terms = sorted(
        term for term in HIGH_RISK_TERMS if term in _risk_text(row, record)
    )
    if matched_terms:
        raise_to(
            "high",
            "sensitive_operational_terms",
            "sensitive operational terms: " + ", ".join(matched_terms),
        )
    matched_standard_terms = sorted(
        term for term in STANDARD_RISK_TERMS if term in _risk_text(row, record)
    )
    if matched_standard_terms:
        raise_to(
            "standard",
            "version_sensitive_operational_terms",
            "version-sensitive or operational terms: "
            + ", ".join(matched_standard_terms),
        )
    matched_concepts = sorted(
        {str(value) for value in row.get("concept_ids") or []} & HIGH_RISK_CONCEPTS
    )
    if matched_concepts:
        raise_to(
            "high",
            "sensitive_operational_concepts",
            "sensitive operational concepts: " + ", ".join(matched_concepts),
        )

    summary_length = len(str(record.get("summary") or "").strip())
    if summary_length < 100:
        raise_to(
            "standard",
            "normalized_source_preview_too_thin",
            "normalized source preview is too thin for low-risk batching",
        )
    if int(record.get("lava_element_count") or 0) > 5:
        raise_to(
            "standard",
            "broad_lava_surface",
            "source declares more than five Lava elements",
        )
    if int(record.get("documentation_table_of_contents_link_count") or 0) > 30:
        raise_to(
            "standard",
            "broad_table_of_contents",
            "source table of contents indicates broad scope",
        )
    if len(record.get("rock_versions") or []) > 5:
        raise_to(
            "standard",
            "broad_version_scope",
            "source spans more than five Rock versions",
        )

    if not reasons:
        reason_codes.append("bounded_current_official_source")
        reasons.append("current official summary-only source with bounded metadata")
    return {
        "level": level,
        "policy_version": RISK_POLICY_VERSION,
        "reason_codes": reason_codes,
        "reasons": reasons,
    }


def _normalized_tokens(value: str) -> list[str]:
    return [
        token
        for token in "".join(
            character.lower() if character.isalnum() else " " for character in value
        ).split()
        if token
    ]


def _source_binding_tokens(value: str) -> set[str]:
    return {
        token
        for token in _normalized_tokens(value)
        if len(token) > 2 and token not in SOURCE_BINDING_STOP_WORDS
    }


def _episode_numbers(value: str) -> set[int]:
    return {int(match) for match in EPISODE_NUMBER_PATTERN.findall(value)}


def _is_generic_landing_snapshot(
    candidate: dict[str, Any],
    record: dict[str, Any],
) -> bool:
    snapshot = candidate.get("source_snapshot") or {}
    source_id = str(snapshot.get("source_id") or record.get("source_id") or "")
    title = str(snapshot.get("title") or "").strip().lower()
    canonical_url = str(snapshot.get("canonical_url") or record.get("source_url") or "")
    source_path = str(snapshot.get("source_path") or "").lower()
    return source_id == "rock_community_blog" and (
        title in {"blog", "connect"}
        or canonical_url.rstrip("/").endswith("/connect")
        or source_path.endswith("/connect.md")
    )


def classify_hydrated_candidate_risk(
    candidate: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    units = candidate.get("source_units") or []
    text = " ".join(str(unit.get("text") or "") for unit in units)
    lowered = text.lower()
    reasons: list[str] = []
    reason_codes: list[str] = []
    level = "low"

    def raise_to(value: str, code: str, reason: str) -> None:
        nonlocal level
        if RISK_ORDER[value] > RISK_ORDER[level]:
            level = value
        reason_codes.append(code)
        reasons.append(reason)

    matched_terms = sorted(term for term in HYDRATED_HIGH_RISK_TERMS if term in lowered)
    if matched_terms:
        raise_to(
            "high",
            "hydrated_sensitive_terms",
            "hydrated source contains sensitive terms: " + ", ".join(matched_terms),
        )
    for code, label, pattern in HYDRATED_STANDARD_RISK_PATTERNS:
        if re.search(pattern, lowered):
            raise_to(
                "standard",
                code,
                f"hydrated source contains {label}",
            )
    if re.search(HYDRATED_POSITIVE_STATUS_PATTERN, lowered) and re.search(
        HYDRATED_NEGATIVE_STATUS_PATTERN,
        lowered,
    ):
        raise_to(
            "standard",
            "hydrated_contradictory_release_status",
            "hydrated source contains contradictory support or release status wording",
        )
    code_count = sum(str(unit.get("unit_kind") or "") == "code_block" for unit in units)
    table_count = sum(str(unit.get("unit_kind") or "") == "table" for unit in units)
    if level == "low" and (code_count > 10 or table_count > 5 or len(units) > 100):
        raise_to(
            "standard",
            "hydrated_structural_bounds",
            "hydrated source exceeds low-risk structural bounds: "
            f"{len(units)} units, {code_count} code blocks, {table_count} tables",
        )

    summary_tokens = _source_binding_tokens(str(record.get("summary") or ""))
    hydrated_tokens = _source_binding_tokens(text)
    overlap_ratio = (
        len(summary_tokens & hydrated_tokens) / len(summary_tokens)
        if summary_tokens
        else 0.0
    )
    if len(summary_tokens) >= 8 and overlap_ratio < 0.6:
        raise_to(
            "high",
            "hydrated_normalized_preview_mismatch",
            "hydrated source has insufficient normalized preview coverage: "
            f"{overlap_ratio:.2f}",
        )

    legacy_text = " ".join(
        " ".join(
            (
                str(item.get("title") or ""),
                str(item.get("retrieval_text") or ""),
            )
        )
        for item in candidate.get("legacy_items") or []
        if isinstance(item, dict)
    )
    legacy_episode_numbers = _episode_numbers(legacy_text)
    hydrated_episode_numbers = _episode_numbers(text)
    if (
        legacy_episode_numbers
        and hydrated_episode_numbers
        and legacy_episode_numbers.isdisjoint(hydrated_episode_numbers)
    ):
        raise_to(
            "high",
            "hydrated_legacy_episode_mismatch",
            "hydrated source episode identity differs from legacy retrieval text: "
            f"legacy={sorted(legacy_episode_numbers)}, "
            f"hydrated={sorted(hydrated_episode_numbers)}",
        )
    legacy_tokens = _source_binding_tokens(legacy_text)
    legacy_overlap_ratio = (
        len(legacy_tokens & hydrated_tokens) / len(legacy_tokens)
        if legacy_tokens
        else None
    )
    generic_landing_snapshot = _is_generic_landing_snapshot(candidate, record)
    if (
        generic_landing_snapshot
        and len(legacy_tokens) >= 8
        and legacy_overlap_ratio is not None
        and legacy_overlap_ratio < 0.6
    ):
        raise_to(
            "high",
            "hydrated_generic_landing_legacy_mismatch",
            "generic hydrated landing page has insufficient legacy item coverage: "
            f"{legacy_overlap_ratio:.2f}",
        )
    if not reasons:
        reason_codes.append("hydrated_bounded_source")
        reasons.append(
            "hydrated source remains within low-risk content and structure bounds"
        )
    return {
        "level": level,
        "policy_version": RISK_POLICY_VERSION,
        "reason_codes": reason_codes,
        "reasons": reasons,
        "source_unit_count": len(units),
        "code_block_count": code_count,
        "table_count": table_count,
        "source_binding_overlap": round(overlap_ratio, 3),
        "identity_checks": {
            "generic_landing_snapshot": generic_landing_snapshot,
            "hydrated_episode_numbers": sorted(hydrated_episode_numbers),
            "legacy_episode_numbers": sorted(legacy_episode_numbers),
            "legacy_source_binding_overlap": (
                round(legacy_overlap_ratio, 3)
                if legacy_overlap_ratio is not None
                else None
            ),
        },
    }


def select_migration_batch(
    *,
    report: dict[str, Any],
    records: Iterable[dict[str, Any]],
    count: int,
    max_risk: str,
    source_ids: Iterable[str] = (),
    concept_ids: Iterable[str] = (),
    exact_source_record_ids: Iterable[str] = (),
) -> dict[str, Any]:
    _validate_priority_report(report)
    if count < 1 or count > 50:
        raise ValueError("migration batch count must be between 1 and 50")
    if max_risk not in RISK_ORDER:
        raise ValueError("max_risk must be low, standard, or high")
    records_by_id = {
        str(record.get("id") or ""): record for record in records if record.get("id")
    }
    source_filter = {str(value) for value in source_ids if str(value)}
    concept_filter = {str(value) for value in concept_ids if str(value)}
    exact_ids = [str(value) for value in exact_source_record_ids if str(value)]
    rows_by_id = {str(row.get("source_record_id") or ""): row for row in report["rows"]}
    if exact_ids:
        if len(exact_ids) != len(set(exact_ids)):
            raise ValueError("exact source record selection contains duplicates")
        missing_exact = sorted(set(exact_ids) - set(rows_by_id))
        if missing_exact:
            raise ValueError(
                "exact source records are absent from the priority report: "
                + ", ".join(missing_exact)
            )
        candidates = [rows_by_id[source_record_id] for source_record_id in exact_ids]
        if count != len(candidates):
            raise ValueError("count must equal the exact source record selection size")
    else:
        candidates = list(report["rows"])

    def classify_row(
        row: dict[str, Any],
    ) -> tuple[str | None, dict[str, Any] | None]:
        source_record_id = str(row.get("source_record_id") or "")
        record = records_by_id.get(source_record_id)
        if record is None:
            raise ValueError(
                f"priority source record disappeared from normalized data: "
                f"{source_record_id}"
            )
        normalized_hash = str(record.get("content_hash") or "")
        if normalized_hash != str(row.get("source_content_hash") or ""):
            raise ValueError(f"priority source hash changed for {source_record_id}")
        if source_filter and str(row.get("source_id") or "") not in source_filter:
            return "source_filter", None
        if concept_filter and not concept_filter.intersection(
            str(value) for value in row.get("concept_ids") or []
        ):
            return "concept_filter", None
        if not row.get("migration_ready"):
            return str(row.get("recommended_action") or "not_migration_ready"), None
        risk = classify_migration_risk(row, record)
        if RISK_ORDER[risk["level"]] > RISK_ORDER[max_risk]:
            return f"risk_{risk['level']}", risk
        return None, risk

    selected: list[dict[str, Any]] = []
    for row in candidates:
        reason, risk = classify_row(row)
        if reason is not None:
            continue
        source_record_id = str(row["source_record_id"])
        selected.append(
            {
                **row,
                "risk": risk,
                "normalized_summary_char_count": len(
                    str(records_by_id[source_record_id].get("summary") or "")
                ),
            }
        )
        if not exact_ids and len(selected) == count:
            break

    if exact_ids and len(selected) != count:
        raise ValueError("one or more exact source records failed the selection policy")
    if len(selected) != count:
        raise ValueError(
            f"requested {count} migration records but only {len(selected)} "
            f"satisfied the {max_risk} risk policy"
        )
    if exact_ids and [row["source_record_id"] for row in selected] != exact_ids:
        raise ValueError("one or more exact source records failed the selection policy")

    selected_ids = [str(row["source_record_id"]) for row in selected]
    selected_set = set(selected_ids)
    excluded = Counter()
    excluded_examples: dict[str, list[str]] = defaultdict(list)
    queues: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in report["rows"]:
        source_record_id = str(row.get("source_record_id") or "")
        if source_record_id in selected_set:
            continue
        reason, risk = classify_row(row)
        if reason is None:
            reason = "eligible_not_selected"
        excluded[reason] += 1
        if len(excluded_examples[reason]) < 10:
            excluded_examples[reason].append(source_record_id)
        queue_name = {
            "refresh_source_first": "refresh_first",
            "risk_high": "high_risk",
            "risk_standard": "standard_risk",
            "eligible_not_selected": "eligible_backlog",
        }.get(reason, "other_excluded")
        queues[queue_name].append(
            {
                "rank": row.get("rank"),
                "source_record_id": source_record_id,
                "source_id": row.get("source_id"),
                "source_title": row.get("source_title"),
                "recommended_action": row.get("recommended_action"),
                "freshness_status": (row.get("freshness") or {}).get("status"),
                "concept_ids": row.get("concept_ids") or [],
                "exclusion_reason": reason,
                "risk": risk,
            }
        )

    selection_payload = {
        "policy_version": BATCH_POLICY_VERSION,
        "risk_policy_version": RISK_POLICY_VERSION,
        "max_risk": max_risk,
        "source_ids": sorted(source_filter),
        "concept_ids": sorted(concept_filter),
        "selected_source_record_ids": selected_ids,
        "selected": selected,
    }
    return {
        "schema": "rock-kb-source-native-migration-batch-selection-v1",
        "status": "ok",
        **selection_payload,
        "selection_hash": sha256_text(canonical_json(selection_payload)),
        "excluded_counts": dict(sorted(excluded.items())),
        "excluded_examples": dict(sorted(excluded_examples.items())),
        "queues": dict(sorted(queues.items())),
    }


def _selection_payload(selection: dict[str, Any]) -> dict[str, Any]:
    return {
        key: selection[key]
        for key in (
            "policy_version",
            "risk_policy_version",
            "max_risk",
            "source_ids",
            "concept_ids",
            "selected_source_record_ids",
            "selected",
        )
    }


def _refresh_selection_hash(selection: dict[str, Any]) -> None:
    selection["selection_hash"] = sha256_text(
        canonical_json(_selection_payload(selection))
    )


def _sanitize_batch_metadata_paths(value: Any, root: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: _sanitize_batch_metadata_paths(item, root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_batch_metadata_paths(item, root) for item in value]
    if isinstance(value, str):
        root_text = str(root.resolve())
        if value == root_text:
            return "."
        if value.startswith(root_text + "/"):
            return value[len(root_text) + 1 :]
    return value


def _prepared_file_inventory(root: Path) -> dict[str, dict[str, Any]]:
    excluded = {
        "batch-manifest.json",
        "batch-state.json",
        ".batch.lock",
        "generated-output.json",
        "validated-reviewed-output.json",
        "comparison-report.json",
        "review-validation-manifest.json",
        ".generated-output.pending.json",
        ".generated-output.recovery.json",
    }
    inventory: dict[str, dict[str, Any]] = {}
    for path in sorted(value for value in root.rglob("*") if value.is_file()):
        relative = path.relative_to(root).as_posix()
        if relative in excluded or relative.startswith("model-output/"):
            continue
        record_count = None
        if path.suffix == ".jsonl":
            record_count = sum(1 for _ in read_jsonl(path))
        inventory[relative] = {
            "sha256": sha256_file(path),
            "record_count": record_count,
        }
    return inventory


def _verify_prepared_files(batch_dir: Path, state: dict[str, Any]) -> None:
    expected = state.get("prepared_files") or {}
    for relative, metadata in expected.items():
        path = (batch_dir / relative).resolve()
        if not path.is_relative_to(batch_dir.resolve()):
            raise ValueError("prepared migration batch state contains a path escape")
        if not path.is_file() or sha256_file(path) != metadata.get("sha256"):
            raise ValueError(
                f"prepared migration batch file changed after preparation: {relative}"
            )
    actual = _prepared_file_inventory(batch_dir)
    if actual != expected:
        raise ValueError("prepared migration batch file inventory changed")


def _batch_manifest_id(payload: dict[str, Any]) -> str:
    return "source-native-migration-batch:" + sha256_text(canonical_json(payload))[:24]


def _write_batch_state(batch_dir: Path, state: dict[str, Any]) -> None:
    _atomic_json(
        batch_dir / "batch-state.json",
        {key: value for key, value in state.items() if key != "_manifest"},
    )


def _validate_batch_manifest(
    batch_dir: Path,
    *,
    repo_root: Path,
    git_state: dict[str, Any],
) -> dict[str, Any]:
    manifest_path = batch_dir / "batch-manifest.json"
    if not manifest_path.is_file():
        raise ValueError("migration batch manifest is missing")
    manifest = _read_json(manifest_path)
    if manifest.get("schema") != BATCH_MANIFEST_SCHEMA:
        raise ValueError("unsupported migration batch manifest schema")
    payload = {
        key: value
        for key, value in manifest.items()
        if key not in {"schema", "batch_id"}
    }
    if manifest.get("batch_id") != _batch_manifest_id(payload):
        raise ValueError("migration batch manifest identity is invalid")
    if git_state["base_commit"] != manifest.get("git", {}).get("base_commit"):
        raise ValueError("migration batch base commit no longer matches HEAD")
    current_contract_hashes = {
        "distillation_prompt": sha256_file(
            repo_root / SOURCE_NATIVE_PROMPT_PATH.relative_to(REPO_ROOT)
        ),
        "migration_prompt": sha256_file(
            repo_root
            / SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_PATH.relative_to(REPO_ROOT)
        ),
        "distillation_schema": sha256_file(
            repo_root / SOURCE_NATIVE_SCHEMA_PATH.relative_to(REPO_ROOT)
        ),
    }
    expected_contract_hashes = {
        "distillation_prompt": manifest["prompts"]["distillation"]["sha256"],
        "migration_prompt": manifest["prompts"]["migration"]["sha256"],
        "distillation_schema": manifest["schema_hashes"]["distillation"],
    }
    if current_contract_hashes != expected_contract_hashes:
        raise ValueError("migration prompt or schema changed after preparation")
    _verify_prepared_files(batch_dir, manifest)
    if manifest["priority"]["file_sha256"] != sha256_file(
        batch_dir / "priority-report.json"
    ):
        raise ValueError("prepared priority report changed after preparation")

    selection = _read_json(batch_dir / "selection.json")
    if manifest["selection_hash"] != sha256_text(
        canonical_json(_selection_payload(selection))
    ):
        raise ValueError("prepared migration selection hash is invalid")

    current_records = {
        str(record.get("id") or ""): record
        for record in concept_source_records(repo_root=repo_root)
        if record.get("id")
    }
    for selected in manifest.get("selected_records") or []:
        source_record_id = str(selected.get("source_record_id") or "")
        current = current_records.get(source_record_id)
        if current is None or current.get("content_hash") != selected.get(
            "source_content_hash"
        ):
            raise ValueError(
                f"normalized source changed after preparation: {source_record_id}"
            )

    migration_rows = list(read_jsonl(batch_dir / "migration-input.jsonl"))
    expected_shards = manifest.get("expected_shards") or []
    if len(migration_rows) != len(expected_shards):
        raise ValueError("migration input count changed after preparation")
    for shard in expected_shards:
        prompt_path = (batch_dir / str(shard.get("prompt_path") or "")).resolve()
        if not prompt_path.is_relative_to(batch_dir.resolve()):
            raise ValueError("migration batch prompt path escapes the batch")
    actual_shards = [
        {
            "source_record_id": str(row["source_snapshot"]["source_record_id"]),
            "candidate_id": str(row["candidate_id"]),
            "source_input_hash": str(row["source_input_hash"]),
            "migration_input_hash": str(row["migration_input_hash"]),
            "prompt_path": expected_shards[index]["prompt_path"],
            "prompt_sha256": sha256_file(
                batch_dir / expected_shards[index]["prompt_path"]
            ),
        }
        for index, row in enumerate(migration_rows)
    ]
    if actual_shards != expected_shards:
        raise ValueError(
            "migration input or per-record prompt changed after preparation"
        )
    return manifest


def _validate_batch_runtime(
    batch_dir: Path,
    *,
    repo_root: Path,
    require_clean: bool,
) -> dict[str, Any]:
    _cleanup_runtime_residue(batch_dir)
    state_path = batch_dir / "batch-state.json"
    if not state_path.exists():
        raise ValueError("migration batch state is missing")
    state = _read_json(state_path)
    if state.get("schema") != BATCH_STATE_SCHEMA:
        raise ValueError("unsupported migration batch state schema")
    git_state = _git_state(repo_root, require_clean=require_clean)
    manifest = _validate_batch_manifest(
        batch_dir,
        repo_root=repo_root,
        git_state=git_state,
    )
    if state.get("batch_id") != manifest.get("batch_id"):
        raise ValueError("migration batch state does not match its sealed manifest")
    state["_manifest"] = manifest
    return state


def _existing_prepare_result(
    destination: Path,
    *,
    expected_config_hash: str,
    repo_root: Path,
    require_clean: bool,
) -> dict[str, Any]:
    state = _validate_batch_runtime(
        destination,
        repo_root=repo_root,
        require_clean=require_clean,
    )
    manifest = state["_manifest"]
    if manifest.get("config_hash") != expected_config_hash:
        raise ValueError("existing migration batch was prepared with different inputs")
    return {
        "schema": BATCH_STATE_SCHEMA,
        "status": "unchanged",
        "batch_id": state["batch_id"],
        "overall_state": state["overall_state"],
        "selected_count": len(manifest.get("selected_records") or []),
        "destination": str(destination),
    }


def prepare_source_native_migration_batch(
    *,
    destination: Path,
    count: int = 30,
    max_risk: str = "low",
    as_of: str | None = None,
    priority_report_path: Path | None = None,
    source_ids: Iterable[str] = (),
    concept_ids: Iterable[str] = (),
    exact_source_record_ids: Iterable[str] = (),
    max_source_units_per_record: int = 200,
    repo_root: Path = REPO_ROOT,
    require_clean: bool = True,
) -> dict[str, Any]:
    destination = _require_review_destination(destination, repo_root)
    if max_source_units_per_record < 1 or max_source_units_per_record > 200:
        raise ValueError("max_source_units_per_record must be between 1 and 200")
    parsed_as_of = parse_utc(as_of)
    if as_of and parsed_as_of is None:
        raise ValueError("as_of must be a valid ISO-8601 timestamp")
    if priority_report_path is None and parsed_as_of is None:
        raise ValueError("automatic priority generation requires a fixed as_of")
    git_state = _git_state(repo_root, require_clean=require_clean)

    with _batch_lock(repo_root), tempfile.TemporaryDirectory(
        prefix="rock-kb-migration-priority-"
    ) as priority_temp:
            if priority_report_path is None:
                generated_priority = Path(priority_temp) / "priority-report.json"
                build_source_native_migration_priority_report(
                    destination=generated_priority,
                    repo_root=repo_root,
                    as_of=parsed_as_of,
                    limit=2000,
                    dashboard=None,
                )
                priority_source = generated_priority
            else:
                priority_source = _require_review_input(priority_report_path, repo_root)
            report = _read_json(priority_source)
            _validate_priority_report(report)
            if parsed_as_of and parse_utc(report.get("as_of")) != parsed_as_of:
                raise ValueError("priority report as_of does not match requested as_of")

            records = concept_source_records(repo_root=repo_root)
            selection = select_migration_batch(
                report=report,
                records=records,
                count=count,
                max_risk=max_risk,
                source_ids=source_ids,
                concept_ids=concept_ids,
                exact_source_record_ids=exact_source_record_ids,
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            staging = Path(
                tempfile.mkdtemp(
                    prefix=f".{destination.name}-",
                    dir=destination.parent,
                )
            )
            started = time.monotonic()
            try:
                shutil.copy2(priority_source, staging / "priority-report.json")
                queue_dir = staging / "queues"
                for queue_name in (
                    "refresh_first",
                    "high_risk",
                    "standard_risk",
                    "eligible_backlog",
                    "other_excluded",
                ):
                    write_jsonl(
                        queue_dir / f"{queue_name.replace('_', '-')}.jsonl",
                        selection.get("queues", {}).get(queue_name) or [],
                    )
                selected_ids = selection["selected_source_record_ids"]
                selected_set = set(selected_ids)
                selected_records = [
                    record
                    for record in records
                    if str(record.get("id") or "") in selected_set
                ]
                selected_by_id = {
                    str(row["source_record_id"]): row for row in selection["selected"]
                }
                record_concepts = {
                    source_record_id: list(row["concept_ids"])
                    for source_record_id, row in selected_by_id.items()
                }
                source_families = sorted(
                    {str(row["source_id"]) for row in selection["selected"]}
                )
                all_concepts = sorted(
                    {
                        str(concept_id)
                        for row in selection["selected"]
                        for concept_id in row["concept_ids"]
                    }
                )
                candidate_dir = staging / "candidates"
                build_result = build_source_native_document_candidates(
                    concept_ids=all_concepts,
                    source_ids=source_families,
                    source_record_ids=selected_ids,
                    source_record_concept_ids=record_concepts,
                    destination=candidate_dir,
                    previous_dir=repo_root
                    / SOURCE_NATIVE_PILOT_DIR.relative_to(REPO_ROOT),
                    checked_at=str(report["as_of"]),
                    records=selected_records,
                )
                candidate_rows = list(
                    read_jsonl(candidate_dir / "distillation-input.jsonl")
                )
                candidates_by_record = {
                    str(row["source_snapshot"]["source_record_id"]): row
                    for row in candidate_rows
                }
                if int(build_result.get("article_count") or 0) != count:
                    missing = sorted(selected_set - set(candidates_by_record))
                    skipped = (build_result.get("document_candidate_build") or {}).get(
                        "skipped"
                    ) or []
                    raise ValueError(
                        "candidate hydration did not preserve the exact batch size; "
                        f"missing={missing}; skipped={skipped}"
                    )
                if set(candidates_by_record) != selected_set:
                    raise ValueError(
                        "candidate hydration changed the exact selected record set"
                    )
                if len(candidates_by_record) != len(candidate_rows):
                    raise ValueError("candidate hydration produced duplicate records")
                records_by_id = {
                    str(record.get("id") or ""): record for record in selected_records
                }
                for source_record_id in selected_ids:
                    candidate = candidates_by_record[source_record_id]
                    if sorted(candidate.get("concept_ids") or []) != sorted(
                        record_concepts[source_record_id]
                    ):
                        raise ValueError(
                            f"candidate concept routing changed for {source_record_id}"
                        )
                    unit_count = len(candidate.get("source_units") or [])
                    if unit_count > max_source_units_per_record:
                        raise ValueError(
                            f"candidate exceeds the {max_source_units_per_record}-unit "
                            f"batch contract: {source_record_id} has {unit_count}"
                        )
                    hydrated_risk = classify_hydrated_candidate_risk(
                        candidate,
                        records_by_id[source_record_id],
                    )
                    if RISK_ORDER[hydrated_risk["level"]] > RISK_ORDER[max_risk]:
                        raise ValueError(
                            f"hydrated candidate exceeds the {max_risk} risk policy: "
                            f"{source_record_id} is {hydrated_risk['level']}"
                        )
                    selected_by_id[source_record_id]["hydrated_risk"] = hydrated_risk
                candidate_summary_path = candidate_dir / "candidate-summary.json"
                if candidate_summary_path.exists():
                    _atomic_json(
                        candidate_summary_path,
                        _sanitize_batch_metadata_paths(
                            _read_json(candidate_summary_path),
                            staging,
                        ),
                    )
                migration_input_path = staging / "migration-input.jsonl"
                migration_result = build_source_native_legacy_migration_inputs(
                    source_native_input_path=(
                        candidate_dir / "distillation-input.jsonl"
                    ),
                    destination=migration_input_path,
                    repo_root=repo_root,
                )
                if int(migration_result.get("article_count") or 0) != count:
                    raise ValueError(
                        "migration input did not preserve the exact batch size"
                    )
                migration_rows = list(read_jsonl(migration_input_path))
                migration_by_record = {
                    str(row["source_snapshot"]["source_record_id"]): row
                    for row in migration_rows
                }
                if set(migration_by_record) != selected_set:
                    raise ValueError(
                        "migration input changed the exact selected record set"
                    )
                for source_record_id in selected_ids:
                    hydrated_risk = classify_hydrated_candidate_risk(
                        migration_by_record[source_record_id],
                        records_by_id[source_record_id],
                    )
                    if RISK_ORDER[hydrated_risk["level"]] > RISK_ORDER[max_risk]:
                        raise ValueError(
                            f"hydrated candidate exceeds the {max_risk} risk policy: "
                            f"{source_record_id} is {hydrated_risk['level']}"
                        )
                    selected_by_id[source_record_id]["hydrated_risk"] = hydrated_risk
                _refresh_selection_hash(selection)
                _atomic_json(staging / "selection.json", selection)

                schema_result = write_source_native_legacy_migration_schema(
                    staging / "migration-schema.json"
                )
                prompt_dir = staging / "prompts"
                prompt_dir.mkdir(parents=True, exist_ok=True)
                expected_shards = []
                rank_by_id = {
                    str(row["source_record_id"]): int(row["rank"])
                    for row in selection["selected"]
                }
                for row in migration_rows:
                    source_record_id = str(row["source_snapshot"]["source_record_id"])
                    filename = (
                        f"{rank_by_id[source_record_id]:04d}-"
                        f"{sha256_text(source_record_id)[:12]}.txt"
                    )
                    prompt_path = prompt_dir / filename
                    write_source_native_legacy_migration_prompt(
                        input_path=migration_input_path,
                        destination=prompt_path,
                        source_record_id=source_record_id,
                    )
                    expected_shards.append(
                        {
                            "source_record_id": source_record_id,
                            "candidate_id": str(row["candidate_id"]),
                            "source_input_hash": str(row["source_input_hash"]),
                            "migration_input_hash": str(row["migration_input_hash"]),
                            "prompt_path": prompt_path.relative_to(staging).as_posix(),
                            "prompt_sha256": sha256_file(prompt_path),
                        }
                    )

                config_payload = {
                    "base_commit": git_state["base_commit"],
                    "priority_input_hash": report["input_hash"],
                    "priority_file_sha256": sha256_file(priority_source),
                    "selection_hash": selection["selection_hash"],
                    "max_source_units_per_record": max_source_units_per_record,
                    "distillation_prompt_version": SOURCE_NATIVE_PROMPT_VERSION,
                    "migration_prompt_version": (
                        SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION
                    ),
                    "batch_policy_version": BATCH_POLICY_VERSION,
                    "risk_policy_version": RISK_POLICY_VERSION,
                }
                config_hash = sha256_text(canonical_json(config_payload))
                distillation_prompt_sha256 = sha256_file(
                    repo_root / SOURCE_NATIVE_PROMPT_PATH.relative_to(REPO_ROOT)
                )
                migration_prompt_sha256 = sha256_file(
                    repo_root
                    / SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_PATH.relative_to(REPO_ROOT)
                )
                final_git_state = _git_state(
                    repo_root,
                    require_clean=require_clean,
                )
                if final_git_state != git_state:
                    raise ValueError(
                        "tracked repository state changed during batch preparation"
                    )
                prepared_files = _prepared_file_inventory(staging)
                manifest_payload = {
                    "config_hash": config_hash,
                    "git": git_state,
                    "priority": {
                        "schema": report["schema"],
                        "algorithm_version": report["algorithm_version"],
                        "as_of": report["as_of"],
                        "input_hash": report["input_hash"],
                        "file_sha256": config_payload["priority_file_sha256"],
                    },
                    "policy": {
                        "batch_policy_version": BATCH_POLICY_VERSION,
                        "risk_policy_version": RISK_POLICY_VERSION,
                        "max_risk": max_risk,
                        "max_source_units_per_record": max_source_units_per_record,
                    },
                    "prompts": {
                        "distillation": {
                            "prompt_id": SOURCE_NATIVE_PROMPT_ID,
                            "version": SOURCE_NATIVE_PROMPT_VERSION,
                            "sha256": distillation_prompt_sha256,
                        },
                        "migration": {
                            "prompt_id": SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_ID,
                            "version": SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION,
                            "sha256": migration_prompt_sha256,
                        },
                    },
                    "schema_hashes": {
                        "distillation": sha256_file(
                            repo_root / SOURCE_NATIVE_SCHEMA_PATH.relative_to(REPO_ROOT)
                        ),
                        "migration": schema_result["sha256"],
                    },
                    "selection_hash": selection["selection_hash"],
                    "selected_records": [
                        {
                            "rank": row["rank"],
                            "source_record_id": row["source_record_id"],
                            "source_id": row["source_id"],
                            "source_content_hash": row["source_content_hash"],
                            "concept_ids": row["concept_ids"],
                            "risk": row["risk"],
                            "hydrated_risk": row["hydrated_risk"],
                        }
                        for row in selection["selected"]
                    ],
                    "expected_shards": expected_shards,
                    "prepared_files": prepared_files,
                }
                batch_id = _batch_manifest_id(manifest_payload)
                manifest = {
                    "schema": BATCH_MANIFEST_SCHEMA,
                    "batch_id": batch_id,
                    **manifest_payload,
                }
                _atomic_json(staging / "batch-manifest.json", manifest)
                state = {
                    "schema": BATCH_STATE_SCHEMA,
                    "batch_id": batch_id,
                    "overall_state": "awaiting_model_generation",
                    "manual_review_required": True,
                    "promotion_permitted": False,
                    "external_writes_permitted": False,
                    "phases": {
                        "prepare": {
                            "status": "passed",
                            "duration": {
                                "value": round(time.monotonic() - started, 3),
                                "unit": "seconds",
                                "evidence_status": "measured",
                            },
                        },
                        "assemble": {"status": "pending"},
                        "validate_review": {"status": "pending"},
                    },
                    "model_metrics": {
                        "input_tokens": {
                            "value": None,
                            "unit": "tokens",
                            "evidence_status": "unavailable",
                            "reason": "The coordinator does not invoke the model.",
                        },
                        "output_tokens": {
                            "value": None,
                            "unit": "tokens",
                            "evidence_status": "unavailable",
                            "reason": "The coordinator does not invoke the model.",
                        },
                        "cost": {
                            "value": None,
                            "unit": "usd",
                            "evidence_status": "unavailable",
                            "reason": "No model billing record was supplied.",
                        },
                    },
                }
                _write_batch_state(staging, state)
                if destination.exists():
                    existing = _existing_prepare_result(
                        destination,
                        expected_config_hash=config_hash,
                        repo_root=repo_root,
                        require_clean=require_clean,
                    )
                    existing_manifest = _read_json(destination / "batch-manifest.json")
                    if existing_manifest.get("batch_id") != batch_id:
                        raise ValueError(
                            "existing migration batch was prepared from different "
                            "hydrated source inputs"
                        )
                    shutil.rmtree(staging, ignore_errors=True)
                    return existing
                staging.replace(destination)
            except Exception:
                shutil.rmtree(staging, ignore_errors=True)
                raise

    return {
        "schema": BATCH_STATE_SCHEMA,
        "status": "ok",
        "batch_id": batch_id,
        "overall_state": "awaiting_model_generation",
        "selected_count": count,
        "source_unit_count": int(build_result.get("source_unit_count") or 0),
        "legacy_item_count": int(migration_result.get("legacy_item_count") or 0),
        "destination": str(destination),
    }


def _reject_low_risk_unmatched_routing(
    output_path: Path,
    manifest: dict[str, Any],
) -> None:
    if str((manifest.get("policy") or {}).get("max_risk") or "") != "low":
        return
    output = _read_json(output_path)
    violations = [
        {
            "candidate_id": str(article.get("candidate_id") or ""),
            "unmatched_routing_terms": list(article.get("unmatched_routing_terms") or []),
        }
        for article in output.get("articles") or []
        if isinstance(article, dict) and article.get("unmatched_routing_terms")
    ]
    if violations:
        raise ValueError(
            "low-risk assembly contains unmatched routing terms: "
            + canonical_json(violations)
        )


def assemble_source_native_migration_batch(
    *,
    batch_dir: Path,
    model_output_paths: Iterable[Path],
    model: str,
    repo_root: Path = REPO_ROOT,
    require_clean: bool = True,
) -> dict[str, Any]:
    batch_dir = _require_review_destination(batch_dir, repo_root)
    model = model.strip()
    if len(model) < 3 or len(model) > 160:
        raise ValueError("model must be an exact bounded model identifier")
    paths = [_require_review_input(path, repo_root) for path in model_output_paths]
    if not paths:
        raise ValueError("at least one model output shard is required")
    with _batch_lock(repo_root):
        state = _validate_batch_runtime(
            batch_dir,
            repo_root=repo_root,
            require_clean=require_clean,
        )
        destination = batch_dir / "generated-output.json"
        requested_shards = [
            {
                "name": path.name,
                "sha256": sha256_file(path),
            }
            for path in paths
        ]
        if destination.exists():
            recorded = state.get("generated_output") or {}
            if recorded:
                if recorded.get("sha256") != sha256_file(destination):
                    raise ValueError(
                        "existing generated output does not match batch state"
                    )
                if recorded.get("shards") != requested_shards:
                    raise ValueError(
                        "requested model shards differ from the assembled batch"
                    )
                if recorded.get("model") != model:
                    raise ValueError("requested model differs from the assembled batch")
                _reject_low_risk_unmatched_routing(
                    destination,
                    state.get("_manifest") or {},
                )
                return {
                    "schema": BATCH_STATE_SCHEMA,
                    "status": "unchanged",
                    "batch_id": state["batch_id"],
                    "overall_state": state["overall_state"],
                    "destination": str(destination),
                }
            recovery_path = batch_dir / ".generated-output.recovery.json"
            recovery_result = merge_source_native_legacy_migration_outputs(
                input_path=batch_dir / "migration-input.jsonl",
                batch_paths=paths,
                destination=recovery_path,
            )
            if sha256_file(recovery_path) != sha256_file(destination):
                recovery_path.unlink(missing_ok=True)
                raise ValueError(
                    "existing generated output differs from the requested model shards"
                )
            try:
                _reject_low_risk_unmatched_routing(
                    recovery_path,
                    state.get("_manifest") or {},
                )
            except Exception:
                recovery_path.unlink(missing_ok=True)
                raise
            recovery_path.unlink(missing_ok=True)
            state["generated_output"] = {
                "path": destination.relative_to(batch_dir).as_posix(),
                "sha256": sha256_file(destination),
                "article_count": int(recovery_result["article_count"]),
                "shards": requested_shards,
                "model": model,
                "recovered_after_interrupted_state_update": True,
            }
            state["phases"]["assemble"] = {
                "status": "passed",
                "duration": {
                    "value": None,
                    "unit": "seconds",
                    "evidence_status": "unavailable",
                    "reason": "Recovered after an interrupted state update.",
                },
            }
            state["overall_state"] = "awaiting_maintainer_review"
            _write_batch_state(batch_dir, state)
            return {
                "schema": BATCH_STATE_SCHEMA,
                "status": "recovered",
                "batch_id": state["batch_id"],
                "overall_state": state["overall_state"],
                "article_count": recovery_result["article_count"],
                "destination": str(destination),
            }
        started = time.monotonic()
        pending_destination = batch_dir / ".generated-output.pending.json"
        try:
            merge_result = merge_source_native_legacy_migration_outputs(
                input_path=batch_dir / "migration-input.jsonl",
                batch_paths=paths,
                destination=pending_destination,
            )
            _reject_low_risk_unmatched_routing(
                pending_destination,
                state.get("_manifest") or {},
            )
        except Exception:
            pending_destination.unlink(missing_ok=True)
            raise
        pending_destination.replace(destination)
        state["generated_output"] = {
            "path": destination.relative_to(batch_dir).as_posix(),
            "sha256": sha256_file(destination),
            "article_count": int(merge_result["article_count"]),
            "shards": requested_shards,
            "model": model,
        }
        state["phases"]["assemble"] = {
            "status": "passed",
            "duration": {
                "value": round(time.monotonic() - started, 3),
                "unit": "seconds",
                "evidence_status": "measured",
            },
        }
        state["overall_state"] = "awaiting_maintainer_review"
        _write_batch_state(batch_dir, state)
    return {
        "schema": BATCH_STATE_SCHEMA,
        "status": "ok",
        "batch_id": state["batch_id"],
        "overall_state": state["overall_state"],
        "article_count": merge_result["article_count"],
        "destination": str(destination),
    }


def _stable_list_key(value: list[Any]) -> str | None:
    if not value or not all(isinstance(row, dict) for row in value):
        return None
    for key in STABLE_LIST_KEYS:
        keys = [str(row.get(key) or "") for row in value]
        if all(keys) and len(keys) == len(set(keys)):
            return key
    return None


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else str(key)
            result.update(_flatten(value[key], path))
        return result
    if isinstance(value, list):
        if not value or all(not isinstance(row, (dict, list)) for row in value):
            return {prefix: value}
        stable_key = _stable_list_key(value)
        result = {}
        for index, row in enumerate(value):
            label = str(row[stable_key]) if stable_key else str(index)
            path = (
                f"{prefix}[{stable_key}={label}]"
                if stable_key
                else f"{prefix}[{label}]"
            )
            result.update(_flatten(row, path))
        return result
    return {prefix: value}


def correction_category(path: str, before: Any, after: Any) -> str:
    lowered = path.lower()
    if (before is None or after is None) and any(
        value in lowered
        for value in ("claim_type", "evidence_class", "replacement_artifact_key")
    ):
        return "schema_mechanical"
    if any(value in lowered for value in ("needs_live_verification", "verification_")):
        return "verification"
    if any(
        value in lowered
        for value in ("rock_versions", "version_scope", "temporal_status")
    ):
        return "version_scope"
    if "legacy_decisions" in lowered or "existing_artifact_decisions" in lowered:
        return "legacy_disposition"
    if "relationships" in lowered or "related_" in lowered:
        return "relationships"
    if "concept_ids" in lowered:
        return "routing"
    if any(
        value in lowered
        for value in (
            "evidence_class",
            "claim_type",
            ".content",
            ".title",
            ".rationale",
        )
    ):
        return "evidence_scope"
    if any(
        value in lowered
        for value in (
            "artifact_type",
            "artifact_key",
            "source_unit_ids",
            "source_unit_dispositions",
            "steps",
            "references",
        )
    ):
        return "artifact_shape"
    return "other"


def compare_migration_outputs(
    generated: dict[str, Any],
    reviewed: dict[str, Any],
) -> dict[str, Any]:
    generated_articles = {
        str(row["candidate_id"]): row for row in generated.get("articles") or []
    }
    reviewed_articles = {
        str(row["candidate_id"]): row for row in reviewed.get("articles") or []
    }
    if set(generated_articles) != set(reviewed_articles):
        raise ValueError("generated and reviewed outputs cover different articles")
    corrections = []
    category_counts: Counter[str] = Counter()
    changed_articles = 0
    for candidate_id, generated_article in generated_articles.items():
        before = _flatten(generated_article)
        after = _flatten(reviewed_articles[candidate_id])
        article_corrections = []
        for path in sorted(set(before) | set(after)):
            old_value = before.get(path)
            new_value = after.get(path)
            if old_value == new_value:
                continue
            category = correction_category(path, old_value, new_value)
            category_counts[category] += 1
            article_corrections.append(
                {
                    "path": path,
                    "category": category,
                    "before_hash": sha256_text(canonical_json(old_value)),
                    "after_hash": sha256_text(canonical_json(new_value)),
                }
            )
        if article_corrections:
            changed_articles += 1
        corrections.append(
            {
                "candidate_id": candidate_id,
                "correction_count": len(article_corrections),
                "corrections": article_corrections,
            }
        )
    return {
        "article_count": len(generated_articles),
        "changed_article_count": changed_articles,
        "unchanged_article_count": len(generated_articles) - changed_articles,
        "correction_count": sum(category_counts.values()),
        "correction_category_counts": dict(sorted(category_counts.items())),
        "article_corrections": corrections,
    }


def _article_hash(article: dict[str, Any]) -> str:
    return sha256_text(canonical_json(article))


def _validate_review_decisions(
    *,
    decisions_path: Path,
    generated: dict[str, Any],
    reviewed: dict[str, Any],
    expected_records: dict[str, str],
    judge_review_path: Path | None,
) -> list[dict[str, Any]]:
    decisions = [
        SourceNativeArticleReview.model_validate(row).model_dump(
            by_alias=True,
            exclude_none=False,
        )
        for row in read_jsonl(decisions_path)
    ]
    generated_by_id = {
        str(row["candidate_id"]): row for row in generated.get("articles") or []
    }
    reviewed_by_id = {
        str(row["candidate_id"]): row for row in reviewed.get("articles") or []
    }
    decisions_by_id = {str(row.get("candidate_id") or ""): row for row in decisions}
    if len(decisions_by_id) != len(decisions):
        raise ValueError("review decisions contain duplicate candidate IDs")
    if set(decisions_by_id) != set(generated_by_id):
        raise ValueError("review decisions must cover every article exactly")

    recommendations: dict[str, set[str]] = defaultdict(set)
    if judge_review_path is not None:
        judge = _read_json(judge_review_path)
        for article in judge.get("articles") or []:
            candidate_id = str(article.get("candidate_id") or "")
            raw_recommendation_ids = []
            for recommendation in article.get("recommendations") or []:
                recommendation_id = str(recommendation.get("recommendation_id") or "")
                if not recommendation_id:
                    raise ValueError("judge recommendation ID is missing")
                raw_recommendation_ids.append(recommendation_id)
                recommendations[candidate_id].add(recommendation_id)
            if len(raw_recommendation_ids) != len(set(raw_recommendation_ids)):
                raise ValueError(
                    f"judge recommendation IDs are duplicated for {candidate_id}"
                )
        unknown_judge_candidates = sorted(set(recommendations) - set(generated_by_id))
        if unknown_judge_candidates:
            raise ValueError(
                "judge review contains unknown candidates: "
                + ", ".join(unknown_judge_candidates)
            )

    for candidate_id, decision in decisions_by_id.items():
        if decision.get("schema") != BATCH_REVIEW_SCHEMA:
            raise ValueError(f"unsupported review decision schema for {candidate_id}")
        source_record_id = str(decision.get("source_record_id") or "")
        if source_record_id != expected_records.get(candidate_id):
            raise ValueError(f"review source record changed for {candidate_id}")
        generated_hash = _article_hash(generated_by_id[candidate_id])
        reviewed_hash = _article_hash(reviewed_by_id[candidate_id])
        if decision.get("generated_article_hash") != generated_hash:
            raise ValueError(f"generated article hash changed for {candidate_id}")
        if decision.get("reviewed_article_hash") != reviewed_hash:
            raise ValueError(f"reviewed article hash changed for {candidate_id}")
        changed = generated_hash != reviewed_hash
        expected_decision = "approved_with_corrections" if changed else "approved"
        if decision.get("decision") != expected_decision:
            raise ValueError(
                f"review decision does not match corrections for {candidate_id}"
            )
        if len(str(decision.get("reviewer") or "").strip()) < 2:
            raise ValueError(f"reviewer is missing for {candidate_id}")
        if parse_utc(decision.get("reviewed_at")) is None:
            raise ValueError(f"review timestamp is invalid for {candidate_id}")
        if changed and not [
            str(value).strip()
            for value in decision.get("notes") or []
            if str(value).strip()
        ]:
            raise ValueError(f"corrected review requires notes for {candidate_id}")
        raw_adjudication_ids = [
            str(row.get("recommendation_id") or "")
            for row in decision.get("adjudications") or []
            if str(row.get("recommendation_id") or "")
        ]
        if len(raw_adjudication_ids) != len(set(raw_adjudication_ids)):
            raise ValueError(f"adjudication IDs are duplicated for {candidate_id}")
        adjudication_ids = set(raw_adjudication_ids)
        if recommendations.get(candidate_id, set()) != adjudication_ids:
            raise ValueError(
                f"judge recommendations require exact adjudication for {candidate_id}"
            )
        for adjudication in decision.get("adjudications") or []:
            if adjudication.get("disposition") not in {"accept", "modify", "reject"}:
                raise ValueError(f"invalid adjudication disposition for {candidate_id}")
            if len(str(adjudication.get("rationale") or "").strip()) < 20:
                raise ValueError(
                    f"adjudication rationale is too short for {candidate_id}"
                )
    return decisions


def _review_validation_manifest_id(payload: dict[str, Any]) -> str:
    return "source-native-review-validation:" + sha256_text(
        canonical_json(payload)
    )[:24]


def _load_review_validation_manifest(
    batch_dir: Path,
    state: dict[str, Any],
) -> dict[str, Any]:
    path = batch_dir / "review-validation-manifest.json"
    if not path.is_file():
        raise ValueError("review validation manifest is missing")
    manifest = _read_json(path)
    if manifest.get("schema") != BATCH_REVIEW_VALIDATION_MANIFEST_SCHEMA:
        raise ValueError("unsupported review validation manifest schema")
    payload = {
        key: value
        for key, value in manifest.items()
        if key not in {"schema", "validation_id"}
    }
    validation_id = _review_validation_manifest_id(payload)
    if manifest.get("validation_id") != validation_id:
        raise ValueError("review validation manifest identity is invalid")
    if manifest.get("batch_id") != state.get("batch_id"):
        raise ValueError("review validation manifest belongs to another batch")
    if state.get("review_validation_manifest_id") != validation_id:
        raise ValueError("batch state does not reference the sealed review validation")
    return manifest


def _verify_review_validation_files(
    *,
    batch_dir: Path,
    manifest: dict[str, Any],
    review_decisions_path: Path,
    judge_review_path: Path | None,
    reviewed_input_path: Path | None = None,
) -> None:
    files = manifest.get("files") or {}
    expected = {
        "generated_output": batch_dir / "generated-output.json",
        "validated_reviewed_output": batch_dir / "validated-reviewed-output.json",
        "comparison_report": batch_dir / "comparison-report.json",
        "review_decisions": review_decisions_path,
    }
    if reviewed_input_path is not None:
        expected["reviewed_input"] = reviewed_input_path
    for label, path in expected.items():
        expected_hash = files.get(f"{label}_sha256")
        if not path.is_file() or not expected_hash or sha256_file(path) != expected_hash:
            raise ValueError(f"{label.replace('_', ' ')} changed after validation")
    expected_judge_hash = files.get("judge_review_sha256")
    current_judge_hash = sha256_file(judge_review_path) if judge_review_path else None
    if current_judge_hash != expected_judge_hash:
        raise ValueError("judge review changed after validation")


def validate_source_native_migration_batch_review(
    *,
    batch_dir: Path,
    reviewed_output_path: Path,
    review_decisions_path: Path,
    judge_review_path: Path | None = None,
    repo_root: Path = REPO_ROOT,
    require_clean: bool = True,
) -> dict[str, Any]:
    batch_dir = _require_review_destination(batch_dir, repo_root)
    reviewed_output_path = _require_review_input(reviewed_output_path, repo_root)
    review_decisions_path = _require_review_input(review_decisions_path, repo_root)
    if judge_review_path is not None:
        judge_review_path = _require_review_input(judge_review_path, repo_root)
    with _batch_lock(repo_root):
        state = _validate_batch_runtime(
            batch_dir,
            repo_root=repo_root,
            require_clean=require_clean,
        )
        manifest = state["_manifest"]
        if state.get("overall_state") not in {
            "awaiting_maintainer_review",
            "ready_for_explicit_promotion",
        }:
            raise ValueError("model output must be assembled before review validation")
        report_path = batch_dir / "comparison-report.json"
        if state.get("overall_state") == "ready_for_explicit_promotion":
            review_manifest = _load_review_validation_manifest(batch_dir, state)
            _verify_review_validation_files(
                batch_dir=batch_dir,
                manifest=review_manifest,
                review_decisions_path=review_decisions_path,
                judge_review_path=judge_review_path,
                reviewed_input_path=reviewed_output_path,
            )
            return {
                "schema": BATCH_STATE_SCHEMA,
                "status": "unchanged",
                "batch_id": state["batch_id"],
                "overall_state": state["overall_state"],
                "destination": str(report_path),
            }

        started = time.monotonic()
        normalized_reviewed_path = batch_dir / "validated-reviewed-output.json"
        merge_source_native_legacy_migration_outputs(
            input_path=batch_dir / "migration-input.jsonl",
            batch_paths=[reviewed_output_path],
            destination=normalized_reviewed_path,
        )
        generated = _read_json(batch_dir / "generated-output.json")
        reviewed = _read_json(normalized_reviewed_path)
        migration_inputs = list(read_jsonl(batch_dir / "migration-input.jsonl"))
        expected_records = {
            str(row["candidate_id"]): str(row["source_snapshot"]["source_record_id"])
            for row in migration_inputs
        }
        decisions = _validate_review_decisions(
            decisions_path=review_decisions_path,
            generated=generated,
            reviewed=reviewed,
            expected_records=expected_records,
            judge_review_path=judge_review_path,
        )
        comparison = compare_migration_outputs(generated, reviewed)
        artifact_counts = Counter(
            str(artifact.get("artifact_type") or "")
            for article in reviewed.get("articles") or []
            for artifact in article.get("artifacts") or []
        )
        legacy_counts = Counter(
            str(decision.get("disposition") or "")
            for article in reviewed.get("articles") or []
            for decision in article.get("legacy_decisions") or []
        )
        source_unit_count = sum(
            len(row.get("source_units") or []) for row in migration_inputs
        )
        verification_request_count = sum(
            len(article.get("verification_requests") or [])
            for article in reviewed.get("articles") or []
        )
        report = {
            "schema": BATCH_COMPARISON_SCHEMA,
            "status": "ready_for_explicit_promotion",
            "batch_identity": {
                "batch_id": state["batch_id"],
                "base_commit": manifest["git"]["base_commit"],
                "priority_input_hash": manifest["priority"]["input_hash"],
                "selection_hash": manifest["selection_hash"],
            },
            "scope": {
                "article_count": len(migration_inputs),
                "source_unit_count": source_unit_count,
                "artifact_count": sum(artifact_counts.values()),
                "artifact_type_counts": dict(sorted(artifact_counts.items())),
                "legacy_decision_count": sum(legacy_counts.values()),
                "legacy_disposition_counts": dict(sorted(legacy_counts.items())),
            },
            "review_metrics": {
                **comparison,
                "explicit_review_decision_count": len(decisions),
                "adjudication_count": sum(
                    len(row.get("adjudications") or []) for row in decisions
                ),
            },
            "verification_metrics": {
                "request_count": verification_request_count,
                "unresolved_count": verification_request_count,
            },
            "throughput": {
                "prepare_duration": state["phases"]["prepare"]["duration"],
                "assemble_duration": state["phases"]["assemble"]["duration"],
                "review_validation_duration": {
                    "value": round(time.monotonic() - started, 3),
                    "unit": "seconds",
                    "evidence_status": "measured",
                },
                "end_to_end_duration": {
                    "value": None,
                    "unit": "seconds",
                    "evidence_status": "unavailable",
                    "reason": "Active maintainer review time is not captured.",
                },
            },
            "cost": state["model_metrics"],
            "gates": {
                "exact_article_coverage": "passed",
                "schema_validation": "passed",
                "explicit_article_review": "passed",
                "promotion_executed": False,
                "public_retrieval_changed": False,
            },
        }
        _atomic_json(report_path, report)
        generation_model = str((state.get("generated_output") or {}).get("model") or "")
        if not generation_model:
            raise ValueError("assembled model provenance is missing")
        review_manifest_payload = {
            "batch_id": state["batch_id"],
            "generation_model": generation_model,
            "files": {
                "generated_output_sha256": sha256_file(
                    batch_dir / "generated-output.json"
                ),
                "reviewed_input_sha256": sha256_file(reviewed_output_path),
                "validated_reviewed_output_sha256": sha256_file(
                    normalized_reviewed_path
                ),
                "review_decisions_sha256": sha256_file(review_decisions_path),
                "judge_review_sha256": (
                    sha256_file(judge_review_path) if judge_review_path else None
                ),
                "comparison_report_sha256": sha256_file(report_path),
            },
            "reviewers": sorted({str(row["reviewer"]) for row in decisions}),
            "reviewed_at": sorted({str(row["reviewed_at"]) for row in decisions}),
        }
        validation_id = _review_validation_manifest_id(review_manifest_payload)
        _atomic_json(
            batch_dir / "review-validation-manifest.json",
            {
                "schema": BATCH_REVIEW_VALIDATION_MANIFEST_SCHEMA,
                "validation_id": validation_id,
                **review_manifest_payload,
            },
        )
        state["review_validation_manifest_id"] = validation_id
        state["phases"]["validate_review"] = {
            "status": "passed",
            "duration": report["throughput"]["review_validation_duration"],
        }
        state["overall_state"] = "ready_for_explicit_promotion"
        state["promotion_permitted"] = False
        _write_batch_state(batch_dir, state)
    return {
        "schema": BATCH_STATE_SCHEMA,
        "status": "ok",
        "batch_id": state["batch_id"],
        "overall_state": state["overall_state"],
        "article_count": report["scope"]["article_count"],
        "changed_article_count": comparison["changed_article_count"],
        "correction_count": comparison["correction_count"],
        "verification_blocker_count": report["verification_metrics"][
            "unresolved_count"
        ],
        "destination": str(report_path),
    }


def _promotion_journal_path(destination: Path) -> Path:
    return destination.parent / f".{destination.name}.promotion-journal.json"


def _validated_journal_sibling(value: str, destination: Path, label: str) -> Path:
    path = Path(value).resolve()
    parent = destination.parent.resolve()
    if path.parent != parent or not path.name.startswith(f".{destination.name}."):
        raise ValueError(f"promotion journal contains an invalid {label} path")
    return path


def _recover_source_native_promotion(destination: Path) -> None:
    destination = destination.resolve()
    journal_path = _promotion_journal_path(destination)
    journal_path.with_name(f".{journal_path.name}.tmp").unlink(missing_ok=True)
    if not journal_path.exists():
        for orphan in destination.parent.glob(
            f".{destination.name}.promotion-staging-*"
        ):
            if orphan.is_dir():
                shutil.rmtree(orphan)
        return
    journal = _read_json(journal_path)
    if journal.get("schema") != "rock-kb-source-native-promotion-journal-v1":
        raise ValueError("unsupported source-native promotion journal")
    if Path(str(journal.get("destination") or "")).resolve() != destination:
        raise ValueError("source-native promotion journal destination changed")
    staging = _validated_journal_sibling(
        str(journal.get("staging") or ""), destination, "staging"
    )
    backup_value = str(journal.get("backup") or "")
    backup = (
        _validated_journal_sibling(backup_value, destination, "backup")
        if backup_value
        else None
    )

    if destination.exists():
        if backup and backup.exists():
            shutil.rmtree(backup)
    elif backup and backup.exists():
        backup.replace(destination)
    elif journal.get("phase") == "new_installed":
        raise ValueError("completed promotion destination disappeared")
    if staging.exists():
        shutil.rmtree(staging)
    journal_path.unlink(missing_ok=True)


def _promote_source_native_migration_transactionally(
    *,
    input_path: Path,
    output_path: Path,
    destination: Path,
    base_dir: Path,
    reviewer: str,
    model: str,
    reviewed_at: str,
    generated_output_path: Path,
) -> dict[str, Any]:
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    _recover_source_native_promotion(destination)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.promotion-staging-",
            dir=destination.parent,
        )
    ).resolve()
    backup = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.promotion-backup-",
            dir=destination.parent,
        )
    ).resolve()
    backup.rmdir()
    journal_path = _promotion_journal_path(destination)
    try:
        result = promote_source_native_legacy_migration(
            input_path=input_path,
            output_path=output_path,
            destination=staging,
            base_dir=base_dir,
            reviewer=reviewer,
            model=model,
            reviewed_at=reviewed_at,
            generated_output_path=generated_output_path,
        )
        journal = {
            "schema": "rock-kb-source-native-promotion-journal-v1",
            "phase": "staged",
            "destination": str(destination),
            "staging": str(staging),
            "backup": str(backup) if destination.exists() else None,
        }
        _atomic_json(journal_path, journal)
        if destination.exists():
            destination.replace(backup)
            journal["phase"] = "old_moved"
            _atomic_json(journal_path, journal)
        staging.replace(destination)
        journal["phase"] = "new_installed"
        _atomic_json(journal_path, journal)
        if backup.exists():
            shutil.rmtree(backup)
        journal_path.unlink(missing_ok=True)
        return {**result, "destination": str(destination)}
    except Exception:
        _recover_source_native_promotion(destination)
        if staging.exists():
            shutil.rmtree(staging)
        raise


def promote_validated_source_native_migration_batch(
    *,
    batch_dir: Path,
    review_decisions_path: Path,
    destination: Path,
    base_dir: Path,
    reviewer: str,
    model: str,
    reviewed_at: str,
    judge_review_path: Path | None = None,
    repo_root: Path = REPO_ROOT,
    require_clean: bool = True,
) -> dict[str, Any]:
    """Explicitly promote only the exact output bound by batch review validation."""

    batch_dir = _require_review_destination(batch_dir, repo_root)
    review_decisions_path = _require_review_input(review_decisions_path, repo_root)
    if judge_review_path is not None:
        judge_review_path = _require_review_input(judge_review_path, repo_root)
    with _batch_lock(repo_root):
        state = _validate_batch_runtime(
            batch_dir,
            repo_root=repo_root,
            require_clean=require_clean,
        )
        if state.get("overall_state") != "ready_for_explicit_promotion":
            raise ValueError("batch review is not ready for explicit promotion")
        validation = _load_review_validation_manifest(batch_dir, state)
        reviewed_output = batch_dir / "validated-reviewed-output.json"
        generated_output = batch_dir / "generated-output.json"
        _verify_review_validation_files(
            batch_dir=batch_dir,
            manifest=validation,
            review_decisions_path=review_decisions_path,
            judge_review_path=judge_review_path,
        )
        if validation.get("generation_model") != model:
            raise ValueError("promotion model must match sealed generation provenance")

        generated = _read_json(generated_output)
        reviewed = _read_json(reviewed_output)
        migration_inputs = list(read_jsonl(batch_dir / "migration-input.jsonl"))
        expected_records = {
            str(row["candidate_id"]): str(row["source_snapshot"]["source_record_id"])
            for row in migration_inputs
        }
        decisions = _validate_review_decisions(
            decisions_path=review_decisions_path,
            generated=generated,
            reviewed=reviewed,
            expected_records=expected_records,
            judge_review_path=judge_review_path,
        )
        if {str(decision["reviewer"]) for decision in decisions} != {reviewer}:
            raise ValueError("promotion reviewer must match every article review")
        if {str(decision["reviewed_at"]) for decision in decisions} != {reviewed_at}:
            raise ValueError("promotion timestamp must match every article review")
        if validation.get("reviewers") != [reviewer]:
            raise ValueError("sealed review manifest has different reviewers")
        if validation.get("reviewed_at") != [reviewed_at]:
            raise ValueError("sealed review manifest has different review timestamps")

        result = _promote_source_native_migration_transactionally(
            input_path=batch_dir / "migration-input.jsonl",
            output_path=reviewed_output,
            destination=destination,
            base_dir=base_dir,
            reviewer=reviewer,
            model=model,
            reviewed_at=reviewed_at,
            generated_output_path=generated_output,
        )
    return {
        **result,
        "batch_id": state["batch_id"],
        "review_validation_id": validation["validation_id"],
        "review_decisions_sha256": validation["files"]["review_decisions_sha256"],
        "comparison_report_sha256": validation["files"]["comparison_report_sha256"],
    }
