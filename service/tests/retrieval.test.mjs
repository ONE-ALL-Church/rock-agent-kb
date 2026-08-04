import assert from "node:assert/strict";
import crypto from "node:crypto";
import test from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { Miniflare } from "miniflare";
import { MockAgent } from "undici";

const WORKER_BUNDLE = "dist/dry-run/index.js";
const RECIPE_FIXTURE_CONTENT = "verified recipe fixture\n";
const RECIPE_FIXTURE_SHA = crypto.createHash("sha256").update(RECIPE_FIXTURE_CONTENT).digest("hex");
const RECIPE_FIXTURE_COMMIT = "d8ea54fa67efe40692689fb009561ff96e88bf42";
const SKILL_FIXTURE_CONTENT = "---\nname: rock-kb-agent\ndescription: Test skill.\n---\n\n# Rock KB Agent\n";
const SKILL_FIXTURE_SHA = crypto.createHash("sha256").update(SKILL_FIXTURE_CONTENT).digest("hex");
const ISSUE_FIXTURE_CATALOG_HASH = "c".repeat(64);
const ISSUE_FIXTURE_SOURCE_HASHES = {
  rock_core_issues: crypto.createHash("sha256")
    .update(`rock_core_issues:${ISSUE_FIXTURE_CATALOG_HASH}:1`)
    .digest("hex"),
  rock_mobile_issues: crypto.createHash("sha256")
    .update(`rock_mobile_issues:${ISSUE_FIXTURE_CATALOG_HASH}:0`)
    .digest("hex"),
};

test("search is compact by default and exact result expands the row", async () => {
  const mf = await buildWorker();
  try {
    const searchResponse = await mf.dispatchFetch("https://kb.example.test/search?q=labels%20printing&limit=1");
    const search = await searchResponse.json();

    assert.equal(searchResponse.status, 200);
    assert.equal(search.schema, "rock-kb-search-result-v3");
    assert.equal(search.detail, "compact");
    assert.equal(search.intent, "reference");
    assert.equal(search.min_claim_tier, "source_backed");
    assert.equal(search.results.length, 1);
    assert.equal(search.results[0].id, "claim:claim:abc123");
    assert.deepEqual(search.results[0].concepts, ["check-in"]);
    assert.equal(typeof search.results[0].snippet, "string");
    assert.equal(typeof search.results[0].score, "number");
    assert.equal("signals" in search.results[0], false);
    assert.equal("body" in search.results[0], false);
    assert.equal("payload" in search.results[0], false);

    const resultResponse = await mf.dispatchFetch("https://kb.example.test/results/claim%3Aclaim%3Aabc123%3Acheck-in");
    const result = await resultResponse.json();
    assert.equal(result.status, "ok");
    assert.equal(result.requested_result_id, "claim:claim:abc123:check-in");
    assert.equal(result.canonical_result_id, "claim:claim:abc123");
    assert.match(result.result.body, /printing/);
    assert.equal(result.result.payload.claim_id, "claim:abc123");

    const conceptResponse = await mf.dispatchFetch("https://kb.example.test/results/concept%3Acheck-in");
    const concept = await conceptResponse.json();
    assert.equal(concept.status, "ok");
    assert.match(concept.result.body, /eligibility and availability troubleshooting/);

    const debugResponse = await mf.dispatchFetch("https://kb.example.test/search?q=labels%20printing&limit=1&debug=true");
    const debug = await debugResponse.json();
    assert.equal(typeof debug.results[0].signals.title_overlap, "number");
    assert.equal(Number.isInteger(debug.results[0].score * 100), true);
    assert.ok(JSON.stringify(search.results[0]).length <= JSON.stringify(debug.results[0]).length * 0.7);
  } finally {
    await mf.dispose();
  }
});

test("search returns a private-instance boundary instead of unrelated public guidance", async () => {
  const mf = await buildWorker();
  const privateQueries = [
    "What is my church's private Twilio authentication token?",
    "What is the exact GUID of a workflow type created only in my local Rock instance?",
    "Which named person attended my church last Sunday?",
    "What is the password for my Rock database?",
    "What custom Lava shortcode exists only in my private Rock database?",
  ];
  try {
    for (const query of privateQueries) {
      const response = await mf.dispatchFetch(
        `https://kb.example.test/search?q=${encodeURIComponent(query)}&limit=3`,
      );
      const payload = await response.json();
      assert.equal(response.status, 200);
      assert.equal(payload.answer_boundary, "private_instance_data_required");
      assert.deepEqual(payload.results, []);
    }

    const guidanceResponse = await mf.dispatchFetch(
      "https://kb.example.test/search?q=How%20do%20I%20secure%20a%20password%20for%20my%20local%20Rock%20database%3F",
    );
    const guidance = await guidanceResponse.json();
    assert.equal(guidance.answer_boundary, null);

    const mcpResponse = await mcp(mf, "tools/call", {
      name: "kb_search",
      arguments: { query: privateQueries[0], limit: 3 },
    });
    assert.deepEqual(mcpResponse.result.structuredContent.results, []);
  } finally {
    await mf.dispose();
  }
});

test("canonical canary is explicit, opt-in, isolated, and outcome-aware", async () => {
  const canonicalHash = "d".repeat(64);
  const mf = await buildWorker({
    canonicalShadow: {
      status: "ready",
      contentHash: canonicalHash,
      searchRowCount: 1,
      knowledgeUnitCount: 1,
      artifactCount: 8,
      observationCount: 1,
    },
  });
  const installationId = `rkbi_${"c".repeat(43)}`;
  const canaryHeaders = {
    "x-rock-kb-client": "cli",
    "x-rock-kb-cohort": "external-test",
    "x-rock-kb-installation-id": installationId,
  };
  const canaryId =
    "cross-source:claim:content-channel-item-list-authorization-6914";
  try {
    const db = await mf.getD1Database("KB_DB");
    await db.prepare(
      `INSERT INTO canonical_search_rows (
         id, kind, title, body, path, url, concept, authority_tier,
         claim_tier, claim_tier_rank, source_id, concepts_json,
         topics_json, payload_json
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    ).bind(
      canaryId,
      "claim",
      "Content Channel Item List Authorization Fix in Rock 19.3",
      "Rock 19.3 authorizes add and delete against the selected content channel.",
      "shadow/canonical/claim.jsonl",
      "https://github.com/SparkDevNetwork/Rock/issues/6914",
      "content-personalization",
      "source-code-confirmed",
      "source_backed",
      1,
      "sparkdevnetwork_rock",
      JSON.stringify([
        "content-personalization",
        "security-permissions",
      ]),
      JSON.stringify(["cms", "permissions"]),
      JSON.stringify({
        knowledge_unit_id: canaryId,
        rock_versions: ["19.3"],
      }),
    ).run();
    await db.prepare(
      "INSERT INTO canonical_search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)",
    ).bind(
      canaryId,
      "Content Channel Item List Authorization Fix in Rock 19.3",
      "Rock 19.3 authorizes add and delete against the selected content channel.",
      "content-personalization security-permissions cms permissions",
    ).run();
    await db.prepare(
      "INSERT INTO canonical_search_row_aliases (alias_id, canonical_id) VALUES (?, ?)",
    ).bind("claim:legacy-6914", canaryId).run();

    const missingOptIn = await mf.dispatchFetch(
      "https://kb.example.test/search?q=content%20channel%20authorization&projection=canonical-canary",
    );
    assert.equal(missingOptIn.status, 400);
    assert.equal(
      (await missingOptIn.json()).error_code,
      "canonical_canary_opt_in_required",
    );

    const communityOnly = await mf.dispatchFetch(
      "https://kb.example.test/search?q=content%20channel%20authorization&projection=canonical-canary",
      {
        headers: {
          ...canaryHeaders,
          "x-rock-kb-cohort": "community",
        },
      },
    );
    assert.equal(communityOnly.status, 400);

    const legacy = await (
      await mf.dispatchFetch(
        "https://kb.example.test/search?q=content%20channel%20authorization",
        { headers: canaryHeaders },
      )
    ).json();
    assert.equal(
      legacy.results.some((row) => row.id === canaryId),
      false,
    );

    const canaryResponse = await mf.dispatchFetch(
      "https://kb.example.test/search?q=content%20channel%20authorization&projection=canonical-canary",
      { headers: canaryHeaders },
    );
    const canary = await canaryResponse.json();
    assert.equal(canaryResponse.status, 200);
    assert.equal(canary.retrieval_projection, "canonical-canary");
    assert.equal(canary.results[0].id, canaryId);
    assert.equal(
      canary.results[0].retrieval_projection,
      "canonical-canary",
    );

    const exactResponse = await mf.dispatchFetch(
      "https://kb.example.test/results/claim%3Alegacy-6914?projection=canonical-canary",
      { headers: canaryHeaders },
    );
    const exact = await exactResponse.json();
    assert.equal(exact.status, "ok");
    assert.equal(exact.canonical_result_id, canaryId);
    assert.equal(exact.retrieval_projection, "canonical-canary");

    const mcpResponse = await mcp(
      mf,
      "tools/call",
      {
        name: "kb_search",
        arguments: {
          query: "content channel authorization",
          projection: "canonical-canary",
        },
      },
      canaryHeaders,
    );
    assert.equal(
      mcpResponse.result.structuredContent.results[0].id,
      canaryId,
    );
    const mcpComparison = await mcp(
      mf,
      "tools/call",
      {
        name: "kb_compare_retrieval",
        arguments: {
          query: "content channel authorization",
          category: "version_sensitive",
        },
      },
      canaryHeaders,
    );
    assert.equal(mcpComparison.result.structuredContent.status, "ready");
    assert.equal(JSON.stringify(mcpComparison).includes("content channel authorization"), false);

    const outcomeResponse = await mf.dispatchFetch(
      "https://kb.example.test/outcomes",
      {
        method: "POST",
        headers: {
          ...canaryHeaders,
          "content-type": "application/json",
        },
        body: JSON.stringify({
          result_id: canaryId,
          outcome: "useful",
          reason_codes: ["answered"],
          consent_attested: true,
          retrieval_projection: "canonical-canary",
        }),
      },
    );
    const outcome = await outcomeResponse.json();
    assert.equal(outcomeResponse.status, 201);
    assert.equal(outcome.projection_version, canonicalHash);
    assert.equal(outcome.retrieval_projection, "canonical-canary");
    const storedOutcome = await db.prepare(
      "SELECT retrieval_projection FROM outcome_events_v1 WHERE result_id = ?",
    ).bind(canaryId).first();
    assert.equal(storedOutcome.retrieval_projection, "canonical-canary");

    const missingComparisonOptIn = await mf.dispatchFetch(
      "https://kb.example.test/comparisons",
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query: "content channel authorization" }),
      },
    );
    assert.equal(missingComparisonOptIn.status, 400);
    assert.equal((await missingComparisonOptIn.json()).error_code, "comparison_opt_in_required");

    const comparisonResponse = await mf.dispatchFetch(
      "https://kb.example.test/comparisons",
      {
        method: "POST",
        headers: { ...canaryHeaders, "content-type": "application/json" },
        body: JSON.stringify({
          query: "content channel authorization",
          category: "version_sensitive",
          limit: 3,
        }),
      },
    );
    assert.equal(comparisonResponse.status, 201);
    const comparison = await comparisonResponse.json();
    assert.equal(comparison.status, "ready");
    assert.match(comparison.comparison_id, /^kbc_[0-9a-f]{24}$/);
    assert.deepEqual(comparison.options.map((option) => option.label), ["A", "B"]);
    assert.equal(comparison.options.every((option) => option.results.every((row) => (
      !("id" in row)
      && !("path" in row)
      && !("retrieval_projection" in row)
      && new RegExp(`^${option.label}\\d+$`).test(row.result_key)
    ))), true);
    assert.equal(JSON.stringify(comparison).includes("content channel authorization"), false);
    const pendingComparison = await db.prepare(
      "SELECT option_a_projection FROM retrieval_comparison_sessions_v1 WHERE comparison_id = ?",
    ).bind(comparison.comparison_id).first();
    const comparisonPreference = pendingComparison.option_a_projection === "canonical-canary" ? "a_better" : "b_better";

    const comparisonReviewResponse = await mf.dispatchFetch(
      "https://kb.example.test/comparisons/review",
      {
        method: "POST",
        headers: { ...canaryHeaders, "content-type": "application/json" },
        body: JSON.stringify({
          comparison_id: comparison.comparison_id,
          preference: comparisonPreference,
          reason_codes: ["better_version_fit"],
          consent_attested: true,
        }),
      },
    );
    assert.equal(comparisonReviewResponse.status, 201);
    const comparisonReview = await comparisonReviewResponse.json();
    assert.equal(comparisonReview.preference, "canonical_better");
    assert.equal(comparisonReview.canonical_projection_version, canonicalHash);
    const duplicateComparisonReview = await mf.dispatchFetch(
      "https://kb.example.test/comparisons/review",
      {
        method: "POST",
        headers: { ...canaryHeaders, "content-type": "application/json" },
        body: JSON.stringify({
          comparison_id: comparison.comparison_id,
          preference: comparisonPreference,
          reason_codes: ["better_version_fit"],
          consent_attested: true,
        }),
      },
    );
    assert.equal(duplicateComparisonReview.status, 409);
    assert.equal((await duplicateComparisonReview.json()).error_code, "comparison_already_submitted");

    const comparisonColumns = await db.prepare("PRAGMA table_info(retrieval_comparison_sessions_v1)").all();
    assert.equal(comparisonColumns.results.some((column) => column.name === "query"), false);
    const storedComparison = await db.prepare(
      "SELECT preference, legacy_result_id, canonical_result_id FROM retrieval_comparison_outcomes_v1 WHERE comparison_id = ?",
    ).bind(comparison.comparison_id).first();
    assert.equal(storedComparison.preference, "canonical_better");
    assert.equal(storedComparison.canonical_result_id, canaryId);

    const comparisonDashboard = await (
      await mf.dispatchFetch("https://kb.example.test/operations/dashboard")
    ).json();
    assert.equal(comparisonDashboard.retrieval_comparisons.outcome_count, 1);
    assert.equal(comparisonDashboard.retrieval_comparisons.by_preference.canonical_better, 1);
    assert.equal(comparisonDashboard.retrieval_comparisons.decision_metrics.canonical_preference_rate, 1);
    assert.equal(comparisonDashboard.retrieval_comparisons.review_queue.length, 0);
    assert.equal(JSON.stringify(comparisonDashboard.retrieval_comparisons).includes(installationId), false);
    assert.equal(JSON.stringify(comparisonDashboard.retrieval_comparisons).includes("content channel authorization"), false);
    await db.prepare(
      "UPDATE retrieval_comparison_sessions_v1 SET expires_at = ? WHERE comparison_id = ?",
    ).bind("2000-01-01T00:00:00.000Z", comparison.comparison_id).run();
    await mf.dispatchFetch("https://kb.example.test/operations/dashboard");
    const expiredComparison = await db.prepare(
      "SELECT comparison_id FROM retrieval_comparison_sessions_v1 WHERE comparison_id = ?",
    ).bind(comparison.comparison_id).first();
    assert.equal(expiredComparison, null);

    const telemetry = await (
      await mf.dispatchFetch("https://kb.example.test/telemetry/summary")
    ).json();
    assert.equal(
      telemetry.canonical_canary.external_test_rows.some(
        (row) => row.event === "search",
      ),
      true,
    );
    assert.equal(telemetry.canonical_canary.outcomes.length, 1);
    assert.equal(
      JSON.stringify(telemetry.canonical_canary).includes(installationId),
      false,
    );
    assert.equal(
      JSON.stringify(telemetry.canonical_canary).includes(
        "content channel authorization",
      ),
      false,
    );

    const health = await (
      await mf.dispatchFetch("https://kb.example.test/health")
    ).json();
    assert.equal(
      health.canonical_shadow.active_retrieval_projection,
      "legacy",
    );
    assert.equal(health.canonical_shadow.active_reader, false);
  } finally {
    await mf.dispose();
  }
});

test("canonical can be the default reader and legacy remains an immediate rollback", async () => {
  const canonicalHash = "e".repeat(64);
  const canonicalId = "source-native:claim:rock_documentation:article-1:check-in-labels";
  const mf = await buildWorker({
    activeProjection: "canonical",
    canonicalShadow: {
      status: "ready",
      contentHash: canonicalHash,
      searchRowCount: 1,
      knowledgeUnitCount: 1,
      artifactCount: 8,
      observationCount: 2,
    },
  });
  try {
    const db = await mf.getD1Database("KB_DB");
    await db.prepare(
      `INSERT INTO canonical_search_rows (
         id, kind, title, body, path, url, concept, authority_tier,
         claim_tier, claim_tier_rank, source_id, concepts_json,
         topics_json, payload_json
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    ).bind(
      canonicalId,
      "claim",
      "Canonical check-in labels",
      "Canonical check-in label printing guidance.",
      "canonical/source-native/v1/reviewed-artifacts.jsonl",
      "https://example.test/canonical-labels",
      "check-in",
      "official",
      "source_backed",
      1,
      "rock_documentation",
      JSON.stringify(["check-in"]),
      JSON.stringify(["labels"]),
      JSON.stringify({ claim_id: "claim:canonical-labels" }),
    ).run();
    await db.prepare(
      "INSERT INTO canonical_search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)",
    ).bind(
      canonicalId,
      "Canonical check-in labels",
      "Canonical check-in label printing guidance.",
      "check-in labels",
    ).run();
    await db.prepare(
      "INSERT INTO canonical_search_row_concepts (row_id, concept) VALUES (?, ?)",
    ).bind(canonicalId, "check-in").run();
    await db.prepare(
      "INSERT INTO canonical_search_row_aliases (alias_id, canonical_id) VALUES (?, ?)",
    ).bind("claim:claim:abc123", canonicalId).run();

    const defaultSearch = await (
      await mf.dispatchFetch("https://kb.example.test/search?q=check-in%20label%20printing&limit=1")
    ).json();
    assert.equal(defaultSearch.retrieval_projection, "canonical");
    assert.equal(defaultSearch.results[0].id, canonicalId);

    const explicitLegacy = await (
      await mf.dispatchFetch("https://kb.example.test/search?q=check-in%20label%20printing&limit=1&projection=legacy")
    ).json();
    assert.equal(explicitLegacy.retrieval_projection, "legacy");
    assert.equal(explicitLegacy.results[0].id, "claim:claim:abc123");

    const claim = await (
      await mf.dispatchFetch("https://kb.example.test/claims/id/claim%3Aabc123")
    ).json();
    assert.equal(claim.status, "ok");
    assert.equal(claim.retrieval_projection, "canonical");
    assert.equal(claim.result_ids[0], canonicalId);

    const claims = await (
      await mf.dispatchFetch("https://kb.example.test/claims/check-in")
    ).json();
    assert.equal(claims.retrieval_projection, "canonical");
    assert.equal(claims.total_count, 1);

    const mcpSearch = await mcp(mf, "tools/call", {
      name: "kb_search",
      arguments: { query: "check-in label printing", limit: 1 },
    });
    assert.equal(mcpSearch.result.structuredContent.results[0].id, canonicalId);

    const feedbackResponse = await mf.dispatchFetch("https://kb.example.test/feedback", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ result_id: canonicalId, rating: 1, reason: "helpful" }),
    });
    const feedback = await feedbackResponse.json();
    assert.equal(feedback.retrieval_projection, "canonical");
    assert.equal(feedback.projection_version, canonicalHash);

    const health = await (
      await mf.dispatchFetch("https://kb.example.test/health")
    ).json();
    assert.equal(health.retrieval_projection, "canonical");
    assert.equal(health.retrieval_projection_version, canonicalHash);
    assert.equal(health.canonical_shadow.active_reader, true);
    assert.equal(health.canonical_shadow.activation_supported, true);

    await db.prepare(
      "UPDATE kb_meta SET value = 'legacy' WHERE key = 'active_retrieval_projection'",
    ).run();
    const rolledBack = await (
      await mf.dispatchFetch("https://kb.example.test/search?q=check-in%20label%20printing&limit=1")
    ).json();
    assert.equal(rolledBack.retrieval_projection, "legacy");
    assert.equal(rolledBack.results[0].id, "claim:claim:abc123");

    const inactiveCanonical = await mf.dispatchFetch(
      "https://kb.example.test/search?q=check-in%20label%20printing&projection=canonical",
    );
    assert.equal(inactiveCanonical.status, 409);
    assert.equal(
      (await inactiveCanonical.json()).error_code,
      "canonical_projection_not_active",
    );
  } finally {
    await mf.dispose();
  }
});

test("full search, exact claim lookup, and MCP progressive tools work", async () => {
  const mf = await buildWorker();
  try {
    const fullResponse = await mf.dispatchFetch("https://kb.example.test/search?q=labels&detail=full");
    const full = await fullResponse.json();
    assert.equal(full.detail, "full");
    assert.match(full.results[0].body, /printing/);
    assert.equal(full.results[0].payload.claim_id, "claim:abc123");

    const claimResponse = await mf.dispatchFetch("https://kb.example.test/claims/id/claim%3Aabc123");
    const claim = await claimResponse.json();
    assert.equal(claim.status, "ok");
    assert.equal(claim.claim.claim_id, "claim:abc123");
    assert.deepEqual(claim.concepts, ["check-in"]);

    const toolsResponse = await mcp(mf, "tools/list", {});
    const toolNames = toolsResponse.result.tools.map((tool) => tool.name);
    assert.equal(toolNames.length, 35);
    assert.equal(toolNames.includes("kb_get_result"), true);
    assert.equal(toolNames.includes("kb_get_claim"), true);
    assert.equal(toolNames.includes("kb_report_issue"), true);
    assert.equal(toolNames.includes("kb_outcome"), true);
    assert.equal(toolNames.includes("kb_compare_retrieval"), true);
    assert.equal(toolNames.includes("kb_submit_retrieval_comparison"), true);
    assert.equal(toolNames.includes("kb_diff_lava_context"), true);
    assert.equal(toolNames.includes("kb_verify_lava_context"), true);
    assert.equal(toolNames.includes("kb_get_freshness"), true);
    assert.equal(toolsResponse.result.tools.find((tool) => tool.name === "kb_search").annotations.readOnlyHint, true);
    assert.equal(toolsResponse.result.tools.find((tool) => tool.name === "kb_submit").annotations.readOnlyHint, false);
    assert.equal(toolsResponse.result.tools.find((tool) => tool.name === "kb_compare_retrieval").annotations.readOnlyHint, false);

    const callResponse = await mcp(mf, "tools/call", { name: "kb_get_claim", arguments: { claim_id: "claim:abc123" } });
    const callResult = JSON.parse(callResponse.result.content[0].text);
    assert.equal(callResult.claim.claim_id, "claim:abc123");
    assert.equal(callResponse.result.structuredContent.claim.claim_id, "claim:abc123");
  } finally {
    await mf.dispose();
  }
});

test("claim listing is paginated, validates tier vocabularies, and supports the authority alias", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const extraRows = [
      {
        id: "claim:claim:official-second",
        kind: "claim",
        title: "Second official check-in claim",
        body: "A second source-backed check-in claim.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/second",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({ claim_id: "claim:official-second", version_scope_status: "unprocessed" }),
      },
      {
        id: "claim:claim:routing-only",
        kind: "claim",
        title: "Routing-only check-in source",
        body: "Use this only to route an agent to a training source.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/routing",
        concept: "check-in",
        authority_tier: "rocku-confirmed",
        claim_tier: "routing_context_only",
        claim_tier_rank: 0,
        source_id: "rock_rocku",
        payload_json: JSON.stringify({ claim_id: "claim:routing-only", version_scope_status: "unprocessed" }),
      },
    ];
    for (const row of extraRows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
      await db.prepare("INSERT INTO search_row_concepts (row_id, concept) VALUES (?, ?)")
        .bind(row.id, row.concept).run();
    }

    const pageResponse = await mf.dispatchFetch("https://kb.example.test/claims/check-in?tier=official&limit=1");
    const page = await pageResponse.json();
    assert.equal(pageResponse.status, 200);
    assert.equal(page.schema, "rock-kb-claims-result-v2");
    assert.equal(page.count, 1);
    assert.equal(page.total_count, 2);
    assert.equal(page.has_more, true);
    assert.equal(page.next_offset, 1);
    assert.equal(page.filters.authority_tier, "official");

    const secondPage = await (await mf.dispatchFetch("https://kb.example.test/claims/check-in?authority_tier=official&limit=1&offset=1")).json();
    assert.equal(secondPage.count, 1);
    assert.equal(secondPage.has_more, false);

    const defaultPage = await (await mf.dispatchFetch("https://kb.example.test/claims/check-in?limit=10")).json();
    assert.equal(defaultPage.total_count, 2);
    assert.equal(defaultPage.claims.some((row) => row.claim_id === "claim:routing-only"), false);

    const routingPage = await (await mf.dispatchFetch("https://kb.example.test/claims/check-in?min_claim_tier=routing_context_only&limit=10")).json();
    assert.equal(routingPage.total_count, 3);

    const invalidResponse = await mf.dispatchFetch("https://kb.example.test/claims/check-in?tier=not-a-tier");
    const invalid = await invalidResponse.json();
    assert.equal(invalidResponse.status, 400);
    assert.equal(invalid.status, "rejected");
    assert.equal(invalid.error_code, "invalid_tier");
    assert.ok(invalid.valid_values.includes("official"));

    const mcpResponse = await mcp(mf, "tools/call", {
      name: "kb_get_claims",
      arguments: { concept_id: "check-in", authority_tier: "official", limit: 1 },
    });
    assert.equal(mcpResponse.result.structuredContent.total_count, 2);
    assert.equal(mcpResponse.result.structuredContent.count, 1);
  } finally {
    await mf.dispose();
  }
});

test("symptom search routes to task cards and troubleshooting nodes before field references", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const guidanceRows = [
      {
        id: "task_card:check-in:diagnose-labels-not-printing",
        kind: "task_card",
        title: "Diagnose Labels Not Printing",
        body: "Find whether check-in labels are not printing because of network printer routing, device configuration, printer hardware, or attendance state.",
        path: "knowledge/concepts/check-in/tasks/diagnose-labels-not-printing.md",
        url: "https://example.test/check-in",
        concept: "check-in",
        authority_tier: "community-reviewed",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({ concept_id: "check-in", task_id: "diagnose-labels-not-printing", version_scope_status: "unprocessed" }),
      },
      {
        id: "troubleshooting_node:check-in:diagnose-labels-not-printing",
        kind: "troubleshooting_node",
        title: "Diagnose Labels Not Printing",
        body: "When a network printer does not print a check-in label, inspect printer routing and whether attendance saved.",
        path: "knowledge/concepts/check-in/troubleshooting-tree.json",
        url: "https://example.test/check-in",
        concept: "check-in",
        authority_tier: "community-reviewed",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({ concept_id: "check-in", id: "diagnose-labels-not-printing", version_scope_status: "unprocessed" }),
      },
    ];
    for (const row of guidanceRows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
    }

    const query = encodeURIComponent("check-in labels not printing to network printer");
    const response = await mf.dispatchFetch(`https://kb.example.test/search?q=${query}&limit=5`);
    const payload = await response.json();
    assert.equal(payload.intent, "symptom");
    assert.equal(payload.results[0].kind, "task_card");
    assert.equal(payload.results[0].intent, "symptom");
    assert.ok(payload.results.slice(0, 3).some((row) => row.kind === "task_card"));

    const taskOnly = await (await mf.dispatchFetch(`https://kb.example.test/search?q=${query}&kind=task_card`)).json();
    assert.equal(taskOnly.results[0].kind, "task_card");
    const nodeOnly = await (await mf.dispatchFetch(`https://kb.example.test/search?q=${query}&kind=troubleshooting_node`)).json();
    assert.equal(nodeOnly.results[0].kind, "troubleshooting_node");
  } finally {
    await mf.dispose();
  }
});

test("Rock version filtering excludes conflicting scoped rows and labels uncertain rows", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const rows = [
      {
        id: "claim:claim:version-probe-18",
        kind: "claim",
        title: "Version filter probe for Rock 18",
        body: "Version filter probe behavior for Rock 18.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/version-18",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({
          claim_id: "claim:version-probe-18",
          rock_versions: ["18.0+"],
          version_scope_status: "scoped",
        }),
      },
      {
        id: "claim:claim:version-probe-19",
        kind: "claim",
        title: "Version filter probe for Rock 19",
        body: "Version filter probe behavior for Rock 19.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/version-19",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({
          claim_id: "claim:version-probe-19",
          rock_versions: ["19.0"],
          version_scope_status: "scoped",
        }),
      },
      {
        id: "claim:claim:version-probe-unprocessed",
        kind: "claim",
        title: "Version filter probe with unprocessed scope",
        body: "Version filter probe behavior with unknown version scope.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/version-unknown",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({
          claim_id: "claim:version-probe-unprocessed",
          rock_versions: [],
          version_scope_status: "unprocessed",
        }),
      },
      {
        id: "source-native:structured_reference:nested-version-probe",
        kind: "structured_reference",
        title: "Nested verification version probe",
        body: "Nested verification version probe for a corrected property interface.",
        path: "shadow/canonical/structured_reference.jsonl",
        url: "https://example.test/nested-version",
        concept: "obsidian-development",
        authority_tier: "source-code-confirmed",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "sparkdevnetwork_rock",
        payload_json: JSON.stringify({
          artifact: {
            rock_versions: [],
            version_scope_status: "unprocessed",
          },
          verification: {
            resolutions: [{
              rock_versions: ["19.4"],
              version_scope_status: "scoped",
            }],
          },
        }),
      },
    ];
    for (const row of rows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
      await db.prepare("INSERT INTO search_row_concepts (row_id, concept) VALUES (?, ?)")
        .bind(row.id, row.concept).run();
    }

    const response = await mf.dispatchFetch(
      "https://kb.example.test/search?q=version%20filter%20probe&rock_version=18.2&limit=10",
    );
    const payload = await response.json();
    const byId = new Map(payload.results.map((row) => [row.id, row]));
    assert.equal(byId.has("claim:claim:version-probe-18"), true);
    assert.equal(byId.has("claim:claim:version-probe-19"), false);
    assert.equal(byId.has("claim:claim:version-probe-unprocessed"), true);
    assert.equal(byId.get("claim:claim:version-probe-18").version_match, "matched");
    assert.equal(byId.get("claim:claim:version-probe-unprocessed").version_match, "unprocessed");

    const nestedMatch = await (await mf.dispatchFetch(
      "https://kb.example.test/search?q=nested%20verification%20version%20probe&rock_version=19.4&limit=10",
    )).json();
    assert.equal(
      nestedMatch.results.some((row) => row.id === "source-native:structured_reference:nested-version-probe"),
      true,
    );
    const nestedMismatch = await (await mf.dispatchFetch(
      "https://kb.example.test/search?q=nested%20verification%20version%20probe&rock_version=20&limit=10",
    )).json();
    assert.equal(
      nestedMismatch.results.some((row) => row.id === "source-native:structured_reference:nested-version-probe"),
      false,
    );

    const claimsResponse = await mf.dispatchFetch(
      "https://kb.example.test/claims/check-in?authority_tier=official&rock_version=18.2&limit=100",
    );
    const claimsPayload = await claimsResponse.json();
    const claimIds = new Set(claimsPayload.claims.map((row) => row.claim_id));
    assert.equal(claimIds.has("claim:version-probe-18"), true);
    assert.equal(claimIds.has("claim:version-probe-19"), false);
    assert.equal(claimIds.has("claim:version-probe-unprocessed"), true);

    const invalidResponse = await mf.dispatchFetch(
      "https://kb.example.test/search?q=labels&min_claim_tier=official",
    );
    const invalid = await invalidResponse.json();
    assert.equal(invalidResponse.status, 400);
    assert.equal(invalid.error_code, "invalid_min_claim_tier");
    assert.ok(invalid.valid_values.includes("source_backed"));
  } finally {
    await mf.dispose();
  }
});

test("direct MCP serves stateless 2026 clients through the official SDK", async () => {
  const mf = await buildWorker();
  const client = new Client(
    { name: "rock-kb-sdk-test", version: "1.0.0" },
    { versionNegotiation: { mode: { pin: "2026-07-28" } } },
  );
  try {
    const discovered = await modernMcp(mf, "server/discover", {});
    assert.equal(discovered.status, 200);
    assert.equal(discovered.headers.get("mcp-session-id"), null);
    assert.equal(discovered.payload.result.supportedVersions.includes("2026-07-28"), true);
    assert.equal(discovered.payload.result.capabilities.tools !== undefined, true);
    assert.equal(
      discovered.payload.result._meta["io.modelcontextprotocol/serverInfo"].name,
      "Rock KB",
    );
    assert.equal(discovered.payload.result.ttlMs, 3_600_000);
    assert.equal(discovered.payload.result.cacheScope, "public");

    const listed = await modernMcp(mf, "tools/list", {});
    assert.equal(listed.status, 200);
    assert.equal(listed.payload.result.tools.length, 35);
    assert.equal(listed.payload.result.ttlMs, 3_600_000);
    assert.equal(listed.payload.result.cacheScope, "public");

    const transport = new StreamableHTTPClientTransport(
      new URL("https://kb.example.test/mcp"),
      { fetch: (input, init) => mf.dispatchFetch(input, init) },
    );
    await client.connect(transport);
    const sdkTools = await client.listTools();
    assert.equal(sdkTools.tools.length, 35);
    const sdkResult = await client.callTool({
      name: "kb_get_claim",
      arguments: { claim_id: "claim:abc123" },
    });
    assert.equal(sdkResult.structuredContent.claim.claim_id, "claim:abc123");
  } finally {
    await client.close();
    await mf.dispose();
  }
});

test("direct MCP enforces modern headers, browser origins, and legacy compatibility", async () => {
  const mf = await buildWorker();
  try {
    const mismatch = await mf.dispatchFetch("https://kb.example.test/mcp", {
      method: "POST",
      headers: modernMcpHeaders("tools/list"),
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 1,
        method: "tools/list",
        params: {
          _meta: modernMcpMeta("2099-01-01"),
        },
      }),
    });
    const mismatchPayload = await mismatch.json();
    assert.equal(mismatch.status, 400);
    assert.equal(mismatchPayload.error.code, -32020);

    const unsupported = await modernMcp(mf, "tools/list", {}, {}, "2099-01-01");
    assert.equal(unsupported.status, 400);
    assert.equal(unsupported.payload.error.code, -32022);
    assert.equal(unsupported.payload.error.data.requested, "2099-01-01");
    assert.equal(unsupported.payload.error.data.supported.includes("2026-07-28"), true);

    const unknown = await modernMcp(mf, "unknown/method", {});
    assert.equal(unknown.status, 404);
    assert.equal(unknown.payload.error.code, -32601);

    const trustedPreflight = await mf.dispatchFetch("https://kb.example.test/mcp", {
      method: "OPTIONS",
      headers: {
        origin: "https://kb.example.test",
        "access-control-request-method": "POST",
        "access-control-request-headers": "content-type,mcp-protocol-version,mcp-method,mcp-name",
      },
    });
    assert.equal(trustedPreflight.status, 200);
    assert.match(trustedPreflight.headers.get("access-control-allow-headers"), /MCP-Protocol-Version/i);
    assert.match(trustedPreflight.headers.get("access-control-allow-headers"), /Mcp-Method/i);

    const untrustedPreflight = await mf.dispatchFetch("https://kb.example.test/mcp", {
      method: "OPTIONS",
      headers: {
        origin: "https://untrusted.example",
        "access-control-request-method": "POST",
      },
    });
    assert.equal(untrustedPreflight.status, 403);

    const initialized = await legacyDirectMcp(mf, "initialize", {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: { name: "rock-kb-legacy-test", version: "1.0.0" },
    });
    assert.equal(initialized.status, 200);
    assert.equal(initialized.payload.result.protocolVersion, "2025-11-25");
    assert.equal(initialized.headers.get("mcp-session-id"), null);

    const legacyTools = await legacyDirectMcp(mf, "tools/list", {});
    assert.equal(legacyTools.status, 200);
    assert.equal(legacyTools.payload.result.tools.length, 35);
    assert.equal("ttlMs" in legacyTools.payload.result, false);

    const legacyCall = await legacyDirectMcp(mf, "tools/call", {
      name: "kb_get_claim",
      arguments: { claim_id: "claim:abc123" },
    });
    assert.equal(legacyCall.status, 200);
    assert.equal(legacyCall.payload.result.structuredContent.claim.claim_id, "claim:abc123");

    const legacyGet = await mf.dispatchFetch("https://kb.example.test/mcp", {
      method: "GET",
      headers: { "mcp-protocol-version": "2025-11-25" },
    });
    assert.equal(legacyGet.status, 405);
  } finally {
    await mf.dispose();
  }
});

test("MCP transport telemetry is bounded, cohort-aware, and excludes request data", async () => {
  const mf = await buildWorker();
  const installationId = `rkbi_${"t".repeat(43)}`;
  const externalHeaders = {
    "x-rock-kb-client": "mcp",
    "x-rock-kb-cohort": "external-test",
    "x-rock-kb-installation-id": installationId,
    "user-agent": "private-agent-name/1.0",
  };
  const privateArgument = "sensitive-example-query-7429";
  try {
    await modernMcp(mf, "server/discover", {}, externalHeaders);
    await modernMcp(mf, "tools/list", {}, externalHeaders);
    await modernMcp(
      mf,
      "tools/call",
      { name: "kb_search", arguments: { query: privateArgument, limit: 2 } },
      externalHeaders,
    );

    const mismatch = await mf.dispatchFetch("https://kb.example.test/mcp", {
      method: "POST",
      headers: {
        ...modernMcpHeaders("tools/list"),
        ...externalHeaders,
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 1,
        method: "tools/list",
        params: {
          _meta: modernMcpMeta("2099-01-01"),
        },
      }),
    });
    assert.equal(mismatch.status, 400);

    await legacyDirectMcp(mf, "initialize", {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: { name: "private-legacy-agent", version: "1.0.0" },
    }, externalHeaders);
    await legacyDirectMcp(mf, "tools/list", {}, externalHeaders);
    const expectedSessionRejection = await mf.dispatchFetch("https://kb.example.test/mcp", {
      method: "GET",
      headers: {
        ...externalHeaders,
        "mcp-protocol-version": "2025-11-25",
      },
    });
    assert.equal(expectedSessionRejection.status, 405);

    const codeInitialized = await streamableMcp(
      mf,
      "initialize",
      {
        protocolVersion: "2025-11-25",
        capabilities: {},
        clientInfo: { name: "private-code-agent", version: "1.0.0" },
      },
      "",
      externalHeaders,
    );
    await streamableMcp(
      mf,
      "tools/list",
      {},
      codeInitialized.sessionId,
      externalHeaders,
    );

    await modernMcp(mf, "tools/list", {}, {
      "x-rock-kb-client": "mcp",
      "x-rock-kb-cohort": "maintainer",
    });

    const response = await mf.dispatchFetch("https://kb.example.test/telemetry/mcp-transport");
    assert.equal(response.status, 200);
    const transport = await response.json();
    assert.equal(transport.schema, "rock-kb-mcp-transport-summary-v1");
    assert.equal(transport.default_scope.maintainer_traffic_included, false);
    assert.equal(transport.summary.total_count, 9);
    assert.equal(transport.summary.success_count, 7);
    assert.equal(transport.summary.failure_count, 2);
    assert.equal(transport.summary.expected_stateless_rejection_count, 1);
    assert.equal(transport.summary.actionable_failure_count, 1);
    assert.equal(transport.summary.actionable_failure_rate, 0.111111);
    assert.equal(transport.summary.by_protocol_generation["2026"], 4);
    assert.equal(transport.summary.by_protocol_generation["2025"], 5);
    assert.equal(transport.summary.by_endpoint.direct, 7);
    assert.equal(transport.summary.by_endpoint.code, 2);
    assert.equal(transport.summary.by_operation_category.discover, 1);
    assert.equal(transport.summary.by_operation_category.initialize, 2);
    assert.equal(transport.summary.by_operation_category.tools_list, 4);
    assert.equal(transport.summary.by_operation_category.tool_call, 1);
    assert.equal(transport.summary.by_operation_category.session_operation, 1);
    assert.equal(transport.summary.by_http_status["200"], 7);
    assert.equal(transport.summary.by_http_status["400"], 1);
    assert.equal(transport.summary.by_http_status["405"], 1);
    assert.equal(transport.summary.by_error_code["mcp_-32020"], 1);
    assert.equal(transport.summary.tools_list_per_tool_call, 4);
    assert.equal(transport.summary.discover_per_tool_call, 1);
    assert.equal(transport.summary.response_size_coverage_rate, 0.555556);
    assert.equal(transport.summary.by_response_size_basis.estimated_payload, 3);
    assert.equal(transport.summary.by_response_size_basis.buffered_error, 2);
    assert.equal(transport.summary.by_response_size_basis.unmeasured, 4);
    assert.equal(transport.maintainer_summary.total_count, 1);
    assert.equal(transport.all_traffic_summary.total_count, 10);
    assert.deepEqual(transport.coverage.projection_versions, ["test-version"]);
    assert.equal(transport.rows.every((row) => row.projection_version === "test-version"), true);
    assert.equal(transport.interpretation.cache_hits_observable, false);
    assert.match(transport.interpretation.response_size_measure, /Successful response streams are not read or cloned/);
    assert.match(transport.interpretation.failure_classification, /actionable_failure_count excludes/);

    const serialized = JSON.stringify(transport);
    assert.equal(serialized.includes(privateArgument), false);
    assert.equal(serialized.includes(installationId), false);
    assert.equal(serialized.includes("private-agent-name"), false);
    assert.equal(serialized.includes("private-legacy-agent"), false);
    assert.equal(serialized.includes("private-code-agent"), false);
    assert.equal(serialized.includes("kb_search"), false);

    const telemetry = await (await mf.dispatchFetch("https://kb.example.test/telemetry/summary")).json();
    assert.equal(telemetry.mcp_transport.schema, "rock-kb-mcp-transport-summary-v1");
    const dashboard = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(dashboard.mcp_transport.schema, "rock-kb-mcp-transport-summary-v1");

    const db = await mf.getD1Database("KB_DB");
    const columns = await db.prepare("PRAGMA table_info(mcp_transport_events_v1)").all();
    const columnNames = columns.results.map((row) => row.name);
    assert.deepEqual(columnNames, [
      "day",
      "projection_version",
      "endpoint",
      "protocol_generation",
      "operation_category",
      "cohort",
      "http_status",
      "error_code",
      "latency_bucket",
      "response_size_bucket",
      "response_size_basis",
      "count",
    ]);
  } finally {
    await mf.dispose();
  }
});

test("experimental Code Mode MCP advertises one read-only composition tool", async () => {
  const mf = await buildWorker();
  try {
    const initialized = await streamableMcp(mf, "initialize", {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: { name: "rock-kb-test", version: "1.0.0" },
    });
    assert.equal(initialized.status, 200);
    assert.equal(initialized.payload.result.protocolVersion, "2025-11-25");

    const listed = await streamableMcp(mf, "tools/list", {}, initialized.sessionId);
    assert.equal(listed.status, 200);
    assert.deepEqual(listed.payload.result.tools.map((tool) => tool.name), ["code"]);
    assert.match(listed.payload.result.tools[0].description, /kb_search/);
    assert.equal(listed.payload.result.tools[0].description.includes("kb_submit("), false);
    assert.deepEqual(listed.payload.result.tools[0].annotations, {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    });

    const executed = await streamableMcp(
      mf,
      "tools/call",
      {
        name: "code",
        arguments: {
          code: "async () => { const claim = await codemode.kb_get_claim({ claim_id: 'claim:abc123' }); return { claim_id: claim.claim.claim_id }; }",
        },
      },
      listed.sessionId,
    );
    assert.equal(executed.status, 200);
    assert.notEqual(executed.payload.result.isError, true, JSON.stringify(executed.payload.result));
    assert.equal(JSON.parse(executed.payload.result.content[0].text).claim_id, "claim:abc123");
  } finally {
    await mf.dispose();
  }
});

test("health reports the active bounded artifact slot and artifact reads use it", async () => {
  const mf = await buildWorker({
    artifactPrefix: "slots/b",
    canonicalShadow: {
      status: "ready",
      contentHash: "a".repeat(64),
      searchRowCount: 14268,
      knowledgeUnitCount: 13704,
      artifactCount: 7,
      observationCount: 2,
    },
  });
  try {
    const healthResponse = await mf.dispatchFetch("https://kb.example.test/health");
    const health = await healthResponse.json();
    assert.equal(health.status, "ok");
    assert.equal(health.retrieval_projection, "legacy");
    assert.equal(health.retrieval_projection_version, "test-version");
    assert.equal(health.artifact_prefix, "slots/b");
    assert.equal(health.artifact_storage, "bounded_two_slot");
    assert.deepEqual(health.canonical_shadow, {
      status: "ready",
      mode: "dual_projection_runtime_switch",
      activation_supported: true,
      activation_control: "kb_meta.active_retrieval_projection",
      supported_retrieval_projections: ["legacy", "canonical", "canonical-canary"],
      rollback_projection: "legacy",
      active_reader: false,
      active_retrieval_projection: "legacy",
      active_retrieval_projection_configuration_status: "valid",
      canary_reader_available: true,
      canary_retrieval_projection: "canonical-canary",
      canary_requires_opt_in: true,
      canary_cohorts: ["external-test", "maintainer"],
      content_hash: "a".repeat(64),
      search_row_count: 14268,
      knowledge_unit_count: 13704,
      artifact_count: 7,
      observation_count: 2,
    });
    assert.equal(health.skill_manifest_url, "https://kb.example.test/skill/manifest.json");

    const skillManifestResponse = await mf.dispatchFetch("https://kb.example.test/skill/manifest.json");
    const skillManifest = await skillManifestResponse.json();
    assert.equal(skillManifest.schema, "rock-kb-skill-manifest-v1");
    assert.equal(skillManifest.skill_version, "1.0.0");
    assert.equal(skillManifest.sha256, SKILL_FIXTURE_SHA);
    assert.equal(skillManifest.source_url, "https://kb.example.test/artifacts/skills/rock-kb-agent/SKILL.md");

    const toolsResponse = await mcp(mf, "tools/list", {});
    assert.equal(toolsResponse.result.tools.some((tool) => tool.name === "kb_skill_manifest"), true);
    const skillToolResponse = await mcp(mf, "tools/call", { name: "kb_skill_manifest", arguments: {} });
    assert.equal(JSON.parse(skillToolResponse.result.content[0].text).sha256, SKILL_FIXTURE_SHA);

    const recipeResponse = await mf.dispatchFetch("https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard");
    assert.equal(recipeResponse.status, 200);
    assert.equal((await recipeResponse.json()).status, "ok");
  } finally {
    await mf.dispose();
  }
});

test("exact concept routing injects authored answers outside the FTS candidate set", async () => {
  const mf = await buildWorker();
  try {
    const response = await mf.dispatchFetch("https://kb.example.test/search?q=What%20should%20I%20check%20first%20when%20troubleshooting%20Workflows%3F&limit=5");
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.results[0].id, "answer:answer:workflows:first-checks");
    assert.equal(payload.results[0].concept, "workflows");
  } finally {
    await mf.dispose();
  }
});

test("search normalizes model intent, plurals, and common check-in misspellings", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    await db.prepare(`INSERT INTO search_rows
      (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(
      "concept:groups",
      "concept",
      "Groups",
      "Groups, group types, members, attendance, and placement.",
      "knowledge/concepts/groups/index.md",
      "",
      "groups",
      "official",
      "answer_pack_approved",
      2,
      "",
      "{}",
    ).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind("concept:groups", "Groups", "Groups, group types, members, attendance, and placement.", "groups").run();

    const broadResponse = await mf.dispatchFetch("https://kb.example.test/search?q=groups&limit=3");
    const broadPayload = await broadResponse.json();
    assert.equal(broadPayload.results[0].id, "concept:groups");

    const modelResponse = await mf.dispatchFetch("https://kb.example.test/search?q=In%20the%20Group%20model%20show%20the%20Members%20property&limit=3");
    const modelPayload = await modelResponse.json();
    assert.equal(modelPayload.results[0].id, "model_map:stable:group");

    const slugResponse = await mf.dispatchFetch("https://kb.example.test/search?q=What%20is%20the%20exact%20model%20slug%20for%20Group%2C%20and%20what%20relationships%20does%20it%20expose%3F&limit=3");
    const slugPayload = await slugResponse.json();
    assert.equal(slugPayload.results[0].id, "model_map:stable:group");

    const typoResponse = await mf.dispatchFetch("https://kb.example.test/search?q=child%20eligable%20but%20not%20avalable%20at%20checkin&limit=3");
    const typoPayload = await typoResponse.json();
    assert.equal(typoPayload.results[0].concept, "check-in");
    assert.match(typoPayload.results[0].snippet, /eligibility/i);
  } finally {
    await mf.dispose();
  }
});

test("search uses the declared default limit when the parameter is omitted", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    for (let index = 0; index < 2; index += 1) {
      const id = `claim:limit-probe-${index}:check-in`;
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, 'claim', 'Limit probe', 'Limit probe result', 'claims/approved-claims.jsonl', '', 'check-in', 'official', 'source_backed', 1, '', '{}')`)
        .bind(id).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, 'Limit probe', 'Limit probe result', 'check-in')")
        .bind(id).run();
    }

    const response = await mf.dispatchFetch("https://kb.example.test/search?q=limit%20probe&kind=claim");
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.results.length, 2);
  } finally {
    await mf.dispose();
  }
});

test("recipe routes and MCP tools return the structured recipe", async () => {
  const mf = await buildWorker();
  try {
    const listResponse = await mf.dispatchFetch("https://kb.example.test/recipes?concept=check-in");
    const list = await listResponse.json();
    assert.equal(listResponse.status, 200);
    assert.equal(list.count, 1);
    assert.equal(list.recipes[0].recipe_id, "oneall:check-in-status-dashboard");

    const getResponse = await mf.dispatchFetch("https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard");
    const result = await getResponse.json();
    assert.equal(result.status, "ok");
    assert.equal(result.recipe.security.data_access, "read_only");
    assert.equal(result.recipe.implementation.commit_sha.length, 40);

    const searchResponse = await mf.dispatchFetch("https://kb.example.test/search?q=registration%20attendance%20dashboard&kind=recipe");
    const search = await searchResponse.json();
    assert.equal(search.kind, "recipe");
    assert.equal(search.results.length, 1);
    assert.equal(search.results[0].kind, "recipe");
    assert.equal(search.results[0].id, "recipe:oneall:check-in-status-dashboard");
    assert.deepEqual(search.results[0].rock_versions, ["18"]);

    const toolsResponse = await mcp(mf, "tools/list", {});
    const toolNames = toolsResponse.result.tools.map((tool) => tool.name);
    assert.equal(toolNames.includes("kb_list_recipes"), true);
    assert.equal(toolNames.includes("kb_get_recipe"), true);
    assert.equal(toolNames.includes("kb_verify_recipe"), true);

    const callResponse = await mcp(mf, "tools/call", { name: "kb_get_recipe", arguments: { recipe_id: "oneall:check-in-status-dashboard" } });
    const callResult = JSON.parse(callResponse.result.content[0].text);
    assert.equal(callResult.recipe.recipe_id, "oneall:check-in-status-dashboard");

    const missingVerifyResponse = await mf.dispatchFetch("https://kb.example.test/recipes/missing%3Arecipe/verify?rock_version=18");
    assert.equal(missingVerifyResponse.status, 404);
  } finally {
    await mf.dispose();
  }
});

test("Lava context REST and MCP tools return exact grouped surfaces", async () => {
  const mf = await buildWorker();
  try {
    const listResponse = await mf.dispatchFetch("https://kb.example.test/lava-contexts?family=check-in-label");
    const listed = await listResponse.json();
    assert.equal(listResponse.status, 200);
    assert.equal(listed.count, 2);
    assert.deepEqual(
      listed.surfaces.map((surface) => surface.context_id),
      ["check-in-label-checkout-dynamic-text", "check-in-label-family-dynamic-text"],
    );

    const getResponse = await mf.dispatchFetch(
      "https://kb.example.test/lava-contexts/check-in-label-checkout-dynamic-text?root=CheckoutDateTime",
    );
    const exact = await getResponse.json();
    assert.equal(getResponse.status, 200);
    assert.equal(exact.status, "ok");
    assert.equal(exact.root_count, 1);
    assert.equal(exact.roots[0].root_key, "CheckoutDateTime");
    assert.equal(exact.roots.some((root) => root.root_key === "Family"), false);
    assert.equal(exact.surface.source_version, "20.0.5");

    const versionedResponse = await mf.dispatchFetch(
      "https://kb.example.test/lava-contexts/check-in-label-checkout-dynamic-text?root=CheckoutDateTime&rock_version=19.0",
    );
    const versioned = await versionedResponse.json();
    assert.equal(versioned.surface.selected_rock_version, "19.0.11");
    assert.equal(versioned.roots[0].source_ref, "release-19.0");

    const diffResponse = await mf.dispatchFetch(
      "https://kb.example.test/lava-contexts/diff?from=19.0&to=20&context=check-in-label-family-dynamic-text",
    );
    const diff = await diffResponse.json();
    assert.equal(diff.count, 1);
    assert.equal(diff.changes[0].change_type, "added");

    const toolResponse = await mcp(mf, "tools/call", {
      name: "kb_get_lava_context",
      arguments: { context_id: "check-in-label-family-dynamic-text", root_key: "Family" },
    });
    const toolResult = JSON.parse(toolResponse.result.content[0].text);
    assert.equal(toolResult.status, "ok");
    assert.equal(toolResult.roots[0].root_key, "Family");
    assert.equal(toolResult.roots.some((root) => root.root_key === "CheckoutDateTime"), false);
  } finally {
    await mf.dispose();
  }
});

test("Lava context verification stores only bounded availability outcomes", async () => {
  const mf = await buildWorker();
  try {
    const headers = {
      "content-type": "application/json",
      "x-rock-kb-installation-id": `rkbi_${"l".repeat(40)}`,
      "x-rock-kb-cohort": "external-test",
    };
    const response = await mf.dispatchFetch("https://kb.example.test/lava-contexts/verification", {
      method: "POST",
      headers,
      body: JSON.stringify({
        context_id: "check-in-label-checkout-dynamic-text",
        root_key: "CheckoutDateTime",
        rock_version: "19.0.11",
        observation: "present",
        consent_attested: true,
      }),
    });
    const result = await response.json();
    assert.equal(response.status, 201);
    assert.equal(result.status, "recorded");
    assert.match(result.verification_id, /^kblv_/);

    const rejected = await mf.dispatchFetch("https://kb.example.test/lava-contexts/verification", {
      method: "POST",
      headers,
      body: JSON.stringify({
        context_id: "check-in-label-checkout-dynamic-text",
        root_key: "CheckoutDateTime",
        rock_version: "19.0.11",
        observation: "present",
        value: "private",
        consent_attested: true,
      }),
    });
    assert.equal(rejected.status, 400);
    assert.equal((await rejected.json()).error_code, "unsupported_fields");

    const dashboard = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(dashboard.field_validation.lava_context_verifications.by_observation.present, 1);
  } finally {
    await mf.dispose();
  }
});

test("search collapses concept-specific rows for one canonical recipe", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const recipe = {
      recipe_id: "oneall:check-in-status-dashboard",
      title: "Check-In Status Dashboard",
    };
    const duplicate = {
      id: "recipe:oneall:check-in-status-dashboard:event-registration",
      kind: "recipe",
      title: "Check-In Status Dashboard",
      body: "Reusable registration roster and latest attendance dashboard implementation.",
      path: "knowledge/recipes/oneall/check-in-status-dashboard.md",
      url: "https://github.com/ONE-ALL-Church/RockRMS-OA-Public",
      concept: "event-registration",
      authority_tier: "community-reviewed",
      claim_tier: "answer_pack_approved",
      claim_tier_rank: 2,
      source_id: "oneall",
      payload_json: JSON.stringify(recipe),
    };
    await db.prepare(`INSERT INTO search_rows
      (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(duplicate)).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind(duplicate.id, duplicate.title, duplicate.body, duplicate.concept).run();

    const response = await mf.dispatchFetch(
      "https://kb.example.test/search?q=registration%20attendance%20dashboard&kind=recipe&limit=10"
    );
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.results.length, 1);
    assert.equal(payload.results[0].id, "recipe:oneall:check-in-status-dashboard");
  } finally {
    await mf.dispose();
  }
});

test("search collapses nested Lava paths for the same context root", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const contexts = [
      ["c845dbbf", "", "List<LabelAttendanceDetail>"],
      ["4c7b56b3", "PersonAttendance.SecurityCode", "LabelAttendanceDetail"],
      ["b8109564", "PersonAttendance.IsFirstTime", "LabelAttendanceDetail"],
    ];
    for (const [suffix, nestedPath, rootType] of contexts) {
      const row = {
        id: `lava_context:check-in-label-person-dynamic-text:personattendance:${suffix}`,
        kind: "lava_context",
        title: "Check-In Label Designer Person Dynamic Text - PersonAttendance",
        body: `Check-In Label Designer Lava root PersonAttendance ${nestedPath}`,
        path: "agent/lava-contexts.jsonl",
        url: "https://example.test/lava-context",
        concept: "lava",
        authority_tier: "source-code-confirmed",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "sparkdevnetwork_rock",
        payload_json: JSON.stringify({
          context_id: "check-in-label-person-dynamic-text",
          root_key: "PersonAttendance",
          nested_path: nestedPath,
          root_type: rootType,
        }),
      };
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
    }

    const response = await mf.dispatchFetch("https://kb.example.test/search?q=Check-In%20Label%20Designer%20PersonAttendance%20Lava%20roots&limit=5");
    const payload = await response.json();
    const personAttendanceRows = payload.results.filter((row) => row.id.includes(":personattendance:"));

    assert.equal(response.status, 200);
    assert.equal(personAttendanceRows.length, 1);
  } finally {
    await mf.dispose();
  }
});

test("Rock issue REST and MCP surfaces keep reports separate and assess versions conservatively", async () => {
  const mf = await buildWorker();
  try {
    const generalResponse = await mf.dispatchFetch("https://kb.example.test/search?q=Azure%20blob%20CPU&limit=5");
    const general = await generalResponse.json();
    assert.equal(general.results.some((row) => row.kind === "rock_issue"), false);

    const searchResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/search?q=Azure%20blob%20CPU%20issue&limit=5");
    const search = await searchResponse.json();
    assert.equal(search.results[0].id, "rock_issue:SparkDevNetwork/Rock#6919");

    const missingExactResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/search?q=Rock%20issue%20%23999999999&limit=5");
    const missingExact = await missingExactResponse.json();
    assert.equal(missingExactResponse.status, 200);
    assert.deepEqual(missingExact.results, []);

    const missingGeneralResponse = await mf.dispatchFetch("https://kb.example.test/search?q=Rock%20issue%20%23999999999&limit=5&min_tier=routing_context_only");
    const missingGeneral = await missingGeneralResponse.json();
    assert.equal(missingGeneralResponse.status, 200);
    assert.deepEqual(missingGeneral.results, []);

    const missingDescriptiveResponse = await mf.dispatchFetch("https://kb.example.test/search?q=Does%20Rock%20issue%20%23999999999%20affect%20Azure%3F&limit=5&min_tier=routing_context_only");
    const missingDescriptive = await missingDescriptiveResponse.json();
    assert.equal(missingDescriptive.results.some((row) => row.kind === "rock_issue"), false);

    const versionSearchResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/search?q=issue%2019.2%20Azure%20Blob%20CPU&limit=5");
    const versionSearch = await versionSearchResponse.json();
    assert.equal(versionSearch.results[0].id, "rock_issue:SparkDevNetwork/Rock#6919");

    const openSearch = await (await mf.dispatchFetch(
      "https://kb.example.test/rock-issues/search?q=open%20Azure%20Blob%20CPU%20issue&limit=5",
    )).json();
    assert.equal(openSearch.results[0].id, "rock_issue:SparkDevNetwork/Rock#6919");
    const closedSearch = await (await mf.dispatchFetch(
      "https://kb.example.test/rock-issues/search?q=closed%20Azure%20Blob%20CPU%20issue&limit=5",
    )).json();
    assert.deepEqual(closedSearch.results, []);
    const criticalSearch = await (await mf.dispatchFetch(
      "https://kb.example.test/rock-issues/search?q=critical%20open%20Azure%20Blob%20CPU%20issue&limit=5",
    )).json();
    assert.deepEqual(criticalSearch.results, []);

    const getResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/6919");
    const get = await getResponse.json();
    assert.equal(get.status, "ok");
    assert.equal(get.issue.body, undefined);
    assert.equal(get.issue.version_evidence[0].normalized_version, "19.2.0");
    assert.equal(get.issue.reviewed_enrichments.length, 2);
    assert.equal(get.relationships[0].source_id, "rock_idea:2250");
    assert.equal(get.relationships[0].direction, "inbound");

    const aliasResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/6000");
    const alias = await aliasResponse.json();
    assert.equal(alias.status, "ok");
    assert.equal(alias.requested_issue_id, "rock_issue:SparkDevNetwork/Rock#6000");
    assert.equal(alias.issue_id, "rock_issue:SparkDevNetwork/Rock#6919");

    const listResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues?repository=core&version=19.2&limit=10");
    const list = await listResponse.json();
    assert.equal(list.count, 1);

    const assessResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile: { core_version: "19.2.0", concepts: ["hosting-infrastructure"] }, limit: 10 }),
    });
    const assessment = await assessResponse.json();
    assert.equal(assessment.count, 1);
    assert.equal(assessment.total_count, 1);
    assert.equal(assessment.offset, 0);
    assert.equal(assessment.has_more, false);
    assert.equal(assessment.next_offset, null);
    assert.equal(assessment.schema, "rock-kb-rock-issue-assessment-v2");
    assert.equal(assessment.scope, "open");
    assert.deepEqual(assessment.population_by_state, { open: 1 });
    assert.equal(typeof assessment.projection_version, "string");
    assert.equal(assessment.results[0].applicability, "possible");
    assert.equal(assessment.results[0].risk.level, "high");
    assert.equal(assessment.results[0].risk.source, "reviewed_enrichment");
    assert.equal(assessment.results[0].requirement_evaluation[0].status, "unknown");
    assert.equal(assessment.results[0].live_verification.playbook_available, true);
    assert.equal(assessment.catalog.status, "not_recorded");
    assert.equal(assessment.catalog.freshness_authority, "hosted_source_operations");
    assert.equal(assessment.results[0].needs_live_verification, true);
    assert.deepEqual(assessment.results[0].revalidation_due_enrichment_ids, ["rock_issue_enrichment:fixture-6919-stale-v1"]);

    const reviewedAssessResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        profile: {
          core_version: "19.3.1",
          concepts: ["hosting-infrastructure"],
          capabilities: ["azure-blob-storage"],
        },
        limit: 10,
      }),
    });
    const reviewedAssessment = await reviewedAssessResponse.json();
    assert.equal(reviewedAssessment.results[0].applicability, "confirmed");
    assert.deepEqual(reviewedAssessment.results[0].reviewed_assertion_ids, ["fixture-affected-19.3.1"]);

    const excludedAssessResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        profile: {
          core_version: "19.3.1",
          concepts: ["hosting-infrastructure"],
          capabilities: ["local-file-storage"],
        },
        limit: 10,
      }),
    });
    const excludedAssessment = await excludedAssessResponse.json();
    assert.equal(excludedAssessment.total_count, 0);
    assert.equal(excludedAssessment.exclusion_summary.count, 1);
    assert.equal(excludedAssessment.exclusion_summary.by_basis["profile_requirement:contains_all"], 1);

    const db = await mf.getD1Database("KB_DB");
    const closedIssue = {
      ...get.issue,
      issue_id: "rock_issue:SparkDevNetwork/Rock#6929",
      github_node_id: "I_fixture_6929",
      number: 6929,
      title: "Historical Azure Blob Storage fixture",
      url: "https://github.com/SparkDevNetwork/Rock/issues/6929",
      state: "closed",
      reviewed_enrichments: [],
    };
    await db.prepare("INSERT INTO rock_issues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(closedIssue.issue_id, closedIssue.github_node_id, closedIssue.repository, closedIssue.number, closedIssue.component,
        closedIssue.state, closedIssue.validation_state, closedIssue.title, closedIssue.url, closedIssue.updated_at,
        closedIssue.evidence_state, JSON.stringify(closedIssue)).run();
    await db.prepare("INSERT INTO rock_issue_versions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(closedIssue.issue_id, "rock_core", "reported_affected", "19.2.0", "19.2", "issue_form",
        "community-unreviewed", "medium", "section:rock version", "").run();
    const staleEnrichment = {
      ...get.issue.reviewed_enrichments[1],
      enrichment_id: "rock_issue_enrichment:fixture-6930-stale-v1",
      issue_id: "rock_issue:SparkDevNetwork/Rock#6930",
    };
    const staleOnlyIssue = {
      ...get.issue,
      issue_id: staleEnrichment.issue_id,
      github_node_id: "I_fixture_6930",
      number: 6930,
      title: "Stale enrichment only fixture",
      url: "https://github.com/SparkDevNetwork/Rock/issues/6930",
      state: "closed",
      version_evidence: [],
      reviewed_enrichments: [staleEnrichment],
    };
    await db.prepare("INSERT INTO rock_issues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(staleOnlyIssue.issue_id, staleOnlyIssue.github_node_id, staleOnlyIssue.repository, staleOnlyIssue.number,
        staleOnlyIssue.component, staleOnlyIssue.state, staleOnlyIssue.validation_state, staleOnlyIssue.title,
        staleOnlyIssue.url, staleOnlyIssue.updated_at, staleOnlyIssue.evidence_state, JSON.stringify(staleOnlyIssue)).run();
    await db.prepare("INSERT INTO rock_issue_enrichments VALUES (?, ?, ?, ?, ?)")
      .bind(staleEnrichment.enrichment_id, staleOnlyIssue.issue_id, staleEnrichment.diagnosis_status,
        staleEnrichment.reviewed_at, JSON.stringify(staleEnrichment)).run();
    const historicalResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        profile: { core_version: "19.2.0", concepts: ["hosting-infrastructure"] },
        scope: "historical-unresolved",
        limit: 10,
      }),
    });
    const historical = await historicalResponse.json();
    assert.equal(historical.scope, "historical-unresolved");
    assert.deepEqual(historical.population_by_state, { closed: 1 });
    assert.deepEqual(historical.results.map((row) => row.issue_id), [closedIssue.issue_id]);

    const allRelevantResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        profile: { core_version: "19.2.0", concepts: ["hosting-infrastructure"] },
        scope: "all-relevant",
        limit: 10,
      }),
    });
    const allRelevant = await allRelevantResponse.json();
    assert.deepEqual(allRelevant.population_by_state, { open: 1, closed: 1 });
    assert.equal(allRelevant.total_count, 2);

    const tools = await mcp(mf, "tools/list", {});
    const names = tools.result.tools.map((tool) => tool.name);
    assert.equal(names.includes("kb_search_rock_issues"), true);
    assert.equal(names.includes("kb_assess_rock_issues"), true);
    assert.equal(names.includes("kb_plan_rock_issue_investigation"), true);
    const assessTool = tools.result.tools.find((tool) => tool.name === "kb_assess_rock_issues");
    assert.equal(assessTool.inputSchema.properties.offset.minimum, 0);
    assert.deepEqual(assessTool.inputSchema.properties.scope.enum, ["open", "historical-unresolved", "all-relevant"]);
    assert.equal(assessTool.inputSchema.properties.profile.properties.configurations.type, "array");

    const emptyPageCall = await mcp(mf, "tools/call", {
      name: "kb_assess_rock_issues",
      arguments: { profile: { core_version: "19.2.0", concepts: ["hosting-infrastructure"] }, limit: 1, offset: 1 },
    });
    const emptyPage = JSON.parse(emptyPageCall.result.content[0].text);
    assert.equal(emptyPage.count, 0);
    assert.equal(emptyPage.total_count, 1);
    assert.equal(emptyPage.offset, 1);
    assert.equal(emptyPage.has_more, false);

    const planCall = await mcp(mf, "tools/call", {
      name: "kb_plan_rock_issue_investigation",
      arguments: { issue: "6919", include_private_instance: true },
    });
    const plan = JSON.parse(planCall.result.content[0].text);
    assert.equal(plan.admission.github_write_enabled, false);
    assert.equal(plan.tasks.find((task) => task.role === "instance_investigator").visibility, "private_only");
  } finally {
    await mf.dispose();
  }
});

test("Rock Ideas are explicit-intent routing metadata across REST, search, and MCP", async () => {
  const mf = await buildWorker();
  try {
    const ordinaryResponse = await mf.dispatchFetch("https://kb.example.test/search?q=event%20duration%20days&limit=5");
    const ordinary = await ordinaryResponse.json();
    assert.equal(ordinary.results.some((row) => row.kind === "rock_idea"), false);

    const searchResponse = await mf.dispatchFetch("https://kb.example.test/rock-ideas/search?q=event%20duration%20feature%20request&limit=5");
    const search = await searchResponse.json();
    assert.equal(search.results[0].id, "rock_idea:2250");
    assert.equal(search.results[0].claim_tier, "routing_context_only");

    const genericIntentResponse = await mf.dispatchFetch("https://kb.example.test/search?q=event%20duration%20feature%20request&limit=5");
    const genericIntent = await genericIntentResponse.json();
    assert.equal(genericIntent.results.some((row) => row.id === "rock_idea:2250"), true);

    const exactIntentResponse = await mf.dispatchFetch("https://kb.example.test/search?q=What%20is%20the%20status%20of%20Rock%20Community%20idea%202250%3F&limit=5");
    const exactIntent = await exactIntentResponse.json();
    assert.equal(exactIntent.results[0].id, "rock_idea:2250");

    const listResponse = await mf.dispatchFetch("https://kb.example.test/rock-ideas?status=complete&concept=event-registration&planned_version=20.0");
    const list = await listResponse.json();
    assert.equal(list.count, 1);
    assert.equal(list.ideas[0].idea_id, "rock_idea:2250");

    const getResponse = await mf.dispatchFetch("https://kb.example.test/rock-ideas/2250");
    const get = await getResponse.json();
    assert.equal(get.status, "ok");
    assert.equal(get.idea.needs_live_verification, true);
    assert.equal(get.idea.verification.verification_state, "candidate_review_pending");
    assert.equal(get.idea.verification.claim_tier, "routing_context_only");
    assert.equal(get.idea.description, undefined);
    assert.equal(get.idea.author, undefined);
    assert.equal(get.relationships[0].target_id, "rock_issue:SparkDevNetwork/Rock#6919");
    assert.equal(get.relationships[0].direction, "outbound");

    const tools = await mcp(mf, "tools/list", {});
    const names = tools.result.tools.map((tool) => tool.name);
    assert.equal(names.includes("kb_search_rock_ideas"), true);
    assert.equal(names.includes("kb_list_rock_ideas"), true);
    assert.equal(names.includes("kb_get_rock_idea"), true);

    const call = await mcp(mf, "tools/call", { name: "kb_get_rock_idea", arguments: { idea: "2250" } });
    const toolResult = JSON.parse(call.result.content[0].text);
    assert.equal(toolResult.idea_id, "rock_idea:2250");

    const conceptCall = await mcp(mf, "tools/call", {
      name: "kb_get_concept",
      arguments: { concept_id: "event-registration" },
    });
    const concept = JSON.parse(conceptCall.result.content[0].text);
    assert.equal(concept.rock_ideas.total_count, 1);
    assert.equal(concept.rock_ideas.by_status.complete, 1);
    assert.equal(concept.rock_ideas.highlights[0].idea_id, "rock_idea:2250");
  } finally {
    await mf.dispose();
  }
});

test("Rock issue assessment evaluates candidates beyond the former 1000-row ceiling", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    for (const base of [0, 600]) {
      await db.prepare(`WITH RECURSIVE seq(x) AS (
        VALUES(1)
        UNION ALL SELECT x + 1 FROM seq WHERE x < 600
      )
      INSERT INTO rock_issues
        (issue_id, github_node_id, repository, number, component, state, validation_state, title, url, updated_at, evidence_state, payload_json)
      SELECT
        'rock_issue:SparkDevNetwork/Rock#' || (8000 + ? + x),
        'I_bulk_' || (? + x),
        'SparkDevNetwork/Rock',
        8000 + ? + x,
        'rock_core',
        'open',
        'reported',
        'Bulk fixture ' || (? + x),
        'https://github.com/SparkDevNetwork/Rock/issues/' || (8000 + ? + x),
        '2026-07-15T00:00:00Z',
        'report_only',
        json_object(
          'issue_id', 'rock_issue:SparkDevNetwork/Rock#' || (8000 + ? + x),
          'title', 'Bulk fixture ' || (? + x),
          'url', 'https://github.com/SparkDevNetwork/Rock/issues/' || (8000 + ? + x),
          'state', 'open',
          'component', 'rock_core',
          'validation_state', 'reported',
          'version_evidence', json('[]'),
          'concept_ids', json('[]'),
          'linked_commit_shas', json('[]'),
          'reviewed_enrichments', json('[]')
        )
      FROM seq`).bind(base, base, base, base, base, base, base, base).run();
    }

    const response = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile: { core_version: "19.2.0" }, limit: 2, offset: 1200 }),
    });
    const assessment = await response.json();

    assert.equal(response.status, 200);
    assert.equal(assessment.total_count, 1201);
    assert.equal(assessment.offset, 1200);
    assert.equal(assessment.count, 1);
    assert.equal(assessment.has_more, false);
  } finally {
    await mf.dispose();
  }
});

test("strong lexical claims outrank incidental recipe matches", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const rows = [
      {
        id: "claim:claim:direct-access:security-permissions",
        kind: "claim",
        title: "operational guidance",
        body: "AI integrations should not receive unrestricted direct database access. Route data operations through managed Rock code that enforces authorization and business rules.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/direct-access",
        concept: "security-permissions",
        authority_tier: "official",
        claim_tier: "answer_pack_approved",
        claim_tier_rank: 2,
        source_id: "rock_official",
        payload_json: JSON.stringify({ claim_id: "claim:direct-access" }),
      },
      {
        id: "recipe:oneall:registration-transfer:security-permissions",
        kind: "recipe",
        title: "Registration Transfer Workflow",
        body: "Registration values are available to authorized Connections staff.",
        path: "knowledge/recipes/oneall/registration-transfer.md",
        url: "https://example.test/registration-transfer",
        concept: "security-permissions",
        authority_tier: "community-reviewed",
        claim_tier: "answer_pack_approved",
        claim_tier_rank: 2,
        source_id: "oneall",
        payload_json: JSON.stringify({ recipe_id: "oneall:registration-transfer" }),
      },
      {
        id: "guide_section:hosting-infrastructure:database-and-persistence",
        kind: "guide_section",
        title: "Hosting And Infrastructure: Database And Persistence",
        body: "Rock agents can inspect database and persistence infrastructure, including direct database access, backups, SQL Server, and data operations. Keep access bounded to the required operational task.",
        path: "knowledge/concepts/hosting-infrastructure/guide.md",
        url: "",
        concept: "hosting-infrastructure",
        authority_tier: "official",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({
          section_id: "database-and-persistence",
          heading: "Database And Persistence",
        }),
      },
    ];
    for (const row of rows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
    }

    const query = encodeURIComponent("AI direct database access managed Rock authorization business rules");
    const response = await mf.dispatchFetch(`https://kb.example.test/search?q=${query}&min_tier=answer_pack_approved&limit=5&debug=true`);
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.results[0].id, "claim:claim:direct-access:security-permissions");
    assert.ok(payload.results[0].signals.bm25_relevance > 0);
    const recipeResult = payload.results.find((row) => row.id === "recipe:oneall:registration-transfer:security-permissions");
    if (recipeResult) {
      assert.ok(payload.results[0].score > recipeResult.score);
      assert.ok(payload.results[0].signals.bm25_relevance > recipeResult.signals.bm25_relevance);
    }

    const paraphrase = encodeURIComponent("Can Rock agents use direct database access?");
    const paraphraseResponse = await mf.dispatchFetch(`https://kb.example.test/search?q=${paraphrase}&limit=3&debug=true`);
    const paraphrasePayload = await paraphraseResponse.json();
    assert.equal(
      paraphrasePayload.results[0].id,
      "claim:claim:direct-access:security-permissions",
      JSON.stringify(
        paraphrasePayload.results.map((row) => ({ id: row.id, score: row.score, signals: row.signals })),
      ),
    );
    assert.ok(
      paraphrasePayload.results.some(
        (row) => row.id === "guide_section:hosting-infrastructure:database-and-persistence",
      ),
    );

    const guideQuery = encodeURIComponent(
      "hosting infrastructure database and persistence guide section",
    );
    const guideResponse = await mf.dispatchFetch(
      `https://kb.example.test/search?q=${guideQuery}&limit=3&debug=true`,
    );
    const guidePayload = await guideResponse.json();
    assert.equal(
      guidePayload.results[0].id,
      "guide_section:hosting-infrastructure:database-and-persistence",
    );
    assert.ok(guidePayload.results[0].signals.exact_lookup_boost >= 100);

    const exactGuideResponse = await mf.dispatchFetch(
      "https://kb.example.test/results/guide_section%3Ahosting-infrastructure%3Adatabase-and-persistence",
    );
    const exactGuide = await exactGuideResponse.json();
    assert.equal(exactGuide.status, "ok");
    assert.equal(exactGuide.result.kind, "guide_section");
    assert.equal(exactGuide.result.payload.section_id, "database-and-persistence");
  } finally {
    await mf.dispose();
  }
});

test("generic title overlap does not displace more complete troubleshooting", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    const rows = [
      {
        id: "claim:claim:damaged-checkin-label",
        kind: "claim",
        title: "A damaged check-in label can obscure a child's name",
        body: "A damaged check-in label can obscure a child's name or security pickup code.",
        path: "claims/approved-claims.jsonl",
        url: "https://example.test/damaged-label",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "rock_documentation",
        payload_json: JSON.stringify({ claim_id: "claim:damaged-checkin-label" }),
      },
      {
        id: "troubleshooting_node:check-in:child-present-no-rooms",
        kind: "troubleshooting_node",
        title: "Symptom: Child Present, No Rooms Available",
        body: "Inspect group and location availability, active schedules, capacity, campus, and eligibility rules.",
        path: "knowledge/concepts/check-in/troubleshooting-tree.json",
        url: "",
        concept: "check-in",
        authority_tier: "community-reviewed",
        claim_tier: "source_backed",
        claim_tier_rank: 1,
        source_id: "",
        payload_json: JSON.stringify({
          id: "child-present-no-rooms",
          concept_id: "check-in",
        }),
      },
    ];
    for (const row of rows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
    }

    const query = encodeURIComponent(
      "A child qualifies for check-in, but no destination can be selected. What availability layers should I inspect?",
    );
    const response = await mf.dispatchFetch(
      `https://kb.example.test/search?q=${query}&limit=5&debug=true`,
    );
    const payload = await response.json();

    assert.equal(response.status, 200);
    const resultIds = payload.results.map((result) => result.id);
    assert.ok(
      resultIds.indexOf("troubleshooting_node:check-in:child-present-no-rooms")
        < resultIds.indexOf(rows[0].id),
      JSON.stringify(payload.results.map((result) => ({
        id: result.id,
        score: result.score,
        signals: result.signals,
      }))),
    );
  } finally {
    await mf.dispose();
  }
});

test("telemetry separates evaluation traffic and records structured feedback without query text", async () => {
  const mf = await buildWorker();
  try {
    await mf.dispatchFetch("https://kb.example.test/search?q=labels", {
      headers: { "x-rock-kb-client": "cli", "x-rock-kb-cohort": "external-test" },
    });
    await mf.dispatchFetch("https://kb.example.test/search?q=prayerzz", {
      headers: { "user-agent": "rock-kb-eval/1.0" },
    });
    await mf.dispatchFetch("https://kb.example.test/search?q=prayerzz", {
      headers: { "x-rock-kb-client": "browser", "x-rock-kb-cohort": "one-all-church" },
    });
    await mf.dispatchFetch("https://kb.example.test/results/claim%3Aclaim%3Aabc123", {
      headers: { "x-rock-kb-client": "cli" },
    });
    await mf.dispatchFetch("https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard", {
      headers: { "x-rock-kb-client": "cli" },
    });
    await mcp(
      mf,
      "tools/call",
      { name: "kb_get_claim", arguments: { claim_id: "claim:abc123" } },
      { "x-rock-kb-cohort": "external-test" },
    );
    await mcp(
      mf,
      "tools/call",
      { name: "kb_get_claim", arguments: { claim_id: "claim:abc123" } },
      { "x-rock-kb-client": "eval", "x-rock-kb-cohort": "external-test" },
    );
    const feedbackResponse = await mf.dispatchFetch("https://kb.example.test/feedback", {
      method: "POST",
      headers: { "content-type": "application/json", "x-rock-kb-client": "cli", "x-rock-kb-cohort": "external-test" },
      body: JSON.stringify({ result_id: "claim:claim:abc123:check-in", rating: -1, reason: "outdated" }),
    });
    assert.equal(feedbackResponse.status, 201);
    const feedbackResult = await feedbackResponse.json();
    assert.equal(feedbackResult.schema, "rock-kb-feedback-result-v2");
    assert.equal(feedbackResult.result_id, "claim:claim:abc123");
    assert.equal(feedbackResult.projection_version, "test-version");

    const telemetryResponse = await mf.dispatchFetch("https://kb.example.test/telemetry/summary");
    const telemetry = await telemetryResponse.json();

    assert.equal(telemetry.schema, "rock-kb-telemetry-summary-v5");
    assert.equal(telemetry.adoption_rows.some((row) => row.client_class === "cli"), true);
    assert.equal(telemetry.external_test_rows.some((row) => row.client_class === "cli" && row.cohort === "external-test"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.client_class === "browser" && row.cohort === "unattributed"), true);
    assert.equal(telemetry.evaluation_rows.some((row) => row.client_class === "eval"), true);
    assert.equal(telemetry.evaluation_rows.every((row) => row.cohort === "evaluation"), true);
    assert.equal(telemetry.zero_result_topics.some((row) => row.topic_hint === "prayer-care"), true);
    assert.equal(telemetry.feedback.some((row) => row.reason === "outdated" && row.rating === -1), true);
    assert.equal(telemetry.feedback.some((row) => row.result_id === "claim:claim:abc123"), true);
    assert.equal(telemetry.feedback.some((row) => row.cohort === "external-test"), true);
    assert.equal(telemetry.result_kinds.some((row) => row.result_kind === "claim" && row.client_class === "cli"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.event === "result_get" && row.client_class === "cli" && row.primary_result_kind === "claim"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.event === "recipe_get" && row.client_class === "cli" && row.primary_result_kind === "recipe"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.event === "claim_get" && row.client_class === "mcp" && row.primary_result_kind === "claim"), true);
    assert.equal(telemetry.external_test_rows.some((row) => row.event === "claim_get" && row.client_class === "mcp"), true);
    assert.match(telemetry.privacy, /No raw or hashed query text/);
    assert.equal(JSON.stringify(telemetry).includes("prayerzz"), false);
    assert.equal(JSON.stringify(telemetry).includes("one-all-church"), false);
  } finally {
    await mf.dispose();
  }
});

test("opted-in outcomes feed a privacy-bounded field-validation funnel and review queue", async () => {
  const mf = await buildWorker();
  const installationId = `rkbi_${"a".repeat(43)}`;
  const maintainerInstallationId = `rkbi_${"b".repeat(43)}`;
  const communityHeaders = {
    "x-rock-kb-client": "cli",
    "x-rock-kb-cohort": "community",
    "x-rock-kb-installation-id": installationId,
  };
  try {
    const missingOptIn = await mf.dispatchFetch("https://kb.example.test/outcomes", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        result_id: "claim:claim:abc123",
        outcome: "useful",
        reason_codes: ["answered"],
        consent_attested: true,
      }),
    });
    assert.equal(missingOptIn.status, 400);
    assert.equal((await missingOptIn.json()).error_code, "installation_opt_in_required");

    const incompatibleReason = await mf.dispatchFetch("https://kb.example.test/outcomes", {
      method: "POST",
      headers: { ...communityHeaders, "content-type": "application/json" },
      body: JSON.stringify({
        result_id: "claim:claim:abc123",
        outcome: "useful",
        reason_codes: ["incorrect"],
        consent_attested: true,
      }),
    });
    assert.equal(incompatibleReason.status, 400);
    assert.equal((await incompatibleReason.json()).error_code, "invalid_reason_codes");

    for (let index = 0; index < 3; index += 1) {
      await mf.dispatchFetch(`https://kb.example.test/search?q=prayerzz${index}`, { headers: communityHeaders });
    }
    await mf.dispatchFetch("https://kb.example.test/search?q=labels", {
      headers: {
        "x-rock-kb-client": "cli",
        "x-rock-kb-cohort": "maintainer",
        "x-rock-kb-installation-id": maintainerInstallationId,
      },
    });
    const missingResult = await mf.dispatchFetch("https://kb.example.test/results/not-a-real-result", { headers: communityHeaders });
    assert.equal(missingResult.status, 404);
    const missingConcept = await mf.dispatchFetch("https://kb.example.test/concepts/not-a-real-concept.md", { headers: communityHeaders });
    assert.equal(missingConcept.status, 404);
    const exactResult = await mf.dispatchFetch("https://kb.example.test/results/claim%3Aclaim%3Aabc123", { headers: communityHeaders });
    assert.equal(exactResult.status, 200);

    const outcomeResponse = await mf.dispatchFetch("https://kb.example.test/outcomes", {
      method: "POST",
      headers: { ...communityHeaders, "content-type": "application/json" },
      body: JSON.stringify({
        result_id: "claim:claim:abc123:check-in",
        outcome: "not_useful",
        reason_codes: ["wrong_route", "missing_detail"],
        consent_attested: true,
      }),
    });
    assert.equal(outcomeResponse.status, 201);
    const outcome = await outcomeResponse.json();
    assert.equal(outcome.status, "recorded");
    assert.equal(outcome.result_id, "claim:claim:abc123");
    assert.match(outcome.outcome_id, /^kbo_[0-9a-f]{24}$/);

    const maintainerOutcome = await mf.dispatchFetch("https://kb.example.test/outcomes", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-rock-kb-client": "cli",
        "x-rock-kb-cohort": "maintainer",
        "x-rock-kb-installation-id": maintainerInstallationId,
      },
      body: JSON.stringify({
        result_id: "claim:claim:abc123",
        outcome: "useful",
        reason_codes: ["answered"],
        consent_attested: true,
      }),
    });
    assert.equal(maintainerOutcome.status, 201);

    await mf.dispatchFetch("https://kb.example.test/feedback", {
      method: "POST",
      headers: { ...communityHeaders, "content-type": "application/json" },
      body: JSON.stringify({ result_id: "claim:claim:abc123", rating: -1, reason: "wrong_route" }),
    });
    const report = await mf.dispatchFetch("https://kb.example.test/issues/report", {
      method: "POST",
      headers: { ...communityHeaders, "content-type": "application/json" },
      body: JSON.stringify({
        failure_type: "retrieval",
        operation: "search",
        error_code: "service_unavailable",
        description: "Hosted retrieval returned a temporary failure.",
        redaction_attested: true,
      }),
    });
    assert.equal(report.status, 201);

    const dashboard = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(dashboard.schema, "rock-kb-operations-dashboard-v5");
    assert.equal(dashboard.field_validation.default_scope.evaluation_traffic_included, false);
    assert.equal(dashboard.field_validation.default_scope.maintainer_traffic_included, false);
    assert.equal(dashboard.field_validation.coverage.event_schema, "usage_events_v5");
    assert.equal(dashboard.field_validation.coverage.historical_event_schemas_included, false);
    assert.equal(dashboard.field_validation.funnel.search_count, 3);
    assert.equal(dashboard.field_validation.funnel.exact_retrieval_count, 3);
    assert.equal(dashboard.field_validation.funnel.exact_retrieval_success_count, 1);
    assert.equal(dashboard.field_validation.funnel.exact_retrieval_failure_count, 2);
    assert.equal(dashboard.field_validation.funnel.outcome_count, 1);
    assert.equal(dashboard.field_validation.funnel.feedback_count, 1);
    assert.equal(dashboard.field_validation.funnel.report_issue_count, 1);
    assert.equal(dashboard.field_validation.opted_in_installation_count, 1);
    assert.equal(dashboard.field_validation.outcomes.by_outcome.not_useful, 1);
    assert.equal(dashboard.field_validation.review_queue.by_signal.negative_outcome, 1);
    assert.equal(dashboard.field_validation.review_queue.by_signal.repeated_zero_result_topic, 1);
    assert.equal(dashboard.field_validation.review_queue.by_signal.failed_exact_lookup, 2);
    assert.equal(JSON.stringify(dashboard).includes(installationId), false);
    assert.equal(JSON.stringify(dashboard).includes(maintainerInstallationId), false);
    assert.equal(JSON.stringify(dashboard).includes("prayerzz"), false);

    const db = await mf.getD1Database("KB_DB");
    const stored = await db.prepare("SELECT installation_hash FROM outcome_events_v1 LIMIT 1").first();
    assert.match(stored.installation_hash, /^[0-9a-f]{64}$/);
    assert.notEqual(stored.installation_hash, installationId);
  } finally {
    await mf.dispose();
  }
});

test("outcome telemetry migrates existing rows to an explicit retrieval projection", async () => {
  const mf = await buildWorker();
  try {
    const db = await mf.getD1Database("KB_DB");
    await db.prepare(
      `CREATE TABLE outcome_events_v1 (
        day TEXT NOT NULL,
        installation_hash TEXT NOT NULL,
        client_class TEXT NOT NULL,
        cohort TEXT NOT NULL,
        result_id TEXT NOT NULL,
        result_kind TEXT NOT NULL,
        projection_version TEXT NOT NULL,
        outcome TEXT NOT NULL,
        reason_codes TEXT NOT NULL,
        count INTEGER NOT NULL,
        PRIMARY KEY(day, installation_hash, client_class, cohort, result_id, projection_version, outcome, reason_codes)
      )`,
    ).run();
    const installationId = `rkbi_${"e".repeat(43)}`;
    const response = await mf.dispatchFetch(
      "https://kb.example.test/outcomes",
      {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "x-rock-kb-client": "cli",
          "x-rock-kb-cohort": "community",
          "x-rock-kb-installation-id": installationId,
        },
        body: JSON.stringify({
          result_id: "claim:claim:abc123",
          outcome: "useful",
          reason_codes: ["answered"],
          consent_attested: true,
        }),
      },
    );
    assert.equal(response.status, 201);
    const columns = await db.prepare(
      "PRAGMA table_info(outcome_events_v1)",
    ).all();
    assert.equal(
      columns.results.some(
        (column) => column.name === "retrieval_projection",
      ),
      true,
    );
    const stored = await db.prepare(
      "SELECT retrieval_projection FROM outcome_events_v1 LIMIT 1",
    ).first();
    assert.equal(stored.retrieval_projection, "legacy");
  } finally {
    await mf.dispose();
  }
});

test("community test rounds require a cohort and aggregate all fixed case outcomes", async () => {
  const mf = await buildWorker();
  try {
    const categories = new Map([
      ["service-health", "service"],
      ["exact-group-model", "exact_lookup"],
      ["check-in-lava-context", "lava_context"],
      ["reviewed-recipe", "recipe"],
      ["check-in-troubleshooting", "semantic_search"],
      ["idea-relationship-trust", "rock_idea"],
      ["core-issue-trust", "imported_issue"],
      ["mobile-issue-release-evidence", "imported_issue"],
      ["issue-version-assessment", "imported_issue"],
      ["no-answer-boundary", "no_answer"],
    ]);
    const review = {
      schema: "rock-kb-community-test-round-review-v1",
      test_round_schema: "rock-kb-community-test-round-v1",
      projection_version: "test-version",
      automatic_status: "ok",
      cases: [...categories].map(([case_id, category]) => {
        const canonicalResultIds = new Map([
          ["exact-group-model", "model_map:stable:group"],
          ["reviewed-recipe", "recipe:oneall:check-in-status-dashboard"],
          ["check-in-troubleshooting", "concept:check-in"],
          ["idea-relationship-trust", "rock_idea:2250"],
          ["core-issue-trust", "rock_issue:SparkDevNetwork/Rock#6919"],
          ["mobile-issue-release-evidence", "rock_issue:SparkDevNetwork/Rock#6919"],
          ["issue-version-assessment", "rock_issue:SparkDevNetwork/Rock#6919"],
        ]);
        return {
          case_id,
          category,
          automatic_status: "pass",
          outcome: case_id === "no-answer-boundary" ? "unsure" : "useful",
          result_id: canonicalResultIds.get(case_id) || (["service", "no_answer"].includes(category) ? null : "claim:claim:abc123"),
        };
      }),
    };
    for (const event of [{ stage: "started" }, { stage: "completed", automatic_status: "ok" }]) {
      const eventResponse = await mf.dispatchFetch("https://kb.example.test/test-rounds/events", {
        method: "POST",
        headers: { "content-type": "application/json", "x-rock-kb-client": "cli", "x-rock-kb-cohort": "external-test" },
        body: JSON.stringify(event),
      });
      assert.equal(eventResponse.status, 201);
    }
    const unattributed = await mf.dispatchFetch("https://kb.example.test/test-rounds/review", {
      method: "POST",
      headers: { "content-type": "application/json", "x-rock-kb-client": "cli" },
      body: JSON.stringify(review),
    });
    assert.equal(unattributed.status, 400);
    assert.equal((await unattributed.json()).error_code, "cohort_required");

    const ordinaryCommunity = await mf.dispatchFetch("https://kb.example.test/test-rounds/review", {
      method: "POST",
      headers: { "content-type": "application/json", "x-rock-kb-client": "cli", "x-rock-kb-cohort": "community" },
      body: JSON.stringify(review),
    });
    assert.equal(ordinaryCommunity.status, 400);
    assert.equal((await ordinaryCommunity.json()).error_code, "cohort_required");

    const recorded = await mf.dispatchFetch("https://kb.example.test/test-rounds/review", {
      method: "POST",
      headers: { "content-type": "application/json", "x-rock-kb-client": "cli", "x-rock-kb-cohort": "external-test" },
      body: JSON.stringify(review),
    });
    assert.equal(recorded.status, 201);
    const result = await recorded.json();
    assert.equal(result.status, "recorded");
    assert.equal(result.case_count, 10);
    assert.equal(result.projection_matches_current, true);

    const dashboard = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(dashboard.test_rounds.submission_count, 1);
    assert.equal(dashboard.test_rounds.case_outcome_count, 10);
    assert.equal(dashboard.test_rounds.by_manual_outcome.useful, 9);
    assert.equal(dashboard.test_rounds.by_manual_outcome.unsure, 1);
    assert.equal(dashboard.test_rounds.funnel.started_count, 1);
    assert.equal(dashboard.test_rounds.funnel.completed_count, 1);
    assert.equal(dashboard.test_rounds.funnel.submitted_count, 1);
    assert.equal(
      dashboard.test_rounds.cases.find((row) => row.case_id === "core-issue-trust").result_ids[
        "rock_issue:SparkDevNetwork/Rock#6919"
      ],
      1,
    );
    assert.equal(JSON.stringify(dashboard.test_rounds).includes("Review this"), false);

    const mcpDefinition = await mcp(mf, "tools/call", { name: "kb_get_test_round", arguments: {} });
    const definition = JSON.parse(mcpDefinition.result.content[0].text);
    assert.equal(definition.cases.length, 10);
    assert.deepEqual(definition.outcomes, ["useful", "incorrect", "incomplete", "unclear", "unsure"]);
    const funnelAfterMcp = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(funnelAfterMcp.test_rounds.funnel.started_count, 2);

    const mcpTools = await mcp(mf, "tools/list", {});
    const submitTool = mcpTools.result.tools.find((tool) => tool.name === "kb_submit_test_round_review");
    assert.equal(submitTool.inputSchema.properties.cases.minItems, 10);
    assert.equal(submitTool.inputSchema.properties.cases.maxItems, 10);
  } finally {
    await mf.dispose();
  }
});

test("operations dashboard separates generated evaluation rows from the latest hosted run", async () => {
  const mf = await buildWorker();
  try {
    await mf.dispatchFetch("https://kb.example.test/operations/dashboard");
    const db = await mf.getD1Database("KB_DB");
    await db.prepare(
      `INSERT INTO hosted_evaluation_runs_v1
       (projection_version, evaluated_at, status, case_count, pass_count, fail_count, metrics_json, client_version)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    ).bind(
      "test-version",
      "2026-07-17T20:00:00Z",
      "ok",
      151,
      151,
      0,
      JSON.stringify({ mean_reciprocal_rank: 0.993377, recall_at_target_rank: 1, duplicate_result_rate: 0 }),
      "workflow-v1",
    ).run();

    const dashboard = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(dashboard.schema, "rock-kb-operations-dashboard-v5");
    assert.equal(dashboard.evaluation.generated_projection.row_count, dashboard.evaluation.row_count);
    assert.equal(dashboard.evaluation.hosted_service.status, "ok");
    assert.equal(dashboard.evaluation.hosted_service.case_count, 151);
    assert.equal(dashboard.evaluation.hosted_service.current_projection, true);
    assert.equal(dashboard.evaluation.hosted_service.metrics.mean_reciprocal_rank, 0.993377);
    assert.equal(dashboard.rock_ideas.record_count, 1);
    assert.equal(dashboard.rock_ideas.relationships.verification_queue.queue_count, 1);
    assert.equal(
      dashboard.rock_ideas.relationships.verification_queue.by_verification_state.candidate_review_pending,
      1,
    );
  } finally {
    await mf.dispose();
  }
});

test("hosted source freshness keeps workflow schedule and source content state separate", async () => {
  const mf = await buildWorker();
  try {
    const initial = await (await mf.dispatchFetch("https://kb.example.test/operations/freshness")).json();
    assert.equal(initial.status, "not_recorded");
    assert.deepEqual(initial.missing_workflow_ids, ["daily-sources", "daily-issues", "weekly-comprehensive"]);

    const db = await mf.getD1Database("KB_DB");
    const now = new Date().toISOString();
    for (const [workflowId, maximumAge] of [["daily-sources", 52], ["daily-issues", 36], ["weekly-comprehensive", 216]]) {
      await db.prepare(
        `INSERT INTO source_workflow_runs_v1
         (workflow_id, run_id, run_url, observed_at, status, maximum_age_hours, source_count, content_hash, counts_json, blocking_source_ids_json)
         VALUES (?, ?, ?, ?, 'ok', ?, 1, ?, ?, '[]')`,
      ).bind(workflowId, "123", "https://github.com/example/actions/runs/123", now, maximumAge, "a".repeat(64), '{"current":1}').run();
    }
    await db.prepare(
      `INSERT INTO source_freshness_state_v1
       (source_id, name, cadence, maximum_age_hours, last_checked_at, content_changed_at, result_count, content_hash, check_status, status, observed_at, workflow_id)
       VALUES (?, ?, 'daily', 48, ?, ?, 321, ?, 'success', 'current', ?, 'daily-issues')`,
    ).bind("rock_core_issues", "Rock Core GitHub Issues", now, now, "b".repeat(64), now).run();

    const current = await (await mf.dispatchFetch("https://kb.example.test/operations/freshness")).json();
    assert.equal(current.status, "ok");
    assert.equal(current.workflows.length, 3);
    assert.equal(current.sources[0].last_checked_at, now);
    assert.equal(current.sources[0].content_changed_at, now);
    assert.equal(current.sources[0].result_count, 321);
    assert.equal(current.sources[0].content_hash, "b".repeat(64));
    assert.equal(current.sources[0].check_status, "success");
    assert.equal(current.sources[0].status, "current");
    assert.equal(current.rock_issues.result_count, 321);

    const laggingAssessment = await (await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile: { core_version: "19.2.0" }, limit: 1 }),
    })).json();
    assert.equal(laggingAssessment.catalog.status, "deployment_lag");
    assert.equal(laggingAssessment.catalog.source_result_count, 321);
    assert.equal(laggingAssessment.catalog.projection_record_count, 1);
    assert.equal(laggingAssessment.catalog.projection_count_matches_source, false);
    assert.equal(laggingAssessment.catalog.projection_content_matches_source, false);
    assert.equal(laggingAssessment.catalog.projection_matches_source, false);

    await db.prepare("UPDATE source_freshness_state_v1 SET result_count = 1 WHERE source_id = 'rock_core_issues'").run();
    const sameCountChangedContent = await (await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile: { core_version: "19.2.0" }, limit: 1 }),
    })).json();
    assert.equal(sameCountChangedContent.catalog.status, "deployment_lag");
    assert.equal(sameCountChangedContent.catalog.projection_count_matches_source, true);
    assert.equal(sameCountChangedContent.catalog.projection_content_matches_source, false);
    assert.equal(sameCountChangedContent.catalog.projection_matches_source, false);
    assert.match(sameCountChangedContent.catalog.warning, /content hash/);

    await db.prepare("UPDATE source_freshness_state_v1 SET content_hash = ? WHERE source_id = 'rock_core_issues'")
      .bind(ISSUE_FIXTURE_SOURCE_HASHES.rock_core_issues).run();
    const currentAssessment = await (await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile: { core_version: "19.2.0" }, limit: 1 }),
    })).json();
    assert.equal(currentAssessment.catalog.status, "current");
    assert.equal(currentAssessment.catalog.projection_count_matches_source, true);
    assert.equal(currentAssessment.catalog.projection_content_matches_source, true);
    assert.equal(currentAssessment.catalog.projection_matches_source, true);
    assert.equal(currentAssessment.catalog.projection_catalog_content_hash, ISSUE_FIXTURE_CATALOG_HASH);
    assert.equal(
      currentAssessment.catalog.source_content_hashes.rock_core_issues,
      ISSUE_FIXTURE_SOURCE_HASHES.rock_core_issues,
    );

    const freshnessTool = await mcp(mf, "tools/call", { name: "kb_get_freshness", arguments: {} });
    assert.equal(freshnessTool.result.structuredContent.status, "ok");
  } finally {
    await mf.dispose();
  }
});

test("structured issue reports capture context, deduplicate, and remain pending review", async () => {
  const mf = await buildWorker();
  try {
    const report = {
      failure_type: "retrieval",
      operation: "search",
      result_id: "claim:claim:abc123",
      http_status: 503,
      error_code: "search_unavailable",
      description: "Search returned a temporary service failure.",
      redaction_attested: true,
    };
    const headers = {
      "content-type": "application/json",
      "x-rock-kb-client": "cli",
      "x-rock-kb-client-version": "0.8.0",
    };
    const firstResponse = await mf.dispatchFetch("https://kb.example.test/issues/report", {
      method: "POST",
      headers,
      body: JSON.stringify(report),
    });
    const first = await firstResponse.json();
    assert.equal(firstResponse.status, 201);
    assert.equal(first.schema, "rock-kb-issue-report-result-v1");
    assert.equal(first.status, "pending_review");
    assert.match(first.report_id, /^kbir_[0-9a-f]{24}$/);
    assert.equal(first.occurrence_count, 1);
    assert.equal(first.github_issue_created, false);
    assert.deepEqual(first.captured, {
      failure_type: "retrieval",
      operation: "search",
      projection_version: "test-version",
      client_class: "cli",
      client_version: "0.8.0",
      result_id: "claim:claim:abc123",
      http_status: 503,
      error_code: "search_unavailable",
    });

    const secondResponse = await mf.dispatchFetch("https://kb.example.test/issues/report", {
      method: "POST",
      headers: { ...headers, "x-rock-kb-client-version": "0.8.1" },
      body: JSON.stringify({ ...report, description: "Search failed again without returning results." }),
    });
    const second = await secondResponse.json();
    assert.equal(second.status, "deduplicated");
    assert.equal(second.report_id, first.report_id);
    assert.equal(second.occurrence_count, 2);

    const dashboardResponse = await mf.dispatchFetch("https://kb.example.test/operations/dashboard");
    const dashboard = await dashboardResponse.json();
    assert.equal(dashboard.schema, "rock-kb-operations-dashboard-v5");
    assert.equal(dashboard.issue_reports.schema, "rock-kb-issue-review-dashboard-v1");
    assert.equal(dashboard.issue_reports.unique_report_count, 1);
    assert.equal(dashboard.issue_reports.total_occurrences, 2);
    assert.equal(dashboard.issue_reports.pending_review_count, 1);
    assert.equal(dashboard.issue_reports.reports[0].description, report.description);
    assert.equal(dashboard.issue_reports.reports[0].first_client_version, "0.8.0");
    assert.equal(dashboard.issue_reports.reports[0].last_client_version, "0.8.1");
    assert.equal(dashboard.issue_reports.reports[0].github_issue_status, "review_required");
    assert.equal(dashboard.issue_reports.reports[0].github_issue_url, null);
  } finally {
    await mf.dispose();
  }
});

test("MCP issue reporting uses the same structured review path", async () => {
  const mf = await buildWorker();
  try {
    const response = await mcp(mf, "tools/call", {
      name: "kb_report_issue",
      arguments: {
        failure_type: "mcp",
        operation: "mcp_tool_call",
        error_code: "tool_result_invalid",
        description: "The tool returned an invalid structured result.",
        redaction_attested: true,
      },
    });
    const result = JSON.parse(response.result.content[0].text);
    assert.equal(result.status, "pending_review");
    assert.equal(result.captured.client_class, "mcp");
    assert.equal(result.captured.projection_version, "test-version");
    assert.equal(result.github_issue_created, false);
  } finally {
    await mf.dispose();
  }
});

test("issue reports reject unsafe, unstructured, unattested, and oversized content", async () => {
  const mf = await buildWorker();
  try {
    const base = {
      failure_type: "service",
      operation: "service_request",
      error_code: "unexpected_failure",
      description: "The service returned an unexpected failure.",
      redaction_attested: true,
    };
    const cases = [
      [{ ...base, redaction_attested: false }, "redaction_attestation_required"],
      [{ ...base, description: "Stack trace: token=private-value" }, "unsafe_description"],
      [{ ...base, query: "private search text" }, "unsupported_fields"],
      [{ ...base, result_id: "/Users/example/private" }, "invalid_result_id"],
      [{ ...base, http_status: "503" }, "invalid_field_types"],
    ];
    for (const [payload, expectedCode] of cases) {
      const response = await mf.dispatchFetch("https://kb.example.test/issues/report", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await response.json();
      assert.equal(response.status, 400);
      assert.equal(result.status, "rejected");
      assert.equal(result.error_code, expectedCode);
      assert.equal(result.github_issue_created, false);
    }

    const oversizedResponse = await mf.dispatchFetch("https://kb.example.test/issues/report", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ ...base, description: "x".repeat(5000) }),
    });
    assert.equal(oversizedResponse.status, 413);
    assert.equal((await oversizedResponse.json()).error_code, "report_too_large");
  } finally {
    await mf.dispose();
  }
});

test("issue report duplicates are rate limited without creating extra occurrences", async () => {
  const mf = await buildWorker();
  try {
    const report = {
      failure_type: "cli",
      operation: "cli_startup",
      error_code: "startup_failed",
      description: "The command could not start in the client.",
      redaction_attested: true,
    };
    for (let attempt = 1; attempt <= 10; attempt += 1) {
      const response = await mf.dispatchFetch("https://kb.example.test/issues/report", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(report),
      });
      assert.equal(response.status, 201);
    }
    const limitedResponse = await mf.dispatchFetch("https://kb.example.test/issues/report", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(report),
    });
    assert.equal(limitedResponse.status, 429);
    assert.equal((await limitedResponse.json()).error_code, "rate_limited");

    const dashboard = await (await mf.dispatchFetch("https://kb.example.test/operations/dashboard")).json();
    assert.equal(dashboard.issue_reports.total_occurrences, 10);
  } finally {
    await mf.dispose();
  }
});

test("recipe verification falls back to GitHub contents API and caches immutable bytes", async () => {
  const fetchMock = new MockAgent();
  fetchMock.disableNetConnect();
  fetchMock.get("https://raw.githubusercontent.com")
    .intercept({
      path: `/ONE-ALL-Church/RockRMS-OA-Public/${RECIPE_FIXTURE_COMMIT}/Recipes/check-in-status-dashboard/README.md`,
      method: "GET",
    })
    .reply(503, "temporary failure")
    .times(3);
  fetchMock.get("https://api.github.com")
    .intercept({
      path: `/repos/ONE-ALL-Church/RockRMS-OA-Public/contents/Recipes/check-in-status-dashboard/README.md?ref=${RECIPE_FIXTURE_COMMIT}`,
      method: "GET",
    })
    .reply(200, RECIPE_FIXTURE_CONTENT, { headers: { "content-type": "application/octet-stream" } });
  const mf = await buildWorker({ fetchMock });
  try {
    const firstResponse = await mf.dispatchFetch(
      "https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard/verify?rock_version=18"
    );
    const first = await firstResponse.json();
    assert.equal(first.status, "pass");
    assert.equal(first.file_checks[0].source, "github_contents_api");
    assert.equal(first.file_checks[0].cache_status, "miss");
    assert.equal(first.file_checks[0].attempts, 4);

    const cachedResponse = await mf.dispatchFetch(
      "https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard/verify?rock_version=18"
    );
    const cached = await cachedResponse.json();
    assert.equal(cached.status, "pass");
    assert.equal(cached.file_checks[0].source, "cache");
    assert.equal(cached.file_checks[0].cache_status, "hit");
    assert.equal(cached.file_checks[0].attempts, 0);
  } finally {
    await mf.dispose();
    await fetchMock.close();
  }
});

test("recipe verification never caches bytes that fail the pinned hash", async () => {
  const fetchMock = new MockAgent();
  fetchMock.disableNetConnect();
  fetchMock.get("https://raw.githubusercontent.com")
    .intercept({
      path: `/ONE-ALL-Church/RockRMS-OA-Public/${RECIPE_FIXTURE_COMMIT}/Recipes/check-in-status-dashboard/README.md`,
      method: "GET",
    })
    .reply(200, "wrong bytes")
    .times(2);
  const mf = await buildWorker({ fetchMock });
  try {
    for (let attempt = 0; attempt < 2; attempt += 1) {
      const response = await mf.dispatchFetch(
        "https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard/verify?rock_version=18"
      );
      const result = await response.json();
      assert.equal(result.status, "fail");
      assert.equal(result.file_checks[0].source, "raw_github");
      assert.equal(result.file_checks[0].cache_status, "miss");
      assert.equal(result.file_checks[0].status, "fail");
    }
  } finally {
    await mf.dispose();
    await fetchMock.close();
  }
});

async function buildWorker(options = {}) {
  const suffix = crypto.randomUUID();
  const mf = new Miniflare({
    modules: true,
    scriptPath: WORKER_BUNDLE,
    compatibilityDate: "2026-07-18",
    compatibilityFlags: ["nodejs_compat"],
    d1Databases: { KB_DB: `kb-retrieval-${suffix}` },
    r2Buckets: { KB_ARTIFACTS: `kb-artifacts-${suffix}` },
    workerLoaders: { LOADER: {} },
    bindings: { PUBLIC_BASE_URL: "https://kb.example.test" },
    fetchMock: options.fetchMock,
  });
  try {
    const db = await mf.getD1Database("KB_DB");
    await db.prepare("CREATE TABLE kb_meta (key TEXT PRIMARY KEY, value TEXT)").run();
    await db.prepare("INSERT INTO kb_meta (key, value) VALUES ('current_version', 'test-version')").run();
    await db.prepare("INSERT INTO kb_meta (key, value) VALUES ('rock_issue_catalog_content_hash', ?)")
      .bind(ISSUE_FIXTURE_CATALOG_HASH).run();
    await db.prepare("INSERT INTO kb_meta (key, value) VALUES ('rock_issue_source_content_hashes', ?)")
      .bind(JSON.stringify(ISSUE_FIXTURE_SOURCE_HASHES)).run();
    if (options.artifactPrefix) {
      await db.prepare("INSERT INTO kb_meta (key, value) VALUES ('artifact_prefix', ?)").bind(options.artifactPrefix).run();
    }
    if (options.canonicalShadow) {
      const shadow = options.canonicalShadow;
      const metadata = {
        active_retrieval_projection: options.activeProjection || "legacy",
        canonical_shadow_status: shadow.status,
        canonical_shadow_content_hash: shadow.contentHash,
        canonical_shadow_search_row_count: String(shadow.searchRowCount),
        canonical_shadow_knowledge_unit_count: String(shadow.knowledgeUnitCount),
        canonical_shadow_artifact_count: String(shadow.artifactCount),
        canonical_shadow_observation_count: String(shadow.observationCount),
      };
      for (const [key, value] of Object.entries(metadata)) {
        await db.prepare("INSERT INTO kb_meta (key, value) VALUES (?, ?)")
          .bind(key, value)
          .run();
      }
    }
    await db.prepare(`CREATE TABLE search_rows (
      id TEXT PRIMARY KEY,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      body TEXT,
      path TEXT NOT NULL,
      url TEXT,
      concept TEXT,
      authority_tier TEXT,
      claim_tier TEXT,
      claim_tier_rank INTEGER,
      source_id TEXT,
      concepts_json TEXT NOT NULL DEFAULT '[]',
      topics_json TEXT NOT NULL DEFAULT '[]',
      payload_json TEXT
    )`).run();
    await db.prepare("CREATE TABLE search_row_concepts (row_id TEXT NOT NULL, concept TEXT NOT NULL, PRIMARY KEY (row_id, concept))").run();
    await db.prepare("CREATE TABLE search_row_aliases (alias_id TEXT PRIMARY KEY, canonical_id TEXT NOT NULL)").run();
    await db.prepare(`CREATE TABLE canonical_search_rows (
      id TEXT PRIMARY KEY,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      body TEXT,
      path TEXT NOT NULL,
      url TEXT,
      concept TEXT,
      authority_tier TEXT,
      claim_tier TEXT,
      claim_tier_rank INTEGER,
      source_id TEXT,
      concepts_json TEXT NOT NULL DEFAULT '[]',
      topics_json TEXT NOT NULL DEFAULT '[]',
      payload_json TEXT
    )`).run();
    await db.prepare("CREATE TABLE canonical_search_row_concepts (row_id TEXT NOT NULL, concept TEXT NOT NULL, PRIMARY KEY (row_id, concept))").run();
    await db.prepare("CREATE TABLE canonical_search_row_aliases (alias_id TEXT PRIMARY KEY, canonical_id TEXT NOT NULL)").run();
    await db.prepare(`CREATE TABLE related_content_edges (
      relationship_id TEXT PRIMARY KEY,
      source_id TEXT NOT NULL,
      target_id TEXT,
      target_url TEXT,
      target_kind TEXT NOT NULL,
      relationship_type TEXT NOT NULL,
      authority_tier TEXT NOT NULL,
      confidence TEXT NOT NULL,
      review_state TEXT NOT NULL,
      payload_json TEXT NOT NULL
    )`).run();
    await db.prepare("CREATE VIRTUAL TABLE search_rows_fts USING fts5(id UNINDEXED, title, body, concept)").run();
    await db.prepare("CREATE VIRTUAL TABLE canonical_search_rows_fts USING fts5(id UNINDEXED, title, body, concept)").run();
    await db.prepare(`CREATE TABLE rock_issues (
      issue_id TEXT PRIMARY KEY,
      github_node_id TEXT NOT NULL UNIQUE,
      repository TEXT NOT NULL,
      number INTEGER NOT NULL,
      component TEXT NOT NULL,
      state TEXT NOT NULL,
      validation_state TEXT NOT NULL,
      title TEXT NOT NULL,
      url TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      evidence_state TEXT NOT NULL,
      payload_json TEXT NOT NULL
    )`).run();
    await db.prepare("CREATE TABLE rock_issue_locations (location_id TEXT PRIMARY KEY, issue_id TEXT NOT NULL, is_current INTEGER NOT NULL)").run();
    await db.prepare("CREATE TABLE rock_issue_enrichments (enrichment_id TEXT PRIMARY KEY, issue_id TEXT NOT NULL, diagnosis_status TEXT NOT NULL, reviewed_at TEXT NOT NULL, payload_json TEXT NOT NULL)").run();
    await db.prepare(`CREATE TABLE rock_issue_versions (
      issue_id TEXT NOT NULL,
      component TEXT NOT NULL,
      relationship TEXT NOT NULL,
      version TEXT NOT NULL,
      version_line TEXT NOT NULL,
      source_kind TEXT NOT NULL,
      authority_tier TEXT NOT NULL,
      confidence TEXT NOT NULL,
      source_ref TEXT NOT NULL,
      observed_at TEXT NOT NULL DEFAULT '',
      PRIMARY KEY (issue_id, component, relationship, version, source_ref, observed_at)
    )`).run();
    await db.prepare("CREATE TABLE rock_issue_concepts (issue_id TEXT NOT NULL, concept TEXT NOT NULL, PRIMARY KEY (issue_id, concept))").run();
    const row = {
    id: "claim:claim:abc123",
    kind: "claim",
    title: "Check-in labels",
    body: "Check-in label printing uses the configured label surface.",
    path: "claims/approved-claims.jsonl",
    url: "https://example.test/labels",
    concept: "check-in",
    authority_tier: "official",
    claim_tier: "source_backed",
    claim_tier_rank: 1,
    source_id: "rock_documentation",
    payload_json: JSON.stringify({ claim_id: "claim:abc123", claim: "Check-in label printing uses the configured label surface." }),
    };
    await db.prepare(`INSERT INTO search_rows
    (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
      .bind(...Object.values(row)).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind(row.id, row.title, row.body, row.concept).run();
    await db.prepare("INSERT INTO search_row_concepts (row_id, concept) VALUES (?, ?)")
      .bind(row.id, row.concept).run();
    await db.prepare("INSERT INTO search_row_aliases (alias_id, canonical_id) VALUES (?, ?)")
      .bind("claim:claim:abc123:check-in", row.id).run();
    const conceptRows = [
      {
        id: "concept:check-in",
        kind: "concept",
        title: "Check-In",
        body: "Check-in eligibility and availability troubleshooting.",
        path: "knowledge/concepts/check-in/index.md",
        url: "",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "answer_pack_approved",
        claim_tier_rank: 2,
        source_id: "",
        payload_json: "{}",
      },
      {
        id: "answer:answer:check-in:first-checks",
        kind: "answer",
        title: "answer:check-in:first-checks",
        body: "Separate child eligibility from room and schedule availability at check-in.",
        path: "agent/answer-pack.jsonl",
        url: "",
        concept: "check-in",
        authority_tier: "official",
        claim_tier: "answer_pack_approved",
        claim_tier_rank: 2,
        source_id: "",
        payload_json: JSON.stringify({ answer_id: "answer:check-in:first-checks" }),
      },
      {
        id: "concept:workflows",
        kind: "concept",
        title: "Workflows",
        body: "",
        path: "knowledge/concepts/workflows/index.md",
        url: "",
        concept: "workflows",
        authority_tier: "official",
        claim_tier: "answer_pack_approved",
        claim_tier_rank: 2,
        source_id: "",
        payload_json: "{}",
      },
      {
        id: "answer:answer:workflows:first-checks",
        kind: "answer",
        title: "answer:workflows:first-checks",
        body: "Inspect WorkflowType and form configuration first.",
        path: "agent/answer-pack.jsonl",
        url: "",
        concept: "workflows",
        authority_tier: "official",
        claim_tier: "answer_pack_approved",
        claim_tier_rank: 2,
        source_id: "",
        payload_json: JSON.stringify({ answer_id: "answer:workflows:first-checks" }),
      },
    ];
    for (const conceptRow of conceptRows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
        .bind(...Object.values(conceptRow)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(conceptRow.id, conceptRow.title, conceptRow.body, conceptRow.concept).run();
    }
    const groupModelRow = {
      id: "model_map:stable:group",
      kind: "model_map",
      title: "Group Model Map",
      body: "Group model Members property relationship to GroupMember.",
      path: "knowledge/model-map/models/group.md",
      url: "",
      concept: "model-map",
      authority_tier: "source-code-confirmed",
      claim_tier: "source_backed",
      claim_tier_rank: 1,
      source_id: "rock_model_map",
      payload_json: JSON.stringify({ identity: { model_slug: "group", model_name: "Group", model_title: "Group" } }),
    };
    await db.prepare(`INSERT INTO search_rows
      (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
      .bind(...Object.values(groupModelRow)).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind(groupModelRow.id, groupModelRow.title, groupModelRow.body, groupModelRow.concept).run();
    const bucket = await mf.getR2Bucket("KB_ARTIFACTS");
    const recipePath = "agent/recipes.jsonl";
    const recipe = {
      schema: "rock-kb-recipe-v1",
      recipe_id: "oneall:check-in-status-dashboard",
      org_id: "oneall",
      title: "Check-In Status Dashboard",
      summary: "Combine registration, placement, and attendance.",
      version: "1.0.0",
      recipe_kind: "lava_application",
      concept_ids: ["check-in", "event-registration", "lava"],
      authority_tier: "community-reviewed",
      security: { data_access: "read_only" },
      compatibility: {
        tested_rock_versions: ["18"],
        version_matrix: [{ rock_version: "18", status: "verified", notes: [] }],
      },
      implementation: {
        repository_url: "https://github.com/ONE-ALL-Church/RockRMS-OA-Public",
        commit_sha: RECIPE_FIXTURE_COMMIT,
        source_path: "Recipes/check-in-status-dashboard",
        files: [{ path: "README.md", sha256: RECIPE_FIXTURE_SHA }],
      },
    };
    const artifactPrefix = options.artifactPrefix || "versions/test-version";
    await putArtifactSet(bucket, artifactPrefix, {
      [recipePath]: `${JSON.stringify(recipe)}\n`,
      "skills/rock-kb-agent/SKILL.md": SKILL_FIXTURE_CONTENT,
      "skills/rock-kb-agent/manifest.json": JSON.stringify({
        schema: "rock-kb-skill-manifest-v1",
        name: "rock-kb-agent",
        skill_version: "1.0.0",
        published_at: "2026-07-17T00:00:00Z",
        source_repository: "https://github.com/ONE-ALL-Church/rock-agent-kb",
        source_path: "skills/rock-kb-agent/SKILL.md",
        minimum_client_version: "0.13.0",
        restart_required: true,
        update_check_interval_hours: 24,
        default_update_policy: "notify",
        supported_agents: ["codex", "claude", "cursor", "opencode"],
      }),
      "agent/concept-index.jsonl": `${JSON.stringify({ concept_id: "event-registration", title: "Event Registration" })}\n`,
      "knowledge/concepts/event-registration/quickstart.md": "# Event Registration\n",
      "knowledge/concepts/event-registration/index.md": "# Event Registration\n",
      "agent/answer-pack.jsonl": "",
      "agent/concept-task-cards.jsonl": "",
      "agent/concept-release-caveats.jsonl": "",
      "agent/rock-idea-summary.json": JSON.stringify({
        schema: "rock-kb-rock-idea-summary-v1",
        record_count: 1,
        relationships: {
          verification_queue: {
            schema: "rock-kb-rock-idea-verification-queue-summary-v1",
            queue_count: 1,
            by_verification_state: { candidate_review_pending: 1 },
          },
        },
      }),
      "agent/rock-issue-summary.json": JSON.stringify({
        schema: "rock-kb-rock-issue-summary-v1",
        record_count: 1,
        catalog_content_hash: ISSUE_FIXTURE_CATALOG_HASH,
        repositories: { "SparkDevNetwork/Rock": 1, "SparkDevNetwork/Rock.Mobile-Issues": 0 },
      }),
      "agent/lava-contexts.jsonl": [
        {
          schema: "rock-kb-lava-context-v3",
          id: "lava_context:check-in-label-checkout-dynamic-text:checkoutdatetime:fixture",
          context_id: "check-in-label-checkout-dynamic-text",
          context_family: "check-in-label",
          surface_name: "Check-In Label Designer Checkout Dynamic Text",
          surface_type: "label_dynamic_text",
          concept_ids: ["lava", "check-in"],
          root_key: "CheckoutDateTime",
          root_type: "DateTime",
          model_slug: null,
          value_kind: "scalar",
          nested_path: "",
          availability: "source-code-confirmed",
          availability_condition: "The Checkout label data type is selected.",
          may_be_null: false,
          required_setting: "",
          execution_phase: "label_render",
          coverage_status: "complete_for_source_snapshot",
          includes_context_ids: [],
          source_id: "sparkdevnetwork_rock",
          source_url: "https://github.com/SparkDevNetwork/Rock/blob/abc/CheckoutLabelData.cs#L68",
          source_file: "Rock/CheckIn/v2/Labels/CheckoutLabelData.cs",
          source_symbol: "CheckoutLabelData",
          source_line_start: 68,
          source_line_end: 68,
          source_ref: "develop",
          source_commit: "a".repeat(40),
          source_version: "20.0.5",
          available_in_versions: ["19.0.11", "20.0.5"],
          version_observations: [
            {
              rock_version: "19.0.11",
              source_version: "19.0.11",
              source_ref: "release-19.0",
              source_commit: "b".repeat(40),
              source_url: "https://github.com/SparkDevNetwork/Rock/blob/def/CheckoutLabelData.cs#L68",
              root_type: "DateTime",
              model_slug: null,
              value_kind: "scalar",
              availability: "source-code-confirmed",
              availability_condition: "The Checkout label data type is selected.",
              may_be_null: false,
              required_setting: "",
              execution_phase: "label_render",
              needs_live_verification: false,
            },
            {
              rock_version: "20.0.5",
              source_version: "20.0.5",
              source_ref: "develop",
              source_commit: "a".repeat(40),
              source_url: "https://github.com/SparkDevNetwork/Rock/blob/abc/CheckoutLabelData.cs#L68",
              root_type: "DateTime",
              model_slug: null,
              value_kind: "scalar",
              availability: "source-code-confirmed",
              availability_condition: "The Checkout label data type is selected.",
              may_be_null: false,
              required_setting: "",
              execution_phase: "label_render",
              needs_live_verification: false,
            },
          ],
          model_map_links: [],
          notes: "",
          needs_live_verification: false,
        },
        {
          schema: "rock-kb-lava-context-v3",
          id: "lava_context:check-in-label-family-dynamic-text:family:fixture",
          context_id: "check-in-label-family-dynamic-text",
          context_family: "check-in-label",
          surface_name: "Check-In Label Designer Family Dynamic Text",
          surface_type: "label_dynamic_text",
          concept_ids: ["lava", "check-in"],
          root_key: "Family",
          root_type: "Rock.Model.Group",
          model_slug: "group",
          value_kind: "object",
          nested_path: "",
          availability: "source-code-confirmed",
          availability_condition: "The Family label data type is selected.",
          may_be_null: true,
          required_setting: "",
          execution_phase: "label_render",
          coverage_status: "complete_for_source_snapshot",
          includes_context_ids: [],
          source_id: "sparkdevnetwork_rock",
          source_url: "https://github.com/SparkDevNetwork/Rock/blob/abc/FamilyLabelData.cs#L52",
          source_file: "Rock/CheckIn/v2/Labels/FamilyLabelData.cs",
          source_symbol: "FamilyLabelData",
          source_line_start: 52,
          source_line_end: 52,
          source_ref: "develop",
          source_commit: "a".repeat(40),
          source_version: "20.0.5",
          model_map_links: [{ model_slug: "group", model_name: "Group" }],
          notes: "",
          needs_live_verification: false,
        },
      ].map((row) => JSON.stringify(row)).join("\n") + "\n",
      "agent/lava-context-version-diff.jsonl": `${JSON.stringify({
        schema: "rock-kb-lava-context-version-diff-v1",
        id: "lava_context_diff:19.0.11:20.0.5:added:fixture",
        from_version: "19.0.11",
        to_version: "20.0.5",
        change_type: "added",
        context_id: "check-in-label-family-dynamic-text",
        root_key: "Family",
        nested_path: "",
      })}\n`,
    });
    const recipeSearchRow = {
      id: "recipe:oneall:check-in-status-dashboard",
      kind: "recipe",
      title: "Check-In Status Dashboard",
      body: "Reusable registration roster and latest attendance dashboard implementation.",
      path: "knowledge/recipes/oneall/check-in-status-dashboard.md",
      url: "https://github.com/ONE-ALL-Church/RockRMS-OA-Public",
      concept: "check-in",
      authority_tier: "community-reviewed",
      claim_tier: "answer_pack_approved",
      claim_tier_rank: 2,
      source_id: "oneall",
      payload_json: JSON.stringify(recipe),
    };
    await db.prepare(`INSERT INTO search_rows
      (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
      .bind(...Object.values(recipeSearchRow)).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind(recipeSearchRow.id, recipeSearchRow.title, recipeSearchRow.body, recipeSearchRow.concept).run();
    for (const concept of recipe.concept_ids) {
      await db.prepare("INSERT INTO search_row_concepts (row_id, concept) VALUES (?, ?)")
        .bind(recipeSearchRow.id, concept).run();
    }
    await db.prepare("INSERT INTO search_row_aliases (alias_id, canonical_id) VALUES (?, ?)")
      .bind("recipe:oneall:check-in-status-dashboard:check-in", recipeSearchRow.id).run();
    const rockIssue = {
      schema: "rock-kb-rock-issue-v1",
      issue_id: "rock_issue:SparkDevNetwork/Rock#6919",
      github_node_id: "I_fixture_6919",
      source_id: "rock_core_issues",
      repository: "SparkDevNetwork/Rock",
      component: "rock_core",
      number: 6919,
      title: "Azure Blob Storage race causes 100 percent CPU",
      url: "https://github.com/SparkDevNetwork/Rock/issues/6919",
      state: "open",
      validation_state: "reported",
      created_at: "2026-07-15T00:00:00Z",
      updated_at: "2026-07-15T00:00:00Z",
      concept_ids: ["hosting-infrastructure"],
      version_evidence: [{
        component: "rock_core",
        relationship: "reported_affected",
        version: "19.2.0",
        normalized_version: "19.2.0",
        version_line: "19.2",
        source_kind: "issue_form",
        source_ref: "section:rock version",
        authority_tier: "community-unreviewed",
        confidence: "medium",
      }],
      linked_commit_shas: [],
      remediation_state: "none_recorded",
      evidence_state: "report_only",
      authority_tier: "community-unreviewed",
      claim_tier: "routing_context_only",
      needs_live_verification: true,
      reviewed_enrichments: [{
        schema: "rock-kb-rock-issue-enrichment-v1",
        enrichment_id: "rock_issue_enrichment:fixture-6919-v1",
        issue_id: "rock_issue:SparkDevNetwork/Rock#6919",
        diagnosis_status: "source_supported",
        diagnosis_summary: "A reviewed fixture diagnosis.",
        applicability_requirements: [{
          field: "capabilities",
          operator: "contains_all",
          values: ["azure-blob-storage"],
        }],
        risk: {
          level: "high",
          rationale: "The reviewed fixture can exhaust a shared host resource.",
          evidence_refs: ["https://github.com/SparkDevNetwork/Rock/issues/6919"],
          assessed_at: "2026-07-15T00:00:00Z",
        },
        verification_playbook: {
          goal: "Check whether the affected storage capability is enabled.",
          steps: [{
            step_id: "check-storage",
            title: "Check storage configuration",
            method: "configuration_check",
            instructions: "Inspect the configured storage provider without changing it.",
            expected_if_affected: "Azure Blob Storage is configured.",
            expected_if_unaffected: "Another storage provider is configured.",
          }],
          production_safe: true,
        },
        applicability: [{
          assertion_id: "fixture-affected-19.3.1",
          component: "rock_core",
          versions: ["19.3.1"],
          ranges: [],
          status: "affected",
        }],
        issue_updated_at: "2026-07-15T00:00:00Z",
        reviewed_at: "2026-07-15T00:00:00Z",
      }, {
        schema: "rock-kb-rock-issue-enrichment-v1",
        enrichment_id: "rock_issue_enrichment:fixture-6919-stale-v1",
        issue_id: "rock_issue:SparkDevNetwork/Rock#6919",
        diagnosis_status: "source_supported",
        diagnosis_summary: "A stale reviewed fixture diagnosis.",
        applicability: [{
          assertion_id: "fixture-fixed-19.2.0",
          component: "rock_core",
          versions: ["19.2.0"],
          ranges: [],
          status: "fixed",
        }],
        issue_updated_at: "2026-07-14T00:00:00Z",
        reviewed_at: "2026-07-14T01:00:00Z",
      }],
    };
    await db.prepare("INSERT INTO rock_issues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(rockIssue.issue_id, rockIssue.github_node_id, rockIssue.repository, rockIssue.number, rockIssue.component, rockIssue.state,
        rockIssue.validation_state, rockIssue.title, rockIssue.url, rockIssue.updated_at, rockIssue.evidence_state,
        JSON.stringify(rockIssue)).run();
    await db.prepare("INSERT INTO rock_issue_locations VALUES (?, ?, 1)")
      .bind("SparkDevNetwork/Rock#6919", rockIssue.issue_id).run();
    await db.prepare("INSERT INTO rock_issue_locations VALUES (?, ?, 0)")
      .bind("SparkDevNetwork/Rock#6000", rockIssue.issue_id).run();
    await db.prepare("INSERT INTO rock_issue_enrichments VALUES (?, ?, ?, ?, ?)")
      .bind("rock_issue_enrichment:fixture-6919-v1", rockIssue.issue_id, "source_supported", "2026-07-15T00:00:00Z",
        JSON.stringify(rockIssue.reviewed_enrichments[0])).run();
    await db.prepare("INSERT INTO rock_issue_versions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(rockIssue.issue_id, "rock_core", "reported_affected", "19.2.0", "19.2", "issue_form",
        "community-unreviewed", "medium", "section:rock version", "").run();
    await db.prepare("INSERT INTO rock_issue_concepts VALUES (?, ?)")
      .bind(rockIssue.issue_id, "hosting-infrastructure").run();
    const rockIssueSearchRow = {
      id: rockIssue.issue_id,
      kind: "rock_issue",
      title: rockIssue.title,
      body: "Azure Blob Storage race CPU 19.2 hosting infrastructure issue 6919",
      path: "agent/rock-issues.jsonl",
      url: rockIssue.url,
      concept: "hosting-infrastructure",
      authority_tier: "community-unreviewed",
      claim_tier: "routing_context_only",
      claim_tier_rank: 0,
      source_id: "rock_core_issues",
      payload_json: JSON.stringify(rockIssue),
    };
    await db.prepare(`INSERT INTO search_rows
      (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(rockIssueSearchRow)).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind(rockIssueSearchRow.id, rockIssueSearchRow.title, rockIssueSearchRow.body, rockIssueSearchRow.concept).run();
    const rockIdea = {
      schema: "rock-kb-rock-idea-v1",
      idea_id: "rock_idea:2250",
      number: 2250,
      title: "Add days to event duration",
      url: "https://community.rockrms.com/ideas/2250/add-days-to-event-duration",
      category: "Event",
      status: "complete",
      status_label: "Complete",
      vote_count: 7,
      planned_version: "20.0",
      feature_size: "Small",
      concept_ids: ["event-registration"],
      authority_tier: "community-unreviewed",
      claim_tier: "routing_context_only",
      needs_live_verification: true,
      verification: {
        schema: "rock-kb-rock-idea-verification-queue-v1",
        queue_id: "rock_idea_verification:2250",
        idea_id: "rock_idea:2250",
        verification_state: "candidate_review_pending",
        recommended_action: "corroborate_completed_state",
        priority_score: 82,
        priority_band: "medium",
        source_content_hash: "idea-source-hash",
        review_input_hash: "review-input-hash",
        content_hash: "verification-content-hash",
        authority_tier: "community-unreviewed",
        claim_tier: "routing_context_only",
        needs_live_verification: true,
      },
    };
    const rockIdeaSearchRow = {
      id: rockIdea.idea_id,
      kind: "rock_idea",
      title: rockIdea.title,
      body: "Add days event duration idea 2250 Event Complete 20.0 feature request roadmap",
      path: "agent/rock-ideas.jsonl",
      url: rockIdea.url,
      concept: "event-registration",
      authority_tier: "community-unreviewed",
      claim_tier: "routing_context_only",
      claim_tier_rank: 0,
      source_id: "rock_ideas",
      payload_json: JSON.stringify(rockIdea),
    };
    await db.prepare(`INSERT INTO search_rows
      (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(rockIdeaSearchRow)).run();
    await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
      .bind(rockIdeaSearchRow.id, rockIdeaSearchRow.title, rockIdeaSearchRow.body, rockIdeaSearchRow.concept).run();
    await db.prepare("INSERT INTO search_row_concepts (row_id, concept) VALUES (?, ?)")
      .bind(rockIdeaSearchRow.id, "event-registration").run();
    const ideaIssueRelationship = {
      schema: "rock-kb-rock-idea-relationship-v1",
      relationship_id: "rock_idea_relationship:fixture",
      source_id: rockIdea.idea_id,
      target_id: rockIssue.issue_id,
      target_url: rockIssue.url,
      target_kind: "rock_issue",
      relationship_type: "references_issue",
      basis: "explicit_staff_response_link",
      signal: "github_issue",
      evidence_url: rockIdea.url,
      authority_tier: "community-unreviewed",
      confidence: "high",
      review_state: "source_observed",
      needs_live_verification: true,
    };
    await db.prepare("INSERT INTO related_content_edges VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(
        ideaIssueRelationship.relationship_id,
        ideaIssueRelationship.source_id,
        ideaIssueRelationship.target_id,
        ideaIssueRelationship.target_url,
        ideaIssueRelationship.target_kind,
        ideaIssueRelationship.relationship_type,
        ideaIssueRelationship.authority_tier,
        ideaIssueRelationship.confidence,
        ideaIssueRelationship.review_state,
        JSON.stringify(ideaIssueRelationship),
      ).run();
    return mf;
  } catch (error) {
    await mf.dispose();
    throw error;
  }
}

async function putArtifactSet(bucket, artifactPrefix, artifacts) {
  const grouped = new Map();
  for (const [artifactPath, value] of Object.entries(artifacts)) {
    const shard = crypto.createHash("sha256").update(artifactPath).digest("hex").slice(0, 2);
    if (!grouped.has(shard)) grouped.set(shard, {});
    grouped.get(shard)[artifactPath] = value;
  }
  for (const [shard, shardArtifacts] of grouped.entries()) {
    await bucket.put(
      `${artifactPrefix}/artifact-shards/${shard}.json`,
      JSON.stringify({ artifacts: shardArtifacts }),
    );
  }
}

async function mcp(mf, method, params, headers = {}) {
  return (await modernMcp(mf, method, params, headers)).payload;
}

async function modernMcp(mf, method, params, headers = {}, protocolVersion = "2026-07-28") {
  const requestParams = {
    ...params,
    _meta: {
      ...params?._meta,
      ...modernMcpMeta(protocolVersion),
    },
  };
  const response = await mf.dispatchFetch("https://kb.example.test/mcp", {
    method: "POST",
    headers: { ...modernMcpHeaders(method, params, protocolVersion), ...headers },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params: requestParams }),
  });
  return { status: response.status, headers: response.headers, payload: await response.json() };
}

function modernMcpMeta(protocolVersion = "2026-07-28") {
  return {
    "io.modelcontextprotocol/protocolVersion": protocolVersion,
    "io.modelcontextprotocol/clientInfo": { name: "rock-kb-test", version: "1.0.0" },
    "io.modelcontextprotocol/clientCapabilities": {},
  };
}

function modernMcpHeaders(method, params = {}, protocolVersion = "2026-07-28") {
  const headers = {
    "content-type": "application/json",
    accept: "application/json, text/event-stream",
    "mcp-protocol-version": protocolVersion,
    "mcp-method": method,
  };
  if (method === "tools/call" && params.name) {
    headers["mcp-name"] = params.name;
  }
  return headers;
}

async function legacyDirectMcp(mf, method, params, extraHeaders = {}) {
  const response = await mf.dispatchFetch("https://kb.example.test/mcp", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      accept: "application/json, text/event-stream",
      "mcp-protocol-version": "2025-11-25",
      ...extraHeaders,
    },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });
  const raw = await response.text();
  const payload = response.headers.get("content-type")?.includes("text/event-stream")
    ? JSON.parse(raw.split("\n").find((line) => line.startsWith("data: ")).slice(6))
    : JSON.parse(raw);
  return { status: response.status, headers: response.headers, payload };
}

async function streamableMcp(mf, method, params, sessionId = "", extraHeaders = {}) {
  const headers = {
    "content-type": "application/json",
    accept: "application/json, text/event-stream",
    "mcp-protocol-version": "2025-11-25",
    ...extraHeaders,
  };
  if (sessionId) headers["mcp-session-id"] = sessionId;
  const response = await mf.dispatchFetch("https://kb.example.test/mcp/code", {
    method: "POST",
    headers,
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });
  const raw = await response.text();
  const payload = response.headers.get("content-type")?.includes("text/event-stream")
    ? JSON.parse(raw.split("\n").find((line) => line.startsWith("data: ")).slice(6))
    : JSON.parse(raw);
  return { status: response.status, payload, sessionId: response.headers.get("mcp-session-id") || sessionId };
}
