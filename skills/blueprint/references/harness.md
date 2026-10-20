# Repository harness

The skill supplies judgment. A repository supplies its own context, deterministic
gates, runtime observations, and durable work state. The bundled tool connects
those pieces without invoking a model or installing hooks.

## Adopt only what the task needs

For an ordinary task in an existing project, use its current tooling. Do not
initialize a harness just because Blueprint is active. Design/review requests
remain read-only. Set up these files when the user requests a harness or equivalent
repository tooling work.

Inspect root and nested instructions, existing docs, CI, and actual test commands.
Link authoritative material instead of creating a competing source of truth.

From the complete installed skill package:

```bash
python3 /path/to/blueprint/scripts/harness.py init --root /path/to/project --dry-run
python3 /path/to/blueprint/scripts/harness.py init --root /path/to/project
```

`init` copies a self-contained runner to `.blueprint/harness.py`, a JSON configuration,
and a small documentation map. Existing files are preserved, including AGENTS.md.
Review the created/preserved list. If AGENTS.md existed, add a link to the new map
within the authorized change. Re-running init fills missing files, not upgrades.
Review runner updates as normal code changes.

Populate docs from inspected project evidence and register real commands:

```json
{
  "schema_version": 1,
  "documents": ["AGENTS.md", "docs/blueprint/index.md"],
  "checks": [
    {
      "name": "contracts",
      "argv": ["python3", "-m", "unittest", "discover", "-s", "tests"],
      "cwd": ".",
      "timeout_seconds": 120
    }
  ]
}
```

This is a Python example, not a prescribed stack. Use existing lint, dependency,
type, build, migration, and regression checks as appropriate. Each check requires
a unique lowercase name, an argv array, a repository-relative cwd, and an integer
timeout from 1 to 3600 seconds. Empty checks fail rather than imply readiness.
The document list must be nonempty Markdown paths within the repository.

## Execute and inspect

```bash
python3 .blueprint/harness.py doctor --json
python3 .blueprint/harness.py check --json
```

- `doctor` validates configuration, document presence, and inline relative file
  links. It executes no configured commands and writes no files.
- `check` first runs doctor. A failed preflight runs no commands. Otherwise it
  executes all registered checks sequentially, collecting each result even after
  a failure. No shell is implicitly involved. Shell operators and variable expansion
  are not supported; use an existing project script when necessary.
- Every check is required. A nonzero exit, launch error, timeout, or interrupt
  prevents a passing report. Exit codes are 0 for success, 1 for failed gates,
  2 for configuration/I/O errors, and 130 for an interrupted check run.
- Reports and combined stdout/stderr logs are stored under a unique
  `.blueprint/runs/<run-id>/`. JSON contains command, cwd, timing, exit status,
  and log location. Git commit and dirty state are best-effort provenance, not a
  snapshot of uncommitted contents.
- Commands run with the caller's permissions and inherited environment. Read the
  config and scripts before running them in an unfamiliar repository. This is
  not a sandbox. Logs stay local; review them before sharing because project
  commands may print sensitive data.
- Timeout/interrupt kills the process group on POSIX. On other platforms only the
  direct process is killed. Checks should be finite commands, not detached services.

## Close the feedback loop

1. Establish the outcome and invariant; choose the smallest revealing baseline.
2. Reproduce the failure or observe the current behavior. Record pre-existing failures.
3. Implement and run the focused check. Read the log, not just the status.
4. If it fails, distinguish product, environment, test, and missing-context causes.
   Gather new evidence before another attempt. Never suppress a gate to claim success.
5. Exercise the affected runtime journey where applicable using the project's
   existing start/stop, worktree, port, and data isolation conventions.
6. Finish required gates, review the diff, and update affected docs and plan state.
   Report unresolved failures and unavailable observations explicitly.

The runner executes a single pass. The agent performs bounded diagnosis and repair
within the user's scope; it does not need a second model or mandatory reviewer.
Two attempts with the same failure and no new evidence are a signal to stop blind
retries and identify the blocker. Further attempts need a changed hypothesis or input.

## Keep knowledge useful

Keep root instructions as a short map. Project architecture docs own boundary rules;
existing structural tests/lints enforce them. Choose the project's actual dependency
direction rather than imposing the source article's example layer stack.

Use a durable plan for long-running work: outcome, invariant, decisions, progress,
next action, verification evidence, and unresolved risk. Keep an evidence-backed
quality inventory and debt entries with an owner and revisit trigger.

On relevant changes, check that linked docs still describe the code. If the user
requests a maintenance pass, inspect drift and propose or implement a small targeted
repair. The tool does not infer semantic freshness, validate Markdown heading anchors
or reference-style links, fetch external links, or schedule maintenance. It does not
boot an application, provision observability, call models, merge PRs, or change host
settings. Add such capabilities only for a concrete project requirement.
