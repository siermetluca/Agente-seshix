# DEVELOPMENT GOVERNANCE v0.1

Status: CANONICAL

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
