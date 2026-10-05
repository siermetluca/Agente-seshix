# DEV-0025 RESULT

Status: BLOCK_VALIDATION_ACTIVE

## Implemented

- hardened deterministic validator for unsupported direct negative conclusions;
- local `OllamaCompanyAnalysis` adapter;
- structured-response constraints for grounded SKILL_02 analysis;
- real-provider validation path using local Ollama;
- anti-hallucination tests for neutral PRIMARY_CONTEXT;
- human acceptance harness chaining SKILL_01 semantic intake -> confirmed PRIMARY_CONTEXT -> SKILL_02 analysis;
- no PRIMARY_CONTEXT mutation capability introduced.

## Automated evidence — 2026-10-06

Local Ollama health: PASS.
Observed models include `qwen2.5:3b`.

```text
DEV-0025 targeted + provider tests: 25 / 25 PASS
real Ollama integration:              1 / 1 PASS
full unit regression:               165 / 165 PASS
compileall:                                PASS
```

The real-provider neutral-context test did not permit direct CRITICITA / INEFFICIENZA / GAP / IMPROVEMENT_AREA / RISK conclusions unsupported by explicit negative-signal context.

## Human replay defect + remediation

Owner replay with noisy natural language exposed a real upstream SKILL_01 issue: the semantic model corrected `elttrici` to `elettrici`, causing exact grounding to reject the candidate. The revised behavior separates semantic interpretation from evidence binding:

- noisy spelling/grammar may be semantically interpreted when sufficiently unambiguous;
- accepted FATTO string/list values are rebound to one unique high-confidence exact source span before entering evidence;
- low-confidence or ambiguous rebinding is not accepted and routes to concise clarification;
- deterministic grounding remains fail-closed.

Verification after remediation:

```text
SKILL_01 semantic intake unit:      11 / 11 PASS
real Ollama semantic replay:         2 / 2 PASS
full unit regression:              167 / 167 PASS
compileall + git diff check:              PASS
exact human input preview:               PASS
```

Exact replay now produces grounded source evidence including `elttrici` and reaches the PRIMARY_CONTEXT confirmation gate without executing SKILL_02 automatically.

## Validation rule

Owner architecture decision supersedes the previous full-flow human gate for this task:

```text
VALIDATE_EACH_BLOCK_IN_ISOLATION = REQUIRED
FULL_CHAIN_AS_ACCEPTANCE_GATE = FORBIDDEN
HUMAN_HARNESS = OPTIONAL_DIAGNOSTIC
ASSEMBLY = DEFERRED_TO_CODEX_ASSEMBLER_WITH_DEFINED_CONTEXT
```

DEV-0025 remains open only until the remaining individual blocks in its scope have explicit PASS/FAIL evidence. A later assembler task will compose validated blocks without retroactively changing their individual validation status.
