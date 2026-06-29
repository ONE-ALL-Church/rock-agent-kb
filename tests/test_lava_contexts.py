from __future__ import annotations

from rock_kb import lava_contexts
from rock_kb.lava_contexts import (
    lava_context_rows,
    parse_common_merge_fields,
    parse_communication_merge_values,
    parse_person_label_data,
    parse_workflow_merge_fields,
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

    assert by_key["CurrentPerson"]["schema"] == "rock-kb-lava-context-v1"
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
