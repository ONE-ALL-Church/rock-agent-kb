from __future__ import annotations

from ._shared import *  # noqa: F401,F403


@dataclass(frozen=True)
class GuideSection:
    heading: str
    level: int
    start_line: int
    end_line: int
    parent: str
    text: str

def parse_markdown_sections(markdown: str) -> list[GuideSection]:
    lines = markdown.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, len(match.group(1)), clean_heading(match.group(2))))
    sections = []
    for idx, (start, level, heading) in enumerate(headings):
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
        parent = nearest_parent_heading(headings[:idx], level)
        text = "\n".join(lines[start:end]).strip()
        sections.append(GuideSection(heading=heading, level=level, start_line=start, end_line=end, parent=parent, text=text))
    return sections

def section_source_map(
    concept_id: str,
    sections: list[GuideSection],
    source_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for section in sections:
        citations = extract_citations(section.text)
        matched_sources = [match_source_for_url(url, source_index) for _, url in citations]
        matched_sources = [source for source in matched_sources if source]
        if not matched_sources and section.heading == "Generated Model Map Pointers":
            matched_sources = [model_map_pointer_source()]
        for source in matched_sources:
            add_source(source_index, source)
        authorities = sorted({source["authority"] for source in matched_sources})
        confidence = confidence_for_section(section, matched_sources)
        rows.append(
            {
                "concept_id": concept_id,
                "section_id": slugify(f"{section.parent} {section.heading}" if section.parent else section.heading),
                "heading": section.heading,
                "parent": section.parent,
                "level": section.level,
                "start_line": section.start_line,
                "end_line": section.end_line,
                "word_count": count_words(section.text),
                "citation_count": len(citations),
                "citations": [{"label": label, "url": url} for label, url in citations],
                "direct_source_keys": [source["source_key"] for source in matched_sources],
                "source_keys": [source["source_key"] for source in matched_sources],
                "source_record_ids": compact_unique(source.get("source_record_id") for source in matched_sources),
                "source_ids": compact_unique(source.get("source_id") for source in matched_sources),
                "authorities": authorities,
                "trace_mode": "direct" if matched_sources else "none",
                "confidence": confidence,
                "needs_live_verification": needs_live_verification(section.text),
            }
        )
    return add_inherited_section_traceability(rows, source_index)

def add_inherited_section_traceability(
    rows: list[dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows_by_heading = {row["heading"]: row for row in rows}
    last_traced_row: Optional[dict[str, Any]] = None
    for row in rows:
        if row.get("source_keys"):
            last_traced_row = row
            continue
        inherited_from = None
        parent = row.get("parent")
        if parent and rows_by_heading.get(parent, {}).get("source_keys"):
            inherited_from = rows_by_heading[parent]
            row["trace_mode"] = "inherited_parent"
        elif last_traced_row and int(row.get("word_count") or 0) >= 20:
            inherited_from = last_traced_row
            row["trace_mode"] = "inherited_previous"
        if not inherited_from:
            continue
        row["source_keys"] = list(inherited_from.get("source_keys") or [])
        row["inherited_from_section_id"] = inherited_from.get("section_id")
        inherited_sources = [source_index[key] for key in row["source_keys"] if key in source_index]
        row["source_record_ids"] = compact_unique(source.get("source_record_id") for source in inherited_sources)
        row["source_ids"] = compact_unique(source.get("source_id") for source in inherited_sources)
        row["authorities"] = sorted({source.get("authority") for source in inherited_sources if source.get("authority")})
    for row in rows:
        if row.get("source_keys"):
            continue
        child_keys = compact_unique(
            key
            for child in rows
            if child.get("parent") == row.get("heading")
            for key in child.get("source_keys") or []
        )
        if not child_keys:
            continue
        row["source_keys"] = child_keys
        row["trace_mode"] = "inherited_children"
        inherited_sources = [source_index[key] for key in child_keys if key in source_index]
        row["source_record_ids"] = compact_unique(source.get("source_record_id") for source in inherited_sources)
        row["source_ids"] = compact_unique(source.get("source_id") for source in inherited_sources)
        row["authorities"] = sorted({source.get("authority") for source in inherited_sources if source.get("authority")})
    return rows

def source_keys_for_keywords(
    keywords: list[str],
    section_rows: list[dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
    limit: int = 12,
) -> list[str]:
    scored: dict[str, int] = {}
    terms = [term.lower() for term in keywords if term]
    for row in section_rows:
        haystack = " ".join([row.get("heading") or "", row.get("parent") or ""]).lower()
        score = sum(1 for term in terms if term.lower() in haystack)
        if score:
            for key in row.get("source_keys") or []:
                scored[key] = scored.get(key, 0) + score + int(source_index.get(key, {}).get("authority_score") or 0)
    for key, source in source_index.items():
        haystack = " ".join(str(source.get(field) or "") for field in ["title", "url", "path"]).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            scored[key] = scored.get(key, 0) + score + int(source.get("authority_score") or 0)
    return [key for key, _ in sorted(scored.items(), key=lambda item: (-item[1], item[0]))[:limit]]

def confidence_for_section(section: GuideSection, sources: list[dict[str, Any]]) -> str:
    if not sources:
        return "needs-citation" if count_words(section.text) > 80 else "structural"
    authorities = {source.get("authority") for source in sources}
    if "official" in authorities and ("source-code" in authorities or "official-release" in authorities):
        return "high"
    if authorities & {"official", "official-developer", "official-release", "source-code"}:
        return "normal"
    if authorities & {"community-example", "community-answer", "community-reference", "org-contribution"}:
        return "community-supported"
    return "citation-only"

def sections_mentioning(guide_text: str, section_rows: list[dict[str, Any]], terms: list[str]) -> list[str]:
    if not terms:
        return []
    lines = guide_text.splitlines()
    output = []
    lowered_terms = [term.lower() for term in terms if term]
    for row in section_rows:
        section_text = "\n".join(lines[int(row["start_line"]) - 1 : int(row["end_line"])]).lower()
        if any(term in section_text for term in lowered_terms):
            output.append(row["section_id"])
    return output[:12]

def nearest_parent_heading(previous: list[tuple[int, int, str]], level: int) -> str:
    for _, candidate_level, heading in reversed(previous):
        if candidate_level < level:
            return heading
    return ""

def clean_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().strip("#").strip()
