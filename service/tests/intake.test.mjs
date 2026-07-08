import assert from "node:assert/strict";
import crypto from "node:crypto";
import test from "node:test";
import { Miniflare } from "miniflare";

const WORKER_BUNDLE = "dist/dry-run/index.js";

test("valid reviewed org bundle opens a PR and enables auto-merge after path gate", async () => {
  const github = githubMock();
  const { mf, token } = await buildWorker({ github });
  try {
    const response = await submitBundle(mf, token, "testorg", [validContribution()]);
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.status, "pr_opened_auto_merge_enabled");
    assert.equal(payload.auto_merge_enabled, true);
    assert.match(payload.auto_merge_checked_path, /^community-contributions\/testorg\/bundle-\d{8}T\d{6}\.jsonl$/);
    assert.deepEqual(github.methods(), ["GET", "POST", "PUT", "POST", "GET", "POST"]);
    assert.equal(github.graphqlCalls.length, 1);
    assert.equal(github.contentBodies.length, 1);
    assert.equal(github.contentBodies[0].branch.startsWith("kb-submit/testorg/"), true);
  } finally {
    await mf.dispose();
  }
});

test("privacy leak validation rejects bundle before GitHub is called", async () => {
  const github = githubMock();
  const { mf, token } = await buildWorker({ github });
  try {
    const row = validContribution({
      contribution_id: "testorg-secret",
      distilled_summary: "This public note accidentally includes api_key=secret-value.",
    });
    const response = await submitBundle(mf, token, "testorg", [row]);
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.status, "rejected");
    assert.deepEqual(github.calls, []);
    assert.equal(payload.errors.some((error) => error.includes("sensitive-looking value")), true);
  } finally {
    await mf.dispose();
  }
});

test("duplicate contribution IDs are rejected before GitHub is called", async () => {
  const github = githubMock();
  const { mf, token } = await buildWorker({ github });
  try {
    const response = await submitBundle(mf, token, "testorg", [validContribution(), validContribution()]);
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.status, "rejected");
    assert.deepEqual(github.calls, []);
    assert.equal(payload.errors.some((error) => error.includes("duplicate contribution_id testorg-source-link-001")), true);
  } finally {
    await mf.dispose();
  }
});

test("auth check validates reviewed org token without opening GitHub", async () => {
  const github = githubMock();
  const { mf, token } = await buildWorker({ github });
  try {
    const response = await mf.dispatchFetch("https://kb.example.test/auth/check", {
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ org_id: "testorg" }),
    });
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.schema, "rock-kb-submit-auth-check-v1");
    assert.equal(payload.status, "ok");
    assert.equal(payload.org_id, "testorg");
    assert.deepEqual(github.calls, []);
  } finally {
    await mf.dispose();
  }
});

test("submit dry run validates bundle without opening GitHub", async () => {
  const github = githubMock();
  const { mf, token } = await buildWorker({ github });
  try {
    const response = await submitBundle(mf, token, "testorg", [validContribution()], { dry_run: true });
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.status, "validated");
    assert.equal(payload.row_count, 1);
    assert.match(payload.next, /Dry run passed/);
    assert.deepEqual(github.calls, []);
  } finally {
    await mf.dispose();
  }
});

test("auto-merge is skipped when GitHub changed-file path differs from expected contribution path", async () => {
  const github = githubMock({ changedFilename: "community-contributions/otherorg/bundle-20260613T000000.jsonl" });
  const { mf, token } = await buildWorker({ github });
  try {
    const response = await submitBundle(mf, token, "testorg", [validContribution()]);
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.status, "pr_opened_review_required");
    assert.equal(payload.auto_merge_enabled, false);
    assert.equal(github.graphqlCalls.length, 0);
    assert.match(payload.auto_merge_skipped_reason, /did not match expected path/);
    assert.match(payload.auto_merge_checked_path, /^community-contributions\/testorg\/bundle-\d{8}T\d{6}\.jsonl$/);
  } finally {
    await mf.dispose();
  }
});

async function buildWorker({ github }) {
  const orgId = "testorg";
  const token = `token-${crypto.randomUUID()}`;
  const tokenHash = crypto.createHash("sha256").update(token).digest("hex");
  const suffix = crypto.randomUUID();
  const mf = new Miniflare({
    modules: true,
    scriptPath: WORKER_BUNDLE,
    d1Databases: { KB_DB: `kb-intake-${suffix}` },
    r2Buckets: { KB_ARTIFACTS: `kb-artifacts-${suffix}` },
    bindings: {
      AUTO_MERGE_INTAKE: "true",
      GITHUB_OWNER: "OWNER",
      GITHUB_REPO: "REPO",
      GITHUB_TOKEN: "github-token-for-test",
      ORG_TOKEN_SHA256_JSON: JSON.stringify({ [orgId]: tokenHash }),
      PUBLIC_BASE_URL: "https://kb.example.test",
    },
    outboundService: github.fetch,
  });
  const db = await mf.getD1Database("KB_DB");
  await db.exec(`
    CREATE TABLE kb_meta (key TEXT PRIMARY KEY, value TEXT);
    INSERT INTO kb_meta (key, value) VALUES ('current_version', 'test-version');
    CREATE TABLE org_registry (org_id TEXT PRIMARY KEY, status TEXT NOT NULL, payload_json TEXT NOT NULL);
  `);
  await db.prepare("INSERT INTO org_registry (org_id, status, payload_json) VALUES (?, 'reviewed', ?)")
    .bind(orgId, JSON.stringify({ org_id: orgId, intake: { auto_merge_allowed: true } }))
    .run();
  return { mf, token };
}

async function submitBundle(mf, token, orgId, bundle, extra = {}) {
  return mf.dispatchFetch("https://kb.example.test/submit", {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ org_id: orgId, bundle, ...extra }),
  });
}

function validContribution(overrides = {}) {
  return {
    schema: "rock-kb-org-contribution-v1",
    contribution_id: "testorg-source-link-001",
    org_id: "testorg",
    concept_ids: ["workflows"],
    contribution_type: "source_link",
    title: "Public workflow source",
    distilled_summary: "A reviewed public source can improve the workflow concept guidance.",
    source_urls: ["https://example.org/rock/workflows"],
    source_record_ids: [],
    redaction_attestation: "yes",
    review_status: "redaction_reviewed",
    license_attestation: "yes",
    confidence: "high",
    needs_live_verification: false,
    ...overrides,
  };
}

function githubMock(options = {}) {
  const calls = [];
  const graphqlCalls = [];
  const contentBodies = [];
  let expectedPath = "";
  return {
    calls,
    graphqlCalls,
    contentBodies,
    methods: () => calls.map((call) => call.method),
    fetch: async (request) => {
      const url = new URL(request.url);
      calls.push({ method: request.method, path: url.pathname, search: url.search });
      if (url.pathname.endsWith("/git/ref/heads/main")) {
        return Response.json({ object: { sha: "base-sha" } });
      }
      if (url.pathname.endsWith("/git/refs")) {
        return Response.json({ ref: "refs/heads/kb-submit/testorg/test" });
      }
      if (url.pathname.includes("/contents/")) {
        expectedPath = decodeURIComponent(url.pathname.split("/contents/")[1]);
        contentBodies.push(await request.json());
        return Response.json({ content: { path: expectedPath } });
      }
      if (url.pathname.endsWith("/pulls")) {
        return Response.json({ number: 123, node_id: "pull-request-node-id", html_url: "https://github.example/pr/123" });
      }
      if (url.pathname.endsWith("/pulls/123/files")) {
        return Response.json([{ filename: options.changedFilename || expectedPath, status: "added" }]);
      }
      if (url.pathname.endsWith("/graphql")) {
        graphqlCalls.push(await request.json());
        return Response.json({ data: { enablePullRequestAutoMerge: { pullRequest: { id: "pull-request-node-id" } } } });
      }
      return Response.json({ error: `Unexpected GitHub mock path: ${url.pathname}` }, { status: 500 });
    },
  };
}
