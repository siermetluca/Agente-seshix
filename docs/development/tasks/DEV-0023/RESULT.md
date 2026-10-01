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
semantic intake unit tests: 7 / 7 PASS
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

## Human-test remediation after owner input `impianti elettrici`

Observed before remediation:

- zero candidates;
- zero mutation;
- no adaptive clarification.

Additional defects found during replay:

- malformed provider classification on re-analysis caused a traceback;
- generic phrase `La mia azienda` was incorrectly proposed as `company.name`;
- model-generated UNKNOWN for unstated fields could trigger unnecessary questions.

Remediation:

- zero-candidate input now produces explicit HITL clarification;
- clarification is iterative (up to 3 rounds in the acceptance harness);
- Ollama response schema constrains classification/value coherence;
- malformed model output retries once and then fails closed without mutation/traceback;
- generic company references cannot become `company.name`;
- UNKNOWN candidates trigger clarification only when the source explicitly marks information unknown/unavailable.

Real replay:

```text
impianti elettrici
→ clarification
→ La mia azienda installa impianti elettrici.
→ company.activities extracted
→ asks company name
→ Siermet SRLS
→ preview: company.name + company.activities
→ approval
→ 2 versioned Evidence-backed context writes
→ PASS
```

Final regression after remediation:

```text
integration: 23 / 23 PASS (+ Ollama opt-in skipped by default)
unit:       139 / 139 PASS
```

SKILL_01_HUMAN_ACCEPTANCE remains PENDING until the owner personally reruns the remediated harness.
