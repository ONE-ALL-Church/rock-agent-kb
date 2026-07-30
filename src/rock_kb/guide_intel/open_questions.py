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
    guide_text: str,
    task_cards: list[dict[str, Any]],
    section_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    rows_by_heading = {str(row.get("heading") or ""): row for row in section_rows}
    sections = [
        section
        for section in parse_markdown_sections(guide_text)
        if section.level == 3 and "troubleshooting" in section.parent.lower()
    ]
    branches = []
    for section in sections:
        row = rows_by_heading.get(section.heading) or {}
        checks = action_items(section.text)
        branches.append(
            {
                "id": slugify(section.heading),
                "title": section.heading,
                "when": section.heading,
                "start_with": checks[:8],
                "inspect": mentioned_entities(section.text),
                "entities": mentioned_entities(section.text),
                "do_not_assume": caution_items(section.text),
                "source_urls": compact_unique(
                    citation.get("url")
                    for citation in row.get("citations") or []
                    if citation.get("url")
                ),
                "guide_section_id": row.get("section_id"),
            }
        )
    if not branches:
        branches = [
            {
                "id": card["task_id"],
                "title": card["title"],
                "when": card["goal"],
                "start_with": card.get("steps", [])[:4],
                "inspect": card.get("live_records") or [],
                "entities": card.get("entities") or [],
                "do_not_assume": card.get("do_not_assume") or [],
                "source_urls": card.get("source_urls") or [],
            }
            for card in task_cards
        ]
    return {
        "concept_id": concept_id,
        "generated_at": generated_at_iso(),
        "entrypoint": "Choose the branch whose symptom matches the user's task, then inspect the live records before making changes.",
        "guide_sections": [row["section_id"] for row in section_rows if "troubleshooting" in row["section_id"] or "agent-task" in row["section_id"]],
        "branches": branches,
    }

def inferred_task_templates(guide_text: str) -> list[dict[str, Any]]:
    templates = []
    sections = [
        section
        for section in parse_markdown_sections(guide_text)
        if section.level == 3 and "agent task" in section.parent.lower()
    ]
    for section in sections:
        title = section.heading
        steps = action_items(section.text)
        if not steps:
            continue
        templates.append(
            {
                "id": slugify(title),
                "title": title,
                "goal": task_goal(title, section.text),
                "guide_sections": [section.parent or "Agent Task Recipes"],
                "steps": steps[:16],
                "do_not_assume": caution_items(section.text)
                or ["Do not treat generated guidance as live-instance proof."],
                "entities": mentioned_entities(section.text),
                "live_records": mentioned_entities(section.text),
                "source_keywords": [title, *mentioned_entities(section.text)],
            }
        )
    return templates

def action_items(text: str) -> list[str]:
    ordered = extract_list_items(text, ordered_only=True)
    return ordered or extract_list_items(text, ordered_only=False)

def extract_list_items(text: str, *, ordered_only: bool) -> list[str]:
    rows = []
    seen: set[str] = set()
    pattern = re.compile(r"^\s*\d+[.)]\s+(.+)$") if ordered_only else re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$")
    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        value = clean_action_text(match.group(1))
        key = value.lower()
        if value and key not in seen:
            seen.add(key)
            rows.append(value)
    return rows

def clean_action_text(value: str) -> str:
    value = re.sub(r"\s*\[[^\]]+\]\([^)]+\)\s*$", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"^\*{0,2}(?:Outcome|Goal):\*{0,2}\s*", "", value, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", value).strip()

def caution_items(text: str) -> list[str]:
    rows = labeled_list_items(text, "do not assume")
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
        value = clean_action_text(re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", sentence))
        value = re.sub(r"^\*{0,2}Do not assume:\*{0,2}\s*", "", value, flags=re.IGNORECASE)
        lowered = value.lower()
        if value and any(marker in lowered for marker in ["do not ", "don't ", "never ", "avoid "]):
            rows.append(value)
    return compact_unique(rows)[:8]

def labeled_list_items(text: str, label: str) -> list[str]:
    rows = []
    capturing = False
    label_re = re.compile(rf"^\*{{0,2}}{re.escape(label)}:\*{{0,2}}\s*(.*)$", re.IGNORECASE)
    list_re = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$")
    for line in text.splitlines():
        stripped = line.strip()
        match = label_re.match(stripped)
        if match:
            capturing = True
            inline = clean_action_text(match.group(1))
            if inline:
                rows.append(inline)
            continue
        if not capturing or not stripped:
            continue
        list_match = list_re.match(line)
        if list_match:
            rows.append(clean_action_text(list_match.group(1)))
            continue
        break
    return rows

def task_goal(title: str, text: str) -> str:
    for line in text.splitlines():
        value = clean_action_text(line)
        if not value or value.endswith(":") or re.match(r"^(?:[-*]|\d+[.)])\s+", line):
            continue
        if value.startswith("[") or value.lower().startswith(("use ", "official ", "community ")):
            continue
        return value
    task = re.sub(r"^Recipe:\s*", "", title, flags=re.IGNORECASE)
    return f"Complete {task} with evidence-backed checks and a verifiable outcome."

def mentioned_entities(text: str) -> list[str]:
    lowered = text.lower()
    return compact_unique(
        entity
        for entity in KNOWN_ENTITY_TERMS
        if any(term.lower() in lowered for term in [entity, *ENTITY_ALIASES.get(entity, [])])
    )[:12]

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
    answer_claims = [
        row
        for row in pack.get("approved_claims") or []
        if str(row.get("claim_tier") or "") in {"source_backed", "answer_pack_approved", "live_verified"}
    ]
    available_source_ids = {
        str(row.get("source_id") or "")
        for row in pack.get("source_records") or []
        if row.get("source_id")
    }
    actionable_ratio = actionable_task_card_ratio(task_cards)
    uncited_ratio = uncited_section_ratio(section_rows)
    claim_reference_count = guide_claim_reference_count(guide_text, answer_claims)
    checks = [
        check("min_words", word_count >= 1200, f"Guide has {word_count} words; expected at least 1200."),
        check("bounded_length", word_count <= 9000, f"Guide has {word_count} words; expected no more than 9000."),
        check("min_sections", len(section_rows) >= 9, f"Guide has {len(section_rows)} sections; expected at least 9."),
        check("official_sources", bool(source_authorities & {"official", "official-developer"}), "Guide should cite official documentation/developer docs."),
        check("task_cards", len(task_cards) >= 3, f"Guide has {len(task_cards)} task cards; expected at least 3."),
        check("actionable_task_cards", actionable_ratio >= 0.8, "Task cards must contain concrete steps."),
        check("entity_coverage", len(entity_rows) >= 3, f"Guide has {len(entity_rows)} entity rows; expected at least 3."),
        check("low_uncited_sections", uncited_ratio <= 0.25, "Too many substantive sections have no citations."),
        check(
            "troubleshooting_structure",
            any("troubleshooting" in str(row.get("parent") or row.get("heading") or "").lower() for row in section_rows),
            "Guide should include evidence-backed troubleshooting branches.",
        ),
    ]
    if available_source_ids & {"rock_core_release_notes", "rock_mobile_release_notes"}:
        checks.append(check("release_sources", "official-release" in source_authorities, "Available release notes should be cited."))
    if pack.get("github_source_files"):
        checks.append(check("source_code", "source-code" in source_authorities, "Available source code should be cited."))
    if answer_claims:
        checks.append(
            check(
                "claim_first_evidence",
                claim_reference_count >= min(8, len(answer_claims)),
                "Guide should visibly ground its factual spine in approved answer-bearing claims.",
            )
        )
    if source_authorities & {"community-example", "community-answer"}:
        checks.append(
            check(
                "community_marked",
                guide_labels_contribution_examples(guide_text),
                "Guides using community sources must label them as examples or patterns, not official guidance.",
            )
        )
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
        "metrics": {
            "word_count": word_count,
            "section_count": len(section_rows),
            "source_count": len(dependency.get("sources") or []),
            "task_card_count": len(task_cards),
            "actionable_task_card_ratio": round(actionable_ratio, 4),
            "substantive_uncited_section_ratio": round(uncited_ratio, 4),
            "answer_claim_count_in_pack": len(answer_claims),
            "answer_claim_reference_count": claim_reference_count,
            "entity_count": len(entity_rows),
        },
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

def actionable_task_card_ratio(task_cards: list[dict[str, Any]]) -> float:
    if not task_cards:
        return 0.0
    actionable = [
        row
        for row in task_cards
        if len(row.get("steps") or []) >= 2
        and not all(str(step).startswith("Read the linked guide section") for step in row.get("steps") or [])
    ]
    return len(actionable) / len(task_cards)

def guide_claim_reference_count(guide_text: str, claims: list[dict[str, Any]]) -> int:
    return sum(
        1
        for row in claims
        if (
            str(row.get("claim_id") or "") in guide_text
            or any(
                str(ref.get("url") or "") in guide_text
                for ref in row.get("source_refs") or []
                if isinstance(ref, dict) and ref.get("url")
            )
            or (
                str(row.get("claim") or "")[:90]
                and str(row.get("claim") or "")[:90] in guide_text
            )
        )
    )
