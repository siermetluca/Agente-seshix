# INITIAL FLOW IMPLEMENTATION PLAN v0.1

Status: DERIVED_OPERATIONAL_PLAN

Purpose: move from the frozen foundation to a real executable flow, testing every stage before activating the first process skills.

## Operating principle

Development proceeds as a vertical flow, not as disconnected framework components.

```text
IMPLEMENT ONE STEP
↓
POSITIVE TESTS
↓
NEGATIVE / STOP TESTS
↓
INTEGRATE WITH PREVIOUS STEP
↓
RECORD RESULT
↓
ONLY THEN MOVE FORWARD
```

No skill becomes `ACTIVE` because its code exists.

```text
DRAFT
→ TESTING
→ VALIDATED
→ ACTIVE
```

`ACTIVE` requires bounded behavior, verified outputs, stop conditions, authority handling and repeatable tests.

## Target initial executable flow

Canonical operating flow is larger. The first implementation slice is deliberately limited to the minimum chain needed to operate SKILL_01–03:

```text
REQUEST
↓
TASK / CONTEXT REQUIREMENTS
↓
TASK CONTEXT RESOLUTION
↓
SKILL RESOLUTION
↓
AUTHORITY CHECK
↓
SKILL EXECUTION
↓
OUTPUT VALIDATION
↓
EVIDENCE / DERIVED OUTPUT
↓
STATE UPDATE OR STOP / HITL
```

## Stage 1 — Runtime control prerequisites

### DEV-0013 — Authority Policy Evaluator

Goal:

- evaluate current authority policy into domain outcomes `ALLOW / DENY / REQUIRES_HITL`;
- keep `CAPABILITY != AUTHORITY` enforceable;
- test ALLOW, DENY, conditional and HITL paths.

Gate:

```text
AUTHORITY_DECISION_TESTS = PASS
```

### DEV-0014 — Skill Registry + Lifecycle

Goal:

- represent registered skill version/state;
- states at minimum `DRAFT / TESTING / ACTIVE / DEPRECATED / DISABLED`;
- resolve only compatible enabled skills;
- prevent unvalidated auto-activation.

Gate:

```text
UNVALIDATED_SKILL_CANNOT_BECOME_ACTIVE = PASS
```

### DEV-0015 — Flow Execution Envelope

Goal:

- create one traceable run and ordered steps;
- record task, context package, selected skill, authority result, output/result and stop reason;
- deterministic states for run/step;
- still in-memory: no Temporal yet.

Gate:

```text
RUN_STATE_TRANSITIONS = PASS
STOP_AND_HITL_PATHS = PASS
```

## Stage 2 — SKILL_01 executable

### DEV-0016 — Source/Evidence Intake Use Case

Goal:

- turn explicit source input into persisted Evidence through the existing EvidenceRepository port;
- retain source, claim and version;
- no autonomous scraping required for this first slice.

Gate:

```text
SOURCE → EVIDENCE = PASS
```

### DEV-0017 — SKILL_01 Context Construction Runtime

Goal:

- consume verified Evidence;
- distinguish `FATTO / IPOTESI / UNKNOWN` under the existing rules;
- build/update `COMPANY_CONTEXT_BASELINE` through the evidence-backed update path;
- expose missing relevant information as a stop/HITL requirement rather than inventing it.

Initial acquisition modes:

```text
HITL user input
provided documents/data
already registered Evidence
```

Gate:

```text
EVIDENCE → PRIMARY_CONTEXT = PASS
MISSING_REQUIRED_DATA → STOP/HITL = PASS
NO_INVENTED_FACT = PASS
VERSION_HISTORY = PASS
```

### DEV-0018 — SKILL_01 Validation + Activation

Goal:

- execute repeatable positive and negative scenarios;
- verify provenance, targeted update, contradictions/missing data handling and no silent overwrite;
- promote `SKILL_01` from `TESTING` to `ACTIVE` only if all gates pass.

## Stage 3 — Close SKILL_01 as a complete node

### DEV-0019 — SKILL_01 Node Runtime Integration

Goal:

- build the actual SKILL_01 node coordinator over the already validated components;
- accept a real SKILL_01 task/run input;
- resolve task context;
- resolve the exact ACTIVE SKILL_01 version from SkillRegistry;
- perform authority evaluation before execution;
- ingest explicit source input when present;
- execute Skill01ContextRuntime;
- map WRITTEN / UNKNOWN / WAITING_HITL / errors into FlowExecutionEnvelope states;
- return one traceable node-run result.

The node must orchestrate existing behavior, not duplicate business rules already owned by the components.

Gate:

```text
SKILL_01_NODE_HAPPY_PATH = PASS
SKILL_01_NODE_AUTHORITY_PATHS = PASS
SKILL_01_NODE_HITL_RESUME = PASS
SKILL_01_NODE_TRACEABILITY = PASS
```

### DEV-0020 — SKILL_01 Full Node Stress, Improvement + Closure

Goal:

- execute the complete SKILL_01 node repeatedly against realistic positive and negative scenarios;
- test missing context, missing evidence, malformed input, conflicting updates, repeated updates, authority denial, HITL/resume, unsupported facts, hypotheses and UNKNOWN handling;
- identify real defects or missing runtime behavior;
- improve only where tests demonstrate a concrete need;
- rerun regression after every correction;
- close SKILL_01 only when the whole node is repeatable and all closure gates pass.

Closure gate:

```text
SKILL_01_NODE_COMPLETE = PASS
SKILL_01_NODE_NEGATIVE_SUITE = PASS
SKILL_01_NODE_REPEATABILITY = PASS
SKILL_01_NO_SILENT_STATE_MUTATION = PASS
SKILL_01_HITL_RESUME = PASS
SKILL_01_CLOSED = PASS
```

Only after this gate may development move to the semantic boundary required by SKILL_02.

## Stage 4 — Human acceptance of SKILL_01

### DEV-0021 — SKILL_01 Human Acceptance Harness

Goal:

- expose the complete SKILL_01 node through a local interactive CLI;
- let the human owner see every FlowRun step/state;
- let the human owner personally exercise a normal FACT path, context HITL/resume and authority HITL/approval;
- record human acceptance separately from automated closure.

Hard gate:

```text
SKILL_01_CLOSED = PASS
+ SKILL_01_HUMAN_ACCEPTANCE = PASS
```

No SKILL_02 work is allowed until both are true.

## Stage 5 — Semantic execution boundary required to finish SKILL_01

### DEV-0022 — Structured Semantic Model Port

This boundary is now required first by SKILL_01 remediation, not by SKILL_02.

Goal:

- accept natural source/human input through a structured semantic request;
- produce schema-constrained candidate facts/hypotheses/unknowns;
- validate output before any Evidence/PRIMARY_CONTEXT mutation;
- provider remains replaceable; no provider owns business rules.

Gate:

```text
MODEL_OUTPUT_WITHOUT_VALIDATION_CANNOT_ENTER_STATE = PASS
```

### DEV-0023 — SKILL_01 Semantic Intake + Human Re-Acceptance

Goal:

- replace developer-facing key/claim entry with human/source input;
- extract candidate key/value/claim/classification semantically;
- reject or query ambiguous/nonsensical inputs;
- retain provenance and authority guarantees;
- rerun full automated SKILL_01 closure tests;
- repeat human acceptance with the owner.

Hard gate:

```text
SKILL_01_CLOSED = PASS
+ SKILL_01_HUMAN_ACCEPTANCE = PASS
```

Only after this gate may SKILL_02 begin.

Goal:

- define the application boundary used by `[D-LLM]` skills;
- structured request/output contract;
- schema/domain validation after model output;
- provider remains replaceable; no provider owns business rules.

Gate:

```text
MODEL_OUTPUT_WITHOUT_VALIDATION_CANNOT_ENTER_STATE = PASS
```

## Stage 6 — SKILL_02 executable

### DEV-0024 — SKILL_02 Company Analysis Runtime

Goal:

- read validated PRIMARY_CONTEXT;
- produce derived company analysis only;
- identify criticalities, inefficiencies, assets, capabilities, gaps and hypotheses;
- never modify PRIMARY_CONTEXT directly.

Gate:

```text
PRIMARY_CONTEXT → ANALISI_AZIENDALE_BASELINE = PASS
DERIVED_OUTPUT != PRIMARY_CONTEXT = PASS
```

### DEV-0025 — SKILL_02 Validation + Activation

Goal:

- stress positive, missing-context, contradictory-context and unsupported-conclusion cases;
- promote to `ACTIVE` only after repeatable validated behavior.

## Stage 7 — External-source capability boundary

### DEV-0026 — Source Acquisition Capability Port

Goal:

- define capability boundary for external sources;
- return traceable source/evidence records;
- capability availability never grants authority automatically;
- first implementations may remain HITL/manual where required.

Gate:

```text
CAPABILITY != AUTHORITY = PASS
SOURCE_PROVENANCE = PASS
```

## Stage 8 — SKILL_03 executable

### DEV-0027 — SKILL_03 External Validation Runtime

Goal:

- consume COMPANY_CONTEXT + company analysis + hypotheses;
- gather/consume external Evidence;
- output structured validated market analysis with source/provenance and explicit missing/contradictory data;
- enforce `NESSUNA EVIDENZA SUFFICIENTE → NESSUNA CONCLUSIONE`.

### DEV-0028 — SKILL_03 Validation + Activation

Goal:

- positive and negative source-quality scenarios;
- insufficient evidence;
- contradictory evidence;
- context mismatch;
- activate only after gates pass.

## Stage 9 — First end-to-end skill flow

### DEV-0029 — SKILL_01 → SKILL_02 → SKILL_03 E2E Flow

Scenario:

```text
company/source input
↓
SKILL_01
↓
COMPANY_CONTEXT_BASELINE
↓
SKILL_02
↓
ANALISI_AZIENDALE_BASELINE
↓
SKILL_03
↓
ANALISI_ESTERNA_VALIDATA
```

Must also test:

```text
missing context → HITL/STOP
new primary fact downstream → CONTEXT_CHANGE_CANDIDATE
→ SKILL_01 TARGETED UPDATE
→ new PRIMARY_CONTEXT version
→ recalculate affected downstream step
```

Milestone:

```text
INITIAL_SKILL_FLOW_OPERATIONAL = PASS
SKILL_01 = CLOSED
SKILL_02 = ACTIVE
SKILL_03 = ACTIVE
```

## Stage 10 — Persistence and durability

Only after the behavior above is stable:

### DEV-0030 — PostgreSQL Repository Adapters

- implement existing context/evidence persistence ports;
- integration tests for history, append/version behavior and restart persistence.

### DEV-0031 — Temporal Durable Flow

- move durable coordination to Temporal;
- activities own side effects;
- resume/ retry / WAITING_HITL / process restart tests;
- no business-rule rewrite inside Temporal.

Milestone:

```text
INITIAL_FLOW_DURABLE = PASS
```

## Stage 9 — Remaining initial process skills

After the SKILL_01–03 flow is operational and durable, continue incrementally:

```text
SKILL_04 — Opportunity formulation/selection
SKILL_05 — Practical/commercial validation
SKILL_06 — Product/service definition
SKILL_07 — Solution/delivery/MVP design
```

Each skill follows the same lifecycle:

```text
contract/context requirements
→ implementation
→ isolated tests
→ negative tests
→ integration with previous flow
→ TESTING
→ validation evidence
→ ACTIVE
```

## Immediate next action

```text
DEV-0019 — SKILL_01 Node Runtime Integration
```

SKILL_01 components are validated, but the complete node is not closed. The next action is to orchestrate the whole node, then stress/improve/close it in DEV-0020 before any SKILL_02 work.
