import json

from rock_kb.cli import candidate_ids_from_file, comprehensive_required_sections
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
