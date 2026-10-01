# FOUNDATION FREEZE v0.1

Status: DERIVED_BASELINE_RECORD

## Frozen code baseline

Foundation scope:

```text
DEV-0001
→
DEV-0011
```

Frozen code baseline SHA:

```text
f4306fb53e7b9c3d7d8cc3762c1ad83b6b510948
```

Verified unit baseline:

```text
67 / 67 PASS
```

## What is frozen

The current DOMAIN/APPLICATION foundation is treated as stable input for flow development:

- evidence classification and provenance;
- SourceReference and Evidence;
- versioned PrimaryContext;
- derived state dependency/staleness primitives;
- AuthorityDecision domain outcome;
- Task and TaskContextRequirements;
- context/evidence repository ports;
- evidence-backed targeted PrimaryContext update;
- TaskContextResolver and TaskContextPackage.

## Freeze rule

Foundation code is not reopened during normal flow development.

A change to the frozen foundation requires at least one of:

```text
verified defect
security issue
canonical-context contradiction
new runtime requirement that cannot be satisfied above the foundation
explicit approved Change Proposal
```

New flow behavior should be implemented above the frozen foundation whenever possible.

## Not frozen

The following are intentionally still to be developed:

- authority policy evaluation;
- runtime execution envelope;
- skill registry and skill activation lifecycle;
- executable SKILL_01 / SKILL_02 / SKILL_03;
- LLM/provider boundaries required by semantic skills;
- source/capability acquisition boundaries;
- PostgreSQL adapters;
- Temporal durable workflow;
- executable SKILL_04–07;
- external interfaces.
