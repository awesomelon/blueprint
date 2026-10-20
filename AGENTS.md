# Working on Blueprint

Maintain `skills/blueprint/` as the single source for standalone use and both host plugins.
Keep the root portable manifest and both compatibility manifests aligned in name,
version, and presentation. Keep marketplace entries pointed at this repository.
Write maintained project documentation and metadata in English; answer users in their language.
Read the [repository map](docs/blueprint/index.md) for architecture, gates, and plans.

Preserve the skill's adaptive depth, single-agent default, read-only design/review
scope, and explicit distinction between measured evidence and proposed validation.
Keep conditional detail in references. The repository harness is an opt-in
standard-library CLI inside the skill folder. Do not add a model
runtime, automatic hooks, model routing, or mandatory delegation without a request.

Run `python3 skills/blueprint/scripts/harness.py check` before committing.
Parse changed JSON/YAML and check relative links. Do not equate
structural validation with host installation or evaluated model behavior.
Preserve unrelated changes and never force-push. Remote work is scoped to
`awesomelon/blueprint`; do not modify the separate `awesomelon/tact` project.
