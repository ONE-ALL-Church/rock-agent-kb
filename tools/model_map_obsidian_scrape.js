#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index === -1 || index + 1 >= process.argv.length) {
    return fallback;
  }
  return process.argv[index + 1];
}

function intArgValue(name, fallback) {
  const raw = argValue(name, String(fallback));
  const parsed = Number.parseInt(raw, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function nowIso() {
  return new Date().toISOString();
}

function stripHtml(value) {
  return String(value || "")
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function relatedEntityLinks(html) {
  const links = [];
  const pattern = /<a\s+[^>]*href=["']([^"']*EntityType=([^"'&]+)[^"']*)["'][^>]*>([\s\S]*?)<\/a>/gi;
  let match;
  while ((match = pattern.exec(String(html || "")))) {
    links.push({
      text: stripHtml(match[3]),
      entity_type_guid: match[2],
      href: match[1]
    });
  }
  return links;
}

function enumValues(keyValues) {
  if (!keyValues || typeof keyValues !== "object") {
    return [];
  }
  return Object.entries(keyValues).map(([value, label]) => ({
    value: String(value),
    label: String(label)
  }));
}

function normalizeMethod(method, index) {
  return {
    row_index: index,
    method_id: method.id ? `m${method.id}` : "",
    signature: method.signature || "",
    inherited: !!method.isInherited,
    is_obsolete: !!method.isObsolete,
    obsolete_message: method.obsoleteMessage || null,
    description: stripHtml(method.comments)
  };
}

function normalizeModel(category, modelOption, detail, collection) {
  const properties = (detail.properties || []).map((property, index) => {
    const isDatabase = !property.isVirtual && !property.notMapped;
    const isNotMapped = !!property.isVirtual || !!property.notMapped;
    const descriptionParts = [stripHtml(property.comments)];
    if (property.enumOrDefinedTypeDescription) {
      descriptionParts.push(stripHtml(property.enumOrDefinedTypeDescription));
    }
    return {
      row_index: index,
      property_id: property.id ? `p${property.id}` : "",
      name: property.name,
      inherited: !!property.isInherited,
      is_database: isDatabase,
      is_not_mapped: isNotMapped,
      is_lava: !!property.isLavaInclude,
      is_qualifier: !!property.isAttributeQualifier,
      is_required: !!property.required,
      is_obsolete: !!property.isObsolete,
      is_virtual: !!property.isVirtual,
      is_enum: !!property.isEnum,
      is_defined_value: !!property.isDefinedValue,
      obsolete_message: property.obsoleteMessage || null,
      description: descriptionParts.filter(Boolean).join(" "),
      related_entity_links: relatedEntityLinks(property.comments),
      related_defined_type_links: [],
      enum_values: enumValues(property.keyValues)
    };
  });
  const methods = (detail.methods || []).map(normalizeMethod);
  return {
    schema: "rock-kb-model-map-obsidian-model-v1",
    requested_url: collection.sourceUrl,
    collection_method: "obsidian_block_action",
    initialization_endpoint: collection.initializationEndpoint,
    detail_endpoint: collection.detailEndpoint,
    block_guid: collection.blockGuid,
    block_type_guid: collection.blockTypeGuid,
    block_file_url: collection.blockFileUrl,
    root_element_id: collection.rootElementId,
    selected_entity_type_id: "",
    selected_entity_type_guid: modelOption.value,
    selected_category_guid: category.guid,
    model_guid: modelOption.value,
    anchor_href: `${collection.sourceUrl}?EntityType=${modelOption.value}`,
    model_title: detail.name || modelOption.text,
    model_link_name: modelOption.text,
    table_name: detail.tableName || null,
    is_obsolete: !!detail.isObsolete,
    obsolete_message: detail.obsoleteMessage || null,
    description: stripHtml(detail.summary),
    example: stripHtml(detail.example),
    category_name: category.name,
    property_count: properties.length,
    database_property_count: properties.filter(row => row.is_database).length,
    lava_property_count: properties.filter(row => row.is_lava).length,
    not_mapped_property_count: properties.filter(row => row.is_not_mapped).length,
    required_property_count: properties.filter(row => row.is_required).length,
    qualifier_property_count: properties.filter(row => row.is_qualifier).length,
    obsolete_property_count: properties.filter(row => row.is_obsolete).length,
    enum_value_property_count: properties.filter(row => row.enum_values.length).length,
    enum_property_count: properties.filter(row => row.is_enum).length,
    defined_value_property_count: properties.filter(row => row.is_defined_value).length,
    related_entity_property_count: properties.filter(row => row.related_entity_links.length).length,
    method_count: methods.length,
    obsolete_method_count: methods.filter(row => row.is_obsolete).length,
    rock_version: collection.version,
    rock_version_source_url: collection.versionSourceUrl,
    rock_version_probed_at: collection.versionProbedAt,
    fetched_at: nowIso(),
    scraped_at: nowIso(),
    properties,
    methods
  };
}

async function login(page, url, username, password) {
  await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
  if (await page.locator('input[type="password"]').count()) {
    await page.locator('input[type="text"]:visible').first().fill(username);
    await page.locator('input[type="password"]:visible').first().fill(password);
    await Promise.all([
      page.waitForLoadState("networkidle", { timeout: 60000 }).catch(() => {}),
      page.getByRole("button", { name: /log in/i }).first().click()
    ]);
    await page.waitForTimeout(1500);
  }
  if (!page.url().includes("/admin/power-tools/model-map")) {
    await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
  }
}

async function parseConfiguration(page) {
  return await page.evaluate(() => {
    const scripts = Array.from(document.querySelectorAll("script")).map(script => script.textContent || "");
    const script = scripts.find(text => text.includes("module.initializeBlock(") && text.includes('"categories"'));
    if (!script) {
      throw new Error("Could not find model-map Obsidian configuration script.");
    }
    const marker = "module.initializeBlock(";
    const start = script.indexOf(marker) + marker.length;
    let depth = 0;
    let inString = false;
    let escaped = false;
    let end = -1;
    for (let index = start; index < script.length; index += 1) {
      const char = script[index];
      if (inString) {
        if (escaped) {
          escaped = false;
        } else if (char === "\\") {
          escaped = true;
        } else if (char === '"') {
          inString = false;
        }
        continue;
      }
      if (char === '"') {
        inString = true;
      } else if (char === "{") {
        depth += 1;
      } else if (char === "}") {
        depth -= 1;
        if (depth === 0) {
          end = index + 1;
          break;
        }
      }
    }
    if (end === -1) {
      throw new Error("Could not parse model-map block initialization JSON.");
    }
    return JSON.parse(script.slice(start, end));
  });
}

async function probeVersion(page, baseUrl) {
  const endpoint = `${baseUrl.replace(/\/$/, "")}/api/Utility/GetRockSemanticVersionNumber`;
  const probedAt = nowIso();
  const response = await page.request.get(endpoint, { timeout: 20000 });
  let version = null;
  if (response.ok()) {
    const text = (await response.text()).trim();
    try {
      const parsed = JSON.parse(text);
      version = String(parsed);
    } catch {
      const match = text.match(/\b\d+\.\d+\.\d+(?:\.\d+)?\b/);
      version = match ? match[0] : null;
    }
  }
  return {
    version,
    endpoint,
    probedAt,
    httpStatus: response.status()
  };
}

async function postJson(page, url, data) {
  const response = await page.request.post(url, {
    data,
    headers: { "Content-Type": "application/json" },
    timeout: 30000
  });
  const text = await response.text();
  if (!response.ok()) {
    throw new Error(`HTTP ${response.status()} from ${url}: ${text.slice(0, 200)}`);
  }
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`Invalid JSON from ${url}: ${text.slice(0, 200)}`);
  }
}

async function mapWithConcurrency(items, limit, mapper) {
  const results = new Array(items.length);
  let next = 0;
  const workers = Array.from({ length: Math.max(1, Math.min(limit, items.length)) }, async () => {
    while (next < items.length) {
      const index = next;
      next += 1;
      results[index] = await mapper(items[index], index);
    }
  });
  await Promise.all(workers);
  return results;
}

async function main() {
  const url = argValue("--url", "https://rockrmslatest.com/admin/power-tools/model-map");
  const output = argValue("--output", "data/review/model-map-scrape/latest-model-map-full-scrape.json");
  const track = argValue("--track", output.includes("demo-") ? "stable" : "latest");
  const username = argValue("--username", "admin");
  const password = argValue("--password", "admin");
  const concurrency = intArgValue("--concurrency", 12);
  const baseUrl = new URL(url).origin;

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const startedAt = nowIso();
  const timing = { started_at: startedAt };
  let observedDetailEndpoint = "";
  page.on("request", request => {
    if (request.url().includes("GetModelDetails")) {
      observedDetailEndpoint = request.url();
    }
  });

  const loginStarted = Date.now();
  await login(page, url, username, password);
  await page.waitForFunction(
    () => (document.querySelector("#bid_796")?.innerText || "").includes("Property"),
    null,
    { timeout: 60000 }
  );
  timing.login_and_page_ms = Date.now() - loginStarted;

  const pageBlock = await parseConfiguration(page);
  const blockActionBase = observedDetailEndpoint
    ? observedDetailEndpoint.replace(/\/GetModelDetails$/, "")
    : `${baseUrl}/api/v2/BlockActions/${pageBlock.blockTypeGuid}/${pageBlock.blockGuid}`;
  const initializationEndpoint = `${blockActionBase}/RefreshObsidianBlockInitialization`;
  const detailEndpoint = `${blockActionBase}/GetModelDetails`;

  const initStarted = Date.now();
  let block = await postJson(page, initializationEndpoint, {});
  timing.initialization_ms = Date.now() - initStarted;
  if (!block.configurationValues?.categories?.length) {
    block = pageBlock;
  }

  const version = await probeVersion(page, baseUrl);
  const categories = block.configurationValues?.categories || [];
  const modelOptions = categories.flatMap(category => (category.models || []).map(model => ({ category, model })));
  const collection = {
    sourceUrl: url,
    initializationEndpoint,
    detailEndpoint,
    blockGuid: block.blockGuid || pageBlock.blockGuid,
    blockTypeGuid: block.blockTypeGuid || pageBlock.blockTypeGuid,
    blockFileUrl: block.blockFileUrl || pageBlock.blockFileUrl,
    rootElementId: block.rootElementId || pageBlock.rootElementId,
    version: version.version,
    versionSourceUrl: version.endpoint,
    versionProbedAt: version.probedAt
  };

  const detailStarted = Date.now();
  const failures = [];
  const models = [];
  await mapWithConcurrency(modelOptions, concurrency, async ({ category, model: modelOption }, index) => {
    try {
      const detail = await postJson(page, detailEndpoint, { entityTypeGuid: modelOption.value });
      const normalized = normalizeModel(category, modelOption, detail, collection);
      models[index] = normalized;
      const count = models.filter(Boolean).length;
      if (count % 25 === 0) {
        console.log(`[${nowIso()}] fetched=${count} latest=${modelOption.text}`);
      }
    } catch (error) {
      failures.push({
        category_name: category.name,
        model_name: modelOption.text,
        entity_type_guid: modelOption.value,
        error: String(error && error.message ? error.message : error)
      });
    }
  });
  timing.detail_fetch_ms = Date.now() - detailStarted;
  timing.finished_at = nowIso();

  const successfulModels = models.filter(Boolean);
  const payload = {
    schema: "rock-kb-model-map-obsidian-block-action-v1",
    legacy_schema: "rock-kb-demo-model-map-scrape-v1",
    track,
    collection_method: "obsidian_block_action",
    source_url: url,
    started_at: startedAt,
    finished_at: timing.finished_at,
    rock_version: version.version,
    rock_version_source_url: version.endpoint,
    rock_version_probed_at: version.probedAt,
    demo_rock_version_context: {
      schema: "rock-kb-demo-rock-version-probe-v1",
      endpoint_url: version.endpoint,
      probed_at: version.probedAt,
      version: version.version,
      status: version.version ? "detected" : "not_detected",
      http_status: version.httpStatus
    },
    obsidian_block_action: {
      schema: "rock-kb-model-map-obsidian-block-action-context-v1",
      block_file_url: collection.blockFileUrl,
      block_guid: collection.blockGuid,
      block_type_guid: collection.blockTypeGuid,
      root_element_id: collection.rootElementId,
      initialization_endpoint: collection.initializationEndpoint,
      detail_endpoint: collection.detailEndpoint,
      initialization_status: "ok",
      category_count: categories.length,
      listed_model_count: modelOptions.length,
      concurrency,
      timing
    },
    category_count: categories.length,
    model_count: successfulModels.length,
    listed_model_count: modelOptions.length,
    property_count: successfulModels.reduce((sum, model) => sum + model.property_count, 0),
    database_property_count: successfulModels.reduce((sum, model) => sum + model.database_property_count, 0),
    lava_property_count: successfulModels.reduce((sum, model) => sum + model.lava_property_count, 0),
    not_mapped_property_count: successfulModels.reduce((sum, model) => sum + model.not_mapped_property_count, 0),
    enum_value_property_count: successfulModels.reduce((sum, model) => sum + model.enum_value_property_count, 0),
    enum_property_count: successfulModels.reduce((sum, model) => sum + model.enum_property_count, 0),
    defined_value_property_count: successfulModels.reduce((sum, model) => sum + model.defined_value_property_count, 0),
    related_entity_property_count: successfulModels.reduce((sum, model) => sum + model.related_entity_property_count, 0),
    method_count: successfulModels.reduce((sum, model) => sum + model.method_count, 0),
    obsolete_method_count: successfulModels.reduce((sum, model) => sum + model.obsolete_method_count, 0),
    table_name_model_count: successfulModels.filter(model => model.table_name).length,
    obsolete_model_count: successfulModels.filter(model => model.is_obsolete).length,
    failure_count: failures.length,
    failures,
    models: successfulModels
  };

  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, `${JSON.stringify(payload, null, 2)}\n`);
  const jsonlPath = output.replace(/\.json$/i, ".models.jsonl");
  fs.writeFileSync(jsonlPath, `${successfulModels.map(model => JSON.stringify(model)).join("\n")}\n`);
  console.log(JSON.stringify({
    output,
    jsonlPath,
    collection_method: payload.collection_method,
    initialization_endpoint: payload.obsidian_block_action.initialization_endpoint,
    detail_endpoint: payload.obsidian_block_action.detail_endpoint,
    model_count: payload.model_count,
    listed_model_count: payload.listed_model_count,
    property_count: payload.property_count,
    method_count: payload.method_count,
    table_name_model_count: payload.table_name_model_count,
    rock_version: payload.rock_version,
    failure_count: payload.failure_count,
    timing
  }, null, 2));
  await browser.close();
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
