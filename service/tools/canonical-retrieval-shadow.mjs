import crypto from "node:crypto";
import fs from "node:fs";
import { performance } from "node:perf_hooks";
import { Miniflare } from "miniflare";

const args = parseArgs(process.argv.slice(2));
const limit = Number(args.limit || 5);
const evaluations = readJsonl(args.evaluation);
const endpointCases = readJsonl(args["endpoint-cases"]);
const variants = await runVariants(
  {
    baseline: readJsonl(args.baseline),
    candidate: readJsonl(args.candidate),
  },
  evaluations,
  endpointCases,
  limit,
  args["artifact-root"],
);

fs.writeFileSync(
  args.output,
  `${JSON.stringify({
    schema: "rock-kb-canonical-retrieval-shadow-raw-v1",
    variants,
  }, null, 2)}\n`,
  "utf8",
);

async function runVariants(rowsByVariant, evaluationRows, endpointRows, resultLimit, artifactRoot) {
  const variantNames = ["baseline", "candidate"];
  const states = {};
  try {
    for (const name of variantNames) {
      states[name] = await prepareVariant(name, rowsByVariant[name], artifactRoot);
    }

    process.stderr.write(
      `[canonical-shadow] paired: running ${evaluationRows.length} queries per variant\n`,
    );
    const results = Object.fromEntries(variantNames.map((name) => [name, []]));
    const queryMs = Object.fromEntries(variantNames.map((name) => [name, 0]));
    for (const [index, evaluation] of evaluationRows.entries()) {
      const order = index % 2 === 0 ? variantNames : [...variantNames].reverse();
      for (const name of order) {
        const result = await runSearchCase(
          states[name].mf,
          name,
          evaluation,
          resultLimit,
        );
        results[name].push(result);
        queryMs[name] += result.latency_ms;
      }
      if ((index + 1) % 40 === 0 || index + 1 === evaluationRows.length) {
        process.stderr.write(
          `[canonical-shadow] paired: ${index + 1}/${evaluationRows.length} queries\n`,
        );
      }
    }

    const output = {};
    for (const name of variantNames) {
      output[name] = {
        row_count: rowsByVariant[name].length,
        setup_ms: states[name].setupMs,
        query_ms: Number(queryMs[name].toFixed(3)),
        results: results[name],
        endpoint_results: await runEndpointCases(
          states[name].mf,
          name,
          endpointRows,
        ),
      };
    }
    return output;
  } finally {
    await Promise.all(
      Object.values(states).map((state) => state.mf.dispose()),
    );
  }
}

async function prepareVariant(name, rows, artifactRoot) {
  const started = performance.now();
  process.stderr.write(`[canonical-shadow] ${name}: loading ${rows.length} rows\n`);
  const mf = new Miniflare({
    modules: true,
    scriptPath: "dist/dry-run/index.js",
    compatibilityDate: "2026-07-18",
    compatibilityFlags: ["nodejs_compat"],
    d1Databases: { KB_DB: `canonical-shadow-${name}-${crypto.randomUUID()}` },
    r2Buckets: { KB_ARTIFACTS: `canonical-shadow-${name}-${crypto.randomUUID()}` },
    workerLoaders: { LOADER: {} },
    bindings: { PUBLIC_BASE_URL: "https://kb.shadow.test" },
  });
  try {
    const db = await mf.getD1Database("KB_DB");
    await initializeDatabase(db);
    await insertRows(db, rows);
    await insertArtifacts(mf, artifactRoot);
    const setupMs = Number((performance.now() - started).toFixed(3));
    process.stderr.write(
      `[canonical-shadow] ${name}: indexed in ${(setupMs / 1000).toFixed(1)}s\n`,
    );
    return { mf, setupMs };
  } catch (error) {
    await mf.dispose();
    throw error;
  }
}

async function runSearchCase(mf, name, evaluation, resultLimit) {
  const requestStarted = performance.now();
  const url = new URL("https://kb.shadow.test/search");
  url.searchParams.set("q", String(evaluation.question || ""));
  url.searchParams.set("limit", String(resultLimit));
  url.searchParams.set("min_tier", "routing_context_only");
  url.searchParams.set("detail", "full");
  const response = await mf.dispatchFetch(url, {
    headers: {
      "user-agent": "rock-kb-eval/1.0",
      "x-rock-kb-client": "eval",
    },
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(
      `${name} query ${evaluation.id} failed (${response.status}): ${JSON.stringify(payload).slice(0, 1000)}`,
    );
  }
  return {
    id: evaluation.id,
    latency_ms: Number((performance.now() - requestStarted).toFixed(3)),
    hits: payload.results || [],
  };
}

async function initializeDatabase(db) {
  const statements = [
    "CREATE TABLE kb_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    "INSERT INTO kb_meta (key, value) VALUES ('current_version', 'canonical-shadow')",
    `CREATE TABLE search_rows (
      id TEXT PRIMARY KEY,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      body TEXT NOT NULL,
      path TEXT NOT NULL,
      url TEXT,
      concept TEXT,
      authority_tier TEXT,
      claim_tier TEXT,
      claim_tier_rank INTEGER NOT NULL,
      source_id TEXT,
      concepts_json TEXT NOT NULL DEFAULT '[]',
      topics_json TEXT NOT NULL DEFAULT '[]',
      payload_json TEXT NOT NULL
    )`,
    "CREATE TABLE search_row_concepts (row_id TEXT NOT NULL, concept TEXT NOT NULL, PRIMARY KEY (row_id, concept))",
    "CREATE TABLE search_row_aliases (alias_id TEXT PRIMARY KEY, canonical_id TEXT NOT NULL)",
    "CREATE VIRTUAL TABLE search_rows_fts USING fts5(id UNINDEXED, title, body, concept, tokenize='porter')",
    `CREATE TABLE rock_issues (
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
    )`,
    "CREATE TABLE rock_issue_locations (location_id TEXT PRIMARY KEY, issue_id TEXT NOT NULL, is_current INTEGER NOT NULL)",
    `CREATE TABLE related_content_edges (
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
    )`,
  ];
  for (const statement of statements) {
    await db.prepare(statement).run();
  }
}

async function insertRows(db, rows) {
  const tierRanks = {
    routing_context_only: 0,
    source_backed: 1,
    answer_pack_approved: 2,
    live_verified: 3,
  };
  let statements = [];
  let statementBytes = 0;
  const flush = async () => {
    if (!statements.length) return;
    await db.exec(`${statements.join(";\n")};`);
    statements = [];
    statementBytes = 0;
  };
  const add = async (statement) => {
    const nextBytes = Buffer.byteLength(statement);
    if (statements.length && statementBytes + nextBytes >= 90_000) {
      await flush();
    }
    statements.push(statement);
    statementBytes += nextBytes;
    if (statements.length >= 300 || statementBytes >= 90_000) {
      await flush();
    }
  };
  for (const row of rows) {
    const concepts = uniqueStrings(row.concepts || [row.concept || ""]);
    const topics = uniqueStrings(row.topics || []);
    const body = d1SearchBody(row.body);
    const payload = row.payload && typeof row.payload === "object" ? row.payload : {};
    const claimTier = String(row.claim_tier || "");
    await add(
      `INSERT INTO search_rows (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, concepts_json, topics_json, payload_json) VALUES (${[
          sqlString(row.id),
          sqlString(row.kind),
          sqlString(row.title),
          sqlString(body),
          sqlString(row.path),
          sqlString(row.url),
          sqlString(concepts[0]),
          sqlString(row.authority_tier),
          sqlString(claimTier),
          String(tierRanks[claimTier] || 0),
          sqlString(row.source_id),
          sqlString(JSON.stringify(concepts)),
          sqlString(JSON.stringify(topics)),
          sqlString(JSON.stringify(payload)),
        ].join(", ")})`,
    );
    await add(
      `INSERT INTO search_rows_fts (id, title, body, concept) VALUES (${[
        sqlString(row.id),
        sqlString(row.title),
        sqlString(body),
        sqlString([...concepts, ...topics].join(" ")),
      ].join(", ")})`,
    );
    for (const concept of concepts) {
      await add(
        `INSERT INTO search_row_concepts (row_id, concept) VALUES (${sqlString(row.id)}, ${sqlString(concept)})`,
      );
    }
    for (const alias of uniqueStrings(row.legacy_ids || [])) {
      await add(
        `INSERT INTO search_row_aliases (alias_id, canonical_id) VALUES (${sqlString(alias)}, ${sqlString(row.id)})`,
      );
    }
    if (row.kind === "rock_issue") {
      const issueId = String(row.id || "");
      const repository = String(payload.repository || "");
      const number = Number(payload.number || 0);
      await add(
        `INSERT INTO rock_issues VALUES (${[
          sqlString(issueId),
          sqlString(payload.github_node_id || issueId),
          sqlString(repository),
          String(number),
          sqlString(payload.component),
          sqlString(payload.state),
          sqlString(payload.validation_state || "reported"),
          sqlString(payload.title || row.title),
          sqlString(payload.url || row.url),
          sqlString(payload.updated_at),
          sqlString(payload.evidence_state || "report_only"),
          sqlString(JSON.stringify(payload)),
        ].join(", ")})`,
      );
      const currentLocation = String(
        payload.location_id || `${repository}#${number}`,
      );
      await add(
        `INSERT INTO rock_issue_locations (location_id, issue_id, is_current) VALUES (${sqlString(currentLocation)}, ${sqlString(issueId)}, 1)`,
      );
      for (const location of uniqueStrings(payload.location_aliases || [])) {
        await add(
          `INSERT OR IGNORE INTO rock_issue_locations (location_id, issue_id, is_current) VALUES (${sqlString(location)}, ${sqlString(issueId)}, 0)`,
        );
      }
    }
  }
  await flush();
}

async function insertArtifacts(mf, artifactRoot) {
  const artifactPaths = [
    "agent/lava-contexts.jsonl",
    "agent/model-map-digests.jsonl",
    "agent/recipes.jsonl",
  ];
  const grouped = new Map();
  for (const artifactPath of artifactPaths) {
    const value = fs.readFileSync(`${artifactRoot}/${artifactPath}`, "utf8");
    const shard = crypto.createHash("sha256").update(artifactPath).digest("hex").slice(0, 2);
    if (!grouped.has(shard)) grouped.set(shard, {});
    grouped.get(shard)[artifactPath] = value;
  }
  const bucket = await mf.getR2Bucket("KB_ARTIFACTS");
  for (const [shard, artifacts] of grouped.entries()) {
    await bucket.put(
      `versions/canonical-shadow/artifact-shards/${shard}.json`,
      JSON.stringify({ artifacts }),
    );
  }
}

async function runEndpointCases(mf, variant, cases) {
  process.stderr.write(
    `[canonical-shadow] ${variant}: running ${cases.length} endpoint compatibility cases\n`,
  );
  const results = [];
  for (const endpointCase of cases) {
    const started = performance.now();
    let response;
    if (endpointCase.transport === "mcp") {
      response = await dispatchMcpCase(mf, endpointCase);
    } else {
      response = await mf.dispatchFetch(
        new URL(endpointCase.path, "https://kb.shadow.test"),
        {
          method: endpointCase.method || "GET",
          headers: {
            "user-agent": "rock-kb-eval/1.0",
            "x-rock-kb-client": "eval",
          },
        },
      );
    }
    const raw = await response.text();
    let payload;
    try {
      payload = raw ? JSON.parse(raw) : {};
    } catch {
      payload = { invalid_json: true, raw: raw.slice(0, 1000) };
    }
    results.push({
      id: endpointCase.id,
      http_status: response.status,
      latency_ms: Number((performance.now() - started).toFixed(3)),
      payload,
    });
  }
  return results;
}

async function dispatchMcpCase(mf, endpointCase) {
  const protocolVersion = "2026-07-28";
  const params = {
    name: endpointCase.tool,
    arguments: endpointCase.arguments || {},
    _meta: {
      "io.modelcontextprotocol/protocolVersion": protocolVersion,
      "io.modelcontextprotocol/clientInfo": {
        name: "rock-kb-canonical-shadow",
        version: "1.0.0",
      },
      "io.modelcontextprotocol/clientCapabilities": {},
    },
  };
  return mf.dispatchFetch("https://kb.shadow.test/mcp", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      accept: "application/json, text/event-stream",
      "mcp-protocol-version": protocolVersion,
      "mcp-method": "tools/call",
      "mcp-name": endpointCase.tool,
      "user-agent": "rock-kb-eval/1.0",
      "x-rock-kb-client": "eval",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params,
    }),
  });
}

function readJsonl(path) {
  return fs.readFileSync(path, "utf8")
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function uniqueStrings(values) {
  return [...new Set(values.map((value) => String(value || "").trim()).filter(Boolean))];
}

function d1SearchBody(value) {
  const body = String(value || "");
  if (body.length <= 75_000) return body;
  return `${body.slice(0, 75_000).trimEnd()}\n\n[Search body truncated; full document is available in R2 artifacts.]`;
}

function sqlString(value) {
  return `'${String(value || "")
    .replaceAll("\0", "\uFFFD")
    .replace(/[\r\n]+/g, " ")
    .replaceAll("'", "''")}'`;
}

function parseArgs(values) {
  const parsed = {};
  for (let index = 0; index < values.length; index += 2) {
    const key = String(values[index] || "").replace(/^--/, "");
    parsed[key] = values[index + 1];
  }
  for (const required of [
    "baseline",
    "candidate",
    "evaluation",
    "endpoint-cases",
    "artifact-root",
    "output",
  ]) {
    if (!parsed[required]) {
      throw new Error(`Missing required argument --${required}`);
    }
  }
  return parsed;
}
