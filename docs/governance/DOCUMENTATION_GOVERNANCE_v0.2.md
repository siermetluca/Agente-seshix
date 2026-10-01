# DOCUMENTATION GOVERNANCE v0.2

Status: CANONICAL

Supersedes: DOCUMENTATION_GOVERNANCE_v0.1

## Purpose

Govern canonical project documentation without duplicating sources of truth.

## Document classes

- CANONICAL: normative or architectural source of truth.
- DERIVED: generated or summarized from canonical sources; cannot override them.
- INFORMATIONAL: explanatory material with no normative authority.
- ADR: decision record capturing an architectural or governance decision and rationale.
- OBSOLETE: superseded material retained only when historical traceability is required.

## Ownership

- docs/architecture/: human-readable canonical architecture and operating models.
- docs/governance/: human-readable canonical governance.
- docs/skills/: human-readable canonical skill definitions and process behavior.
- docs/development/: development bootstrap, entry conditions, migration/extraction maps and development documentation.
- docs/development/DEVELOPMENT_STATUS.md: derived operational index of the current development state; it never overrides task artifacts or canonical governance.
- docs/decisions/: ADR records.
- contracts/: structured canonical contracts intended for deterministic consumption or validation.
- README.md: project overview, navigation and current high-level status. It is not the detailed source of truth for contracts.

## Canonicality rules

1. A canonical rule has one authoritative home.
2. README summaries must link to the authoritative document and must not become a second detailed contract.
3. contracts/ may encode a human-readable canonical rule in structured form; conflicts between docs/ and contracts/ are BLOCKING and require reconciliation.
4. DERIVED and INFORMATIONAL documents cannot override CANONICAL documents.
5. UNKNOWN content must not be promoted to canonical fact.

## Versioning

- Material semantic change to a canonical document requires a version change or an explicitly governed in-version correction before release.
- Pure typo/format/link fixes may retain the version when semantics do not change.
- Breaking governance or architecture changes require the applicable CHANGE_PROPOSAL lifecycle.
- Historical versions may be retained when needed for traceability.

## Supersession

When a canonical document is replaced, record:
- status: DEPRECATED or SUPERSEDED;
- superseded_by: replacement identifier/version;
- effective reference or commit when relevant.

The replacement becomes authoritative only after it is committed through repository governance.

## Traceability

Changes to canonical documentation must be attributable to:
- DEV_TASK_ID or CHANGE_PROPOSAL_ID when development/governance scope applies;
- affected canonical documents;
- repository commit/PR.

Documentation-only editorial changes may use DEV_RISK_0 when they do not alter behavior, authority, architecture or requirements.

## README rule

README.md contains:
- project identity and vision;
- core principles in summary form;
- high-level architecture/operating overview;
- documentation navigation;
- repository boundary summary;
- current project status.

Detailed ownership rules, skill contracts, process gates, architecture details and governance must live in their canonical documents.

## ADR rule

An ADR is required when a decision:
- changes or selects a significant architecture mechanism;
- establishes a durable cross-component dependency or boundary;
- replaces a previously accepted architectural choice;
- materially affects compatibility or migration.

An ADR is not required for ordinary implementation choices already constrained by canonical architecture.

## Extraction / duplication rule

Before removing normative material from README or another source:
1. classify it;
2. move/copy it to the canonical target;
3. commit the canonical target;
4. verify traceability;
5. only then remove or summarize the original duplicated material.

## Status transitions

DRAFT -> CANONICAL_CANDIDATE -> CANONICAL -> DEPRECATED -> SUPERSEDED

A document may remain DRAFT/INFORMATIONAL outside this lifecycle when it has no canonical authority.
