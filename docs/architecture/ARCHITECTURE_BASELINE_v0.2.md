# ARCHITECTURE BASELINE v0.2

Status: FROZEN_FOR_DEVELOPMENT

- PostgreSQL owns business/source-of-truth persistence.
- Temporal owns durable process execution.
- LangGraph owns bounded semantic/agentic reasoning only.
- Authority Engine owns permission decisions.
- Skill contracts own behavior.
- One durability owner per execution level.
- Temporal Workflow is deterministic coordination.
- External side effects execute through Temporal Activities.
- LangGraph must not be imported/executed directly inside a Temporal Workflow.
