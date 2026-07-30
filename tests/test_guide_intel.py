from rock_kb.guide_intel import (
    audit_guide_quality,
    authority_for_source_id,
    build_entity_rows,
    build_source_index,
    build_task_cards,
    build_troubleshooting_tree,
    entity_search_terms,
    guide_synthesis_provenance,
    parse_markdown_sections,
    release_caveat_rows,
    section_source_map,
    source_id_for_url,
)
from rock_kb.guide_intel.manifest import concept_knowledge_quality


def test_parse_markdown_sections_tracks_parent_and_lines():
    markdown = "# Title\n\n## Parent\n\nText.\n\n### Child\n\nMore text."

    sections = parse_markdown_sections(markdown)

    assert len(sections) == 2
    assert sections[0].heading == "Parent"
    assert sections[0].level == 2
    assert sections[1].heading == "Child"
    assert sections[1].parent == "Parent"


def test_task_cards_use_authored_recipe_steps():
    markdown = (
        "## Agent Task Recipes\n\n"
        "### Recipe: Diagnose A Stalled Workflow\n\n"
        "Find the first action that did not complete.\n\n"
        "1. Inspect the Workflow record and its current activity.\n"
        "2. Compare the configured action order with the execution log.\n"
        "3. Stop when the failing action and evidence are identified.\n\n"
        "**Do not assume:**\n"
        "- The last visible action caused the failure.\n"
        "- A retry is safe merely because the workflow remains active."
    )
    section_rows = section_source_map("workflows", parse_markdown_sections(markdown), {})

    cards = build_task_cards("workflows", markdown, section_rows, {})

    assert len(cards) == 1
    assert cards[0]["task_id"] == "recipe-diagnose-a-stalled-workflow"
    assert cards[0]["steps"][0].startswith("Inspect the Workflow record")
    assert len(cards[0]["steps"]) == 3
    assert cards[0]["goal"] == "Find the first action that did not complete."
    assert cards[0]["do_not_assume"] == [
        "The last visible action caused the failure.",
        "A retry is safe merely because the workflow remains active.",
    ]


def test_troubleshooting_tree_uses_authored_symptom_branches():
    markdown = (
        "## Troubleshooting Decision Tree\n\n"
        "### Workflow Is Stuck In Processing\n\n"
        "1. Inspect the Workflow and current activity.\n"
        "2. Check the configured action and its completion state. "
        "[Workflow Actions](https://community.rockrms.com/documentation/workflow-actions)\n\n"
        "Do not assume the last visible action caused the failure."
    )
    section_rows = section_source_map("workflows", parse_markdown_sections(markdown), {})

    tree = build_troubleshooting_tree("workflows", markdown, [], section_rows)

    assert [row["title"] for row in tree["branches"]] == ["Workflow Is Stuck In Processing"]
    assert tree["branches"][0]["start_with"][0].startswith("Inspect the Workflow")
    assert tree["branches"][0]["start_with"][1] == "Check the configured action and its completion state."
    assert tree["branches"][0]["guide_section_id"]


def test_guide_synthesis_provenance_prefers_stamped_frontmatter():
    guide = (
        "---\n"
        'synthesis_model: "gpt-5.6-sol"\n'
        'synthesis_reasoning_effort: "xhigh"\n'
        'synthesis_prompt_id: "rock-kb-concept-guide-synthesis"\n'
        'synthesis_prompt_version: "2.0.0"\n'
        'synthesis_source_pack_hash: "abc123"\n'
        "---\n\n# Workflows\n"
    )

    provenance = guide_synthesis_provenance(
        guide,
        {"synthesis_request": {"model": "old-model", "prompt_version": "1.0.0"}},
    )

    assert provenance == {
        "model": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "prompt_id": "rock-kb-concept-guide-synthesis",
        "prompt_version": "2.0.0",
        "source_pack_hash": "abc123",
    }


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


def test_concept_knowledge_quality_separates_answer_value_from_artifact_completeness():
    claims = [
        {
            "claim_id": "claim:answer",
            "concept_ids": ["workflows"],
            "primary_concept_id": "workflows",
            "claim_tier": "answer_pack_approved",
            "claim_type": "configuration",
            "rock_versions": ["19.0"],
            "version_scope_status": "scoped",
            "source_refs": [{"url": "https://example.test"}],
        },
        {
            "claim_id": "claim:routing",
            "concept_ids": ["workflows"],
            "primary_concept_id": "workflows",
            "claim_tier": "routing_context_only",
            "claim_type": "source_summary",
            "rock_versions": [],
            "version_scope_status": "unprocessed",
            "source_refs": [{"url": "https://example.test"}],
        },
    ]

    quality = concept_knowledge_quality("workflows", claims, [])
    secondary_only = concept_knowledge_quality(
        "system-admin-ops",
        [{**claims[0], "concept_ids": ["system-admin-ops"], "primary_concept_id": "workflows"}],
        [],
    )

    assert quality["metrics"]["answer_bearing_rate"] == 0.5
    assert quality["metrics"]["version_scope_rate"] == 1.0
    assert quality["metrics"]["retrieval_evaluation_status"] == "pending_service"
    assert quality["score"] < 100
    assert secondary_only["status"] == "needs_coverage"
    assert secondary_only["score"] <= 49


def test_audit_guide_quality_marks_explicit_starter_guides():
    markdown = "---\nguide_status: starter_needs_review\n---\n\n## Tiny\n\nNo citations."
    sections = section_source_map("check-in", parse_markdown_sections(markdown), {})

    audit = audit_guide_quality("check-in", markdown, sections, {"sources": []}, [])

    assert audit["status"] == "starter"
    assert any(check["id"] == "min_words" and not check["passed"] for check in audit["checks"])


def test_audit_guide_quality_requires_community_label_only_when_community_sources_exist():
    markdown = ("## Official Only\n\nOfficial docs and source code cover this. " * 900)
    sections = section_source_map("obsidian-development", parse_markdown_sections(markdown), {})
    dependency = {
        "sources": [
            {"authority": "official-developer"},
            {"authority": "official-release"},
            {"authority": "source-code"},
        ]
    }

    official_audit = audit_guide_quality("obsidian-development", markdown, sections, dependency, [{}] * 5, [{}] * 8)

    assert "community_marked" not in {check["id"] for check in official_audit["checks"]}

    community_dependency = {"sources": [*dependency["sources"], {"authority": "community-example"}]}

    community_audit = audit_guide_quality("obsidian-development", markdown, sections, community_dependency, [{}] * 5, [{}] * 8)

    checks = {check["id"]: check["passed"] for check in community_audit["checks"]}
    assert checks["community_marked"] is False


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
