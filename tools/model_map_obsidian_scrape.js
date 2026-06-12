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

function normalizeModel(category, modelOption, detail, sourceUrl, version, versionSourceUrl, probedAt) {
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
      obsolete_message: property.obsoleteMessage || null,
      description: descriptionParts.filter(Boolean).join(" "),
      related_entity_links: relatedEntityLinks(property.comments),
      related_defined_type_links: [],
      enum_values: enumValues(property.keyValues)
    };
  });
  return {
    schema: "rock-kb-demo-model-map-scrape-model-v1",
    requested_url: sourceUrl,
    selected_entity_type_id: "",
    selected_entity_type_guid: modelOption.value,
    selected_category_guid: category.guid,
    model_guid: modelOption.value,
    anchor_href: `${sourceUrl}?EntityType=${modelOption.value}`,
    model_title: detail.name || modelOption.text,
    model_link_name: modelOption.text,
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
    related_entity_property_count: properties.filter(row => row.related_entity_links.length).length,
    rock_version: version,
    rock_version_source_url: versionSourceUrl,
    rock_version_probed_at: probedAt,
    scraped_at: nowIso(),
    properties
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

async function main() {
  const url = argValue("--url", "https://rockrmslatest.com/admin/power-tools/model-map");
  const output = argValue("--output", "data/review/model-map-scrape/latest-model-map-full-scrape.json");
  const username = argValue("--username", "admin");
  const password = argValue("--password", "admin");
  const baseUrl = new URL(url).origin;

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  let detailEndpoint = "";
  let actionContext = null;
  page.on("request", request => {
    if (request.url().includes("GetModelDetails")) {
      detailEndpoint = request.url();
      try {
        actionContext = JSON.parse(request.postData() || "{}").__context || null;
      } catch {
        actionContext = null;
      }
    }
  });

  await login(page, url, username, password);
  await page.waitForFunction(
    () => (document.querySelector("#bid_796")?.innerText || "").includes("Property"),
    null,
    { timeout: 60000 }
  );
  const block = await parseConfiguration(page);
  const version = await probeVersion(page, baseUrl);
  if (!detailEndpoint || !actionContext) {
    throw new Error("Could not capture GetModelDetails block action context.");
  }

  const models = [];
  const failures = [];
  for (const category of block.configurationValues.categories || []) {
    for (const modelOption of category.models || []) {
      try {
        const detail = await page.evaluate(
          async ({ endpoint, context, entityTypeGuid }) => {
            const response = await fetch(endpoint, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ __context: context, entityTypeGuid })
            });
            if (!response.ok) {
              throw new Error(`HTTP ${response.status}`);
            }
            return await response.json();
          },
          { endpoint: detailEndpoint, context: actionContext, entityTypeGuid: modelOption.value }
        );
        models.push(normalizeModel(category, modelOption, detail, url, version.version, version.endpoint, version.probedAt));
        if (models.length % 25 === 0) {
          console.log(`[${nowIso()}] scraped=${models.length} latest=${modelOption.text}`);
        }
      } catch (error) {
        failures.push({
          category_name: category.name,
          model_name: modelOption.text,
          entity_type_guid: modelOption.value,
          error: String(error && error.message ? error.message : error)
        });
      }
    }
  }

  const payload = {
    schema: "rock-kb-demo-model-map-scrape-v1",
    track: "latest",
    source_url: url,
    started_at: models[0]?.scraped_at || nowIso(),
    finished_at: nowIso(),
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
    model_count: models.length,
    property_count: models.reduce((sum, model) => sum + model.property_count, 0),
    database_property_count: models.reduce((sum, model) => sum + model.database_property_count, 0),
    lava_property_count: models.reduce((sum, model) => sum + model.lava_property_count, 0),
    not_mapped_property_count: models.reduce((sum, model) => sum + model.not_mapped_property_count, 0),
    enum_value_property_count: models.reduce((sum, model) => sum + model.enum_value_property_count, 0),
    related_entity_property_count: models.reduce((sum, model) => sum + model.related_entity_property_count, 0),
    failure_count: failures.length,
    failures,
    models
  };

  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, `${JSON.stringify(payload, null, 2)}\n`);
  const jsonlPath = output.replace(/\.json$/i, ".models.jsonl");
  fs.writeFileSync(jsonlPath, `${models.map(model => JSON.stringify(model)).join("\n")}\n`);
  console.log(JSON.stringify({
    output,
    jsonlPath,
    model_count: payload.model_count,
    property_count: payload.property_count,
    rock_version: payload.rock_version,
    failure_count: payload.failure_count
  }, null, 2));
  await browser.close();
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
