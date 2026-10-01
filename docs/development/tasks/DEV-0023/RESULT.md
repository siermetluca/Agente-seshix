# DEV-0023 RESULT

Status: WAITING_HUMAN_ACCEPTANCE

## Implemented

- real local Ollama adapter behind SemanticModelPort;
- default acceptance model `qwen2.5:3b`;
- SKILL_01 semantic intake catalog v1;
- read-only semantic preview;
- UNKNOWN -> clarification questions/no write;
- human confirmation before commit;
- validated candidate -> Evidence -> existing SKILL_01 node;
- chained PrimaryContextVersion writes with provenance;
- new human acceptance v2 harness using natural-language input only.

## Automated evidence

```text
semantic intake unit tests: 4 / 4 PASS
real Ollama opt-in test:    1 / 1 PASS
integration regression:     23 / 23 PASS (+ 1 opt-in skipped normally)
unit regression:           136 / 136 PASS
```

Real local smoke results:

- `llama3.1:8b`: correct 6-candidate extraction, ~96 seconds on CPU;
- `qwen2.5:3b`: correct 6-candidate extraction, ~32 seconds cold test and ~16 seconds warm harness run.

## End-to-end dry run

Natural-language description produced:

- company.name = Siermet SRLS;
- company.activities = electrical/technological installation;
- company.employees = 6;
- company.owner_count = 1;
- company.admin_staff = 1;
- company.country = Italy.

After explicit preview approval, six versioned Evidence-backed context updates completed with PASSED node runs.

## Gate

```text
SKILL_01_HUMAN_ACCEPTANCE = PENDING
```

DEV-0023 cannot close until the owner personally reruns the v2 harness and explicitly approves the observed behavior.
