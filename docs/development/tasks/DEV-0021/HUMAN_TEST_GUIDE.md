# DEV-0021 — SKILL_01 Human Acceptance Test

Status: READY_FOR_HUMAN_TEST

## Run

```bash
cd /home/lucas/Documenti/Agente-seshix
PYTHONPATH=src python3 scripts/skill_01_human_acceptance.py
```

Choose `4` to execute all three scenarios.

## Scenario 1 — FACT

You provide a real context key/value, claim and source reference.

Expected:

```text
CONTEXT → PASSED
SKILL_RESOLUTION → PASSED
AUTHORITY → ALLOW / PASSED
EVIDENCE_INTAKE → PASSED
SKILL_EXECUTION → PASSED
run_state → PASSED
```

The output must show Evidence provenance and the resulting PrimaryContextVersion.

## Scenario 2 — UNKNOWN / HITL / resume

The node starts with required data marked UNKNOWN.

Expected before your input:

```text
SKILL_EXECUTION → WAITING_HITL
run_state → WAITING_HITL
no PrimaryContext write
```

Then provide the missing value, claim and source.

Expected after resume:

```text
SKILL_EXECUTION → PASSED
run_state → PASSED
new Evidence → present
new PrimaryContextVersion → present
```

## Scenario 3 — Authority HITL

The authority policy requires explicit human approval.

Expected before approval:

```text
AUTHORITY → REQUIRES_HITL
run_state → WAITING_HITL
Evidence write → absent
PrimaryContext write → absent
```

Choose `s` only when you personally approve.

Expected after approval:

```text
AUTHORITY → ALLOW
EVIDENCE_INTAKE → PASSED
SKILL_EXECUTION → PASSED
run_state → PASSED
```

## Human acceptance decision

Do not mark PASS automatically.

After running the harness, the human owner must explicitly state whether:

```text
SKILL_01_HUMAN_ACCEPTANCE = PASS
```

or report the observed defect. Any defect reopens SKILL_01 for correction and retest.
