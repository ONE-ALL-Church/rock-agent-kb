from __future__ import annotations

import os
from typing import Any, Optional

import httpx

from .extract import USER_AGENT

CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4"


def cloudflare_markdown_endpoint(account_id: str) -> str:
    return f"{CLOUDFLARE_API_BASE}/accounts/{account_id}/browser-rendering/markdown"


def cloudflare_markdown_env_ready() -> bool:
    return bool(os.getenv("CLOUDFLARE_ACCOUNT_ID") and os.getenv("CLOUDFLARE_API_TOKEN"))


def extract_cloudflare_markdown(
    *,
    url: Optional[str] = None,
    html: Optional[str] = None,
    account_id: Optional[str] = None,
    api_token: Optional[str] = None,
    timeout: float = 90.0,
    reject_request_patterns: Optional[list[str]] = None,
    goto_options: Optional[dict[str, Any]] = None,
    user_agent: str = USER_AGENT,
    client: Optional[httpx.Client] = None,
) -> str:
    """Return Markdown from Cloudflare Browser Rendering.

    This is intentionally optional infrastructure. Local extraction remains the
    default rebuild path so the KB is not dependent on hosted scraping.
    """
    if not url and not html:
        raise ValueError("url or html is required.")
    if url and html:
        raise ValueError("Provide either url or html, not both.")

    account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = api_token or os.getenv("CLOUDFLARE_API_TOKEN")
    if not account_id or not api_token:
        raise RuntimeError("CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN are required for Cloudflare extraction.")

    payload: dict[str, Any] = {"userAgent": user_agent}
    if url:
        payload["url"] = url
    if html:
        payload["html"] = html
    if reject_request_patterns:
        payload["rejectRequestPattern"] = reject_request_patterns
    if goto_options:
        payload["gotoOptions"] = goto_options

    owns_client = client is None
    client = client or httpx.Client(timeout=timeout)
    try:
        response = client.post(
            cloudflare_markdown_endpoint(account_id),
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
    finally:
        if owns_client:
            client.close()

    if not data.get("success", False):
        raise RuntimeError(f"Cloudflare markdown extraction failed: {data.get('errors') or data}")
    result = data.get("result")
    if not isinstance(result, str):
        raise RuntimeError("Cloudflare markdown extraction returned no Markdown result.")
    return result
