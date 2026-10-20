# Repository map

Status: onboarding incomplete. Replace assumptions with inspected evidence.

| Need | Source |
| --- | --- |
| Boundaries, ownership, invariants | [Architecture](architecture.md) |
| Checks, runtime evidence, known gaps | [Quality](quality.md) |
| Resumable work | [Plans](plans/README.md) |
| Deferred improvements | [Debt](debt.md) |
| Executable checks | [Harness configuration](../../.blueprint/config.json) |

## Complete onboarding

1. Link this map from the root AGENTS.md if it already existed.
2. Link existing authoritative project docs instead of duplicating their contents.
3. Record actual setup, test, and application start commands in the quality guide.
4. Add existing checks to the configuration as argv arrays, with explicit cwd and
   timeout_seconds. Do not invent passing placeholder commands.
5. Run `python3 .blueprint/harness.py doctor`, then
   `python3 .blueprint/harness.py check`. Empty checks deliberately fail.
6. Review the report and logs under `.blueprint/runs/`. Commit the configuration,
   runner, and maintained docs; generated evidence stays local and ignored.

The copied runner is self-contained. For an update, review and replace it explicitly
from the Blueprint package; `init` preserves existing files and is not an upgrader.
