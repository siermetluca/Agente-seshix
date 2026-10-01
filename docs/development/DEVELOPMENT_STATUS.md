# DEVELOPMENT STATUS

Status: DERIVED_OPERATIONAL_INDEX

Questo file è lo schermo operativo dello sviluppo.
Non è fonte canonica dei dettagli: indicizza piani, task, test, risultati e stato corrente.

## Current state

- Phase: INITIAL FLOW IMPLEMENTATION
- Canonical branch: `main`
- Current canonical base: current `main` HEAD (the commit containing this index)
- Last completed DEV_TASK: [DEV-0017](tasks/DEV-0017/)
- Active DEV_TASK: NONE
- Current step: READY_FOR_DEV-0018
- Blockers: NONE

## Implemented

- DEV-0001 — Context Evidence Domain Model — PASS
  - `EvidenceClassification`
  - `Provenance`
  - `ContextValue`
  - tests: 7/7 PASS
  - result: [RESULT.md](tasks/DEV-0001/RESULT.md)

- DEV-0002 — SourceReference + Evidence — PASS
  - `SourceReference`
  - `Evidence`
  - tests: 13/13 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0002/RESULT.md)

- DEV-0003 — Primary Context Record + Version — PASS
  - `PrimaryContextRecord`
  - `PrimaryContextVersion`
  - tests: 20/20 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0003/RESULT.md)

- DEV-0004 — Derived State + Dependency + Staleness — PASS
  - `DependencyReference`
  - `DerivedState`
  - immutable `mark_stale()`
  - tests: 27/27 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0004/RESULT.md)

- DEV-0005 — Authority Decision domain model — PASS
  - `AuthorityOutcome`
  - `AuthorityDecision`
  - tests: 35/35 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0005/RESULT.md)

- DEV-0006 — Task + Task Context requirements — PASS
  - `Task`
  - `ContextSection`
  - `TaskContextRequirements`
  - tests: 45/45 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0006/RESULT.md)

- DEV-0007 — Context repository ports — PASS
  - `PrimaryContextRepository` Protocol
  - save/get operations
  - tests: 48/48 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0007/RESULT.md)

- DEV-0008 — Evidence repository ports — PASS
  - `EvidenceRepository` Protocol
  - save/get operations
  - tests: 51/51 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0008/RESULT.md)

- DEV-0009 — Context update application use-case — PASS
  - `UpdatePrimaryContextCommand`
  - `UpdatePrimaryContextUseCase`
  - tests: 57/57 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0009/RESULT.md)

- DEV-0010 — Task Context Resolver use-case — PASS
  - `TaskContextResolver`
  - `TaskContextPackage`
  - required/optional section validation
  - tests: 61/61 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0010/RESULT.md)

- DEV-0011 — Evidence-backed Primary Context Update — PASS
  - exact Evidence-backed provenance
  - EvidenceRepository enforcement
  - unresolved evidence blocks update
  - tests: 67/67 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0011/RESULT.md)

## Current development plan

1. DEV-0002 — SourceReference + Evidence — PASS
2. DEV-0003 — Primary Context Record + Version — PASS
3. DEV-0004 — Derived State + Dependency + Staleness — PASS
4. DEV-0005 — Authority Decision domain model — PASS
5. DEV-0006 — Task + Task Context requirements — PASS
6. DEV-0007 — Context repository ports — PASS
7. DEV-0008 — Evidence repository ports — PASS
8. DEV-0009 — Context update application use-case — PASS
9. DEV-0010 — Task Context Resolver use-case — PASS

## Foundation milestone

- DEV-0001 → DEV-0010 — COMPLETE
- DOMAIN/APPLICATION FOUNDATION — COMPLETE_FOR_CURRENT_SCOPE
- Gap review: [FOUNDATION_GAP_REVIEW_v0.1.md](FOUNDATION_GAP_REVIEW_v0.1.md)
- DEV-0011 — Evidence-backed Primary Context Update — PASS
- Foundation freeze: [FOUNDATION_FREEZE_v0.1.md](FOUNDATION_FREEZE_v0.1.md)
- Initial flow plan: [INITIAL_FLOW_IMPLEMENTATION_PLAN_v0.1.md](INITIAL_FLOW_IMPLEMENTATION_PLAN_v0.1.md)
- Next DEV_TASK: DEV-0013 — Authority Policy Evaluator

## Gap priority

1. P0 — Evidence → PrimaryContext verification boundary — PASS
2. P1 — Authority evaluator — DEV-0013 NEXT
3. P2 — PostgreSQL repository adapters
4. P3 — Context retrieval source abstraction

Review verification: 61/61 unit tests PASS.

## Flow implementation plan

1. DEV-0013 — Authority Policy Evaluator — PASS
2. DEV-0014 — Skill Registry + Lifecycle — PASS
3. DEV-0015 — Flow Execution Envelope — PASS
4. DEV-0016 — Source/Evidence Intake Use Case — PASS
5. DEV-0017 — SKILL_01 Context Construction Runtime — PASS
6. DEV-0018 — SKILL_01 Validation + Activation — NEXT
7. DEV-0019 — Structured Semantic Model Port
8. DEV-0020 — SKILL_02 Company Analysis Runtime
9. DEV-0021 — SKILL_02 Validation + Activation
10. DEV-0022 — Source Acquisition Capability Port
11. DEV-0023 — SKILL_03 External Validation Runtime
12. DEV-0024 — SKILL_03 Validation + Activation
13. DEV-0025 — SKILL_01 → SKILL_02 → SKILL_03 E2E Flow
14. DEV-0026 — PostgreSQL Repository Adapters
15. DEV-0027 — Temporal Durable Flow

Then extend the same validated lifecycle to SKILL_04–07.

## Flow runtime implemented

- DEV-0013 — Authority Policy Evaluator — PASS
  - `AuthorityPolicyEvaluator`
  - ALLOW / DENY / conditional / HITL paths
  - fail-closed unknown policy paths
  - tests: 80/80 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0013/RESULT.md)

- DEV-0014 — Skill Registry + Lifecycle — PASS
  - `SkillRegistry`
  - explicit version/state metadata
  - validation-gated activation
  - tests: 94/94 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0014/RESULT.md)

- DEV-0015 — Flow Execution Envelope — PASS
  - `FlowExecutionEnvelope`
  - ordered immutable run/step snapshots
  - WAITING_HITL / BLOCKED / FAILED paths
  - tests: 103/103 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0015/RESULT.md)

- DEV-0016 — Source/Evidence Intake Use Case — PASS
  - `EvidenceIntakeUseCase`
  - duplicate-id protection
  - SOURCE → EVIDENCE persistence
  - tests: 110/110 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0016/RESULT.md)

- DEV-0017 — SKILL_01 Context Construction Runtime — PASS
  - `Skill01ContextRuntime`
  - FATTO/IPOTESI/UNKNOWN handling
  - STOP/HITL on required UNKNOWN
  - tests: 118/118 PASS (full unit suite)
  - result: [RESULT.md](tasks/DEV-0017/RESULT.md)

## Component index

- DOMAIN FOUNDATION — FROZEN
- APPLICATION FOUNDATION — FROZEN
- FLOW RUNTIME — OPERATIONAL_V1
- SKILL_01 — TESTING_RUNTIME_READY
- SKILL_02 — NOT_STARTED
- SKILL_03 — NOT_STARTED
- PERSISTENCE — NOT_STARTED
- AUTHORITY ENGINE — OPERATIONAL_V1
- CONTEXT ENGINE — OPERATIONAL_INTAKE_V1
- SKILL RUNTIME — OPERATIONAL_V1
- WORKFLOW / TEMPORAL — NOT_STARTED
- AGENTIC / LANGGRAPH — NOT_STARTED
- INTERFACES / DJANGO API — NOT_STARTED
- CAPABILITIES / CONNECTORS — NOT_STARTED
- END-TO-END BUSINESS FLOWS — NOT_STARTED

## Update rule

Aggiornare questo indice quando:
- viene pianificato un DEV_TASK;
- cambia lo stato del DEV_TASK attivo;
- viene completato uno step significativo;
- viene eseguito un test rilevante;
- compare o si chiude un blocker;
- una PR viene mergiata;
- cambia il piano immediatamente successivo.

I dettagli restano negli artefatti del task. Qui si registra solo indice, stato e riferimento.
