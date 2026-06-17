import json

import rock_kb.model_map as model_map
from rock_kb.jsonl import read_jsonl, write_jsonl


def test_build_model_map_writes_scraped_models_properties_and_category_pages(monkeypatch, tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    agent_dir = tmp_path / "agent"
    model_dir = knowledge_dir / "model-map"

    monkeypatch.setattr(model_map, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(model_map, "KNOWLEDGE_DIR", knowledge_dir)
    monkeypatch.setattr(model_map, "AGENT_DIR", agent_dir)
    monkeypatch.setattr(model_map, "MODEL_MAP_DIR", model_dir)
    monkeypatch.setattr(model_map, "MODEL_MAP_CONCEPT_DIR", model_dir / "concept-slices")
    monkeypatch.setattr(model_map, "MODEL_MAP_MODELS_DIR", model_dir / "models")
    monkeypatch.setattr(model_map, "MODEL_MAP_INDEX_PATH", model_dir / "index.md")
    monkeypatch.setattr(model_map, "MODEL_MAP_PUBLIC_MODELS_PATH", model_dir / "public-models.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_INSTANCE_SCHEMA_PATH", model_dir / "instance-schema.json")
    monkeypatch.setattr(model_map, "MODEL_MAP_CROSSWALK_PATH", model_dir / "entity-crosswalk.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_RELATIONSHIPS_PATH", model_dir / "relationships.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_REFLECTION_PROPERTIES_PATH", model_dir / "reflection-properties.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_STABLE_MODELS_PATH", model_dir / "stable-models.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_LATEST_MODELS_PATH", model_dir / "latest-models.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_STABLE_PROPERTIES_PATH", model_dir / "stable-properties.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_LATEST_PROPERTIES_PATH", model_dir / "latest-properties.jsonl")
    monkeypatch.setattr(model_map, "MODEL_MAP_PUBLIC_VERSION_DIFF_PATH", model_dir / "version-diff.json")
    monkeypatch.setattr(model_map, "MODEL_MAP_PUBLIC_VERSION_DIFF_JSONL_PATH", model_dir / "version-diff.jsonl")
    monkeypatch.setattr(model_map, "AGENT_MODEL_MAP_SUMMARY_PATH", agent_dir / "model-map-summary.json")
    monkeypatch.setattr(model_map, "AGENT_MODEL_MAP_ENTITIES_PATH", agent_dir / "model-map-entities.jsonl")
    monkeypatch.setattr(model_map, "AGENT_MODEL_MAP_RELATIONSHIPS_PATH", agent_dir / "model-map-relationships.jsonl")
    monkeypatch.setattr(model_map, "AGENT_MODEL_MAP_REFLECTION_PATH", agent_dir / "model-map-reflection-properties.jsonl")
    monkeypatch.setattr(model_map, "AGENT_MODEL_MAP_PROPERTIES_PATH", agent_dir / "model-map-properties.jsonl")
    monkeypatch.setattr(model_map, "AGENT_MODEL_MAP_VERSION_DIFF_PATH", agent_dir / "model-map-version-diff.jsonl")
    model_dir.mkdir(parents=True)
    (model_dir / "instance-schema.json").write_text("{}", encoding="utf-8")
    (model_dir / "entity-crosswalk.jsonl").write_text("", encoding="utf-8")
    (agent_dir).mkdir(parents=True)
    (agent_dir / "model-map-relationships.jsonl").write_text("", encoding="utf-8")
    stable_path = tmp_path / "stable.json"
    latest_path = tmp_path / "latest.json"
    stable_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-demo-model-map-scrape-v1",
                "source_url": "https://stable.example/admin/power-tools/model-map",
                "rock_version": "18.2.4",
                "models": [
                    {
                        "model_link_name": "Person",
                        "model_title": "Person",
                        "category_name": "CRM",
                        "selected_entity_type_guid": "entity-person",
                        "property_count": 2,
                        "database_property_count": 1,
                        "lava_property_count": 2,
                        "not_mapped_property_count": 1,
                        "properties": [
                            {
                                "name": "FullName",
                                "description": "Gets the full name.",
                                "is_database": False,
                                "is_lava": True,
                                "is_not_mapped": True,
                                "enum_values": [],
                                "related_entity_links": [],
                            },
                            {
                                "name": "IsSystem",
                                "description": "Gets whether this is a system record.",
                                "is_database": True,
                                "is_lava": True,
                                "is_not_mapped": False,
                                "enum_values": [],
                                "related_entity_links": [
                                    {
                                        "text": "Group",
                                        "entity_type_guid": "entity-group",
                                        "href": "?EntityType=entity-group",
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "model_link_name": "Group",
                        "model_title": "Group",
                        "category_name": "Group",
                        "property_count": 0,
                        "properties": [],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    latest_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-demo-model-map-scrape-v1",
                "source_url": "https://latest.example/admin/power-tools/model-map",
                "rock_version": "20.0.3",
                "models": [
                    {
                        "model_link_name": "Person",
                        "model_title": "Person",
                        "category_name": "CRM",
                        "selected_entity_type_guid": "entity-person",
                        "property_count": 2,
                        "database_property_count": 1,
                        "lava_property_count": 2,
                        "not_mapped_property_count": 1,
                        "properties": [
                            {
                                "name": "FullName",
                                "description": "Gets the formatted full name.",
                                "is_database": False,
                                "is_lava": True,
                                "is_not_mapped": True,
                                "enum_values": [],
                                "related_entity_links": [],
                            },
                            {
                                "name": "IsSystem",
                                "description": "Gets whether this is a system record.",
                                "is_database": True,
                                "is_lava": True,
                                "is_not_mapped": False,
                                "enum_values": [],
                                "related_entity_links": [
                                    {
                                        "text": "Group",
                                        "entity_type_guid": "entity-group",
                                        "href": "?EntityType=entity-group",
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "model_link_name": "Group",
                        "model_title": "Group",
                        "category_name": "Group",
                        "property_count": 0,
                        "properties": [],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    counts = model_map.build_model_map(stable_scrape_path=stable_path, latest_scrape_path=latest_path)

    assert counts["source"] == "scraped_model_maps"
    assert counts["stable_version"] == "18.2.4"
    assert counts["pre_alpha_version"] == "20.0.3"
    assert counts["stable_models"] == 2
    assert counts["stable_properties"] == 2
    assert counts["pre_alpha_models"] == 2
    assert counts["pre_alpha_properties"] == 2
    assert counts["model_detail_pages"] == 2
    assert counts["version_diff_changes"] == 1

    stable_models = list(read_jsonl(model_dir / "stable-models.jsonl"))
    person = next(row for row in stable_models if row["model_name"] == "Person")
    assert person["model_detail_path"] == "knowledge/model-map/models/person.md"
    assert person["entity_type_guid"] == "entity-person"
    assert person["database_property_count"] == 1
    assert person["lava_property_count"] == 2
    assert person["lava_non_database_property_count"] == 1

    summary = json.loads((agent_dir / "model-map-summary.json").read_text(encoding="utf-8"))
    assert summary["stable_model_count"] == 2
    assert summary["pre_alpha_model_count"] == 2
    assert summary["model_detail_count"] == 2
    assert summary["contains_row_data"] is False
    assert summary["stable"]["rock_version"] == "18.2.4"
    assert summary["pre_alpha"]["rock_version"] == "20.0.3"
    assert summary["version_diff"]["property_changed_count"] == 1
    assert summary["paths"]["agent_entities"] == "agent/model-map-entities.jsonl"
    assert summary["paths"]["agent_properties"] == "agent/model-map-properties.jsonl"
    properties = list(read_jsonl(model_dir / "stable-properties.jsonl"))
    full_name = next(row for row in properties if row["property_name"] == "FullName")
    assert full_name["is_lava"] is True
    assert full_name["is_not_mapped"] is True
    assert full_name["is_lava_supported_non_database"] is True
    is_system = next(row for row in properties if row["property_name"] == "IsSystem")
    assert is_system["is_lava"] is True
    assert is_system["is_database"] is True
    assert is_system["is_lava_supported_non_database"] is False
    assert list(read_jsonl(agent_dir / "model-map-properties.jsonl")) == properties
    assert (model_dir / "version-diff.jsonl").exists()
    assert (agent_dir / "model-map-version-diff.jsonl").exists()
    assert not (model_dir / "instance-schema.json").exists()
    assert not (model_dir / "entity-crosswalk.jsonl").exists()
    assert not (agent_dir / "model-map-relationships.jsonl").exists()
    assert (model_dir / "concept-slices" / "crm.md").exists()
    model_detail = (model_dir / "models" / "person.md").read_text(encoding="utf-8")
    assert "# Person Model Detail" in model_detail
    assert "| IsSystem |" in model_detail
    assert "## Related Model Map Links" in model_detail
    assert "| IsSystem | [Group](group.md) | entity-group |" in model_detail
    assert "18.2.4" in model_detail
    assert "Stable To Pre-Alpha Changes" in model_detail
    assert "Rock Model Map" in (model_dir / "index.md").read_text(encoding="utf-8")
    category_slice = (model_dir / "concept-slices" / "crm.md").read_text(encoding="utf-8")
    assert "Generated stable-track slice" in category_slice
    assert "Generated latest-track slice" not in category_slice


def test_stamp_model_map_scrape_version_records_demo_version(monkeypatch, tmp_path):
    scrape_path = tmp_path / "demo-model-map-full-scrape.json"
    models_jsonl_path = tmp_path / "demo-model-map-full-scrape.models.jsonl"
    scrape_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-demo-model-map-scrape-v1",
                "source_url": "https://rocksolidchurchdemo.com/admin/power-tools/model-map",
                "models": [],
            }
        ),
        encoding="utf-8",
    )
    write_jsonl(models_jsonl_path, [{"model_title": "Person", "selected_entity_type_id": "15"}])

    class FakeResponse:
        status = 200
        headers = {"content-type": "application/json; charset=utf-8"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self, _limit):
            return b'"18.2.4"'

    def fake_urlopen(request, timeout):
        assert request.full_url == "https://demo.example/api/Utility/GetRockSemanticVersionNumber"
        assert timeout == 7
        return FakeResponse()

    monkeypatch.setattr(model_map.urllib.request, "urlopen", fake_urlopen)

    result = model_map.stamp_model_map_scrape_version(
        scrape_path=scrape_path,
        endpoint_url="https://demo.example/api/Utility/GetRockSemanticVersionNumber",
        timeout_seconds=7,
    )

    assert result["rock_version"] == "18.2.4"
    assert result["models_jsonl_updated"] == 1
    stamped = json.loads(scrape_path.read_text(encoding="utf-8"))
    assert stamped["rock_version"] == "18.2.4"
    assert stamped["rock_version_source_url"] == "https://demo.example/api/Utility/GetRockSemanticVersionNumber"
    assert stamped["demo_rock_version_context"]["status"] == "detected"
    assert stamped["demo_rock_version_context"]["http_status"] == 200
    model_rows = list(read_jsonl(models_jsonl_path))
    assert model_rows[0]["rock_version"] == "18.2.4"
    assert model_rows[0]["rock_version_source_url"] == "https://demo.example/api/Utility/GetRockSemanticVersionNumber"


def test_model_map_artifact_freshness_flags_live_version_drift(monkeypatch, tmp_path):
    summary_path = tmp_path / "model-map-summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "stable": {
                    "rock_version": "18.2.4",
                    "rock_version_source_url": "https://stable.example/api/Utility/GetRockSemanticVersionNumber",
                    "source_url": "https://stable.example/admin/power-tools/model-map",
                },
                "latest": {
                    "rock_version": "20.0.3",
                    "rock_version_source_url": "https://latest.example/api/Utility/GetRockSemanticVersionNumber",
                    "source_url": "https://latest.example/admin/power-tools/model-map",
                },
            }
        ),
        encoding="utf-8",
    )

    class FakeResponse:
        status = 200
        headers = {"content-type": "application/json"}

        def __init__(self, body):
            self.body = body

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self, _limit):
            return self.body

    def fake_urlopen(request, timeout):
        assert timeout == 3
        if request.full_url == "https://stable.example/api/Utility/GetRockSemanticVersionNumber":
            return FakeResponse(b'"19.1.8"')
        if request.full_url == "https://latest.example/api/Utility/GetRockSemanticVersionNumber":
            return FakeResponse(b'"20.0.4"')
        raise AssertionError(request.full_url)

    monkeypatch.setattr(model_map.urllib.request, "urlopen", fake_urlopen)

    result = model_map.model_map_artifact_freshness(summary_path=summary_path, timeout_seconds=3)

    assert result["status"] == "stale"
    assert [(row["track"], row["recorded_version"], row["live_version"]) for row in result["stale_tracks"]] == [
        ("stable", "18.2.4", "19.1.8"),
        ("latest", "20.0.3", "20.0.4"),
    ]


def test_model_map_scrape_freshness_accepts_current_scrapes(monkeypatch, tmp_path):
    stable_path = tmp_path / "stable.json"
    latest_path = tmp_path / "latest.json"
    stable_path.write_text(
        json.dumps(
            {
                "rock_version": "19.1.8",
                "rock_version_source_url": "https://stable.example/api/Utility/GetRockSemanticVersionNumber",
                "source_url": "https://stable.example/admin/power-tools/model-map",
            }
        ),
        encoding="utf-8",
    )
    latest_path.write_text(
        json.dumps(
            {
                "rock_version": "20.0.4",
                "rock_version_source_url": "https://latest.example/api/Utility/GetRockSemanticVersionNumber",
                "source_url": "https://latest.example/admin/power-tools/model-map",
            }
        ),
        encoding="utf-8",
    )

    class FakeResponse:
        status = 200
        headers = {"content-type": "application/json"}

        def __init__(self, body):
            self.body = body

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self, _limit):
            return self.body

    def fake_urlopen(request, timeout):
        if "stable.example" in request.full_url:
            return FakeResponse(b'"19.1.8"')
        if "latest.example" in request.full_url:
            return FakeResponse(b'"20.0.4"')
        raise AssertionError(request.full_url)

    monkeypatch.setattr(model_map.urllib.request, "urlopen", fake_urlopen)

    result = model_map.model_map_scrape_freshness(
        stable_scrape_path=stable_path,
        latest_scrape_path=latest_path,
    )

    assert result["status"] == "current"
    assert [row["status"] for row in result["tracks"]] == ["current", "current"]


def test_build_model_map_version_diff_tracks_added_and_changed_properties(tmp_path):
    stable_path = tmp_path / "stable.json"
    latest_path = tmp_path / "latest.json"
    output_path = tmp_path / "diff.json"
    output_jsonl_path = tmp_path / "diff.jsonl"
    stable_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-demo-model-map-scrape-v1",
                "source_url": "https://stable.example/admin/power-tools/model-map",
                "rock_version": "18.2.4",
                "models": [
                    {
                        "model_link_name": "Person",
                        "model_title": "Person",
                        "category_name": "CRM",
                        "property_count": 1,
                        "properties": [
                            {
                                "name": "FullName",
                                "description": "Gets the full name.",
                                "is_database": False,
                                "is_lava": True,
                                "is_not_mapped": True,
                                "enum_values": [],
                                "related_entity_links": [],
                            },
                            {
                                "name": "1020 = Anonymous Visitor",
                                "description": "Enum value row captured by older table scraping.",
                                "is_database": False,
                                "is_lava": False,
                                "is_not_mapped": False,
                                "enum_values": [],
                                "related_entity_links": [],
                            },
                            {
                                "name": "-1",
                                "description": "Negative enum sentinel row captured by older table scraping.",
                                "is_database": False,
                                "is_lava": False,
                                "is_not_mapped": False,
                                "enum_values": [],
                                "related_entity_links": [],
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    latest_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-demo-model-map-scrape-v1",
                "source_url": "https://latest.example/admin/power-tools/model-map",
                "rock_version": "20.0.3",
                "models": [
                    {
                        "model_link_name": "Person",
                        "model_title": "Person",
                        "category_name": "CRM",
                        "property_count": 2,
                        "properties": [
                            {
                                "name": "FullName",
                                "description": "Gets the formatted full name.",
                                "is_database": False,
                                "is_lava": True,
                                "is_not_mapped": True,
                                "enum_values": [],
                                "related_entity_links": [],
                            },
                            {
                                "name": "AccountProtectionProfile",
                                "description": "Gets the account protection profile.",
                                "is_database": True,
                                "is_lava": True,
                                "is_not_mapped": False,
                                "enum_values": [{"value": "0", "label": "Low"}],
                                "related_entity_links": [],
                            },
                        ],
                    },
                    {
                        "model_link_name": "AI Agent",
                        "model_title": "AIAgent",
                        "category_name": "AI",
                        "property_count": 0,
                        "properties": [],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    result = model_map.build_model_map_version_diff(
        stable_path=stable_path,
        latest_path=latest_path,
        output_path=output_path,
        output_jsonl_path=output_jsonl_path,
    )

    assert result["stable_version"] == "18.2.4"
    assert result["latest_version"] == "20.0.3"
    assert result["model_added_count"] == 1
    assert result["property_added_count"] == 1
    assert result["property_changed_count"] == 1
    rows = list(read_jsonl(output_jsonl_path))
    assert {row["change_type"] for row in rows} == {"model_added", "property_added", "property_changed"}
    assert all(row.get("property_name") != "1020 = Anonymous Visitor" for row in rows)
    assert all(row.get("property_name") != "-1" for row in rows)
    changed = next(row for row in rows if row["change_type"] == "property_changed")
    assert changed["property_name"] == "FullName"
    assert changed["changed_fields"] == ["description"]
    summary = json.loads(output_path.read_text(encoding="utf-8"))
    assert summary["changed_field_counts"] == {"description": 1}
