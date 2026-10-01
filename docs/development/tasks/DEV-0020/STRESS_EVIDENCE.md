# DEV-0020 STRESS EVIDENCE

Status: PASS

## Initial stress result

The first closure run intentionally failed:

```text
Ran 11 tests
FAILED
failures = 1
errors = 3
```

Demonstrated defects:

1. authority-HITL resume implicitly approved when no explicit approval context was provided;
2. inactive/missing SKILL_01 escaped as raw SkillNotFound;
3. missing Evidence escaped as raw EvidenceNotFound;
4. duplicate Evidence during node execution escaped as raw EvidenceAlreadyExists.

A further closure review identified that missing required task context was still an untraced pre-run exception.

## Corrections

Only demonstrated defects were corrected:

- authority-HITL resume now requires explicit AuthorityEvaluationContext;
- inactive/missing skill is mapped to FlowRun BLOCKED;
- missing Evidence is mapped to FlowRun BLOCKED;
- duplicate Evidence is mapped to FlowRun BLOCKED without overwrite;
- missing required task context is mapped to a traceable CONTEXT/BLOCKED run using a partial resolved context snapshot.

No SKILL_02, semantic-model, persistence or Temporal behavior was introduced.

## Final stress scenarios

- explicit authority approval required on resume;
- repeated context HITL until valid input arrives;
- duplicate Evidence cannot overwrite prior Evidence;
- IPOTESI remains IPOTESI;
- inactive skill blocks before Evidence/context mutation;
- missing Evidence blocks without context write;
- missing required task context blocks without state mutation;
- optional UNKNOWN completes with no context write;
- repeated fresh runs are deterministic;
- repeated versioned updates preserve history;
- unsupported FATTO replacement is rejected before execution.

## Final verification

Stress suite:

```text
Ran 11 tests
OK
```

All integration tests:

```text
Ran 23 tests
OK
```

Unit regression:

```text
Ran 118 tests
OK
```

## Closure gates

```text
SKILL_01_NODE_COMPLETE = PASS
SKILL_01_NODE_NEGATIVE_SUITE = PASS
SKILL_01_NODE_REPEATABILITY = PASS
SKILL_01_NO_SILENT_STATE_MUTATION = PASS
SKILL_01_HITL_RESUME = PASS
SKILL_01_CLOSED = PASS
```
