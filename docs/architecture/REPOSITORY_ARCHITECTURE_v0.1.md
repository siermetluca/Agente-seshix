# REPOSITORY ARCHITECTURE v0.1

Status: CANONICAL

Top-level:
- README.md
- LICENSE
- pyproject.toml
- .gitignore
- .env.example
- AGENTS.md
- docs/
- contracts/
- src/agente_seshix/
- tests/
- schemas/
- config/
- scripts/
- .github/

Source boundaries under src/agente_seshix:
domain, application, workflow, agentic, infrastructure, interfaces, development.

The public core must not depend on Agent-web-siermet.
