# REPOSITORY GOVERNANCE v0.1

Status: CANONICAL

PUBLIC_CORE_REPO = siermetluca/Agente-seshix
PRIVATE_MANAGED_REPO = siermetluca/Agent-web-siermet

Dependency:
- PRIVATE → PUBLIC: allowed
- PUBLIC → PRIVATE: forbidden

Rules:
- repository not in approved CHANGE_PLAN → write forbidden
- public/private classification UNKNOWN → public write blocked
- unexpected diff → commit blocked
- RELEASE_GATE not ready → merge forbidden
- required HITL missing → merge forbidden

Agent-web-siermet architecture is DEFERRED and will update this governance later.
