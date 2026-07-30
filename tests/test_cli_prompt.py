import json

from rock_kb.cli import candidate_ids_from_file, comprehensive_required_sections
from rock_kb.cli._legacy import concept_synthesis_prompt, stamp_synthesized_guide_provenance
from rock_kb.concepts import get_concept


def test_groups_comprehensive_outline_is_group_specific():
    concept = get_concept("groups").raw
    outline = comprehensive_required_sections(concept)
    assert "Group Types Deep Dive" in outline
    assert "Group Finder Deep Dive" in outline
    assert "Group Attendance Deep Dive" in outline
    assert "Related Rock Areas: People, Attendance, Security, Locations, Schedules" in outline
    assert "Running Check-In And Check-Out" not in outline
    assert "Labels, Security Codes, Pickup, And Label Data" not in outline


def test_comprehensive_outline_uses_registry_subguides():
    concept = get_concept("check-in").raw
    outline = comprehensive_required_sections(concept)
    assert "Labels Deep Dive" in outline
    assert "Mobile Check-In Deep Dive" in outline
    assert "Attendance Deep Dive" in outline


def test_candidate_ids_from_file_reads_jsonl_and_plain_ids(tmp_path):
    path = tmp_path / "ids.jsonl"
    path.write_text(
        json.dumps({"candidate_id": "media-public-candidate:a"}) + "\n"
        + "media-public-candidate:b\n"
        + json.dumps({"id": "media-public-candidate:c"}) + "\n"
        + json.dumps({"candidate_id": "media-public-candidate:a"}) + "\n",
        encoding="utf-8",
    )

    assert candidate_ids_from_file(path) == [
        "media-public-candidate:a",
        "media-public-candidate:b",
        "media-public-candidate:c",
    ]


def test_concept_synthesis_prompt_uses_versioned_bounded_claim_first_contract():
    prompt = concept_synthesis_prompt(
        {
            "concept": {"id": "workflows", "title": "Workflows"},
            "synthesis_profile": "standard",
            "approved_claims": [],
            "routing_context": [],
            "evidence_policy": {},
        }
    )

    assert "Prompt version: `2.0.0`" in prompt
    assert "Approved answer-bearing claims are the factual spine" in prompt
    assert "separate bounded" in prompt
    assert "10,000" not in prompt
    assert "18,000" not in prompt


def test_stamp_synthesized_guide_provenance(tmp_path):
    path = tmp_path / "guide.md"
    path.write_text(
        "---\nid: authored-workflows\ntitle: Workflows\n---\n\n# Workflows\n",
        encoding="utf-8",
    )

    stamp_synthesized_guide_provenance(
        path,
        model="gpt-5.6-sol",
        reasoning_effort="xhigh",
        source_pack_hash="abc123",
    )

    text = path.read_text(encoding="utf-8")
    assert 'synthesis_model: "gpt-5.6-sol"' in text
    assert 'synthesis_reasoning_effort: "xhigh"' in text
    assert 'synthesis_prompt_version: "2.0.0"' in text
    assert 'synthesis_source_pack_hash: "abc123"' in text
