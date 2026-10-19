# Failure lenses

Read only the lenses relevant to the affected operation. These are investigation
prompts, not default requirements to add infrastructure.

## Concurrent state changes

- Identify the invariant, competing writers, and the exact read/write ordering
  that can violate it. Inspect transaction boundaries and database isolation.
- Compare an atomic conditional write, database constraint, optimistic concurrency,
  or a short database lock using the actual data model. Do not prescribe one by
  keyword. Confirm every competing path participates in the chosen mechanism.
- Keep retries bounded and handle conflicts visibly. Avoid locks over slow
  external calls. Evaluate lock ordering if multiple records are involved.
- Verify the relevant interleaving using coordinated transactions or requests.
  Sequential success is insufficient evidence for a concurrency fix.

## Retries and side effects

- Distinguish at-most-once execution, retryable delivery, and idempotent business
  effects. Do not promise exactly-once behavior without a defined scope and proof.
- Check what happens if a commit succeeds but its response is lost. Where
  deduplication is needed, define key scope, lifetime, and behavior for a reused
  key with a different payload.
- Examine the gap between commit and notification or dispatch. Add an outbox or
  queue only when its guarantee is needed and operating cost justified. An
  in-memory flag is not durable recovery.

## Frontend and API state

- Separate local interaction state from authoritative server state. Inspect cache
  invalidation, cancellation, stale responses, and navigation when relevant.
- For optimistic updates, define reconciliation and rollback. Retain server-side
  validation and permissions even when the UI already checks them.
- Verify loading, empty, failure, and success states the changed flow can reach;
  preserve keyboard access and accessible status feedback where affected.

## Large content and search

- Determine bounded data size, concurrency, memory expansion, rendering cost,
  retention, and authorization before selecting transport.
- Separate network streaming from rendering and search. Streaming alone does not
  bound retained DOM or memory. Browser find cannot search unloaded or virtualized
  content; partial loading needs an explicit search contract.
- Prefer a bounded simple download or text view when sufficient. Add pagination,
  virtualization, or server search for a measured limit or required capability.
  Avoid realtime infrastructure for static data.

## Performance and capacity

- Locate the critical path with evidence. Separate network wait, server execution,
  database time, and rendering before choosing an optimization.
- Derive only quantities that influence the choice: request rate, peak concurrency,
  transfer volume, storage growth, or working set. Preserve units and distinguish
  averages, peaks, and percentiles.
- For caching, define freshness, invalidation, ownership, authorization scope, and
  behavior on cache failure. A faster incorrect answer is not a win.
- Consider backpressure and bounded resources before multiplying workers or retries.
  Tie scaling to saturation or a stated service objective.

## Deployment and recovery

- Confirm versions, on-premise or cloud constraints, available services, and
  operational ownership from evidence. Do not assume managed services.
- For schema or API evolution, check mixed-version behavior and data migration.
  Prefer reversible sequencing; identify steps that cannot be rolled back.
- Distinguish reverting code from restoring transformed or deleted data. Define
  rollout checks and failure signals proportional to the change.
