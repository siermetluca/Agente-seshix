# CONTEXT AND OWNERSHIP v0.1

Status: CANONICAL

## Principio fondamentale: evidenza prima dell'inferenza

Il framework distingue sempre:

```text
FATTO
= supportato da evidenza

IPOTESI
= interpretazione o possibilità esplicitamente dichiarata

UNKNOWN
= informazione non disponibile o non verificata
```

Un dato aziendale non deve essere inventato per completare il contesto.

Le fonti iniziali possono includere:

- visura camerale;
- codice ATECO;
- oggetto sociale;
- email;
- documenti;
- progetti;
- prodotti;
- servizi;
- clienti;
- fornitori;
- procedure;
- preventivi;
- fatture;
- CRM;
- ERP;
- file aziendali;
- sito web;
- dati operativi.

Se una fonte non esiste o non è disponibile, il relativo campo rimane `UNKNOWN`.

---

## Modello del contesto

Ogni task riceve un contesto specifico composto esclusivamente dalle parti rilevanti.

```text
POLICY
STATE
TASK
DATA / EVIDENCE
CAPABILITIES
AUTHORITY
```

### POLICY

Regole, limiti, obblighi e divieti applicabili.

### STATE

Stato corrente dell'azienda, del sistema e del workflow.

### TASK

Attività concreta da svolgere nel momento corrente.

### DATA / EVIDENCE

Dati ed evidenze utilizzabili per prendere decisioni.

### CAPABILITIES

Strumenti e funzioni tecnicamente disponibili: API, browser, database, modelli, software, connettori e tool.

### AUTHORITY

Azioni e decisioni che l'agente è autorizzato a compiere autonomamente.

```text
CAPABILITY != AUTHORITY
```

Essere tecnicamente capaci di eseguire un'azione non significa essere autorizzati a farlo.

---

## Gestore del Contesto

Il Gestore del Contesto non carica indiscriminatamente tutta la memoria disponibile.

Il principio è:

```text
Gestore del Contesto
=
motore generale del contesto
+
specifiche delle competenze risolte
+
task runtime
```

Workflow:

```text
TASK
  ↓
classificazione
  ↓
risoluzione delle competenze
  ↓
definizione del fabbisogno di contesto
  ↓
recupero delle sole informazioni pertinenti
  ↓
validazione
  ↓
TASK CONTEXT PACKAGE
```

Formalmente:

```text
C_task =
P_rilevante
+ S_rilevante
+ T
+ D_rilevante
+ C_rilevante
+ A_rilevante
```


---

## Context Ownership & Provenance — SKILL_01–07

Il framework distingue il **contesto primario aziendale** dagli **output derivati** prodotti dalle skill successive.

Principio:

```text
PRIMARY_CONTEXT
→ rappresenta lo stato aziendale verificato e versionato
→ può essere scritto / aggiornato solo da SKILL_01

SKILL_02 ... SKILL_07
→ leggono il PRIMARY_CONTEXT
→ producono analisi, evidenze, runtime state,
  opportunità, definizioni e piani derivati
→ NON modificano direttamente il PRIMARY_CONTEXT
```

Un output derivato non diventa automaticamente un fatto aziendale.

```text
DERIVED OUTPUT
!=
PRIMARY_CONTEXT
```

Se una skill downstream rileva un nuovo fatto aziendale, un cambiamento rilevante o un dato primario mancante:

```text
DOWNSTREAM SKILL
↓
CONTEXT_CHANGE_CANDIDATE
↓
SKILL_01 TARGETED UPDATE
↓
verifica della fonte e della provenienza
↓
nuova versione PRIMARY_CONTEXT
↓
ritorno alla skill sospesa
↓
ricalcolo delle sole dipendenze interessate
```

La catena concettuale resta:

```text
SOURCE
↓
EVIDENCE
↓
CONTEXT / DERIVED STATE
↓
ANALYSIS
↓
DECISION
↓
ACTION
```

e non:

```text
LLM OUTPUT
↓
PRIMARY_CONTEXT
```

### Ownership SKILL_01 — Costruzione Contesto Aziendale

**Fonti utilizzabili**

SKILL_01 può utilizzare fonti aziendali dirette, dichiarazioni dell'utente e fonti esterne verificabili quando pertinenti, per esempio:

```text
utente / HITL
visura camerale
ATECO
oggetto sociale
documenti aziendali
email
fatture
preventivi
CRM / ERP
file
sito aziendale
prodotti / servizi
clienti / fornitori
procedure
progetti
dati economici
dati operativi
asset
software / hardware
decisioni
vincoli
policy
fonti pubbliche verificabili pertinenti
```

Ogni informazione rilevante deve mantenere provenienza e stato:

```text
FATTO
IPOTESI
UNKNOWN
PROVENIENZA
VERSIONE
```

**Contesto letto**

```text
fonti grezze
+
versione precedente PRIMARY_CONTEXT
+
CONTEXT_CHANGE_CANDIDATE
+
richieste mirate provenienti dalle skill downstream
```

**Contesto scritto**

SKILL_01 è l'unica skill che può creare o aggiornare:

```text
PRIMARY_CONTEXT
/
COMPANY_CONTEXT_BASELINE
```

che può comprendere, quando disponibili e pertinenti:

```text
identità
struttura aziendale
attività effettive
prodotti / servizi
clienti / fornitori
asset
persone
competenze
software / hardware
economics
risorse
capacità
vincoli
authority
preferenze
decisioni
policy aziendali
obiettivi
limiti
```

SKILL_01 non deve trasformare automaticamente analisi, opportunità, previsioni o ipotesi in fatti aziendali.

### Ownership SKILL_02 — Analisi Aziendale

**Fonti utilizzate**

Fonte primaria:

```text
PRIMARY_CONTEXT validato
```

Può utilizzare fonti esterne solo per:

```text
benchmark
confronto
quantificazione
verifica
```

senza usarle per inventare problemi interni.

**Contesto letto**

```text
COMPANY_CONTEXT_BASELINE
+
evidenze interne pertinenti
+
eventuali fonti esterne di confronto
```

**Output derivato scritto**

```text
ANALISI_AZIENDALE_BASELINE
```

che può contenere:

```text
criticità
inefficienze
asset
capability
gap
aree di miglioramento
rischi
ipotesi da verificare
relazioni causa-effetto ipotizzate
```

SKILL_02 non modifica direttamente il PRIMARY_CONTEXT.

Se manca un dato aziendale necessario:

```text
CONTEXT_CHANGE_CANDIDATE
→ SKILL_01
```

### Ownership SKILL_03 — Analisi Esterna e Validazione di Mercato

**Fonti utilizzate**

SKILL_03 utilizza fonti esterne pertinenti alla domanda da verificare, per esempio:

```text
marketplace
richieste di acquisto
job posting
tender / procurement
forum / community
recensioni
directory
competitor
siti aziendali
pricing pubblico
report
statistiche
associazioni
fonti normative
fonti pubbliche
trend
canali di domanda
```

**Contesto letto**

```text
PRIMARY_CONTEXT
+
ANALISI_AZIENDALE_BASELINE
+
IPOTESI DA VERIFICARE
```

**Output derivato scritto**

```text
ANALISI_ESTERNA_VALIDATA
```

e record di evidenza che, quando pertinenti, dichiarano:

```text
CLAIM
EVIDENCE
SOURCE
RECENCY
GEOGRAPHY
TARGET
CONFIDENCE
CONTRADICTIONS
MISSING_DATA
```

SKILL_03 non trasforma evidenze di mercato in fatti interni dell'azienda.

### Ownership SKILL_04 — Formulazione e Selezione Opportunità

**Fonti utilizzate**

Le fonti principali sono output già validati:

```text
PRIMARY_CONTEXT
+
ANALISI_AZIENDALE_BASELINE
+
ANALISI_ESTERNA_VALIDATA
```

Se l'evidenza è insufficiente, SKILL_04 deve richiedere approfondimento alla skill competente invece di colmare il gap.

**Output derivato scritto**

```text
OPPORTUNITY_CANDIDATE
```

che può includere:

```text
problema
soggetto che soffre il problema
buyer
evidenze
soluzione proposta
fit con l'azienda
gap
rischi
costo e tempo del test
burocrazia
ricavo potenziale
ricorrenza
scalabilità
KPI
success condition
abandon condition
```

Un'opportunità è un oggetto decisionale derivato e non modifica automaticamente il PRIMARY_CONTEXT.

### Ownership SKILL_05 — Validazione Pratica / Commerciale

**Fonti utilizzate**

SKILL_05 combina fonti interne, commerciali e operative.

Fonti interne:

```text
PRIMARY_CONTEXT
opportunity
capabilities
authority
vincoli economici
capacità disponibile
```

Fonti commerciali reali:

```text
buyer
candidature
messaggi
richieste
chiarimenti
sample
task reali
feedback
rejection
acceptance
payment
repeat order
```

Fonti operative:

```text
tempi reali
errori
correzioni
quality control
tool usage
delivery outcomes
```

**Contesto letto**

```text
PRIMARY_CONTEXT
+
OPPORTUNITY
+
TASK_CONTEXT
+
CAPABILITIES
+
AUTHORITY
+
MARKET_VALIDATION_RUNTIME
```

**Output / runtime scritto**

SKILL_05 non modifica direttamente il PRIMARY_CONTEXT.

Scrive principalmente:

```text
MARKET_VALIDATION_RUNTIME
```

che può contenere:

```text
opportunity
buyer
target hypothesis
channel
application
experiment
buyer events
commercial evidence
pricing evidence
sample / task
delivery state
feedback
payment / rejection
outcome
```

Può inoltre produrre:

```text
VALIDATION_EVIDENCE
FLOW_CANDIDATE
SKILL_CANDIDATE
CAPABILITY_GAP
```

Un `SKILL_CANDIDATE` non diventa automaticamente una skill `ACTIVE`.

Se SKILL_05 rileva un dato strutturale aziendale mancante:

```text
CONTEXT_CHANGE_CANDIDATE
→ SKILL_01
```

### Ownership SKILL_06 — Definizione Prodotto / Servizio

**Fonti utilizzate**

SKILL_06 utilizza principalmente:

```text
PRIMARY_CONTEXT
+
OPPORTUNITY sufficientemente validata
+
SKILL_05 VALIDATION_EVIDENCE
+
CAPABILITIES disponibili
+
AUTHORITY
+
VINCOLI ECONOMICI
+
eventuali obblighi già identificati
```

Non deve riaprire autonomamente una ricerca di mercato generale per compensare evidenze mancanti.

**Output derivato scritto**

```text
PRODUCT_SERVICE_DEFINITION
```

che può includere:

```text
target
buyer
problem
job_to_be_done
value_proposition
input_contract
deliverable
output_contract
in_scope
out_of_scope
delivery_model
pricing_model
price_status
cost_model
unit_economics_status
required_capabilities
missing_capabilities
risks
obligations
success_metrics
acceptance_criteria
evidence_refs
unknowns
assumptions
status
```

SKILL_06 può inoltre scrivere la classificazione degli UNKNOWN rilevanti:

```text
UNKNOWN_ID
DESCRIPTION
IMPACT_CLASS
REASON
AFFECTED_PRODUCT_AREA
RESOLUTION_PATH
OWNER_SKILL
MVP_HANDLING
```

SKILL_06 non modifica direttamente il PRIMARY_CONTEXT e non inventa prezzo, margine, capability o promessa commerciale.

### Ownership SKILL_07 — Progettazione Soluzione e Piano Delivery / MVP

**Fonti utilizzate**

SKILL_07 utilizza principalmente:

```text
PRIMARY_CONTEXT
+
PRODUCT_SERVICE_DEFINITION
+
PRODUCT_DEFINITION_GATE
+
MVP_VALIDATION_HYPOTHESES
+
AVAILABLE_CAPABILITIES
+
CAPABILITY_GAPS
+
AUTHORITY
+
POLICY / OBLIGATIONS
+
ECONOMIC / RESOURCE CONSTRAINTS
```

Può utilizzare fonti esterne per valutare componenti della soluzione, per esempio:

```text
tool
API
vendor
software
servizi
specifiche tecniche
pricing
compatibilità
documentazione
```

Queste fonti servono alla progettazione della soluzione e non ridefiniscono automaticamente il mercato o il PRIMARY_CONTEXT.

**Output derivato scritto**

```text
SOLUTION_DELIVERY_PLAN
```

che può includere:

```text
MVP_SCOPE
VALUE_TO_DELIVER
USER / DELIVERY FLOW
FUNCTIONAL_REQUIREMENTS
NON_FUNCTIONAL_REQUIREMENTS
COMPONENTS
CAPABILITIES
MAKE / BUY / INTEGRATE DECISIONS
DEPENDENCIES
RESOURCES
DATA / INPUT REQUIREMENTS
AUTHORITY REQUIREMENTS
RISKS
TEST_PLAN
ACCEPTANCE_CRITERIA
FALLBACK
ROLLBACK
COST_BOUND
TIME_BOUND
MVP_VALIDATION_HYPOTHESES
DELIVERY_PLAN_STATUS
```

Può inoltre produrre:

```text
CAPABILITY_GAP
PRODUCT_CHANGE_CANDIDATE
ESTIMATION_GAP
CRITICAL_DEPENDENCY
```

ma deve inoltrare ciascun problema alla skill o lifecycle competente invece di modificare silenziosamente altri livelli.

### Mappa sintetica di ownership

| Skill | Fonte principale | Scrive PRIMARY_CONTEXT | Output principale |
|---|---|---:|---|
| SKILL_01 | fonti aziendali, utente, fonti verificabili | sì | `COMPANY_CONTEXT_BASELINE` |
| SKILL_02 | PRIMARY_CONTEXT | no | `ANALISI_AZIENDALE_BASELINE` |
| SKILL_03 | contesto + analisi interna + fonti esterne | no | `ANALISI_ESTERNA_VALIDATA` |
| SKILL_04 | contesto + analisi interna + mercato validato | no | `OPPORTUNITY_CANDIDATE` |
| SKILL_05 | opportunità + buyer/task/eventi commerciali e operativi | no | `MARKET_VALIDATION_RUNTIME`, `VALIDATION_EVIDENCE` |
| SKILL_06 | opportunità validata + evidenza commerciale/economica | no | `PRODUCT_SERVICE_DEFINITION` |
| SKILL_07 | product definition + capabilities/resources/constraints | no | `SOLUTION_DELIVERY_PLAN` |

Questa ownership è concettuale: non definisce ancora schema database, storage, API o implementazione runtime.


---


[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]