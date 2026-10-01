# DEVELOPMENT STATUS

Status: DERIVED_OPERATIONAL_INDEX

Questo file è lo schermo operativo dello sviluppo.
Non è fonte canonica dei dettagli: indicizza piani, task, test, risultati e stato corrente.

## Current state

- Phase: INITIAL FLOW IMPLEMENTATION
- Canonical branch: `main`
- Current canonical base: current `main` HEAD (the commit containing this index)
- Last completed DEV_TASK: [DEV-0022](tasks/DEV-0022/)
- Active DEV_TASK: [DEV-0023](tasks/DEV-0023/)
- Current step: WAITING_HUMAN_REACCEPTANCE_RETEST
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
6. DEV-0018 — SKILL_01 Validation + Activation — PASS
7. DEV-0019 — SKILL_01 Node Runtime Integration — PASS
8. DEV-0020 — SKILL_01 Automated Closure — PASS
9. DEV-0021 — SKILL_01 Human Acceptance — FAIL / REOPENED
10. DEV-0022 — Structured Semantic Model Port for SKILL_01 — PASS
11. DEV-0023 — SKILL_01 Semantic Intake + Human Re-Acceptance — WAITING_HUMAN_ACCEPTANCE
12. DEV-0024 — SKILL_02 Company Analysis Runtime
13. DEV-0025 — SKILL_02 Validation + Activation
14. DEV-0026 — Source Acquisition Capability Port
15. DEV-0027 — SKILL_03 External Validation Runtime
16. DEV-0028 — SKILL_03 Validation + Activation
17. DEV-0029 — SKILL_01 → SKILL_02 → SKILL_03 E2E Flow
18. DEV-0030 — PostgreSQL Repository Adapters
19. DEV-0031 — Temporal Durable Flow

Hard gate before SKILL_02 work:

```text
SKILL_01_CLOSED = PASS
+ SKILL_01_HUMAN_ACCEPTANCE = PASS
```

Current gate status:

```text
SKILL_01_CLOSED (automated) = PASS
SKILL_01_HUMAN_ACCEPTANCE = FAIL
SKILL_01 overall = REOPENED
```

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

- DEV-0018 — SKILL_01 Validation + Activation — PASS
  - integrated validation: 7/7 PASS
  - unit regression: 118/118 PASS
  - SKILL_01@0.1 DRAFT → TESTING → ACTIVE
  - validation evidence: [VALIDATION_EVIDENCE.md](tasks/DEV-0018/VALIDATION_EVIDENCE.md)
  - result: [RESULT.md](tasks/DEV-0018/RESULT.md)

- DEV-0019 — SKILL_01 Node Runtime Integration — PASS
  - `Skill01NodeRuntime`
  - complete in-memory node orchestration
  - authority/context HITL resume
  - node tests: 5/5 PASS; integration: 12/12 PASS; unit regression: 118/118 PASS
  - result: [RESULT.md](tasks/DEV-0019/RESULT.md)

- DEV-0020 — SKILL_01 Full Node Stress, Improvement + Closure — PASS
  - initial stress exposed 4 runtime defects + 1 traceability gap
  - all demonstrated defects corrected
  - stress: 11/11 PASS; integration: 23/23 PASS; unit regression: 118/118 PASS
  - SKILL_01_CLOSED = PASS
  - stress evidence: [STRESS_EVIDENCE.md](tasks/DEV-0020/STRESS_EVIDENCE.md)
  - result: [RESULT.md](tasks/DEV-0020/RESULT.md)

- DEV-0022 — Structured Semantic Model Port — PASS
  - provider-agnostic semantic model port
  - deterministic structured-output validator
  - runtime-control-token rejection
  - semantic tests: 14/14 PASS; integration: 23/23 PASS; unit regression: 132/132 PASS
  - gate: MODEL_OUTPUT_WITHOUT_VALIDATION_CANNOT_ENTER_STATE = PASS
  - result: [RESULT.md](tasks/DEV-0022/RESULT.md)

## Component index

- DOMAIN FOUNDATION — FROZEN
- APPLICATION FOUNDATION — FROZEN
- FLOW RUNTIME — OPERATIONAL_V1
- SKILL_01 — SEMANTIC_INTAKE_READY / HUMAN_REACCEPTANCE_PENDING
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
