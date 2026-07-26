from __future__ import annotations

import json
from pathlib import Path

from rock_kb import lava_contexts
from rock_kb.lava_contexts import (
    SourceSnapshot,
    build_lava_context_version_diffs,
    combine_versioned_context_rows,
    discover_lava_context_candidates,
    get_lava_context_surface,
    get_lava_context_version_diff,
    lava_context_rows,
    list_lava_context_surfaces,
    normalize_context_rows,
    parse_common_merge_fields,
    parse_communication_merge_values,
    parse_curated_surface_contexts,
    parse_label_data,
    parse_person_label_data,
    parse_workflow_merge_fields,
    validate_lava_context_extension,
    validate_private_lava_context_overlay,
)


def test_parse_common_merge_fields_links_person_model(monkeypatch):
    monkeypatch.setattr(
        lava_contexts,
        "model_map_links_by_slug",
        lambda: {
            "person": [
                {
                    "model_slug": "person",
                    "model_name": "Person",
                    "model_title": "Person",
                    "model_detail_path": "knowledge/model-map/models/person.md",
                }
            ]
        },
    )
    source = """
public static Dictionary<string, object> GetCommonMergeFields()
{
    var mergeFields = new Dictionary<string, object>();
    mergeFields.Add( "PageParameter", rockPage.PageParameters() );
    mergeFields.Add( "CurrentPerson", currentPerson );
}
"""

    rows = lava_context_rows({"lava_helper": source})
    by_key = {row["root_key"]: row for row in rows}

    assert by_key["CurrentPerson"]["schema"] == "rock-kb-lava-context-v3"
    assert by_key["CurrentPerson"]["model_slug"] == "person"
    assert by_key["CurrentPerson"]["model_map_links"][0]["model_detail_path"] == "knowledge/model-map/models/person.md"
    assert by_key["PageParameter"]["needs_live_verification"] is True
    assert by_key["CurrentPerson"]["source_url"].endswith("#L6")


def test_parse_person_label_data_includes_roots_and_nested_paths():
    source = """
internal class PersonLabelData : ILabelDataHasPerson
{
    public Person Person { get; }
    public List<LabelAttendanceDetail> PersonAttendance { get; }
    public Group Family { get; }
    public string SecurityCode { get; }
    public List<string> GroupNames { get; }

    public PersonLabelData()
    {
        GroupNames = PersonAttendance.Select( a => a.Group.Name ).ToList();
        LocationNames = PersonAttendance.Select( a => a.Location.Name ).ToList();
        ScheduleNames = PersonAttendance.Select( a => a.Schedule.Name ).ToList();
    }
}
"""

    rows = parse_person_label_data(source)
    keys = {(row["root_key"], row["nested_path"]) for row in rows}

    assert ("Person", "") in keys
    assert ("PersonAttendance", "") in keys
    assert ("SecurityCode", "") in keys
    assert ("PersonAttendance", "PersonAttendance.Group") in keys
    assert ("PersonAttendance", "PersonAttendance.Location") in keys
    assert ("PersonAttendance", "PersonAttendance.Schedule") in keys
    assert next(row for row in rows if row["root_key"] == "Family")["model_slug"] == "group"


def test_versioned_contexts_remain_canonical_and_emit_typed_diffs(monkeypatch):
    monkeypatch.setattr(lava_contexts, "model_map_links_by_slug", lambda: {})
    base = {
        "context_id": "example-surface",
        "context_family": "lava",
        "surface_name": "Example",
        "surface_type": "template",
        "concept_ids": ["lava"],
        "root_key": "Person",
        "nested_path": "",
        "source_symbol": "Example.Render",
        "source_id": "sparkdevnetwork_rock",
        "source_file": "Example.cs",
        "source_line_start": 10,
        "source_line_end": 10,
        "source_ref": "release-19.0",
        "source_commit": "a",
        "source_commit_date": "2026-01-01T00:00:00Z",
        "source_url": "https://github.com/SparkDevNetwork/Rock/blob/a/Example.cs#L10",
        "source_version": "19.0.11",
        "root_type": "Rock.Model.Person",
        "model_slug": "person",
        "value_kind": "object",
        "availability": "source-code-confirmed",
        "availability_condition": "always",
        "may_be_null": False,
        "required_setting": "",
        "execution_phase": "render",
        "needs_live_verification": False,
        "includes_context_ids": [],
        "coverage_status": "complete_for_source_snapshot",
        "model_map_links": [],
        "notes": "Fixture.",
    }
    changed = {
        **base,
        "source_ref": "develop",
        "source_commit": "b",
        "source_version": "20.0.5",
        "source_url": "https://github.com/SparkDevNetwork/Rock/blob/b/Example.cs#L12",
        "source_line_start": 12,
        "source_line_end": 12,
        "root_type": "Rock.Model.PersonAlias",
        "model_slug": "person-alias",
        "availability_condition": "feature_enabled",
    }

    rows = combine_versioned_context_rows({"19.0.11": [base], "20.0.5": [changed]})
    result = get_lava_context_surface(rows, "example-surface", rock_version="19.0")
    diff = get_lava_context_version_diff(rows, "19", "20")

    assert len(rows) == 1
    assert rows[0]["available_in_versions"] == ["19.0.11", "20.0.5"]
    assert rows[0]["first_seen_version"] == "19.0.11"
    assert result["roots"][0]["root_type"] == "Rock.Model.Person"
    assert result["surface"]["selected_rock_version"] == "19.0.11"
    assert {row["change_type"] for row in diff["changes"]} == {"type_changed", "condition_changed"}
    assert len(build_lava_context_version_diffs(rows)) == 2


def test_parse_all_check_in_label_surfaces_keeps_roots_separate():
    fixtures = {
        "attendance_label_data": """
public LabelAttendanceDetail Attendance { get; set; }
public Person Person => Attendance.Person;
public NamedLocationCache Location => Attendance.Location;
public List<LabelAttendanceDetail> PersonAttendance { get; set; }
""",
        "family_label_data": """
public List<LabelAttendanceDetail> AllAttendance { get; }
public Group Family { get; }
public List<string> NickNames { get; set; }
""",
        "checkout_label_data": """
public LabelAttendanceDetail Attendance { get; set; }
public Person Person => Attendance.Person;
public DateTime CheckoutDateTime { get; }
""",
        "person_location_label_data": """
public Person Person { get; }
public NamedLocationCache Location { get; }
public List<LabelAttendanceDetail> LocationAttendance { get; }
""",
    }
    expected = {
        "attendance_label_data": ("check-in-label-attendance-dynamic-text", "PersonAttendance"),
        "family_label_data": ("check-in-label-family-dynamic-text", "NickNames"),
        "checkout_label_data": ("check-in-label-checkout-dynamic-text", "CheckoutDateTime"),
        "person_location_label_data": ("check-in-label-person-location-dynamic-text", "LocationAttendance"),
    }

    for source_key, text in fixtures.items():
        context_id, required_root = expected[source_key]
        rows = parse_label_data(source_key, text, context_id, context_id)
        assert {row["context_id"] for row in rows} == {context_id}
        assert required_root in {row["root_key"] for row in rows}

    checkout_rows = parse_label_data(
        "checkout_label_data",
        fixtures["checkout_label_data"],
        "check-in-label-checkout-dynamic-text",
        "Checkout",
    )
    assert "Family" not in {row["root_key"] for row in checkout_rows}


def test_parse_communication_merge_values_tracks_dynamic_additional_fields():
    source = """
public Dictionary<string, object> CommunicationMergeValues( Dictionary<string, object> globalConfigValues )
{
    mergeValues.Add( "Communication", this.Communication );
    mergeValues.Add( "Person", this.PersonAlias.Person );
    mergeValues.Add( entityTypeType.Name, mergeEntity );
}
"""

    rows = parse_communication_merge_values(source)
    by_key = {row["root_key"]: row for row in rows}

    assert by_key["Communication"]["model_slug"] == "communication"
    assert by_key["Person"]["model_slug"] == "person"
    assert by_key["AdditionalMergeValues"]["value_kind"] == "dynamic"
    assert by_key["AdditionalMergeValues"]["needs_live_verification"] is True


def test_parse_workflow_merge_fields_extracts_action_activity_workflow():
    source = """
protected Dictionary<string, object> GetMergeFields( WorkflowAction action )
{
    var mergeFields = Lava.LavaHelper.GetCommonMergeFields( null );
    mergeFields.Add( "Action", action );
    mergeFields.Add( "Activity", action.Activity );
    mergeFields.Add( "Workflow", action.Activity.Workflow );
}
"""

    rows = parse_workflow_merge_fields(source)
    by_key = {row["root_key"]: row for row in rows}

    assert by_key["Action"]["model_slug"] == "workflow-action"
    assert by_key["Activity"]["model_slug"] == "workflow-activity"
    assert by_key["Workflow"]["model_slug"] == "workflow"


def test_parse_curated_surface_contexts_covers_v2_context_families():
    rows = parse_curated_surface_contexts(
        {
            "content_channel_view": """
itemMergeFields["Item"] = item;
mergeFields.TryAdd( "Person", RequestContext.CurrentPerson );
["Items"] = currentPageContent,
""",
            "mobile_prayer_session": """
mergeFields.Add( "SessionContext", Encryption.EncryptString( sessionContext.ToJson() ) );
mergeFields.Add( "Request", request );
""",
            "workflow_entry": """
mergeFields.Add( "Action", action );
mergeFields.Add( "Activity", activity );
mergeFields.Add( "Workflow", workflow );
mergeFields.Add( "Item", workflowType );
""",
            "registrant_waitlist_move": """
{ MergeFieldKey.RegistrationInstance, registrationInstance },
{ MergeFieldKey.TransitionedRegistrants, transitionedRegistrants },
""",
            "group_detail_lava": 'mergeFields.Add( "AllowedActions", securityActions );',
            "calendar_lava": 'mergeFields.Add( "EventItemOccurrences", eventOccurrenceSummaries );',
            "event_item_occurrence_lava": 'mergeFields.Add( "Event", eventItemOccurrence.EventItem );',
            "realtime_visualizer": 'mergeFields.AddOrReplace( "Args", LavaHelper.JavaScriptObjectToLavaObject( arguments ) );',
            "following_by_entity_lava": 'mergeFields.Add( "FollowingItems", items.Take( quantity ) );',
            "motivators": """
mergeFields.Add( "Person", targetPerson );
mergeFields.Add( "MotivatorScores", results.MotivatorScores );
""",
            "fundraising_opportunity_view": """
mergeFields.Add( "RegistrationInstance", registrationInstance );
mergeFields.Add( "GroupMember", groupMember );
""",
            "transaction_entry_v2": """
mergeFields.Add( "ScheduledTransactions", scheduledTransactionList );
mergeFields.Add( "PaymentDetail", financialPaymentDetail );
mergeFields.Add( "TransactionAccountDetails", commentTransactionAccountDetails );
""",
        }
    )

    keys = {(row["context_family"], row["context_id"], row["root_key"]) for row in rows}

    assert ("cms-block", "cms-content-channel-view-template", "Items") in keys
    assert ("mobile-block", "mobile-prayer-session-template", "Request") in keys
    assert ("workflow", "workflow-entry-form-template", "Workflow") in keys
    assert ("event-registration", "event-registrant-waitlist-transition-template", "TransitionedRegistrants") in keys
    assert ("group-lava", "group-detail-lava-template", "AllowedActions") in keys
    assert ("event-lava", "calendar-lava-template", "EventItemOccurrences") in keys
    assert ("utility-lava", "realtime-visualizer-message-template", "Args") in keys
    assert ("following", "following-by-entity-lava-template", "FollowingItems") in keys
    assert ("assessment-lava", "motivators-assessment-template", "MotivatorScores") in keys
    assert ("finance-lava", "transaction-entry-payment-comment-template", "TransactionAccountDetails") in keys
    assert next(row for row in rows if row["root_key"] == "Request")["model_slug"] == "prayer-request"
    assert next(row for row in rows if row["root_key"] == "PaymentDetail")["model_slug"] == "financial-payment-detail"
    fundraising_rows = [row for row in rows if row["context_id"] == "fundraising-opportunity-template"]
    assert fundraising_rows
    assert {row["source_file"] for row in fundraising_rows} == {
        "Rock.Blocks/Fundraising/FundraisingOpportunityView.cs"
    }
    assert {row["source_symbol"] for row in fundraising_rows} == {
        "FundraisingOpportunityView.GetFundraisingOpportunityBox"
    }


def test_lava_context_rows_have_stable_required_fields(monkeypatch):
    monkeypatch.setattr(lava_contexts, "model_map_links_by_slug", lambda: {})
    rows = lava_context_rows(
        {
            "lava_helper": 'mergeFields.Add( "CurrentPerson", currentPerson );',
            "communication_recipient": 'mergeValues.Add( "Communication", this.Communication );',
            "workflow_action": """
protected Dictionary<string, object> GetMergeFields( WorkflowAction action )
{
    mergeFields.Add( "Workflow", action.Activity.Workflow );
}
""",
        }
    )

    assert rows
    assert all(row["id"].startswith("lava_context:") for row in rows)
    assert all(row["source_url"].startswith("https://github.com/SparkDevNetwork/Rock/blob/develop/") for row in rows)
    assert len({(row["context_id"], row["root_key"], row["nested_path"], row["source_symbol"]) for row in rows}) == len(rows)


def test_context_ids_survive_line_moves_and_preserve_legacy_id(monkeypatch):
    monkeypatch.setattr(lava_contexts, "model_map_links_by_slug", lambda: {})
    source_a = 'mergeFields.Add( "CurrentPerson", currentPerson );'
    source_b = '\n\nmergeFields.Add( "CurrentPerson", currentPerson );'
    snapshot = SourceSnapshot(
        source_ref="develop",
        source_commit="a" * 40,
        source_commit_date="2026-07-26T00:00:00Z",
        source_version="20.0.5",
    )

    first = lava_context_rows({"lava_helper": source_a}, snapshot=snapshot)[0]
    second = lava_context_rows({"lava_helper": source_b}, snapshot=snapshot, previous_rows=[first])[0]

    assert first["id"] == second["id"]
    assert first["source_line_start"] != second["source_line_start"]
    assert first["id"] not in second["legacy_ids"]
    assert set(first["legacy_ids"]) <= set(second["legacy_ids"])
    assert second["source_url"].startswith(
        "https://github.com/SparkDevNetwork/Rock/blob/" + "a" * 40
    )
    assert second["source_version"] == "20.0.5"
    assert second["first_seen_version"] == "20.0.5"


def test_grouped_surface_lookup_returns_direct_and_inherited_roots():
    rows = normalize_context_rows(
        [
            {
                "context_id": "global-common",
                "context_family": "global",
                "surface_name": "Global",
                "surface_type": "common",
                "concept_ids": ["lava"],
                "root_key": "CurrentPerson",
                "root_type": "Rock.Model.Person",
                "model_slug": "person",
                "value_kind": "object",
                "nested_path": "",
                "availability": "source-code-confirmed",
                "source_id": "fixture",
                "source_url": "https://example.test/global.cs#L1",
                "source_file": "global.cs",
                "source_symbol": "Global",
                "source_line_start": 1,
                "source_line_end": 1,
                "source_ref": "a" * 40,
                "notes": "",
                "needs_live_verification": True,
                "coverage_status": "complete_for_source_snapshot",
            },
            {
                "context_id": "checkout",
                "context_family": "check-in-label",
                "surface_name": "Checkout",
                "surface_type": "label_dynamic_text",
                "concept_ids": ["lava", "check-in"],
                "root_key": "CheckoutDateTime",
                "root_type": "DateTime",
                "model_slug": None,
                "value_kind": "scalar",
                "nested_path": "",
                "availability": "source-code-confirmed",
                "source_id": "fixture",
                "source_url": "https://example.test/checkout.cs#L1",
                "source_file": "checkout.cs",
                "source_symbol": "Checkout",
                "source_line_start": 1,
                "source_line_end": 1,
                "source_ref": "a" * 40,
                "notes": "",
                "needs_live_verification": False,
                "includes_context_ids": ["global-common"],
                "coverage_status": "complete_for_source_snapshot",
            },
        ]
    )

    listed = list_lava_context_surfaces(rows, context_family="check-in-label")
    exact = get_lava_context_surface(rows, "checkout")
    filtered = get_lava_context_surface(rows, "checkout", root_key="CheckoutDateTime")

    assert listed["count"] == 1
    assert listed["surfaces"][0]["root_keys"] == ["CheckoutDateTime"]
    assert exact["root_count"] == 2
    assert exact["direct_root_count"] == 1
    assert exact["inherited_root_count"] == 1
    assert filtered["root_count"] == 1
    assert filtered["roots"][0]["defined_in_context_id"] == "checkout"


def test_discovery_queue_contains_public_relative_paths_only(tmp_path):
    source_tree = tmp_path / "rock"
    source_tree.mkdir()
    candidate = source_tree / "Rock.Blocks" / "CheckIn" / "Example.cs"
    candidate.parent.mkdir(parents=True)
    candidate.write_text(
        """
public Dictionary<string, object> GetMergeFields()
{
    mergeFields.Add( "Attendance", attendance );
}
""",
        encoding="utf-8",
    )
    output = tmp_path / "queue.jsonl"

    result = discover_lava_context_candidates(
        source_tree,
        output,
        source_commit="b" * 40,
        source_version="20.0.5",
    )
    row = json.loads(output.read_text(encoding="utf-8"))

    assert result["pending_count"] == 1
    assert row["source_file"] == "Rock.Blocks/CheckIn/Example.cs"
    assert str(tmp_path) not in json.dumps(row)
    assert row["root_keys"] == ["Attendance"]


def test_reviewed_extension_and_private_overlay_boundaries(tmp_path):
    extension = tmp_path / "extension.json"
    extension.write_text(
        json.dumps(
            {
                "schema": "rock-kb-lava-context-extension-v1",
                "extension_id": "test-org-labels",
                "org_id": "test-org",
                "title": "Test Org public label context",
                "repository_url": "https://github.com/test-org/public-rock",
                "commit_sha": "c" * 40,
                "source_version": "19.0",
                "license": "MIT",
                "license_url": "https://github.com/test-org/public-rock/blob/main/LICENSE",
                "license_attestation": True,
                "redaction_attestation": True,
                "review_status": "community_reviewed",
                "contexts": [
                    {
                        "context_id": "test-org:custom-label",
                        "context_family": "check-in-label",
                        "surface_name": "Custom Label",
                        "surface_type": "label_dynamic_text",
                        "concept_ids": ["lava", "check-in"],
                        "availability_condition": "The custom label is selected.",
                        "coverage_status": "reviewed_curated",
                        "roots": [
                            {
                                "root_key": "Person",
                                "root_type": "Rock.Model.Person",
                                "value_kind": "object",
                                "availability_condition": "A person is available.",
                                "source_path": "src/CustomLabel.cs",
                                "source_symbol": "CustomLabel.GetMergeFields",
                                "source_line_start": 10,
                                "source_line_end": 12,
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    overlay = tmp_path / "overlay.jsonl"
    overlay.write_text(
        json.dumps(
            {
                "schema": "rock-kb-private-lava-context-overlay-v1",
                "access_scope": "organization",
                "context_id": "private:label",
                "root_key": "Person",
                "publish": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    assert validate_lava_context_extension(extension)["status"] == "valid"
    overlay_result = validate_private_lava_context_overlay(overlay)
    assert overlay_result["status"] == "valid"
    assert overlay_result["public_export_eligible"] is False

    unsafe_extension = json.loads(extension.read_text(encoding="utf-8"))
    unsafe_extension["contexts"][0]["roots"][0]["source_path"] = "/Users/private/CustomLabel.cs"
    extension.write_text(json.dumps(unsafe_extension), encoding="utf-8")
    assert validate_lava_context_extension(extension)["status"] == "invalid"
