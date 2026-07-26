from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, REPO_ROOT, REVIEW_DIR
from .schemas.lava_context import LavaContextExtensionManifest

LAVA_CONTEXT_SCHEMA = "rock-kb-lava-context-v2"
LAVA_CONTEXT_SUMMARY_SCHEMA = "rock-kb-lava-context-summary-v2"
LAVA_CONTEXT_DEPENDENCIES_SCHEMA = "rock-kb-lava-context-dependencies-v2"
LAVA_CONTEXT_EXTENSION_SCHEMA = "rock-kb-lava-context-extension-v1"
LAVA_CONTEXT_DISCOVERY_SCHEMA = "rock-kb-lava-context-discovery-v1"
LAVA_CONTEXT_SNAPSHOT_SCHEMA = "rock-kb-lava-context-source-snapshot-v1"
SOURCE_REF = "develop"
SOURCE_ID = "sparkdevnetwork_rock"
SOURCE_REPOSITORY = "SparkDevNetwork/Rock"

LAVA_CONCEPT_DIR = KNOWLEDGE_DIR / "concepts" / "lava"
CONTEXT_JSONL = LAVA_CONCEPT_DIR / "lava-contexts.jsonl"
CONTEXT_INDEX = LAVA_CONCEPT_DIR / "lava-context-directory.md"
CONTEXT_DEPENDENCY_JSON = LAVA_CONCEPT_DIR / "lava-context-dependencies.json"
AGENT_CONTEXT_JSONL = AGENT_DIR / "lava-contexts.jsonl"
AGENT_CONTEXT_SUMMARY_JSON = AGENT_DIR / "lava-context-summary.json"
SOURCE_CACHE_DIR = REVIEW_DIR / "lava-context-source" / SOURCE_REF
SOURCE_SNAPSHOT_JSON = SOURCE_CACHE_DIR / "snapshot.json"
DISCOVERY_QUEUE_JSONL = REVIEW_DIR / "lava-context-discovery.jsonl"
PUBLIC_EXTENSION_DIR = REPO_ROOT / "lava-contexts" / "extensions"
PRIVATE_OVERLAY_DIR = REVIEW_DIR / "lava-context-overlays"

DEFAULT_CONCEPT_IDS = ["lava"]
CHECK_IN_CONCEPT_IDS = ["lava", "check-in", "groups"]
COMMUNICATION_CONCEPT_IDS = ["lava", "communications", "people-families"]
WORKFLOW_CONCEPT_IDS = ["lava", "workflows"]
CMS_CONCEPT_IDS = ["lava", "cms-websites"]
MOBILE_CONCEPT_IDS = ["lava", "mobile"]
EVENT_CONCEPT_IDS = ["lava", "event-registration"]
GROUP_CONCEPT_IDS = ["lava", "groups"]
EVENT_LAVA_CONCEPT_IDS = ["lava", "event-calendar"]
FOLLOWING_CONCEPT_IDS = ["lava", "people-families"]
ASSESSMENT_CONCEPT_IDS = ["lava", "people-families", "engagement-tracking"]
FINANCE_CONCEPT_IDS = ["lava", "giving-finance"]


@dataclass(frozen=True)
class SourceFile:
    key: str
    source_file: str
    source_symbol: str

    @property
    def cache_path(self) -> Path:
        return SOURCE_CACHE_DIR / self.source_file.replace("/", "__")

    def raw_url(self, source_ref: str = SOURCE_REF) -> str:
        return f"https://raw.githubusercontent.com/SparkDevNetwork/Rock/{source_ref}/{self.source_file}"

    def blob_url(self, source_ref: str = SOURCE_REF) -> str:
        return f"https://github.com/SparkDevNetwork/Rock/blob/{source_ref}/{self.source_file}"


@dataclass(frozen=True)
class SourceSnapshot:
    source_ref: str = SOURCE_REF
    source_commit: str = ""
    source_commit_date: str = ""
    source_version: str = ""

    @property
    def pinned_ref(self) -> str:
        return self.source_commit or self.source_ref

    def as_dict(self) -> dict[str, str]:
        return {
            "schema": LAVA_CONTEXT_SNAPSHOT_SCHEMA,
            "source_id": SOURCE_ID,
            "source_repository": SOURCE_REPOSITORY,
            "source_ref": self.source_ref,
            "source_commit": self.source_commit,
            "source_commit_date": self.source_commit_date,
            "source_version": self.source_version,
        }


@dataclass(frozen=True)
class CuratedContextRoot:
    root_key: str
    root_type: str
    model_slug: str | None = None
    value_kind: str = "object"
    nested_path: str = ""
    availability: str = "source-code-confirmed"
    needs_live_verification: bool = False
    source_symbol: str | None = None
    notes: str = ""
    source_patterns: tuple[str, ...] = ()
    availability_condition: str = "always"
    may_be_null: bool = False
    required_setting: str = ""
    execution_phase: str = "render"


@dataclass(frozen=True)
class CuratedContextSpec:
    source_key: str
    context_id: str
    context_family: str
    surface_name: str
    surface_type: str
    concept_ids: tuple[str, ...]
    source_symbol: str
    notes: str
    roots: tuple[CuratedContextRoot, ...]
    includes_context_ids: tuple[str, ...] = ()
    availability_condition: str = "surface_selected"
    coverage_status: str = "reviewed_curated"


SOURCE_FILES: dict[str, SourceFile] = {
    "lava_helper": SourceFile("lava_helper", "Rock/Lava/LavaHelper.cs", "LavaHelper.GetCommonMergeFields"),
    "request_context": SourceFile("request_context", "Rock/Net/RockRequestContext.cs", "RockRequestContext.GetCommonMergeFields"),
    "person_label_data": SourceFile("person_label_data", "Rock/CheckIn/v2/Labels/PersonLabelData.cs", "PersonLabelData"),
    "attendance_label_data": SourceFile(
        "attendance_label_data",
        "Rock/CheckIn/v2/Labels/AttendanceLabelData.cs",
        "AttendanceLabelData",
    ),
    "family_label_data": SourceFile("family_label_data", "Rock/CheckIn/v2/Labels/FamilyLabelData.cs", "FamilyLabelData"),
    "checkout_label_data": SourceFile(
        "checkout_label_data",
        "Rock/CheckIn/v2/Labels/CheckoutLabelData.cs",
        "CheckoutLabelData",
    ),
    "person_location_label_data": SourceFile(
        "person_location_label_data",
        "Rock/CheckIn/v2/Labels/PersonLocationLabelData.cs",
        "PersonLocationLabelData",
    ),
    "field_source_helper": SourceFile("field_source_helper", "Rock/CheckIn/v2/Labels/FieldSourceHelper.cs", "FieldSourceHelper"),
    "label_field": SourceFile("label_field", "Rock/CheckIn/v2/Labels/LabelField.cs", "LabelField"),
    "communication_recipient": SourceFile(
        "communication_recipient",
        "Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs",
        "CommunicationRecipient.CommunicationMergeValues",
    ),
    "workflow_action": SourceFile("workflow_action", "Rock/Workflow/ActionComponent.cs", "ActionComponent.GetMergeFields"),
    "content_channel_view": SourceFile("content_channel_view", "Rock.Blocks/Cms/ContentChannelView.cs", "ContentChannelView"),
    "content_channel_item_view": SourceFile(
        "content_channel_item_view",
        "Rock.Blocks/Cms/ContentChannelItemView.cs",
        "ContentChannelItemView",
    ),
    "mobile_cms_content": SourceFile("mobile_cms_content", "Rock/Blocks/Types/Mobile/Cms/Content.cs", "Mobile.Cms.Content"),
    "mobile_group_view": SourceFile("mobile_group_view", "Rock/Blocks/Types/Mobile/Groups/GroupView.cs", "Mobile.Groups.GroupView"),
    "mobile_prayer_session": SourceFile(
        "mobile_prayer_session",
        "Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs",
        "Mobile.Prayer.PrayerSession",
    ),
    "mobile_communication_view": SourceFile(
        "mobile_communication_view",
        "Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs",
        "Mobile.Communication.CommunicationView",
    ),
    "workflow_entry": SourceFile("workflow_entry", "Rock.Blocks/WorkFlow/WorkflowEntry.cs", "WorkflowEntry"),
    "registration_entry": SourceFile("registration_entry", "Rock.Blocks/Event/RegistrationEntry.cs", "RegistrationEntry"),
    "registrant_waitlist_move": SourceFile(
        "registrant_waitlist_move",
        "Rock.Blocks/Event/RegistrantWaitListMove.cs",
        "RegistrantWaitListMove",
    ),
    "group_detail_lava": SourceFile("group_detail_lava", "RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs", "GroupDetailLava"),
    "group_finder": SourceFile("group_finder", "RockWeb/Blocks/Groups/GroupFinder.ascx.cs", "GroupFinder"),
    "calendar_lava": SourceFile("calendar_lava", "RockWeb/Blocks/Event/CalendarLava.ascx.cs", "CalendarLava"),
    "event_item_occurrence_lava": SourceFile(
        "event_item_occurrence_lava",
        "RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs",
        "EventItemOccurrenceLava",
    ),
    "realtime_visualizer": SourceFile("realtime_visualizer", "Rock.Blocks/Utility/RealTimeVisualizer.cs", "RealTimeVisualizer"),
    "following_by_entity_lava": SourceFile(
        "following_by_entity_lava",
        "Rock.Blocks/Core/FollowingByEntityLava.cs",
        "FollowingByEntityLava",
    ),
    "motivators": SourceFile("motivators", "Rock.Blocks/Crm/Motivators.cs", "Motivators"),
    "gifts_assessment": SourceFile("gifts_assessment", "Rock.Blocks/Crm/GiftsAssessment.cs", "GiftsAssessment"),
    "conflict_profile": SourceFile("conflict_profile", "Rock.Blocks/Crm/ConflictProfile.cs", "ConflictProfile"),
    "disc": SourceFile("disc", "Rock.Blocks/Crm/Disc.cs", "Disc"),
    "fundraising_opportunity_view": SourceFile(
        "fundraising_opportunity_view",
        "Rock.Blocks/Fundraising/FundraisingOpportunityView.cs",
        "FundraisingOpportunityView",
    ),
    "transaction_entry_v2": SourceFile(
        "transaction_entry_v2",
        "RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs",
        "TransactionEntryV2",
    ),
}

TYPE_MODEL_MAP = {
    "Person": ("Rock.Model.Person", "person", "object"),
    "PersonAlias": ("Rock.Model.PersonAlias", "person-alias", "object"),
    "Group": ("Rock.Model.Group", "group", "object"),
    "Location": ("Rock.Model.Location", "location", "object"),
    "Schedule": ("Rock.Model.Schedule", "schedule", "object"),
    "Communication": ("Rock.Model.Communication", "communication", "object"),
    "WorkflowAction": ("Rock.Model.WorkflowAction", "workflow-action", "object"),
    "WorkflowActivity": ("Rock.Model.WorkflowActivity", "workflow-activity", "object"),
    "Workflow": ("Rock.Model.Workflow", "workflow", "object"),
    "WorkflowType": ("Rock.Model.WorkflowType", "workflow-type", "object"),
    "Campus": ("Rock.Model.Campus", "campus", "object"),
    "ContentChannel": ("Rock.Model.ContentChannel", "content-channel", "object"),
    "ContentChannelItem": ("Rock.Model.ContentChannelItem", "content-channel-item", "object"),
    "Registration": ("Rock.Model.Registration", "registration", "object"),
    "RegistrationInstance": ("Rock.Model.RegistrationInstance", "registration-instance", "object"),
    "RegistrationRegistrant": ("Rock.Model.RegistrationRegistrant", "registration-registrant", "object"),
    "GroupMember": ("Rock.Model.GroupMember", "group-member", "object"),
    "EventItem": ("Rock.Model.EventItem", "event-item", "object"),
    "EventItemOccurrence": ("Rock.Model.EventItemOccurrence", "event-item-occurrence", "object"),
    "PrayerRequest": ("Rock.Model.PrayerRequest", "prayer-request", "object"),
    "FinancialTransaction": ("Rock.Model.FinancialTransaction", "financial-transaction", "object"),
    "FinancialScheduledTransaction": ("Rock.Model.FinancialScheduledTransaction", "financial-scheduled-transaction", "object"),
    "FinancialPaymentDetail": ("Rock.Model.FinancialPaymentDetail", "financial-payment-detail", "object"),
    "NamedLocationCache": ("Rock.Web.Cache.NamedLocationCache", "location", "object"),
    "Device": ("Rock.Common.Mobile.DeviceData", None, "object"),
}

COMMON_KEY_TYPE_MAP = {
    "Context": ("Dictionary<string, object>", None, "dictionary"),
    "PageParameter": ("IDictionary<string, string>", None, "dictionary"),
    "OSFamily": ("string", None, "scalar"),
    "DeviceFamily": ("string", None, "scalar"),
    "CurrentPerson": TYPE_MODEL_MAP["Person"],
    "CurrentVisitor": TYPE_MODEL_MAP["PersonAlias"],
    "Campuses": ("IEnumerable<CampusCache>", "campus", "collection"),
    "Geolocation": ("Rock.Net.Geolocation", None, "object"),
    "ExperienceMode": ("string", None, "scalar"),
    "Device": TYPE_MODEL_MAP["Device"],
}

LABEL_NESTED_MODEL_MAP = {
    "Area": ("Rock.Model.GroupType", None, "object"),
    "Campus": TYPE_MODEL_MAP["Campus"],
    "CheckedInByPerson": TYPE_MODEL_MAP["Person"],
    "Device": TYPE_MODEL_MAP["Device"],
    "Group": TYPE_MODEL_MAP["Group"],
    "Location": TYPE_MODEL_MAP["Location"],
    "Schedule": TYPE_MODEL_MAP["Schedule"],
}

LABEL_DATA_SPECS = (
    (
        "person_label_data",
        "check-in-label-person-dynamic-text",
        "Check-In Label Designer Person Dynamic Text",
    ),
    (
        "attendance_label_data",
        "check-in-label-attendance-dynamic-text",
        "Check-In Label Designer Attendance Dynamic Text",
    ),
    (
        "family_label_data",
        "check-in-label-family-dynamic-text",
        "Check-In Label Designer Family Dynamic Text",
    ),
    (
        "checkout_label_data",
        "check-in-label-checkout-dynamic-text",
        "Check-In Label Designer Checkout Dynamic Text",
    ),
    (
        "person_location_label_data",
        "check-in-label-person-location-dynamic-text",
        "Check-In Label Designer Person Location Dynamic Text",
    ),
)

CONTEXT_METADATA: dict[str, dict[str, Any]] = {
    "global-lava-helper-common": {
        "coverage_status": "complete_for_source_snapshot",
        "availability_condition": "Web Forms or legacy Lava rendering requests common merge fields.",
        "execution_phase": "request",
    },
    "global-request-context-common": {
        "coverage_status": "complete_for_source_snapshot",
        "availability_condition": "A RockRequestContext is available and common merge fields are requested.",
        "execution_phase": "request",
    },
    "workflow-action-component-merge-fields": {
        "includes_context_ids": ["global-lava-helper-common", "global-request-context-common"],
        "coverage_status": "complete_for_source_snapshot",
        "availability_condition": "The workflow action overload and request context determine which common context is inherited.",
        "execution_phase": "workflow_action",
    },
    "communication-recipient-merge-values": {
        "coverage_status": "complete_for_source_snapshot",
        "availability_condition": "The communication recipient is being rendered for its configured medium.",
        "execution_phase": "communication_render",
    },
}

for _source_key, _context_id, _surface_name in LABEL_DATA_SPECS:
    CONTEXT_METADATA[_context_id] = {
        "coverage_status": "complete_for_source_snapshot",
        "availability_condition": f"The label is configured for the {_surface_name.removeprefix('Check-In Label Designer ').removesuffix(' Dynamic Text')} data type.",
        "execution_phase": "label_render",
    }


def simple_context_root(
    root_key: str,
    root_type: str,
    value_kind: str,
    *,
    model_slug: str | None = None,
    availability: str = "source-code-confirmed",
    needs_live_verification: bool = False,
    source_symbol: str | None = None,
    notes: str = "",
    source_patterns: tuple[str, ...] = (),
    availability_condition: str = "always",
    may_be_null: bool = False,
    required_setting: str = "",
    execution_phase: str = "render",
) -> CuratedContextRoot:
    return CuratedContextRoot(
        root_key=root_key,
        root_type=root_type,
        model_slug=model_slug,
        value_kind=value_kind,
        availability=availability,
        needs_live_verification=needs_live_verification,
        source_symbol=source_symbol,
        notes=notes,
        source_patterns=source_patterns,
        availability_condition=availability_condition,
        may_be_null=may_be_null,
        required_setting=required_setting,
        execution_phase=execution_phase,
    )


def model_context_root(
    root_key: str,
    type_key: str,
    *,
    value_kind: str | None = None,
    root_type: str | None = None,
    needs_live_verification: bool = False,
    source_symbol: str | None = None,
    notes: str = "",
    source_patterns: tuple[str, ...] = (),
    availability_condition: str = "always",
    may_be_null: bool = False,
    required_setting: str = "",
    execution_phase: str = "render",
) -> CuratedContextRoot:
    default_type, model_slug, default_kind = TYPE_MODEL_MAP[type_key]
    return simple_context_root(
        root_key,
        root_type or default_type,
        value_kind or default_kind,
        model_slug=model_slug,
        needs_live_verification=needs_live_verification,
        source_symbol=source_symbol,
        notes=notes,
        source_patterns=source_patterns,
        availability_condition=availability_condition,
        may_be_null=may_be_null,
        required_setting=required_setting,
        execution_phase=execution_phase,
    )


CURATED_CONTEXT_SPECS: tuple[CuratedContextSpec, ...] = (
    CuratedContextSpec(
        source_key="content_channel_view",
        context_id="cms-content-channel-view-template",
        context_family="cms-block",
        surface_name="CMS Content Channel View Lava template",
        surface_type="cms_content_channel_view_template",
        concept_ids=tuple(CMS_CONCEPT_IDS),
        source_symbol="ContentChannelView.GetTemplateMergeFields",
        notes="ContentChannelView builds these roots for the list/archive Lava template.",
        roots=(
            simple_context_root("DetailPage", "PageReference route", "scalar"),
            simple_context_root("DetailPageRoute", "string", "scalar"),
            model_context_root("Person", "Person", needs_live_verification=True),
            model_context_root("Item", "ContentChannelItem"),
            simple_context_root("Pagination", "PaginationBag", "object"),
            simple_context_root("LinkedPages", "Dictionary<string, object>", "dictionary"),
            model_context_root("Items", "ContentChannelItem", value_kind="collection", root_type="IEnumerable<ContentChannelItem>"),
            simple_context_root("ItemTagList", "IEnumerable<Tag>", "collection"),
            simple_context_root("ArchiveSummary", "IEnumerable<ArchiveSummary>", "collection"),
            simple_context_root("RockVersion", "string", "scalar"),
            simple_context_root("CurrentPageUrl", "string", "scalar"),
            simple_context_root("ArchiveSummaryPageUrl", "string", "scalar"),
        ),
    ),
    CuratedContextSpec(
        source_key="content_channel_item_view",
        context_id="cms-content-channel-item-view-template",
        context_family="cms-block",
        surface_name="CMS Content Channel Item View Lava template",
        surface_type="cms_content_channel_item_view_template",
        concept_ids=tuple(CMS_CONCEPT_IDS),
        source_symbol="ContentChannelItemView.GetTemplateMergeFields",
        notes="ContentChannelItemView builds these roots for single content item Lava rendering.",
        roots=(
            model_context_root("Item", "ContentChannelItem"),
            simple_context_root("RockVersion", "string", "scalar"),
            simple_context_root("DetailPage", "int or string", "scalar"),
            simple_context_root("DetailPageRoute", "string", "scalar"),
        ),
    ),
    CuratedContextSpec(
        source_key="mobile_cms_content",
        context_id="mobile-cms-content-template",
        context_family="mobile-block",
        surface_name="Mobile CMS Content block server Lava",
        surface_type="mobile_cms_content_template",
        concept_ids=tuple(MOBILE_CONCEPT_IDS),
        source_symbol="Mobile.Cms.Content.GetInitialContent",
        notes="Mobile CMS Content adds CurrentPage when server-side Lava processing is enabled.",
        roots=(simple_context_root("CurrentPage", "PageCache", "object", needs_live_verification=True),),
    ),
    CuratedContextSpec(
        source_key="mobile_cms_content",
        context_id="mobile-cms-command-template",
        context_family="mobile-block",
        surface_name="Mobile CMS Content command Lava",
        surface_type="mobile_cms_command_template",
        concept_ids=tuple(MOBILE_CONCEPT_IDS),
        source_symbol="Mobile.Cms.Content.ProcessCallbackCommand",
        notes="Mobile CMS callback command Lava receives command metadata plus the current page.",
        roots=(
            simple_context_root("Command", "string", "scalar"),
            simple_context_root("Parameters", "IDictionary<string, object>", "dictionary"),
            simple_context_root("CurrentPage", "PageCache", "object", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="mobile_group_view",
        context_id="mobile-group-view-template",
        context_family="mobile-block",
        surface_name="Mobile Group View block Lava template",
        surface_type="mobile_group_view_template",
        concept_ids=tuple(MOBILE_CONCEPT_IDS + GROUP_CONCEPT_IDS[1:]),
        source_symbol="Mobile.Groups.GroupView.GetTemplateMergeFields",
        notes="Mobile Group View declares group, linked-page, attribute, and authorization roots for its template.",
        roots=(
            model_context_root("Group", "Group"),
            simple_context_root("GroupEditPage", "string", "scalar"),
            simple_context_root("ShowLeaderList", "bool", "scalar"),
            simple_context_root("VisibleAttributes", "IEnumerable<AttributeCache>", "collection"),
            simple_context_root("AllowedActions", "Dictionary<string, bool>", "dictionary", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="mobile_prayer_session",
        context_id="mobile-prayer-session-template",
        context_family="mobile-block",
        surface_name="Mobile Prayer Session block Lava template",
        surface_type="mobile_prayer_session_template",
        concept_ids=tuple(MOBILE_CONCEPT_IDS + ["prayer-care"]),
        source_symbol="Mobile.Prayer.PrayerSession.GetRequestContent",
        notes="Mobile Prayer Session declares button labels, session context, and the prayer request root.",
        roots=(
            simple_context_root("PrayedButtonText", "string", "scalar"),
            simple_context_root("ShowFollowButton", "bool", "scalar"),
            simple_context_root("ShowInappropriateButton", "bool", "scalar"),
            simple_context_root("SessionContext", "encrypted JSON string", "scalar", needs_live_verification=True),
            model_context_root("Request", "PrayerRequest"),
        ),
    ),
    CuratedContextSpec(
        source_key="mobile_communication_view",
        context_id="mobile-communication-view-template",
        context_family="mobile-block",
        surface_name="Mobile Communication View block Lava template",
        surface_type="mobile_communication_view_template",
        concept_ids=tuple(MOBILE_CONCEPT_IDS + COMMUNICATION_CONCEPT_IDS[1:]),
        source_symbol="Mobile.Communication.CommunicationView.GetTemplateMergeFields",
        notes="Mobile Communication View declares communication recipient roots and may copy additional recipient merge values.",
        roots=(
            simple_context_root("CurrentPage", "PageCache", "object", needs_live_verification=True),
            model_context_root("Communication", "Communication"),
            model_context_root("Person", "Person"),
            simple_context_root("Content", "string", "scalar"),
            simple_context_root(
                "AdditionalRecipientMergeValues",
                "dynamic recipient merge values",
                "dynamic",
                needs_live_verification=True,
                source_patterns=(r"mergeFields\.Add\(\s*mergeField\.Key\s*,\s*mergeField\.Value\s*\)",),
            ),
        ),
    ),
    CuratedContextSpec(
        source_key="workflow_entry",
        context_id="workflow-entry-form-template",
        context_family="workflow",
        surface_name="Workflow Entry block form Lava",
        surface_type="workflow_entry_form_template",
        concept_ids=tuple(WORKFLOW_CONCEPT_IDS),
        source_symbol="WorkflowEntry.GetMergeFields",
        notes="Workflow Entry adds workflow state roots for form rendering and action processing.",
        roots=(
            model_context_root("Action", "WorkflowAction", needs_live_verification=True),
            model_context_root("Activity", "WorkflowActivity", needs_live_verification=True),
            model_context_root("Workflow", "Workflow"),
            model_context_root("Item", "WorkflowType", notes="WorkflowEntry uses Item for workflow-type selection in some form flows."),
        ),
    ),
    CuratedContextSpec(
        source_key="registration_entry",
        context_id="event-registration-entry-template",
        context_family="event-registration",
        surface_name="Event Registration Entry Lava templates",
        surface_type="event_registration_entry_template",
        concept_ids=tuple(EVENT_CONCEPT_IDS),
        source_symbol="RegistrationEntry.GetMergeFields",
        notes="Registration Entry uses these roots for registration UI, success, and confirmation Lava.",
        roots=(
            model_context_root("RegistrationInstance", "RegistrationInstance", source_patterns=(r'mergeFields\.Add\(\s*"RegistrationInstance"',)),
            model_context_root("Registration", "Registration", source_patterns=(r'mergeFields\.Add\(\s*"Registration"',)),
        ),
    ),
    CuratedContextSpec(
        source_key="registration_entry",
        context_id="event-registration-signature-document",
        context_family="event-registration",
        surface_name="Event Registration signature document Lava",
        surface_type="event_registration_signature_document",
        concept_ids=tuple(EVENT_CONCEPT_IDS + ["documents-signatures"]),
        source_symbol="RegistrationEntry.BuildSignatureDocumentMergeFields",
        notes="Registration Entry builds signature-document Lava roots for registration and registrant context.",
        roots=(
            model_context_root("Registration", "Registration", source_patterns=(r'\{\s*"Registration"\s*,',)),
            model_context_root("Registrant", "RegistrationRegistrant", source_patterns=(r'\{\s*"Registrant"\s*,',)),
        ),
    ),
    CuratedContextSpec(
        source_key="registrant_waitlist_move",
        context_id="event-registrant-waitlist-transition-template",
        context_family="event-registration",
        surface_name="Registrant wait-list transition email Lava",
        surface_type="event_registration_waitlist_transition_template",
        concept_ids=tuple(EVENT_CONCEPT_IDS + COMMUNICATION_CONCEPT_IDS[1:]),
        source_symbol="RegistrantWaitListMove.BuildMergeFields",
        notes="Registrant wait-list transition emails use these roots when resolving the email template.",
        roots=(
            model_context_root("RegistrationInstance", "RegistrationInstance"),
            model_context_root("Registration", "Registration"),
            model_context_root("TransitionedRegistrants", "RegistrationRegistrant", value_kind="collection", root_type="List<RegistrationRegistrant>"),
            simple_context_root("AdditionalFieldsNeeded", "bool", "scalar"),
        ),
    ),
    CuratedContextSpec(
        source_key="group_detail_lava",
        context_id="group-detail-lava-template",
        context_family="group-lava",
        surface_name="Group Detail Lava block",
        surface_type="group_detail_lava_template",
        concept_ids=tuple(GROUP_CONCEPT_IDS),
        source_symbol="GroupDetailLava.ShowViewGroup",
        notes="Legacy Group Detail Lava exposes the group plus linked page and security helper dictionaries.",
        roots=(
            model_context_root("Group", "Group"),
            simple_context_root("LinkedPages", "Dictionary<string, object>", "dictionary"),
            simple_context_root("AllowedActions", "Dictionary<string, bool>", "dictionary", needs_live_verification=True),
            simple_context_root("CurrentPage", "Dictionary<string, object>", "dictionary", needs_live_verification=True),
            simple_context_root("ButtonVisibility", "Dictionary<string, bool>", "dictionary", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="group_finder",
        context_id="group-finder-lava-template",
        context_family="group-lava",
        surface_name="Group Finder Lava block",
        surface_type="group_finder_lava_template",
        concept_ids=tuple(GROUP_CONCEPT_IDS),
        source_symbol="GroupFinder.ShowResults",
        notes="Group Finder exposes selected group/location context, linked pages, campus context, and result lists.",
        roots=(
            model_context_root("Group", "Group", needs_live_verification=True),
            model_context_root("Location", "Location", needs_live_verification=True),
            simple_context_root("LinkedPages", "Dictionary<string, object>", "dictionary"),
            model_context_root("CampusContext", "Campus", needs_live_verification=True),
            simple_context_root("AllowedActions", "Dictionary<string, bool>", "dictionary", needs_live_verification=True),
            simple_context_root("Fences", "IEnumerable<GeoFence>", "collection", needs_live_verification=True),
            model_context_root("Groups", "Group", value_kind="collection", root_type="IEnumerable<Group>"),
        ),
    ),
    CuratedContextSpec(
        source_key="calendar_lava",
        context_id="calendar-lava-template",
        context_family="event-lava",
        surface_name="Calendar Lava block",
        surface_type="calendar_lava_template",
        concept_ids=tuple(EVENT_LAVA_CONCEPT_IDS),
        source_symbol="CalendarLava.BindEvents",
        notes="Calendar Lava exposes date filters plus event summaries and occurrence summaries.",
        roots=(
            simple_context_root("DetailsPage", "PageReference route", "scalar"),
            model_context_root("EventItems", "EventItem", value_kind="collection", root_type="IEnumerable<EventItem>"),
            model_context_root("EventItemOccurrences", "EventItemOccurrence", value_kind="collection", root_type="IEnumerable<EventItemOccurrence>"),
            model_context_root("CurrentPerson", "Person", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="event_item_occurrence_lava",
        context_id="event-item-occurrence-lava-template",
        context_family="event-lava",
        surface_name="Event Item Occurrence Lava block",
        surface_type="event_item_occurrence_lava_template",
        concept_ids=tuple(EVENT_LAVA_CONCEPT_IDS),
        source_symbol="EventItemOccurrenceLava.ShowEventItemOccurrence",
        notes="Event Item Occurrence Lava exposes occurrence, event, campus, registration, and status roots.",
        roots=(
            simple_context_root("RegistrationPage", "PageReference route", "scalar"),
            model_context_root("CampusContext", "Campus", needs_live_verification=True),
            simple_context_root("RegistrationStatusLabel", "string", "scalar", needs_live_verification=True),
            simple_context_root("RegistrationStatusLabels", "Dictionary<string, string>", "dictionary", needs_live_verification=True),
            model_context_root("EventItemOccurrence", "EventItemOccurrence"),
            model_context_root("Event", "EventItem"),
            model_context_root("CurrentPerson", "Person", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="realtime_visualizer",
        context_id="realtime-visualizer-settings-template",
        context_family="utility-lava",
        surface_name="Real Time Visualizer settings Lava",
        surface_type="realtime_visualizer_settings_template",
        concept_ids=tuple(DEFAULT_CONCEPT_IDS),
        source_symbol="RealTimeVisualizer.GetSettingsHtml",
        notes="Real Time Visualizer settings templates receive the block settings root.",
        roots=(simple_context_root("Settings", "Dictionary<string, object>", "dictionary"),),
    ),
    CuratedContextSpec(
        source_key="realtime_visualizer",
        context_id="realtime-visualizer-message-template",
        context_family="utility-lava",
        surface_name="Real Time Visualizer message Lava",
        surface_type="realtime_visualizer_message_template",
        concept_ids=tuple(DEFAULT_CONCEPT_IDS),
        source_symbol="RealTimeVisualizer.OnMessage",
        notes="Real Time Visualizer message templates receive real-time topic, message, and argument roots.",
        roots=(
            simple_context_root("Topic", "string", "scalar"),
            simple_context_root("Message", "string", "scalar"),
            simple_context_root("Args", "Lava object converted from JavaScript arguments", "dynamic", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="following_by_entity_lava",
        context_id="following-by-entity-lava-template",
        context_family="following",
        surface_name="Following By Entity Lava block",
        surface_type="following_by_entity_lava_template",
        concept_ids=tuple(FOLLOWING_CONCEPT_IDS),
        source_symbol="FollowingByEntityLava.BindGrid",
        notes="Following By Entity Lava exposes followed items and paging/link metadata.",
        roots=(
            simple_context_root("FollowingItems", "IEnumerable<Following>", "collection"),
            simple_context_root("HasMore", "bool", "scalar"),
            simple_context_root("EntityType", "string", "scalar"),
            simple_context_root("LinkUrl", "string", "scalar"),
            simple_context_root("Quantity", "int", "scalar"),
            simple_context_root("BlockId", "int", "scalar"),
        ),
    ),
    CuratedContextSpec(
        source_key="motivators",
        context_id="motivators-assessment-template",
        context_family="assessment-lava",
        surface_name="Motivators assessment Lava templates",
        surface_type="assessment_lava_template",
        concept_ids=tuple(ASSESSMENT_CONCEPT_IDS),
        source_symbol="Motivators.ShowResults",
        notes="Motivators assessment result templates receive the target person and score roots.",
        roots=(
            model_context_root("Person", "Person"),
            simple_context_root("MotivatorThemeScores", "IEnumerable<MotivatorThemeScore>", "collection"),
            simple_context_root("MotivatorScores", "IEnumerable<MotivatorScore>", "collection"),
            simple_context_root("GrowthScore", "object", "object"),
        ),
    ),
    CuratedContextSpec(
        source_key="gifts_assessment",
        context_id="gifts-assessment-template",
        context_family="assessment-lava",
        surface_name="Gifts assessment Lava template",
        surface_type="assessment_lava_template",
        concept_ids=tuple(ASSESSMENT_CONCEPT_IDS),
        source_symbol="GiftsAssessment.ShowResults",
        notes="Gifts assessment result templates receive the target person root.",
        roots=(model_context_root("Person", "Person"),),
    ),
    CuratedContextSpec(
        source_key="conflict_profile",
        context_id="conflict-profile-template",
        context_family="assessment-lava",
        surface_name="Conflict profile Lava template",
        surface_type="assessment_lava_template",
        concept_ids=tuple(ASSESSMENT_CONCEPT_IDS),
        source_symbol="ConflictProfile.ShowResults",
        notes="Conflict profile result templates receive the target person root.",
        roots=(model_context_root("Person", "Person"),),
    ),
    CuratedContextSpec(
        source_key="disc",
        context_id="disc-assessment-template",
        context_family="assessment-lava",
        surface_name="DISC assessment Lava template",
        surface_type="assessment_lava_template",
        concept_ids=tuple(ASSESSMENT_CONCEPT_IDS),
        source_symbol="Disc.ShowResults",
        notes="DISC assessment result templates receive the target person root.",
        roots=(model_context_root("Person", "Person"),),
    ),
    CuratedContextSpec(
        source_key="fundraising_opportunity_view",
        context_id="fundraising-opportunity-template",
        context_family="finance-lava",
        surface_name="Fundraising Opportunity View Lava template",
        surface_type="fundraising_opportunity_lava_template",
        concept_ids=tuple(FINANCE_CONCEPT_IDS + EVENT_CONCEPT_IDS[1:]),
        source_symbol="FundraisingOpportunityView.GetFundraisingOpportunityBox",
        notes="Fundraising Opportunity View exposes group, registration, progress, and content-channel roots.",
        roots=(
            simple_context_root("Block", "BlockCache", "object", needs_live_verification=True),
            model_context_root("Group", "Group"),
            simple_context_root("RegistrationPage", "PageReference route", "scalar"),
            model_context_root("RegistrationInstance", "RegistrationInstance"),
            simple_context_root("RegistrationInstanceLinkages", "IEnumerable<RegistrationInstanceLinkage>", "collection"),
            simple_context_root("CurrentRegistrationCount", "int", "scalar"),
            simple_context_root("MaxRegistrantCount", "int", "scalar"),
            simple_context_root("RegistrationSpotsAvailable", "int", "scalar"),
            model_context_root("GroupMember", "GroupMember", needs_live_verification=True),
            simple_context_root("ParticipationMode", "string", "scalar"),
            simple_context_root("ProgressTitle", "string", "scalar"),
            simple_context_root("FamilyMemberGroupMembers", "IEnumerable<GroupMember>", "collection", model_slug="group-member"),
            simple_context_root("AmountLeft", "decimal", "scalar"),
            simple_context_root("PercentMet", "decimal", "scalar"),
            simple_context_root("MakeDonationUrl", "string", "scalar"),
            simple_context_root("ParticipantPageUrl", "string", "scalar"),
            simple_context_root("MakeDonationButtonText", "string", "scalar"),
            model_context_root("ContentChannelItems", "ContentChannelItem", value_kind="collection", root_type="IEnumerable<ContentChannelItem>"),
        ),
    ),
    CuratedContextSpec(
        source_key="transaction_entry_v2",
        context_id="transaction-entry-scheduled-transactions-template",
        context_family="finance-lava",
        surface_name="Transaction Entry scheduled transactions Lava template",
        surface_type="transaction_entry_scheduled_transactions_template",
        concept_ids=tuple(FINANCE_CONCEPT_IDS),
        source_symbol="TransactionEntryV2.LoadScheduledTransactions",
        notes="Transaction Entry exposes these roots when rendering scheduled transaction rows.",
        roots=(
            simple_context_root("GiftTerm", "string", "scalar"),
            simple_context_root("LinkedPages", "Dictionary<string, object>", "dictionary"),
            model_context_root(
                "ScheduledTransactions",
                "FinancialScheduledTransaction",
                value_kind="collection",
                root_type="IEnumerable<FinancialScheduledTransaction>",
            ),
        ),
    ),
    CuratedContextSpec(
        source_key="transaction_entry_v2",
        context_id="transaction-entry-confirm-account-email",
        context_family="finance-lava",
        surface_name="Transaction Entry confirm account email Lava",
        surface_type="transaction_entry_confirm_account_email",
        concept_ids=tuple(FINANCE_CONCEPT_IDS + COMMUNICATION_CONCEPT_IDS[1:]),
        source_symbol="TransactionEntryV2.SendConfirmAccountEmail",
        notes="Transaction Entry confirmation emails receive account URL, person, and user roots.",
        roots=(
            simple_context_root("ConfirmAccountUrl", "string", "scalar"),
            model_context_root("Person", "Person"),
            simple_context_root("User", "UserLogin", "object", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="transaction_entry_v2",
        context_id="transaction-entry-intro-message",
        context_family="finance-lava",
        surface_name="Transaction Entry intro message Lava",
        surface_type="transaction_entry_intro_message",
        concept_ids=tuple(FINANCE_CONCEPT_IDS),
        source_symbol="TransactionEntryV2.SetIntroMessage",
        notes="Transaction Entry intro message can expose the transaction entity root when configured.",
        roots=(simple_context_root("TransactionEntity", "IEntity", "dynamic", needs_live_verification=True),),
    ),
    CuratedContextSpec(
        source_key="transaction_entry_v2",
        context_id="transaction-entry-finish-template",
        context_family="finance-lava",
        surface_name="Transaction Entry finish Lava template",
        surface_type="transaction_entry_finish_template",
        concept_ids=tuple(FINANCE_CONCEPT_IDS),
        source_symbol="TransactionEntryV2.ShowTransactionSummary",
        notes="Transaction Entry finish template receives transaction, person, payment, and billing roots after payment.",
        roots=(
            simple_context_root("TransactionEntity", "IEntity", "dynamic", needs_live_verification=True, source_patterns=(r'mergeFields\.Add\(\s*"TransactionEntity"',)),
            simple_context_root("Transaction", "FinancialTransaction or FinancialScheduledTransaction", "object", model_slug="financial-transaction"),
            model_context_root("Person", "Person"),
            model_context_root("PaymentDetail", "FinancialPaymentDetail"),
            model_context_root("BillingLocation", "Location", needs_live_verification=True),
        ),
    ),
    CuratedContextSpec(
        source_key="transaction_entry_v2",
        context_id="transaction-entry-payment-comment-template",
        context_family="finance-lava",
        surface_name="Transaction Entry payment comment Lava template",
        surface_type="transaction_entry_payment_comment_template",
        concept_ids=tuple(FINANCE_CONCEPT_IDS),
        source_symbol="TransactionEntryV2.SetPaymentComment",
        notes="Transaction Entry payment comment template receives payment timing, currency, and account allocation roots.",
        roots=(
            simple_context_root("TransactionDateTime", "DateTime", "scalar"),
            simple_context_root("CurrencyType", "DefinedValueCache", "object", needs_live_verification=True),
            simple_context_root("TransactionAccountDetails", "IEnumerable<FinancialTransactionDetail>", "collection"),
        ),
    ),
)


def build_lava_context_reference(fetch_missing: bool = True, source_dir: Path | None = None) -> dict[str, Any]:
    """Build generated Lava data-context artifacts from public Rock source files."""
    base = source_dir or SOURCE_CACHE_DIR
    snapshot = load_source_snapshot(base)
    if not snapshot.source_commit and fetch_missing:
        snapshot = resolve_source_snapshot()
        write_source_snapshot(base, snapshot)
    source_texts = load_source_texts(fetch_missing=fetch_missing, source_dir=base, snapshot=snapshot)
    previous_rows = list(read_jsonl(AGENT_CONTEXT_JSONL))
    rows = lava_context_rows(source_texts, snapshot=snapshot, previous_rows=previous_rows)
    rows.extend(load_public_extension_rows(snapshot))
    rows = normalize_context_rows(rows, previous_rows=previous_rows)
    source_dependencies = lava_context_source_dependencies(source_texts, snapshot=snapshot)
    write_lava_context_artifacts(rows, source_dependencies)
    return {
        "lava_contexts": len(rows),
        "lava_context_source_files": len(source_dependencies),
        "lava_context_families": len({row.get("context_family") for row in rows}),
        "source_commit": snapshot.source_commit,
        "source_version": snapshot.source_version,
    }


def refresh_lava_context_source_cache(source_dir: Path | None = None) -> dict[str, Any]:
    destination = source_dir or SOURCE_CACHE_DIR
    destination.mkdir(parents=True, exist_ok=True)
    snapshot = resolve_source_snapshot()
    write_source_snapshot(destination, snapshot)
    fetched = []
    for source in SOURCE_FILES.values():
        target = destination / source.source_file.replace("/", "__")
        text = fetch_public_source(source.raw_url(snapshot.pinned_ref))
        target.write_text(text, encoding="utf-8")
        fetched.append({"source_file": source.source_file, "bytes": len(text.encode("utf-8")), "content_hash": sha256_text(text)})
    return {
        **snapshot.as_dict(),
        "schema": "rock-kb-lava-context-source-refresh-v2",
        "source_files": fetched,
    }


def load_source_texts(
    fetch_missing: bool = True,
    source_dir: Path | None = None,
    snapshot: SourceSnapshot | None = None,
) -> dict[str, str]:
    base = source_dir or SOURCE_CACHE_DIR
    snapshot = snapshot or load_source_snapshot(base)
    texts: dict[str, str] = {}
    for key, source in SOURCE_FILES.items():
        path = base / source.source_file.replace("/", "__")
        if path.exists():
            texts[key] = path.read_text(encoding="utf-8", errors="ignore")
            continue
        if not fetch_missing:
            continue
        text = fetch_public_source(source.raw_url(snapshot.pinned_ref))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        texts[key] = text
    return texts


def fetch_public_source(url: str) -> str:
    request = urllib.request.Request(url, headers=github_headers())
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def resolve_source_snapshot(source_ref: str = SOURCE_REF) -> SourceSnapshot:
    commit_url = f"https://api.github.com/repos/{SOURCE_REPOSITORY}/commits/{urllib.parse.quote(source_ref, safe='')}"
    request = urllib.request.Request(commit_url, headers=github_headers())
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    source_commit = str(payload.get("sha") or "")
    commit = payload.get("commit") or {}
    committer = commit.get("committer") or {}
    source_commit_date = str(committer.get("date") or "")
    version_text = fetch_public_source(
        f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{source_commit or source_ref}/Directory.Build.props"
    )
    version_match = re.search(r"<Version>\s*([^<]+?)\s*</Version>", version_text)
    return SourceSnapshot(
        source_ref=source_ref,
        source_commit=source_commit,
        source_commit_date=source_commit_date,
        source_version=version_match.group(1).strip() if version_match else "",
    )


def github_headers() -> dict[str, str]:
    headers = {
        "User-Agent": "rock-kb-lava-context-builder",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def source_snapshot_path(source_dir: Path) -> Path:
    return source_dir / "snapshot.json"


def load_source_snapshot(source_dir: Path) -> SourceSnapshot:
    path = source_snapshot_path(source_dir)
    if not path.exists():
        return SourceSnapshot()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return SourceSnapshot()
    return SourceSnapshot(
        source_ref=str(payload.get("source_ref") or SOURCE_REF),
        source_commit=str(payload.get("source_commit") or ""),
        source_commit_date=str(payload.get("source_commit_date") or ""),
        source_version=str(payload.get("source_version") or ""),
    )


def write_source_snapshot(source_dir: Path, snapshot: SourceSnapshot) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    source_snapshot_path(source_dir).write_text(
        json.dumps(snapshot.as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def lava_context_rows(
    source_texts: dict[str, str],
    *,
    snapshot: SourceSnapshot | None = None,
    previous_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(parse_common_merge_fields("lava_helper", source_texts.get("lava_helper", ""), "global-lava-helper-common"))
    rows.extend(parse_common_merge_fields("request_context", source_texts.get("request_context", ""), "global-request-context-common"))
    for source_key, context_id, surface_name in LABEL_DATA_SPECS:
        rows.extend(parse_label_data(source_key, source_texts.get(source_key, ""), context_id, surface_name))
    rows.extend(parse_field_source_helper_person_label_paths(source_texts.get("field_source_helper", "")))
    rows.extend(parse_communication_merge_values(source_texts.get("communication_recipient", "")))
    rows.extend(parse_workflow_merge_fields(source_texts.get("workflow_action", "")))
    rows.extend(parse_curated_surface_contexts(source_texts))
    rows.extend(static_surface_boundary_rows(source_texts))
    return normalize_context_rows(rows, snapshot=snapshot, previous_rows=previous_rows)


def normalize_context_rows(
    rows: list[dict[str, Any]],
    *,
    snapshot: SourceSnapshot | None = None,
    previous_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    snapshot = snapshot or SourceSnapshot()
    model_links = model_map_links_by_slug()
    previous_first_seen = {
        context_identity(row): str(row.get("first_seen_version") or row.get("source_version") or "")
        for row in previous_rows or []
    }
    previous_aliases = {
        context_identity(row): {
            str(alias)
            for alias in [row.get("id"), *(row.get("legacy_ids") or [])]
            if alias
        }
        for row in previous_rows or []
    }
    normalized = []
    seen: set[tuple[str, str, str, str]] = set()
    for row in rows:
        key = context_identity(row)
        if key in seen:
            continue
        seen.add(key)
        metadata = CONTEXT_METADATA.get(str(row.get("context_id") or ""), {})
        row["schema"] = LAVA_CONTEXT_SCHEMA
        row["includes_context_ids"] = sorted(
            set(row.get("includes_context_ids") or metadata.get("includes_context_ids") or [])
        )
        row["availability_condition"] = str(
            row.get("availability_condition") or metadata.get("availability_condition") or "surface_selected"
        )
        row["coverage_status"] = str(row.get("coverage_status") or metadata.get("coverage_status") or "partial_curated")
        row["execution_phase"] = str(row.get("execution_phase") or metadata.get("execution_phase") or "render")
        row["may_be_null"] = bool(row.get("may_be_null", False))
        row["required_setting"] = str(row.get("required_setting") or "")
        if snapshot.source_commit and str(row.get("source_id") or "") == SOURCE_ID:
            row["source_ref"] = snapshot.source_ref
            row["source_commit"] = snapshot.source_commit
            row["source_commit_date"] = snapshot.source_commit_date
            row["source_version"] = snapshot.source_version
            row["source_url"] = pinned_source_url(row, snapshot.source_commit)
        else:
            row.setdefault("source_commit", "")
            row.setdefault("source_commit_date", "")
            row.setdefault("source_version", "")
        first_seen_version = previous_first_seen.get(key) or str(row.get("source_version") or "")
        row["first_seen_version"] = first_seen_version
        row["last_seen_version"] = str(row.get("source_version") or first_seen_version)
        model_slug = row.get("model_slug")
        row["model_map_links"] = model_links.get(str(model_slug), []) if model_slug else []
        old_id = legacy_lava_context_id(row)
        row["id"] = lava_context_id(row)
        row["legacy_ids"] = sorted(
            (
                set(row.get("legacy_ids") or [])
                | previous_aliases.get(key, set())
                | {old_id}
            )
            - {row["id"]}
        )
        normalized.append(row)
    return sorted(
        normalized,
        key=lambda row: (
            str(row.get("context_family") or ""),
            str(row.get("context_id") or ""),
            str(row.get("root_key") or ""),
            str(row.get("nested_path") or ""),
            str(row.get("source_symbol") or ""),
        ),
    )


def parse_common_merge_fields(source_key: str, text: str, context_id: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES[source_key]
    if source_key == "lava_helper":
        surface_name = "Global common Lava merge fields"
        notes = "Common fields returned by LavaHelper.GetCommonMergeFields for Web Forms/page Lava surfaces."
    else:
        surface_name = "Rock request-context common Lava merge fields"
        notes = "Common fields returned by RockRequestContext.GetCommonMergeFields for request-context and Obsidian/block-action surfaces."
    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.search(r'mergeFields\.Add\(\s*"([^"]+)"\s*,\s*(.*?)\s*\);', line)
        if not match:
            continue
        root_key = match.group(1)
        root_type, model_slug, value_kind = COMMON_KEY_TYPE_MAP.get(root_key, ("object", None, "unknown"))
        rows.append(
            context_row(
                context_id=context_id,
                context_family="global",
                surface_name=surface_name,
                surface_type="common_merge_fields",
                concept_ids=DEFAULT_CONCEPT_IDS,
                root_key=root_key,
                root_type=root_type,
                model_slug=model_slug,
                value_kind=value_kind,
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes=notes,
                needs_live_verification=root_key in {"Context", "PageParameter", "CurrentPerson", "CurrentVisitor", "Device", "Geolocation"},
                availability_condition=common_root_condition(root_key),
                may_be_null=root_key in {"CurrentPerson", "CurrentVisitor", "Device", "Geolocation"},
                execution_phase="request",
                coverage_status="complete_for_source_snapshot",
            )
        )
    return rows


def common_root_condition(root_key: str) -> str:
    return {
        "CurrentPerson": "A person is authenticated or otherwise resolved for the current request.",
        "CurrentVisitor": "A visitor person alias is available for the current request.",
        "Device": "The request originated from a supported mobile/device context.",
        "Geolocation": "The request includes resolvable geolocation data.",
        "PageParameter": "The rendering surface has page or route parameters.",
        "Context": "The rendering surface contributes context entities.",
    }.get(root_key, "Common merge fields were requested for this rendering surface.")


def parse_person_label_data(text: str) -> list[dict[str, Any]]:
    return parse_label_data(
        "person_label_data",
        text,
        "check-in-label-person-dynamic-text",
        "Check-In Label Designer Person Dynamic Text",
    )


def parse_label_data(
    source_key: str,
    text: str,
    context_id: str,
    surface_name: str,
) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES[source_key]
    rows = []
    property_pattern = re.compile(
        r"public\s+([^;{}=]+?)\s+([A-Za-z][A-Za-z0-9_]*)\s*(?:\{\s*get;\s*(?:set;\s*)?\}|=>)"
    )
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = property_pattern.search(line)
        if not match:
            continue
        raw_type = normalize_cs_type(match.group(1))
        root_key = match.group(2)
        root_type, model_slug, value_kind = classify_cs_type(raw_type)
        rows.append(
            context_row(
                context_id=context_id,
                context_family="check-in-label",
                surface_name=surface_name,
                surface_type="label_dynamic_text",
                concept_ids=CHECK_IN_CONCEPT_IDS,
                root_key=root_key,
                root_type=root_type,
                model_slug=model_slug,
                value_kind=value_kind,
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes=f"{source.source_symbol} property exposed to Check-In label Dynamic Text through the selected label data object.",
                needs_live_verification=False,
                availability_condition=f"The label renderer selected the {source.source_symbol} data type.",
                may_be_null=root_key in {"Attendance", "Family", "Location", "Person"},
                execution_phase="label_render",
                coverage_status="complete_for_source_snapshot",
            )
        )
    if source_key == "person_label_data":
        rows.extend(parse_person_attendance_assignment_paths(text, source))
    return rows


def parse_person_attendance_assignment_paths(text: str, source: SourceFile) -> list[dict[str, Any]]:
    rows = []
    patterns = [
        re.compile(r"(?P<label>\w+)\s*=\s*PersonAttendance\.Select\( a => a\.(?P<nested>\w+)\.Name \)"),
        re.compile(r"(?P<label>\w+)\s*=\s*PersonAttendance\.Select\( a => a\.(?P<nested>SecurityCode) \)"),
        re.compile(r"(?P<label>\w+)\s*=\s*PersonAttendance\.Any\( a => a\.(?P<nested>IsFirstTime) \)"),
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            match = pattern.search(line)
            if not match:
                continue
            nested = match.group("nested")
            root_type, model_slug, value_kind = LABEL_NESTED_MODEL_MAP.get(nested, ("LabelAttendanceDetail", None, "scalar"))
            rows.append(
                context_row(
                    context_id="check-in-label-person-dynamic-text",
                    context_family="check-in-label",
                    surface_name="Check-In Label Designer Person Dynamic Text",
                    surface_type="label_dynamic_text_nested_path",
                    concept_ids=CHECK_IN_CONCEPT_IDS,
                    root_key="PersonAttendance",
                    root_type=root_type,
                    model_slug=model_slug,
                    value_kind=value_kind,
                    nested_path=f"PersonAttendance.{nested}",
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes=f"Nested path used while deriving the `{match.group('label')}` label data property.",
                    needs_live_verification=False,
                    availability_condition="The label renderer selected the PersonLabelData data type.",
                    execution_phase="label_render",
                    coverage_status="complete_for_source_snapshot",
                )
            )
    return rows


def parse_field_source_helper_person_label_paths(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["field_source_helper"]
    rows = []
    patterns = [
        re.compile(r"source\.PersonAttendance\.FirstOrDefault\(\)\?\.(?P<nested>\w+)"),
        re.compile(r"source\.PersonAttendance\.Select\( a => a\.(?P<nested>\w+)"),
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            match = pattern.search(line)
            if not match:
                continue
            nested = match.group("nested")
            if nested not in LABEL_NESTED_MODEL_MAP:
                continue
            root_type, model_slug, value_kind = LABEL_NESTED_MODEL_MAP[nested]
            rows.append(
                context_row(
                    context_id="check-in-label-person-field-sources",
                    context_family="check-in-label",
                    surface_name="Check-In Label Designer Person field sources",
                    surface_type="label_field_source",
                    concept_ids=CHECK_IN_CONCEPT_IDS,
                    root_key="PersonAttendance",
                    root_type=root_type,
                    model_slug=model_slug,
                    value_kind=value_kind,
                    nested_path=f"PersonAttendance.{nested}",
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes="FieldSourceHelper references this nested person-attendance path while building Check-In label data sources.",
                    needs_live_verification=False,
                )
            )
    return rows


def parse_communication_merge_values(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["communication_recipient"]
    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.search(r'mergeValues\.Add\(\s*"([^"]+)"\s*,\s*(.*?)\s*\);', line)
        if match:
            root_key = match.group(1)
            root_type, model_slug, value_kind = {
                "Communication": TYPE_MODEL_MAP["Communication"],
                "Person": TYPE_MODEL_MAP["Person"],
            }.get(root_key, ("object", None, "unknown"))
            rows.append(
                context_row(
                    context_id="communication-recipient-merge-values",
                    context_family="communication",
                    surface_name="Communication recipient merge values",
                    surface_type="communication_template_merge_values",
                    concept_ids=COMMUNICATION_CONCEPT_IDS,
                    root_key=root_key,
                    root_type=root_type,
                    model_slug=model_slug,
                    value_kind=value_kind,
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes="CommunicationRecipient.CommunicationMergeValues adds this root when preparing recipient Lava merge values.",
                    needs_live_verification=False,
                )
            )
        if "mergeValues.Add( entityTypeType.Name, mergeEntity )" in line:
            rows.append(
                context_row(
                    context_id="communication-recipient-merge-values",
                    context_family="communication",
                    surface_name="Communication recipient additional merge values",
                    surface_type="communication_template_dynamic_merge_values",
                    concept_ids=COMMUNICATION_CONCEPT_IDS,
                    root_key="AdditionalMergeValues",
                    root_type="dynamic entity or scalar",
                    model_slug=None,
                    value_kind="dynamic",
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes="Additional merge values may add an entity by entity type name or a scalar by merge field key; inspect the communication/report setup before relying on a specific root.",
                    needs_live_verification=True,
                )
            )
    return rows


def parse_workflow_merge_fields(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["workflow_action"]
    rows = []
    current_symbol = ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "protected Dictionary<string, object> GetMergeFields( WorkflowAction action )" in line:
            current_symbol = "ActionComponent.GetMergeFields(WorkflowAction)"
        elif "protected Dictionary<string, object> GetMergeFields( WorkflowAction action, RockRequestContext requestContext )" in line:
            current_symbol = "ActionComponent.GetMergeFields(WorkflowAction,RockRequestContext)"
        match = re.search(r'mergeFields\.Add\(\s*"([^"]+)"\s*,\s*(.*?)\s*\);', line)
        if not match or not current_symbol:
            continue
        root_key = match.group(1)
        root_type, model_slug, value_kind = {
            "Action": TYPE_MODEL_MAP["WorkflowAction"],
            "Activity": TYPE_MODEL_MAP["WorkflowActivity"],
            "Workflow": TYPE_MODEL_MAP["Workflow"],
        }.get(root_key, ("object", None, "unknown"))
        rows.append(
            context_row(
                context_id="workflow-action-component-merge-fields",
                context_family="workflow",
                surface_name="Workflow action component Lava merge fields",
                surface_type="workflow_action_merge_fields",
                concept_ids=WORKFLOW_CONCEPT_IDS,
                root_key=root_key,
                root_type=root_type,
                model_slug=model_slug,
                value_kind=value_kind,
                source=source,
                source_symbol=current_symbol,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes="Workflow ActionComponent.GetMergeFields adds this root when resolving Lava in workflow action components.",
                needs_live_verification=False,
            )
        )
    return rows


def parse_curated_surface_contexts(source_texts: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in CURATED_CONTEXT_SPECS:
        text = source_texts.get(spec.source_key, "")
        if not text:
            continue
        source = SOURCE_FILES[spec.source_key]
        for root in spec.roots:
            line_number = find_curated_root_line(text, root)
            if line_number is None:
                continue
            rows.append(
                context_row(
                    context_id=spec.context_id,
                    context_family=spec.context_family,
                    surface_name=spec.surface_name,
                    surface_type=spec.surface_type,
                    concept_ids=list(spec.concept_ids),
                    root_key=root.root_key,
                    root_type=root.root_type,
                    model_slug=root.model_slug,
                    value_kind=root.value_kind,
                    nested_path=root.nested_path,
                    source=source,
                    source_symbol=root.source_symbol or spec.source_symbol,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability=root.availability,
                    notes=root.notes or spec.notes,
                    needs_live_verification=root.needs_live_verification,
                    includes_context_ids=list(spec.includes_context_ids),
                    availability_condition=root.availability_condition
                    if root.availability_condition != "always"
                    else spec.availability_condition,
                    may_be_null=root.may_be_null,
                    required_setting=root.required_setting,
                    execution_phase=root.execution_phase,
                    coverage_status=spec.coverage_status,
                )
            )
    return rows


def find_curated_root_line(text: str, root: CuratedContextRoot) -> int | None:
    patterns = root.source_patterns or curated_root_patterns(root.root_key)
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(re.search(pattern, line) for pattern in patterns):
            return line_number
    return None


def curated_root_patterns(root_key: str) -> tuple[str, ...]:
    escaped = re.escape(root_key)
    merge_field_variables = (
        "mergeFields",
        "itemMergeFields",
        "introMessageMergeFields",
        "feeCoverageMergeFields",
        "amountSummaryMergeFields",
    )
    merge_field_expression = "|".join(merge_field_variables)
    return (
        rf"\b(?:{merge_field_expression})\.(?:Add|AddOrReplace|TryAdd)\(\s*\"{escaped}\"\s*,",
        rf"\[\s*\"{escaped}\"\s*\]\s*=",
        rf"\{{\s*\"{escaped}\"\s*,",
        rf"\{{\s*MergeFieldKey\.{escaped}\s*,",
    )


def static_surface_boundary_rows(source_texts: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for source_key, context_id, family, surface_name, concept_ids, notes in [
        (
            "label_field",
            "check-in-label-field-definition",
            "check-in-label",
            "Check-In Label Designer field definition",
            CHECK_IN_CONCEPT_IDS,
            "LabelField exposes field configuration, but not arbitrary Lava roots; use label data rows for Dynamic Text context roots.",
        ),
        (
            "field_source_helper",
            "check-in-label-field-source-directory",
            "check-in-label",
            "Check-In Label Designer field-source directory",
            CHECK_IN_CONCEPT_IDS,
            "FieldSourceHelper defines available formatted label fields and filters; do not treat every field source as a raw Lava root.",
        ),
    ]:
        text = source_texts.get(source_key, "")
        if not text:
            continue
        source = SOURCE_FILES[source_key]
        line_number = first_interesting_line(text, source.source_symbol)
        rows.append(
            context_row(
                context_id=context_id,
                context_family=family,
                surface_name=surface_name,
                surface_type="surface_boundary",
                concept_ids=concept_ids,
                root_key="source-boundary",
                root_type="source-code boundary",
                model_slug=None,
                value_kind="boundary",
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes=notes,
                needs_live_verification=True,
            )
        )
    return rows


def context_row(
    *,
    context_id: str,
    context_family: str,
    surface_name: str,
    surface_type: str,
    concept_ids: list[str],
    root_key: str,
    root_type: str,
    model_slug: str | None,
    value_kind: str,
    source: SourceFile,
    source_line_start: int,
    source_line_end: int,
    availability: str,
    notes: str,
    needs_live_verification: bool,
    nested_path: str = "",
    source_symbol: str | None = None,
    includes_context_ids: list[str] | None = None,
    availability_condition: str = "surface_selected",
    may_be_null: bool = False,
    required_setting: str = "",
    execution_phase: str = "render",
    coverage_status: str = "partial_curated",
) -> dict[str, Any]:
    return {
        "schema": LAVA_CONTEXT_SCHEMA,
        "context_id": context_id,
        "context_family": context_family,
        "surface_name": surface_name,
        "surface_type": surface_type,
        "concept_ids": concept_ids,
        "root_key": root_key,
        "root_type": root_type,
        "model_slug": model_slug,
        "value_kind": value_kind,
        "nested_path": nested_path,
        "availability": availability,
        "source_id": SOURCE_ID,
        "source_url": source_url(source, source_line_start, source_line_end),
        "source_file": source.source_file,
        "source_symbol": source_symbol or source.source_symbol,
        "source_line_start": source_line_start,
        "source_line_end": source_line_end,
        "source_ref": SOURCE_REF,
        "model_map_links": [],
        "notes": notes,
        "needs_live_verification": needs_live_verification,
        "includes_context_ids": includes_context_ids or [],
        "availability_condition": availability_condition,
        "may_be_null": may_be_null,
        "required_setting": required_setting,
        "execution_phase": execution_phase,
        "coverage_status": coverage_status,
    }


def source_url(source: SourceFile, start: int, end: int, source_ref: str = SOURCE_REF) -> str:
    if start == end:
        return f"{source.blob_url(source_ref)}#L{start}"
    return f"{source.blob_url(source_ref)}#L{start}-L{end}"


def pinned_source_url(row: dict[str, Any], source_commit: str) -> str:
    source_file = str(row.get("source_file") or "")
    start = int(row.get("source_line_start") or 1)
    end = int(row.get("source_line_end") or start)
    source = SourceFile("row", source_file, str(row.get("source_symbol") or ""))
    return source_url(source, start, end, source_commit)


def context_identity(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("context_id") or ""),
        str(row.get("root_key") or ""),
        str(row.get("nested_path") or ""),
        str(row.get("source_symbol") or ""),
    )


def lava_context_id(row: dict[str, Any]) -> str:
    stable = "|".join(
        str(row.get(key) or "")
        for key in ["context_id", "root_key", "nested_path", "source_symbol"]
    )
    return f"lava_context:{row.get('context_id')}:{normalize_key(str(row.get('root_key') or 'root'))}:{sha256_text(stable)[:8]}"


def legacy_lava_context_id(row: dict[str, Any]) -> str:
    stable = "|".join(
        str(row.get(key) or "")
        for key in ["context_id", "root_key", "nested_path", "source_symbol", "source_file", "source_line_start"]
    )
    return f"lava_context:{row.get('context_id')}:{normalize_key(str(row.get('root_key') or 'root'))}:{sha256_text(stable)[:8]}"


def normalize_cs_type(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("?", "")).strip()


def classify_cs_type(raw_type: str) -> tuple[str, str | None, str]:
    type_name = raw_type
    list_match = re.match(r"(?:List|IEnumerable|ICollection)<(.+)>", raw_type)
    if list_match:
        inner = normalize_cs_type(list_match.group(1))
        root_type, model_slug, _ = TYPE_MODEL_MAP.get(inner, (inner, None, "object"))
        if inner in {"string", "int", "bool", "DateTime", "Guid", "decimal"}:
            return raw_type, None, "scalar_collection"
        return f"List<{root_type}>", model_slug, "collection"
    if type_name in TYPE_MODEL_MAP:
        return TYPE_MODEL_MAP[type_name]
    if type_name in {"string", "int", "bool", "DateTime", "Guid", "decimal"}:
        return type_name, None, "scalar"
    return type_name, None, "object"


def first_interesting_line(text: str, needle: str) -> int:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return line_number
    return 1


def validate_lava_context_extension(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        manifest = LavaContextExtensionManifest.model_validate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return {
            "schema": "rock-kb-lava-context-extension-validation-v1",
            "status": "invalid",
            "path": path.name,
            "errors": [str(exc)],
        }
    return {
        "schema": "rock-kb-lava-context-extension-validation-v1",
        "status": "valid",
        "path": path.name,
        "extension_id": manifest.extension_id,
        "context_count": len(manifest.contexts),
        "root_count": sum(len(context.roots) for context in manifest.contexts),
    }


def load_public_extension_rows(snapshot: SourceSnapshot | None = None) -> list[dict[str, Any]]:
    del snapshot
    rows: list[dict[str, Any]] = []
    if not PUBLIC_EXTENSION_DIR.exists():
        return rows
    for path in sorted(PUBLIC_EXTENSION_DIR.glob("*/*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        manifest = LavaContextExtensionManifest.model_validate(payload)
        source_id = f"community_lava_context:{manifest.org_id}"
        for context in manifest.contexts:
            for root in context.roots:
                source_url = (
                    f"{manifest.repository_url.rstrip('/')}/blob/{manifest.commit_sha}/{root.source_path}"
                    f"#L{root.source_line_start}"
                )
                if root.source_line_end != root.source_line_start:
                    source_url += f"-L{root.source_line_end}"
                rows.append(
                    {
                        "schema": LAVA_CONTEXT_SCHEMA,
                        "context_id": context.context_id,
                        "context_family": context.context_family,
                        "surface_name": context.surface_name,
                        "surface_type": context.surface_type,
                        "concept_ids": context.concept_ids,
                        "root_key": root.root_key,
                        "root_type": root.root_type,
                        "model_slug": root.model_slug,
                        "value_kind": root.value_kind,
                        "nested_path": root.nested_path,
                        "availability": "community-source-code-confirmed",
                        "source_id": source_id,
                        "source_url": source_url,
                        "source_file": root.source_path,
                        "source_symbol": root.source_symbol,
                        "source_line_start": root.source_line_start,
                        "source_line_end": root.source_line_end,
                        "source_ref": manifest.commit_sha,
                        "source_commit": manifest.commit_sha,
                        "source_commit_date": "",
                        "source_version": manifest.source_version,
                        "model_map_links": [],
                        "notes": root.notes,
                        "needs_live_verification": root.needs_live_verification,
                        "includes_context_ids": context.includes_context_ids,
                        "availability_condition": root.availability_condition or context.availability_condition,
                        "may_be_null": root.may_be_null,
                        "required_setting": root.required_setting,
                        "execution_phase": root.execution_phase,
                        "coverage_status": context.coverage_status,
                        "authority_tier": "community-reviewed",
                        "claim_tier": "source_backed",
                        "extension_id": manifest.extension_id,
                        "license": manifest.license,
                        "license_url": manifest.license_url,
                    }
                )
    return rows


DISCOVERY_ROOT_PATTERN = re.compile(
    r"\b(?:mergeFields|mergeValues|itemMergeFields|introMessageMergeFields|feeCoverageMergeFields|amountSummaryMergeFields)"
    r"(?:\.(?:Add|AddOrReplace|TryAdd)\(\s*|\[\s*)\"([A-Za-z][A-Za-z0-9_]*)\""
)
DISCOVERY_CONTEXT_PATTERN = re.compile(r"\b(?:GetMergeFields|ResolveMergeFields|ResolveMergeFieldsWithCurrentPerson)\b")
METHOD_PATTERN = re.compile(
    r"\b(?:public|private|protected|internal)\s+(?:static\s+)?(?:async\s+)?[\w<>,?.\[\]\s]+\s+([A-Za-z][A-Za-z0-9_]*)\s*\("
)


def discover_lava_context_candidates(
    source_tree: Path,
    output_path: Path = DISCOVERY_QUEUE_JSONL,
    *,
    source_commit: str = "",
    source_version: str = "",
) -> dict[str, Any]:
    source_tree = source_tree.expanduser().resolve()
    if not source_tree.is_dir():
        raise ValueError("source_tree must be an existing Rock source checkout")
    tracked_files = {source.source_file for source in SOURCE_FILES.values()}
    candidates = []
    for path in sorted(source_tree.rglob("*.cs")):
        try:
            relative = path.relative_to(source_tree).as_posix()
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        root_keys = sorted(set(DISCOVERY_ROOT_PATTERN.findall(text)))
        has_context_method = bool(DISCOVERY_CONTEXT_PATTERN.search(text))
        if not root_keys and not has_context_method:
            continue
        symbols = discovered_symbols(text)
        identity = "|".join([relative, ",".join(root_keys), ",".join(symbols)])
        candidates.append(
            {
                "schema": LAVA_CONTEXT_DISCOVERY_SCHEMA,
                "candidate_id": f"lava_context_candidate:{sha256_text(identity)[:16]}",
                "source_id": SOURCE_ID,
                "source_file": relative,
                "source_commit": source_commit,
                "source_version": source_version,
                "content_hash": sha256_text(text),
                "context_family_hint": infer_context_family(relative),
                "source_symbols": symbols,
                "root_keys": root_keys,
                "pattern_count": len(root_keys),
                "already_tracked": relative in tracked_files,
                "review_status": "tracked" if relative in tracked_files else "pending",
                "notes": "Candidate only. Review the rendering call path and conditions before promotion.",
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_path, candidates)
    return {
        "schema": "rock-kb-lava-context-discovery-result-v1",
        "source_commit": source_commit,
        "source_version": source_version,
        "candidate_count": len(candidates),
        "pending_count": sum(1 for row in candidates if row["review_status"] == "pending"),
        "tracked_count": sum(1 for row in candidates if row["review_status"] == "tracked"),
        "queue_path": output_path.relative_to(REPO_ROOT).as_posix()
        if output_path.is_relative_to(REPO_ROOT)
        else output_path.name,
    }


def discovered_symbols(text: str) -> list[str]:
    symbols = []
    current_symbol = ""
    for line in text.splitlines():
        match = METHOD_PATTERN.search(line)
        if match:
            current_symbol = match.group(1)
        if (DISCOVERY_ROOT_PATTERN.search(line) or DISCOVERY_CONTEXT_PATTERN.search(line)) and current_symbol:
            symbols.append(current_symbol)
    return sorted(set(symbols))[:50]


def infer_context_family(source_file: str) -> str:
    lowered = source_file.lower()
    hints = [
        ("checkin", "check-in-label"),
        ("communication", "communication"),
        ("workflow", "workflow"),
        ("prayer", "prayer"),
        ("finance", "finance-lava"),
        ("event", "event-lava"),
        ("registration", "event-registration"),
        ("group", "group-lava"),
        ("mobile", "mobile-block"),
        ("report", "reporting-lava"),
        ("cms", "cms-block"),
        ("lms", "lms-lava"),
        ("connection", "connections-lava"),
    ]
    return next((family for token, family in hints if token in lowered), "other")


def validate_private_lava_context_overlay(path: Path) -> dict[str, Any]:
    errors = []
    rows = list(read_jsonl(path))
    for index, row in enumerate(rows, start=1):
        label = f"row {index}"
        if row.get("schema") != "rock-kb-private-lava-context-overlay-v1":
            errors.append(f"{label}: invalid schema")
        if row.get("access_scope") not in {"organization", "installation"}:
            errors.append(f"{label}: access_scope must be organization or installation")
        if not row.get("context_id") or not row.get("root_key"):
            errors.append(f"{label}: context_id and root_key are required")
        if row.get("publish") is not False:
            errors.append(f"{label}: publish must be false")
        if any(key in row for key in {"person_id", "entity_id", "query", "secret", "token"}):
            errors.append(f"{label}: private identifiers, queries, and secrets are forbidden")
    return {
        "schema": "rock-kb-private-lava-context-overlay-validation-v1",
        "status": "invalid" if errors else "valid",
        "row_count": len(rows),
        "errors": errors,
        "public_export_eligible": False,
    }


def list_lava_context_surfaces(
    rows: list[dict[str, Any]],
    *,
    context_family: str | None = None,
    surface_type: str | None = None,
) -> dict[str, Any]:
    """Return one compact, exact-retrieval row per Lava rendering surface."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        context_id = str(row.get("context_id") or "")
        if not context_id:
            continue
        if context_family and row.get("context_family") != context_family:
            continue
        if surface_type and row.get("surface_type") != surface_type:
            continue
        grouped.setdefault(context_id, []).append(row)

    surfaces = []
    for context_id, context_rows in grouped.items():
        first = context_rows[0]
        surfaces.append(
            {
                "context_id": context_id,
                "context_family": first.get("context_family"),
                "surface_name": first.get("surface_name"),
                "surface_type": first.get("surface_type"),
                "concept_ids": sorted(
                    {
                        str(concept_id)
                        for row in context_rows
                        for concept_id in row.get("concept_ids") or []
                        if concept_id
                    }
                ),
                "coverage_status": surface_coverage_status(context_rows),
                "includes_context_ids": sorted(
                    {
                        str(included_id)
                        for row in context_rows
                        for included_id in row.get("includes_context_ids") or []
                        if included_id
                    }
                ),
                "direct_root_count": len(context_rows),
                "root_keys": sorted({str(row.get("root_key") or "") for row in context_rows if row.get("root_key")}),
                "source_version": first_nonempty(context_rows, "source_version"),
                "source_commit": first_nonempty(context_rows, "source_commit"),
                "needs_live_verification": any(row.get("needs_live_verification") for row in context_rows),
            }
        )
    return {
        "schema": "rock-kb-lava-context-surface-list-v1",
        "count": len(surfaces),
        "filters": {
            "context_family": context_family,
            "surface_type": surface_type,
        },
        "surfaces": sorted(surfaces, key=lambda row: (str(row["context_family"]), str(row["surface_name"]))),
    }


def get_lava_context_surface(
    rows: list[dict[str, Any]],
    context_id: str,
    *,
    root_key: str | None = None,
) -> dict[str, Any]:
    """Return one complete surface with explicitly inherited context rows."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        row_context_id = str(row.get("context_id") or "")
        if row_context_id:
            grouped.setdefault(row_context_id, []).append(row)

    matched_id = next(
        (
            candidate
            for candidate in grouped
            if normalize_key(candidate) == normalize_key(context_id)
        ),
        None,
    )
    if not matched_id:
        return {
            "schema": "rock-kb-lava-context-surface-result-v1",
            "status": "not_found",
            "context_id": context_id,
        }

    direct_rows = grouped[matched_id]
    included_ids = sorted(
        {
            str(included_id)
            for row in direct_rows
            for included_id in row.get("includes_context_ids") or []
            if included_id
        }
    )
    inherited_rows: list[dict[str, Any]] = []
    missing_includes: list[str] = []
    visited = {matched_id}

    def collect_inherited(parent_id: str) -> None:
        if parent_id in visited:
            return
        visited.add(parent_id)
        parent_rows = grouped.get(parent_id)
        if not parent_rows:
            missing_includes.append(parent_id)
            return
        for row in parent_rows:
            inherited_rows.append({**row, "defined_in_context_id": parent_id, "inherited": True})
        for row in parent_rows:
            for included_id in row.get("includes_context_ids") or []:
                collect_inherited(str(included_id))

    for included_id in included_ids:
        collect_inherited(included_id)

    combined_rows = [
        {**row, "defined_in_context_id": matched_id, "inherited": False}
        for row in direct_rows
    ] + inherited_rows
    if root_key:
        normalized_root = normalize_key(root_key)
        combined_rows = [
            row
            for row in combined_rows
            if normalized_root
            in {
                normalize_key(str(row.get("root_key") or "")),
                normalize_key(str(row.get("nested_path") or "")),
            }
        ]

    first = direct_rows[0]
    return {
        "schema": "rock-kb-lava-context-surface-result-v1",
        "status": "ok",
        "query": {
            "context_id": context_id,
            "root_key": root_key,
        },
        "surface": {
            "context_id": matched_id,
            "context_family": first.get("context_family"),
            "surface_name": first.get("surface_name"),
            "surface_type": first.get("surface_type"),
            "concept_ids": sorted(
                {
                    str(concept_id)
                    for row in direct_rows
                    for concept_id in row.get("concept_ids") or []
                    if concept_id
                }
            ),
            "coverage_status": surface_coverage_status(direct_rows),
            "availability_conditions": sorted(
                {
                    str(row.get("availability_condition") or "")
                    for row in direct_rows
                    if row.get("availability_condition")
                }
            ),
            "execution_phases": sorted(
                {
                    str(row.get("execution_phase") or "")
                    for row in direct_rows
                    if row.get("execution_phase")
                }
            ),
            "includes_context_ids": included_ids,
            "source_version": first_nonempty(direct_rows, "source_version"),
            "source_commit": first_nonempty(direct_rows, "source_commit"),
        },
        "root_filter": root_key,
        "root_count": len(combined_rows),
        "direct_root_count": sum(1 for row in combined_rows if not row["inherited"]),
        "inherited_root_count": sum(1 for row in combined_rows if row["inherited"]),
        "roots": sorted(
            combined_rows,
            key=lambda row: (
                bool(row.get("inherited")),
                str(row.get("defined_in_context_id") or ""),
                str(row.get("root_key") or ""),
                str(row.get("nested_path") or ""),
            ),
        ),
        "composition_warnings": [
            f"Included context `{included_id}` is missing from this artifact."
            for included_id in sorted(set(missing_includes))
        ],
    }


def surface_coverage_status(rows: list[dict[str, Any]]) -> str:
    statuses = {str(row.get("coverage_status") or "partial_curated") for row in rows}
    priority = [
        "dynamic",
        "partial_curated",
        "reviewed_curated",
        "complete_for_source_snapshot",
    ]
    return next((status for status in priority if status in statuses), sorted(statuses)[0])


def first_nonempty(rows: list[dict[str, Any]], field: str) -> str:
    return next((str(row.get(field)) for row in rows if row.get(field)), "")


def model_map_links_by_slug() -> dict[str, list[dict[str, Any]]]:
    links: dict[str, list[dict[str, Any]]] = {}
    for digest in read_jsonl(AGENT_DIR / "model-map-digests.jsonl"):
        identity = digest.get("identity") or {}
        slug = str(identity.get("model_slug") or "")
        if not slug:
            continue
        links[slug] = [
            {
                "model_slug": slug,
                "model_name": identity.get("model_name"),
                "model_title": identity.get("model_title"),
                "model_detail_path": identity.get("model_detail_path"),
                "rock_version": identity.get("rock_version"),
            }
        ]
    return links


def lava_context_source_dependencies(
    source_texts: dict[str, str],
    snapshot: SourceSnapshot | None = None,
) -> list[dict[str, Any]]:
    snapshot = snapshot or SourceSnapshot()
    rows = []
    for key, text in sorted(source_texts.items()):
        source = SOURCE_FILES.get(key)
        if not source:
            continue
        rows.append(
            {
                "source_id": SOURCE_ID,
                "source_ref": snapshot.source_ref,
                "source_commit": snapshot.source_commit,
                "source_commit_date": snapshot.source_commit_date,
                "source_version": snapshot.source_version,
                "source_file": source.source_file,
                "source_url": source.blob_url(snapshot.pinned_ref),
                "content_hash": sha256_text(text),
            }
        )
    return rows


def write_lava_context_artifacts(rows: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> None:
    LAVA_CONCEPT_DIR.mkdir(parents=True, exist_ok=True)
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(CONTEXT_JSONL, rows)
    write_jsonl(AGENT_CONTEXT_JSONL, rows)
    CONTEXT_INDEX.write_text(render_lava_context_directory(rows, source_dependencies), encoding="utf-8")
    summary = lava_context_summary(rows, source_dependencies)
    AGENT_CONTEXT_SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    source_metadata = source_dependencies[0] if source_dependencies else {}
    CONTEXT_DEPENDENCY_JSON.write_text(
        json.dumps(
            {
                "schema": LAVA_CONTEXT_DEPENDENCIES_SCHEMA,
                "generated_at": generated_at_iso(),
                "source_id": SOURCE_ID,
                "source_ref": source_metadata.get("source_ref") or SOURCE_REF,
                "source_commit": source_metadata.get("source_commit") or "",
                "source_commit_date": source_metadata.get("source_commit_date") or "",
                "source_version": source_metadata.get("source_version") or "",
                "source_dependencies": source_dependencies,
                "context_count": len(rows),
                "context_families": dict(sorted(Counter(row["context_family"] for row in rows).items())),
                "resource_paths": {
                    "contexts": relative_path(CONTEXT_JSONL),
                    "directory": relative_path(CONTEXT_INDEX),
                    "agent_contexts": relative_path(AGENT_CONTEXT_JSONL),
                    "agent_summary": relative_path(AGENT_CONTEXT_SUMMARY_JSON),
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def lava_context_summary(rows: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> dict[str, Any]:
    source_metadata = source_dependencies[0] if source_dependencies else {}
    return {
        "schema": LAVA_CONTEXT_SUMMARY_SCHEMA,
        "generated_at": generated_at_iso(),
        "source_id": SOURCE_ID,
        "source_ref": source_metadata.get("source_ref") or SOURCE_REF,
        "source_commit": source_metadata.get("source_commit") or "",
        "source_commit_date": source_metadata.get("source_commit_date") or "",
        "source_version": source_metadata.get("source_version") or "",
        "source_file_count": len(source_dependencies),
        "context_count": len(rows),
        "surface_count": len({row.get("context_id") for row in rows}),
        "context_families": dict(sorted(Counter(row["context_family"] for row in rows).items())),
        "surface_types": dict(sorted(Counter(row["surface_type"] for row in rows).items())),
        "availability": dict(sorted(Counter(row["availability"] for row in rows).items())),
        "coverage_status": dict(sorted(Counter(row["coverage_status"] for row in rows).items())),
        "needs_live_verification_count": sum(1 for row in rows if row.get("needs_live_verification")),
        "model_link_count": sum(1 for row in rows if row.get("model_map_links")),
        "extension_context_count": sum(1 for row in rows if row.get("source_id") != SOURCE_ID),
        "paths": {
            "contexts": relative_path(CONTEXT_JSONL),
            "directory": relative_path(CONTEXT_INDEX),
            "dependencies": relative_path(CONTEXT_DEPENDENCY_JSON),
            "agent_contexts": relative_path(AGENT_CONTEXT_JSONL),
        },
    }


def render_lava_context_directory(rows: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> str:
    family_counts = Counter(row["context_family"] for row in rows)
    lines = [
        "# Lava Data Context Directory",
        "",
        "Generated from public SparkDevNetwork/Rock source files. This directory answers which root objects are available in selected Lava rendering surfaces; use the Model Map after identifying a root object.",
        "",
        "## Agent Use",
        "",
        "1. Identify the rendering surface and context family.",
        "2. Use this directory to find available root keys and nested paths.",
        "3. Use `agent/model-map-digests.jsonl`, `uvx rock-kb model <slug>`, or `uvx rock-kb model-map get <slug>` to inspect properties for linked model roots.",
        "4. Use `agent/lava-capabilities.jsonl` for filters, commands, and Lava behavior.",
        "5. Treat rows marked for live verification as source-code leads that still depend on the page, block, communication, workflow, or label configuration.",
        "",
        "## Coverage",
        "",
        f"- Lava context rows: `{len(rows)}`",
        f"- Context surfaces: `{len({row.get('context_id') for row in rows})}`",
        f"- Public source files: `{len(source_dependencies)}`",
        f"- Pinned source commit: `{(source_dependencies[0].get('source_commit') if source_dependencies else '') or 'unavailable'}`",
        f"- Observed Rock source version: `{(source_dependencies[0].get('source_version') if source_dependencies else '') or 'unavailable'}`",
        "- Machine-readable rows: `lava-contexts.jsonl` and `../../../agent/lava-contexts.jsonl`",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"- `{family}`: {count}")
    lines.extend(["", "## Context Rows", "", "| Family | Surface | Root Key | Nested Path | Type | Coverage | Model Map | Verification | Source |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for row in rows:
        model_links = row.get("model_map_links") or []
        if model_links:
            first = model_links[0]
            model_text = f"`{first.get('model_slug')}`"
        else:
            model_text = ""
        verification = "live check" if row.get("needs_live_verification") else "source code"
        lines.append(
            f"| `{row['context_family']}` "
            f"| {escape_cell(row.get('surface_name'))} "
            f"| `{escape_cell(row.get('root_key'))}` "
            f"| {escape_cell(row.get('nested_path') or '')} "
            f"| {escape_cell(row.get('root_type'))} "
            f"| `{escape_cell(row.get('coverage_status'))}` "
            f"| {model_text} "
            f"| {verification} "
            f"| [source]({row['source_url']}) |"
        )
    lines.extend(["", "## Public Source Files", ""])
    for dependency in source_dependencies:
        lines.append(f"- [{dependency['source_file']}]({dependency['source_url']})")
    lines.append("")
    return "\n".join(lines)


def relative_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "root"
