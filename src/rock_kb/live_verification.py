from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .extract import generated_at_iso, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, REVIEW_DIR

LIVE_VERIFICATION_PROBES_PATH = REVIEW_DIR / "live-verification-probes.jsonl"
LIVE_VERIFICATION_REPORT_PATH = REVIEW_DIR / "live-verification-report.json"

VERIFY_ACTION = "verify_live_before_operational_answer"


PROBE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "security_auth": {
        "title": "Security, Auth, Page, And Block Boundaries",
        "terms": ["security", "permission", "access", "auth", "role", "page", "block"],
        "tables": ["Auth", "Page", "Block", "Group", "GroupMember", "PersonAlias"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Auth','Page','Block','Group','GroupMember','PersonAlias') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('Auth','Page','Block','Group','GroupMember','PersonAlias') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "workflow_connections": {
        "title": "Workflow And Connection Surfaces",
        "terms": ["workflow", "connection request", "connection type", "connection opportunity", "connector"],
        "tables": ["Workflow", "WorkflowType", "WorkflowActivityType", "WorkflowActionType", "ConnectionType", "ConnectionOpportunity", "ConnectionRequest", "ConnectionStatus"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Workflow','WorkflowType','WorkflowActivityType','WorkflowActionType','ConnectionType','ConnectionOpportunity','ConnectionRequest','ConnectionStatus') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('Workflow','WorkflowType','WorkflowActivityType','WorkflowActionType','ConnectionType','ConnectionOpportunity','ConnectionRequest','ConnectionStatus') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "data_reporting": {
        "title": "Data Views, Reports, Metrics, And SQL Reporting",
        "terms": ["data view", "report", "sql", "analytics", "metric", "dashboard"],
        "tables": ["DataView", "DataViewFilter", "Report", "ReportField", "Metric", "MetricValue", "PersistedDataset", "PersistedDatasetValue"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('DataView','DataViewFilter','Report','ReportField','Metric','MetricValue','PersistedDataset','PersistedDatasetValue') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('DataView','DataViewFilter','Report','ReportField','Metric','MetricValue','PersistedDataset','PersistedDatasetValue') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "mobile_checkin": {
        "title": "Mobile Check-In, Devices, Labels, Groups, Locations, And Schedules",
        "terms": ["mobile check-in", "check-in", "kiosk", "label", "geofence", "device"],
        "tables": ["Device", "DefinedType", "DefinedValue", "GroupType", "Group", "GroupLocation", "GroupLocationSchedule", "Location", "Schedule", "Attendance"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Device','DefinedType','DefinedValue','GroupType','Group','GroupLocation','GroupLocationSchedule','Location','Schedule','Attendance') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('Device','DefinedType','DefinedValue','GroupType','Group','GroupLocation','GroupLocationSchedule','Location','Schedule','Attendance') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "cms_lava": {
        "title": "CMS, Lava, Content Channels, Pages, And Blocks",
        "terms": ["content channel", "advanced html", "lava", "cms", "page", "block", "route"],
        "tables": ["Page", "PageRoute", "Block", "BlockType", "Site", "ContentChannel", "ContentChannelItem", "ContentChannelType", "Attribute", "AttributeValue"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Page','PageRoute','Block','BlockType','Site','ContentChannel','ContentChannelItem','ContentChannelType','Attribute','AttributeValue') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('Page','PageRoute','Block','BlockType','Site','ContentChannel','ContentChannelItem','ContentChannelType','Attribute','AttributeValue') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "people_notes": {
        "title": "People, Families, Notes, Note Types, Aliases, And Attributes",
        "terms": ["person profile", "person", "family", "note", "note type", "duplicate", "attribute"],
        "tables": ["Person", "PersonAlias", "Group", "GroupMember", "Note", "NoteType", "Attribute", "AttributeValue"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Person','PersonAlias','Group','GroupMember','Note','NoteType','Attribute','AttributeValue') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('Person','PersonAlias','Group','GroupMember','Note','NoteType','Attribute','AttributeValue') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "communications": {
        "title": "Communications, Recipients, Mediums, And Delivery",
        "terms": ["communication", "email", "sms", "push", "recipient", "medium"],
        "tables": ["Communication", "CommunicationRecipient", "CommunicationMedium", "CommunicationTemplate", "Person", "PhoneNumber"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Communication','CommunicationRecipient','CommunicationMedium','CommunicationTemplate','Person','PhoneNumber') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('Communication','CommunicationRecipient','CommunicationMedium','CommunicationTemplate','Person','PhoneNumber') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "finance": {
        "title": "Giving, Financial Transactions, Accounts, Gateways, And Receipts",
        "terms": ["giving", "financial", "transaction", "gateway", "receipt", "account"],
        "tables": ["FinancialTransaction", "FinancialTransactionDetail", "FinancialAccount", "FinancialGateway", "FinancialBatch", "FinancialScheduledTransaction"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('FinancialTransaction','FinancialTransactionDetail','FinancialAccount','FinancialGateway','FinancialBatch','FinancialScheduledTransaction') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('FinancialTransaction','FinancialTransactionDetail','FinancialAccount','FinancialGateway','FinancialBatch','FinancialScheduledTransaction') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
    "groups_scheduling": {
        "title": "Groups, Group Types, Scheduling, Locations, And Attendance",
        "terms": ["group", "schedule", "location", "attendance", "rsvp"],
        "tables": ["GroupType", "Group", "GroupMember", "GroupLocation", "GroupLocationSchedule", "Location", "Schedule", "Attendance"],
        "sql": [
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('GroupType','Group','GroupMember','GroupLocation','GroupLocationSchedule','Location','Schedule','Attendance') ORDER BY TABLE_NAME;",
            "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('GroupType','Group','GroupMember','GroupLocation','GroupLocationSchedule','Location','Schedule','Attendance') ORDER BY TABLE_NAME, ORDINAL_POSITION;",
        ],
    },
}


def classify_probe(row: dict[str, Any]) -> str:
    text = " ".join(
        [
            str(row.get("claim") or ""),
            " ".join(str(value) for value in row.get("concept_ids") or []),
            " ".join(str(value) for value in row.get("common_failure_mode") or []),
        ]
    ).lower()
    for probe_id, definition in PROBE_DEFINITIONS.items():
        if any(term in text for term in definition["terms"]):
            return probe_id
    return "general_instance_review"


def build_live_verification_probe_plan(queue_path: Path | None = None) -> dict[str, Any]:
    path = queue_path or AGENT_DIR / "claim-review-queue.jsonl"
    rows = [
        row
        for row in read_jsonl(path)
        if row.get("recommended_action") == VERIFY_ACTION
    ]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[classify_probe(row)].append(row)
    probe_rows = []
    for probe_type, claims in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        definition = PROBE_DEFINITIONS.get(probe_type, {})
        concept_ids = sorted({str(value) for row in claims for value in row.get("concept_ids") or []})
        claim_ids = [str(row.get("claim_id")) for row in sorted(claims, key=lambda item: (-int(item.get("operational_priority") or 0), str(item.get("claim_id") or ""))) if row.get("claim_id")]
        probe_rows.append(
            {
                "schema": "rock-kb-live-verification-probe-v1",
                "probe_id": "live-probe:" + sha256_text(probe_type)[:16],
                "probe_type": probe_type,
                "title": definition.get("title") or "General Instance Review",
                "status": "ready_for_read_only_probe" if definition else "needs_manual_target_binding",
                "claim_count": len(claim_ids),
                "claim_ids": claim_ids,
                "concept_ids": concept_ids,
                "read_only_sql_probes": definition.get("sql") or [],
                "expected_tables": definition.get("tables") or [],
                "sample_claims": [
                    {
                        "claim_id": row.get("claim_id"),
                        "claim": row.get("claim"),
                        "concept_ids": row.get("concept_ids") or [],
                    }
                    for row in claims[:8]
                ],
                "promotion_rule": "Promote a claim to live_verified only when the probe evidence directly verifies the named structural surface or concrete configured object in the claim.",
                "created_at": now_iso(),
            }
        )
    write_jsonl(LIVE_VERIFICATION_PROBES_PATH, probe_rows)
    report = {
        "schema": "rock-kb-live-verification-report-v1",
        "generated_at": generated_at_iso(),
        "source_queue": str(path),
        "probe_path": str(LIVE_VERIFICATION_PROBES_PATH),
        "probe_count": len(probe_rows),
        "claim_count": len(rows),
        "status_counts": dict(Counter(row["status"] for row in probe_rows)),
        "probe_type_counts": {row["probe_type"]: row["claim_count"] for row in probe_rows},
    }
    LIVE_VERIFICATION_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report
