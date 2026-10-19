# Sources and adaptation boundary

Reviewed on 2026-10-19.

## Course

- User-supplied video: [Design Software Systems Like a Senior Engineer – Complete
  Course](https://www.youtube.com/watch?v=soTfFFIQQ8U).
- Primary source: [freeCodeCamp's official course
  introduction](https://www.freecodecamp.org/news/learn-how-to-design-software-systems-like-a-senior-engineer-in-our-new-course/),
  published 2026-10-16.

The official introduction confirms a five-step approach to ambiguous system-design
questions, worked examples, simple starting architectures, bottleneck analysis,
capacity estimates, and technical trade-offs. These ideas motivate this skill.

The full video transcript was not retrieved or verified. The five operational steps
in SKILL.md are an original implementation-oriented adaptation, not a claim about
the lecturer's exact wording or step labels. Failure lenses, task-depth selection,
single-agent behavior, verification rules, and user-facing output are additions.
Do not attribute these additions to the lecturer or invent timestamps or quotations.

## Ponytail

- [Official repository](https://github.com/DietrichGebert/ponytail)
- [Core skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)

Ponytail was inspected as a reference for a concise, reusable behavior-changing
skill. It already considers affected code, scope, correctness, and verification;
do not describe it as concerned only with reducing lines of code.

Blueprint is independently written. Its emphasis is explicit invariants, data and
API contracts, failure behavior, and criteria for reconsidering a design. It is
not a fork, an official integration, or a replacement for Ponytail's runtime hooks.
Do not claim reduced cost, faster work, or better reliability without evaluation.

## Delivery scope

The core skill contains instructions and supporting references. Its repository
also packages it with optional Codex and Claude Code plugin manifests. Neither
route installs hooks, background jobs, model-routing rules, or automatic session
activation. Naming the skill in a prompt requests its use; availability and
invocation syntax depend on the host application's skill support.
