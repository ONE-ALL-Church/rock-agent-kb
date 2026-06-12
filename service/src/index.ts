type JsonRecord = Record<string, unknown>;

type SearchRow = {
  id: string;
  kind: string;
  title: string;
  body?: string;
  path: string;
  url?: string;
  concept?: string;
  authority_tier?: string;
  claim_tier?: string;
  claim_tier_rank?: number;
  source_id?: string;
  payload_json?: string;
};

type ContributionRow = {
  schema?: unknown;
  contribution_id?: unknown;
  org_id?: unknown;
  concept_ids?: unknown;
  contribution_type?: unknown;
  title?: unknown;
  distilled_summary?: unknown;
  source_urls?: unknown;
  source_record_ids?: unknown;
  redaction_attestation?: unknown;
  review_status?: unknown;
  license_attestation?: unknown;
  confidence?: unknown;
  needs_live_verification?: unknown;
};

type ServiceEnv = Omit<Env, "AUTO_MERGE_INTAKE"> & {
  GITHUB_TOKEN?: string;
  ORG_TOKEN_SHA256_JSON?: string;
  AUTO_MERGE_INTAKE?: string;
};

const CLAIM_TIER_RANK: Record<string, number> = {
  routing_context_only: 0,
  source_backed: 1,
  answer_pack_approved: 2,
  live_verified: 3
};

const CONTRIBUTION_TYPES = new Set([
  "task_card",
  "troubleshooting_pattern",
  "release_caveat",
  "entity_note",
  "guide_section",
  "source_link",
  "open_question"
]);

const PUBLIC_REVIEW_STATUSES = new Set(["redaction_reviewed", "approved_for_public_distillation"]);
const CONFIDENCE_VALUES = new Set(["low", "medium", "high", "needs_review"]);
const ALLOWED_CONTRIBUTION_FIELDS = new Set([
  "schema",
  "contribution_id",
  "org_id",
  "org_display_name",
  "concept_ids",
  "contribution_type",
  "title",
  "distilled_summary",
  "source_urls",
  "source_record_ids",
  "redaction_attestation",
  "review_status",
  "license_attestation",
  "confidence",
  "needs_live_verification",
  "created_at",
  "publishability_status",
  "source_review_origin",
  "reviewer_notes"
]);
const PRIVATE_FIELD_NAMES = new Set([
  "raw_text",
  "full_text",
  "content",
  "html",
  "markdown",
  "transcript",
  "media_url",
  "private_path",
  "private_source_paths",
  "private_corpus_pointer"
]);

const PRIVATE_PATH_PREFIXES = [
  "data/review/",
  "data/media/",
  "data/normalized/",
  "data/raw-manifests/",
  "data/index/"
];

const DIRECT_MEDIA_HINTS = [
  ".mp3",
  ".mp4",
  ".m3u8",
  ".mpd",
  "player.vimeo.com",
  "oauth2_token_id=",
  "access_token=",
  "signature="
];

export default {
  async fetch(request: Request, env: ServiceEnv, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    try {
      if (request.method === "OPTIONS") {
        return cors(new Response(null, { status: 204 }));
      }
      if (url.pathname === "/health") {
        return json({ status: "ok", version: await currentVersion(env) });
      }
      if (url.pathname === "/manifest.json") {
        return artifactJson(env, "agent/rock-kb-manifest.json");
      }
      if (url.pathname === "/llms.txt") {
        return artifactText(env, "agent/llms.txt", "text/plain; charset=utf-8");
      }
      if (url.pathname.startsWith("/artifacts/")) {
        const path = decodeURIComponent(url.pathname.slice("/artifacts/".length));
        if (!safeArtifactPath(path)) {
          return json({ error: "invalid_artifact_path" }, 400);
        }
        return artifactText(env, path, contentTypeForPath(path));
      }
      if (url.pathname === "/concepts") {
        return artifactJsonl(env, "agent/concept-index.jsonl");
      }
      if (url.pathname.startsWith("/concepts/") && url.pathname.endsWith(".md")) {
        const conceptId = decodeURIComponent(url.pathname.slice("/concepts/".length, -".md".length));
        return artifactText(env, `knowledge/concepts/${conceptId}/index.md`, "text/markdown; charset=utf-8");
      }
      if (url.pathname === "/search") {
        const query = url.searchParams.get("q") || "";
        const limit = boundedInt(url.searchParams.get("limit"), 10, 1, 50);
        const minTier = url.searchParams.get("min_tier") || "routing_context_only";
        const rows = await search(env, query, limit, minTier);
        ctx.waitUntil(recordUsage(env, "search", query, rows.length));
        return json({ schema: "rock-kb-search-result-v1", query, min_tier: minTier, results: rows });
      }
      if (url.pathname.startsWith("/claims/")) {
        const conceptId = decodeURIComponent(url.pathname.slice("/claims/".length));
        const minTier = url.searchParams.get("min_tier") || "routing_context_only";
        const tier = url.searchParams.get("tier");
        return json({ schema: "rock-kb-claims-result-v1", concept_id: conceptId, claims: await claims(env, conceptId, minTier, tier) });
      }
      if (url.pathname === "/telemetry/summary") {
        return json(await telemetrySummary(env));
      }
      if (url.pathname === "/operations/dashboard") {
        return json(await operationsDashboard(env));
      }
      if (url.pathname === "/mcp" && request.method === "POST") {
        return json(await handleMcp(request, env, ctx));
      }
      if (url.pathname === "/submit" && request.method === "POST") {
        return json(await submitContribution(request, env));
      }
      return json({ error: "not_found" }, 404);
    } catch (error) {
      console.log(JSON.stringify({ level: "error", message: String(error) }));
      return json({ error: "internal_error", message: String(error) }, 500);
    }
  }
};

async function search(env: ServiceEnv, query: string, limit: number, minTier: string): Promise<JsonRecord[]> {
  const fts = buildFtsQuery(query);
  if (!fts) {
    return [];
  }
  const minRank = CLAIM_TIER_RANK[minTier] ?? 0;
  const terms = searchTerms(query);
  const candidateLimit = Math.max(limit * 25, 200);
  const result = await env.KB_DB.prepare(
    `SELECT r.*, bm25(search_rows_fts) AS rank
     FROM search_rows_fts f
     JOIN search_rows r ON r.id = f.id
     WHERE search_rows_fts MATCH ? AND r.claim_tier_rank >= ?
     ORDER BY rank
     LIMIT ?`
  ).bind(fts, minRank, candidateLimit).all<SearchRow & { rank?: number }>();
  return (result.results || [])
    .map((row) => ({ row, score: searchScore(row, terms) }))
    .sort((left, right) => right.score - left.score || String(left.row.id).localeCompare(String(right.row.id)))
    .slice(0, limit)
    .map((item) => publicSearchRow(item.row));
}

async function claims(env: ServiceEnv, conceptId: string, minTier: string, tier: string | null): Promise<JsonRecord[]> {
  const minRank = CLAIM_TIER_RANK[minTier] ?? 0;
  const result = await env.KB_DB.prepare(
    `SELECT * FROM search_rows
     WHERE kind IN ('claim', 'community_contribution') AND concept = ? AND claim_tier_rank >= ?
     ORDER BY id`
  ).bind(conceptId, minRank).all<SearchRow>();
  return (result.results || [])
    .filter((row: SearchRow) => !tier || row.claim_tier === tier)
    .map((row: SearchRow) => parsePayload(row));
}

async function handleMcp(request: Request, env: ServiceEnv, ctx: ExecutionContext): Promise<JsonRecord> {
  const body = await request.json<JsonRecord>();
  const id = body.id ?? null;
  const method = String(body.method || "");
  if (method === "initialize") {
    return { jsonrpc: "2.0", id, result: { protocolVersion: "2025-03-26", serverInfo: { name: "Rock KB", version: await currentVersion(env) }, capabilities: { tools: {} } } };
  }
  if (method === "tools/list") {
    return { jsonrpc: "2.0", id, result: { tools: toolDefinitions() } };
  }
  if (method === "tools/call") {
    const params = asRecord(body.params);
    const name = String(params.name || "");
    const args = asRecord(params.arguments);
    const result = await callTool(name, args, env, request, ctx);
    return { jsonrpc: "2.0", id, result: { content: [{ type: "text", text: JSON.stringify(result) }] } };
  }
  return { jsonrpc: "2.0", id, error: { code: -32601, message: "Method not found" } };
}

async function callTool(name: string, args: JsonRecord, env: ServiceEnv, request: Request, ctx: ExecutionContext): Promise<unknown> {
  if (name === "kb_search") {
    const query = String(args.query || "");
    const limit = boundedInt(args.limit, 10, 1, 50);
    const minTier = String(args.min_tier || "routing_context_only");
    const rows = await search(env, query, limit, minTier);
    ctx.waitUntil(recordUsage(env, "mcp_search", query, rows.length));
    return rows;
  }
  if (name === "kb_manifest") {
    return artifactJsonValue(env, "agent/rock-kb-manifest.json");
  }
  if (name === "kb_list_concepts") {
    return artifactJsonlValue(env, "agent/concept-index.jsonl");
  }
  if (name === "kb_get_concept") {
    const conceptId = String(args.concept_id || "");
    return conceptPackage(env, conceptId);
  }
  if (name === "kb_get_claims") {
    return claims(env, String(args.concept_id || ""), String(args.min_tier || "routing_context_only"), stringOrNull(args.tier));
  }
  if (name === "kb_review_dashboard") {
    return operationsDashboard(env);
  }
  if (name === "kb_submit") {
    return submitContribution(new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(args) }), env);
  }
  throw new Error(`Unknown tool: ${name}`);
}

async function conceptPackage(env: ServiceEnv, conceptId: string): Promise<JsonRecord> {
  const [index, quickstart, guide, answers, tasks, caveats, claimRows] = await Promise.all([
    artifactJsonlValue(env, "agent/concept-index.jsonl"),
    artifactTextValue(env, `knowledge/concepts/${conceptId}/quickstart.md`),
    artifactTextValue(env, `knowledge/concepts/${conceptId}/index.md`),
    artifactJsonlValue(env, "agent/answer-pack.jsonl"),
    artifactJsonlValue(env, "agent/concept-task-cards.jsonl"),
    artifactJsonlValue(env, "agent/concept-release-caveats.jsonl"),
    claims(env, conceptId, "routing_context_only", null)
  ]);
  return {
    concept_id: conceptId,
    index: index.find((row) => row.concept_id === conceptId) || null,
    quickstart,
    guide,
    answers: answers.filter((row) => row.concept_id === conceptId),
    task_cards: tasks.filter((row) => row.concept_id === conceptId),
    release_caveats: caveats.filter((row) => row.concept_id === conceptId),
    claims: claimRows
  };
}

async function submitContribution(request: Request, env: ServiceEnv): Promise<JsonRecord> {
  const body = await request.json<JsonRecord>();
  const orgId = String(body.org_id || "");
  const bundle = Array.isArray(body.bundle) ? body.bundle : [];
  const auth = request.headers.get("Authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice("Bearer ".length).trim() : String(body.token || "");
  if (!orgId || !(await tokenAllowed(env, orgId, token))) {
    return { schema: "rock-kb-submit-result-v1", status: "rejected", errors: ["unauthorized org token"] };
  }
  const org = await registeredOrg(env, orgId);
  if (!org) {
    return { schema: "rock-kb-submit-result-v1", status: "rejected", errors: [`org ${orgId} is not registered`] };
  }
  const errors = validateBundle(bundle, orgId);
  if (errors.length) {
    return { schema: "rock-kb-submit-result-v1", status: "rejected", errors };
  }
  if (!env.GITHUB_TOKEN) {
    return {
      schema: "rock-kb-submit-result-v1",
      status: "validated",
      org_id: orgId,
      row_count: bundle.length,
      next: "GITHUB_TOKEN is not configured, so the Worker validated but did not open a PR."
    };
  }
  return createContributionPullRequest(env, orgId, org, bundle as JsonRecord[]);
}

async function createContributionPullRequest(env: ServiceEnv, orgId: string, org: JsonRecord, bundle: JsonRecord[]): Promise<JsonRecord> {
  const owner = env.GITHUB_OWNER || "ONE-ALL-Church";
  const repo = env.GITHUB_REPO || "rock-agent-kb";
  const timestamp = new Date().toISOString().replace(/[-:.]/g, "").slice(0, 15);
  const branch = `kb-submit/${orgId}/${timestamp}`;
  const baseRef = await github(env, `/repos/${owner}/${repo}/git/ref/heads/main`);
  const sha = asRecord(asRecord(baseRef).object).sha;
  await github(env, `/repos/${owner}/${repo}/git/refs`, "POST", { ref: `refs/heads/${branch}`, sha });
  const path = `community-contributions/${orgId}/bundle-${timestamp}.jsonl`;
  const content = bundle.map((row) => JSON.stringify(row)).join("\n") + "\n";
  await github(env, `/repos/${owner}/${repo}/contents/${encodeURIComponent(path).replace(/%2F/g, "/")}`, "PUT", {
    message: `Submit ${orgId} community contribution bundle`,
    content: btoaUtf8(content),
    branch
  });
  const pr = await github(env, `/repos/${owner}/${repo}/pulls`, "POST", {
    title: `Community contribution from ${orgId}`,
    head: branch,
    base: "main",
    body: `Automated contribution intake for \`${orgId}\`.\n\nRows: ${bundle.length}\n\nValidation passed in the Worker before this PR was opened.`
  });
  const prRecord = asRecord(pr);
  const autoMerge = await maybeEnableAutoMerge(env, owner, repo, orgId, org, prRecord, path);
  return {
    schema: "rock-kb-submit-result-v1",
    status: autoMerge.enabled ? "pr_opened_auto_merge_enabled" : "pr_opened_review_required",
    org_id: orgId,
    row_count: bundle.length,
    pull_request_url: prRecord.html_url,
    auto_merge_enabled: autoMerge.enabled,
    auto_merge_error: autoMerge.error || "",
    auto_merge_skipped_reason: autoMerge.skipped_reason || "",
    auto_merge_checked_path: autoMerge.checked_path || path
  };
}

async function maybeEnableAutoMerge(
  env: ServiceEnv,
  owner: string,
  repo: string,
  orgId: string,
  org: JsonRecord,
  prRecord: JsonRecord,
  expectedPath: string
): Promise<{ enabled: boolean; error?: string; skipped_reason?: string; checked_path?: string }> {
  if (env.AUTO_MERGE_INTAKE !== "true") {
    return { enabled: false, skipped_reason: "AUTO_MERGE_INTAKE is not true.", checked_path: expectedPath };
  }
  const intake = asRecord(org.intake);
  if (intake.auto_merge_allowed !== true) {
    return { enabled: false, skipped_reason: `Org ${orgId} is not approved for auto-merge.`, checked_path: expectedPath };
  }
  const eligibility = await autoMergeEligibility(env, owner, repo, Number(prRecord.number || 0), expectedPath);
  if (!eligibility.allowed) {
    return { enabled: false, skipped_reason: eligibility.reason, checked_path: expectedPath };
  }
  return enableAutoMerge(env, String(prRecord.node_id || ""), expectedPath);
}

async function autoMergeEligibility(
  env: ServiceEnv,
  owner: string,
  repo: string,
  pullNumber: number,
  expectedPath: string
): Promise<{ allowed: boolean; reason: string }> {
  if (!pullNumber) {
    return { allowed: false, reason: "Pull request number was missing from GitHub response." };
  }
  const files = await github(env, `/repos/${owner}/${repo}/pulls/${pullNumber}/files?per_page=100`);
  if (!Array.isArray(files)) {
    return { allowed: false, reason: "GitHub pull-request files response was not an array." };
  }
  if (files.length !== 1) {
    return { allowed: false, reason: `Auto-merge requires exactly one changed file; found ${files.length}.` };
  }
  const file = asRecord(files[0]);
  const filename = String(file.filename || "");
  const status = String(file.status || "");
  if (filename !== expectedPath) {
    return { allowed: false, reason: `Changed file ${filename || "<missing>"} did not match expected path ${expectedPath}.` };
  }
  if (!["added", "modified"].includes(status)) {
    return { allowed: false, reason: `Changed file status ${status || "<missing>"} is not auto-merge eligible.` };
  }
  return { allowed: true, reason: "ok" };
}

async function enableAutoMerge(env: ServiceEnv, pullRequestId: string, checkedPath: string): Promise<{ enabled: boolean; error?: string; checked_path?: string }> {
  if (!pullRequestId) {
    return { enabled: false, error: "Pull request node_id was missing from GitHub response.", checked_path: checkedPath };
  }
  try {
    await githubGraphql(env, `mutation EnableAutoMerge($pullRequestId: ID!) {
      enablePullRequestAutoMerge(input: { pullRequestId: $pullRequestId, mergeMethod: SQUASH }) {
        pullRequest { id }
      }
    }`, { pullRequestId });
    return { enabled: true, checked_path: checkedPath };
  } catch (error) {
    return { enabled: false, error: String(error), checked_path: checkedPath };
  }
}

async function github(env: ServiceEnv, path: string, method = "GET", body?: JsonRecord): Promise<unknown> {
  const response = await fetch(`https://api.github.com${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "rock-agent-kb-service",
      "X-GitHub-Api-Version": "2022-11-28"
    },
    body: body ? JSON.stringify(body) : undefined
  });
  if (!response.ok) {
    throw new Error(`GitHub ${method} ${path} failed: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

async function githubGraphql(env: ServiceEnv, query: string, variables: JsonRecord): Promise<unknown> {
  const response = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "rock-agent-kb-service"
    },
    body: JSON.stringify({ query, variables })
  });
  if (!response.ok) {
    throw new Error(`GitHub GraphQL failed: ${response.status} ${await response.text()}`);
  }
  const payload = await response.json<JsonRecord>();
  const errors = payload.errors;
  if (Array.isArray(errors) && errors.length) {
    throw new Error(`GitHub GraphQL errors: ${JSON.stringify(errors)}`);
  }
  return payload.data;
}

function validateBundle(bundle: unknown[], orgId: string): string[] {
  const errors: string[] = [];
  if (!bundle.length || bundle.length > 200) {
    errors.push("bundle must contain 1 to 200 rows");
  }
  bundle.forEach((value, index) => {
    const row = asRecord(value) as ContributionRow;
    const label = `bundle[${index}]`;
    const required = [
      "schema",
      "contribution_id",
      "org_id",
      "concept_ids",
      "contribution_type",
      "title",
      "distilled_summary",
      "source_urls",
      "source_record_ids",
      "redaction_attestation",
      "review_status",
      "license_attestation",
      "confidence",
      "needs_live_verification"
    ];
    for (const field of required) {
      if ((row as JsonRecord)[field] === undefined || (row as JsonRecord)[field] === null) {
        errors.push(`${label} missing field: ${field}`);
      }
    }
    for (const field of ["concept_ids", "title", "distilled_summary"]) {
      if (isEmpty((row as JsonRecord)[field])) {
        errors.push(`${label} missing field: ${field}`);
      }
    }
    const unknownFields = Object.keys(row as JsonRecord).filter((field) => !ALLOWED_CONTRIBUTION_FIELDS.has(field)).sort();
    if (unknownFields.length) {
      errors.push(`${label} unknown fields: ${unknownFields.join(", ")}`);
    }
    if (row.schema !== "rock-kb-org-contribution-v1") errors.push(`${label} schema must be rock-kb-org-contribution-v1`);
    if (row.org_id !== orgId) errors.push(`${label} org_id must match authenticated org`);
    if (!CONTRIBUTION_TYPES.has(String(row.contribution_type))) errors.push(`${label} invalid contribution_type`);
    if (!PUBLIC_REVIEW_STATUSES.has(String(row.review_status))) errors.push(`${label} public contribution must be redaction reviewed or approved`);
    if (!CONFIDENCE_VALUES.has(String(row.confidence))) errors.push(`${label} invalid confidence`);
    if (typeof row.needs_live_verification !== "boolean") errors.push(`${label} needs_live_verification must be true or false`);
    if (!Array.isArray(row.concept_ids) || row.concept_ids.length === 0) errors.push(`${label} concept_ids must be a non-empty list`);
    if (!Array.isArray(row.source_urls)) errors.push(`${label} source_urls must be a list`);
    if (!Array.isArray(row.source_record_ids)) errors.push(`${label} source_record_ids must be a list`);
    if (Array.isArray(row.source_urls) && Array.isArray(row.source_record_ids) && row.source_urls.length === 0 && row.source_record_ids.length === 0) {
      errors.push(`${label} must include source_urls or source_record_ids`);
    }
    if (Array.isArray(row.source_urls)) {
      for (const url of row.source_urls) {
        if (typeof url !== "string") {
          errors.push(`${label} source_urls must contain strings`);
        } else if (url && hasUnsupportedUrlScheme(url)) {
          errors.push(`${label} source_urls must use http or https URLs`);
        }
      }
    }
    if (!truthyAttestation(row.redaction_attestation)) errors.push(`${label} redaction_attestation must be affirmative`);
    if (!truthyAttestation(row.license_attestation)) errors.push(`${label} license_attestation must be affirmative`);
    errors.push(...findLeaks(row as JsonRecord).map((message) => `${label} ${message}`));
  });
  return errors;
}

function findLeaks(value: JsonRecord): string[] {
  const errors: string[] = [];
  for (const [path, nested] of walk(value)) {
    if (PRIVATE_FIELD_NAMES.has(path.split(".").pop() || "")) {
      errors.push(`contains prohibited public field: ${path}`);
    }
    if (typeof nested === "string") {
      const normalized = nested.replaceAll("\\", "/").toLowerCase();
      if (PRIVATE_PATH_PREFIXES.some((prefix) => normalized.includes(prefix))) {
        errors.push(`contains private path reference at ${path}`);
      }
      if (DIRECT_MEDIA_HINTS.some((hint) => normalized.includes(hint))) {
        errors.push(`contains direct/tokenized media URL at ${path}`);
      }
      if (/(password|secret|api[_-]?key|token)\s*[:=]\s*['"]?[^'"\s]+/i.test(nested)) {
        errors.push(`contains sensitive-looking value at ${path}`);
      }
      if (/(^|[^A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}([^A-Za-z0-9_-]|$)/.test(nested)) {
        errors.push(`contains sensitive-looking value at ${path}`);
      }
      if (/connectionstring\s*[:=]/i.test(nested)) {
        errors.push(`contains sensitive-looking value at ${path}`);
      }
    }
  }
  const summary = String(value.distilled_summary || "");
  if (rawTranscriptMarker(summary)) {
    errors.push("distilled_summary looks like raw transcript text");
  }
  return errors;
}

function* walk(value: unknown, path = "$"): Generator<[string, unknown]> {
  if (Array.isArray(value)) {
    for (let index = 0; index < value.length; index += 1) {
      yield* walk(value[index], `${path}[${index}]`);
    }
  } else if (value && typeof value === "object") {
    for (const [key, nested] of Object.entries(value)) {
      const nextPath = `${path}.${key}`;
      yield [nextPath, nested];
      yield* walk(nested, nextPath);
    }
  }
}

async function tokenAllowed(env: ServiceEnv, orgId: string, token: string): Promise<boolean> {
  if (!token || !env.ORG_TOKEN_SHA256_JSON) {
    return false;
  }
  const mapping = JSON.parse(env.ORG_TOKEN_SHA256_JSON) as Record<string, string>;
  const expected = mapping[orgId] || "";
  const actual = await sha256Hex(token);
  return constantTimeEqual(actual, expected);
}

async function registeredOrg(env: ServiceEnv, orgId: string): Promise<JsonRecord | null> {
  const result = await env.KB_DB.prepare("SELECT payload_json FROM org_registry WHERE org_id = ? AND status = 'reviewed'").bind(orgId).first<{ payload_json: string }>();
  return result ? JSON.parse(result.payload_json) as JsonRecord : null;
}

async function currentVersion(env: ServiceEnv): Promise<string> {
  const result = await env.KB_DB.prepare("SELECT value FROM kb_meta WHERE key = 'current_version'").first<{ value: string }>();
  return result?.value || "unknown";
}

async function artifactKey(env: ServiceEnv, path: string): Promise<string> {
  return `versions/${await currentVersion(env)}/${path}`;
}

async function artifactTextValue(env: ServiceEnv, path: string): Promise<string> {
  const object = await env.KB_ARTIFACTS.get(await artifactKey(env, path));
  if (!object) {
    throw new Error(`Artifact not found: ${path}`);
  }
  return object.text();
}

async function artifactJsonValue(env: ServiceEnv, path: string): Promise<JsonRecord> {
  return JSON.parse(await artifactTextValue(env, path)) as JsonRecord;
}

async function artifactJsonlValue(env: ServiceEnv, path: string): Promise<JsonRecord[]> {
  return (await artifactTextValue(env, path))
    .split("\n")
    .filter((line) => line.trim())
    .map((line) => JSON.parse(line) as JsonRecord);
}

async function artifactText(env: ServiceEnv, path: string, contentType: string): Promise<Response> {
  return new Response(await artifactTextValue(env, path), { headers: { "content-type": contentType } });
}

async function artifactJson(env: ServiceEnv, path: string): Promise<Response> {
  return json(await artifactJsonValue(env, path));
}

async function artifactJsonl(env: ServiceEnv, path: string): Promise<Response> {
  return json({ rows: await artifactJsonlValue(env, path) });
}

async function recordUsage(env: ServiceEnv, event: string, query: string, resultCount: number): Promise<void> {
  await ensureUsageEventsTable(env);
  const hash = query ? await sha256Hex(normalizeQuery(query)) : "";
  const day = new Date().toISOString().slice(0, 10);
  await env.KB_DB.prepare(
    `INSERT INTO usage_events (day, event, query_hash, result_count, count)
     VALUES (?, ?, ?, ?, 1)
     ON CONFLICT(day, event, query_hash, result_count)
     DO UPDATE SET count = count + 1`
  ).bind(day, event, hash, resultCount).run();
}

async function telemetrySummary(env: ServiceEnv): Promise<JsonRecord> {
  await ensureUsageEventsTable(env);
  const result = await env.KB_DB.prepare(
    `SELECT day, event, result_count, SUM(count) AS count
     FROM usage_events
     GROUP BY day, event, result_count
     ORDER BY day DESC, count DESC
     LIMIT 100`
  ).all<JsonRecord>();
  return { schema: "rock-kb-telemetry-summary-v1", rows: result.results || [] };
}

async function ensureUsageEventsTable(env: ServiceEnv): Promise<void> {
  await env.KB_DB.prepare(
    `CREATE TABLE IF NOT EXISTS usage_events (
      day TEXT NOT NULL,
      event TEXT NOT NULL,
      query_hash TEXT,
      result_count INTEGER NOT NULL,
      count INTEGER NOT NULL,
      PRIMARY KEY(day, event, query_hash, result_count)
    )`
  ).run();
}

async function operationsDashboard(env: ServiceEnv): Promise<JsonRecord> {
  const [reviewQueue, conflicts, sectionStatus, evaluationResults, telemetry, communityRows] = await Promise.all([
    artifactJsonlOptional(env, "agent/claim-review-queue.jsonl"),
    artifactJsonlOptional(env, "agent/source-conflicts.jsonl"),
    artifactJsonlOptional(env, "agent/section-status.jsonl"),
    artifactJsonlOptional(env, "agent/evaluation-results.jsonl"),
    telemetrySummary(env),
    communityContributionRows(env)
  ]);
  return {
    schema: "rock-kb-operations-dashboard-v1",
    version: await currentVersion(env),
    review_queue: summarizeReviewQueue(reviewQueue),
    community_contributions: summarizeCommunityContributions(communityRows),
    source_conflicts: summarizeSourceConflicts(conflicts),
    section_status: summarizeSectionStatus(sectionStatus),
    evaluation: summarizeEvaluationResults(evaluationResults),
    telemetry
  };
}

async function artifactJsonlOptional(env: ServiceEnv, path: string): Promise<JsonRecord[]> {
  try {
    return await artifactJsonlValue(env, path);
  } catch (error) {
    console.log(JSON.stringify({ level: "warn", message: `Optional artifact unavailable: ${path}`, error: String(error) }));
    return [];
  }
}

async function communityContributionRows(env: ServiceEnv): Promise<SearchRow[]> {
  const result = await env.KB_DB.prepare(
    `SELECT id, kind, title, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, payload_json
     FROM search_rows
     WHERE kind = 'community_contribution'
     ORDER BY id
     LIMIT 1000`
  ).all<SearchRow>();
  return result.results || [];
}

function summarizeReviewQueue(rows: JsonRecord[]): JsonRecord {
  return {
    row_count: rows.length,
    by_recommended_action: countByField(rows, "recommended_action"),
    by_authority_tier: countByField(rows, "authority_tier"),
    by_concept: countByListField(rows, "concept_ids"),
    top_items: rows.slice(0, 20).map((row) => ({
      claim_id: row.claim_id || "",
      recommended_action: row.recommended_action || "",
      authority_tier: row.authority_tier || "",
      claim_tier: row.claim_tier || "",
      concept_ids: row.concept_ids || []
    }))
  };
}

function summarizeCommunityContributions(rows: SearchRow[]): JsonRecord {
  const payloads = rows.map((row) => ({ row, payload: parsePayload(row) }));
  return {
    row_count: rows.length,
    by_org: countValues(payloads.map(({ row, payload }) => String(payload.org_id || row.source_id || "unknown"))),
    by_concept: countValues(rows.map((row) => row.concept || "unknown")),
    by_authority_tier: countValues(rows.map((row) => row.authority_tier || "unknown")),
    top_items: payloads.slice(0, 20).map(({ row, payload }) => ({
      id: row.id,
      org_id: payload.org_id || row.source_id || "",
      contribution_id: payload.contribution_id || "",
      concept: row.concept || "",
      authority_tier: row.authority_tier || "",
      claim_tier: row.claim_tier || "",
      path: row.path
    }))
  };
}

function summarizeSourceConflicts(rows: JsonRecord[]): JsonRecord {
  return {
    row_count: rows.length,
    by_concept: countByField(rows, "concept_id"),
    by_authority_tiers: countByJoinedListField(rows, "authority_tiers"),
    top_items: rows.slice(0, 20).map((row) => ({
      id: row.id || "",
      concept_id: row.concept_id || "",
      authority_tiers: row.authority_tiers || [],
      community_claim_count: row.community_claim_count || 0,
      higher_authority_claim_count: row.higher_authority_claim_count || 0,
      live_verification_claim_count: row.live_verification_claim_count || 0
    }))
  };
}

function summarizeSectionStatus(rows: JsonRecord[]): JsonRecord {
  const flagged = rows.filter((row) => String(row.status || "current") !== "current");
  return {
    row_count: rows.length,
    by_status: countByField(rows, "status"),
    by_concept: countByField(flagged, "concept_id"),
    flagged_items: flagged.slice(0, 20).map((row) => ({
      concept_id: row.concept_id || "",
      section_id: row.section_id || "",
      heading: row.heading || "",
      status: row.status || "",
      reasons: row.reasons || []
    }))
  };
}

function summarizeEvaluationResults(rows: JsonRecord[]): JsonRecord {
  return {
    row_count: rows.length,
    by_status: countByField(rows, "status"),
    by_concept: countByField(rows, "concept_id"),
    failed_items: rows
      .filter((row) => row.status !== "pass")
      .slice(0, 20)
      .map((row) => ({
        id: row.id || "",
        concept_id: row.concept_id || "",
        answer_id: row.answer_id || "",
        score: row.score || 0,
        missing_terms: row.missing_terms || []
      }))
  };
}

function countByField(rows: JsonRecord[], field: string): JsonRecord {
  return countValues(rows.map((row) => String(row[field] || "unknown")));
}

function countByListField(rows: JsonRecord[], field: string): JsonRecord {
  const values = rows.flatMap((row) => Array.isArray(row[field]) ? (row[field] as unknown[]).map((value) => String(value || "unknown")) : ["unknown"]);
  return countValues(values);
}

function countByJoinedListField(rows: JsonRecord[], field: string): JsonRecord {
  const values = rows.map((row) => Array.isArray(row[field]) ? (row[field] as unknown[]).map(String).sort().join(",") : "unknown");
  return countValues(values);
}

function countValues(values: string[]): JsonRecord {
  const counts: Record<string, number> = {};
  for (const value of values) {
    counts[value] = (counts[value] || 0) + 1;
  }
  return Object.fromEntries(Object.entries(counts).sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0])));
}

function publicSearchRow(row: SearchRow): JsonRecord {
  return {
    id: row.id,
    kind: row.kind,
    title: row.title,
    body: row.kind === "concept" ? "" : row.body || "",
    path: row.path,
    url: row.url || "",
    concept: row.concept || "",
    authority_tier: row.authority_tier || "",
    claim_tier: row.claim_tier || "",
    source_id: row.source_id || "",
    payload: parsePayload(row)
  };
}

function parsePayload(row: SearchRow): JsonRecord {
  if (!row.payload_json) {
    return {};
  }
  return JSON.parse(row.payload_json) as JsonRecord;
}

const SEARCH_STOP_WORDS = new Set([
  "and",
  "are",
  "bad",
  "for",
  "from",
  "how",
  "matter",
  "rock",
  "should",
  "the",
  "troubleshooting",
  "what",
  "when",
  "with"
]);

function buildFtsQuery(query: string): string {
  return searchTerms(query).map((term) => `${term}*`).slice(0, 12).join(" OR ");
}

function searchTerms(query: string): string[] {
  const rawTerms = (query.match(/[A-Za-z0-9_]+/g) || [])
    .map((term) => term.toLowerCase())
    .filter((term) => term.length >= 3 || term === "ai" || term === "tv");
  const filteredTerms = rawTerms.filter((term) => !SEARCH_STOP_WORDS.has(term));
  return Array.from(new Set(filteredTerms.length ? filteredTerms : rawTerms));
}

function searchScore(row: SearchRow & { rank?: number }, queryTerms: string[]): number {
  const conceptTerms = new Set(searchTerms(`${row.concept || ""} ${row.title || ""}`));
  const titleTerms = new Set(searchTerms(row.title || ""));
  const bodyTerms = new Set(searchTerms(row.body || ""));
  const conceptOverlap = overlapCount(queryTerms, conceptTerms);
  const titleOverlap = overlapCount(queryTerms, titleTerms);
  const bodyOverlap = overlapCount(queryTerms, bodyTerms);
  const kindBoost = row.kind === "answer" ? 28 : row.kind === "concept" ? 16 : row.kind === "claim" ? 6 : 2;
  const tierBoost = (row.claim_tier_rank || 0) * 4;
  const rankPenalty = Math.min(Math.max(Number(row.rank || 0), 0), 100);
  return conceptOverlap * 40 + titleOverlap * 20 + bodyOverlap + kindBoost + tierBoost - rankPenalty;
}

function overlapCount(queryTerms: string[], candidateTerms: Set<string>): number {
  return queryTerms.filter((term) => candidateTerms.has(term)).length;
}

function normalizeQuery(query: string): string {
  return searchTerms(query).join(" ");
}

function safeArtifactPath(path: string): boolean {
  return Boolean(path) && !path.startsWith("/") && !path.includes("..") && !path.includes("\\");
}

function contentTypeForPath(path: string): string {
  if (path.endsWith(".json")) {
    return "application/json; charset=utf-8";
  }
  if (path.endsWith(".jsonl")) {
    return "application/x-ndjson; charset=utf-8";
  }
  if (path.endsWith(".md")) {
    return "text/markdown; charset=utf-8";
  }
  if (path.endsWith(".txt")) {
    return "text/plain; charset=utf-8";
  }
  if (path.endsWith(".yaml") || path.endsWith(".yml")) {
    return "application/yaml; charset=utf-8";
  }
  return "text/plain; charset=utf-8";
}

function boundedInt(value: unknown, fallback: number, min: number, max: number): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return fallback;
  }
  return Math.max(min, Math.min(max, Math.floor(parsed)));
}

function stringOrNull(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function asRecord(value: unknown): JsonRecord {
  return value && typeof value === "object" && !Array.isArray(value) ? value as JsonRecord : {};
}

function truthyAttestation(value: unknown): boolean {
  if (value === true) {
    return true;
  }
  return typeof value === "string" && ["true", "yes", "reviewed", "attested", "approved"].includes(value.trim().toLowerCase());
}

function isEmpty(value: unknown): boolean {
  if (value === null || value === undefined || value === "") {
    return true;
  }
  if (Array.isArray(value) && value.length === 0) {
    return true;
  }
  return Boolean(value && typeof value === "object" && !Array.isArray(value) && Object.keys(value).length === 0);
}

function hasUnsupportedUrlScheme(value: string): boolean {
  try {
    const url = new URL(value);
    return !["http:", "https:"].includes(url.protocol);
  } catch {
    return false;
  }
}

function rawTranscriptMarker(text: string): boolean {
  const lowered = text.toLowerCase().replace(/\s+/g, " ").trim();
  return lowered.startsWith("speaker ") || lowered.slice(0, 120).includes(" transcript ");
}

async function sha256Hex(value: string): Promise<string> {
  const data = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function constantTimeEqual(a: string, b: string): boolean {
  const left = new TextEncoder().encode(a);
  const right = new TextEncoder().encode(b);
  const length = Math.max(left.length, right.length);
  let diff = left.length ^ right.length;
  for (let index = 0; index < length; index += 1) {
    diff |= (left[index] || 0) ^ (right[index] || 0);
  }
  return diff === 0;
}

function btoaUtf8(value: string): string {
  const bytes = new TextEncoder().encode(value);
  let binary = "";
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary);
}

function json(value: unknown, status = 200): Response {
  return cors(new Response(JSON.stringify(value, null, 2) + "\n", { status, headers: { "content-type": "application/json; charset=utf-8" } }));
}

function cors(response: Response): Response {
  const headers = new Headers(response.headers);
  headers.set("access-control-allow-origin", "*");
  headers.set("access-control-allow-methods", "GET,POST,OPTIONS");
  headers.set("access-control-allow-headers", "authorization,content-type");
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}

function toolDefinitions(): JsonRecord[] {
  return [
    { name: "kb_search", description: "Search public Rock KB rows with authority and claim tiers.", inputSchema: { type: "object", properties: { query: { type: "string" }, limit: { type: "number" }, min_tier: { type: "string" } }, required: ["query"] } },
    { name: "kb_manifest", description: "Return the public Rock KB manifest.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_list_concepts", description: "List public Rock KB concepts.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_get_concept", description: "Return one concept package.", inputSchema: { type: "object", properties: { concept_id: { type: "string" } }, required: ["concept_id"] } },
    { name: "kb_get_claims", description: "Return claims for a concept, optionally filtered by tier.", inputSchema: { type: "object", properties: { concept_id: { type: "string" }, tier: { type: "string" }, min_tier: { type: "string" } }, required: ["concept_id"] } },
    { name: "kb_review_dashboard", description: "Return public operations counts for review queues, conflicts, community intake, evaluation, and telemetry.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_submit", description: "Validate and submit a community contribution bundle for a registered org.", inputSchema: { type: "object", properties: { org_id: { type: "string" }, bundle: { type: "array" } }, required: ["org_id", "bundle"] } }
  ];
}
