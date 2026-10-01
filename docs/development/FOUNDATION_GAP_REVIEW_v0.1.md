# FOUNDATION GAP REVIEW v0.1

Status: DERIVED_REVIEW

Scope: DEV-0001 through DEV-0010.

## Verified baseline

- DOMAIN/APPLICATION foundation implemented for current scope.
- Full unit suite: 61/61 PASS.
- `PRIMARY_CONTEXT` is versioned and immutable by replacement.
- `EvidenceRepository` and `PrimaryContextRepository` ports exist.
- `UpdatePrimaryContextUseCase` performs targeted versioned updates.
- `TaskContextResolver` selects only requested context and rejects missing required sections.

## P0 gap — Evidence to Primary Context enforcement

Canonical flow requires:

```text
SOURCE
↓
EVIDENCE
↓
CONTEXT / DERIVED STATE
```

and targeted PRIMARY_CONTEXT updates require source/provenance verification before a new version is created.

Current implementation gap:

- `Evidence` has `evidence_id`, source and version.
- `EvidenceRepository` can save/get evidence.
- `Provenance` currently stores only `source_ref`.
- `UpdatePrimaryContextUseCase` accepts a ready-made `PrimaryContextRecord` and does not consult `EvidenceRepository`.
- Therefore a `FATTO` can currently be inserted into a new PRIMARY_CONTEXT version without proving that the supporting Evidence exists.

Decision:

```text
P0
→ close Evidence → PrimaryContext verification boundary before infrastructure persistence
```

Next DEV_TASK candidate:

```text
DEV-0011 — Evidence-backed Primary Context Update
```

Expected responsibility:

- bind a proposed context update to explicit evidence references;
- verify referenced evidence exists;
- preserve source/provenance traceability;
- reject promotion/update when required evidence cannot be resolved;
- keep update versioned and non-destructive.

Exact domain shape is intentionally not fixed by this review and must be resolved in the DEV-0011 context/change plan.

## P1 gap — Authority evaluator

`AuthorityDecision` exists, but no component evaluates policy into ALLOW / DENY / REQUIRES_HITL.

Required before autonomous protected actions or full SKILL_01 runtime.

## P2 gap — PostgreSQL persistence adapter

Repository ports exist but have no real infrastructure implementation.

PostgreSQL remains the frozen source-of-truth persistence owner, but implementing it before P0 would persist a semantically incomplete update path.

## P3 gap — Context retrieval source abstraction

`TaskContextResolver` receives already-available context. Retrieval/acquisition sources are not yet abstracted.

This is not blocking the current pure application behavior and should follow the integrity/authority boundaries.

## Priority

```text
P0 Evidence → PrimaryContext verification
↓
P1 Authority evaluator
↓
P2 PostgreSQL adapters
↓
P3 Context retrieval sources
```
