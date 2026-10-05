# DEV-0025 HUMAN TEST GUIDE

Status: REQUIRED / OWNER HITL

## Purpose

Validate SKILL_02 with a real local Ollama provider using a PRIMARY_CONTEXT produced through the existing SKILL_01 semantic intake path. Activation is forbidden until the owner personally accepts the observed analysis.

## Preconditions

- Ollama reachable at `http://127.0.0.1:11434`.
- `qwen2.5:3b` available, unless another model is explicitly selected.
- Run from the DEV-0025 branch with `PYTHONPATH=src`.

## Run

```bash
cd /home/lucas/Documenti/Agente-seshix
export PYTHONPATH="$PWD/src"
python3 scripts/skill_02_human_acceptance.py
```

## Owner checks

1. Describe a company using only facts you know.
2. Review the SKILL_01 PRIMARY_CONTEXT preview and confirm it only if correct.
3. Review `ANALISI_AZIENDALE_BASELINE`.
4. Reject the test if SKILL_02 invents a problem, capability, risk, gap, or datum not grounded in the displayed PRIMARY_CONTEXT.
5. Accept only if findings/candidates remain grounded and missing information is routed as `CONTEXT_CHANGE_CANDIDATE`.

## Gate

```text
OWNER_ACCEPTANCE = explicit human approval
OWNER_ACCEPTANCE missing -> SKILL_02 activation forbidden
```
