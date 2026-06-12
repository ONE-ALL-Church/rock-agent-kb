from bs4 import BeautifulSoup

from rock_kb.community import extract_lava_doc_fields
from rock_kb.concepts import Concept, build_concept_guide
from rock_kb.lava_capabilities import (
    LAVA_DEPENDENT_CONCEPTS,
    lava_capability_rows,
    lava_source_dependency_hashes,
    render_reference_index,
)


def test_extract_lava_filter_elements_from_official_page_shape():
    html = """
    <main>
      <h1>Text Filters</h1>
      <h1>Append</h1>
      <p>Server: v1.0 Mobile: v1.0 Adds a given string to another string.</p>
      <h1>Escape</h1>
      <p>Server: v2.0 Escapes text for HTML output.</p>
    </main>
    """

    fields = extract_lava_doc_fields(
        BeautifulSoup(html, "html.parser"),
        "https://community.rockrms.com/lava/filters/text-filters",
        "Text Filters Append Escape",
    )

    assert fields["lava_doc_category"] == "filter"
    assert [row["name"] for row in fields["lava_elements"]] == ["Append", "Escape"]
    assert fields["lava_elements"][0]["server_versions"] == ["1.0"]
    assert fields["lava_elements"][0]["mobile_versions"] == ["1.0"]


def test_lava_capability_rows_classify_high_risk_commands():
    rows = lava_capability_rows(
        [
            {
                "id": "rock_lava_docs:sql",
                "source_id": "rock_lava_docs",
                "source_url": "https://community.rockrms.com/lava/commands/sql-commands",
                "source_title": "SQL",
                "summary": "SQL Command The SQL Lava command allows you to run SQL. {% sql %} SELECT 1 {% endsql %} Your SQL can also contain Lava. Do not allow SQL injection attacks.",
                "content_hash": "hash-sql",
                "rock_versions": [],
                "topics": ["lava", "sql"],
                "lava_doc_category": "command",
                "lava_elements": [
                    {
                        "category": "command",
                        "name": "SQL",
                        "official_url": "https://community.rockrms.com/lava/commands/sql-commands",
                        "server_versions": [],
                        "mobile_versions": [],
                        "source_fragment_hash": "fragment-sql",
                    }
                ],
            },
            {
                "id": "rock_lava_docs:append",
                "source_id": "rock_lava_docs",
                "source_url": "https://community.rockrms.com/lava/filters/text-filters",
                "source_title": "Text Filters",
                "summary": "Text Filters",
                "content_hash": "hash-text",
                "rock_versions": [],
                "topics": ["lava"],
                "lava_doc_category": "filter",
                "lava_elements": [
                    {
                        "category": "filter",
                        "name": "Append",
                        "official_url": "https://community.rockrms.com/lava/filters/text-filters",
                        "server_versions": ["1.0"],
                        "mobile_versions": ["1.0"],
                        "summary_hint": "Append Show Details Server: v1.0 Mobile: v1.0 Adds a given string to another string.",
                        "source_fragment_hash": "fragment-append",
                    }
                ],
            },
        ]
    )
    by_name = {row["name"]: row for row in rows}

    assert by_name["SQL"]["risk_tier"] == "high"
    assert by_name["SQL"]["uses_sql_or_entity_access"] is True
    assert by_name["SQL"]["command_enablement_required"] is True
    assert by_name["SQL"]["requires_live_instance_verification"] is True
    assert by_name["SQL"]["description"].startswith("The SQL Lava command allows you to run SQL")
    assert by_name["SQL"]["usage_summary"].startswith("Use SQL as an enabled Lava command")
    assert "official command page" in by_name["SQL"]["parameter_summary"]
    assert by_name["SQL"]["example_summary"].startswith("Official page includes Lava examples")
    assert any("SQL" in gotcha and "input" in gotcha for gotcha in by_name["SQL"]["gotchas"])
    assert by_name["Append"]["mobile_client_support"]["supported"] is True
    assert by_name["Append"]["description"] == "Adds a given string to another string."
    assert by_name["Append"]["usage_summary"].startswith("Use Append as a Lava filter")
    assert by_name["Append"]["official_docs_note"].startswith("Link to the official Rock Lava page")


def test_lava_reference_index_includes_usage_detail_rows():
    rows = lava_capability_rows(
        [
            {
                "id": "rock_lava_docs:sql",
                "source_id": "rock_lava_docs",
                "source_url": "https://community.rockrms.com/lava/commands/sql-commands",
                "source_title": "SQL",
                "summary": "The SQL Lava command allows you to run SQL. {% sql %} SELECT 1 {% endsql %} Do not allow SQL injection attacks.",
                "content_hash": "hash-sql",
                "rock_versions": [],
                "topics": ["lava", "sql"],
                "lava_doc_category": "command",
                "lava_elements": [
                    {
                        "category": "command",
                        "name": "SQL",
                        "official_url": "https://community.rockrms.com/lava/commands/sql-commands",
                        "server_versions": [],
                        "mobile_versions": [],
                        "source_fragment_hash": "fragment-sql",
                    }
                ],
            },
        ]
    )

    index = render_reference_index(rows, [])

    assert "## Usage Detail Rows" in index
    assert "| Category | Name | How To Use | Parameters | Examples | Gotchas | Official Docs Boundary | Official Page |" in index
    assert "Use SQL as an enabled Lava command" in index
    assert "Official page includes Lava examples" in index
    assert "Do not concatenate untrusted input into SQL" in index
    assert "Link to the official Rock Lava page for syntax, parameters, and examples" in index


def test_lava_capability_flags_are_literal_not_page_keyword_inherited():
    rows = lava_capability_rows(
        [
            {
                "id": "rock_lava_docs:entity",
                "source_id": "rock_lava_docs",
                "source_url": "https://community.rockrms.com/lava/commands/entity-commands",
                "source_title": "Entity",
                "summary": "Entity command reads Rock entities and references securityenabled.",
                "content_hash": "hash-entity",
                "topics": ["lava"],
                "lava_doc_category": "command",
                "lava_elements": [{"category": "command", "name": "Entity", "official_url": "https://community.rockrms.com/lava/commands/entity-commands"}],
            },
            {
                "id": "rock_lava_docs:array",
                "source_id": "rock_lava_docs",
                "source_url": "https://community.rockrms.com/lava/filters/array-filters",
                "source_title": "Array Filters",
                "summary": "The page mentions entity command sorting, SQL-shaped examples, and output.",
                "content_hash": "hash-array",
                "topics": ["lava"],
                "lava_doc_category": "filter",
                "lava_elements": [
                    {"category": "filter", "name": "First", "official_url": "https://community.rockrms.com/lava/filters/array-filters"},
                    {"category": "filter", "name": "Capitalize", "official_url": "https://community.rockrms.com/lava/filters/text-filters"},
                    {"category": "filter", "name": "ToJSON", "official_url": "https://community.rockrms.com/lava/filters/other-filters"},
                    {"category": "filter", "name": "CreateEntitySet", "official_url": "https://community.rockrms.com/lava/filters/other-filters"},
                    {"category": "tag", "name": "Lava", "official_url": "https://community.rockrms.com/lava/tags/lava-tags"},
                ],
            },
        ]
    )
    by_name = {row["name"]: row for row in rows}

    assert by_name["Entity"]["risk_tier"] == "high"
    assert by_name["Entity"]["reads_data"] is True
    assert by_name["Entity"]["mutates_data"] is False
    assert by_name["Entity"]["uses_sql_or_entity_access"] is True
    assert by_name["First"]["risk_tier"] == "low"
    assert by_name["First"]["uses_sql_or_entity_access"] is False
    assert by_name["Capitalize"]["performs_external_io"] is False
    assert by_name["Capitalize"]["risk_tier"] == "low"
    assert by_name["ToJSON"]["performs_external_io"] is False
    assert by_name["ToJSON"]["risk_tier"] == "low"
    assert by_name["CreateEntitySet"]["risk_tier"] == "high"
    assert by_name["CreateEntitySet"]["mutates_data"] is True
    assert by_name["CreateEntitySet"]["uses_sql_or_entity_access"] is True
    assert by_name["Lava"]["risk_tier"] == "low"


def test_lava_dependent_concepts_attach_lava_hashes():
    concept = Concept(
        id="api-integrations",
        title="API Integrations",
        description="API.",
        keywords=["api"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=2,
        raw={},
    )
    records = [
        {"id": "api-doc", "source_id": "rock_api_docs", "source_title": "API", "summary": "API", "content_hash": "api-hash"},
        {
            "id": "lava-api",
            "source_id": "rock_lava_docs",
            "source_url": "https://community.rockrms.com/lava/lava-api",
            "source_title": "Creating APIs Using Lava",
            "summary": "Lava API",
            "content_hash": "lava-hash",
        },
    ]

    _text, dependency = build_concept_guide(concept, records, {})

    assert "api-integrations" in LAVA_DEPENDENT_CONCEPTS
    assert dependency["lava_capability_record_hashes"] == {"lava-api": "lava-hash"}
    assert dependency["source_hashes"]["lava-api"] == "lava-hash"


def test_lava_source_dependency_hashes_are_source_record_based():
    hashes = lava_source_dependency_hashes(
        [
            {"id": "a", "source_id": "rock_lava_docs", "source_url": "https://example.test/a", "content_hash": "1"},
            {"id": "b", "source_id": "rock_lava_docs", "source_url": "https://example.test/b", "content_hash": "2"},
        ]
    )

    assert hashes == {"a": "1", "b": "2"}
