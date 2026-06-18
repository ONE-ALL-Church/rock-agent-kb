from __future__ import annotations

from ._shared import *  # noqa: F401,F403


def build_section_status_rows(
    concept_id: str,
    section_rows: list[dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for row in section_rows:
        sources = [source_index[key] for key in row.get("source_keys") or [] if key in source_index]
        status = "current"
        reasons = []
        if row.get("confidence") == "needs-citation":
            status = "needs-review"
            reasons.append("section_needs_citation")
        if row.get("confidence") == "community-supported":
            reasons.append("community_supported_only")
        if row.get("needs_live_verification"):
            reasons.append("needs_live_verification")
        rows.append(
            {
                "concept_id": concept_id,
                "section_id": row["section_id"],
                "heading": row["heading"],
                "status": status,
                "reasons": reasons or ["source_hashes_current"],
                "depends_on_sources": [
                    {
                        "source_key": source.get("source_key"),
                        "source_id": source.get("source_id"),
                        "source_record_id": source.get("source_record_id"),
                        "url": source.get("url"),
                        "content_hash": source.get("content_hash"),
                        "excerpt_hash": source.get("excerpt_hash"),
                        "authority": source.get("authority"),
                    }
                    for source in sources
                ],
            }
        )
    return rows

def build_troubleshooting_tree(
    concept_id: str,
    task_cards: list[dict[str, Any]],
    section_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    branches = []
    for card in task_cards:
        branches.append(
            {
                "id": card["task_id"],
                "title": card["title"],
                "when": card["goal"],
                "start_with": card.get("steps", [])[:2],
                "inspect": card.get("live_records") or [],
                "entities": card.get("entities") or [],
                "do_not_assume": card.get("do_not_assume") or [],
                "source_urls": card.get("source_urls") or [],
            }
        )
    return {
        "concept_id": concept_id,
        "generated_at": generated_at_iso(),
        "entrypoint": "Choose the branch whose symptom matches the user's task, then inspect the live records before making changes.",
        "guide_sections": [row["section_id"] for row in section_rows if "troubleshooting" in row["section_id"] or "agent-task" in row["section_id"]],
        "branches": branches,
    }

def inferred_task_templates(guide_text: str) -> list[dict[str, Any]]:
    templates = []
    in_agent_recipes = False
    for line in guide_text.splitlines():
        if line.startswith("## ") and "Agent Task" in line:
            in_agent_recipes = True
            continue
        if in_agent_recipes and line.startswith("## "):
            break
        if in_agent_recipes and line.startswith("### "):
            title = clean_heading(line.removeprefix("### "))
            templates.append(
                {
                    "id": slugify(title),
                    "title": title,
                    "goal": f"Follow the guide section for {title}.",
                    "guide_sections": ["Agent Task Recipes"],
                    "steps": ["Read the linked guide section.", "Inspect live Rock records before making changes.", "Cite exact source URLs in the final answer."],
                    "do_not_assume": ["Do not treat generated guidance as live-instance proof."],
                    "source_keywords": title.split(),
                }
            )
    return templates

def audit_guide_quality(
    concept_id: str,
    guide_text: str,
    section_rows: list[dict[str, Any]],
    dependency: dict[str, Any],
    task_cards: list[dict[str, Any]],
    entity_rows: Optional[list[dict[str, Any]]] = None,
    pack: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    word_count = count_words(guide_text)
    source_authorities = {source.get("authority") for source in dependency.get("sources") or []}
    entity_rows = entity_rows or []
    pack = pack or {}
    contribution_records = pack.get("contribution_records") or []
    private_draft_records = pack.get("private_draft_contribution_records") or []
    checks = [
        check("min_words", word_count >= 7000, f"Guide has {word_count} words; expected at least 7000."),
        check("min_sections", len(section_rows) >= 35, f"Guide has {len(section_rows)} sections; expected at least 35."),
        check("official_sources", bool(source_authorities & {"official", "official-developer"}), "Guide should cite official documentation/developer docs."),
        check("release_sources", "official-release" in source_authorities, "Guide should cite release notes."),
        check("source_code", "source-code" in source_authorities, "Guide should cite source code."),
        check("community_marked", "community-example" in source_authorities or "community-answer" in source_authorities, "Guide should include community examples as examples."),
        check("task_cards", len(task_cards) >= 5, f"Guide has {len(task_cards)} task cards; expected at least 5."),
        check("entity_coverage", len(entity_rows) >= 8, f"Guide has {len(entity_rows)} entity rows; expected at least 8."),
        check("low_uncited_sections", uncited_section_ratio(section_rows) <= 0.35, "Too many substantive sections have no citations."),
    ]
    checks.extend(contribution_quality_checks(guide_text, contribution_records, private_draft_records))
    failures = [item for item in checks if not item["passed"]]
    score = int(100 * (len(checks) - len(failures)) / len(checks))
    is_starter_guide = "guide_status: starter_needs_review" in guide_text[:1000]
    return {
        "concept_id": concept_id,
        "status": "pass" if not failures else "starter" if is_starter_guide else "fail",
        "score": score,
        "generated_at": generated_at_iso(),
        "guide_word_count": word_count,
        "guide_line_count": len(guide_text.splitlines()),
        "section_count": len(section_rows),
        "source_count": len(dependency.get("sources") or []),
        "contribution_record_count": len(contribution_records),
        "private_draft_contribution_record_count": len(private_draft_records),
        "authority_coverage": sorted(authority for authority in source_authorities if authority),
        "task_card_count": len(task_cards),
        "entity_count": len(entity_rows),
        "checks": checks,
    }

def contribution_quality_checks(
    guide_text: str,
    contribution_records: list[dict[str, Any]],
    private_draft_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks = []
    if contribution_records:
        traceable = all(record.get("source_urls") or record.get("source_record_ids") for record in contribution_records)
        checks.append(
            check(
                "contribution_traceability",
                traceable,
                "Reviewed public contribution records must include source URLs or source record IDs.",
            )
        )
        checks.append(
            check(
                "contribution_not_official",
                guide_labels_contribution_examples(guide_text),
                "Guides using org/community contributions must label them as examples, patterns, or non-official guidance.",
            )
        )
        needs_live = any(record.get("needs_live_verification") for record in contribution_records)
        checks.append(
            check(
                "contribution_live_verification",
                not needs_live or needs_live_verification(guide_text),
                "Contribution-influenced guides that need live verification must tell agents what to verify.",
            )
        )
    if private_draft_records:
        checks.append(
            check(
                "private_draft_guardrail",
                "private draft" in guide_text.lower() or "live verification" in guide_text.lower(),
                "Private draft records require explicit private/local guardrails and live-verification language.",
            )
        )
    return checks

def guide_labels_contribution_examples(guide_text: str) -> bool:
    lowered = guide_text.lower()
    return (
        ("contribution" in lowered or "community" in lowered or "org" in lowered or "organization" in lowered)
        and ("example" in lowered or "pattern" in lowered or "not official" in lowered or "official" in lowered)
    )

def needs_live_verification(text: str) -> bool:
    lowered = text.lower()
    markers = ["inspect", "verify", "live rock", "live instance", "test", "do not assume", "check the rock version"]
    return any(marker in lowered for marker in markers)

def uncited_section_ratio(section_rows: list[dict[str, Any]]) -> float:
    substantive = [row for row in section_rows if int(row.get("word_count") or 0) >= 80]
    if not substantive:
        return 0
    uncited = [row for row in substantive if int(row.get("citation_count") or 0) == 0]
    return len(uncited) / len(substantive)
