from __future__ import annotations

import json
import importlib.util
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


spec = importlib.util.spec_from_file_location("network_operations_smoke", Path("scripts/network_operations_smoke.py"))
assert spec and spec.loader
network_operations_smoke_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network_operations_smoke_module)
decode_response_payload = network_operations_smoke_module.decode_response_payload
network_operations_smoke = network_operations_smoke_module.network_operations_smoke


class SmokeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.write_json({"status": "ok", "version": "test"})
        elif self.path == "/manifest.json":
            self.write_json({"schema": "manifest"})
        elif self.path == "/operations/dashboard":
            self.write_json({"schema": "rock-kb-operations-dashboard-v2", "issue_reports": {"pending_review_count": 0}})
        elif self.path == "/operations/freshness":
            self.write_json({"schema": "rock-kb-source-operations-v1", "status": "ok", "workflow_count": 3, "source_count": 44})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("content-length") or "0")
        if length:
            self.rfile.read(length)
        if self.path == "/mcp":
            accepted = {
                value.strip()
                for value in (self.headers.get("accept") or "").split(",")
                if value.strip()
            }
            if not {"application/json", "text/event-stream"}.issubset(accepted):
                self.write_json(
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32000,
                            "message": "Client must accept both application/json and text/event-stream",
                        },
                    },
                    status=406,
                )
                return
            self.write_sse(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {
                        "tools": [
                            {"name": "kb_search"},
                            {"name": "kb_get_claims"},
                            {"name": "kb_submit"},
                            {"name": "kb_review_dashboard"},
                            {"name": "kb_get_freshness"},
                            {"name": "kb_report_issue"},
                        ]
                    },
                }
            )
        elif self.path == "/submit":
            self.write_json({"schema": "rock-kb-submit-result-v1", "status": "rejected", "errors": ["unauthorized org token"]})
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *_args):
        return

    def write_json(self, payload, *, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def write_sse(self, payload, *, status=200):
        body = f"event: message\ndata: {json.dumps(payload)}\n\n".encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "text/event-stream; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def test_decode_response_payload_accepts_json():
    payload = {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}

    assert decode_response_payload(json.dumps(payload), "application/json; charset=utf-8") == payload


def test_decode_response_payload_accepts_sse_and_selects_response_event():
    notification = {"jsonrpc": "2.0", "method": "notifications/progress"}
    response = {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}
    body = (
        f"event: message\ndata: {json.dumps(notification)}\n\n"
        f"event: message\ndata: {json.dumps(response)}\n\n"
    )

    assert decode_response_payload(body, "text/event-stream; charset=utf-8") == response


def test_network_operations_smoke_passes_against_expected_service():
    server = ThreadingHTTPServer(("127.0.0.1", 0), SmokeHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        result = network_operations_smoke(base_url, evaluator=lambda _base_url, _limit: {"status": "ok", "pass_count": 100, "fail_count": 0})
    finally:
        server.shutdown()

    assert result["status"] == "ok"
    assert {row["name"]: row["status"] for row in result["checks"]} == {
        "health": "pass",
        "manifest": "pass",
        "operations_dashboard": "pass",
        "source_freshness": "pass",
        "mcp_tools": "pass",
        "unauthorized_submit": "pass",
        "hosted_eval": "pass",
    }


def test_network_operations_smoke_fails_missing_mcp_tool():
    class MissingToolHandler(SmokeHandler):
        def do_POST(self):
            length = int(self.headers.get("content-length") or "0")
            if length:
                self.rfile.read(length)
            if self.path == "/mcp":
                self.write_json({"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "kb_search"}]}})
            elif self.path == "/submit":
                self.write_json({"status": "rejected", "errors": ["unauthorized org token"]})
            else:
                self.send_response(404)
                self.end_headers()

    server = ThreadingHTTPServer(("127.0.0.1", 0), MissingToolHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        result = network_operations_smoke(base_url, evaluator=lambda _base_url, _limit: {"status": "ok", "pass_count": 100, "fail_count": 0})
    finally:
        server.shutdown()

    checks = {row["name"]: row for row in result["checks"]}
    assert result["status"] == "fail"
    assert checks["mcp_tools"]["status"] == "fail"
    assert "missing tools" in checks["mcp_tools"]["message"]


def test_network_operations_smoke_fails_stale_source_workflow():
    class StaleSourceHandler(SmokeHandler):
        def do_GET(self):
            if self.path == "/operations/freshness":
                self.write_json(
                    {
                        "schema": "rock-kb-source-operations-v1",
                        "status": "fail",
                        "blocking_workflow_ids": ["daily-sources"],
                        "blocking_source_ids": [],
                    }
                )
            else:
                super().do_GET()

    server = ThreadingHTTPServer(("127.0.0.1", 0), StaleSourceHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        result = network_operations_smoke(
            base_url,
            evaluator=lambda _base_url, _limit: {"status": "ok", "pass_count": 100, "fail_count": 0},
        )
    finally:
        server.shutdown()

    checks = {row["name"]: row for row in result["checks"]}
    assert result["status"] == "fail"
    assert checks["source_freshness"]["status"] == "fail"
    assert checks["source_freshness"]["evidence"]["blocking_workflow_ids"] == ["daily-sources"]
