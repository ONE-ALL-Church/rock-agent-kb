from __future__ import annotations

import argparse
import json
import os
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from urllib import error, request

from .validator import validate_bundle
from .installer import (
    SKILL_POLICIES,
    SUPPORTED_AGENTS,
    check_agents,
    install_agents,
    passive_skill_checks,
    selected_agents,
    set_skill_policy,
    skill_status,
    update_agents,
)
from .issue_watch import run_issue_watch
from .okf import conform_okf, download_okf, inspect_okf, verify_okf
from .cohort_test import REVIEW_OUTCOMES, build_test_round_review, review_outcomes_from_payload, run_cohort_test

DEFAULT_BASE_URL = "https://rock-agent-kb.oneandall.church"
COHORT_VALUES = ("external-test", "maintainer")
REQUEST_COHORT = ""
PASSIVE_SKILL_CHECK_COMMANDS = {
    "search",
    "result",
    "claim",
    "concepts",
    "get",
    "claims",
    "model",
    "model-map",
    "recipe",
    "recipes",
    "issue",
    "issues",
    "idea",
    "ideas",
    "manifest",
    "dashboard",
    "test-round",
}


def package_version() -> str:
    try:
        return version("rock-kb")
    except PackageNotFoundError:
        return "dev"


USER_AGENT = f"rock-kb-client/{package_version()} (+https://github.com/ONE-ALL-Church/rock-agent-kb)"


def main(argv: list[str] | None = None) -> int:
    global REQUEST_COHORT
    parser = argparse.ArgumentParser(prog="rock-kb")
    parser.add_argument("--url", default=os.environ.get("ROCK_KB_URL", DEFAULT_BASE_URL), help="Rock KB service base URL")
    parser.add_argument(
        "--cohort",
        default=os.environ.get("ROCK_KB_COHORT", ""),
        help="Optional aggregate telemetry cohort: external-test or maintainer. This is not authentication.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--min-tier", default="routing_context_only")
    search.add_argument("--full", action="store_true", help="Include full row bodies and payloads. Compact results are the default.")

    result = subparsers.add_parser("result")
    result.add_argument("result_id")

    claim = subparsers.add_parser("claim")
    claim.add_argument("claim_id")

    subparsers.add_parser("concepts")
    get = subparsers.add_parser("get")
    get.add_argument("concept_id")

    claims = subparsers.add_parser("claims")
    claims.add_argument("concept_id")
    claims.add_argument("--tier")
    claims.add_argument("--min-tier", default="routing_context_only")

    model = subparsers.add_parser("model")
    model.add_argument("model")
    model.add_argument("--fields")
    model.add_argument("--property")
    model.add_argument("--format", choices=["json", "markdown"], default="json")

    model_map = subparsers.add_parser("model-map")
    model_map_subparsers = model_map.add_subparsers(dest="model_map_command", required=True)
    model_map_subparsers.add_parser("list")
    model_map_get = model_map_subparsers.add_parser("get")
    model_map_get.add_argument("model")
    model_map_get.add_argument("--fields")
    model_map_get.add_argument("--property")
    model_map_get.add_argument("--format", choices=["json", "markdown"], default="json")

    recipe = subparsers.add_parser("recipe")
    recipe.add_argument("recipe_args", nargs="+")
    recipe.add_argument("--rock-version")

    recipes = subparsers.add_parser("recipes")
    recipes_subparsers = recipes.add_subparsers(dest="recipes_command", required=True)
    recipes_list = recipes_subparsers.add_parser("list")
    recipes_list.add_argument("--concept")
    recipes_search = recipes_subparsers.add_parser("search")
    recipes_search.add_argument("query")
    recipes_search.add_argument("--limit", type=int, default=10)

    issue = subparsers.add_parser("issue", help="Get one exact Rock product issue; this is separate from report-issue.")
    issue.add_argument("issue_ref", help="GitHub URL, canonical ID, core number, or mobile:number.")

    issues = subparsers.add_parser("issues", help="Search, list, assess, and plan investigation of public Rock issues.")
    issues_subparsers = issues.add_subparsers(dest="issues_command", required=True)
    issues_list = issues_subparsers.add_parser("list")
    issues_list.add_argument("--repository", choices=["core", "mobile", "SparkDevNetwork/Rock", "SparkDevNetwork/Rock.Mobile-Issues"])
    issues_list.add_argument("--state", choices=["open", "closed"])
    issues_list.add_argument("--concept")
    issues_list.add_argument("--version")
    issues_list.add_argument("--limit", type=int, default=50)
    issues_list.add_argument("--offset", type=int, default=0)
    issues_search = issues_subparsers.add_parser("search")
    issues_search.add_argument("query")
    issues_search.add_argument("--limit", type=int, default=10)
    issues_assess = issues_subparsers.add_parser("assess")
    issues_assess.add_argument("profile", type=Path, help="Bounded JSON profile with versions, platforms, concepts, and capabilities only.")
    issues_assess.add_argument("--limit", type=int, default=100)
    issues_assess.add_argument("--offset", type=int, default=0)
    issues_watch = issues_subparsers.add_parser("watch", help="Store a private local baseline and report changes in relevant public Rock issues.")
    issues_watch.add_argument("profile", type=Path, help="Bounded JSON profile with versions, platforms, concepts, and capabilities only.")
    issues_watch.add_argument("--state", type=Path, help="Private local snapshot path. Defaults under the user state directory.")
    issues_watch.add_argument("--page-size", type=int, default=500)
    issues_watch.add_argument("--reset", action="store_true", help="Replace any existing baseline after a complete assessment succeeds.")
    issues_watch.add_argument("--no-write", action="store_true", help="Compare without changing the local snapshot.")
    issues_plan = issues_subparsers.add_parser("plan")
    issues_plan.add_argument("issue_ref")
    issues_plan.add_argument("--include-private-instance", action="store_true")

    idea = subparsers.add_parser("idea", help="Get one exact Rock Community idea metadata row.")
    idea.add_argument("idea_ref", help="Idea number, canonical ID, or public Rock Community URL.")

    ideas = subparsers.add_parser("ideas", help="Search and list Rock Community feature-request and roadmap metadata.")
    ideas_subparsers = ideas.add_subparsers(dest="ideas_command", required=True)
    ideas_search = ideas_subparsers.add_parser("search")
    ideas_search.add_argument("query")
    ideas_search.add_argument("--limit", type=int, default=10)
    ideas_list = ideas_subparsers.add_parser("list")
    ideas_list.add_argument("--status", choices=["not_planned", "under_review", "started", "planned", "pending", "open", "complete"])
    ideas_list.add_argument("--category")
    ideas_list.add_argument("--concept")
    ideas_list.add_argument("--planned-version")
    ideas_list.add_argument("--limit", type=int, default=50)
    ideas_list.add_argument("--offset", type=int, default=0)

    subparsers.add_parser("manifest")
    subparsers.add_parser("dashboard")
    test_round = subparsers.add_parser("test-round", help="Run the public structured church testing cohort cases.")
    test_round.add_argument("--review", action="store_true", help="Prompt for one fixed manual outcome for every case.")
    test_round.add_argument("--review-file", type=Path, help="Read case outcomes from a bounded JSON object instead of prompting.")
    test_round.add_argument("--submit", action="store_true", help="Submit the complete structured review for aggregate maintainer reporting.")

    feedback = subparsers.add_parser("feedback")
    feedback.add_argument("result_id")
    feedback.add_argument("--rating", type=int, choices=[-1, 1], required=True)
    feedback.add_argument("--reason", choices=["helpful", "outdated", "missing", "incorrect", "wrong_route"], required=True)

    report_issue = subparsers.add_parser("report-issue", help="Report a structured Rock KB malfunction for maintainer review.")
    report_issue.add_argument("--failure-type", choices=["service", "mcp", "cli", "schema", "authentication", "retrieval"], required=True)
    report_issue.add_argument("--operation", required=True, help="Short operation identifier, such as search or mcp_tool_call.")
    report_issue.add_argument("--error-code", required=True, help="Short structured error code; do not paste an error message.")
    report_issue.add_argument("--description", required=True, help="Short redacted summary; never include logs, queries, secrets, or private Rock data.")
    report_issue.add_argument("--result-id", help="Optional public Rock KB result ID.")
    report_issue.add_argument("--http-status", type=int, help="Optional HTTP status from 100 through 599.")
    report_issue.add_argument("--redaction-attested", action="store_true", required=True, help="Attest that the description contains no logs, queries, secrets, or private Rock data.")

    validate = subparsers.add_parser("validate")
    validate.add_argument("bundle", type=Path)

    auth_check = subparsers.add_parser("auth-check")
    auth_check.add_argument("--org", required=True)
    add_token_options(auth_check)

    submit = subparsers.add_parser("submit")
    submit.add_argument("bundle", type=Path)
    submit.add_argument("--org", help="Defaults to the org_id in the bundle when every row has the same org_id.")
    submit.add_argument("--dry-run", action="store_true", help="Validate hosted auth and bundle without opening a PR.")
    add_token_options(submit)

    subparsers.add_parser("mcp-config")

    okf = subparsers.add_parser("okf")
    okf_subparsers = okf.add_subparsers(dest="okf_command", required=True)
    okf_download = okf_subparsers.add_parser("download")
    okf_download.add_argument("--version", default="latest", help="Release version or 'latest'.")
    okf_download.add_argument("--format", choices=["zip", "tar.gz"], default="zip")
    okf_download.add_argument("--profile", choices=["full", "core"], default="full")
    okf_download.add_argument("--destination", type=Path)
    okf_download.add_argument("--force", action="store_true")
    okf_inspect = okf_subparsers.add_parser("inspect")
    okf_inspect.add_argument("bundle", type=Path)
    okf_conformance = okf_subparsers.add_parser("conformance")
    okf_conformance.add_argument("bundle", type=Path)
    okf_verify = okf_subparsers.add_parser("verify")
    okf_verify.add_argument("bundle", type=Path)
    okf_validate = okf_subparsers.add_parser("validate")
    okf_validate.add_argument("bundle", type=Path)

    skill = subparsers.add_parser("skill", help="Check, update, inspect, or pin the installed Rock KB agent skill.")
    skill_subparsers = skill.add_subparsers(dest="skill_command", required=True)
    skill_check = skill_subparsers.add_parser("check", help="Check the hosted skill manifest without changing agent files.")
    add_skill_target_options(skill_check)
    skill_check.add_argument("--if-due", action="store_true", help="Skip the network check when a successful check is less than 24 hours old.")
    skill_check.add_argument("--skip-verify", action="store_true", help="Skip the hosted health check.")
    skill_update = skill_subparsers.add_parser("update", help="Back up and update the managed skill and MCP configuration.")
    add_skill_target_options(skill_update)
    skill_update.add_argument("--unpin", action="store_true", help="Clear a pinned policy before updating.")
    skill_update.add_argument("--skip-verify", action="store_true", help="Skip the hosted health check.")
    skill_status_parser = skill_subparsers.add_parser("status", help="Inspect local skill state without a network request.")
    add_skill_target_options(skill_status_parser)
    skill_status_parser.add_argument("--format", choices=["json", "text"], default="json")
    skill_policy = skill_subparsers.add_parser("policy", help="Persist notify, auto, or pinned update behavior.")
    skill_policy.add_argument("policy", choices=SKILL_POLICIES)
    add_skill_target_options(skill_policy)

    install_agent = subparsers.add_parser("install-agent")
    install_agent.add_argument("--agent", action="append", choices=[*SUPPORTED_AGENTS, "all"], help="Agent host to configure. Repeat for multiple hosts; defaults to detected hosts.")
    install_agent.add_argument("--scope", choices=["user", "project"], default="user")
    install_agent.add_argument("--project-dir", type=Path, default=Path.cwd())
    install_agent.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    install_agent.add_argument("--dry-run", action="store_true")
    install_agent.add_argument("--skip-verify", action="store_true", help="Skip the hosted health check.")

    args = parser.parse_args(argv)
    if args.cohort and args.cohort not in COHORT_VALUES:
        parser.error(f"--cohort must be one of: {', '.join(COHORT_VALUES)}")
    REQUEST_COHORT = str(args.cohort or "")
    base_url = str(args.url).rstrip("/")
    if args.command in PASSIVE_SKILL_CHECK_COMMANDS:
        for notice in passive_skill_checks(
            base_url=base_url,
            home=Path.home().expanduser().resolve(),
            project_dir=Path.cwd().resolve(),
            fetch_text=get_text,
            fetch_json=get_json,
            client_version=package_version(),
        ):
            if notice.get("status") == "updated":
                suffix = " Restart or reload the agent before the next task." if notice.get("restart_required") else ""
                print(f"Rock KB agent skill updated automatically.{suffix}", file=sys.stderr)
            elif notice.get("status") == "update_available":
                print("Rock KB agent skill update available. Run: uvx rock-kb skill update", file=sys.stderr)
    if args.command == "test-round":
        if args.submit and not (args.review or args.review_file):
            parser.error("test-round --submit requires --review or --review-file")
        if args.review and args.review_file:
            parser.error("test-round accepts either --review or --review-file, not both")
        if args.submit and REQUEST_COHORT not in COHORT_VALUES:
            parser.error("test-round --submit requires --cohort external-test or --cohort maintainer")

    if args.command == "search":
        detail = "full" if args.full else "compact"
        return print_json(get_json(f"{base_url}/search?q={quote(args.query)}&limit={args.limit}&min_tier={quote(args.min_tier)}&detail={detail}"))
    if args.command == "result":
        return print_json(get_json(f"{base_url}/results/{quote(args.result_id)}"))
    if args.command == "claim":
        return print_json(get_json(f"{base_url}/claims/id/{quote(args.claim_id)}"))
    if args.command == "concepts":
        return print_json(get_json(f"{base_url}/concepts"))
    if args.command == "get":
        return print_text(get_text(f"{base_url}/concepts/{quote(args.concept_id)}.md"))
    if args.command == "claims":
        suffix = f"?min_tier={quote(args.min_tier)}"
        if args.tier:
            suffix += f"&tier={quote(args.tier)}"
        return print_json(get_json(f"{base_url}/claims/{quote(args.concept_id)}{suffix}"))
    if args.command == "model":
        return print_model(base_url, args.model, args.fields, args.property, args.format)
    if args.command == "model-map":
        if args.model_map_command == "list":
            return print_json(get_json(f"{base_url}/model-map/models"))
        if args.model_map_command == "get":
            return print_model(base_url, args.model, args.fields, args.property, args.format)
    if args.command == "recipe":
        if args.recipe_args[0] == "verify":
            if len(args.recipe_args) != 2:
                parser.error("recipe verify requires a recipe_id")
            suffix = f"?rock_version={quote(args.rock_version)}" if args.rock_version else ""
            return print_json(get_json(f"{base_url}/recipes/{quote(args.recipe_args[1])}/verify{suffix}"))
        if len(args.recipe_args) != 1:
            parser.error("recipe requires one recipe_id, or use recipe verify <recipe_id>")
        return print_json(get_json(f"{base_url}/recipes/{quote(args.recipe_args[0])}"))
    if args.command == "recipes":
        if args.recipes_command == "list":
            suffix = f"?concept={quote(args.concept)}" if args.concept else ""
            return print_json(get_json(f"{base_url}/recipes{suffix}"))
        if args.recipes_command == "search":
            return print_json(get_json(f"{base_url}/search?q={quote(args.query)}&limit={args.limit}&min_tier=routing_context_only&kind=recipe&detail=compact"))
    if args.command == "issue":
        return print_json(get_json(f"{base_url}/rock-issues/{quote(args.issue_ref)}"))
    if args.command == "issues":
        if args.issues_command == "search":
            return print_json(get_json(f"{base_url}/rock-issues/search?q={quote(args.query)}&limit={args.limit}"))
        if args.issues_command == "list":
            params = [f"limit={args.limit}", f"offset={args.offset}"]
            for key in ["repository", "state", "concept", "version"]:
                value = getattr(args, key)
                if value:
                    params.append(f"{key}={quote(value)}")
            return print_json(get_json(f"{base_url}/rock-issues?{'&'.join(params)}"))
        if args.issues_command == "assess":
            profile = json.loads(args.profile.read_text(encoding="utf-8"))
            if not isinstance(profile, dict):
                parser.error("issues assess profile must contain a JSON object")
            payload = {"profile": profile, "limit": args.limit}
            if args.offset:
                payload["offset"] = args.offset
            return print_json(post_json(f"{base_url}/rock-issues/assess", payload))
        if args.issues_command == "watch":
            profile = json.loads(args.profile.read_text(encoding="utf-8"))
            if not isinstance(profile, dict):
                parser.error("issues watch profile must contain a JSON object")
            return print_json(
                run_issue_watch(
                    profile=profile,
                    service=base_url,
                    fetch_page=lambda payload: post_json(f"{base_url}/rock-issues/assess", payload),
                    state_path=args.state,
                    page_size=args.page_size,
                    reset=bool(args.reset),
                    write=not bool(args.no_write),
                )
            )
        if args.issues_command == "plan":
            suffix = "?include_private_instance=true" if args.include_private_instance else ""
            return print_json(get_json(f"{base_url}/rock-issues/{quote(args.issue_ref)}/plan{suffix}"))
    if args.command == "idea":
        return print_json(get_json(f"{base_url}/rock-ideas/{quote(args.idea_ref)}"))
    if args.command == "ideas":
        if args.ideas_command == "search":
            return print_json(get_json(f"{base_url}/rock-ideas/search?q={quote(args.query)}&limit={args.limit}"))
        if args.ideas_command == "list":
            params = [f"limit={args.limit}", f"offset={args.offset}"]
            for argument, parameter in [
                ("status", "status"),
                ("category", "category"),
                ("concept", "concept"),
                ("planned_version", "planned_version"),
            ]:
                value = getattr(args, argument)
                if value:
                    params.append(f"{parameter}={quote(value)}")
            return print_json(get_json(f"{base_url}/rock-ideas?{'&'.join(params)}"))
    if args.command == "manifest":
        return print_json(get_json(f"{base_url}/manifest.json"))
    if args.command == "dashboard":
        return print_json(get_json(f"{base_url}/operations/dashboard"))
    if args.command == "test-round":
        report = run_cohort_test(base_url=base_url, get_json=get_json, post_json=post_json)
        if args.review or args.review_file:
            try:
                if args.review_file:
                    outcomes = review_outcomes_from_payload(json.loads(args.review_file.read_text(encoding="utf-8")))
                else:
                    outcomes = prompt_for_test_round_outcomes(report)
                review = build_test_round_review(report, outcomes)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                parser.error(f"invalid test-round review: {exc}")
            submission = None
            if args.submit:
                submission = post_json(f"{base_url}/test-rounds/review", review)
            print_json({"schema": "rock-kb-community-test-round-result-v1", "test_round": report, "review": review, "submission": submission})
            if args.submit and (not isinstance(submission, dict) or submission.get("status") != "recorded"):
                return 1
        else:
            print_json(report)
        return 0 if report["status"] == "ok" else 1
    if args.command == "feedback":
        return print_json(post_json(f"{base_url}/feedback", {"result_id": args.result_id, "rating": args.rating, "reason": args.reason}))
    if args.command == "report-issue":
        payload = {
            "failure_type": args.failure_type,
            "operation": args.operation,
            "error_code": args.error_code,
            "description": args.description,
            "redaction_attested": bool(args.redaction_attested),
        }
        if args.result_id:
            payload["result_id"] = args.result_id
        if args.http_status is not None:
            payload["http_status"] = args.http_status
        return print_json(post_json(f"{base_url}/issues/report", payload))
    if args.command == "validate":
        errors = validate_bundle(args.bundle)
        if errors:
            for error in errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        return print_json({"status": "ok", "file": str(args.bundle)})
    if args.command == "auth-check":
        token = resolve_token(args)
        if not token:
            print(missing_token_message(args.org), file=sys.stderr)
            return 1
        return print_json(post_json(f"{base_url}/auth/check", {"org_id": args.org}, token=token))
    if args.command == "submit":
        errors = validate_bundle(args.bundle)
        if errors:
            for error in errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        rows = [json.loads(line) for line in args.bundle.read_text(encoding="utf-8").splitlines() if line.strip()]
        org_id = args.org or infer_org_id(rows)
        if not org_id:
            print("ERROR --org is required when bundle rows do not all use the same org_id", file=sys.stderr)
            return 1
        token = resolve_token(args)
        if not token:
            print(missing_token_message(org_id), file=sys.stderr)
            return 1
        return print_json(post_json(f"{base_url}/submit", {"org_id": org_id, "bundle": rows, "dry_run": bool(args.dry_run)}, token=token))
    if args.command == "mcp-config":
        server = {
            "type": "http",
            "url": f"{base_url}/mcp",
        }
        if REQUEST_COHORT:
            server["headers"] = {"x-rock-kb-cohort": REQUEST_COHORT}
        return print_json(
            {
                "mcpServers": {
                    "rock-kb": server
                }
            }
        )
    if args.command == "okf":
        if args.okf_command == "download":
            return print_json(
                download_okf(
                    version=args.version,
                    archive_format=args.format,
                    profile=args.profile,
                    destination=args.destination,
                    force=bool(args.force),
                    user_agent=USER_AGENT,
                )
            )
        if args.okf_command == "inspect":
            return print_json(inspect_okf(args.bundle))
        if args.okf_command == "conformance":
            report = conform_okf(args.bundle)
            print_json(report)
            return 0 if report["status"] == "ok" else 1
        if args.okf_command in {"verify", "validate"}:
            report = verify_okf(args.bundle)
            print_json(report)
            return 0 if report["status"] == "ok" else 1
    if args.command == "skill":
        home = args.home.expanduser().resolve()
        project_dir = args.project_dir.expanduser().resolve()
        agents = selected_agents(args.agent, home)
        if args.skill_command == "check":
            report = check_agents(
                base_url=base_url,
                agents=agents,
                scope=args.scope,
                home=home,
                project_dir=project_dir,
                verify=not bool(args.skip_verify),
                fetch_text=get_text,
                fetch_json=get_json,
                client_version=package_version(),
                if_due=bool(args.if_due),
            )
            print_json(report)
            return 0 if report.get("status") != "no_agents_detected" else 1
        if args.skill_command == "update":
            report = update_agents(
                base_url=base_url,
                agents=agents,
                scope=args.scope,
                home=home,
                project_dir=project_dir,
                verify=not bool(args.skip_verify),
                fetch_text=get_text,
                fetch_json=get_json,
                client_version=package_version(),
                unpin=bool(args.unpin),
            )
            print_json(report)
            return 0 if report.get("status") not in {"no_agents_detected", "pinned"} else 1
        if args.skill_command == "status":
            report = skill_status(base_url=base_url, agents=agents, scope=args.scope, home=home, project_dir=project_dir)
            if args.format == "text":
                print_text(format_skill_status(report))
            else:
                print_json(report)
            return 0
        if args.skill_command == "policy":
            try:
                report = set_skill_policy(
                    base_url=base_url,
                    policy=args.policy,
                    agents=agents,
                    scope=args.scope,
                    home=home,
                    project_dir=project_dir,
                )
            except ValueError as exc:
                print_json({"schema": "rock-kb-skill-policy-v1", "status": "error", "error": str(exc)})
                return 1
            print_json(report)
            return 0 if report.get("status") != "not_installed" else 1
    if args.command == "install-agent":
        agents = selected_agents(args.agent, args.home)
        report = install_agents(
            base_url=base_url,
            agents=agents,
            scope=args.scope,
            home=args.home.expanduser().resolve(),
            project_dir=args.project_dir.expanduser().resolve(),
            dry_run=bool(args.dry_run),
            verify=not bool(args.skip_verify),
            fetch_text=get_text,
            fetch_json=get_json,
            client_version=package_version(),
        )
        print_json(report)
        return 0 if report.get("status") != "no_agents_detected" else 1
    return 1


def add_skill_target_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--agent", action="append", choices=[*SUPPORTED_AGENTS, "all"], help="Agent host to inspect or update. Repeat for multiple hosts; defaults to detected or previously managed hosts.")
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)


def format_skill_status(report: dict) -> str:
    lines = [
        f"Rock KB skill: {report.get('status', 'unknown')}",
        f"Policy: {report.get('policy', 'notify')}",
        f"Scope: {report.get('scope', 'user')}",
        f"Check due: {'yes' if report.get('check_due') else 'no'}",
    ]
    if report.get("last_checked_at"):
        lines.append(f"Last checked: {report['last_checked_at']}")
    for agent in report.get("agents") or []:
        lines.append(f"{agent['agent']}: {agent['status']} ({agent['skill_path']})")
    return "\n".join(lines) + "\n"


def add_token_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--token-file", type=Path, help="Read the submit token from a secret-mounted file.")
    parser.add_argument("--token-stdin", action="store_true", help="Read the submit token from stdin.")


def resolve_token(args) -> str:
    if getattr(args, "token_stdin", False):
        return sys.stdin.read().strip()
    token_file = getattr(args, "token_file", None) or (Path(os.environ["ROCK_KB_TOKEN_FILE"]) if os.environ.get("ROCK_KB_TOKEN_FILE") else None)
    if token_file:
        return token_file.read_text(encoding="utf-8").strip()
    return os.environ.get("ROCK_KB_TOKEN", "").strip()


def infer_org_id(rows: list[dict]) -> str:
    org_ids = {str(row.get("org_id") or "") for row in rows}
    org_ids.discard("")
    return next(iter(org_ids)) if len(org_ids) == 1 else ""


def missing_token_message(org_id: str) -> str:
    return (
        "ERROR hosted submission requires a per-organization submit token.\n"
        f"Org: {org_id}\n"
        "Ask a Rock KB maintainer to review orgs/<org-id>.yaml and issue or rotate a token outside git.\n"
        "Provide it to this command with ROCK_KB_TOKEN, ROCK_KB_TOKEN_FILE, --token-file, or --token-stdin."
    )


def prompt_for_test_round_outcomes(report: dict) -> dict[str, str]:
    choices = ", ".join(REVIEW_OUTCOMES)
    outcomes: dict[str, str] = {}
    for case in report.get("cases") or []:
        case_id = str(case.get("case_id") or "")
        prompt = str(case.get("manual_review_prompt") or case_id)
        while True:
            value = input(f"{case_id}: {prompt}\nOutcome ({choices}): ").strip().lower()
            if value in REVIEW_OUTCOMES:
                outcomes[case_id] = value
                break
            print(f"Choose one of: {choices}", file=sys.stderr)
    return outcomes


def print_model(base_url: str, model: str, fields: str | None, property_name: str | None, format_name: str) -> int:
    params = []
    if fields:
        params.append(f"fields={quote(fields)}")
    if property_name:
        params.append(f"property={quote(property_name)}")
    if format_name:
        params.append(f"format={quote(format_name)}")
    suffix = f"?{'&'.join(params)}" if params else ""
    url = f"{base_url}/model-map/models/{quote(model)}{suffix}"
    if format_name == "markdown":
        return print_text(get_text(url))
    return print_json(get_json(url))


def get_json(url: str):
    return json.loads(get_text(url))


def get_text(url: str) -> str:
    req = request.Request(url, headers=client_headers())
    with request.urlopen(req) as response:
        return response.read().decode("utf-8")


def post_json(url: str, payload: dict, token: str = ""):
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method="POST",
        headers={**client_headers(), "content-type": "application/json", "accept": "application/json"},
    )
    if token:
        req.add_header("authorization", f"Bearer {token}")
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def quote(value: str) -> str:
    from urllib.parse import quote as url_quote

    return url_quote(value, safe="")


def client_headers() -> dict[str, str]:
    headers = {
        "user-agent": USER_AGENT,
        "x-rock-kb-client": "cli",
        "x-rock-kb-client-version": package_version(),
    }
    if REQUEST_COHORT:
        headers["x-rock-kb-cohort"] = REQUEST_COHORT
    return headers


def print_json(value) -> int:
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


def print_text(value: str) -> int:
    print(value, end="" if value.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
