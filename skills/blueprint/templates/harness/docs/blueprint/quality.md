# Quality and runtime evidence

Status: unverified. Owner: assign the responsible maintainer during onboarding.

Document the actual setup, focused tests, lint/build commands, app start/stop
commands, and where to inspect logs or UI behavior. A structural pass does not
prove product behavior.

| Invariant or user journey | Check or observation | Evidence | Known gap |
| --- | --- | --- | --- |
| Not assessed | Not configured | None | Inspect the affected flow |

Register deterministic gates in the harness configuration. For application changes,
also reproduce the relevant journey and inspect runtime output; link the evidence
or state why it was unavailable. Do not record an unexecuted plan as passing.

Keep local runs isolated using the project's existing worktree, port, database,
and cleanup conventions. Do not share mutable test state between concurrent runs.
Store no credentials or personal data in committed examples or evidence.

When a recurring failure is observed, add a focused regression check or improve
the relevant tool/document. Do not repeatedly retry unchanged failures or remove
a gate to make the report green.
