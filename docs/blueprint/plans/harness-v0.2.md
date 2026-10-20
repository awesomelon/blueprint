# Blueprint v0.2 repository harness

Status: completed (implementation and local validation). Owner: Blueprint maintainers.

## Outcome

Evolve the instruction-only skill into an opt-in repository harness that exposes
project knowledge, runs explicit verification gates, and preserves failure evidence.
The source article and adaptation boundary are recorded in
[sources](../../../skills/blueprint/references/sources.md).

## Constraints and decisions

Preserve existing user files, host packaging, adaptive depth, read-only design/review,
and the single-agent default. Keep the runner inside the standalone skill package.
Use Python 3.10+ standard library, JSON config, sequential finite checks, and
repository-local evidence. No automatic hooks, model runtime, or merge policy changes.

## Progress

- Implemented init/doctor/check, templates, failure evidence, and timeout handling.
- Connected the skill's engineering judgment to a bounded repair and verification loop.
- Added package validation, CLI integration coverage, and CI using the same gates.
- Reviewed the diff and passed package validation and all 16 CLI integration tests.

## Verification

Run `python3 skills/blueprint/scripts/harness.py check --json`.
Exercise empty/malformed configuration, existing-file preservation, invalid paths,
failed commands, missing executables, timeout cleanup, interruption, and repeat runs.
Separate local test results from remote CI, host installation, and model evaluation.

Executed on 2026-10-20 with Python 3.12.14: package validation passed and 16 integration
tests passed, including preservation of a dangling local symlink. The local evidence
run was `20261020T105838Z-788cd396a9ce`; generated reports remain ignored. CI validates
the pushed revision separately. Host installation and agent effectiveness were not tested.

## Next action

Review the draft PR and its CI results before adopting v0.2 in a real project.
Use observed adoption gaps to select the next capability.
