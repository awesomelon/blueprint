# Sources and adaptation boundary

Harness source reviewed on 2026-10-20. Earlier source notes retained below.

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

The core skill contains instructions, supporting references, and an opt-in
repository harness tool with templates. Its repository packages the same folder
with Codex and Claude Code manifests. No route installs hooks, background jobs,
model-routing rules, or automatic session activation. Naming the skill in a prompt
requests its use; invocation syntax depends on the host's skill support.

## Harness engineering

- OpenAI, Ryan Lopopolo, [Harness engineering: leveraging Codex in an agent-first
  world](https://openai.com/ko-KR/index/harness-engineering/), published 2026-02-11.

The article motivates repository-local knowledge, concise entry-point instructions,
mechanically enforced constraints, accessible runtime evidence, and feedback that
improves the environment after failures. Blueprint applies these ideas through a
small check runner, documentation templates, and an explicit repair loop.

The CLI, schema, defaults, and templates are independent design choices. This
package does not reproduce OpenAI's internal infrastructure or establish the
article's reported productivity in other repositories. Automatic merging, relaxed
gates, and multiple agents are not inferred requirements. Structural tests do not
measure agent behavior or prove an application works.
