# Quality and known gaps

Owner: Blueprint maintainers.

| Concern | Gate or evidence | Limit |
| --- | --- | --- |
| Package consistency | `python3 scripts/validate_package.py` | No host installation verification |
| Safe initialization and preflight | CLI integration tests | Not a hostile-code sandbox |
| Failure and timeout reporting | CLI integration tests | Non-POSIX kills only the direct process |
| Interrupted and repeated runs | CLI integration tests | Abrupt host termination may leave partial logs |
| Actual agent engineering behavior | Not evaluated | No reliability, speed, or cost claim |
| Runtime product journeys | Project-specific | No bundled browser or telemetry provisioning |

Run the declared gates through `python3 skills/blueprint/scripts/harness.py check`.
Inspect the returned report path and logs. Evidence directories are ignored; do not
commit generated logs. CI uses the same command on Python 3.10 and 3.12.

The harness checks inline relative file targets, not heading anchors, reference-style
links, external URLs, or whether prose still matches code. Review semantic changes
with the affected implementation. The runner records a commit and dirty flag, not
a reproducible snapshot of uncommitted files.

## Follow-up triggers

- Before claiming agent quality gains: maintain representative task cases and compare
  actual runs for completion, invariant violations, rework, time, and cost.
- When an adopting app needs UI/telemetry proof: integrate its existing runtime tools
  and isolation/cleanup contract; do not substitute structural validation.
- If copied runners drift in real projects: design explicit, reviewed upgrade support.
- Before claiming Windows process-tree cleanup: implement and test that platform.
