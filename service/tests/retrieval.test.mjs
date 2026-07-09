import assert from "node:assert/strict";
import crypto from "node:crypto";
import test from "node:test";
import { Miniflare } from "miniflare";

const WORKER_BUNDLE = "dist/dry-run/index.js";

test("search is compact by default and exact result expands the row", async () => {
  const mf = await buildWorker();
  try {
    const searchResponse = await mf.dispatchFetch("https://kb.example.test/search?q=check-in%20labels");
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
