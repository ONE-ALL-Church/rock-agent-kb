from __future__ import annotations

from rock_kb import lava_contexts
from rock_kb.lava_contexts import (
    lava_context_rows,
    parse_common_merge_fields,
    parse_communication_merge_values,
    parse_curated_surface_contexts,
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
