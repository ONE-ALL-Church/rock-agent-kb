from __future__ import annotations

from ._shared import *  # noqa: F401,F403


def selected_records_for_concept(concept_id: str, limit: int = 40) -> list[dict[str, Any]]:
    concept = get_concept(concept_id)
    records = concept_source_records()
    ranked = rank_records_for_concept(concept, records)
    return ensure_weighted_source_coverage(concept, ranked, limit)

def concept_source_records(repo_root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    """Return records allowed to influence public concept guides.

    Private transcript-derived media insights must be promoted by review before
    they can affect public guide dependencies or authored synthesis packs.
    """
    records = (
        all_normalized_records()
        if repo_root == REPO_ROOT
        else all_normalized_records(repo_root / "data" / "normalized")
    )
    return public_agent_records(records)

def approved_media_dependencies_for_concept(
    concept_id: str,
    records: Optional[list[dict[str, Any]]] = None,
    guide_text: str = "",
    coverage_text: str = "",
) -> list[dict[str, Any]]:
    concept = get_concept(concept_id)
    source_records = records if records is not None else concept_source_records()
    ranked = rank_records_for_concept(concept, source_records)
    selected = ensure_weighted_source_coverage(concept, ranked, concept.max_records)
    dependencies = []
    search_text = "\n".join(value for value in [guide_text, coverage_text] if value)
    for record in selected:
        if not is_approved_media_insight_record(record):
            continue
        source_url = str(record.get("source_url") or "")
        source_title = str(record.get("source_title") or "")
        insight_urls = [
            str(item.get("source_url") or item.get("source_timestamp_url") or "")
            for item in record.get("key_insights") or []
            if isinstance(item, dict)
        ]
        mentioned = bool(
            search_text
            and (
                (source_url and source_url in search_text)
                or (source_title and source_title in search_text)
                or any(url and url in search_text for url in insight_urls)
            )
        )
        dependencies.append(
            {
                "source_record_id": record.get("id"),
                "source_id": record.get("source_id"),
                "source_title": source_title,
                "source_url": source_url,
                "content_hash": record.get("content_hash"),
                "public_promotion_id": record.get("public_promotion_id"),
                "public_promotion_candidate_id": record.get("public_promotion_candidate_id"),
                "review_status": record.get("review_status"),
                "approved_concept_ids": record.get("approved_concept_ids") or [],
                "key_insight_count": len(record.get("key_insights") or []),
                "mentioned_in_guide": mentioned,
            }
        )
    return dependencies

def is_approved_media_insight_record(record: dict[str, Any]) -> bool:
    return (
        str(record.get("id") or "").startswith("media-insight:")
        and record.get("needs_review") is False
        and str(record.get("review_status") or "") in PUBLIC_MEDIA_REVIEW_STATUSES
        and bool(record.get("key_insights") or record.get("summary"))
    )

def concept_synthesis_pack(
    concept_id: str,
    limit: int = 40,
    include_contributions: bool = True,
) -> dict[str, Any]:
    concept = get_concept(concept_id)
    records = selected_records_for_concept(concept_id, limit=limit)
    contribution_records = public_contribution_records(concept_id) if include_contributions else []
    approved_claims, routing_context = claims_for_concept_synthesis(concept_id)
    return {
        "concept": {
            "id": concept.id,
            "title": concept.title,
            "description": concept.description,
            "depends_on_topics": concept.depends_on_topics,
            "subguides": concept.subguides,
            "routing_role": concept.routing_role,
            "parent_concept_id": concept.parent_concept_id,
            "documentation_branches": record_constraint_values(concept.raw, "documentation_branches"),
            "guide_status": "llm_generated_needs_review",
        },
        "approved_claims": approved_claims,
        "routing_context": routing_context,
        "source_records": [compact_record_for_synthesis(record) for record in records],
        "contribution_records": [compact_record_for_synthesis(record) for record in contribution_records],
        "evidence_policy": concept_synthesis_evidence_policy(),
    }

def concept_synthesis_evidence_policy() -> dict[str, Any]:
    return {
        "factual_spine": "approved_claims",
        "routing_context_is_answer_evidence": False,
        "source_excerpts_require_direct_support": True,
        "public_source_code": {
            "use_when_helpful": True,
            "requires_supplied_excerpt": True,
            "requires_public_commit_ref": True,
            "authority": "implementation_evidence_not_universal_configuration",
        },
        "live_instance_verification": {
            "default": "not_performed",
            "use_when_helpful": True,
            "mode": "separate_bounded_read_only_review",
            "appropriate_for": [
                "installed_schema_or_configuration",
                "version_or_plugin_applicability",
                "issue_reproduction_or_instance_impact",
                "existence_and_count_checks",
            ],
            "prohibited": [
                "sql_writes",
                "raw_private_data_in_public_outputs",
                "treating_one_instance_as_universal_behavior",
            ],
            "public_use_requires_reviewed_safe_conclusion": True,
        },
    }

def claims_for_concept_synthesis(
    concept_id: str,
    *,
    answer_limit: int = 160,
    routing_limit: int = 24,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    dependencies = approved_claim_dependencies_for_concept(concept_id)
    answer_bearing = [
        row
        for row in dependencies
        if str(row.get("claim_tier") or "") in {"source_backed", "answer_pack_approved", "live_verified"}
    ]
    routing = [
        row for row in dependencies if str(row.get("claim_tier") or "") == "routing_context_only"
    ]
    answer_bearing.sort(key=claim_synthesis_sort_key)
    routing.sort(key=claim_synthesis_sort_key)
    return (
        [compact_claim_for_synthesis(row) for row in answer_bearing[:answer_limit]],
        [compact_claim_for_synthesis(row) for row in routing[:routing_limit]],
    )

def claim_synthesis_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
    tier = {"live_verified": 0, "answer_pack_approved": 1, "source_backed": 2}.get(
        str(row.get("claim_tier") or ""),
        3,
    )
    authority = {
        "live-verified": 0,
        "release-note-confirmed": 1,
        "source-code-confirmed": 1,
        "official": 2,
        "rocku-confirmed": 3,
        "community-reviewed": 4,
        "community-unreviewed": 5,
    }.get(str(row.get("authority_tier") or ""), 6)
    return tier, authority, str(row.get("claim_id") or "")

def compact_claim_for_synthesis(row: dict[str, Any]) -> dict[str, Any]:
    keep = [
        "claim_id",
        "claim",
        "claim_type",
        "authority_tier",
        "claim_tier",
        "confidence",
        "rock_versions",
        "version_scope_status",
        "concept_ids",
        "source_record_ids",
        "source_refs",
        "needs_live_verification",
        "live_verification",
    ]
    return {key: row.get(key) for key in keep if row.get(key) not in (None, "", [], {})}

def compact_record_for_synthesis(record: dict[str, Any]) -> dict[str, Any]:
    keep = [
        "id",
        "source_id",
        "source_url",
        "source_title",
        "summary",
        "excerpt",
        "topics",
        "rock_versions",
        "detail_type",
        "module",
        "version",
        "release_date",
        "change_type",
        "severity",
        "model_name",
        "model_category",
        "repo",
        "language",
        "inclusion_reason",
        "recipe_id",
        "question_id",
        "question_category",
        "answer_count",
        "training_section",
        "duration",
        "developer_doc_path",
        "api_related",
        "plugin_id",
        "org_id",
        "org_display_name",
        "contribution_id",
        "contribution_type",
        "source_urls",
        "source_record_ids",
        "source_review_origin",
        "needs_live_verification",
        "bundle_path",
        "publishability_status",
        "private_source_hash_count",
        "private_path_hash_count",
    ]
    return {key: record.get(key) for key in keep if record.get(key) not in (None, "", [], {})}

def synthesis_output_path(concept_id: str) -> Path:
    return KNOWLEDGE_DIR / "concepts" / concept_id / "guide.md"

def rank_records_for_concept(concept: Concept, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = []
    source_record_ids = record_constraint_values(concept.raw, "source_record_ids")
    exact_ids_are_exclusive = source_record_ids and not has_non_record_path_constraints(concept.raw)
    for record in records:
        if exact_ids_are_exclusive and str(record.get("id") or "") not in source_record_ids:
            continue
        if concept_has_path_constraints(concept) and (
            record_is_unmatched_developer_branch(record, concept.raw)
            or record_is_unmatched_documentation_branch(record, concept.raw)
        ):
            continue
        text = record_text(record)
        score = score_text(text, concept.keywords)
        score += concept.source_weights.get(record.get("source_id") or "", 0)
        score += topic_overlap_score(record, concept)
        if record_matches_path_constraints(record, concept.raw):
            score += 10_000
        if concept.id in {str(value) for value in record.get("approved_concept_ids") or []}:
            score += 10_000
        if score > 0:
            scored.append((score, record.get("updated_at") or record.get("retrieved_at") or "", record))
    scored.sort(key=lambda item: (-item[0], item[1], item[2].get("source_title") or ""))
    return [record for _, _, record in scored]

def records_matching_subguide(records: list[dict[str, Any]], subguide: dict[str, Any], keywords: list[str]) -> list[dict[str, Any]]:
    constrained = subguide_has_path_constraints(subguide)
    matched = []
    for record in records:
        if constrained:
            if record_matches_path_constraints(record, subguide):
                matched.append(record)
            continue
        if score_text(record_text(record), keywords) > 0:
            matched.append(record)
    return matched

def concept_has_path_constraints(concept: Concept) -> bool:
    return (
        record_constraint_values(concept.raw, "source_record_ids")
        or record_constraint_values(concept.raw, "source_url_prefixes")
        or record_constraint_values(concept.raw, "developer_doc_prefixes")
        or record_constraint_values(concept.raw, "documentation_branches")
        or record_constraint_values(concept.raw, "documentation_path_prefixes")
    )

def has_non_record_path_constraints(config: dict[str, Any]) -> bool:
    return bool(
        record_constraint_values(config, "source_url_prefixes")
        or record_constraint_values(config, "developer_doc_prefixes")
        or record_constraint_values(config, "documentation_branches")
        or record_constraint_values(config, "documentation_path_prefixes")
    )

def subguide_has_path_constraints(subguide: dict[str, Any]) -> bool:
    return (
        record_constraint_values(subguide, "source_record_ids")
        or record_constraint_values(subguide, "source_url_prefixes")
        or record_constraint_values(subguide, "developer_doc_prefixes")
        or record_constraint_values(subguide, "documentation_branches")
        or record_constraint_values(subguide, "documentation_path_prefixes")
    )

def record_matches_path_constraints(record: dict[str, Any], config: dict[str, Any]) -> bool:
    source_record_ids = record_constraint_values(config, "source_record_ids")
    if str(record.get("id") or "") in source_record_ids:
        return True

    source_url_prefixes = record_constraint_values(config, "source_url_prefixes")
    if source_url_prefixes:
        source_url = str(record.get("source_url") or "")
        if any(source_url.startswith(prefix) for prefix in source_url_prefixes):
            return True

    developer_doc_prefixes = record_constraint_values(config, "developer_doc_prefixes")
    if developer_doc_prefixes:
        doc_path = "/".join(str(part) for part in record.get("developer_doc_path") or [])
        if any(doc_path == prefix or doc_path.startswith(f"{prefix}/") for prefix in developer_doc_prefixes):
            return True

    documentation_branches = record_constraint_values(config, "documentation_branches")
    if documentation_branches:
        record_branches = {
            str(value).rstrip("/")
            for value in [
                record.get("documentation_branch"),
                *(record.get("documentation_branches") or []),
            ]
            if str(value or "").strip()
        }
        if record_branches & set(documentation_branches):
            return True

    documentation_path_prefixes = record_constraint_values(config, "documentation_path_prefixes")
    if documentation_path_prefixes:
        documentation_path = str(record.get("documentation_path") or "").rstrip("/")
        if any(documentation_path == prefix or documentation_path.startswith(f"{prefix}/") for prefix in documentation_path_prefixes):
            return True

    return False

def record_is_unmatched_developer_branch(record: dict[str, Any], config: dict[str, Any]) -> bool:
    source_url = str(record.get("source_url") or "")
    if not source_url.startswith("https://community.rockrms.com/developer"):
        return False
    return not record_matches_path_constraints(record, config)

def record_is_unmatched_documentation_branch(record: dict[str, Any], config: dict[str, Any]) -> bool:
    if not (
        record_constraint_values(config, "documentation_branches")
        or record_constraint_values(config, "documentation_path_prefixes")
    ):
        return False
    source_url = str(record.get("source_url") or "")
    if not (source_url.startswith("https://community.rockrms.com/documentation") or record.get("documentation_family") == "documentation"):
        return False
    return not record_matches_path_constraints(record, config)

def record_constraint_values(config: dict[str, Any], key: str) -> list[str]:
    values = config.get(key) or []
    if isinstance(values, str):
        values = [values]
    return [str(value).rstrip("/") for value in values if str(value or "").strip()]

def ensure_weighted_source_coverage(concept: Concept, ranked: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Keep explicitly weighted authority families from being squeezed out.

    Concept guides need release-note, source-code, and high-authority source
    coverage even when generic keyword ranking favors many records from one
    family. Preserve overall ranking order, but reserve a tiny floor for sources
    the concept registry intentionally weighted.
    """
    required_ids: set[str] = set()
    for source_id, weight in sorted(concept.source_weights.items(), key=lambda item: (-item[1], item[0])):
        if weight < 3:
            continue
        minimum = 2 if source_id in {"rock_core_release_notes", "rock_mobile_release_notes"} else 1
        matches = [record for record in ranked if record.get("source_id") == source_id]
        for record in matches[:minimum]:
            required_ids.add(str(record.get("id")))

    selected_ids: set[str] = set(required_ids)
    for record in ranked:
        if len(selected_ids) >= limit:
            break
        selected_ids.add(str(record.get("id")))
    return [record for record in ranked if str(record.get("id")) in selected_ids][:limit]

def record_text(record: dict[str, Any]) -> str:
    values = [
        record.get("source_title"),
        record.get("source_url"),
        record.get("summary"),
        record.get("excerpt"),
        record.get("detail_type"),
        record.get("module"),
        record.get("model_name"),
        record.get("model_category"),
        record.get("repo"),
        " ".join(record.get("topics") or []),
        " ".join(record.get("rock_versions") or []),
        record.get("documentation_branch"),
        record.get("documentation_path"),
        " ".join(record.get("documentation_branches") or []),
        " ".join(record.get("documentation_path_parts") or []),
    ]
    return " ".join(str(value or "") for value in values).lower()

def score_text(text: str, keywords: list[str]) -> int:
    score = 0
    for keyword in keywords:
        keyword = keyword.lower()
        if " " in keyword or "-" in keyword:
            score += 4 if keyword in text else 0
        else:
            score += len(re.findall(rf"\b{re.escape(keyword)}\b", text))
    return score

def topic_overlap_score(record: dict[str, Any], concept: Concept) -> int:
    topics = {str(topic).lower() for topic in record.get("topics") or []}
    deps = {topic.lower() for topic in concept.depends_on_topics}
    return len(topics & deps)

def top_records(records: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    priority = {
        "triumph_resources": 11,
        "rock_documentation": 10,
        "rock_lava_docs": 10,
        "rock_mobile_docs": 10,
        "rock_api_docs": 10,
        "rock_rocku": 9,
        "rock_youtube": 9,
        "rock_community_blog": 9,
        "rock_developer": 8,
        "rock_model_map": 7,
        "rock_core_release_notes": 6,
        "rock_mobile_release_notes": 6,
        "rock_recipes": 5,
        "rock_qa": 4,
    }
    return sorted(records, key=lambda record: (-priority.get(record.get("source_id"), 0), record.get("source_title") or ""))[:limit]

def count_by(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = record.get(field) or "unknown"
        counts[value] = counts.get(value, 0) + 1
    return counts

def is_reviewed_media_insight(record: dict[str, Any]) -> bool:
    return (
        str(record.get("id") or "").startswith("media-insight:")
        and record.get("needs_review") is False
        and bool(record.get("key_insights") or record.get("summary"))
    )

def score_media_insight_for_keywords(record: dict[str, Any], keywords: list[str]) -> int:
    values = [
        str(record.get("source_title") or ""),
        str(record.get("source_url") or ""),
        " ".join(record.get("topics") or []),
    ]
    for item in record.get("key_insights") or []:
        if isinstance(item, dict):
            values.append(str(item.get("topic") or ""))
        else:
            values.append(str(item or ""))
    return score_text(" ".join(values).lower(), keywords)
