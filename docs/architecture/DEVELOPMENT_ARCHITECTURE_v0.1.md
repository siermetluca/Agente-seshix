# DEVELOPMENT ARCHITECTURE v0.1

Status: CANONICAL

Boundaries:
- DOMAIN
- APPLICATION
- WORKFLOW
- AGENTIC
- INFRASTRUCTURE
- INTERFACES
- DEVELOPMENT SYSTEM

Rules:
- DOMAIN must not depend on infrastructure/framework details.
- WORKFLOW uses Temporal for durable coordination.
- AGENTIC uses LangGraph only for bounded reasoning.
- INTERFACES do not own authority decisions.
- DEVELOPMENT SYSTEM follows governed contracts and traceability.
