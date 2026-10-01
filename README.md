# Agente-seshix

Agente-seshix è un framework agentico open source progettato per inserirsi nel contesto operativo di un'azienda, costruirne una rappresentazione verificabile a partire da dati reali e supportarne l'evoluzione attraverso analisi, automazione, ricerca di opportunità e coordinamento di competenze specialistiche.

Il progetto separa nettamente il **core open source dell'agente** dai **servizi centrali proprietari Seshix**.

---

## Visione

Agente-seshix parte dall'azienda reale, non da un settore predefinito.

L'agente deve poter:

- comprendere l'azienda senza inventare dati;
- costruire un contesto verificabile;
- individuare criticità, asset e opportunità;
- proporre miglioramenti ed evoluzioni;
- coordinare competenze specialistiche;
- operare con autonomia controllata;
- richiedere intervento umano quando authority, rischio o policy lo impongono.

---

## Principi fondamentali

### Evidenza prima dell'inferenza

```text
FATTO
= supportato da evidenza

IPOTESI
= interpretazione o possibilità da validare

UNKNOWN
= informazione non disponibile o non verificata
```

Un `UNKNOWN` non deve essere colmato automaticamente e un'ipotesi non diventa fatto senza evidenza.

### Capability non significa authority

```text
CAPABILITY != AUTHORITY
```

Essere tecnicamente capaci di eseguire un'azione non significa essere autorizzati a compierla.

### Contesto primario e output derivati

```text
PRIMARY_CONTEXT
!=
DERIVED_OUTPUT
```

Il contesto primario è verificato e versionato; analisi, opportunità, piani e risultati downstream restano output derivati finché non attraversano il lifecycle previsto.

Dettagli: [Context and Ownership](docs/architecture/CONTEXT_AND_OWNERSHIP_v0.1.md).

---

## Architettura in sintesi

Baseline corrente:

```text
PostgreSQL
→ facts / source-of-truth persistence

Temporal
→ durable process

LangGraph
→ bounded reasoning

Authority Engine
→ permission

Skill Contracts
→ behavior
```

Boundary principali del core:

```text
DOMAIN
APPLICATION
WORKFLOW
AGENTIC
INFRASTRUCTURE
INTERFACES
DEVELOPMENT SYSTEM
```

Riferimenti:

- [Architecture Baseline v0.2](docs/architecture/ARCHITECTURE_BASELINE_v0.2.md)
- [Development Architecture v0.1](docs/architecture/DEVELOPMENT_ARCHITECTURE_v0.1.md)
- [Repository Architecture v0.1](docs/architecture/REPOSITORY_ARCHITECTURE_v0.1.md)
- [Operating Model v0.1](docs/architecture/OPERATING_MODEL_v0.1.md)

---

## Skill e comportamento

Le skill sono attivate in funzione del task e del contesto necessario. Una skill dichiara requisiti di contesto, capability, authority, output, stop condition ed escalation.

Le classi di comportamento distinguono:

```text
[D-CODICE]
→ regole deterministiche, validazioni, state machine, authority

[D-LLM]
→ interpretazione semantica vincolata e validata

[LLM]
→ esplorazione, ipotesi e sintesi
```

Riferimenti:

- [Skill Model v0.1](docs/architecture/SKILL_MODEL_v0.1.md)
- [Process Skills v0.1](docs/skills/PROCESS_SKILLS_v0.1.md)
- [Skill Runtime Model v0.1](docs/architecture/SKILL_RUNTIME_MODEL_v0.1.md)

---

## Governance

Lo sviluppo reale è governato da requirement tracciabili, DEV_TASK, CHANGE_PLAN, test, audit, authority e release gate.

```text
CANONICAL CONTEXT
→ REQUIREMENT
→ DEV_TASK
→ CHANGE_PLAN
→ CODE CHANGE
→ TEST
→ RESULT
```

Riferimenti:

- [Development Governance v0.2](docs/governance/DEVELOPMENT_GOVERNANCE_v0.2.md)
- [Repository Governance v0.1](docs/governance/REPOSITORY_GOVERNANCE_v0.1.md)
- [Documentation Governance v0.2](docs/governance/DOCUMENTATION_GOVERNANCE_v0.2.md)
- [Development Execution Contract v0.1](contracts/development/DEVELOPMENT_EXECUTION_CONTRACT_v0.1.yaml)

Il README è una overview e un indice: i contratti dettagliati vivono nei documenti e nei file `contracts/`.

---

## Repository

```text
Agente-seshix/
├── README.md
├── AGENTS.md
├── docs/
├── contracts/
├── src/
│   └── agente_seshix/
│       ├── domain/
│       ├── application/
│       ├── workflow/
│       ├── agentic/
│       ├── infrastructure/
│       ├── interfaces/
│       └── development/
├── tests/
├── schemas/
├── config/
├── scripts/
└── .github/
```

La repository pubblica contiene il core generico.

```text
PRIVATE_MANAGED_REPO
→ may depend on PUBLIC_CORE_REPO

PUBLIC_CORE_REPO
→ must not depend on PRIVATE_MANAGED_REPO
```

L'architettura della repository privata `Agent-web-siermet` sarà definita separatamente e richiederà l'aggiornamento della governance cross-repo.

---

## Documentazione

| Area | Percorso |
|---|---|
| Architettura | [docs/architecture/](docs/architecture/) |
| Governance | [docs/governance/](docs/governance/) |
| Skill di processo | [docs/skills/](docs/skills/) |
| Development | [docs/development/](docs/development/) |
| Decisioni / ADR | [docs/decisions/](docs/decisions/) |
| Contratti strutturati | [contracts/](contracts/) |

La mappa usata per estrarre il precedente README monolitico è conservata in [README Extraction Map v0.1](docs/development/README_EXTRACTION_MAP_v0.1.md).

---

## Stato del progetto

Sono definiti e congelati per lo sviluppo:

- Architecture Baseline v0.2;
- Development Architecture v0.1;
- Repository Architecture v0.1;
- Development Governance v0.2;
- Repository Governance v0.1;
- Documentation Governance v0.2;
- Development Skills v0.1;
- Development Execution Contract v0.1.

Restano da definire progressivamente, quando richiesti dallo sviluppo reale:

- schema database definitivo;
- API interne definitive;
- contratti runtime del Context Manager;
- protocollo Opportunity Network;
- implementazione concreta dell'Authority Engine;
- architettura della repository privata Agent-web-siermet;
- piani commerciali;
- licenza open source.

`FROZEN_FOR_DEVELOPMENT` non significa `FINAL_FOREVER`: le modifiche alle baseline congelate devono attraversare il relativo processo governato di change proposal.

---

## Principio progettuale

Agente-seshix non deve delegare a un LLM ciò che può essere espresso in modo affidabile come codice, regola, contratto o macchina a stati.

L'LLM viene usato dove serve comprensione semantica; authority, validazioni critiche, stato canonico e transizioni governate restano sotto controllo esplicito.
