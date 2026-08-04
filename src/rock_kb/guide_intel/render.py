from __future__ import annotations

from ._shared import *  # noqa: F401,F403


def render_task_card(card: dict[str, Any]) -> str:
    lines = [
        "---",
        f"concept_id: {card['concept_id']}",
        f"task_id: {card['task_id']}",
        f"title: {card['title']}",
        "generated: true",
        "---",
        "",
        f"# {card['title']}",
        "",
        card["goal"],
        "",
        "## When To Use",
        "",
        "- Use this when the user's task matches this operational symptom or implementation path.",
        "- Verify live Rock records before making changes.",
        "",
        "## Live Records To Inspect",
        "",
    ]
    lines.extend(f"- `{value}`" for value in card.get("live_records") or ["Guide section"])
    lines.extend(["", "## Entities And Tables", ""])
    lines.extend(f"- `{value}`" for value in card.get("entities") or ["See guide"])
    lines.extend(["", "## Steps", ""])
    lines.extend(f"{index}. {step}" for index, step in enumerate(card.get("steps") or [], start=1))
    lines.extend(["", "## Do Not Assume", ""])
    lines.extend(f"- {item}" for item in card.get("do_not_assume") or ["Do not assume generated guidance proves live-instance state."])
    lines.extend(["", "## Source Links", ""])
    lines.extend(f"- {url}" for url in card.get("source_urls") or [])
    lines.append("")
    return "\n".join(line.rstrip() for line in lines)

def render_quickstart(
    concept_id: str,
    guide_text: str,
    section_rows: list[dict[str, Any]],
    task_cards: list[dict[str, Any]],
    entity_rows: list[dict[str, Any]],
    release_rows: list[dict[str, Any]],
) -> str:
    concept = get_concept(concept_id)
    high_signal_sections = high_signal_section_rows(section_rows)
    lines = [
        "---",
        f"concept_id: {concept_id}",
        f"title: {concept.title} Quickstart",
        "generated: true",
        "---",
        "",
        f"# {concept.title} Quickstart",
        "",
        concept.description,
        "",
        "## Agent Entry Points",
        "",
        "- Start with a task card when the user has an operational symptom or implementation request.",
        "- Use the entity index when the task mentions a table, model, block, source file, or report.",
        "- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.",
        "- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.",
        "- Use the long guide only when planning broadly or when the task card points to a section.",
        "",
        "## Primary Tasks",
        "",
    ]
    lines.extend(f"- [{card['title']}](tasks/{card['task_id']}.md): {card['goal']}" for card in task_cards)
    lines.extend(["", "## High-Signal Sections", ""])
    lines.extend(
        f"- `{row['section_id']}` lines {row['start_line']}-{row['end_line']}: {row['heading']} ({row['confidence']})"
        for row in high_signal_sections
    )
    lines.extend(["", "## Core Entities", ""])
    lines.extend(f"- `{row['entity']}`: {row['purpose']}" for row in entity_rows[:12])
    lines.extend(["", "## Version Caveats", ""])
    for row in release_rows[:8]:
        version = row.get("version") or "unknown version"
        summary = str(row.get("summary") or "").strip()
        lines.append(f"- `{version}`: {summary[:220]}")
    lines.extend(["", "## Files For Agents", ""])
    lines.extend(
        [
            "- `guide.md`: long-form guide.",
            "- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.",
            "- `entities.jsonl`: concept-specific entity/model/table map.",
            "- `section-source-map.jsonl`: section citations and source authority.",
            "- `section-status.jsonl`: section review/staleness hints.",
            "- `release-caveats.jsonl`: version-specific source rows.",
            "- `troubleshooting-tree.json`: machine-readable branch selector.",
        ]
    )
    lines.append("")
    return "\n".join(line.rstrip() for line in lines)

def render_agent_cheatsheet(
    concept_id: str,
    section_rows: list[dict[str, Any]],
    task_cards: list[dict[str, Any]],
    entity_rows: list[dict[str, Any]],
    release_rows: list[dict[str, Any]],
) -> str:
    concept = get_concept(concept_id)
    lines = [
        "---",
        f"concept_id: {concept_id}",
        f"title: {concept.title} Agent Cheatsheet",
        "generated: true",
        "---",
        "",
        f"# {concept.title} Agent Cheatsheet",
        "",
        "## Tasks",
        "",
        "| Task | Inspect | Entities |",
        "| --- | --- | --- |",
    ]
    for card in task_cards:
        inspect = ", ".join(f"`{item}`" for item in card.get("live_records") or [])
        entities = ", ".join(f"`{item}`" for item in card.get("entities") or [])
        lines.append(f"| [{escape_pipe(card['title'])}](tasks/{card['task_id']}.md) | {escape_pipe(inspect)} | {escape_pipe(entities)} |")
    lines.extend(["", "## Entities", "", "| Entity | Common Joins | Agent Notes |", "| --- | --- | --- |"])
    for row in entity_rows:
        joins = ", ".join(f"`{item}`" for item in row.get("common_joins") or [])
        notes = " ".join(row.get("agent_notes") or [])[:220]
        lines.append(f"| `{escape_pipe(row['entity'])}` | {escape_pipe(joins)} | {escape_pipe(notes)} |")
    lines.extend(["", "## Release Caveats", "", "| Version | Channel | Summary |", "| --- | --- | --- |"])
    for row in release_rows[:20]:
        lines.append(
            f"| `{escape_pipe(str(row.get('version') or ''))}` | {escape_pipe(str(row.get('channel') or ''))} | {escape_pipe(str(row.get('summary') or '')[:240])} |"
        )
    lines.extend(["", "## Sections Needing Review", "", "| Section | Confidence | Reason |", "| --- | --- | --- |"])
    for row in section_rows:
        if row.get("confidence") in {"needs-citation", "community-supported"} or row.get("needs_live_verification"):
            reason = "live verification" if row.get("needs_live_verification") else row.get("confidence")
            lines.append(f"| `{row['section_id']}` | {row.get('confidence')} | {reason} |")
    lines.append("")
    return "\n".join(line.rstrip() for line in lines)

def render_open_questions(concept_id: str, section_rows: list[dict[str, Any]]) -> str:
    concept = get_concept(concept_id)
    needs_citation = [row for row in section_rows if row.get("confidence") == "needs-citation"]
    community_only = [row for row in section_rows if row.get("confidence") == "community-supported"]
    live_verify = [row for row in section_rows if row.get("needs_live_verification")]
    lines = [
        "---",
        f"concept_id: {concept_id}",
        f"title: {concept.title} Open Questions",
        "generated: true",
        "---",
        "",
        f"# {concept.title} Open Questions",
        "",
        "This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.",
        "",
        "## Needs Citation",
        "",
    ]
    lines.extend(f"- `{row['section_id']}`: {row['heading']} ({row['word_count']} words)" for row in needs_citation[:30])
    lines.extend(["", "## Community-Supported Only", ""])
    lines.extend(f"- `{row['section_id']}`: {row['heading']}" for row in community_only[:30])
    lines.extend(["", "## Needs Live Verification", ""])
    lines.extend(f"- `{row['section_id']}`: {row['heading']}" for row in live_verify[:40])
    if live_verify:
        lines.extend(
            [
                "",
                "## Live Verification Clarification",
                "",
                "Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.",
                "",
                "Schema corrections from the 2026-06-07 read-only production/source pass:",
                "",
                "- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.",
                "- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.",
                "- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.",
                "- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.",
                "- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.",
                "- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.",
                "- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.",
                "",
                "Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.",
            ]
        )
    lines.append("")
    return "\n".join(line.rstrip() for line in lines)
