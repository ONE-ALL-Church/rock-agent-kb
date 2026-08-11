from __future__ import annotations

import json
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import quote, unquote, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from .extract import USER_AGENT, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, NORMALIZED_DIR
from .rock_idea_relationships import build_rock_idea_relationship_artifacts
from .source_hashing import NORMALIZED_SOURCE_HASH_ALGORITHM, source_content_hash
from .sources import Source, get_source


ROCK_IDEA_PATH = AGENT_DIR / "rock-ideas.jsonl"
ROCK_IDEA_SUMMARY_PATH = AGENT_DIR / "rock-idea-summary.json"
ROCK_IDEA_GUIDE_PATH = KNOWLEDGE_DIR / "ideas" / "index.md"
ROCK_IDEA_NORMALIZED_PATH = NORMALIZED_DIR / "rock_ideas.jsonl"
ROCK_IDEA_HOME = "https://community.rockrms.com/ideas"
ROCK_IDEA_PANEL_ID = "ctl00_main_ctl09_ctl01_ctl00_upnlContent"
ROCK_IDEA_PANEL_NAME = "ctl00$main$ctl09$ctl01$ctl00$upnlContent"
ROCK_IDEA_PAGE_FIELD = "ctl00$main$ctl09$ctl01$ctl00$hfPageNo"
ROCK_IDEA_SCRIPT_MANAGER = "ctl00$sManager"
ROCK_IDEA_WEBFORMS_USER_AGENT = (
    "Mozilla/5.0 (compatible; RockGeneralKnowledgeBase/0.1; "
    "+https://github.com/ONE-ALL-Church/Rock-General-Knowledge-Base)"
)
ROCK_IDEA_DETAIL_SHAPE_VERSION = 2
IDEA_STATUSES = {
    "not planned": "not_planned",
    "under review": "under_review",
    "started": "started",
    "planned": "planned",
    "pending": "pending",
    "open": "open",
    "complete": "complete",
}
IDEA_CATEGORIES = {
    "API",
    "Apple TV",
    "CMS",
    "Check-in",
    "Communication",
    "Connection",
    "Core",
    "CRM",
    "Engagement",
    "Event",
    "Farm",
    "Finance",
    "Group",
    "Lava",
    "LMS",
    "Mobile",
    "Other",
    "Prayer",
    "Reminders",
    "Reporting",
    "Security",
    "Workflow",
}
CATEGORY_CONCEPTS = {
    "API": "api-integrations",
    "Apple TV": "apple-tv",
    "CMS": "cms-websites",
    "Check-in": "check-in",
    "Communication": "communications",
    "Connection": "connections",
    "Core": "platform-configuration",
    "CRM": "people-families",
    "Engagement": "engagement-tracking",
    "Event": "event-registration",
    "Farm": "system-admin-ops",
    "Finance": "giving-finance",
    "Group": "groups",
    "Lava": "lava",
    "LMS": "learning-lms-engagement",
    "Mobile": "mobile",
    "Other": "platform-configuration",
    "Prayer": "prayer-care",
    "Reminders": "engagement-tracking",
    "Reporting": "data-views-reports",
    "Security": "security-permissions",
    "Workflow": "workflows",
}
SENSITIVE_IDEA_FIELDS = {
    "author",
    "submitter",
    "organization",
    "description",
    "body",
    "response",
    "response_text",
    "comments",
    "comment_count",
}


def sync_rock_ideas(
    *,
    workers: int = 5,
    enrich_details: bool = True,
    detail_refresh_limit: int = 120,
) -> dict[str, Any]:
    source = get_source("rock_ideas")
    checked_at = utc_now()
    catalog_rows, page_count, catalog_complete = fetch_idea_catalog()
    if not catalog_complete:
        raise RuntimeError("Rock Ideas native catalog ended before its final page; existing artifacts were not replaced")
    discovered: dict[int, dict[str, Any]] = {}
    merge_idea_rows(discovered, catalog_rows)
    existing = {int(row["number"]): row for row in read_jsonl(ROCK_IDEA_PATH) if row.get("number")}

    detail_refreshed = 0
    detail_selected = 0
    if enrich_details and detail_refresh_limit > 0:
        detail_urls = idea_detail_refresh_urls(discovered, existing, limit=detail_refresh_limit)
        detail_selected = len(detail_urls)
        with ThreadPoolExecutor(max_workers=max(1, min(8, workers * 2))) as executor:
            details = executor.map(fetch_idea_detail, detail_urls)
        detail_rows = []
        for row in details:
            if not row:
                continue
            row["_detail_observed"] = True
            row["detail_last_checked_at"] = checked_at
            detail_rows.append(row)
        detail_refreshed = len(detail_rows)
        merge_idea_rows(discovered, detail_rows)

    idea_rows = []
    for number, partial in sorted(discovered.items(), reverse=True):
        row = finalize_idea_row(partial, checked_at=checked_at, previous=existing.get(number))
        idea_rows.append(row)
    validate_rock_idea_rows(idea_rows)
    normalized_rows = [normalized_idea_record(source, row) for row in idea_rows]
    write_jsonl(ROCK_IDEA_PATH, idea_rows)
    write_jsonl(ROCK_IDEA_NORMALIZED_PATH, normalized_rows)
    previous_summary = read_json_object(ROCK_IDEA_SUMMARY_PATH)
    summary = build_rock_idea_summary(
        idea_rows,
        checked_at=checked_at,
        page_count=page_count,
        catalog_complete=catalog_complete,
        detail_selected=detail_selected,
        detail_refreshed=detail_refreshed,
        normalized_rows=normalized_rows,
        previous=previous_summary,
    )
    summary["relationships"] = build_rock_idea_relationship_artifacts(idea_rows, checked_at=checked_at)
    ROCK_IDEA_SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    render_rock_idea_guide(summary)
    return summary


def fetch_idea_catalog(*, max_pages: Optional[int] = None) -> tuple[list[dict[str, Any]], int, bool]:
    """Enumerate the public Ideas list through its stateful WebForms pager."""
    rows: list[dict[str, Any]] = []
    page_count = 0
    seen_page_signatures: set[tuple[int, ...]] = set()
    with httpx.Client(
        follow_redirects=True,
        timeout=35,
        headers={"User-Agent": ROCK_IDEA_WEBFORMS_USER_AGENT},
    ) as client:
        response = client.get(ROCK_IDEA_HOME)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.select_one("form")
        if form is None:
            raise RuntimeError("Rock Ideas page did not contain its expected WebForms form")
        form_data = webforms_form_fields(form)

        while True:
            page_rows = parse_idea_list_html(str(soup))
            signature = tuple(int(row["number"]) for row in page_rows)
            if not signature or signature in seen_page_signatures:
                raise RuntimeError("Rock Ideas pager returned an empty or repeated page")
            seen_page_signatures.add(signature)
            rows.extend(page_rows)
            page_count += 1

            next_target = idea_next_page_target(soup)
            if not next_target:
                return rows, page_count, True
            if max_pages is not None and page_count >= max_pages:
                return rows, page_count, False

            update_webforms_controls(form_data, soup)
            form_data.update(
                {
                    ROCK_IDEA_SCRIPT_MANAGER: f"{ROCK_IDEA_PANEL_NAME}|{next_target}",
                    "__EVENTTARGET": next_target,
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__ASYNCPOST": "true",
                }
            )
            delta_records = parse_ms_ajax_delta(post_idea_page(client, form_data))
            for record_type, record_id, value in delta_records:
                if record_type == "hiddenField":
                    form_data[record_id] = value
            panel_html = next(
                (
                    value
                    for record_type, record_id, value in delta_records
                    if record_type == "updatePanel" and record_id == ROCK_IDEA_PANEL_ID
                ),
                None,
            )
            if panel_html is None:
                raise RuntimeError("Rock Ideas pager response did not contain the Ideas update panel")
            soup = BeautifulSoup(panel_html, "html.parser")
            time.sleep(0.02)


def post_idea_page(client: httpx.Client, form_data: dict[str, str]) -> str:
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://community.rockrms.com",
        "Referer": ROCK_IDEA_HOME,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-MicrosoftAjax": "Delta=true",
        "X-Requested-With": "XMLHttpRequest",
    }
    last_response: Optional[httpx.Response] = None
    for attempt in range(3):
        try:
            response = client.post(ROCK_IDEA_HOME, data=form_data, headers=headers)
            last_response = response
            if response.status_code == 200 and re.match(r"^\d+\|#\|\|\d+\|", response.text):
                return response.text
        except httpx.HTTPError:
            pass
        if attempt < 2:
            time.sleep(0.5 * (attempt + 1))
    status = last_response.status_code if last_response is not None else "network_error"
    raise RuntimeError(f"Rock Ideas pager request failed after retries with status {status}")


def webforms_form_fields(form: Any) -> dict[str, str]:
    values: dict[str, str] = {}
    update_webforms_controls(values, form)
    return values


def update_webforms_controls(values: dict[str, str], container: Any) -> None:
    for node in container.select("input[name], select[name], textarea[name]"):
        name = str(node.get("name") or "")
        input_type = str(node.get("type") or "").lower()
        if not name or input_type in {"submit", "button", "image", "file"}:
            continue
        if input_type in {"checkbox", "radio"} and not node.has_attr("checked"):
            continue
        if node.name == "select":
            selected = node.select_one("option[selected]") or node.select_one("option")
            value = str(selected.get("value") or "") if selected else ""
        elif node.name == "textarea":
            value = node.get_text()
        else:
            value = str(node.get("value") or "")
        values[name] = value


def idea_next_page_target(container: Any) -> Optional[str]:
    anchor = next(
        (node for node in container.select('a[href*="__doPostBack"]') if clean_text(node.get_text()).lower() == "next"),
        None,
    )
    if anchor is None:
        return None
    match = re.search(r"__doPostBack\('([^']+)'", str(anchor.get("href") or ""))
    return match.group(1) if match else None


def parse_ms_ajax_delta(payload: str) -> list[tuple[str, str, str]]:
    prefix = re.match(r"^\d+\|#\|\|\d+\|", payload)
    if prefix is None:
        raise ValueError("Invalid Microsoft AJAX delta prefix")
    position = prefix.end()
    records: list[tuple[str, str, str]] = []
    while position < len(payload):
        delimiter = payload.find("|", position)
        if delimiter < 0:
            break
        length_text = payload[position:delimiter]
        if not length_text:
            position = delimiter + 1
            continue
        try:
            value_length = int(length_text)
        except ValueError as exc:
            raise ValueError("Invalid Microsoft AJAX delta record length") from exc
        type_end = payload.find("|", delimiter + 1)
        id_end = payload.find("|", type_end + 1)
        if type_end < 0 or id_end < 0:
            raise ValueError("Truncated Microsoft AJAX delta record header")
        record_type = payload[delimiter + 1 : type_end]
        record_id = payload[type_end + 1 : id_end]
        value_start = id_end + 1
        value_end = advance_utf16_units(payload, value_start, value_length)
        if value_end >= len(payload) or payload[value_end] != "|":
            raise ValueError("Invalid Microsoft AJAX delta record value length")
        records.append((record_type, record_id, payload[value_start:value_end]))
        position = value_end + 1
    return records


def advance_utf16_units(value: str, start: int, unit_count: int) -> int:
    position = start
    consumed = 0
    while position < len(value) and consumed < unit_count:
        consumed += 2 if ord(value[position]) > 0xFFFF else 1
        position += 1
    if consumed != unit_count:
        raise ValueError("Microsoft AJAX delta value ended inside a UTF-16 character")
    return position


def parse_idea_list_html(html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for anchor in soup.select('.feature-title h2 a[href*="/ideas/"]'):
        url = urljoin(ROCK_IDEA_HOME, str(anchor.get("href") or ""))
        number = idea_number_from_url(url)
        container = idea_list_container(anchor)
        if number is None or container is None:
            continue
        labels = [clean_text(node.get_text(" ", strip=True)) for node in container.select(".feature-title .label")]
        labels = [value for value in labels if value]
        category = next((value for value in labels if value in IDEA_CATEGORIES), "Other")
        status_label = next((value for value in labels if value.lower() in IDEA_STATUSES), "")
        planned_version = next(
            (normalize_planned_version_label(value) for value in labels if re.fullmatch(r"[0-9]+(?:\.[0-9]+){0,2}", value)),
            None,
        )
        vote_node = container.select_one(".well h3")
        time_node = container.select_one("time[datetime]")
        rows.append(
            {
                "number": number,
                "title": clean_text(anchor.get_text(" ", strip=True)),
                "url": canonical_idea_url(url),
                "category": category,
                "status": IDEA_STATUSES.get(status_label.lower(), "open"),
                "status_label": status_label or "Open",
                "status_is_inferred": not bool(status_label),
                "vote_count": parse_int(vote_node.get_text(" ", strip=True) if vote_node else "0"),
                "planned_version": planned_version,
                "submitted_at": str(time_node.get("datetime") or "") if time_node else None,
            }
        )
    return rows


def idea_list_container(anchor: Any) -> Optional[Any]:
    for parent in anchor.parents:
        if getattr(parent, "name", None) != "div":
            continue
        classes = set(parent.get("class") or [])
        if "row" in classes and parent.select_one(".well h3") and parent.select_one(".feature-title h2 a"):
            return parent
    return None


def fetch_idea_detail(url: str) -> Optional[dict[str, Any]]:
    try:
        with httpx.Client(follow_redirects=True, timeout=25, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(url)
            response.raise_for_status()
    except httpx.HTTPError:
        return None
    return parse_idea_detail_html(response.text, str(response.url))


def idea_detail_refresh_urls(
    discovered: dict[int, dict[str, Any]],
    existing: dict[int, dict[str, Any]],
    *,
    limit: int,
) -> list[str]:
    """Prioritize new, lifecycle-changed, old-shape, and least-recently enriched ideas."""
    comparison_fields = (
        "title",
        "category",
        "status",
        "status_label",
        "vote_count",
        "submitted_at",
    )
    candidates: list[tuple[int, str, int, str]] = []
    for number, current in discovered.items():
        previous = existing.get(number)
        is_lifecycle_row = current.get("status") != "open" or bool(current.get("planned_version"))
        changed = previous is not None and (
            any(current.get(key) != previous.get(key) for key in comparison_fields)
            or (
                bool(current.get("planned_version"))
                and current.get("planned_version") != previous.get("planned_version")
            )
        )
        if changed:
            priority = 0
        elif previous is None and is_lifecycle_row:
            priority = 1
        elif previous is not None and not previous.get("detail_last_checked_at") and is_lifecycle_row:
            priority = 2
        elif previous is None:
            priority = 3
        elif not previous.get("detail_last_checked_at"):
            priority = 4
        elif int(previous.get("detail_shape_version") or 0) < ROCK_IDEA_DETAIL_SHAPE_VERSION:
            priority = 5
        else:
            priority = 6
        candidates.append(
            (
                priority,
                str((previous or {}).get("detail_last_checked_at") or ""),
                -number,
                str(current["url"]),
            )
        )
    candidates.sort()
    return [url for _, _, _, url in candidates[: max(0, limit)]]


def parse_idea_detail_html(html: str, url: str) -> Optional[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".feature-detail")
    if not container or "that idea does not exist" in clean_text(container.get_text(" ", strip=True)).lower():
        return None
    heading = container.select_one("h2.h2")
    number = idea_number_from_url(url)
    if not heading or number is None:
        return None
    heading_parent = heading.parent
    labels = [clean_text(node.get_text(" ", strip=True)) for node in heading_parent.select(".label")]
    labels = [value for value in labels if value]
    category = next((value for value in labels if value in IDEA_CATEGORIES), "Other")
    status_label = next((value for value in labels if value.lower() in IDEA_STATUSES), "")
    planned_version = next(
        (normalize_planned_version_label(value) for value in labels if re.fullmatch(r"[0-9]+(?:\.[0-9]+){0,2}", value)),
        None,
    )
    table_values = idea_response_table(container)
    response = container.select_one(".response")
    response_time = response.select_one("time[datetime]") if response else None
    submitted_time = next(
        (node for node in container.select("time[datetime]") if not node.find_parent(class_="response")),
        None,
    )
    vote_node = container.select_one(".well h3")
    strength = parse_strength(table_values.get("Ministry Strength"))
    return {
        "number": number,
        "title": clean_text(heading.get_text(" ", strip=True)),
        "url": canonical_idea_url(url),
        "category": category,
        "status": IDEA_STATUSES.get(status_label.lower(), "open"),
        "status_label": status_label or "Open",
        "status_is_inferred": not bool(status_label),
        "vote_count": parse_int(vote_node.get_text(" ", strip=True) if vote_node else "0"),
        "planned_version": table_values.get("Planned Version") or planned_version,
        "ministry_strength": strength,
        "feature_size": table_values.get("Feature Size") or None,
        "submitted_at": str(submitted_time.get("datetime") or "") if submitted_time else None,
        "response_updated_at": str(response_time.get("datetime") or "") if response_time else None,
        "staff_response_present": bool(response),
        "detail_shape_version": ROCK_IDEA_DETAIL_SHAPE_VERSION,
        "evidence_links": idea_evidence_links(container),
    }


def idea_evidence_links(container: Any) -> list[dict[str, str]]:
    links: dict[tuple[str, str, str], dict[str, str]] = {}
    for selector, origin in ((".description", "proposal"), (".response", "staff_response")):
        section = container.select_one(selector)
        if section is None:
            continue
        for anchor in section.select("a[href]"):
            classified = classify_idea_evidence_link(str(anchor.get("href") or ""), origin=origin)
            if classified:
                key = (
                    str(classified.get("link_kind") or ""),
                    str(classified.get("target_id") or ""),
                    str(classified.get("url") or ""),
                )
                links[key] = classified
    return sorted(
        links.values(),
        key=lambda row: (str(row.get("link_kind") or ""), str(row.get("target_id") or row.get("url") or "")),
    )


def classify_idea_evidence_link(href: str, *, origin: str) -> Optional[dict[str, str]]:
    if not href.strip():
        return None
    absolute = urljoin(ROCK_IDEA_HOME, href.strip())
    parsed = urlparse(absolute)
    if parsed.scheme != "https" or parsed.username or parsed.password:
        return None
    host = parsed.hostname.lower() if parsed.hostname else ""
    path = re.sub(r"/{2,}", "/", parsed.path)
    base = f"https://{host}{path}"
    if parsed.fragment:
        base += f"#{parsed.fragment}"

    if host == "github.com":
        issue_match = re.fullmatch(
            r"/SparkDevNetwork/(?P<repo>Rock(?:\.Mobile-Issues)?)/issues/(?P<number>[1-9][0-9]*)(?:/)?",
            path,
            re.IGNORECASE,
        )
        if issue_match:
            repo = issue_match.group("repo")
            repository = "SparkDevNetwork/Rock.Mobile-Issues" if repo.lower().endswith("mobile-issues") else "SparkDevNetwork/Rock"
            number = int(issue_match.group("number"))
            return {
                "link_kind": "github_issue",
                "target_kind": "rock_issue",
                "target_id": f"rock_issue:{repository}#{number}",
                "url": f"https://github.com/{repository}/issues/{number}",
                "origin": origin,
                "authority_tier": "community-unreviewed",
            }
        if re.match(r"^/SparkDevNetwork/Rock/(?:blob|tree|commit)/", path, re.IGNORECASE):
            return {
                "link_kind": "official_source",
                "target_kind": "official_source",
                "url": base,
                "origin": origin,
                "authority_tier": "official",
            }
        return None

    if host == "community.rockrms.com":
        idea_number = idea_number_from_url(base)
        if idea_number:
            return {
                "link_kind": "rock_idea",
                "target_kind": "rock_idea",
                "target_id": f"rock_idea:{idea_number}",
                "url": canonical_idea_url(base),
                "origin": origin,
                "authority_tier": "community-unreviewed",
            }
        if path.startswith("/documentation/") or path.startswith("/developer/"):
            return {
                "link_kind": "official_documentation",
                "target_kind": "official_documentation",
                "url": base,
                "origin": origin,
                "authority_tier": "official",
            }
        return None

    if host in {"rockrms.com", "www.rockrms.com"} and path.rstrip("/").lower() in {
        "/releasenotes",
        "/mobilereleasenotes",
    }:
        return {
            "link_kind": "release_notes",
            "target_kind": "release_notes",
            "url": base,
            "origin": origin,
            "authority_tier": "official",
        }
    return None


def idea_response_table(container: Any) -> dict[str, str]:
    values = {}
    for heading in container.select(".response table th"):
        cell = heading.find_next("td")
        key = clean_text(heading.get_text(" ", strip=True))
        value = clean_text(cell.get_text(" ", strip=True)) if cell else ""
        if key and value:
            values[key] = value
    return values


def merge_idea_rows(target: dict[int, dict[str, Any]], rows: Iterable[dict[str, Any]]) -> None:
    for incoming in rows:
        number = int(incoming.get("number") or 0)
        if not number:
            continue
        current = target.get(number, {})
        merged = {**current, **{key: value for key, value in incoming.items() if value not in (None, "", [], {})}}
        if current.get("status_is_inferred") is False and incoming.get("status_is_inferred") is True:
            for key in ["status", "status_label", "status_is_inferred"]:
                merged[key] = current.get(key)
        target[number] = merged


def finalize_idea_row(partial: dict[str, Any], *, checked_at: str, previous: Optional[dict[str, Any]]) -> dict[str, Any]:
    number = int(partial["number"])
    title = clean_text(str(partial.get("title") or f"Rock Idea {number}"))
    category = str(partial.get("category") or "Other")
    status = str(partial.get("status") or "open")
    concept_routes = concept_routes_for_idea(category, title)
    row = {
        "schema": "rock-kb-rock-idea-v1",
        "idea_id": f"rock_idea:{number}",
        "number": number,
        "title": title,
        "url": canonical_idea_url(str(partial.get("url") or f"{ROCK_IDEA_HOME}/{number}")),
        "category": category,
        "status": status,
        "status_label": str(partial.get("status_label") or status.replace("_", " ").title()),
        "status_is_inferred": bool(partial.get("status_is_inferred", status == "open")),
        "lifecycle_phase": lifecycle_phase(status),
        "vote_count": max(0, int(partial.get("vote_count") or 0)),
        "planned_version": idea_planned_version(partial, previous),
        "ministry_strength": idea_detail_value(partial, previous, "ministry_strength"),
        "feature_size": idea_detail_value(partial, previous, "feature_size"),
        "submitted_at": partial.get("submitted_at") or None,
        "response_updated_at": idea_detail_value(partial, previous, "response_updated_at"),
        "staff_response_present": bool(idea_detail_value(partial, previous, "staff_response_present", False)),
        "detail_last_checked_at": idea_detail_value(partial, previous, "detail_last_checked_at"),
        "detail_shape_version": int(idea_detail_value(partial, previous, "detail_shape_version", 0) or 0),
        "evidence_links": idea_detail_value(partial, previous, "evidence_links", []),
        "concept_ids": [route["concept_id"] for route in concept_routes],
        "concept_routes": concept_routes,
        "source_id": "rock_ideas",
        "source_kind": "rock_ideas",
        "authority_tier": "community-unreviewed",
        "claim_tier": "routing_context_only",
        "needs_live_verification": True,
        "availability_caveat": "An idea status records community roadmap state, not proof that a capability is present in a specific Rock release or instance. Corroborate with official documentation, release notes, source code, and local read-only verification.",
        "last_checked_at": checked_at,
    }
    row["content_hash"] = idea_content_hash(row)
    row["content_changed_at"] = (
        previous.get("content_changed_at")
        if previous and previous.get("content_hash") == row["content_hash"] and previous.get("content_changed_at")
        else checked_at
    )
    return row


def idea_detail_value(
    current: dict[str, Any],
    previous: Optional[dict[str, Any]],
    key: str,
    default: Any = None,
) -> Any:
    if key in current:
        return current.get(key)
    if current.get("_detail_observed"):
        return default
    if previous and key in previous:
        return previous.get(key)
    return default


def idea_planned_version(current: dict[str, Any], previous: Optional[dict[str, Any]]) -> Optional[str]:
    value = current.get("planned_version")
    if value:
        return str(value)
    if current.get("_detail_observed"):
        return None
    previous_value = (previous or {}).get("planned_version")
    return str(previous_value) if previous_value else None


def normalized_idea_record(source: Source, idea: dict[str, Any]) -> dict[str, Any]:
    version = str(idea.get("planned_version") or "")
    summary = f"{idea['title']}. Community idea status: {idea['status_label']}. Category: {idea['category']}."
    if version:
        summary += f" Planned version label: {version}."
    return {
        "id": f"rock_ideas:{idea['number']}",
        "source_id": source.id,
        "source_url": idea["url"],
        "source_title": idea["title"],
        "source_kind": source.kind,
        "retrieved_at": idea["last_checked_at"],
        "updated_at": idea.get("response_updated_at") or idea.get("submitted_at"),
        "license_status": source.license_status,
        "allowed_extraction_mode": source.allowed_extraction_mode,
        "content_hash": idea["content_hash"],
        "extraction_tool": "aspnet_webforms_native_pager",
        "extraction_mode": "structured_metadata",
        "summary_model": None,
        "topics": sorted(set([*source.topics, *idea.get("concept_ids", [])])),
        "rock_version_min": None,
        "rock_version_max": None,
        "rock_versions": [version] if version else [],
        "audience": ["rock-admin", "agent"],
        "summary": summary,
        "excerpt": "",
        "canonical_path": "knowledge/ideas/index.md",
        "citations": [{"source_id": source.id, "url": idea["url"]}],
        "needs_review": True,
        "routing_metadata_only": True,
        "idea_id": idea["idea_id"],
        "idea_status": idea["status"],
        "idea_category": idea["category"],
        "planned_version": idea.get("planned_version"),
        "vote_count": idea["vote_count"],
        "concept_ids": idea["concept_ids"],
        "concept_routes": idea.get("concept_routes") or [],
    }


def validate_rock_idea_rows(rows: Iterable[dict[str, Any]]) -> None:
    seen: set[str] = set()
    for index, row in enumerate(rows, 1):
        idea_id = str(row.get("idea_id") or "")
        if row.get("schema") != "rock-kb-rock-idea-v1" or not re.fullmatch(r"rock_idea:[1-9][0-9]*", idea_id):
            raise ValueError(f"Rock idea row {index} has an invalid schema or idea_id")
        if idea_id in seen:
            raise ValueError(f"Duplicate Rock idea ID: {idea_id}")
        seen.add(idea_id)
        if row.get("status") not in set(IDEA_STATUSES.values()) or row.get("category") not in IDEA_CATEGORIES:
            raise ValueError(f"Rock idea {idea_id} has an invalid status or category")
        if row.get("authority_tier") != "community-unreviewed" or row.get("claim_tier") != "routing_context_only":
            raise ValueError(f"Rock idea {idea_id} must remain routing-only community metadata")
        if row.get("needs_live_verification") is not True:
            raise ValueError(f"Rock idea {idea_id} must require live and official-source verification")
        if idea_number_from_url(str(row.get("url") or "")) != int(row.get("number") or 0):
            raise ValueError(f"Rock idea {idea_id} has a mismatched canonical URL")
        if SENSITIVE_IDEA_FIELDS & set(row):
            raise ValueError(f"Rock idea {idea_id} contains disallowed proposal, response, comment, or identity fields")
        routes = row.get("concept_routes") or []
        routed_concepts = [str(route.get("concept_id") or "") for route in routes if isinstance(route, dict)]
        if not routes or routed_concepts != list(row.get("concept_ids") or []):
            raise ValueError(f"Rock idea {idea_id} has invalid concept route provenance")
        for route in routes:
            if set(route) != {"concept_id", "basis", "signal"} or route.get("basis") not in {
                "official_category",
                "title_keyword",
            }:
                raise ValueError(f"Rock idea {idea_id} has an invalid concept route")
        for link in row.get("evidence_links") or []:
            validate_idea_evidence_link(idea_id, link)


def validate_idea_evidence_link(idea_id: str, link: Any) -> None:
    if not isinstance(link, dict):
        raise ValueError(f"Rock idea {idea_id} has a non-object evidence link")
    allowed_fields = {"link_kind", "target_kind", "target_id", "url", "origin", "authority_tier"}
    if set(link) - allowed_fields or not link.get("url"):
        raise ValueError(f"Rock idea {idea_id} has an invalid evidence link shape")
    origin = str(link.get("origin") or "")
    if origin not in {"proposal", "staff_response"}:
        raise ValueError(f"Rock idea {idea_id} has an invalid evidence link origin")
    expected = classify_idea_evidence_link(str(link["url"]), origin=origin)
    if expected != link:
        raise ValueError(f"Rock idea {idea_id} has a non-allowlisted or non-canonical evidence link")


def build_rock_idea_artifacts_from_normalized() -> dict[str, int]:
    rows = list(read_jsonl(ROCK_IDEA_PATH))
    if rows:
        validate_rock_idea_rows(rows)
    summary = read_json_object(ROCK_IDEA_SUMMARY_PATH)
    checked_at = str(summary.get("last_checked_at") or utc_now())
    relationships = build_rock_idea_relationship_artifacts(rows, checked_at=checked_at)
    if summary:
        normalized_rows = list(read_jsonl(ROCK_IDEA_NORMALIZED_PATH))
        normalized_source_hash = source_content_hash(
            {
                "source_records": {
                    str(row.get("id") or ""): row
                    for row in normalized_rows
                    if row.get("id")
                }
            },
            "rock_ideas",
        )
        if normalized_source_hash:
            summary["source_content_hash"] = normalized_source_hash
            summary["source_content_hash_algorithm"] = NORMALIZED_SOURCE_HASH_ALGORITHM
        summary["relationships"] = relationships
        ROCK_IDEA_SUMMARY_PATH.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        render_rock_idea_guide(summary)
    return {
        "rock_ideas": len(rows),
        "rock_idea_relationships": int(relationships["relationship_count"]),
        "rock_idea_verification_queue": int((relationships.get("verification_queue") or {}).get("queue_count") or 0),
    }


def build_rock_idea_summary(
    rows: list[dict[str, Any]],
    *,
    checked_at: str,
    page_count: int,
    catalog_complete: bool,
    detail_selected: int,
    detail_refreshed: int,
    normalized_rows: Optional[list[dict[str, Any]]] = None,
    previous: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    catalog_content_hash = sha256_text(
        json.dumps(
            [(row["idea_id"], row["content_hash"]) for row in rows],
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    content_changed_at = (
        previous.get("content_changed_at")
        if previous
        and previous.get("catalog_content_hash") == catalog_content_hash
        and previous.get("content_changed_at")
        else checked_at
    )
    normalized_source_hash = ""
    if normalized_rows is not None:
        normalized_source_hash = source_content_hash(
            {
                "source_records": {
                    str(row.get("id") or ""): row
                    for row in normalized_rows
                    if row.get("id")
                }
            },
            "rock_ideas",
        )
    return {
        "schema": "rock-kb-rock-idea-summary-v1",
        "generated_at": checked_at,
        "last_checked_at": checked_at,
        "content_changed_at": content_changed_at,
        "catalog_content_hash": catalog_content_hash,
        "source_content_hash": normalized_source_hash or str((previous or {}).get("source_content_hash") or ""),
        "source_content_hash_algorithm": (
            NORMALIZED_SOURCE_HASH_ALGORITHM
            if normalized_source_hash
            else str((previous or {}).get("source_content_hash_algorithm") or "")
        ),
        "status": "ok" if catalog_complete else "incomplete",
        "source_id": "rock_ideas",
        "record_count": len(rows),
        "result_count": len(rows),
        "latest_idea_number": max((int(row["number"]) for row in rows), default=0),
        "by_status": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
        "by_category": dict(sorted(Counter(str(row["category"]) for row in rows).items())),
        "by_concept": dict(sorted(Counter(value for row in rows for value in row.get("concept_ids") or []).items())),
        "catalog_page_count": page_count,
        "catalog_complete": catalog_complete,
        "detail_rows_selected": detail_selected,
        "detail_rows_refreshed": detail_refreshed,
        "detail_rows_failed": max(0, detail_selected - detail_refreshed),
        "detail_shape_version": ROCK_IDEA_DETAIL_SHAPE_VERSION,
        "detail_shape_current_count": sum(
            1 for row in rows if int(row.get("detail_shape_version") or 0) >= ROCK_IDEA_DETAIL_SHAPE_VERSION
        ),
        "evidence_link_count": sum(len(row.get("evidence_links") or []) for row in rows),
        "discovery": {
            "method": "Complete traversal of the public Feature Request View WebForms pager.",
            "coverage": "The artifact is replaced only after traversal reaches the final native catalog page without an empty or repeated page.",
            "detail_enrichment": "New, lifecycle-changed, old-shape, and least-recently checked ideas receive bounded rolling detail-page enrichment.",
            "rejected_primary_method": "The Obsidian Universal Search block action is capped at about 200 results per query and is not used as the catalog source of record.",
        },
        "public_shape": [
            "idea_id",
            "title",
            "url",
            "category",
            "status",
            "vote_count",
            "planned_version",
            "ministry_strength",
            "feature_size",
            "timestamps",
            "concept_ids",
            "concept_routes",
            "allowlisted evidence links without anchor or surrounding text",
        ],
        "excluded_shape": ["submitter identity", "organization identity", "proposal body", "staff response text or identity", "comments"],
        "trust_boundary": "Idea metadata is a feature-gap and roadmap routing signal. It is never sufficient evidence that a feature exists, is absent, or applies to an instance.",
    }


def read_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def render_rock_idea_guide(summary: dict[str, Any]) -> None:
    lines = [
        "# Rock Ideas Intelligence",
        "",
        "Rock Community Ideas are indexed as bounded metadata for finding known feature gaps and tracking community roadmap states.",
        "",
        "## Trust Boundary",
        "",
        "- An idea is a community request, not an approved product claim.",
        "- `Planned`, `Started`, and `Complete` are roadmap labels. Confirm actual release availability through official documentation, release notes, source code, and local read-only checks.",
        "- The public KB does not republish proposal bodies, comments, submitter identities, organization identities, or staff response text.",
        "",
        "## Agent Use",
        "",
        "1. Search Ideas only when the question is explicitly about a feature request, known product gap, or roadmap state.",
        "2. Use typed relationships to route to concepts, exact multiword models, explicitly linked issues, and corroborating official records.",
        "3. Treat `references_issue` as an explicit link only. It does not prove the issue implements the Idea; `implemented_by_issue` requires official release-note evidence.",
        "4. If the idea has a planned version or completed state, corroborate it with official release evidence before saying the feature is available.",
        "5. Treat open and not-planned ideas as research leads, not proof that no workaround or newer capability exists.",
        "6. Use the verification queue to prioritize lifecycle claims. A queue state or private candidate count is not public evidence; only reviewed or deterministic official relationships can corroborate availability.",
        "",
        f"Current generated catalog: {summary.get('record_count', 0)} metadata rows. See [`agent/rock-ideas.jsonl`](../../agent/rock-ideas.jsonl), [`agent/rock-idea-relationships.jsonl`](../../agent/rock-idea-relationships.jsonl), [`agent/rock-idea-verification-queue.jsonl`](../../agent/rock-idea-verification-queue.jsonl), and [`agent/rock-idea-summary.json`](../../agent/rock-idea-summary.json).",
    ]
    ROCK_IDEA_GUIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROCK_IDEA_GUIDE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def concept_ids_for_idea(category: str, title: str) -> list[str]:
    return [route["concept_id"] for route in concept_routes_for_idea(category, title)]


def concept_routes_for_idea(category: str, title: str) -> list[dict[str, str]]:
    routes = [
        {
            "concept_id": CATEGORY_CONCEPTS.get(category, "platform-configuration"),
            "basis": "official_category",
            "signal": category,
        }
    ]
    lowered = title.lower()
    keyword_routes = [
        (("document", "signature", "e-sign"), "documents-signatures"),
        (("hosting", "server", "infrastructure", "azure", "database"), "hosting-infrastructure"),
        (("prayer", "pastoral care"), "prayer-care"),
        (("step", "streak", "assessment", "achievement", "engagement"), "engagement-tracking"),
        (("personalization", "personalize", "adaptive message", "segment"), "content-personalization"),
        (("obsidian", "block action"), "obsidian-development"),
        (("helix",), "helix"),
        (("apple tv", "tvos"), "apple-tv"),
        (("roku",), "roku"),
        (("schedule", "calendar", "location"), "scheduling-locations"),
        (("registration", "registrant", "waitlist"), "event-registration"),
        (("family", "person", "campus"), "people-families"),
        (("security", "permission", "authorization"), "security-permissions"),
        (("report", "data view", "analytics"), "data-views-reports"),
    ]
    seen = {routes[0]["concept_id"]}
    for needles, concept in keyword_routes:
        signal = next((needle for needle in needles if needle in lowered), "")
        if signal and concept not in seen:
            routes.append({"concept_id": concept, "basis": "title_keyword", "signal": signal})
            seen.add(concept)
    return routes


def lifecycle_phase(status: str) -> str:
    if status == "complete":
        return "completed_label"
    if status in {"planned", "started"}:
        return "roadmap_commitment_label"
    if status == "not_planned":
        return "not_planned_label"
    return "request_or_review"


def idea_content_hash(row: dict[str, Any]) -> str:
    payload = {
        key: row.get(key)
        for key in [
            "idea_id",
            "title",
            "url",
            "category",
            "status",
            "status_label",
            "status_is_inferred",
            "vote_count",
            "planned_version",
            "ministry_strength",
            "feature_size",
            "submitted_at",
            "response_updated_at",
            "staff_response_present",
            "detail_shape_version",
            "evidence_links",
            "concept_ids",
            "concept_routes",
        ]
    }
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def canonical_idea_url(url: str) -> str:
    parsed = urlparse(url)
    path = quote(unquote(parsed.path), safe="/-._~").rstrip("/")
    return f"https://community.rockrms.com{path}"


def idea_number_from_url(url: str) -> Optional[int]:
    match = re.search(r"/ideas/(?P<number>[1-9][0-9]*)(?:/|$)", urlparse(url).path, re.IGNORECASE)
    return int(match.group("number")) if match else None


def parse_strength(value: Optional[str]) -> Optional[dict[str, int]]:
    if not value:
        return None
    match = re.fullmatch(r"\s*(?P<score>[0-9]+)\s*/\s*(?P<maximum>[0-9]+)\s*", value)
    if not match:
        return None
    return {"score": int(match.group("score")), "maximum": int(match.group("maximum"))}


def normalize_planned_version_label(value: str) -> str:
    """Normalize the legacy 1.<major>.<minor> badge to Rock's <major>.<minor> label."""
    match = re.fullmatch(r"1\.(?P<major>[2-9]|[1-9][0-9]+)\.(?P<minor>[0-9]+)", value)
    return f"{match.group('major')}.{match.group('minor')}" if match else value


def parse_int(value: str) -> int:
    match = re.search(r"[0-9]+", value.replace(",", ""))
    return int(match.group(0)) if match else 0


def clean_text(value: str) -> str:
    return " ".join(value.split())


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
