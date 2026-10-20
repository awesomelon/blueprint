#!/usr/bin/env python3
"""Repository-local checks and evidence. Python 3.10+, standard library only."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import uuid
from urllib.parse import unquote, urlsplit


CONFIG = ".blueprint/config.json"


class HarnessError(Exception):
    """An actionable configuration or filesystem error."""


def local_path(root, value):
    """Resolve a repository path without allowing absolute paths or escapes."""
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise HarnessError(f"Expected a nonempty relative path, got {value!r}.")
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise HarnessError(f"Path escapes the repository: {value!r}. Use a local path.")
    return path


def load_config(root):
    path = local_path(root, CONFIG)
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise HarnessError(f"Cannot read {CONFIG}: {exc}. Run init or repair the file.") from exc
    if not isinstance(config, dict):
        raise HarnessError(f"{CONFIG} must contain a JSON object.")
    if set(config) != {"schema_version", "documents", "checks"}:
        raise HarnessError("Config keys must be schema_version, documents, checks.")
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise HarnessError("Unsupported schema_version. Expected integer 1.")
    documents = config["documents"]
    if not isinstance(documents, list) or not documents:
        raise HarnessError("documents must be a nonempty list of local Markdown paths.")
    for document in documents:
        path = local_path(root, document)
        if path.suffix != ".md":
            raise HarnessError(f"Document must be Markdown: {document!r}.")
    if len(set(documents)) != len(documents):
        raise HarnessError("documents contains duplicate paths.")
    checks = config["checks"]
    if not isinstance(checks, list):
        raise HarnessError("checks must be a list.")
    names = set()
    for check in checks:
        if not isinstance(check, dict) or set(check) != {
            "name", "argv", "cwd", "timeout_seconds"
        }:
            raise HarnessError("Each check needs name, argv, cwd, timeout_seconds.")
        name = check["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", name):
            raise HarnessError("Check names must match [a-z][a-z0-9_-]{0,63}.")
        if name in names:
            raise HarnessError(f"Duplicate check name: {name}.")
        names.add(name)
        argv = check["argv"]
        if not isinstance(argv, list) or not argv or any(
            not isinstance(arg, str) or "\0" in arg for arg in argv
        ) or not argv[0]:
            raise HarnessError(f"{name}: argv must be a nonempty list of strings.")
        cwd = local_path(root, check["cwd"])
        if not cwd.is_dir():
            raise HarnessError(f"{name}: cwd does not exist: {check['cwd']}.")
        timeout = check["timeout_seconds"]
        if type(timeout) is not int or not 1 <= timeout <= 3600:
            raise HarnessError(f"{name}: timeout_seconds must be an integer from 1 to 3600.")
    return config


def document_errors(root, documents):
    """Check inline file links. Remote URLs and heading anchors are not fetched."""
    errors = []
    for document in documents:
        path = local_path(root, document)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{document}: cannot read document: {exc}.")
            continue
        # Ignore fenced code; examples are not maintained cross-references.
        text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", "", text)
        for match in re.finditer(r"!?\[[^\]\n]*\]\(<([^>\n]+)>\)|!?\[[^\]\n]*\]\(([^)\s]+)\)", text):
            target = match.group(1) or match.group(2)
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            relative = unquote(parsed.path)
            try:
                if Path(relative).is_absolute():
                    raise HarnessError("Use a relative file link.")
                resolved = local_path(root, str(path.parent.relative_to(root) / relative))
                if not resolved.exists():
                    errors.append(f"{document}: broken link {target!r}. Fix the link or restore its target.")
            except HarnessError as exc:
                errors.append(f"{document}: invalid link {target!r}: {exc}")
    return errors


def diagnose(root):
    config = load_config(root)
    errors = document_errors(root, config["documents"])
    if not config["checks"]:
        errors.append("No checks configured. Add real project commands to .blueprint/config.json.")
    warnings = []
    agents = root / "AGENTS.md"
    if agents.is_file() and not agents.is_symlink():
        text = agents.read_text(encoding="utf-8")
        if "docs/blueprint/index.md" not in text:
            warnings.append("Link docs/blueprint/index.md from AGENTS.md so agents can find the harness.")
    return config, {"status": "fail" if errors else "pass", "errors": errors, "warnings": warnings}


def initialize(root, dry_run):
    template_root = Path(__file__).resolve().parent.parent / "templates" / "harness"
    if not template_root.is_dir():
        raise HarnessError("init needs the complete Blueprint skill package, including templates/harness.")
    sources = [(p.relative_to(template_root).as_posix(), p) for p in sorted(template_root.rglob("*")) if p.is_file()]
    sources.append((".blueprint/harness.py", Path(__file__).resolve()))
    # Validate every target before creating any files. Existing files are never replaced.
    targets = [(name, source, local_path(root, name)) for name, source in sources]
    created, preserved = [], []
    for name, source, target in targets:
        if (root / name).is_symlink() or target.exists():
            preserved.append(name)
            continue
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as output:
                output.write(source.read_bytes())
        created.append(name)
    return {
        "status": "planned" if dry_run else "initialized",
        "created": created,
        "preserved": preserved,
        "next": "Read docs/blueprint/index.md, configure real checks, then run doctor and check.",
    }


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def git_state(root):
    """Best-effort provenance; a dirty flag is not a full worktree snapshot."""
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, timeout=5
        )
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, timeout=5
        )
        if revision.returncode or status.returncode:
            return None
        return {"commit": revision.stdout.strip(), "dirty": bool(status.stdout.strip())}
    except (OSError, subprocess.TimeoutExpired):
        return None


def stop_process(process):
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:
        process.kill()
    process.wait()


def execute_check(root, check, run_dir):
    started = time.monotonic()
    result = {**check, "started_at": utc_now(), "exit_code": None}
    log_path = run_dir / f"{check['name']}.log"
    result["log"] = str(log_path.relative_to(root))
    process = None
    with log_path.open("xb") as output:
        try:
            process = subprocess.Popen(
                check["argv"], cwd=local_path(root, check["cwd"]),
                stdout=output, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                start_new_session=os.name == "posix",
            )
            result["exit_code"] = process.wait(timeout=check["timeout_seconds"])
            result["status"] = "pass" if result["exit_code"] == 0 else "fail"
        except subprocess.TimeoutExpired:
            stop_process(process)
            result["status"] = "timeout"
        except KeyboardInterrupt:
            if process is not None:
                stop_process(process)
            result["status"] = "interrupted"
        except OSError as exc:
            result.update(status="error", error=str(exc))
    result["duration_seconds"] = round(time.monotonic() - started, 3)
    return result


def run_checks(root, config, diagnosis):
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:12]
    run_dir = local_path(root, f".blueprint/runs/{run_id}")
    run_dir.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 1, "run_id": run_id, "started_at": utc_now(),
        "git": git_state(root), "doctor": diagnosis, "checks": [],
    }
    interrupted = False
    for check in config["checks"]:
        if interrupted:
            report["checks"].append({**check, "status": "not_run"})
            continue
        result = execute_check(root, check, run_dir)
        report["checks"].append(result)
        interrupted = result["status"] == "interrupted"
    report["status"] = "pass" if all(c["status"] == "pass" for c in report["checks"]) else "fail"
    report["finished_at"] = utc_now()
    report["report"] = str((run_dir / "report.json").relative_to(root))
    temporary = run_dir / "report.json.tmp"
    temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    temporary.replace(run_dir / "report.json")
    return report, 130 if interrupted else (0 if report["status"] == "pass" else 1)


def emit(result, as_json):
    if as_json:
        print(json.dumps(result, indent=2))
        return
    print(f"Blueprint: {result['status']}")
    for key in ("errors", "warnings", "created", "preserved"):
        for item in result.get(key, []):
            print(f"  {key}: {item}")
    for check in result.get("checks", []):
        print(f"  {check['name']}: {check['status']}")
        if check.get("error"):
            print(f"    {check['error']}")
    for key in ("report", "next"):
        if key in result:
            print(f"  {key}: {result[key]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "doctor", "check"):
        command = commands.add_parser(name)
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--json", action="store_true")
        if name == "init":
            command.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if not root.is_dir():
            raise HarnessError(f"Repository directory does not exist: {root}.")
        if args.command == "init":
            result, code = initialize(root, args.dry_run), 0
        else:
            config, result = diagnose(root)
            code = 0 if result["status"] == "pass" else 1
            if args.command == "check" and code == 0:
                result, code = run_checks(root, config, result)
        emit(result, args.json)
        return code
    except (HarnessError, OSError, UnicodeError, ValueError) as exc:
        emit({"status": "error", "errors": [str(exc)]}, args.json)
        return 2


if __name__ == "__main__":
    sys.exit(main())
