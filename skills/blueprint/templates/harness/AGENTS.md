# Working in this repository

Read the [repository map](docs/blueprint/index.md) and the instructions nearest
the affected code. Keep this entry point short; put detailed knowledge in linked
documents and update it alongside code changes.

- Establish the user-visible outcome and the invariant that must hold.
- Use existing project conventions and the smallest sufficient implementation.
- Run relevant checks and inspect their evidence before claiming completion.
- Design and review requests stay read-only. Preserve unrelated changes.
- Use one agent unless the user explicitly requests delegation.
- A failing check is evidence to investigate, not a reason to weaken the gate.

Harness commands, after project checks are configured:

```bash
python3 .blueprint/harness.py doctor
python3 .blueprint/harness.py check
```
