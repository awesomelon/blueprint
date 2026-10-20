# Blueprint repository map

Blueprint packages one engineering skill and its opt-in repository harness.

| Need | Source |
| --- | --- |
| Install and use | [README](../../README.md) |
| Package boundaries and invariants | [Architecture](architecture.md) |
| Validation and known gaps | [Quality](quality.md) |
| Current evolution plan | [Harness v0.2](plans/harness-v0.2.md) |
| Runtime gates | [Configuration](../../.blueprint/config.json) |
| Agent workflow | [Core skill](../../skills/blueprint/SKILL.md) |

Run `python3 -m pip install -r requirements-dev.txt`, then
`python3 skills/blueprint/scripts/harness.py check`. The harness itself uses only
the standard library; package validation additionally parses YAML with PyYAML.
