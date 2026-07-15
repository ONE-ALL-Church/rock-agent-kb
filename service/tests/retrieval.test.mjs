import assert from "node:assert/strict";
import crypto from "node:crypto";
import test from "node:test";
import { Miniflare } from "miniflare";
import { MockAgent } from "undici";

const WORKER_BUNDLE = "dist/dry-run/index.js";
const RECIPE_FIXTURE_CONTENT = "verified recipe fixture\n";
const RECIPE_FIXTURE_SHA = crypto.createHash("sha256").update(RECIPE_FIXTURE_CONTENT).digest("hex");
const RECIPE_FIXTURE_COMMIT = "d8ea54fa67efe40692689fb009561ff96e88bf42";

test("search is compact by default and exact result expands the row", async () => {
  const mf = await buildWorker();
  try {
    const searchResponse = await mf.dispatchFetch("https://kb.example.test/search?q=labels%20printing&limit=1");
    const search = await searchResponse.json();

    assert.equal(searchResponse.status, 200);
    assert.equal(search.schema, "rock-kb-search-result-v2");
    assert.equal(search.detail, "compact");
    assert.equal(search.results.length, 1);
    assert.equal(search.results[0].id, "claim:claim:abc123");
    assert.deepEqual(search.results[0].concepts, ["check-in"]);
    assert.equal(typeof search.results[0].snippet, "string");
    assert.equal(typeof search.results[0].score, "number");
    assert.equal(typeof search.results[0].signals.title_overlap, "number");
    assert.equal("body" in search.results[0], false);
    assert.equal("payload" in search.results[0], false);

    const resultResponse = await mf.dispatchFetch("https://kb.example.test/results/claim%3Aclaim%3Aabc123%3Acheck-in");
    const result = await resultResponse.json();
    assert.equal(result.status, "ok");
    assert.equal(result.requested_result_id, "claim:claim:abc123:check-in");
    assert.equal(result.canonical_result_id, "claim:claim:abc123");
    assert.match(result.result.body, /printing/);
    assert.equal(result.result.payload.claim_id, "claim:abc123");
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
    assert.equal(toolNames.includes("kb_get_result"), true);
    assert.equal(toolNames.includes("kb_get_claim"), true);
    assert.equal(toolNames.includes("kb_report_issue"), true);

    const callResponse = await mcp(mf, "tools/call", { name: "kb_get_claim", arguments: { claim_id: "claim:abc123" } });
    const callResult = JSON.parse(callResponse.result.content[0].text);
    assert.equal(callResult.claim.claim_id, "claim:abc123");
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
    const modelResponse = await mf.dispatchFetch("https://kb.example.test/search?q=In%20the%20Group%20model%20show%20the%20Members%20property&limit=3");
    const modelPayload = await modelResponse.json();
    assert.equal(modelPayload.results[0].id, "model_map:stable:group");

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

    const getResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/6919");
    const get = await getResponse.json();
    assert.equal(get.status, "ok");
    assert.equal(get.issue.body, undefined);
    assert.equal(get.issue.version_evidence[0].normalized_version, "19.2.0");
    assert.equal(get.issue.reviewed_enrichments.length, 1);

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
    assert.equal(assessment.results[0].applicability, "possible");
    assert.equal(assessment.results[0].needs_live_verification, true);

    const reviewedAssessResponse = await mf.dispatchFetch("https://kb.example.test/rock-issues/assess", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ profile: { core_version: "19.3.1", concepts: ["hosting-infrastructure"] }, limit: 10 }),
    });
    const reviewedAssessment = await reviewedAssessResponse.json();
    assert.equal(reviewedAssessment.results[0].applicability, "confirmed");
    assert.deepEqual(reviewedAssessment.results[0].reviewed_assertion_ids, ["fixture-affected-19.3.1"]);

    const tools = await mcp(mf, "tools/list", {});
    const names = tools.result.tools.map((tool) => tool.name);
    assert.equal(names.includes("kb_search_rock_issues"), true);
    assert.equal(names.includes("kb_assess_rock_issues"), true);
    assert.equal(names.includes("kb_plan_rock_issue_investigation"), true);

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
    ];
    for (const row of rows) {
      await db.prepare(`INSERT INTO search_rows
        (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...Object.values(row)).run();
      await db.prepare("INSERT INTO search_rows_fts (id, title, body, concept) VALUES (?, ?, ?, ?)")
        .bind(row.id, row.title, row.body, row.concept).run();
    }

    const query = encodeURIComponent("AI direct database access managed Rock authorization business rules");
    const response = await mf.dispatchFetch(`https://kb.example.test/search?q=${query}&min_tier=answer_pack_approved&limit=5`);
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
    const paraphraseResponse = await mf.dispatchFetch(`https://kb.example.test/search?q=${paraphrase}&min_tier=answer_pack_approved&limit=3`);
    const paraphrasePayload = await paraphraseResponse.json();
    assert.equal(paraphrasePayload.results[0].id, "claim:claim:direct-access:security-permissions");
  } finally {
    await mf.dispose();
  }
});

test("telemetry separates evaluation traffic and records structured feedback without query text", async () => {
  const mf = await buildWorker();
  try {
    await mf.dispatchFetch("https://kb.example.test/search?q=labels", {
      headers: { "x-rock-kb-client": "cli" },
    });
    await mf.dispatchFetch("https://kb.example.test/search?q=prayerzz", {
      headers: { "user-agent": "rock-kb-eval/1.0" },
    });
    await mf.dispatchFetch("https://kb.example.test/search?q=prayerzz", {
      headers: { "x-rock-kb-client": "browser" },
    });
    await mf.dispatchFetch("https://kb.example.test/results/claim%3Aclaim%3Aabc123", {
      headers: { "x-rock-kb-client": "cli" },
    });
    await mf.dispatchFetch("https://kb.example.test/recipes/oneall%3Acheck-in-status-dashboard", {
      headers: { "x-rock-kb-client": "cli" },
    });
    await mcp(mf, "tools/call", { name: "kb_get_claim", arguments: { claim_id: "claim:abc123" } });
    const feedbackResponse = await mf.dispatchFetch("https://kb.example.test/feedback", {
      method: "POST",
      headers: { "content-type": "application/json", "x-rock-kb-client": "cli" },
      body: JSON.stringify({ result_id: "claim:claim:abc123:check-in", rating: -1, reason: "outdated" }),
    });
    assert.equal(feedbackResponse.status, 201);
    const feedbackResult = await feedbackResponse.json();
    assert.equal(feedbackResult.schema, "rock-kb-feedback-result-v2");
    assert.equal(feedbackResult.result_id, "claim:claim:abc123");
    assert.equal(feedbackResult.projection_version, "test-version");

    const telemetryResponse = await mf.dispatchFetch("https://kb.example.test/telemetry/summary");
    const telemetry = await telemetryResponse.json();

    assert.equal(telemetry.schema, "rock-kb-telemetry-summary-v3");
    assert.equal(telemetry.adoption_rows.some((row) => row.client_class === "cli"), true);
    assert.equal(telemetry.evaluation_rows.some((row) => row.client_class === "eval"), true);
    assert.equal(telemetry.zero_result_topics.some((row) => row.topic_hint === "prayer-care"), true);
    assert.equal(telemetry.feedback.some((row) => row.reason === "outdated" && row.rating === -1), true);
    assert.equal(telemetry.feedback.some((row) => row.result_id === "claim:claim:abc123"), true);
    assert.equal(telemetry.result_kinds.some((row) => row.result_kind === "claim" && row.client_class === "cli"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.event === "result_get" && row.client_class === "cli" && row.primary_result_kind === "claim"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.event === "recipe_get" && row.client_class === "cli" && row.primary_result_kind === "recipe"), true);
    assert.equal(telemetry.adoption_rows.some((row) => row.event === "claim_get" && row.client_class === "mcp" && row.primary_result_kind === "claim"), true);
    assert.match(telemetry.privacy, /No raw or hashed query text/);
    assert.equal(JSON.stringify(telemetry).includes("prayerzz"), false);
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
    assert.equal(dashboard.schema, "rock-kb-operations-dashboard-v2");
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
    d1Databases: { KB_DB: `kb-retrieval-${suffix}` },
    r2Buckets: { KB_ARTIFACTS: `kb-artifacts-${suffix}` },
    bindings: { PUBLIC_BASE_URL: "https://kb.example.test" },
    fetchMock: options.fetchMock,
  });
  try {
    const db = await mf.getD1Database("KB_DB");
    await db.prepare("CREATE TABLE kb_meta (key TEXT PRIMARY KEY, value TEXT)").run();
    await db.prepare("INSERT INTO kb_meta (key, value) VALUES ('current_version', 'test-version')").run();
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
    await db.prepare("CREATE VIRTUAL TABLE search_rows_fts USING fts5(id UNINDEXED, title, body, concept)").run();
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
    const shard = crypto.createHash("sha256").update(recipePath).digest("hex").slice(0, 2);
    await bucket.put(`versions/test-version/artifact-shards/${shard}.json`, JSON.stringify({ artifacts: { [recipePath]: `${JSON.stringify(recipe)}\n` } }));
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
        applicability: [{
          assertion_id: "fixture-affected-19.3.1",
          component: "rock_core",
          versions: ["19.3.1"],
          ranges: [],
          status: "affected",
        }],
        reviewed_at: "2026-07-15T00:00:00Z",
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
    return mf;
  } catch (error) {
    await mf.dispose();
    throw error;
  }
}

async function mcp(mf, method, params) {
  const response = await mf.dispatchFetch("https://kb.example.test/mcp", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });
  return response.json();
}
