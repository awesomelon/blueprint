# Architecture and invariants

Owner: Blueprint maintainers. Status: implemented; see [quality](quality.md) for
the distinction between structural checks and behavioral evaluation.

`skills/blueprint/` is the single distributable source for standalone, Codex, and
Claude Code use. SKILL.md selects relevant reference material. The optional
`scripts/harness.py` uses only Python's standard library and reads templates from
the same skill folder. Initialization copies the runner into an adopting repository
so normal doctor/check runs do not depend on the original checkout.

The runner reads `.blueprint/config.json`, validates it and declared documentation,
then executes explicit argv commands in the target repository. Each run writes
isolated evidence under `.blueprint/runs/`. It does not call models or services.

## Invariants

- Initialization never replaces existing files; paths must remain in the repository.
- Doctor does not execute configured commands or write evidence.
- Invalid preflight prevents all configured commands from executing.
- A passing check report requires at least one configured check and every check passing.
- Failure, timeout, launch error, and interruption remain distinguishable in evidence.
- Host manifests package the same skill and agree on version and presentation.
- Existing adaptive depth, read-only review scope, and single-agent defaults remain.

The CLI integration suite enforces execution invariants. The package validator
enforces distribution alignment and inline file-link integrity. Product-specific
dependency boundaries belong to adopting repositories, not a universal layer stack.

## Chosen baseline

Use a small synchronous CLI with JSON configuration before introducing a daemon,
agent SDK, or model orchestrator. This provides inspectable feedback with no
provider credentials and no runtime dependency installation. Accepted costs are
manual registration of project checks and explicit runner upgrades.

Reconsider only when actual adoption demonstrates a need for provider execution,
parallel isolated checks, or managed runner updates. Record concrete failure and
maintenance evidence before expanding the runtime.
