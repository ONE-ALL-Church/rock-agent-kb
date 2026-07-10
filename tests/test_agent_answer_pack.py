import json

import rock_kb.agent_answer_pack as answer_module
from rock_kb.agent_answer_pack import build_agent_answer_pack
from rock_kb.concepts import Concept
from rock_kb.jsonl import read_jsonl


def test_first_check_ranking_prefers_introductory_official_source_when_priorities_tie():
    concept = Concept(
        id="engagement-tracking",
        title="Engagement Tracking",
        description="Engagement behavior.",
        keywords=["engagement", "streak"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    intro = {
        "claim_id": "claim:intro",
        "claim": "A streak type defines the engagement source and time pattern used for tracking.",
        "claim_type": "behavior",
        "operational_priority": 100,
        "primary_concept_id": concept.id,
        "source_refs": [{"title": "Intro to Streak Types", "url": "https://example.com/intro"}],
    }
    specialized = {
        "claim_id": "claim:specialized",
        "claim": "A specialized streak map operation rebuilds one internal map.",
        "claim_type": "configuration",
        "operational_priority": 100,
        "primary_concept_id": concept.id,
        "source_refs": [{"title": "Rebuild Streak Type", "url": "https://example.com/rebuild"}],
    }

    ranked = sorted([specialized, intro], key=lambda row: answer_module.first_check_claim_sort_key(concept, row))

    assert ranked[0]["claim_id"] == "claim:intro"


def test_first_check_selection_reserves_distinct_documentation_branches():
    rows = [
        {"claim_id": claim_id, "source_refs": [{"url": url}]}
        for claim_id, url in [
            ("claim:step-one", "https://community.rockrms.com/documentation/engagement/steps/intro"),
            ("claim:step-two", "https://community.rockrms.com/documentation/engagement/steps/configure"),
            ("claim:streak", "https://community.rockrms.com/documentation/engagement/streaks/intro"),
            ("claim:assessment", "https://community.rockrms.com/documentation/engagement/assessments/intro"),
            (
                "claim:achievement",
                "https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro",
            ),
        ]
    ]

    selected = answer_module.diverse_claim_selection(rows, 4)

    assert [row["claim_id"] for row in selected] == [
        "claim:step-one",
        "claim:streak",
        "claim:assessment",
        "claim:achievement",
    ]
    assert answer_module.claim_source_branch_key(
        {
            "source_refs": [
                {"url": "https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro"}
            ]
        }
    ) == "documentation/supporting-rock/hosting/azure-hosting"
    assert answer_module.claim_source_branch_key(
        {
            "source_refs": [
                {"url": "https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro"}
            ]
        }
    ) == "documentation/supporting-rock/hosting/internal-hosting"


def test_first_check_selection_keeps_existing_order_for_other_concepts():
    concept = Concept(
        id="workflows",
        title="Workflows",
        description="Workflow automation.",
        keywords=["workflow"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    rows = [
        {"claim_id": "claim:lower", "operational_priority": 80},
        {"claim_id": "claim:higher", "operational_priority": 90},
    ]

    selected = answer_module.first_check_claims_for_concept(concept, rows, 2)

    assert [row["claim_id"] for row in selected] == ["claim:higher", "claim:lower"]


def test_build_agent_answer_pack_writes_answers_checklists_review_and_conflicts(monkeypatch, tmp_path):
    agent_dir = tmp_path / "agent"
    knowledge_dir = tmp_path / "knowledge"
    monkeypatch.setattr(answer_module, "AGENT_DIR", agent_dir)
    monkeypatch.setattr(answer_module, "KNOWLEDGE_DIR", knowledge_dir)
    monkeypatch.setattr(answer_module, "ANSWER_PACK_PATH", agent_dir / "answer-pack.jsonl")
    monkeypatch.setattr(answer_module, "LIVE_CHECKLISTS_PATH", agent_dir / "live-inspection-checklists.jsonl")
    monkeypatch.setattr(answer_module, "LIVE_PROBE_RECIPES_PATH", agent_dir / "live-probe-recipes.jsonl")
    monkeypatch.setattr(answer_module, "CLAIM_REVIEW_QUEUE_PATH", agent_dir / "claim-review-queue.jsonl")
    monkeypatch.setattr(answer_module, "SOURCE_CONFLICTS_PATH", agent_dir / "source-conflicts.jsonl")
    monkeypatch.setattr(answer_module, "DISTILLED_CLAIMS_PATH", agent_dir / "distilled-claims.jsonl")
    monkeypatch.setattr(answer_module, "DISTILLED_CLAIM_REVIEWS_PATH", tmp_path / "distilled-claim-reviews.jsonl")
    monkeypatch.setattr(answer_module, "AUTHORITY_RULES_PATH", agent_dir / "source-authority-rules.jsonl")
    monkeypatch.setattr(answer_module, "EVALUATION_SET_PATH", agent_dir / "evaluation-set.jsonl")
    monkeypatch.setattr(answer_module, "EVALUATION_RESULTS_PATH", agent_dir / "evaluation-results.jsonl")
    monkeypatch.setattr(answer_module, "EVALUATION_REPORT_PATH", agent_dir / "evaluation-report.json")
    monkeypatch.setattr(answer_module, "REVIEW_DASHBOARD_PATH", agent_dir / "claim-review-dashboard.md")

    concept = Concept(
        id="workflows",
        title="Workflows",
        description="Workflow automation.",
        keywords=["workflow"],
        source_weights={},
        depends_on_topics=["workflows", "security"],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    monkeypatch.setattr(answer_module, "load_answer_concepts", lambda: [concept])
    monkeypatch.setattr(
        answer_module,
        "approved_claim_rows",
        lambda: [
            {
                "claim_id": "claim:rocku",
                "claim": "Verify workflow launch configuration and permissions before production use.",
                "claim_type": "configuration",
                "concept_ids": ["workflows"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 95,
                "answer_candidate": True,
                "requires_live_instance": True,
                "common_failure_mode": ["workflow", "permission"],
                "source_refs": [{"source_id": "rock_rocku", "title": "Workflow Training", "url": "https://example.com/rocku"}],
            },
            {
                "claim_id": "claim:tagged-adjacent",
                "claim": "Inspect opportunity filters, status, campus, connector assignment, and security before changing the request.",
                "claim_type": "implementation_pattern",
                "concept_ids": ["workflows"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 99,
                "answer_candidate": True,
                "requires_live_instance": True,
                "common_failure_mode": ["permission"],
                "source_refs": [{"source_id": "rock_rocku", "title": "Connections Board", "url": "https://example.com/connections"}],
            },
            {
                "claim_id": "claim:community",
                "claim": "A community pattern may help explain a custom workflow launch.",
                "claim_type": "configuration",
                "concept_ids": ["workflows"],
                "authority_tier": "community-reviewed",
                "operational_priority": 72,
                "answer_candidate": True,
                "requires_live_instance": True,
                "common_failure_mode": ["workflow"],
                "source_refs": [{"source_id": "rock_community_hubs", "title": "Community", "url": "https://example.com/community"}],
            },
            {
                "claim_id": "claim:workflow-form",
                "claim": "Workflow form fields should be reviewed with downstream actions, launch configuration, and permissions before production use.",
                "claim_type": "configuration",
                "concept_ids": ["workflows"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 94,
                "answer_candidate": True,
                "requires_live_instance": True,
                "common_failure_mode": ["workflow", "permission"],
                "primary_concept_id": "workflows",
                "secondary_concept_ids": [],
                "source_refs": [
                    {
                        "source_id": "rock_rocku",
                        "title": "Form Builder",
                        "url": "https://example.com/rocku/workflows/form-builder",
                        "source_timestamp_url": "https://example.com/rocku/workflows/form-builder?t=83",
                        "timestamp": "01:23",
                        "timestamp_seconds": 83,
                    },
                    {
                        "source_id": "rock_rocku",
                        "title": "Form Builder",
                        "url": "https://example.com/rocku/workflows/form-builder",
                    },
                ],
            },
            {
                "claim_id": "claim:generic",
                "claim": "The lesson provides training context and helps route agents, not as a substitute for official documentation.",
                "claim_type": "risk",
                "concept_ids": ["workflows"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 100,
                "answer_candidate": False,
                "requires_live_instance": True,
                "common_failure_mode": ["permission"],
                "source_refs": [{"source_id": "rock_rocku", "title": "Generic", "url": "https://example.com/generic"}],
            },
        ],
    )

    counts = build_agent_answer_pack()
    answers = list(read_jsonl(agent_dir / "answer-pack.jsonl"))
    checklists = list(read_jsonl(agent_dir / "live-inspection-checklists.jsonl"))
    probe_recipes = list(read_jsonl(agent_dir / "live-probe-recipes.jsonl"))
    review_rows = list(read_jsonl(agent_dir / "claim-review-queue.jsonl"))
    conflicts = list(read_jsonl(agent_dir / "source-conflicts.jsonl"))
    distilled = list(read_jsonl(agent_dir / "distilled-claims.jsonl"))
    authority_rules = list(read_jsonl(agent_dir / "source-authority-rules.jsonl"))
    eval_set = list(read_jsonl(agent_dir / "evaluation-set.jsonl"))
    eval_results = list(read_jsonl(agent_dir / "evaluation-results.jsonl"))

    assert counts["answer_pack"] == 3
    assert counts["live_probe_recipes"] == 4
    assert counts["evaluation_set"] == 4
    assert counts["evaluation_results"] == 4
    assert counts["source_authority_rules"] == 1
    assert answers[0]["top_claim_ids"]
    assert answers[0]["top_claim_ids"][0] == "claim:workflow-form"
    assert answers[0]["answer_status"] == "reviewer_authored_override"
    assert "WorkflowType" in answers[0]["answer"]
    assert answers[0]["top_distilled_claim_ids"] == []
    assert answers[0]["citations"][0]["source_timestamp_url"] == "https://example.com/rocku/workflows/form-builder?t=83"
    assert answers[0]["citations"][0]["timestamp"] == "01:23"
    assert "claim:generic" not in answers[0]["top_claim_ids"]
    assert checklists[0]["inspection_targets"]
    assert checklists[0]["probes"]
    assert probe_recipes
    assert all(row["schema"] == "rock-kb-live-probe-recipe-v1" for row in probe_recipes)
    assert any(row["required_parameters"] == ["workflow_type_id"] for row in probe_recipes)
    assert any("WorkflowActionType" in row["expected_tables"] for row in probe_recipes)
    assert all("SELECT" in row["read_only_sql"] or row["manual_check"] for row in probe_recipes)
    assert any("WorkflowType" in (probe.get("sql") or "") for probe in checklists[0]["probes"])
    probe_sql = "\n".join(str(probe.get("sql") or "") for probe in checklists[0]["probes"])
    assert "ActionTypeName" not in probe_sql
    assert "EntityType" in probe_sql
    assert "RockMigration" not in probe_sql
    rocku_review = next(row for row in review_rows if row["claim_id"] == "claim:rocku")
    assert rocku_review["recommended_action"] == "verify_live_before_operational_answer"
    assert all(row["claim_id"] != "claim:generic" for row in review_rows)
    assert conflicts
    assert distilled
    assert authority_rules[0]["preferred_sources"]
    assert len(eval_set) == 4
    assert all(row["status"] == "pass" for row in eval_results)
    assert (knowledge_dir / "concepts" / "workflows" / "answers" / "first-checks.md").exists()
    assert (knowledge_dir / "concepts" / "workflows" / "live-inspection-checklist.md").exists()
    assert (knowledge_dir / "concepts" / "workflows" / "live-probe-recipes.md").exists()
    assert (agent_dir / "claim-review-dashboard.md").exists()
    assert (agent_dir / "evaluation-report.json").exists()
    report = json.loads((agent_dir / "answer-pack-report.json").read_text(encoding="utf-8"))
    assert report["answer_count"] == 3
    assert report["reviewer_override_count"] == 1
    rendered_answer = (knowledge_dir / "concepts" / "workflows" / "answers" / "first-checks.md").read_text(encoding="utf-8")
    assert "[Form Builder](https://example.com/rocku/workflows/form-builder?t=83) (`01:23`)" in rendered_answer
    assert rendered_answer.count("[Form Builder]") == 1
    rendered_recipes = (knowledge_dir / "concepts" / "workflows" / "live-probe-recipes.md").read_text(encoding="utf-8")
    assert "WorkflowActionType" in rendered_recipes
    assert "Bind `<workflow_type_id>`" in rendered_recipes


def test_claim_review_queue_excludes_answer_pack_usable_and_singleton_routing_claims():
    rows = answer_module.claim_review_queue_rows(
        [
            {
                "claim_id": "claim:usable",
                "claim": "Use this in answers.",
                "claim_type": "configuration",
                "concept_ids": ["workflows"],
                "claim_tier": "live_verified",
                "authority_tier": "live-verified",
                "answer_candidate": True,
                "source_refs": [{"source_id": "rock_docs", "url": "https://example.com/docs"}],
            },
            {
                "claim_id": "claim:routing",
                "claim": "Use this only for source routing, even if the extractor marked it as a candidate.",
                "claim_type": "risk",
                "concept_ids": ["workflows"],
                "claim_tier": "routing_context_only",
                "authority_tier": "community-reviewed",
                "answer_candidate": True,
                "source_refs": [{"source_id": "rock_rocku", "url": "https://example.com/rocku"}],
            },
        ]
    )

    assert rows == []


def test_groups_first_checks_uses_reviewer_authored_override():
    concept = Concept(
        id="groups",
        title="Groups",
        description="Group operations.",
        keywords=["group"],
        source_weights={},
        depends_on_topics=["groups", "security"],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    rows = answer_module.answer_rows_for_concept(
        concept,
        [
            {
                "claim_id": "claim:group",
                "claim": "A group finder issue may depend on group type, status, schedule, and security.",
                "claim_type": "configuration",
                "concept_ids": ["groups"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 80,
                "answer_candidate": True,
                "requires_live_instance": True,
                "source_refs": [{"source_id": "rock_rocku", "title": "Groups", "url": "https://example.com/groups"}],
            }
        ],
        [
            {
                "id": "distilled-claim:unapproved",
                "concept_id": "groups",
                "distilled_claim": "Unapproved generated cluster text should not appear in answer prose.",
                "operational_priority": 100,
                "distillation_status": "generated_needs_reviewer_approval",
            }
        ],
    )

    first = rows[0]
    assert first["answer_status"] == "reviewer_authored_override"
    assert "GroupType" in first["answer"]
    assert "Unapproved generated cluster text" not in first["answer"]
    assert first["top_distilled_claim_ids"] == []


def test_distilled_claim_reviews_promote_only_approved_rows(tmp_path, monkeypatch):
    review_path = tmp_path / "distilled-claim-reviews.jsonl"
    review_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "schema": "rock-kb-distilled-claim-review-v1",
                        "distilled_claim_id": "distilled-claim:approved",
                        "review_status": "approved_for_answer_pack",
                        "reviewed_claim": "Reviewed operational guidance should appear in answers.",
                        "reviewer": "test-reviewer",
                        "reviewed_at": "2026-06-08T00:00:00+00:00",
                    }
                ),
                json.dumps(
                    {
                        "schema": "rock-kb-distilled-claim-review-v1",
                        "distilled_claim_id": "distilled-claim:rejected",
                        "review_status": "rejected_for_answer_pack",
                        "reviewer": "test-reviewer",
                        "reviewed_at": "2026-06-08T00:00:00+00:00",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(answer_module, "DISTILLED_CLAIM_REVIEWS_PATH", review_path)
    rows = answer_module.apply_distilled_claim_reviews(
        [
                {
                    "id": "distilled-claim:approved",
                    "concept_id": "test-concept",
                    "distilled_claim": "Generated text",
                    "operational_priority": 80,
                    "distillation_status": "generated_needs_reviewer_approval",
                },
                {
                    "id": "distilled-claim:rejected",
                    "concept_id": "test-concept",
                    "distilled_claim": "Rejected text should not appear.",
                    "operational_priority": 90,
                    "distillation_status": "generated_needs_reviewer_approval",
            },
        ]
    )

    concept = Concept(
        id="test-concept",
        title="Test Concept",
        description="Workflow automation.",
        keywords=[],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    answers = answer_module.answer_rows_for_concept(concept, [], rows)

    first = answers[0]
    assert first["top_distilled_claim_ids"] == ["distilled-claim:approved"]
    assert "Reviewed operational guidance should appear in answers" in first["answer"]
    assert "Rejected text should not appear" not in first["answer"]


def test_distilled_claim_review_supplements_override_base_reviews(tmp_path, monkeypatch):
    review_path = tmp_path / "distilled-claim-reviews.jsonl"
    review_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-distilled-claim-review-v1",
                "distilled_claim_id": "distilled-claim:changed",
                "review_status": "approved_for_answer_pack",
                "reviewed_claim": "Earlier approved text.",
                "reviewer": "test-reviewer",
                "reviewed_at": "2026-06-08T00:00:00+00:00",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "distilled-claim-reviews-2026-06-10.jsonl").write_text(
        json.dumps(
            {
                "schema": "rock-kb-distilled-claim-review-v1",
                "distilled_claim_id": "distilled-claim:changed",
                "review_status": "rejected_for_answer_pack",
                "review_notes": ["Later review found this too source-light for answer prose."],
                "reviewer": "codex-review",
                "reviewed_at": "2026-06-10T00:00:00-07:00",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(answer_module, "DISTILLED_CLAIM_REVIEWS_PATH", review_path)

    reviews = answer_module.load_distilled_claim_reviews()

    assert reviews["distilled-claim:changed"]["review_status"] == "rejected_for_answer_pack"
    assert reviews["distilled-claim:changed"]["reviewer"] == "codex-review"


def test_preserve_stable_distilled_claim_created_at_when_source_input_matches():
    row = {
        "id": "distilled-claim:stable",
        "concept_id": "workflows",
        "claim_type": "configuration",
        "distilled_claim": "Generated workflow claim.",
        "supporting_claim_ids": ["claim:a", "claim:b"],
        "supporting_claim_count": 2,
        "authority_tiers": ["rocku-confirmed"],
        "source_refs": [{"source_id": "rock_rocku", "url": "https://example.com"}],
        "operational_priority": 90,
        "recommended_promotion": "review_cluster_before_promotion",
        "source_input_hash": "same-input",
        "created_at": "2026-06-10T22:00:00+00:00",
    }
    existing = [{**row, "created_at": "2026-06-08T00:00:00+00:00"}]

    stabilized = answer_module.preserve_stable_distilled_claim_metadata([row], existing)

    assert stabilized[0]["created_at"] == "2026-06-08T00:00:00+00:00"


def test_preserve_stable_distilled_claim_keeps_new_timestamp_when_source_input_changes():
    row = {
        "id": "distilled-claim:changed",
        "concept_id": "workflows",
        "claim_type": "configuration",
        "distilled_claim": "Generated workflow claim.",
        "supporting_claim_ids": ["claim:a", "claim:b"],
        "supporting_claim_count": 2,
        "authority_tiers": ["rocku-confirmed"],
        "source_refs": [{"source_id": "rock_rocku", "url": "https://example.com"}],
        "operational_priority": 90,
        "recommended_promotion": "review_cluster_before_promotion",
        "source_input_hash": "new-input",
        "created_at": "2026-06-10T22:00:00+00:00",
    }
    existing = [{**row, "source_input_hash": "old-input", "created_at": "2026-06-08T00:00:00+00:00"}]

    stabilized = answer_module.preserve_stable_distilled_claim_metadata([row], existing)

    assert stabilized[0]["created_at"] == "2026-06-10T22:00:00+00:00"


def test_build_agent_answer_pack_preserves_distilled_claims_on_repeat_run(monkeypatch, tmp_path):
    agent_dir = tmp_path / "agent"
    knowledge_dir = tmp_path / "knowledge"
    monkeypatch.setattr(answer_module, "AGENT_DIR", agent_dir)
    monkeypatch.setattr(answer_module, "KNOWLEDGE_DIR", knowledge_dir)
    monkeypatch.setattr(answer_module, "ANSWER_PACK_PATH", agent_dir / "answer-pack.jsonl")
    monkeypatch.setattr(answer_module, "LIVE_CHECKLISTS_PATH", agent_dir / "live-inspection-checklists.jsonl")
    monkeypatch.setattr(answer_module, "LIVE_PROBE_RECIPES_PATH", agent_dir / "live-probe-recipes.jsonl")
    monkeypatch.setattr(answer_module, "CLAIM_REVIEW_QUEUE_PATH", agent_dir / "claim-review-queue.jsonl")
    monkeypatch.setattr(answer_module, "SOURCE_CONFLICTS_PATH", agent_dir / "source-conflicts.jsonl")
    monkeypatch.setattr(answer_module, "DISTILLED_CLAIMS_PATH", agent_dir / "distilled-claims.jsonl")
    monkeypatch.setattr(answer_module, "DISTILLED_CLAIM_REVIEWS_PATH", tmp_path / "distilled-claim-reviews.jsonl")
    monkeypatch.setattr(answer_module, "AUTHORITY_RULES_PATH", agent_dir / "source-authority-rules.jsonl")
    monkeypatch.setattr(answer_module, "EVALUATION_SET_PATH", agent_dir / "evaluation-set.jsonl")
    monkeypatch.setattr(answer_module, "EVALUATION_RESULTS_PATH", agent_dir / "evaluation-results.jsonl")
    monkeypatch.setattr(answer_module, "EVALUATION_REPORT_PATH", agent_dir / "evaluation-report.json")
    monkeypatch.setattr(answer_module, "REVIEW_DASHBOARD_PATH", agent_dir / "claim-review-dashboard.md")
    concept = Concept(
        id="test-concept",
        title="Test Concept",
        description="Test concept.",
        keywords=["workflow"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="",
        guide_status="",
        max_records=5,
        raw={},
    )
    monkeypatch.setattr(answer_module, "load_answer_concepts", lambda: [concept])
    monkeypatch.setattr(
        answer_module,
        "approved_claim_rows",
        lambda: [
            {
                "claim_id": "claim:a",
                "claim": "Workflow launch configuration should be verified before production use.",
                "claim_type": "configuration",
                "concept_ids": ["test-concept"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 90,
                "answer_candidate": True,
                "requires_live_instance": True,
                "source_refs": [{"source_id": "rock_rocku", "title": "A", "url": "https://example.com/a"}],
            },
            {
                "claim_id": "claim:b",
                "claim": "Workflow launch permissions should be verified before production use.",
                "claim_type": "configuration",
                "concept_ids": ["test-concept"],
                "authority_tier": "rocku-confirmed",
                "operational_priority": 80,
                "answer_candidate": True,
                "requires_live_instance": True,
                "source_refs": [{"source_id": "rock_rocku", "title": "B", "url": "https://example.com/b"}],
            },
        ],
    )
    timestamps = iter(["2026-06-10T22:00:00+00:00", "2026-06-10T23:00:00+00:00"])
    monkeypatch.setattr(answer_module, "now_iso", lambda: next(timestamps))

    build_agent_answer_pack()
    first = (agent_dir / "distilled-claims.jsonl").read_text(encoding="utf-8")
    build_agent_answer_pack()
    second = (agent_dir / "distilled-claims.jsonl").read_text(encoding="utf-8")

    assert first == second
    row = next(read_jsonl(agent_dir / "distilled-claims.jsonl"))
    assert row["source_input_hash"]
    assert row["created_at"] == "2026-06-10T22:00:00+00:00"


def test_live_probe_templates_match_verified_schema():
    serialized = json.dumps(answer_module.LIVE_INSPECTION_TEMPLATES, sort_keys=True)
    generic = json.dumps(answer_module.generic_live_probe_templates(Concept(
        id="groups",
        title="Groups",
        description="",
        keywords=[],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="",
        guide_status="",
        max_records=1,
        raw={},
    )), sort_keys=True)

    assert "ActionTypeName" not in serialized
    assert "ReportField WHERE ReportId = <report_id> ORDER BY [Order]" not in serialized
    assert "SELECT Id, Name, IsActive FROM GroupType" not in serialized
    assert "RockMigration" not in serialized
    assert "SELECT TOP 1 Version FROM RockMigration" not in generic
    assert "PageRoute" in serialized
    assert "PageRoute" in generic
    assert "__MigrationHistory" in generic


def test_live_probe_recipes_are_bound_and_read_only():
    concept = Concept(
        id="data-views-reports",
        title="Data Views And Reports",
        description="",
        keywords=[],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="",
        guide_status="",
        max_records=1,
        raw={},
    )
    checklist = answer_module.live_checklist_for_concept(concept, [])
    recipes = answer_module.live_probe_recipes_for_concept(concept, checklist)

    assert recipes
    assert any("data_view_id" in row["required_parameters"] for row in recipes)
    assert any("ReportField" in row["expected_tables"] for row in recipes)
    assert all("read-only SELECT" in " ".join(row["safety_rules"]) for row in recipes)
    assert all("Promote or answer" in row["promotion_rule"] for row in recipes)
