from __future__ import annotations

import json
import socket
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import httpx

from .service_eval import evaluate_service
from .service_projection import SERVICE_DIR, build_service_projection


RunCommand = Callable[[list[str], Path], None]


@dataclass(frozen=True)
class QualityThresholds:
    minimum_mrr: float = 0.99
    minimum_recall: float = 1.0
    maximum_duplicate_rate: float = 0.0
    minimum_authority_pass_rate: float = 1.0


def run_service_quality_gate(
    *,
    thresholds: QualityThresholds | None = None,
    concurrency: int = 6,
    target_rank: int = 2,
    run_command: RunCommand | None = None,
) -> dict[str, Any]:
    thresholds = thresholds or QualityThresholds()
    run_command = run_command or run_checked
    projection = build_service_projection()
    with tempfile.TemporaryDirectory(prefix="rock-kb-quality-gate-") as temp_dir:
        state_dir = Path(temp_dir) / "wrangler-state"
        run_command(
            [
                "npx",
                "wrangler",
                "d1",
                "execute",
                "rock-agent-kb",
                "--local",
                "--env",
                "production",
                "--persist-to",
                str(state_dir),
                "--file",
                str(projection.sql_path),
                "--yes",
            ],
            SERVICE_DIR,
        )
        port = available_port()
        log_path = Path(temp_dir) / "wrangler-dev.log"
        with log_path.open("w", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                [
                    "npx",
                    "wrangler",
                    "dev",
                    "--local",
                    "--env",
                    "production",
                    "--persist-to",
                    str(state_dir),
                    "--port",
                    str(port),
                    "--show-interactive-dev-session=false",
                ],
                cwd=SERVICE_DIR,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
            )
            try:
                base_url = f"http://127.0.0.1:{port}"
                wait_for_worker(base_url, process, log_path)
                evaluation = evaluate_service(
                    base_url=base_url,
                    limit=5,
                    concurrency=concurrency,
                    target_rank=target_rank,
                ).as_dict()
            finally:
                terminate_process(process)

    failures = quality_failures(evaluation, thresholds)
    report = {
        "schema": "rock-kb-service-quality-gate-v1",
        "status": "fail" if failures else "ok",
        "projection_version": projection.version,
        "thresholds": {
            "minimum_mrr": thresholds.minimum_mrr,
            "minimum_recall": thresholds.minimum_recall,
            "maximum_duplicate_rate": thresholds.maximum_duplicate_rate,
            "minimum_authority_pass_rate": thresholds.minimum_authority_pass_rate,
        },
        "metrics": evaluation["metrics"],
        "pass_count": evaluation["pass_count"],
        "fail_count": evaluation["fail_count"],
        "failures": failures,
        "failed_questions": [row for row in evaluation.get("results") or [] if row.get("status") == "fail"],
    }
    destination = SERVICE_DIR / "dist" / "lexical-quality-gate.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def quality_failures(evaluation: dict[str, Any], thresholds: QualityThresholds) -> list[str]:
    metrics = evaluation.get("metrics") or {}
    failures: list[str] = []
    if int(evaluation.get("fail_count") or 0):
        failures.append(f"{evaluation['fail_count']} evaluation questions failed")
    checks = [
        ("mean_reciprocal_rank", thresholds.minimum_mrr, "minimum"),
        ("recall_at_target_rank", thresholds.minimum_recall, "minimum"),
        ("duplicate_result_rate", thresholds.maximum_duplicate_rate, "maximum"),
        ("authority_pass_rate", thresholds.minimum_authority_pass_rate, "minimum"),
    ]
    for key, threshold, direction in checks:
        actual = float(metrics.get(key) or 0)
        failed = actual < threshold if direction == "minimum" else actual > threshold
        if failed:
            failures.append(f"{key} {actual:.6f} missed {direction} {threshold:.6f}")
    return failures


def available_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_worker(base_url: str, process: subprocess.Popen[str], log_path: Path, timeout: float = 60) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Wrangler dev exited before readiness:\n{log_path.read_text(encoding='utf-8')[-4000:]}")
        try:
            response = httpx.get(f"{base_url}/health", timeout=2)
            if response.is_success:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"Wrangler dev did not become ready within {timeout:.0f}s")


def terminate_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def run_checked(command: list[str], cwd: Path) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode:
        output = (result.stdout or "").splitlines()
        diagnostic = "\n".join(output[-200:])
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}\n{diagnostic}")
