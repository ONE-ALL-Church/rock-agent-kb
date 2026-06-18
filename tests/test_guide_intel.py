from rock_kb.guide_intel import (
    audit_guide_quality,
    authority_for_source_id,
    build_entity_rows,
    build_source_index,
    entity_search_terms,
    parse_markdown_sections,
    release_caveat_rows,
    section_source_map,
    source_id_for_url,
)


def test_parse_markdown_sections_tracks_parent_and_lines():
    markdown = "# Title\n\n## Parent\n\nText.\n\n### Child\n\nMore text."

    sections = parse_markdown_sections(markdown)

    assert len(sections) == 2
    assert sections[0].heading == "Parent"
    assert sections[0].level == 2
    assert sections[1].heading == "Child"
    assert sections[1].parent == "Parent"


def test_section_source_map_links_citations_to_pack_sources():
    pack = {
        "source_records": [
            {
                "id": "doc:1",
                "source_id": "rock_documentation",
                "source_title": "Checking-out Check-in",
                "source_url": "https://community.rockrms.com/documentation/bookcontent/10/266",
                "content_hash": "abc",
            }
        ],
        "github_source_files": [
            {
                "repo": "SparkDevNetwork/Rock",
                "path": "Rock/CheckIn/v2/Labels/AttendanceLabelData.cs",
                "url": "https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs",
                "content_hash": "def",
            }
        ],
    }
    source_index = build_source_index(pack)
    markdown = (
        "## Labels\n\n"
        "Official docs are useful ([docs](https://community.rockrms.com/documentation/bookcontent/10/266)). "
        "Source code confirms label behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs))."
    )

    rows = section_source_map("check-in", parse_markdown_sections(markdown), source_index)

    assert rows[0]["citation_count"] == 2
    assert "rock_documentation" in rows[0]["source_ids"]
    assert "sparkdevnetwork_rock" in rows[0]["source_ids"]
    assert rows[0]["confidence"] == "high"


def test_build_source_index_includes_org_contributions():
    pack = {
        "contribution_records": [
            {
                "id": "org_contribution:org:workflow-pattern",
                "source_id": "org_contribution",
                "source_title": "Workflow Pattern",
                "source_url": "https://community.rockrms.com/documentation",
                "content_hash": "abc",
                "contribution_id": "org:workflow-pattern",
                "contribution_type": "guide_section",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "needs_live_verification": True,
            }
        ]
    }

    source_index = build_source_index(pack)
    source = next(iter(source_index.values()))

    assert source["source_id"] == "org_contribution"
    assert source["authority"] == "org-contribution"
    assert source["contribution_id"] == "org:workflow-pattern"


def test_triumph_resources_are_highest_authority():
    assert authority_for_source_id("triumph_resources") == "official-triumph"
    assert source_id_for_url("https://www.triumph.tech/resources/github-spotlight-5212026") == "triumph_resources"


def test_section_source_map_inherits_traceability_from_parent_section():
    pack = {
        "source_records": [
            {
                "id": "doc:1",
                "source_id": "rock_documentation",
                "source_title": "Groups",
                "source_url": "https://community.rockrms.com/documentation/bookcontent/7",
                "content_hash": "abc",
            }
        ]
    }
    source_index = build_source_index(pack)
    markdown = (
        "## Parent\n\n"
        "Official docs explain this. [source](https://community.rockrms.com/documentation/bookcontent/7)\n\n"
        "### Child\n\n"
        "This operational detail belongs to the same cited source context and should not be orphaned."
    )

    rows = section_source_map("groups", parse_markdown_sections(markdown), source_index)

    child = rows[1]
    assert child["source_keys"] == rows[0]["source_keys"]
    assert child["direct_source_keys"] == []
    assert child["trace_mode"] == "inherited_parent"
    assert child["inherited_from_section_id"] == rows[0]["section_id"]


def test_section_source_map_inherits_traceability_from_child_sections():
    pack = {
        "source_records": [
            {
                "id": "doc:1",
                "source_id": "rock_documentation",
                "source_title": "Groups",
                "source_url": "https://community.rockrms.com/documentation/bookcontent/7",
            }
        ]
    }
    source_index = build_source_index(pack)
    markdown = (
        "## Parent\n\n"
        "### Child\n\n"
        "Official docs explain this. [source](https://community.rockrms.com/documentation/bookcontent/7)"
    )

    rows = section_source_map("groups", parse_markdown_sections(markdown), source_index)

    parent = rows[0]
    assert parent["source_keys"] == rows[1]["source_keys"]
    assert parent["trace_mode"] == "inherited_children"


def test_audit_guide_quality_flags_shallow_guides():
    markdown = "## Tiny\n\nNo citations."
    sections = section_source_map("check-in", parse_markdown_sections(markdown), {})

    audit = audit_guide_quality("check-in", markdown, sections, {"sources": []}, [])

    assert audit["status"] == "fail"
    assert any(check["id"] == "min_words" and not check["passed"] for check in audit["checks"])


def test_audit_guide_quality_marks_explicit_starter_guides():
    markdown = "---\nguide_status: starter_needs_review\n---\n\n## Tiny\n\nNo citations."
    sections = section_source_map("check-in", parse_markdown_sections(markdown), {})

    audit = audit_guide_quality("check-in", markdown, sections, {"sources": []}, [])

    assert audit["status"] == "starter"
    assert any(check["id"] == "min_words" and not check["passed"] for check in audit["checks"])


def test_audit_guide_quality_checks_contribution_guardrails():
    markdown = (
        ("## Contribution Examples\n\n"
         "Community and organization contribution patterns are examples, not official guidance. "
         "Agents should verify behavior in a live Rock instance before changing configuration. "
         "[source](https://community.rockrms.com/documentation)\n\n")
        * 900
    )
    pack = {
        "contribution_records": [
            {
                "id": "org_contribution:org:workflow-pattern",
                "source_id": "org_contribution",
                "source_title": "Workflow Pattern",
                "source_url": "https://community.rockrms.com/documentation",
                "content_hash": "abc",
                "contribution_id": "org:workflow-pattern",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "needs_live_verification": True,
            }
        ]
    }
    source_index = build_source_index(pack)
    sections = section_source_map("workflows", parse_markdown_sections(markdown), source_index)
    dependency = {"sources": list(source_index.values())}

    audit = audit_guide_quality("workflows", markdown, sections, dependency, [{}] * 5, [{}] * 8, pack)

    checks = {check["id"]: check["passed"] for check in audit["checks"]}
    assert checks["contribution_traceability"]
    assert checks["contribution_not_official"]
    assert checks["contribution_live_verification"]


def test_build_entity_rows_maps_entities_to_tasks_and_sections():
    markdown = (
        "## Reporting\n\n"
        "Join `Attendance` to `AttendanceOccurrence` before reporting. "
        "[source](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_Attendees.sql)"
    )
    pack = {
        "github_source_files": [
            {
                "repo": "SparkDevNetwork/Rock",
                "path": "database/Procedures/spCheckin_AttendanceAnalyticsQuery_Attendees.sql",
                "url": "https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_Attendees.sql",
            }
        ]
    }
    source_index = build_source_index(pack)
    section_rows = section_source_map("check-in", parse_markdown_sections(markdown), source_index)
    task_cards = [{"task_id": "build-attendance-report", "entities": ["Attendance"], "live_records": []}]

    rows = build_entity_rows("check-in", markdown, section_rows, task_cards, source_index)

    attendance = next(row for row in rows if row["entity"] == "Attendance")
    assert "build-attendance-report" in attendance["task_ids"]
    assert attendance["used_by_sections"]


def test_build_entity_rows_falls_back_to_mentioning_section_sources():
    markdown = (
        "## Data Model\n\n"
        "AttendanceOccurrence is the meeting context. "
        "[source](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_Attendees.sql)"
    )
    pack = {
        "github_source_files": [
            {
                "repo": "SparkDevNetwork/Rock",
                "path": "database/Procedures/spCheckin_AttendanceAnalyticsQuery_Attendees.sql",
                "url": "https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_Attendees.sql",
            }
        ]
    }
    source_index = build_source_index(pack)
    section_rows = section_source_map("check-in", parse_markdown_sections(markdown), source_index)

    rows = build_entity_rows("check-in", markdown, section_rows, [], source_index)

    occurrence = next(row for row in rows if row["entity"] == "AttendanceOccurrence")
    assert occurrence["source_keys"]


def test_entity_search_terms_include_human_aliases():
    assert "Group Type" in entity_search_terms("GroupType")
    assert "Kiosk" in entity_search_terms("Device/Kiosk")


def test_release_caveats_only_emit_source_backed_rows():
    guide = "## Versions\n\nRock v18.3 matters here, but v99 is only mentioned."
    sections = section_source_map("groups", parse_markdown_sections(guide), {})
    pack = {
        "source_records": [
            {
                "id": "release:1",
                "source_id": "rock_core_release_notes",
                "source_url": "https://www.rockrms.com/releasenotes",
                "version": "18.3",
                "release_date": "May 20, 2026",
                "module": "Groups",
                "change_type": "bug_fix",
                "severity": "normal",
                "summary": "Fixed group behavior.",
            }
        ]
    }

    rows = release_caveat_rows("groups", guide, pack, sections)

    assert [row["version"] for row in rows] == ["18.3"]
    assert rows[0]["source_url"] == "https://www.rockrms.com/releasenotes"
