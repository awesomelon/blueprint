# Blueprint

**Design for what must hold.**

Blueprint is a reusable engineering skill for Codex and Claude Code. It establishes
requirements, traces data and API contracts, identifies invariants, and chooses the
simplest design that handles the relevant failures. Implementation requests continue
through the authorized change and verification; design and review requests remain read-only.

## How it works

1. Establish the outcome, constraints, and what must remain true.
2. Trace authoritative state, API contracts, and affected callers.
3. Choose a sufficient baseline using existing capabilities where possible.
4. Examine relevant failures and bottlenecks; estimate capacity only when it affects a choice.
5. Complete the requested work and distinguish verification from assumptions.

A small local edit receives a quick pass. Shared-state changes receive more investigation.
Cross-service changes and costly migrations receive deeper comparison, failure analysis,
and rollout considerations. These depths do not change the host's model or reasoning settings.

Use one agent by default. Subagents require an explicit user request. The package contains
instructions only: no runtime, hooks, background jobs, or automatic session activation.

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

## Contents

- [Core skill](skills/blueprint/SKILL.md)
- [Conditional failure lenses](skills/blueprint/references/failure-lenses.md)
- [Sources and adaptation boundary](skills/blueprint/references/sources.md)

The portable root manifest and Codex/Claude compatibility manifests package the same skill.
This is a separate project from Tact.

## Evidence and limitations

This initial version draws on freeCodeCamp's official introduction to
[Design Software Systems Like a Senior Engineer](https://www.youtube.com/watch?v=soTfFFIQQ8U)
and uses Ponytail as a reference for concise behavioral guidance. The full course transcript
was not verified. The workflow is an independent adaptation, not the lecturer's exact wording.

Package metadata and local references can be checked structurally. That does not establish
behavioral effectiveness, host installation, or a measured quality/cost improvement.

## License

[MIT](LICENSE).
