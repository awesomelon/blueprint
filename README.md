# Blueprint

**Design for what must hold.**

Blueprint combines a reusable engineering skill for Codex and Claude Code with an
opt-in repository harness. The skill establishes requirements, traces contracts,
identifies invariants, and chooses a sufficient design. The harness makes project
knowledge and verification commands available in the repository and records what
actually passed or failed.

Implementation requests continue through the authorized change and verification;
design and review requests remain read-only.

## How it works

1. Establish the outcome, constraints, and what must remain true.
2. Trace authoritative state, API contracts, and affected callers.
3. Choose a sufficient baseline using existing capabilities where possible.
4. Examine relevant failures and bottlenecks; estimate capacity only when it affects a choice.
5. Run checks, inspect evidence, fix failures, and update affected project knowledge.

A small local edit receives a quick pass. Shared-state changes receive more investigation.
Cross-service changes and costly migrations receive deeper comparison, failure analysis,
and rollout considerations. These depths do not change the host's model or reasoning settings.

Use one agent by default. Subagents require an explicit user request. The optional
CLI runs explicit project checks; it does not call models, install hooks, schedule
background work, or automatically activate the skill.

## Set up a repository harness

Use Python 3.10+ and a local checkout or installed copy of the full skill folder.
The harness uses only the standard library.

```bash
python3 /path/to/blueprint/skills/blueprint/scripts/harness.py init --root /path/to/project --dry-run
python3 /path/to/blueprint/skills/blueprint/scripts/harness.py init --root /path/to/project
```

Initialization creates a runner, configuration, and a small documentation map.
It preserves existing files. Link `docs/blueprint/index.md` from an existing
AGENTS.md and populate the docs from actual project evidence.

Register real checks in `.blueprint/config.json`, for example in a Python project:

```json
{
  "schema_version": 1,
  "documents": ["AGENTS.md", "docs/blueprint/index.md"],
  "checks": [
    {
      "name": "tests",
      "argv": ["python3", "-m", "unittest", "discover", "-s", "tests"],
      "cwd": ".",
      "timeout_seconds": 120
    }
  ]
}
```

From the target project's root:

```bash
python3 .blueprint/harness.py doctor
python3 .blueprint/harness.py check --json
```

`doctor` checks configuration and document links without executing commands.
`check` requires a successful preflight, runs each registered command, and writes
reports and logs under `.blueprint/runs/`. Empty checks, failures, launch errors,
timeouts, and interrupted runs cannot produce a passing report. Commands execute
with your current permissions; inspect unfamiliar configurations before running.

See the [harness guide](skills/blueprint/references/harness.md) for schema, exit codes,
evidence limits, updates, and the agent's repair loop.

## Install with Codex

Use a Codex CLI with plugin support, authenticated to GitHub if the repository is private.
Run each command after the preceding one succeeds:

```bash
codex plugin marketplace add awesomelon/blueprint
codex plugin add blueprint@blueprint
```

Start a new conversation and invoke `$blueprint`, or the namespaced skill shown by your host.

## Install with Claude Code

Use a Claude Code CLI with plugin support and GitHub access to this repository:

```bash
claude plugin marketplace add awesomelon/blueprint
claude plugin install blueprint@blueprint
```

Restart Claude Code and invoke `/blueprint:blueprint`.

The same self-contained [skill folder](skills/blueprint/SKILL.md) can also be copied to
a skill directory supported by your host. Preserve an existing installation before replacing it.

## Use

```text
$blueprint Diagnose why simultaneous signatures leave a document pending, then fix it.
```

```text
$blueprint Design a static log viewer with whole-file search. Explain the trade-offs before implementation.
```

```text
$blueprint Review this API change for contract and retry failures. Do not edit files.
```

```text
$blueprint Set up a repository harness using our existing docs, tests, and architecture checks.
```

## Contents

- [Core skill](skills/blueprint/SKILL.md)
- [Conditional failure lenses](skills/blueprint/references/failure-lenses.md)
- [Harness guide](skills/blueprint/references/harness.md)
- [Repository harness CLI](skills/blueprint/scripts/harness.py)
- [Maintainer map](docs/blueprint/index.md)
- [Sources and adaptation boundary](skills/blueprint/references/sources.md)

The portable root manifest and Codex/Claude compatibility manifests package the same skill.
This is a separate project from Tact.

## Evidence and limitations

The engineering workflow draws on freeCodeCamp's official introduction to
[Design Software Systems Like a Senior Engineer](https://www.youtube.com/watch?v=soTfFFIQQ8U)
and uses Ponytail as a reference for concise behavioral guidance. The full course transcript
was not verified. The workflow is an independent adaptation, not the lecturer's exact wording.

The harness is an independent adaptation of OpenAI's
[harness engineering article](https://openai.com/ko-KR/index/harness-engineering/):
repository knowledge, executable constraints, inspectable evidence, and feedback
that improves the environment. It does not reproduce OpenAI's internal systems.

The CLI tests exercise file preservation, preflight, failed commands, timeouts,
interruption, and evidence. Package checks validate metadata and inline file links.
These do not establish host installation, model effectiveness, semantic document
freshness, or measured quality/cost improvement. Application journeys still need
project-specific runtime verification.

## Develop

```bash
python3 -m pip install -r requirements-dev.txt
python3 skills/blueprint/scripts/harness.py check --json
```

CI runs the same gates. PyYAML is a development dependency for package metadata
validation; adopting repositories need no runtime dependencies beyond Python.

## License

[MIT](LICENSE).
