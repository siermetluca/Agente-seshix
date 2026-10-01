# DEV-0023 — SKILL_01 Human Re-Acceptance

Status: READY_FOR_HUMAN_REACCEPTANCE

## Run

```bash
cd /home/lucas/Documenti/Agente-seshix
PYTHONPATH=src python3 scripts/skill_01_human_acceptance_v2.py
```

Default local semantic model:

```text
qwen2.5:3b
```

Override if desired:

```bash
AGENTE_SESHIX_SEMANTIC_MODEL=llama3.1:8b PYTHONPATH=src python3 scripts/skill_01_human_acceptance_v2.py
```

## What the human should provide

Only a natural-language company description.

Example:

```text
Siermet SRLS installa impianti elettrici e tecnologici.
Ha 6 dipendenti, 1 titolare e 1 amministrativa.
Opera in Italia.
```

The human must not provide semantic keys, claims, evidence ids or classifications.

## Expected preview

The system should extract only supported candidates from the v1 intake catalog and show them before any write.

The human must be able to reject the preview. Rejection must produce zero Evidence/PRIMARY_CONTEXT mutations.

If the preview is accepted, validated candidates are committed through the existing Evidence + Authority + SKILL_01 node runtime with versioned provenance.

## Acceptance decision

Do not mark PASS automatically.

The owner must explicitly state:

```text
SKILL_01_HUMAN_ACCEPTANCE = PASS
```

or report defects. Any defect keeps SKILL_01 reopened.
