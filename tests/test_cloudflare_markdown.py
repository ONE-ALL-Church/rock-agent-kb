import json

import httpx
import pytest

from rock_kb.cloudflare_markdown import cloudflare_markdown_endpoint, extract_cloudflare_markdown


def test_cloudflare_markdown_endpoint():
    assert (
        cloudflare_markdown_endpoint("abc")
        == "https://api.cloudflare.com/client/v4/accounts/abc/browser-rendering/markdown"
    )


def test_extract_cloudflare_markdown_posts_expected_payload():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["authorization"] = request.headers["Authorization"]
        captured["payload"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(200, json={"success": True, "result": "# Rendered"})

    client = httpx.Client(transport=httpx.MockTransport(handler))

    markdown = extract_cloudflare_markdown(
        url="https://www.triumph.tech/resources",
        account_id="acct",
        api_token="token",
        reject_request_patterns=["/^.*\\.(png|jpg)$/"],
        goto_options={"waitUntil": "networkidle"},
        client=client,
    )

    assert markdown == "# Rendered"
    assert captured["url"] == cloudflare_markdown_endpoint("acct")
    assert captured["authorization"] == "Bearer token"
    assert captured["payload"]["url"] == "https://www.triumph.tech/resources"
    assert captured["payload"]["rejectRequestPattern"] == ["/^.*\\.(png|jpg)$/"]
    assert captured["payload"]["gotoOptions"] == {"waitUntil": "networkidle"}


def test_extract_cloudflare_markdown_requires_one_input():
    with pytest.raises(ValueError):
        extract_cloudflare_markdown(account_id="acct", api_token="token")
    with pytest.raises(ValueError):
        extract_cloudflare_markdown(url="https://example.com", html="<p>x</p>", account_id="acct", api_token="token")


def test_extract_cloudflare_markdown_requires_credentials(monkeypatch):
    monkeypatch.delenv("CLOUDFLARE_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("CLOUDFLARE_API_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="CLOUDFLARE_ACCOUNT_ID"):
        extract_cloudflare_markdown(url="https://example.com")
