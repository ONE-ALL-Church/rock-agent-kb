from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

from ..claims import approved_claim_dependencies_for_concept
from ..concepts import approved_media_dependencies_for_concept, get_concept, load_concepts, synthesis_output_path
from ..extract import generated_at_iso, now_iso, sha256_text
from ..jsonl import read_jsonl, write_jsonl
from ..paths import AGENT_DIR, CLAIMS_DIR, KNOWLEDGE_DIR, MEDIA_DIR, REPO_ROOT, REVIEW_DIR

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
VERSION_RE = re.compile(r"\b(?:Rock\s+)?v?(\d{1,2}(?:\.\d{1,2})?)\b", re.IGNORECASE)

KNOWN_ENTITY_TERMS = [
    "Attendance",
    "AttendanceOccurrence",
    "Person",
    "PersonAlias",
    "LearningProgram",
    "LearningCourse",
    "LearningClass",
    "LearningClassActivity",
    "LearningClassActivityCompletion",
    "LearningProgramCompletion",
    "LearningCourseRequirement",
    "LearningSemester",
    "LearningParticipant",
    "StepProgram",
    "StepType",
    "Step",
    "DataView",
    "Group",
    "GroupType",
    "GroupMember",
    "GroupMemberRequirement",
    "Location",
    "Schedule",
    "Campus",
    "Device",
    "Check-in Configuration",
    "Label",
    "SecurityCode",
    "Family",
    "Workflow",
    "Page",
    "Block",
    "DefinedType",
    "Attribute",
]

ENTITY_ALIASES = {
    "Device/Kiosk": ["Device", "Kiosk"],
    "Family Group": ["Family", "Family Group"],
    "GroupType": ["Group Type", "GroupType"],
    "LearningProgram": ["Learning Program", "LearningProgram"],
    "LearningCourse": ["Learning Course", "LearningCourse"],
    "LearningClass": ["Learning Class", "LearningClass"],
    "LearningClassActivity": ["Learning Class Activity", "LearningClassActivity"],
    "LearningClassActivityCompletion": ["Learning Class Activity Completion", "LearningClassActivityCompletion"],
    "LearningProgramCompletion": ["Learning Program Completion", "LearningProgramCompletion"],
    "LearningCourseRequirement": ["Learning Course Requirement", "LearningCourseRequirement"],
    "LearningSemester": ["Learning Semester", "LearningSemester"],
    "LearningParticipant": ["Learning Participant", "LearningParticipant"],
    "Mobile Block": ["Mobile Block", "Block"],
    "Mobile Page": ["Mobile Page", "Page"],
    "PersonAlias": ["Person Alias", "PersonAlias"],
    "StepProgram": ["Step Program", "StepProgram"],
    "StepType": ["Step Type", "StepType"],
    "DataView": ["Data View", "DataView"],
    "GroupMemberRequirement": ["Group Member Requirement", "GroupMemberRequirement"],
}

ENTITY_NOTES = {
    "Attendance": {
        "purpose": "Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.",
        "common_joins": ["AttendanceOccurrence", "PersonAlias"],
        "agent_notes": ["Filter `DidAttend` when counting actual attendance.", "Do not infer group/schedule/location without joining occurrence context."],
    },
    "AttendanceOccurrence": {
        "purpose": "Occurrence context for attendance, including group, schedule, location, date, and SundayDate.",
        "common_joins": ["Attendance", "Group", "Schedule", "Location", "Campus"],
        "agent_notes": ["Use this for reporting context.", "Check group, location, schedule, and SundayDate before blaming the UI."],
    },
    "Group": {
        "purpose": "Concrete attendance destination, room, service, team, class, or group.",
        "common_joins": ["GroupType", "Location", "Schedule", "AttendanceOccurrence"],
        "agent_notes": ["Verify active state, campus, group type, location, schedule, and capacity assumptions."],
    },
    "GroupType": {
        "purpose": "Rule container for groups, including attendance/check-in settings and inherited behavior.",
        "common_joins": ["Group"],
        "agent_notes": ["Confirm the type takes attendance and supports the intended check-in pattern."],
    },
    "Location": {
        "purpose": "Named physical or logical location used for rooms, campuses, buildings, and printer routing.",
        "common_joins": ["Group", "AttendanceOccurrence", "Device"],
        "agent_notes": ["Check active state, campus, location hierarchy, and printer behavior."],
    },
    "Schedule": {
        "purpose": "Time window that makes groups and locations available for check-in or attendance.",
        "common_joins": ["Group", "AttendanceOccurrence"],
        "agent_notes": ["Schedule windows are a frequent reason eligible rooms do not appear."],
    },
    "Device": {
        "purpose": "Kiosk, printer, or device record that affects check-in availability and label routing.",
        "common_joins": ["Location"],
        "agent_notes": ["Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant."],
    },
    "LearningProgram": {
        "purpose": "Top-level LMS program container for courses, classes, semesters, requirements, and learner progress.",
        "common_joins": ["LearningCourse", "LearningClass", "LearningProgramCompletion"],
        "agent_notes": ["Verify active course/class structure and completion semantics before treating LMS completion as ministry qualification."],
    },
    "LearningCourse": {
        "purpose": "Course definition used to organize classes, activities, requirements, and completion reporting.",
        "common_joins": ["LearningProgram", "LearningClass", "LearningCourseRequirement"],
        "agent_notes": ["Confirm whether a question is about the course definition, a class instance, or a person's completion state."],
    },
    "LearningClass": {
        "purpose": "Scheduled or on-demand class instance where learners complete activities inside a course.",
        "common_joins": ["LearningCourse", "LearningClassActivity", "LearningClassActivityCompletion", "LearningParticipant"],
        "agent_notes": ["Inspect class status, semester, participants, activities, and workflow side effects when troubleshooting completion."],
    },
    "LearningClassActivity": {
        "purpose": "Unit of LMS work, assessment, or content that can drive completion and follow-up automation.",
        "common_joins": ["LearningClass", "LearningClassActivityCompletion"],
        "agent_notes": ["Check activity configuration and completion rules before assuming a learner failed to finish the course."],
    },
    "LearningClassActivityCompletion": {
        "purpose": "Person-specific activity completion signal used by LMS reporting, workflow triggers, and downstream engagement steps.",
        "common_joins": ["LearningClassActivity", "LearningClass", "Person"],
        "agent_notes": ["Use this to diagnose missing activity completion before escalating to program or step logic."],
    },
    "LearningProgramCompletion": {
        "purpose": "Program-level completion signal for learners after course/class requirements are satisfied.",
        "common_joins": ["LearningProgram", "Person", "LearningClassActivityCompletion"],
        "agent_notes": ["Confirm which activity and course completions roll up to the program before reporting someone as complete."],
    },
    "StepProgram": {
        "purpose": "Engagement journey container that can represent milestones, achievements, or discipleship paths.",
        "common_joins": ["StepType", "Step", "Person"],
        "agent_notes": ["Do not equate a training completion with a Step unless the workflow or data view explicitly writes it."],
    },
    "StepType": {
        "purpose": "Specific milestone or badge-like step definition within a Step Program.",
        "common_joins": ["StepProgram", "Step"],
        "agent_notes": ["Check prerequisites, filters, workflows, and achievement behavior when a badge or step is missing."],
    },
    "Step": {
        "purpose": "Person-specific engagement milestone instance.",
        "common_joins": ["StepType", "StepProgram", "Person"],
        "agent_notes": ["Verify the Step row exists before troubleshooting badge display or engagement reporting."],
    },
    "GroupMemberRequirement": {
        "purpose": "Serving or membership qualification gate that can depend on training, background checks, documents, or manual review.",
        "common_joins": ["GroupMember", "Person", "Group"],
        "agent_notes": ["Keep LMS completion separate from serving eligibility unless a requirement explicitly connects them."],
    },
}

AUTHORITY_BY_SOURCE_ID = {
    "triumph_resources": "official-triumph",
    "rock_documentation": "official",
    "rock_core_release_notes": "official-release",
    "rock_mobile_release_notes": "official-release",
    "rock_developer": "official-developer",
    "rock_mobile_docs": "official-developer",
    "rock_model_map": "official-model-map",
    "rock_api_docs": "official-api",
    "rock_lava_docs": "official-developer",
    "rock_rocku": "official-training",
    "sparkdevnetwork_rock": "source-code",
    "sparkdevnetwork_slingshot": "source-code",
    "oneall_rock_sql_library": "community-code",
    "public_rock_repos": "community-code",
    "rock_recipes": "community-example",
    "rock_qa": "community-answer",
    "rock_community_site": "community-reference",
    "rock_community_hubs": "community-reference",
    "org_contribution": "org-contribution",
}

SOURCE_PRIORITY = {
    "official-triumph": 105,
    "official": 100,
    "official-release": 95,
    "official-developer": 90,
    "official-api": 88,
    "official-model-map": 86,
    "source-code": 84,
    "official-training": 75,
    "community-code": 62,
    "org-contribution": 58,
    "community-example": 55,
    "community-answer": 50,
    "community-reference": 45,
}

CHECK_IN_TASK_CARDS = [
    {
        "id": "diagnose-labels-not-printing",
        "title": "Diagnose Labels Not Printing",
        "goal": "Find whether the failure is configuration, device routing, printer hardware, label definition, mobile/cloud print, or version-specific behavior.",
        "guide_sections": [
            "Kiosks, Devices, Printers, And Physical Operations",
            "Labels, Security Codes, Pickup, And Label Data",
            "Troubleshooting Decision Tree",
        ],
        "live_records": ["Device", "Location", "Check-in Configuration", "Label", "Attendance"],
        "entities": ["Device", "Location", "Attendance", "AttendanceOccurrence"],
        "source_keywords": ["printer", "label", "Next-Gen", "DPI", "Windows Check-In Application"],
        "steps": [
            "Identify whether the flow is legacy, Next-Gen, mobile, or Windows Check-In Application.",
            "Inspect whether labels route to the device printer, location printer, or cloud/mobile print route.",
            "Verify the device, named location, physical printer, DPI, label dimensions, and label stock.",
            "Run a test check-in and confirm whether an Attendance row is created before debugging the printer.",
            "Check release caveats for shared printers, mobile self-check-in printing, DPI, and Windows app cut settings.",
        ],
        "do_not_assume": [
            "Do not assume the label template is broken before confirming printer routing.",
            "Do not assume mobile check-in prints to the phone.",
        ],
    },
    {
        "id": "diagnose-person-not-eligible",
        "title": "Diagnose Person Found But No Eligible Rooms",
        "goal": "Trace eligibility from person/family search through configuration, group type, group, location, schedule, campus, capacity, and version caveats.",
        "guide_sections": [
            "People, Families, Search, And Eligibility",
            "Group Types, Groups, Locations, Campuses, And Schedules",
            "Troubleshooting Decision Tree",
        ],
        "live_records": ["Person", "Family Group", "GroupType", "Group", "Location", "Schedule", "Campus"],
        "entities": ["Person", "Group", "GroupType", "Location", "Schedule", "AttendanceOccurrence"],
        "source_keywords": ["eligibility", "age", "grade", "capacity", "inactive groups", "schedule"],
        "steps": [
            "Confirm the person is searchable in the current check-in configuration and family context.",
            "Inspect age, grade, status, campus, family relationship, and can-check-in relationship assumptions.",
            "Verify the target group type takes attendance and its check-in behavior matches the desired model.",
            "Verify active group, active location, linked schedule, check-in window, campus, and capacity.",
            "Check release notes for known age/grade, inactive group, schedule exclusion, and capacity fixes.",
        ],
        "do_not_assume": [
            "Do not assume a missing room means the group is missing.",
            "Do not ignore schedule windows and kiosk/device location filters.",
        ],
    },
    {
        "id": "add-new-room",
        "title": "Add A New Check-In Room",
        "goal": "Add a room without breaking eligibility, labels, printer routing, capacity, or reporting.",
        "guide_sections": [
            "Core Configuration Model",
            "Group Types, Groups, Locations, Campuses, And Schedules",
            "Implementation Playbooks",
        ],
        "live_records": ["Group", "Location", "Schedule", "Device", "Label"],
        "entities": ["Group", "Location", "Schedule", "AttendanceOccurrence"],
        "source_keywords": ["group locations", "schedules", "locations", "printer", "capacity"],
        "steps": [
            "Create or verify the named location and campus.",
            "Create or update the group under the correct group type and area.",
            "Attach the location and schedule expected for check-in.",
            "Set capacity and printer behavior if used.",
            "Run a test check-in and inspect the AttendanceOccurrence group, location, and schedule.",
        ],
        "do_not_assume": [
            "Do not add a room only in the UI; verify the data written after a test check-in.",
        ],
    },
    {
        "id": "audit-mobile-check-in",
        "title": "Audit Mobile Check-In",
        "goal": "Confirm mobile check-in uses the intended configuration template, kiosk, areas, authentication, and print route.",
        "guide_sections": ["Mobile Check-In And Mobile Attendance", "Version And Release Caveats"],
        "live_records": ["Mobile Page", "Mobile Block", "Check-in Configuration", "Device/Kiosk", "Printer"],
        "entities": ["Attendance", "AttendanceOccurrence", "Device"],
        "source_keywords": ["mobile check-in", "Mobile CheckIn block", "proximity attendance", "mobile release"],
        "steps": [
            "Verify Rock server version and Rock Mobile version.",
            "Inspect mobile block settings for configuration template, kiosk, primary areas, and secondary areas.",
            "Confirm the logged-in family/person context and shell route.",
            "Test label routing to the venue printer or cloud print path.",
            "Check mobile release notes for family-mode, page-parameter, proximity, and label printing fixes.",
        ],
        "do_not_assume": [
            "Do not treat mobile check-in as anonymous QR attendance.",
            "Do not assume mobile uses different attendance tables.",
        ],
    },
    {
        "id": "build-attendance-report",
        "title": "Build Or Debug Attendance Reporting",
        "goal": "Use the attendance data model correctly so reports match check-in behavior.",
        "guide_sections": ["Attendance Data Model, Analytics, And Reporting", "Agent Task Recipes"],
        "live_records": ["Attendance", "AttendanceOccurrence", "Group", "Schedule", "Location", "Campus"],
        "entities": ["Attendance", "AttendanceOccurrence", "PersonAlias", "Group", "Schedule", "Location", "Campus"],
        "source_keywords": ["AttendanceOccurrence", "SundayDate", "DidAttend", "spCheckin"],
        "steps": [
            "Join Attendance through AttendanceOccurrence before interpreting group, schedule, location, or date.",
            "Filter on DidAttend when the report should count actual attendance.",
            "Decide whether the report counts rows, people, dates, families, occurrences, or groups.",
            "Use SundayDate carefully for weekly reporting.",
            "Compare results against Attendance Analytics before shipping a custom report.",
        ],
        "do_not_assume": [
            "Do not report from group membership alone.",
            "Do not ignore duplicate attendance across schedules or services.",
        ],
    },
]

LEARNING_LMS_TASK_CARDS = [
    {
        "id": "recipe-audit-one-lms-program",
        "title": "Recipe: Audit One LMS Program",
        "goal": "Trace a program from source content through courses, classes, activities, completion, communications, and reporting.",
        "guide_sections": [
            "Core Configuration And Data Model",
            "Courses And Lessons Deep Dive",
            "Agent Task Recipes",
        ],
        "live_records": [
            "Learning Program",
            "Learning Course",
            "Learning Class",
            "Learning Class Activity",
            "Learning Class Activity Completion",
            "System Communication",
        ],
        "entities": [
            "LearningProgram",
            "LearningCourse",
            "LearningClass",
            "LearningClassActivity",
            "LearningClassActivityCompletion",
            "Person",
        ],
        "source_keywords": ["Learning Program", "Learning Course", "Learning Class", "Learning Management System", "LMS"],
        "steps": [
            "Identify the program, course, class, semester, and activity records involved.",
            "Confirm whether the program is scheduled, self-paced, or hybrid before interpreting completion.",
            "Inspect activity completion rows and program/course rollup behavior.",
            "Review communications, workflows, and reporting dependencies tied to the program.",
            "Cite the exact source and live record boundary before recommending changes.",
        ],
        "do_not_assume": [
            "Do not assume a course definition proves a specific learner completed the work.",
            "Do not treat a training program as a serving eligibility gate without the requirement record.",
        ],
    },
    {
        "id": "recipe-find-why-a-person-is-not-complete",
        "title": "Recipe: Find Why A Person Is Not Complete",
        "goal": "Determine whether the missing completion is caused by enrollment, activity completion, program rollup, workflow timing, or reporting filters.",
        "guide_sections": [
            "Requirements And Completion Deep Dive",
            "Troubleshooting Decision Tree",
            "Agent Task Recipes",
        ],
        "live_records": [
            "Person",
            "Learning Class",
            "Learning Class Activity",
            "Learning Class Activity Completion",
            "Learning Program Completion",
            "Learning Course Requirement",
            "Workflow",
        ],
        "entities": [
            "Person",
            "LearningClass",
            "LearningClassActivity",
            "LearningClassActivityCompletion",
            "LearningProgramCompletion",
            "LearningCourseRequirement",
            "Workflow",
        ],
        "source_keywords": ["completion", "Learning Class Activity Completion", "Course Requirement", "Has Completed Course"],
        "steps": [
            "Confirm the person is the intended learner and is attached to the expected class or program.",
            "Inspect required activities and their completion records before checking program rollups.",
            "Check whether course requirements or workflows are waiting on another Rock entity.",
            "Compare the live completion rows with the report or data view that raised the issue.",
            "Separate LMS completion from serving approval or group requirement state.",
        ],
        "do_not_assume": [
            "Do not infer completion from attendance, registration, or group membership alone.",
            "Do not mark a person complete until the required activity and rollup records agree.",
        ],
    },
    {
        "id": "recipe-prepare-a-course-for-launch",
        "title": "Recipe: Prepare A Course For Launch",
        "goal": "Prepare a course or class for learners by checking structure, activities, schedules, access, communications, and reporting.",
        "guide_sections": [
            "Common Learning LMS And Engagement Workflows",
            "Courses And Lessons Deep Dive",
            "Implementation Playbooks",
        ],
        "live_records": [
            "Learning Program",
            "Learning Course",
            "Learning Class",
            "Learning Semester",
            "Learning Class Activity",
            "Learning Participant",
            "System Communication",
        ],
        "entities": [
            "LearningProgram",
            "LearningCourse",
            "LearningClass",
            "LearningSemester",
            "LearningClassActivity",
            "LearningParticipant",
        ],
        "source_keywords": ["course", "class", "activity", "semester", "lesson", "Learning Plan"],
        "steps": [
            "Confirm the course belongs to the intended program and has the expected class structure.",
            "Review activities, lesson order, due dates, prerequisites, and learner-facing content.",
            "Verify participant access, campus or semester scope, and communication triggers.",
            "Check reporting and completion behavior before inviting learners.",
            "Run a small test learner through the course and inspect the resulting rows.",
        ],
        "do_not_assume": [
            "Do not launch from content review alone; verify the data model and learner path.",
            "Do not ignore version-specific LMS release caveats.",
        ],
    },
    {
        "id": "recipe-build-a-step-journey-from-training",
        "title": "Recipe: Build A Step Journey From Training",
        "goal": "Connect training completion to an engagement journey only through explicit workflows, data views, or step-writing logic.",
        "guide_sections": [
            "Engagement Journeys Deep Dive",
            "Related Rock Areas",
            "Agent Task Recipes",
        ],
        "live_records": [
            "Learning Class Activity Completion",
            "Learning Program Completion",
            "Step Program",
            "Step Type",
            "Step",
            "Data View",
            "Workflow",
        ],
        "entities": [
            "LearningClassActivityCompletion",
            "LearningProgramCompletion",
            "StepProgram",
            "StepType",
            "Step",
            "DataView",
            "Workflow",
        ],
        "source_keywords": ["Step Program", "Step Type", "Step Workflow", "badge", "engagement", "completion"],
        "steps": [
            "Define which completion event should create or update the engagement step.",
            "Inspect the Step Program and Step Type before configuring workflow or data view logic.",
            "Verify prerequisites, badge or achievement display behavior, and reporting scope.",
            "Test with a known learner and confirm both completion and Step records exist.",
            "Document the boundary between training history and engagement journey state.",
        ],
        "do_not_assume": [
            "Do not assume a completed training automatically creates a Step.",
            "Do not troubleshoot badge display until the Step row and Step Type are verified.",
        ],
    },
    {
        "id": "recipe-review-upgrade-risk",
        "title": "Recipe: Review Upgrade Risk",
        "goal": "Review LMS, engagement, requirement, workflow, and communication behavior against current release notes and source-code caveats.",
        "guide_sections": [
            "Administration And Operational Guardrails",
            "Version And Release Caveats",
            "Agent Task Recipes",
        ],
        "live_records": [
            "Rock Version",
            "Learning Course",
            "Learning Class Activity Completion",
            "Step Program",
            "Group Member Requirement",
            "Workflow",
            "System Communication",
        ],
        "entities": [
            "LearningCourse",
            "LearningClassActivityCompletion",
            "StepProgram",
            "GroupMemberRequirement",
            "Workflow",
        ],
        "source_keywords": ["release notes", "Learning", "LMS", "Step", "GroupMemberRequirement", "workflow"],
        "steps": [
            "Identify the current and target Rock versions.",
            "Review release notes for LMS, Step, requirement, workflow, and communication changes.",
            "Spot-check source-code landmarks for renamed or changed model behavior.",
            "List affected programs, classes, Step Programs, and requirement gates before upgrading.",
            "Validate a representative learner path after the upgrade.",
        ],
        "do_not_assume": [
            "Do not rely on old task-card behavior after an LMS or Step-related release.",
            "Do not merge upgrade guidance until release-note and live-record checks agree.",
        ],
    },
]

def repo_relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)

def relative_path(path: Path) -> str:
    try:
        return path.relative_to(KNOWLEDGE_DIR.parents[0]).as_posix()
    except ValueError:
        return str(path)

def check(check_id: str, passed: bool, message: str) -> dict[str, Any]:
    return {"id": check_id, "passed": bool(passed), "message": message}

def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"

def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))

def count_jsonl(path: Path) -> int:
    return sum(1 for _ in read_jsonl(path)) if path.exists() else 0

def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")

def compact_unique(values: Iterable[Any]) -> list[Any]:
    seen = set()
    output = []
    for value in values:
        if value in (None, "", [], {}):
            continue
        key = json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
        if key not in seen:
            seen.add(key)
            output.append(value)
    return output

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp_path.replace(path)

def upsert_jsonl(path: Path, rows: list[dict[str, Any]], key: str, value: str) -> None:
    existing = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get(key) != value:
                existing.append(row)
    existing.extend(rows)
    write_jsonl(path, existing)
