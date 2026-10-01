# DEVELOPMENT STATUS

Status: DERIVED_OPERATIONAL_INDEX

Questo file è lo schermo operativo dello sviluppo.
Non è fonte canonica dei dettagli: indicizza piani, task, test, risultati e stato corrente.

## Current state

- Phase: DOMAIN FOUNDATION
- Canonical branch: `main`
- Current canonical base: current `main` HEAD (the commit containing this index)
- Last completed DEV_TASK: [DEV-0006](tasks/DEV-0006/)
- Active DEV_TASK: NONE
- Current step: READY_FOR_NEXT_DEV_TASK
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

## Current development plan

1. DEV-0002 — SourceReference + Evidence — PASS
2. DEV-0003 — Primary Context Record + Version — PASS
3. DEV-0004 — Derived State + Dependency + Staleness — PASS
4. DEV-0005 — Authority Decision domain model — PASS
5. DEV-0006 — Task + Task Context requirements — PASS
6. DEV-0007 — Context repository ports — NEXT
7. DEV-0008 — Evidence repository ports — PLANNED
8. DEV-0009 — Context update application use-case — PLANNED
9. DEV-0010 — Task Context Resolver use-case — PLANNED

## Component index

- DOMAIN — IN_PROGRESS
- APPLICATION — NOT_STARTED
- PERSISTENCE — NOT_STARTED
- AUTHORITY ENGINE — NOT_STARTED
- CONTEXT ENGINE — NOT_STARTED
- SKILL RUNTIME — NOT_STARTED
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
