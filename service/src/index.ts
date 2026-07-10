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
  concepts_json?: string;
  topics_json?: string;
  payload_json?: string;
  snippet?: string;
  rank?: number;
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
  recipe?: unknown;
};

type RecipeSourceFetch = {
  bytes: ArrayBuffer | null;
  actualSha256?: string;
  source: "cache" | "raw_github" | "github_contents_api" | "unavailable";
  cacheStatus: "hit" | "miss";
  attempts: number;
  rawHttpStatus?: number;
  apiHttpStatus?: number;
  error?: string;
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
  "open_question",
  "recipe"
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
  "reviewer_notes",
  "recipe"
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

const FEEDBACK_REASONS = new Set(["helpful", "outdated", "missing", "incorrect", "wrong_route"]);
const TOPIC_HINTS: Array<[string, string[]]> = [
  ["check-in", ["checkin", "check-in", "check in", "kiosk", "label", "attendance"]],
  ["workflows", ["workflow", "actiontype", "trigger"]],
  ["lava", ["lava", "mergefield", "merge", "liquid"]],
  ["mobile", ["mobile", "maui", "shell", "selector"]],
  ["event-registration", ["registration", "registrant", "waitlist"]],
  ["connections", ["connection", "opportunity", "connector"]],
  ["communications", ["communication", "email", "sms", "push"]],
  ["groups", ["group", "groupmember", "grouptype"]],
  ["security-permissions", ["security", "permission", "authorization", "auth"]],
  ["data-views-reports", ["dataview", "report", "sql", "analytics"]],
  ["documents-signatures", ["document", "signature", "esign"]],
  ["hosting-infrastructure", ["hosting", "infrastructure", "server", "database"]],
  ["prayer-care", ["prayer", "care"]],
  ["content-personalization", ["personalize", "personalization", "adaptive message"]],
  ["obsidian-development", ["obsidian", "block action"]],
  ["model-map", ["modelmap", "model", "property", "relationship"]],
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
        const response = await artifactText(env, `knowledge/concepts/${conceptId}/index.md`, "text/markdown; charset=utf-8");
        ctx.waitUntil(recordAccessUsage(env, "concept_get", "concept", 1, classifyClient(request)));
        return response;
      }
      if (url.pathname === "/search") {
        const query = url.searchParams.get("q") || "";
        const limit = boundedInt(url.searchParams.get("limit"), 10, 1, 50);
        const minTier = url.searchParams.get("min_tier") || "routing_context_only";
        const detail = url.searchParams.get("detail") === "full" ? "full" : "compact";
        const kind = url.searchParams.get("kind") || "";
        const rows = await search(env, query, limit, minTier, detail === "full", kind);
        ctx.waitUntil(recordUsage(env, "search", query, rows, classifyClient(request)));
        return json({ schema: "rock-kb-search-result-v2", query, min_tier: minTier, kind: kind || null, detail, results: rows });
      }
      if (url.pathname.startsWith("/results/")) {
        const resultId = decodeURIComponent(url.pathname.slice("/results/".length));
        const result = await getResult(env, resultId);
        if (result.status === "ok") {
          ctx.waitUntil(recordAccessUsage(env, "result_get", String(asRecord(result.result).kind || "unknown"), 1, classifyClient(request)));
        }
        return json(result, result.status === "not_found" ? 404 : 200);
      }
      if (url.pathname === "/model-map/models") {
        const result = await listModelMapModels(env);
        ctx.waitUntil(recordAccessUsage(env, "model_list", "model_map", Number(result.count || 0), classifyClient(request)));
        return json(result);
      }
      if (url.pathname === "/recipes") {
        const result = await listRecipes(env, url.searchParams.get("concept"));
        ctx.waitUntil(recordAccessUsage(env, "recipe_list", "recipe", Number(result.count || 0), classifyClient(request)));
        return json(result);
      }
      if (url.pathname.startsWith("/recipes/") && url.pathname.endsWith("/verify")) {
        const recipeId = decodeURIComponent(url.pathname.slice("/recipes/".length, -"/verify".length));
        const result = await verifyRecipe(env, recipeId, url.searchParams.get("rock_version"));
        if (result.status !== "not_found") {
          ctx.waitUntil(recordAccessUsage(env, "recipe_verify", "recipe", 1, classifyClient(request)));
        }
        return json(result, result.status === "not_found" ? 404 : result.status === "fail" ? 409 : 200);
      }
      if (url.pathname.startsWith("/recipes/")) {
        const recipeId = decodeURIComponent(url.pathname.slice("/recipes/".length));
        const result = await getRecipe(env, recipeId);
        if (result.status === "ok") {
          ctx.waitUntil(recordAccessUsage(env, "recipe_get", "recipe", 1, classifyClient(request)));
        }
        return json(result, result.status === "not_found" ? 404 : 200);
      }
      if (url.pathname.startsWith("/model-map/models/")) {
        const model = decodeURIComponent(url.pathname.slice("/model-map/models/".length));
        const result = await getModelMapModel(env, model, {
          fields: url.searchParams.get("fields"),
          property: url.searchParams.get("property"),
        });
        if (!result) {
          return json({ schema: "rock-kb-model-map-model-result-v1", status: "not_found", model }, 404);
        }
        ctx.waitUntil(recordAccessUsage(env, "model_get", "model_map", 1, classifyClient(request)));
        if ((url.searchParams.get("format") || "json") === "markdown") {
          return text(renderModelMapMarkdown(result), "text/markdown; charset=utf-8");
        }
        return json(result);
      }
      if (url.pathname.startsWith("/claims/id/")) {
        const claimId = decodeURIComponent(url.pathname.slice("/claims/id/".length));
        const result = await getClaim(env, claimId);
        if (result.status === "ok") {
          ctx.waitUntil(recordAccessUsage(env, "claim_get", "claim", 1, classifyClient(request)));
        }
        return json(result, result.status === "not_found" ? 404 : 200);
      }
      if (url.pathname.startsWith("/claims/")) {
        const conceptId = decodeURIComponent(url.pathname.slice("/claims/".length));
        const minTier = url.searchParams.get("min_tier") || "routing_context_only";
        const tier = url.searchParams.get("tier");
        const claimRows = await claims(env, conceptId, minTier, tier);
        ctx.waitUntil(recordAccessUsage(env, "claim_list", "claim", claimRows.length, classifyClient(request)));
        return json({ schema: "rock-kb-claims-result-v1", concept_id: conceptId, claims: claimRows });
      }
      if (url.pathname === "/telemetry/summary") {
        return json(await telemetrySummary(env));
      }
      if (url.pathname === "/feedback" && request.method === "POST") {
        return json(await submitFeedback(request, env), 201);
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
      if (url.pathname === "/auth/check" && request.method === "POST") {
        return json(await checkSubmitAuth(request, env));
      }
      return json({ error: "not_found" }, 404);
    } catch (error) {
      console.log(JSON.stringify({ level: "error", message: String(error) }));
      return json({ error: "internal_error", message: String(error) }, 500);
    }
  }
};

async function search(env: ServiceEnv, query: string, limit: number, minTier: string, full = false, kind = ""): Promise<JsonRecord[]> {
  const fts = buildFtsQuery(query);
  if (!fts) {
    return [];
  }
  const minRank = CLAIM_TIER_RANK[minTier] ?? 0;
  const terms = searchTerms(query);
  const candidateLimit = Math.max(limit * 25, 200);
  const result = await env.KB_DB.prepare(
    `SELECT r.*, bm25(search_rows_fts) AS rank,
            snippet(search_rows_fts, 2, '', '', '...', 28) AS snippet
     FROM search_rows_fts f
     JOIN search_rows r ON r.id = f.id
     WHERE search_rows_fts MATCH ? AND r.claim_tier_rank >= ?
       AND (? = '' OR r.kind = ?)
     ORDER BY rank
     LIMIT ?`
  ).bind(fts, minRank, kind, kind, candidateLimit).all<SearchRow & { rank?: number }>();
  const rowsById = new Map<string, SearchRow & { rank?: number }>();
  for (const row of result.results || []) {
    rowsById.set(row.id, row);
  }
  if (!kind) {
    for (const row of await exactModelMapRows(env, query, minRank)) {
      rowsById.set(row.id, row);
    }
    for (const row of await exactConceptRows(env, query, minRank)) {
      rowsById.set(row.id, row);
    }
  }
  const ranked = Array.from(rowsById.values())
    .map((row) => ({ row, signals: searchSignals(row, terms, query) }))
    .sort((left, right) => Number(right.signals.score || 0) - Number(left.signals.score || 0) || String(left.row.id).localeCompare(String(right.row.id)));
  const seenResultGroups = new Set<string>();
  const collapsed = ranked.filter(({ row }) => {
    const group = searchResultGroup(row);
    if (!group) {
      return true;
    }
    if (seenResultGroups.has(group)) {
      return false;
    }
    seenResultGroups.add(group);
    return true;
  });
  return collapsed
    .slice(0, limit)
    .map((item) => full ? publicResultRow(item.row, item.signals) : publicSearchRow(item.row, item.signals));
}

function searchResultGroup(row: SearchRow): string {
  const payload = parsePayload(row);
  if (row.kind === "recipe") {
    const recipeId = String(payload.recipe_id || "");
    return recipeId ? `recipe:${recipeId}` : "";
  }
  if (row.kind === "lava_context") {
    const contextId = String(payload.context_id || "");
    const rootKey = String(payload.root_key || "").toLowerCase();
    return contextId && rootKey ? `lava_context:${contextId}:${rootKey}` : "";
  }
  return "";
}

async function getResult(env: ServiceEnv, resultId: string): Promise<JsonRecord> {
  const result = await resolveSearchRow(env, resultId);
  if (!result) {
    return { schema: "rock-kb-result-v1", status: "not_found", result_id: resultId };
  }
  return {
    schema: "rock-kb-result-v1",
    status: "ok",
    requested_result_id: resultId,
    canonical_result_id: result.id,
    result: publicResultRow(result),
  };
}

async function getClaim(env: ServiceEnv, requestedId: string): Promise<JsonRecord> {
  const bareId = requestedId.replace(/^claim:/, "");
  const claimId = `claim:${bareId}`;
  if (!/^[A-Za-z0-9._-]+$/.test(bareId)) {
    return { schema: "rock-kb-claim-result-v1", status: "not_found", claim_id: claimId };
  }
  const row = await resolveSearchRow(env, `claim:${claimId}`);
  if (!row || row.kind !== "claim") {
    return { schema: "rock-kb-claim-result-v1", status: "not_found", claim_id: claimId };
  }
  const payload = parsePayload(row);
  return {
    schema: "rock-kb-claim-result-v1",
    status: "ok",
    claim_id: payload.claim_id || claimId,
    concepts: rowConcepts(row),
    claim: payload,
    result_ids: [row.id],
  };
}

async function exactConceptRows(env: ServiceEnv, query: string, minRank: number): Promise<Array<SearchRow & { rank?: number }>> {
  const queryTerms = new Set(searchTerms(query));
  if (!queryTerms.size || !hasConceptNavigationIntent(query)) {
    return [];
  }
  const result = await env.KB_DB.prepare(
    `SELECT *
     FROM search_rows
     WHERE kind IN ('concept', 'answer') AND claim_tier_rank >= ?`
  ).bind(minRank).all<SearchRow>();
  const rows = result.results || [];
  const matchedConcepts = new Set(
    rows
      .filter((row) => row.kind === "concept" && conceptRowMatchesQuery(row, queryTerms))
      .map((row) => row.concept || row.id.replace(/^concept:/, ""))
  );
  return rows
    .filter((row) => row.kind === "concept" ? conceptRowMatchesQuery(row, queryTerms) : rowConcepts(row).some((concept) => matchedConcepts.has(concept)))
    .map((row) => ({ ...row, rank: 0 }));
}

function conceptRowMatchesQuery(row: SearchRow, queryTerms: Set<string>): boolean {
  const titleTerms = searchTerms(row.title || "");
  const overlap = titleTerms.filter((term) => queryTerms.has(term)).length;
  return titleTerms.length > 0 && overlap >= Math.max(1, Math.ceil(titleTerms.length / 2));
}

function hasConceptNavigationIntent(query: string): boolean {
  const normalized = normalizeSearchText(query);
  return normalized.includes("check first")
    || normalized.includes("start with")
    || normalized.includes("live records")
    || normalized.includes("source authority")
    || normalized.includes("caveats")
    || normalized.includes("risks matter")
    || normalized.includes("troubleshoot")
    || normalized.includes("troubleshooting")
    || normalized.includes("answer about");
}

async function exactModelMapRows(env: ServiceEnv, query: string, minRank: number): Promise<Array<SearchRow & { rank?: number }>> {
  if (!normalizeModelLookup(query)) {
    return [];
  }
  const result = await env.KB_DB.prepare(
    `SELECT *
     FROM search_rows
     WHERE kind = 'model_map' AND claim_tier_rank >= ?`
  ).bind(minRank).all<SearchRow>();
  return (result.results || [])
    .filter((row) => exactModelMapBoost(row, query) > 0)
    .map((row) => ({ ...row, rank: 0 }));
}

async function claims(env: ServiceEnv, conceptId: string, minTier: string, tier: string | null): Promise<JsonRecord[]> {
  const minRank = CLAIM_TIER_RANK[minTier] ?? 0;
  const result = await env.KB_DB.prepare(
    `SELECT r.* FROM search_rows r
     JOIN search_row_concepts c ON c.row_id = r.id
     WHERE r.kind IN ('claim', 'community_contribution') AND c.concept = ? AND r.claim_tier_rank >= ?
     ORDER BY r.id`
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
    const rows = await search(env, query, limit, minTier, args.full === true, String(args.kind || ""));
    ctx.waitUntil(recordUsage(env, "search", query, rows, "mcp"));
    return rows;
  }
  if (name === "kb_get_result") {
    const result = await getResult(env, String(args.id || args.result_id || ""));
    if (result.status === "ok") {
      ctx.waitUntil(recordAccessUsage(env, "result_get", String(asRecord(result.result).kind || "unknown"), 1, "mcp"));
    }
    return result;
  }
  if (name === "kb_get_claim") {
    const result = await getClaim(env, String(args.claim_id || ""));
    if (result.status === "ok") ctx.waitUntil(recordAccessUsage(env, "claim_get", "claim", 1, "mcp"));
    return result;
  }
  if (name === "kb_list_models") {
    const result = await listModelMapModels(env);
    ctx.waitUntil(recordAccessUsage(env, "model_list", "model_map", Number(result.count || 0), "mcp"));
    return result;
  }
  if (name === "kb_get_model") {
    const result = await getModelMapModel(env, String(args.model || args.model_slug || ""), {
      fields: stringOrNull(args.fields),
      property: stringOrNull(args.property),
    });
    if (!result) {
      return { schema: "rock-kb-model-map-model-result-v1", status: "not_found", model: String(args.model || args.model_slug || "") };
    }
    ctx.waitUntil(recordAccessUsage(env, "model_get", "model_map", 1, "mcp"));
    return result;
  }
  if (name === "kb_list_recipes") {
    const result = await listRecipes(env, stringOrNull(args.concept_id));
    ctx.waitUntil(recordAccessUsage(env, "recipe_list", "recipe", Number(result.count || 0), "mcp"));
    return result;
  }
  if (name === "kb_get_recipe") {
    const result = await getRecipe(env, String(args.recipe_id || ""));
    if (result.status === "ok") ctx.waitUntil(recordAccessUsage(env, "recipe_get", "recipe", 1, "mcp"));
    return result;
  }
  if (name === "kb_verify_recipe") {
    const result = await verifyRecipe(env, String(args.recipe_id || ""), stringOrNull(args.rock_version));
    if (result.status !== "not_found") ctx.waitUntil(recordAccessUsage(env, "recipe_verify", "recipe", 1, "mcp"));
    return result;
  }
  if (name === "kb_manifest") {
    return artifactJsonValue(env, "agent/rock-kb-manifest.json");
  }
  if (name === "kb_list_concepts") {
    return artifactJsonlValue(env, "agent/concept-index.jsonl");
  }
  if (name === "kb_get_concept") {
    const conceptId = String(args.concept_id || "");
    const result = await conceptPackage(env, conceptId);
    ctx.waitUntil(recordAccessUsage(env, "concept_get", "concept", 1, "mcp"));
    return result;
  }
  if (name === "kb_get_claims") {
    const result = await claims(env, String(args.concept_id || ""), String(args.min_tier || "routing_context_only"), stringOrNull(args.tier));
    ctx.waitUntil(recordAccessUsage(env, "claim_list", "claim", result.length, "mcp"));
    return result;
  }
  if (name === "kb_review_dashboard") {
    return operationsDashboard(env);
  }
  if (name === "kb_feedback") {
    return submitFeedback(new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(args) }), env, "mcp");
  }
  if (name === "kb_submit") {
    return submitContribution(new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(args) }), env);
  }
  throw new Error(`Unknown tool: ${name}`);
}

async function conceptPackage(env: ServiceEnv, conceptId: string): Promise<JsonRecord> {
  const [index, quickstart, guide, answers, tasks, caveats, recipeRows, claimRows] = await Promise.all([
    artifactJsonlValue(env, "agent/concept-index.jsonl"),
    artifactTextValue(env, `knowledge/concepts/${conceptId}/quickstart.md`),
    artifactTextValue(env, `knowledge/concepts/${conceptId}/index.md`),
    artifactJsonlValue(env, "agent/answer-pack.jsonl"),
    artifactJsonlValue(env, "agent/concept-task-cards.jsonl"),
    artifactJsonlValue(env, "agent/concept-release-caveats.jsonl"),
    artifactJsonlValue(env, "agent/recipes.jsonl"),
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
    recipes: recipeRows.filter((row) => Array.isArray(row.concept_ids) && row.concept_ids.includes(conceptId)),
    claims: claimRows
  };
}

async function listModelMapModels(env: ServiceEnv): Promise<JsonRecord> {
  const digests = await artifactJsonlValue(env, "agent/model-map-digests.jsonl");
  return {
    schema: "rock-kb-model-map-model-list-v1",
    count: digests.length,
    models: digests.map((digest) => {
      const identity = asRecord(digest.identity);
      const counts = asRecord(digest.counts);
      return {
        model_slug: identity.model_slug || "",
        model_name: identity.model_name || "",
        model_title: identity.model_title || "",
        model_category: identity.model_category || "",
        rock_version: identity.rock_version || "",
        property_count: counts.properties || 0,
        method_count: counts.methods || 0,
        model_detail_path: identity.model_detail_path || "",
      };
    }).sort((left, right) => String(left.model_name).localeCompare(String(right.model_name)))
  };
}

async function listRecipes(env: ServiceEnv, conceptId: string | null = null): Promise<JsonRecord> {
  let recipes = await artifactJsonlValue(env, "agent/recipes.jsonl");
  if (conceptId) {
    recipes = recipes.filter((recipe) => Array.isArray(recipe.concept_ids) && recipe.concept_ids.includes(conceptId));
  }
  return {
    schema: "rock-kb-recipe-list-v1",
    count: recipes.length,
    recipes: recipes.map((recipe) => ({
      recipe_id: recipe.recipe_id || "",
      title: recipe.title || "",
      summary: recipe.summary || "",
      version: recipe.version || "",
      recipe_kind: recipe.recipe_kind || "",
      concept_ids: recipe.concept_ids || [],
      authority_tier: recipe.authority_tier || "community-unreviewed",
    })),
  };
}

async function getRecipe(env: ServiceEnv, recipeId: string): Promise<JsonRecord> {
  const normalized = recipeId.startsWith("recipe:") ? recipeId.slice("recipe:".length) : recipeId;
  const recipes = await artifactJsonlValue(env, "agent/recipes.jsonl");
  const recipe = recipes.find((row) => String(row.recipe_id || "") === normalized);
  if (!recipe) {
    return { schema: "rock-kb-recipe-result-v1", status: "not_found", recipe_id: normalized };
  }
  return { schema: "rock-kb-recipe-result-v1", status: "ok", recipe };
}

async function verifyRecipe(env: ServiceEnv, recipeId: string, rockVersion: string | null): Promise<JsonRecord> {
  const normalized = recipeId.startsWith("recipe:") ? recipeId.slice("recipe:".length) : recipeId;
  const recipes = await artifactJsonlValue(env, "agent/recipes.jsonl");
  const recipe = recipes.find((row) => String(row.recipe_id || "") === normalized);
  if (!recipe) {
    return { schema: "rock-kb-recipe-verification-v1", status: "not_found", recipe_id: normalized };
  }
  const implementation = asRecord(recipe.implementation);
  const repositoryUrl = String(implementation.repository_url || "");
  const repositoryMatch = repositoryUrl.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+?)(?:\.git)?$/);
  if (!repositoryMatch) {
    return { schema: "rock-kb-recipe-verification-v1", status: "fail", recipe_id: normalized, error: "unsupported repository URL" };
  }
  const [, owner, repository] = repositoryMatch;
  const commit = String(implementation.commit_sha || "");
  const sourcePath = String(implementation.source_path || "").replace(/^\/+|\/+$/g, "");
  const files = Array.isArray(implementation.files) ? implementation.files.map(asRecord) : [];
  const fileChecks = await Promise.all(files.map(async (file) => {
    const path = String(file.path || "");
    const expected = String(file.sha256 || "");
    const source = await fetchRecipeSource(owner, repository, commit, [sourcePath, path].filter(Boolean).join("/"), expected);
    if (!source.bytes) {
      return {
        path,
        status: "unavailable",
        expected_sha256: expected,
        source: source.source,
        cache_status: source.cacheStatus,
        attempts: source.attempts,
        raw_http_status: source.rawHttpStatus,
        api_http_status: source.apiHttpStatus,
        error: source.error,
      };
    }
    const actual = source.actualSha256 || await sha256HexBytes(source.bytes);
    return {
      path,
      status: actual === expected ? "pass" : "fail",
      expected_sha256: expected,
      actual_sha256: actual,
      source: source.source,
      cache_status: source.cacheStatus,
      attempts: source.attempts,
    };
  }));
  const compatibility = recipeCompatibility(recipe, rockVersion);
  const failed = fileChecks.some((row) => row.status === "fail") || compatibility.status === "fail";
  const unavailable = fileChecks.some((row) => row.status === "unavailable");
  return {
    schema: "rock-kb-recipe-verification-v1",
    status: failed ? "fail" : unavailable ? "unavailable" : "pass",
    recipe_id: normalized,
    recipe_version: recipe.version || "",
    pinned_commit: commit,
    compatibility,
    file_checks: fileChecks,
    verifier_files: files.map((file) => String(file.path || "")).filter((path) => path.startsWith("tests/") || path.endsWith(".sql")),
    attestation_count: Array.isArray(recipe.verification_attestations) ? recipe.verification_attestations.length : 0,
    safety: "Verification is read-only and does not execute community recipe code or modify a Rock instance.",
  };
}

async function fetchRecipeSource(owner: string, repository: string, commit: string, path: string, expectedSha256: string): Promise<RecipeSourceFetch> {
  const cacheKey = new Request(
    `https://rock-agent-kb.oneandall.church/__recipe-source-cache/${[owner, repository, commit, ...path.split("/")].map(encodeURIComponent).join("/")}`
  );
  try {
    const cached = await caches.default.match(cacheKey);
    if (cached?.ok) {
      const bytes = await cached.arrayBuffer();
      const actualSha256 = await sha256HexBytes(bytes);
      if (actualSha256 === expectedSha256) {
        return { bytes, actualSha256, source: "cache", cacheStatus: "hit", attempts: 0 };
      }
      await caches.default.delete(cacheKey);
    }
  } catch {
    // Cache availability must not determine whether an immutable recipe can be verified.
  }

  const encodedPath = path.split("/").map(encodeURIComponent).join("/");
  const rawUrl = `https://raw.githubusercontent.com/${owner}/${repository}/${commit}/${encodedPath}`;
  const raw = await fetchRecipeUrl(rawUrl, { "user-agent": "rock-kb-recipe-verify/1.0" });
  let selected = raw;
  let source: RecipeSourceFetch["source"] = "raw_github";
  let attempts = raw.attempts;
  let apiHttpStatus: number | undefined;
  let lastError = raw.error;
  if (!raw.response?.ok) {
    const apiUrl = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repository)}/contents/${encodedPath}?ref=${encodeURIComponent(commit)}`;
    const api = await fetchRecipeUrl(apiUrl, {
      accept: "application/vnd.github.raw+json",
      "user-agent": "rock-kb-recipe-verify/1.0",
      "x-github-api-version": "2022-11-28",
    });
    selected = api;
    source = "github_contents_api";
    attempts += api.attempts;
    apiHttpStatus = api.response?.status;
    lastError = api.error || lastError;
  }
  if (!selected.response?.ok) {
    return {
      bytes: null,
      source: "unavailable",
      cacheStatus: "miss",
      attempts,
      rawHttpStatus: raw.response?.status,
      apiHttpStatus,
      error: lastError,
    };
  }
  const bytes = await selected.response.arrayBuffer();
  const actualSha256 = await sha256HexBytes(bytes);
  if (actualSha256 === expectedSha256) {
    try {
      await caches.default.put(
        cacheKey,
        new Response(bytes.slice(0), {
          status: 200,
          headers: { "cache-control": "public, max-age=2592000", "content-type": "application/octet-stream" },
        })
      );
    } catch {
      // Verification remains valid when the cache is unavailable.
    }
  }
  return {
    bytes,
    actualSha256,
    source,
    cacheStatus: "miss",
    attempts,
    rawHttpStatus: raw.response?.status,
    apiHttpStatus,
  };
}

async function fetchRecipeUrl(sourceUrl: string, headers: Record<string, string>): Promise<{ response: Response | null; attempts: number; error?: string }> {
  let lastResponse: Response | null = null;
  let lastError: unknown = null;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      const response = await fetch(sourceUrl, { headers });
      lastResponse = response;
      if (response.ok || (response.status !== 429 && response.status < 500)) {
        return { response, attempts: attempt + 1 };
      }
    } catch (error) {
      lastError = error;
    }
    if (attempt < 2) await new Promise((resolve) => setTimeout(resolve, 100 * (attempt + 1)));
  }
  return {
    response: lastResponse,
    attempts: 3,
    error: lastError instanceof Error ? lastError.message : lastError ? String(lastError) : undefined,
  };
}

function recipeCompatibility(recipe: JsonRecord, rockVersion: string | null): JsonRecord {
  const compatibility = asRecord(recipe.compatibility);
  if (!rockVersion) return { status: "not_checked", rock_version: null, declared: compatibility };
  const matrix = Array.isArray(compatibility.version_matrix) ? compatibility.version_matrix.map(asRecord) : [];
  const declaration = matrix.find((row) => String(row.rock_version || "") === rockVersion);
  if (declaration) {
    const declaredStatus = String(declaration.status || "");
    return { status: declaredStatus === "unsupported" ? "fail" : declaredStatus === "verified" ? "pass" : "warn", rock_version: rockVersion, declaration };
  }
  const tested = Array.isArray(compatibility.tested_rock_versions) ? compatibility.tested_rock_versions.map(String) : [];
  if (tested.includes(rockVersion)) return { status: "pass", rock_version: rockVersion, declaration: { status: "verified" } };
  return { status: "warn", rock_version: rockVersion, reason: "version lacks a verification declaration" };
}

async function getModelMapModel(env: ServiceEnv, query: string, options: { fields?: string | null; property?: string | null } = {}): Promise<JsonRecord | null> {
  const digests = await artifactJsonlValue(env, "agent/model-map-digests.jsonl");
  const digest = findModelDigest(digests, query);
  if (!digest) {
    return null;
  }
  const selected = selectModelDigest(digest, options.fields, options.property);
  const identity = asRecord(digest.identity);
  return {
    schema: "rock-kb-model-map-model-result-v1",
    status: "ok",
    query,
    matched_model: {
      model_slug: identity.model_slug || "",
      model_name: identity.model_name || "",
      model_title: identity.model_title || "",
    },
    model: selected,
  };
}

function findModelDigest(digests: JsonRecord[], query: string): JsonRecord | null {
  const normalized = normalizeModelLookup(query);
  if (!normalized) {
    return null;
  }
  for (const digest of digests) {
    const identity = asRecord(digest.identity);
    const candidates = [
      identity.model_slug,
      identity.model_name,
      identity.model_title,
      `${identity.model_name || ""} Model Map`,
    ].map((value) => normalizeModelLookup(String(value || "")));
    if (candidates.includes(normalized)) {
      return digest;
    }
  }
  return null;
}

function selectModelDigest(digest: JsonRecord, fieldsValue?: string | null, propertyValue?: string | null): JsonRecord {
  const fields = parseCsv(fieldsValue);
  let selected = fields.length ? selectFields(digest, fields) : { ...digest };
  if (propertyValue) {
    selected = { ...selected, property_matches: findProperties(digest, propertyValue) };
  }
  return selected;
}

function selectFields(digest: JsonRecord, fields: string[]): JsonRecord {
  const aliases: Record<string, string> = {
    required: "required_fields",
    relationships: "relationships",
    diffs: "version_diffs",
    properties: "property_groups",
    property_groups: "property_groups",
    methods: "methods",
    notes: "operational_notes",
  };
  const selected: JsonRecord = {
    schema: digest.schema || "rock-kb-agent-model-map-digest-v1",
    identity: digest.identity,
  };
  for (const rawField of fields) {
    const field = aliases[rawField] || rawField;
    if (field in digest) {
      selected[field] = digest[field];
    }
  }
  return selected;
}

function findProperties(digest: JsonRecord, propertyValue: string): JsonRecord[] {
  const propertyGroups = asRecord(digest.property_groups);
  const normalized = normalizeModelLookup(propertyValue);
  const seen = new Set<string>();
  const matches: JsonRecord[] = [];
  for (const [group, rows] of Object.entries(propertyGroups)) {
    if (!Array.isArray(rows)) {
      continue;
    }
    for (const row of rows) {
      const property = asRecord(row);
      const key = String(property.name || "");
      if (!key || seen.has(`${group}:${key}`)) {
        continue;
      }
      const propertyCandidates = [property.name, property.slug].map((value) => normalizeModelLookup(String(value || "")));
      if (propertyCandidates.includes(normalized) || propertyCandidates.some((candidate) => candidate.includes(normalized))) {
        seen.add(`${group}:${key}`);
        matches.push({ group, ...property });
      }
    }
  }
  return matches;
}

function renderModelMapMarkdown(result: JsonRecord): string {
  const model = asRecord(result.model);
  const identity = asRecord(model.identity);
  const counts = asRecord(model.counts);
  const lines = [
    `# ${identity.model_name || result.query} Model Map`,
    "",
    `- Slug: \`${identity.model_slug || ""}\``,
    `- Rock version: \`${identity.rock_version || "unknown"}\``,
    `- Category: \`${identity.model_category || ""}\``,
    `- Detail path: \`${identity.model_detail_path || ""}\``,
    "",
    "## Counts",
    "",
    `- Properties: ${counts.properties || 0}`,
    `- Database properties: ${counts.database_properties || 0}`,
    `- Lava properties: ${counts.lava_properties || 0}`,
    `- NotMapped properties: ${counts.not_mapped_properties || 0}`,
    `- Methods: ${counts.methods || 0}`,
  ];
  const required = Array.isArray(model.required_fields) ? model.required_fields : [];
  if (required.length) {
    lines.push("", "## Required Fields", "");
    for (const property of required) {
      const row = asRecord(property);
      lines.push(`- \`${row.name || ""}\` - ${row.description || ""}`);
    }
  }
  const notes = Array.isArray(model.operational_notes) ? model.operational_notes : [];
  if (notes.length) {
    lines.push("", "## Operational Notes", "");
    for (const note of notes) {
      lines.push(`- ${note}`);
    }
  }
  return `${lines.join("\n")}\n`;
}

async function submitContribution(request: Request, env: ServiceEnv): Promise<JsonRecord> {
  const body = await request.json<JsonRecord>();
  const orgId = String(body.org_id || "");
  const bundle = Array.isArray(body.bundle) ? body.bundle : [];
  const dryRun = body.dry_run === true;
  const auth = request.headers.get("Authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice("Bearer ".length).trim() : String(body.token || "");
  if (!orgId || !(await tokenAllowed(env, orgId, token))) {
    return submitRejected(["unauthorized org token"], orgId);
  }
  const org = await registeredOrg(env, orgId);
  if (!org) {
    return submitRejected([`org ${orgId} is not registered or is not reviewed`], orgId);
  }
  const errors = validateBundle(bundle, orgId);
  if (errors.length) {
    return submitRejected(errors, orgId);
  }
  if (dryRun) {
    return {
      schema: "rock-kb-submit-result-v1",
      status: "validated",
      org_id: orgId,
      row_count: bundle.length,
      next: "Dry run passed. Re-run without dry_run to open a contribution PR."
    };
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

async function checkSubmitAuth(request: Request, env: ServiceEnv): Promise<JsonRecord> {
  const body = await request.json<JsonRecord>();
  const orgId = String(body.org_id || "");
  const auth = request.headers.get("Authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice("Bearer ".length).trim() : String(body.token || "");
  if (!orgId) {
    return submitRejected(["org_id is required"], "");
  }
  if (!(await tokenAllowed(env, orgId, token))) {
    return submitRejected(["unauthorized org token"], orgId);
  }
  const org = await registeredOrg(env, orgId);
  if (!org) {
    return submitRejected([`org ${orgId} is not registered or is not reviewed`], orgId);
  }
  return {
    schema: "rock-kb-submit-auth-check-v1",
    status: "ok",
    org_id: orgId,
    next: "Auth is valid. Use /submit or rock-kb submit to validate and open a contribution PR."
  };
}

function submitRejected(errors: string[], orgId: string): JsonRecord {
  return {
    schema: "rock-kb-submit-result-v1",
    status: "rejected",
    org_id: orgId,
    errors,
    next: "Use a reviewed org registration and provide the per-org token with Authorization: Bearer <token> or ROCK_KB_TOKEN. Tokens must be delivered outside git and stored only in a secret store."
  };
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
  const seenContributionIds = new Map<string, string>();
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
    const contributionId = String(row.contribution_id || "");
    if (contributionId) {
      const firstLabel = seenContributionIds.get(contributionId);
      if (firstLabel) {
        errors.push(`${label} duplicate contribution_id ${contributionId}; first seen at ${firstLabel}`);
      } else {
        seenContributionIds.set(contributionId, label);
      }
    }
    if (!CONTRIBUTION_TYPES.has(String(row.contribution_type))) errors.push(`${label} invalid contribution_type`);
    if (row.contribution_type === "recipe") {
      const recipe = asRecord(row.recipe);
      if (!row.recipe || Object.keys(recipe).length === 0) {
        errors.push(`${label} recipe contribution requires a recipe object`);
      } else {
        if (recipe.schema !== "rock-kb-recipe-v1") errors.push(`${label} recipe.schema must be rock-kb-recipe-v1`);
        if (recipe.recipe_id !== row.contribution_id) errors.push(`${label} recipe.recipe_id must match contribution_id`);
        if (recipe.org_id !== row.org_id) errors.push(`${label} recipe.org_id must match org_id`);
        if (!Array.isArray(recipe.concept_ids) || recipe.concept_ids.length === 0) errors.push(`${label} recipe.concept_ids must be a non-empty list`);
        const implementation = asRecord(recipe.implementation);
        if (!/^[0-9a-f]{40}$/.test(String(implementation.commit_sha || ""))) errors.push(`${label} recipe implementation requires a 40-character commit_sha`);
        if (!String(implementation.repository_url || "").startsWith("https://github.com/")) errors.push(`${label} recipe repository_url must be an HTTPS GitHub repository`);
      }
    } else if (row.recipe !== undefined) {
      errors.push(`${label} recipe object is only valid for recipe contributions`);
    }
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

async function artifactShardKey(env: ServiceEnv, path: string): Promise<string> {
  const shard = (await sha256Hex(path)).slice(0, 2);
  return `versions/${await currentVersion(env)}/artifact-shards/${shard}.json`;
}

async function artifactTextValue(env: ServiceEnv, path: string): Promise<string> {
  const object = await env.KB_ARTIFACTS.get(await artifactShardKey(env, path));
  if (!object) {
    throw new Error(`Artifact shard not found: ${path}`);
  }
  const shard = JSON.parse(await object.text()) as { artifacts?: Record<string, string> };
  const artifact = shard.artifacts?.[path];
  if (artifact === undefined) {
    throw new Error(`Artifact not found: ${path}`);
  }
  return artifact;
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

async function recordUsage(env: ServiceEnv, event: string, query: string, results: JsonRecord[], clientClass: string): Promise<void> {
  const resultCount = results.length;
  const primaryResultKind = String(results[0]?.kind || "none");
  const kindCounts = countValues(results.map((row) => String(row.kind || "unknown")));
  await recordUsageSummary(env, event, clientClass, queryTopicHint(query), resultCount, primaryResultKind, kindCounts);
}

async function recordAccessUsage(env: ServiceEnv, event: string, resultKind: string, resultCount: number, clientClass: string): Promise<void> {
  const count = Math.max(0, Math.floor(resultCount));
  await recordUsageSummary(
    env,
    event,
    clientClass,
    "unclassified",
    count,
    count > 0 ? resultKind : "none",
    count > 0 ? { [resultKind]: count } : {},
  );
}

async function recordUsageSummary(
  env: ServiceEnv,
  event: string,
  clientClass: string,
  topicHint: string,
  resultCount: number,
  primaryResultKind: string,
  kindCounts: JsonRecord,
): Promise<void> {
  await ensureTelemetryTables(env);
  const day = new Date().toISOString().slice(0, 10);
  await env.KB_DB.prepare(
    `INSERT INTO usage_events_v3 (day, event, client_class, topic_hint, result_count, primary_result_kind, count)
     VALUES (?, ?, ?, ?, ?, ?, 1)
     ON CONFLICT(day, event, client_class, topic_hint, result_count, primary_result_kind)
     DO UPDATE SET count = count + 1`
  ).bind(day, event, clientClass, topicHint, resultCount, primaryResultKind).run();
  for (const [resultKind, count] of Object.entries(kindCounts)) {
    await env.KB_DB.prepare(
      `INSERT INTO usage_result_kinds (day, event, client_class, result_kind, count)
       VALUES (?, ?, ?, ?, ?)
       ON CONFLICT(day, event, client_class, result_kind)
       DO UPDATE SET count = count + excluded.count`
    ).bind(day, event, clientClass, resultKind, Number(count)).run();
  }
}

async function telemetrySummary(env: ServiceEnv): Promise<JsonRecord> {
  await ensureTelemetryTables(env);
  const [result, zeroResults, resultKinds, feedback] = await Promise.all([
    env.KB_DB.prepare(
    `SELECT day, event, client_class, result_count, primary_result_kind, SUM(count) AS count
     FROM usage_events_v3
     GROUP BY day, event, client_class, result_count, primary_result_kind
     ORDER BY day DESC, count DESC
     LIMIT 100`
    ).all<JsonRecord>(),
    env.KB_DB.prepare(
    `SELECT day, topic_hint, SUM(count) AS count
     FROM usage_events_v3
     WHERE result_count = 0 AND client_class <> 'eval' AND topic_hint <> 'unclassified'
     GROUP BY day, topic_hint
     ORDER BY day DESC, count DESC
     LIMIT 50`
    ).all<JsonRecord>(),
    env.KB_DB.prepare(
    `SELECT day, event, client_class, result_kind, SUM(count) AS count
     FROM usage_result_kinds
     GROUP BY day, event, client_class, result_kind
     ORDER BY day DESC, count DESC
     LIMIT 100`
    ).all<JsonRecord>(),
    env.KB_DB.prepare(
    `SELECT day, client_class, result_id, result_kind, projection_version, rating, reason, SUM(count) AS count
     FROM feedback_events_v2
     GROUP BY day, client_class, result_id, result_kind, projection_version, rating, reason
     ORDER BY day DESC, count DESC
     LIMIT 100`
    ).all<JsonRecord>(),
  ]);
  const rows = result.results || [];
  return {
    schema: "rock-kb-telemetry-summary-v3",
    rows,
    adoption_rows: rows.filter((row) => row.client_class !== "eval"),
    evaluation_rows: rows.filter((row) => row.client_class === "eval"),
    zero_result_topics: zeroResults.results || [],
    result_kinds: resultKinds.results || [],
    feedback: feedback.results || [],
    privacy: "No raw or hashed query text and no free-text feedback are retained in current telemetry. Adoption uses aggregate client classes, topic categories, result kinds, counts, and fixed feedback reasons.",
  };
}

async function ensureTelemetryTables(env: ServiceEnv): Promise<void> {
  await env.KB_DB.prepare(
    `CREATE TABLE IF NOT EXISTS usage_events_v3 (
      day TEXT NOT NULL,
      event TEXT NOT NULL,
      client_class TEXT NOT NULL,
      topic_hint TEXT NOT NULL,
      result_count INTEGER NOT NULL,
      primary_result_kind TEXT NOT NULL,
      count INTEGER NOT NULL,
      PRIMARY KEY(day, event, client_class, topic_hint, result_count, primary_result_kind)
    )`
  ).run();
  await env.KB_DB.prepare(
    `CREATE TABLE IF NOT EXISTS usage_result_kinds (
      day TEXT NOT NULL,
      event TEXT NOT NULL,
      client_class TEXT NOT NULL,
      result_kind TEXT NOT NULL,
      count INTEGER NOT NULL,
      PRIMARY KEY(day, event, client_class, result_kind)
    )`
  ).run();
  await env.KB_DB.prepare(
    `CREATE TABLE IF NOT EXISTS usage_events_v2 (
      day TEXT NOT NULL,
      event TEXT NOT NULL,
      client_class TEXT NOT NULL,
      query_hash TEXT NOT NULL,
      topic_hint TEXT NOT NULL,
      result_count INTEGER NOT NULL,
      count INTEGER NOT NULL,
      PRIMARY KEY(day, event, client_class, query_hash, topic_hint, result_count)
    )`
  ).run();
  await env.KB_DB.prepare(
    `CREATE TABLE IF NOT EXISTS feedback_events_v2 (
      day TEXT NOT NULL,
      client_class TEXT NOT NULL,
      result_id TEXT NOT NULL,
      result_kind TEXT NOT NULL,
      projection_version TEXT NOT NULL,
      rating INTEGER NOT NULL,
      reason TEXT NOT NULL,
      count INTEGER NOT NULL,
      PRIMARY KEY(day, client_class, result_id, projection_version, rating, reason)
    )`
  ).run();
  await env.KB_DB.prepare(
    `CREATE TABLE IF NOT EXISTS feedback_events (
      day TEXT NOT NULL,
      client_class TEXT NOT NULL,
      result_id_hash TEXT NOT NULL,
      rating INTEGER NOT NULL,
      reason TEXT NOT NULL,
      count INTEGER NOT NULL,
      PRIMARY KEY(day, client_class, result_id_hash, rating, reason)
    )`
  ).run();
}

async function submitFeedback(request: Request, env: ServiceEnv, forcedClientClass = ""): Promise<JsonRecord> {
  const body = await request.json<JsonRecord>();
  const resultId = String(body.result_id || "").trim();
  const rating = Number(body.rating);
  const reason = String(body.reason || "").trim().toLowerCase();
  if (!resultId || ![-1, 1].includes(rating) || !FEEDBACK_REASONS.has(reason)) {
    throw new Error("feedback requires result_id, rating -1 or 1, and a supported reason");
  }
  const result = await resolveSearchRow(env, resultId);
  if (!result) {
    throw new Error("feedback result_id was not found");
  }
  await ensureTelemetryTables(env);
  const day = new Date().toISOString().slice(0, 10);
  const clientClass = forcedClientClass || classifyClient(request);
  const projectionVersion = await currentVersion(env);
  await env.KB_DB.prepare(
    `INSERT INTO feedback_events_v2 (day, client_class, result_id, result_kind, projection_version, rating, reason, count)
     VALUES (?, ?, ?, ?, ?, ?, ?, 1)
     ON CONFLICT(day, client_class, result_id, projection_version, rating, reason)
     DO UPDATE SET count = count + 1`
  ).bind(day, clientClass, result.id, result.kind, projectionVersion, rating, reason).run();
  return { schema: "rock-kb-feedback-result-v2", status: "recorded", result_id: result.id, projection_version: projectionVersion, rating, reason };
}

function classifyClient(request: Request): string {
  const declared = String(request.headers.get("x-rock-kb-client") || "").trim().toLowerCase();
  if (["cli", "mcp", "browser", "eval"].includes(declared)) {
    return declared;
  }
  const userAgent = String(request.headers.get("user-agent") || "").toLowerCase();
  if (userAgent.includes("rock-kb-eval")) return "eval";
  if (userAgent.includes("rock-kb-cli") || userAgent.includes("rock-kb-client")) return "cli";
  if (userAgent.includes("mozilla/")) return "browser";
  return "unknown";
}

function queryTopicHint(query: string): string {
  const normalized = normalizeSearchText(query).replace(/\s+/g, " ");
  for (const [topic, hints] of TOPIC_HINTS) {
    if (hints.some((hint) => normalized.includes(hint))) {
      return topic;
    }
  }
  return "unclassified";
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
    `SELECT id, kind, title, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, concepts_json, topics_json, payload_json
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
    by_concept: countValues(rows.flatMap((row) => rowConcepts(row).length ? rowConcepts(row) : ["unknown"])),
    by_authority_tier: countValues(rows.map((row) => row.authority_tier || "unknown")),
    top_items: payloads.slice(0, 20).map(({ row, payload }) => ({
      id: row.id,
      org_id: payload.org_id || row.source_id || "",
      contribution_id: payload.contribution_id || "",
      concept: row.concept || "",
      concepts: rowConcepts(row),
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
      .filter((row) => row.status === "fail")
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

function publicSearchRow(row: SearchRow, signals: JsonRecord = {}): JsonRecord {
  return {
    id: row.id,
    kind: row.kind,
    title: row.title,
    snippet: row.snippet || compactSnippet(row.body || ""),
    path: row.path,
    url: row.url || "",
    concept: row.concept || "",
    concepts: rowConcepts(row),
    topics: rowTopics(row),
    authority_tier: row.authority_tier || "",
    claim_tier: row.claim_tier || "",
    source_id: row.source_id || "",
    score: signals.score || 0,
    signals,
  };
}

function publicResultRow(row: SearchRow, signals: JsonRecord = {}): JsonRecord {
  return {
    ...publicSearchRow(row, signals),
    body: row.kind === "concept" ? "" : row.body || "",
    payload: parsePayload(row),
  };
}

function compactSnippet(value: string): string {
  const compact = value.replace(/\s+/g, " ").trim();
  return compact.length <= 280 ? compact : `${compact.slice(0, 277)}...`;
}

function parsePayload(row: SearchRow): JsonRecord {
  if (!row.payload_json) {
    return {};
  }
  return JSON.parse(row.payload_json) as JsonRecord;
}

function rowConcepts(row: SearchRow): string[] {
  if (row.concepts_json) {
    try {
      const parsed = JSON.parse(row.concepts_json);
      if (Array.isArray(parsed)) {
        const concepts = Array.from(new Set(parsed.map((value) => String(value || "").trim()).filter(Boolean)));
        if (concepts.length) return concepts;
      }
    } catch {
      // Fall through to the legacy primary concept.
    }
  }
  return row.concept ? [row.concept] : [];
}

function rowTopics(row: SearchRow): string[] {
  if (!row.topics_json) return [];
  try {
    const parsed = JSON.parse(row.topics_json);
    if (Array.isArray(parsed)) {
      return Array.from(new Set(parsed.map((value) => String(value || "").trim()).filter(Boolean)));
    }
  } catch {
    return [];
  }
  return [];
}

async function resolveSearchRow(env: ServiceEnv, resultId: string): Promise<SearchRow | null> {
  const direct = await env.KB_DB.prepare("SELECT * FROM search_rows WHERE id = ? LIMIT 1").bind(resultId).first<SearchRow>();
  if (direct) return direct;
  return env.KB_DB.prepare(
    `SELECT r.* FROM search_row_aliases a
     JOIN search_rows r ON r.id = a.canonical_id
     WHERE a.alias_id = ? LIMIT 1`
  ).bind(resultId).first<SearchRow>();
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
  "use",
  "what",
  "when",
  "with"
]);

const LAVA_CONTEXT_QUERY_INTENT_TERMS = new Set([
  "context",
  "contexts",
  "field",
  "fields",
  "lava",
  "merge",
  "root",
  "roots",
  "syntax",
  "template",
  "templates",
]);

const RECIPE_QUERY_INTENT_TERMS = new Set([
  "build",
  "code",
  "create",
  "example",
  "implement",
  "implementation",
  "recipe",
]);

function buildFtsQuery(query: string): string {
  return searchTerms(query).map((term) => `${term}*`).slice(0, 12).join(" OR ");
}

function searchTerms(query: string): string[] {
  const rawTerms = (query.match(/[A-Za-z0-9_]+/g) || [])
    .map(normalizeSearchTerm)
    .filter((term) => term.length >= 3 || term === "ai" || term === "tv");
  const filteredTerms = rawTerms.filter((term) => !SEARCH_STOP_WORDS.has(term));
  return Array.from(new Set(filteredTerms.length ? filteredTerms : rawTerms));
}

function normalizeSearchTerm(value: string): string {
  const term = value.toLowerCase();
  const aliases: Record<string, string> = {
    agent: "ai",
    agents: "ai",
    avalable: "availability",
    available: "availability",
    eligable: "eligibility",
    eligible: "eligibility",
    personalize: "personalization",
    personalized: "personalization",
    developer: "develop",
    development: "develop",
    workflows: "workflow",
    requests: "request",
    checkin: "check",
  };
  if (aliases[term]) return aliases[term];
  if (term.length > 4 && term.endsWith("s") && !term.endsWith("ss")) return term.slice(0, -1);
  return term;
}

function searchSignals(row: SearchRow & { rank?: number }, queryTerms: string[], query: string): JsonRecord {
  const concepts = rowConcepts(row);
  const topics = rowTopics(row);
  const conceptTerms = new Set(searchTerms(`${concepts.join(" ")} ${row.title || ""}`));
  const topicTerms = new Set(searchTerms(topics.join(" ")));
  const titleTerms = new Set(searchTerms(row.title || ""));
  const bodyTerms = new Set(searchTerms(row.body || ""));
  const conceptOverlap = overlapCount(queryTerms, conceptTerms);
  const topicOverlap = overlapCount(queryTerms, topicTerms);
  const titleOverlap = overlapCount(queryTerms, titleTerms);
  const bodyOverlap = overlapCount(queryTerms, bodyTerms);
  const conceptPhraseBoost = Math.max(0, ...concepts.map((concept) => phraseMatchBoost(query, concept, 48)));
  const titlePhraseBoost = phraseMatchBoost(query, row.title || "", 24);
  const bodyExactPhraseBoost = bodyPhraseBoost(row, queryTerms);
  const kindBoost = kindIntentBoost(row, queryTerms);
  const modelMapExactBoost = exactModelMapBoost(row, query);
  const lavaContextRootBoost = exactLavaContextRootBoost(row, queryTerms, query);
  const conceptIntent = conceptIntentBoost(row, queryTerms, query);
  const routeIntent = concepts.includes(queryTopicHint(query)) ? 80 : 0;
  const tierBoost = (row.claim_tier_rank || 0) * 4;
  const lexicalCoverage = bodyOverlap / Math.max(1, queryTerms.length);
  const lexicalCoverageBoost = lexicalCoverage >= 0.75 ? 120 : lexicalCoverage >= 0.5 ? 40 : 0;
  // FTS5 negates BM25 so stronger matches have numerically lower values.
  const bm25Relevance = Math.min(Math.max(-Number(row.rank || 0), 0), 60);
  const score = conceptOverlap * 40 + topicOverlap * 4 + titleOverlap * 20 + bodyOverlap + conceptPhraseBoost + titlePhraseBoost + bodyExactPhraseBoost + kindBoost + modelMapExactBoost + lavaContextRootBoost + conceptIntent + routeIntent + tierBoost + lexicalCoverageBoost + bm25Relevance;
  return {
    score,
    title_overlap: titleOverlap,
    body_overlap: bodyOverlap,
    concept_overlap: conceptOverlap,
    topic_overlap: topicOverlap,
    lexical_coverage: Number(lexicalCoverage.toFixed(4)),
    lexical_coverage_boost: lexicalCoverageBoost,
    phrase_boost: conceptPhraseBoost + titlePhraseBoost + bodyExactPhraseBoost,
    exact_lookup_boost: modelMapExactBoost + lavaContextRootBoost + conceptIntent + routeIntent,
    authority_boost: tierBoost,
    bm25_rank: Number(row.rank || 0),
    bm25_relevance: bm25Relevance,
  };
}

function kindIntentBoost(row: SearchRow, queryTerms: string[]): number {
  if (row.kind === "recipe") {
    return queryTerms.some((term) => RECIPE_QUERY_INTENT_TERMS.has(term)) ? 30 : 4;
  }
  if (row.kind === "lava_context") {
    return queryTerms.some((term) => LAVA_CONTEXT_QUERY_INTENT_TERMS.has(term)) ? 20 : 4;
  }
  if (row.kind === "answer") return 14;
  if (row.kind === "concept") return 10;
  if (row.kind === "claim") return 6;
  return 2;
}

function conceptIntentBoost(row: SearchRow, queryTerms: string[], query: string): number {
  if (!["concept", "answer"].includes(row.kind) || !hasConceptNavigationIntent(query)) return 0;
  const terms = new Set(queryTerms);
  const concepts = rowConcepts(row).join(" ");
  const conceptTerms = searchTerms(row.kind === "answer" ? concepts : `${concepts} ${row.title || ""}`);
  const overlap = conceptTerms.filter((term) => terms.has(term)).length;
  return overlap >= Math.max(1, Math.ceil(conceptTerms.length / 2)) ? 90 + overlap * 12 : 0;
}

function exactModelMapBoost(row: SearchRow, query: string): number {
  if (row.kind !== "model_map") {
    return 0;
  }
  const payload = parsePayload(row);
  const identity = asRecord(payload.identity || payload);
  const lookupQueries = modelLookupQueries(query);
  if (!lookupQueries.length) {
    return 0;
  }
  const candidates = [
    identity.model_slug,
    identity.model_name,
    identity.model_title,
    `${identity.model_name || ""} Model Map`,
    row.id.replace(/^model_map:stable:/, ""),
    row.title,
    row.path.split("/").pop()?.replace(/\.md$/, ""),
  ].map((value) => normalizeModelLookup(String(value || ""))).filter(Boolean);
  return lookupQueries.some((lookup) => candidates.includes(lookup)) ? 500 : 0;
}

function exactLavaContextRootBoost(row: SearchRow, queryTerms: string[], query: string): number {
  if (row.kind !== "lava_context") {
    return 0;
  }
  if (!hasLavaContextQueryIntent(queryTerms)) {
    return 0;
  }
  const payload = parsePayload(row);
  const rootKey = String(payload.root_key || "");
  if (!rootKey) {
    return 0;
  }
  const aliases = [rootKey, spacedSearchAlias(rootKey)].filter(Boolean);
  const rootTerms = new Set(searchTerms(aliases.join(" ")));
  const rootOverlap = overlapCount(queryTerms, rootTerms);
  if (rootOverlap === 0) {
    return 0;
  }
  return rootOverlap * 70 + Math.max(...aliases.map((alias) => phraseMatchBoost(query, alias, 90)));
}

function hasLavaContextQueryIntent(queryTerms: string[]): boolean {
  return queryTerms.some((term) => LAVA_CONTEXT_QUERY_INTENT_TERMS.has(term));
}

function overlapCount(queryTerms: string[], candidateTerms: Set<string>): number {
  return queryTerms.filter((term) => candidateTerms.has(term)).length;
}

function phraseMatchBoost(query: string, candidate: string, boost: number): number {
  const queryText = normalizeSearchText(query);
  const candidateWords = searchTerms(candidate.replace(/[-_/]+/g, " "));
  if (!queryText || candidateWords.length === 0) {
    return 0;
  }
  if (queryText.includes(candidateWords.join(" "))) {
    return boost;
  }
  return candidateWords.every((term) => queryText.split(" ").includes(term)) ? Math.floor(boost * 0.75) : 0;
}

function bodyPhraseBoost(row: SearchRow, queryTerms: string[]): number {
  if (queryTerms.length < 2 || !row.body) {
    return 0;
  }
  const body = normalizeSearchText(row.body);
  for (let size = Math.min(4, queryTerms.length); size >= 2; size -= 1) {
    for (let index = 0; index <= queryTerms.length - size; index += 1) {
      if (body.includes(queryTerms.slice(index, index + size).join(" "))) {
        return row.kind === "claim" ? 72 : 18;
      }
    }
  }
  return 0;
}

function normalizeSearchText(value: string): string {
  return (value.match(/[A-Za-z0-9_]+/g) || [])
    .map((term) => term.toLowerCase())
    .join(" ");
}

function spacedSearchAlias(value: string): string {
  return value
    .replace(/[-_/]+/g, " ")
    .replace(/([a-z0-9])(?=[A-Z])/g, "$1 ")
    .replace(/([A-Z])(?=[A-Z][a-z])/g, "$1 ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeQuery(query: string): string {
  return searchTerms(query).join(" ");
}

function normalizeModelLookup(value: string): string {
  const words = (value.match(/[A-Za-z0-9_]+/g) || [])
    .map(normalizeSearchTerm)
    .filter((term) => term !== "model" && term !== "map" && term !== "modelmap");
  return words.join(" ").trim();
}

function modelLookupQueries(value: string): string[] {
  const queries = new Set<string>();
  const full = normalizeModelLookup(value);
  if (full) queries.add(full);
  for (const match of value.matchAll(/\b([A-Za-z][A-Za-z0-9_-]*)\s+model(?:\s+map)?\b/gi)) {
    const captured = normalizeModelLookup(match[1]);
    if (captured) queries.add(captured);
  }
  return Array.from(queries);
}

function parseCsv(value?: string | null): string[] {
  return String(value || "")
    .split(",")
    .map((part) => part.trim().toLowerCase())
    .filter(Boolean);
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
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
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

async function sha256HexBytes(value: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", value);
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

function text(value: string, contentType = "text/plain; charset=utf-8", status = 200): Response {
  return cors(new Response(value, { status, headers: { "content-type": contentType } }));
}

function cors(response: Response): Response {
  const headers = new Headers(response.headers);
  headers.set("access-control-allow-origin", "*");
  headers.set("access-control-allow-methods", "GET,POST,OPTIONS");
  headers.set("access-control-allow-headers", "authorization,content-type,x-rock-kb-client");
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}

function toolDefinitions(): JsonRecord[] {
  return [
    { name: "kb_search", description: "Start here for any Rock question. Returns compact ranked results; use kb_get_result or kb_get_claim for full detail.", inputSchema: { type: "object", properties: { query: { type: "string" }, limit: { type: "number" }, min_tier: { type: "string" }, kind: { type: "string", description: "Optional exact result-kind filter, such as recipe." }, full: { type: "boolean", description: "Compatibility option that includes full body and payload in search results." } }, required: ["query"] } },
    { name: "kb_get_result", description: "Return the full body and payload for one exact kb_search result ID.", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
    { name: "kb_get_claim", description: "Return one exact approved claim by claim_id, including all concept routes and result IDs.", inputSchema: { type: "object", properties: { claim_id: { type: "string" } }, required: ["claim_id"] } },
    { name: "kb_list_models", description: "List stable Rock Model Map models with slugs, categories, versions, and property/method counts.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_get_model", description: "Return an exact stable Model Map digest by slug or model name, optionally filtered by fields or one property.", inputSchema: { type: "object", properties: { model: { type: "string" }, fields: { type: "string" }, property: { type: "string" } }, required: ["model"] } },
    { name: "kb_list_recipes", description: "List reusable community Rock recipes, optionally filtered by concept.", inputSchema: { type: "object", properties: { concept_id: { type: "string" } } } },
    { name: "kb_get_recipe", description: "Return one exact recipe with its pinned source, adaptation points, security, compatibility, validation, and reusable learnings.", inputSchema: { type: "object", properties: { recipe_id: { type: "string" } }, required: ["recipe_id"] } },
    { name: "kb_verify_recipe", description: "Verify a recipe's immutable source hashes and optional target Rock version without executing its code.", inputSchema: { type: "object", properties: { recipe_id: { type: "string" }, rock_version: { type: "string" } }, required: ["recipe_id"] } },
    { name: "kb_manifest", description: "Return the public Rock KB manifest.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_list_concepts", description: "List public Rock KB concepts.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_get_concept", description: "Return one concept package.", inputSchema: { type: "object", properties: { concept_id: { type: "string" } }, required: ["concept_id"] } },
    { name: "kb_get_claims", description: "Return claims for a concept, optionally filtered by tier.", inputSchema: { type: "object", properties: { concept_id: { type: "string" }, tier: { type: "string" }, min_tier: { type: "string" } }, required: ["concept_id"] } },
    { name: "kb_review_dashboard", description: "Return public operations counts for review queues, conflicts, community intake, evaluation, and telemetry.", inputSchema: { type: "object", properties: {} } },
    { name: "kb_feedback", description: "Record structured feedback for an exact result without retaining free text.", inputSchema: { type: "object", properties: { result_id: { type: "string" }, rating: { type: "number", enum: [-1, 1] }, reason: { type: "string", enum: ["helpful", "outdated", "missing", "incorrect", "wrong_route"] } }, required: ["result_id", "rating", "reason"] } },
    { name: "kb_submit", description: "Validate and submit a community contribution bundle for a registered org.", inputSchema: { type: "object", properties: { org_id: { type: "string" }, bundle: { type: "array" }, dry_run: { type: "boolean" } }, required: ["org_id", "bundle"] } }
  ];
}
