# DEVELOPMENT GOVERNANCE v0.2

Status: CANONICAL

Supersedes: DEVELOPMENT_GOVERNANCE_v0.1

CODE CHANGE must be traceable to an approved requirement.
REQUIREMENT must be traceable to canonical context or an approved change proposal.

Flow:
CANONICAL CONTEXT
→ REQUIREMENT
→ DEV_TASK
→ CHANGE_PLAN
→ CODE CHANGE
→ TEST
→ RESULT

Hard rules:
- NO CONTEXT → NO CHANGE
- NO TRACEABLE REQUIREMENT → NO CHANGE
- SCOPE EXPANSION → STOP
- NEW DEPENDENCY → PLAN REVISION
- TEST NOT EXECUTED != PASS
- CODE CANNOT OVERRIDE CONTEXT
- governance/architecture changes require their own change proposal.

Development status rule:
- every DEV_TASK must keep `docs/development/DEVELOPMENT_STATUS.md` aligned with its current plan and state;
- test execution/result is indexed there but evidence remains in the task artifact;
- a task is not operationally closed until the index reflects its final state and next step.
