# Architecture

Status: unverified. Owner: assign the responsible maintainer during onboarding.

Link existing architecture documentation here. Record only what the affected code
and its callers establish; do not impose a generic layer model.

For each important boundary, capture:

- Entry point, authoritative state, writers, and affected callers.
- Allowed dependency direction and the project check that enforces it.
- Invariant, likely violation, and observable recovery behavior.
- External data validation and authorization at the trust boundary.

For a consequential decision, record the simplest viable alternative, the deciding
constraint, accepted cost, and evidence that would justify reconsideration.
