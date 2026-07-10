import assert from "node:assert/strict";
import crypto from "node:crypto";
import test from "node:test";
import { Miniflare } from "miniflare";

const WORKER_BUNDLE = "dist/dry-run/index.js";

test("search is compact by default and exact result expands the row", async () => {
  const mf = await buildWorker();
  try {
    const searchResponse = await mf.dispatchFetch("https://kb.example.test/search?q=labels%20printing&limit=1");
    const search = await searchResponse.json();

    assert.equal(searchResponse.status, 200);
    assert.equal(search.schema, "rock-kb-search-result-v2");
    assert.equal(search.detail, "compact");
    assert.equal(search.results.length, 1);
    assert.equal(search.results[0].id, "claim:claim:abc123:check-in");
    assert.equal(typeof search.results[0].snippet, "string");
    assert.equal(typeof search.results[0].score, "number");
    assert.equal(typeof search.results[0].signals.title_overlap, "number");
    assert.equal("body" in search.results[0], false);
    assert.equal("payload" in search.results[0], false);

    const resultResponse = await mf.dispatchFetch("https://kb.example.test/results/claim%3Aclaim%3Aabc123%3Acheck-in");
    const result = await resultResponse.json();
    assert.equal(result.status, "ok");
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
    assert.equal(search.results[0].id, "recipe:oneall:check-in-status-dashboard:check-in");

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
    const feedbackResponse = await mf.dispatchFetch("https://kb.example.test/feedback", {
      method: "POST",
      headers: { "content-type": "application/json", "x-rock-kb-client": "cli" },
      body: JSON.stringify({ result_id: "claim:claim:abc123:check-in", rating: -1, reason: "outdated" }),
    });
    assert.equal(feedbackResponse.status, 201);

    const telemetryResponse = await mf.dispatchFetch("https://kb.example.test/telemetry/summary");
    const telemetry = await telemetryResponse.json();

    assert.equal(telemetry.schema, "rock-kb-telemetry-summary-v2");
    assert.equal(telemetry.adoption_rows.some((row) => row.client_class === "cli"), true);
    assert.equal(telemetry.evaluation_rows.some((row) => row.client_class === "eval"), true);
    assert.equal(telemetry.zero_result_topics.some((row) => row.topic_hint === "prayer-care"), true);
    assert.equal(telemetry.feedback.some((row) => row.reason === "outdated" && row.rating === -1), true);
    assert.match(telemetry.privacy, /No raw query text/);
    assert.equal(JSON.stringify(telemetry).includes("prayerzz"), false);
  } finally {
    await mf.dispose();
  }
});

async function buildWorker() {
  const suffix = crypto.randomUUID();
  const mf = new Miniflare({
    modules: true,
    scriptPath: WORKER_BUNDLE,
    d1Databases: { KB_DB: `kb-retrieval-${suffix}` },
    r2Buckets: { KB_ARTIFACTS: `kb-artifacts-${suffix}` },
    bindings: { PUBLIC_BASE_URL: "https://kb.example.test" },
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
      payload_json TEXT
    )`).run();
    await db.prepare("CREATE VIRTUAL TABLE search_rows_fts USING fts5(id UNINDEXED, title, body, concept)").run();
    const row = {
    id: "claim:claim:abc123:check-in",
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
      implementation: { commit_sha: "d8ea54fa67efe40692689fb009561ff96e88bf42" },
    };
    const shard = crypto.createHash("sha256").update(recipePath).digest("hex").slice(0, 2);
    await bucket.put(`versions/test-version/artifact-shards/${shard}.json`, JSON.stringify({ artifacts: { [recipePath]: `${JSON.stringify(recipe)}\n` } }));
    const recipeSearchRow = {
      id: "recipe:oneall:check-in-status-dashboard:check-in",
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
