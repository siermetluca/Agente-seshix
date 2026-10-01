# DEV-0022 RESULT

Status: PASS

## Implementation

Added:

- `src/agente_seshix/application/semantic_model.py`
- `tests/unit/test_semantic_model.py`

Implemented:

- immutable `SemanticModelRequest`;
- provider-agnostic `SemanticModelPort` Protocol;
- raw boundary types `RawSemanticCandidate` / `RawSemanticOutput`;
- validated `SemanticCandidate` / `SemanticOutput`;
- deterministic `SemanticOutputValidator`;
- `StructuredSemanticService` that always validates provider output before returning trusted semantic output.

Validation rules include:

- canonical FATTO / IPOTESI / UNKNOWN only;
- FATTO/IPOTESI require a concrete value;
- UNKNOWN forbids a concrete value;
- semantic keys must match canonical dotted-key syntax;
- source URI alone cannot be accepted as claim;
- runtime control tokens cannot be business keys/values;
- arbitrary provider payloads are rejected.

## Test evidence

```text
semantic boundary: 14 / 14 PASS
integration:       23 / 23 PASS
unit regression: 132 / 132 PASS
```

## Gate

```text
MODEL_OUTPUT_WITHOUT_VALIDATION_CANNOT_ENTER_STATE = PASS
```

## Scope

No concrete LLM provider, network/API call, Evidence write or PRIMARY_CONTEXT write was introduced.

DEV-0023 must integrate this boundary into SKILL_01 natural-language intake and repeat human acceptance.
