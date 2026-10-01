# Agente-seshix repository rules

- Canonical governance lives under docs/ and contracts/.
- Real development requires an approved DEV_TASK and CHANGE_PLAN.
- Every development task must keep docs/development/DEVELOPMENT_STATUS.md aligned as the operational index of plan, step, test/result status, blockers and next action.
- Direct writes to main are forbidden by policy.
- Work must occur on a task branch.
- Repository scope may not expand silently.
- Tests not executed are never PASS.
- Failed critical gates cannot be compensated by scores.
- Public/private classification UNKNOWN blocks public publication.
- Secrets, credentials, private customer/tenant data and proprietary managed-service details must not enter the public core.
- Merge/release eligibility does not grant merge/release authority.
- Architecture or governance changes require their own governed change proposal.
- Agent-web-siermet architecture is deferred; Agente-seshix must not depend on it.
