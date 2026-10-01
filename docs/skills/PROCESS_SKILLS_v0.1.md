# PROCESS SKILLS v0.1

Status: CANONICAL

## Prime skill di processo di riferimento

In questa fase le skill seguenti sono **contratti concettuali di processo**, non implementazioni definitive.

Servono a definire come dovrebbe comportarsi l'agente durante sviluppo e test.

### SKILL_01 — Costruzione Contesto Aziendale

Obiettivo:

```text
acquisire fonti disponibili
→ estrarre fatti
→ distinguere FATTO / IPOTESI / UNKNOWN
→ identificare informazioni mancanti rilevanti
→ condurre colloquio adattivo con l'utente
→ registrare configurazioni, vincoli e decisioni
→ costruire COMPANY_CONTEXT_BASELINE
```

Il contesto deve essere:

- verificabile;
- modificabile;
- versionato;
- richiamabile dall'utente;
- privo di dati inventati.

Se un'informazione rilevante manca, l'agente deve poterla chiedere.

Se un'informazione non è rilevante per il task corrente, può rimanere `UNKNOWN`.

L'utente deve poter richiamare e modificare decisioni, configurazioni, preferenze e vincoli.

Le revisioni devono essere versionate, non cancellate silenziosamente.


Una skill downstream non deve modificare silenziosamente il contesto primario. Se durante l'esecuzione emerge un'informazione primaria mancante o una possibile variazione rilevante:

```text
DOWNSTREAM SKILL
↓
CONTEXT_CHANGE_CANDIDATE
↓
SKILL_01 TARGETED UPDATE
↓
validazione e provenienza
↓
nuova versione del contesto
↓
ritorno al punto di esecuzione sospeso
↓
ricalcolo delle sole dipendenze interessate
```

L'aggiornamento deve essere mirato al dato necessario; non richiede la ripetizione indiscriminata dell'intero processo di acquisizione.

### SKILL_02 — Analisi Aziendale

Input principale:

```text
COMPANY_CONTEXT_BASELINE
```

Obiettivo:

- analizzare struttura e funzionamento dell'azienda;
- individuare criticità;
- individuare inefficienze;
- individuare asset;
- individuare capacità;
- individuare gap;
- individuare aree di miglioramento;
- produrre ipotesi da verificare.

La Skill 02 utilizza prima le fonti interne validate e solo successivamente fonti esterne per confronto, quantificazione o verifica.

Regola:

```text
prima comprendere l'azienda
poi confrontarla con l'esterno
mai usare l'esterno per inventare problemi interni
```

### SKILL_03 — Analisi Esterna e Validazione di Mercato

Input:

```text
COMPANY_CONTEXT_BASELINE
+
ANALISI_AZIENDALE_BASELINE
+
IPOTESI DA VERIFICARE
```

Analizza, quando pertinente:

- trend;
- domanda;
- target;
- buyer;
- concorrenza;
- alternative;
- prezzi;
- mercato;
- canali;
- normativa;
- barriere;
- segnali di acquisto.

Ogni risultato dovrebbe dichiarare:

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

Stati possibili:

```text
VALIDATED
PARTIALLY_VALIDATED
INSUFFICIENT_EVIDENCE
CONTRADICTED
INVALID_DATA
CONTEXT_MISMATCH
```

Regola:

```text
NESSUNA EVIDENZA SUFFICIENTE
→ NESSUNA CONCLUSIONE
```

Se emergono dati incoerenti, insufficienti o incompatibili con il contesto, l'agente deve fermare il flusso, identificare la causa e tornare alla fase corretta.

### SKILL_04 — Formulazione e Selezione Opportunità

Input:

```text
COMPANY_CONTEXT_BASELINE
+
ANALISI_AZIENDALE_BASELINE
+
ANALISI_ESTERNA_VALIDATA
```

Trasforma evidenze interne ed esterne in opportunità concrete e testabili.

Un'idea diventa opportunità solo se dispone almeno di:

```text
problema verificato
+
buyer
+
evidenza
+
compatibilità con il contesto
+
test minimo
+
metrica
+
condizione di abbandono
```

Ogni opportunità dovrebbe dichiarare:

- problema;
- soggetto che soffre il problema;
- buyer;
- evidenze;
- soluzione proposta;
- adiacenza con l'azienda;
- gap da colmare;
- costo e tempo del test;
- burocrazia necessaria;
- rischio;
- ricavo potenziale;
- ricorrenza;
- scalabilità;
- KPI;
- condizione di successo;
- condizione di abbandono.

### SKILL_05 — Validazione Pratica / Commerciale

Obiettivo:

```text
verificare con minimo costo e minimo tempo
se un'opportunità già formulata genera:
- interesse reale;
- task reale;
- utilizzo reale;
- pagamento reale;
- condizioni economiche compatibili con il contesto aziendale.
```

SKILL_05 non deve confondere la validazione commerciale con la sola capacità tecnica di eseguire il lavoro.

Principio:

```text
CAN_DO_IT
!=
SHOULD_DO_IT
```

La validazione comprende due rami distinti.

```text
OPERATIONAL VALIDATION
→ possiamo eseguire il task
  in modo stabile, delimitato,
  ripetibile e verificabile?

COMMERCIAL VALIDATION
→ esiste un buyer reale
  che affida, utilizza e paga
  il risultato a condizioni sostenibili?
```

Il ramo operativo può generare evidenza sufficiente per una `SKILL_CANDIDATE`, ma non abilita automaticamente una skill `ACTIVE`.

Una competenza candidata deriva dalla versione più recente del flow pertinente che abbia dimostrato sufficiente:

- stabilità;
- delimitazione;
- ripetibilità;
- verificabilità dell'output;
- gestione osservabile di errori ed eccezioni;
- separazione tra regole, capability e authority.

Un singolo test riuscito non è sufficiente.

#### Validazione commerciale

Il processo concettuale di validazione commerciale è:

```text
DISCOVER
→ QUALIFY
→ MATCH
→ APPLY
→ WAIT
→ CLASSIFY EVENT
→ INTAKE
→ DELIVERY
→ VERIFY
→ PAYMENT / REJECTION
→ EVIDENCE UPDATE
```

Le singole candidature o interazioni con buyer sono istanze indipendenti e possono procedere in parallelo.

Principio:

```text
WAITING_EXTERNAL_EVENT
!=
GLOBAL_STOP
```

Una branch può essere in attesa mentre altre attività autorizzate continuano.

Il runtime commerciale non coincide con il contesto primario aziendale.

```text
PRIMARY_CONTEXT
!=
MARKET_VALIDATION_RUNTIME
```

Il `MARKET_VALIDATION_RUNTIME` è uno stato operativo derivato e dinamico che può contenere, quando pertinenti:

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

Il Context Manager può quindi comporre, secondo il task:

```text
PRIMARY_CONTEXT
+
TASK_CONTEXT
+
MARKET_VALIDATION_RUNTIME
+
EVIDENCE
+
CAPABILITIES
+
AUTHORITY
```

senza riscrivere silenziosamente il contesto primario.

#### Stati ed eventi commerciali

Una sequenza tipica può essere:

```text
READY
→ APPLICATION_SUBMITTED
→ WAITING_RESPONSE
```

Da `WAITING_RESPONSE` possono emergere eventi differenti.

```text
NO_RESPONSE_FINAL
→ NO_EVIDENCE

REJECTION
→ registrare il motivo dichiarato;
→ causa radice UNKNOWN se non osservabile

CLARIFICATION_REQUESTED
→ estrarre le richieste;
→ rispondere solo con dati disponibili;
→ non inventare prezzo, tempo o capability

SAMPLE_RECEIVED
→ intake;
→ scope gate;
→ privacy gate;
→ authority gate;
→ capability match;
→ delivery

[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]
CORRECTION_REQUESTED
→ classificare la causa;
→ modificare solo il livello realmente responsabile

OUTPUT_REJECTED
→ root-cause classification;
→ non invalidare automaticamente flow o opportunità

OUTPUT_ACCEPTED
→ evidenza di accettazione/utilizzo

PAYMENT
→ evidenza commerciale forte

SECOND_ORDER
→ evidenza ulteriore di ricorrenza
```

Regole:

```text
DELIVERY_SENT
!=
DELIVERY_ACCEPTED

CORRECTION_REQUESTED
!=
FLOW_FAILURE

NO_RESPONSE_FINAL
→ NO_EVIDENCE
```

La mancata risposta chiude la finestra osservata della singola candidatura, ma non costituisce automaticamente evidenza negativa sul problema, sul target, sul prezzo o sull'opportunità.

Più risultati comparabili possono essere aggregati per identificare pattern, ma la causa deve rimanere `UNKNOWN` quando non è osservabile.

#### Livelli di evidenza commerciale

Principio:

```text
interesse dichiarato
< task reale / campione
< utilizzo reale
< pagamento reale
< riordino / ricorrenza osservata
```

Gli eventi simulati durante progettazione e test non devono essere confusi con gate commerciali reali.

#### Intake e delivery

Quando un buyer fornisce un task o campione, prima della delivery devono essere verificati:

```text
INTAKE
→ SCOPE
→ PRIVACY
→ AUTHORITY
→ CAPABILITY MATCH
→ FIELD / OUTPUT CONTRACT
→ DELIVERY
→ QUALITY CHECK
```

Se una regola necessaria manca, l'agente deve fermare localmente la delivery e richiedere chiarimento.

Non deve dedurre arbitrariamente valori, regole professionali o significati necessari all'esecuzione.

#### Gestione delle correzioni

Una richiesta di correzione deve essere classificata almeno rispetto al livello responsabile, per esempio:

```text
CONTEXT
CONTRACT
EXECUTION
CAPABILITY
FLOW
TOOL
BUYER_REQUIREMENT_CHANGE
UNKNOWN
```

Deve essere modificato solo il livello smentito dall'evidenza.

Un flow non viene sostituito quando il problema deriva da un'esecuzione errata, da un contratto di output incompleto o da una nuova preferenza del buyer già gestibile dal flow.

#### Capability gap

Quando il task eccede il dominio validato di una capability o skill:

```text
CAPABILITY_GAP
↓
STOP LOCALE
↓
DELIMITAZIONE
↓
CLASSIFICAZIONE
↓
RICERCA DI RIUSO
↓
VALUTAZIONE DELLA NECESSITÀ
↓
eventuale FLOW_CANDIDATE minimo
↓
TEST
↓
STABILITÀ
↓
RIPETIBILITÀ
↓
eventuale SKILL_CANDIDATE
```

Il gap non deve produrre automaticamente una nuova skill né estendere una skill esistente fuori dal proprio dominio validato.

Se il gap non è necessario per un task o un'opportunità sufficientemente validata, può rimanere in backlog.

#### Dati mancanti del contesto primario

Una skill downstream non modifica direttamente il `PRIMARY_CONTEXT`.

Quando SKILL_05 scopre un dato primario mancante che blocca una decisione:

```text
SKILL_05
↓
CONTEXT_CHANGE_CANDIDATE
↓
SKILL_01 TARGETED UPDATE
↓
validazione / provenienza
↓
nuova versione PRIMARY_CONTEXT
↓
ritorno a SKILL_05
↓
ricalcolo delle sole decisioni dipendenti
```

Il questionario o recupero dati deve essere mirato al gap emerso, senza riaprire indiscriminatamente tutto il contesto.

#### Gate economico

La capacità tecnica non abilita automaticamente l'accettazione commerciale.

Prima di accettare un lavoro possono essere necessari:

```text
CAPABILITY_GATE
→ possiamo eseguirlo?

CAPACITY_GATE
→ abbiamo capacità disponibile?

ECONOMIC_GATE
→ è economicamente sostenibile?

AUTHORITY_GATE
→ siamo autorizzati a impegnarci?
```

L'analisi economica deve distinguere almeno:

```text
NOMINAL_PRICE
BILLABLE_TIME
ACTUAL_TOTAL_TIME
VARIABLE_COSTS
EFFECTIVE_CONTRIBUTION
INTERNAL_ECONOMIC_FLOOR
```

Non deve chiamare "margine" il solo fatturato o una tariffa nominale.

Se i dati economici necessari sono insufficienti:

```text
ECONOMIC_GATE
→ INSUFFICIENT_DATA
```

e viene applicato il ritorno mirato a SKILL_01 quando il dato mancante appartiene al contesto primario.

Possibili decisioni del gate, quando supportate dai dati:

```text
ACCEPT
NEGOTIATE
DECLINE
```

Una differenza tra willingness-to-pay del buyer e floor economico interno deve essere classificata come mismatch economico circoscritto, non come invalidazione automatica del problema, del target, del flow o dell'intera opportunità.

#### Automazione e retrofit

L'automazione non deve essere introdotta per principio.

Un bisogno di automazione può emergere da evidenza operativa o economica, per esempio quando:

```text
delivery manuale
→ overhead elevato
→ economics insufficienti
```

In tal caso può essere proposta e successivamente testata una capability assistita, privilegiando quando possibile:

```text
tool esistente
+
adapter / retrofit
+
contratto Agent-seshix
+
HITL dove necessario
```

prima di costruire automaticamente nuovo software custom.

Gli strumenti integrati dovrebbero poter fornire, quando applicabile:

```text
INPUT CONTRACT
OUTPUT CONTRACT
EVIDENCE
ERROR STATE
AUTHORITY REQUIREMENT
AUDIT TRACE
```

La scelta concreta di tool, adapter, API e implementazione rimane da validare nelle fasi successive.

#### Esiti di SKILL_05

Possibili esiti:

```text
VALIDATED
PARTIALLY_VALIDATED
INVALIDATED
INSUFFICIENT_EVIDENCE
CONTEXT_MISMATCH
MARKET_MISMATCH
OPPORTUNITY_MISMATCH
```

Se `INVALIDATED`, l'agente deve classificare la causa e correggere solo la parte smentita.

Esempi:

```text
INVALID_PROBLEM
INVALID_TARGET
INVALID_VALUE_PROPOSITION
INVALID_PRICE
INVALID_CHANNEL
INVALID_DELIVERY
INVALID_ECONOMICS
INVALID_CONTEXT
INVALID_CAPABILITY
```

Solo una validazione sufficientemente forte abilita la fase successiva.

#### Stato concettuale corrente di SKILL_05

La definizione comportamentale è considerata sufficientemente completa per la fase corrente:

```text
BEHAVIORAL DEFINITION
→ COMPLETE_FOR_CURRENT_PHASE

CONCEPTUAL FLOW
→ DEFINED

STATE MODEL
→ DEFINED

STOP / RETURN CONDITIONS
→ DEFINED

CONTEXT INTERACTION
→ DEFINED

CAPABILITY GAP HANDLING
→ DEFINED

COMMERCIAL EVIDENCE HANDLING
→ DEFINED

ECONOMIC GATE
→ DEFINED CONCEPTUALLY

PARALLEL EXECUTION
→ DEFINED

REAL VALIDATION
→ PENDING

IMPLEMENTATION
→ NOT STARTED

FINAL ARCHITECTURE
→ NOT CLOSED
```

I test reali e i benchmark operativi devono essere ripresi solo quando il contesto necessario è sufficientemente definito e versionato.

### SKILL_06 — Definizione Prodotto / Servizio

Trasforma un'opportunità sufficientemente validata in un'offerta concreta, costruibile, erogabile, misurabile e vendibile.

SKILL_06 non deve compensare evidenze commerciali mancanti inventando prodotto, prezzo, capability o promesse. Deve definire il core dell'offerta e rendere espliciti gli elementi ancora da validare.

Input concettuali:

```text
PRIMARY_CONTEXT
+
OPPORTUNITY VALIDATA / SUFFICIENTLY VALIDATED
+
SKILL_05 VALIDATION EVIDENCE
+
CAPABILITIES DISPONIBILI
+
AUTHORITY
+
VINCOLI ECONOMICI
```

Deve definire almeno:

```text
COSA VENDIAMO
A CHI
QUALE PROBLEMA RISOLVIAMO
COSA RICEVE IL CLIENTE
INPUT CONTRACT
OUTPUT CONTRACT
CRITERI DI ACCETTAZIONE
COME VIENE EROGATO
MODELLO DI PREZZO
STRUTTURA DEI COSTI
UNIT ECONOMICS
QUALI RISORSE SERVONO
CAPABILITY NECESSARIE
COSA È INCLUSO
COSA È ESCLUSO
RISCHI / OBBLIGHI
COME SI TESTA
COME SI MISURA
```

Il flusso concettuale è:

```text
VALIDATED OPPORTUNITY
↓
VALIDATE INPUT EVIDENCE
↓
DEFINE TARGET / BUYER
↓
DEFINE PROBLEM / JOB
↓
DEFINE VALUE PROPOSITION
↓
DEFINE DELIVERABLE
↓
DEFINE INPUT / OUTPUT CONTRACT
↓
DEFINE SCOPE
↓
DEFINE DELIVERY MODEL
↓
DEFINE PRICING MODEL
↓
DEFINE COST MODEL / UNIT ECONOMICS
↓
DEFINE CAPABILITIES / RESOURCES
↓
DEFINE RISKS / OBLIGATIONS
↓
DEFINE SUCCESS METRICS
↓
CLASSIFY UNKNOWN
↓
PRODUCT_DEFINITION_GATE
```

Regola sulle feature:

```text
una feature entra nel perimetro solo se deriva da:
- problema validato;
- requisito necessario alla delivery;
- vincolo tecnico o normativo.
```

Il resto rimane fuori scope, opzionale o future feature.

### Gestione degli UNKNOWN in SKILL_06

SKILL_06 non deve eliminare artificialmente tutti gli `UNKNOWN`.

Deve invece classificarli in base all'impatto che hanno sul passaggio a SKILL_07.

```text
UNKNOWN
↓
IMPACT CLASSIFICATION
↓
BLOCKING
CONDITIONALLY_BLOCKING
NON_BLOCKING
```

#### BLOCKING

Un `UNKNOWN` è bloccante quando impedisce di definire o verificare in modo sufficientemente sicuro almeno uno degli elementi essenziali del prodotto/servizio, per esempio:

```text
core deliverable
criteri di accettazione
scope essenziale
authority
obblighi / compliance critici
privacy / sicurezza critica
capability necessaria
fattibilità economica minima
```

Comportamento:

```text
BLOCKING UNKNOWN
→ deve essere risolto prima di SKILL_07
→ ritorno alla skill o fonte competente
```

#### CONDITIONALLY_BLOCKING

Un `UNKNOWN` è condizionatamente bloccante quando può essere neutralizzato restringendo esplicitamente il perimetro del prodotto o dell'MVP, introducendo una fallback rule o escludendo il caso non validato.

Esempio concettuale:

```text
capability narrativa non validata
↓
prodotto ampio
→ BLOCKING

MVP ristretto a documenti strutturati/tabellari
→ gap escluso dallo scope
→ non blocca SKILL_07
```

Comportamento:

```text
CONDITIONALLY_BLOCKING
→ restringere scope / definire fallback / escludere caso
→ registrare esplicitamente la limitazione
```

#### NON_BLOCKING

Un `UNKNOWN` è non bloccante quando:

```text
- non impedisce la definizione del core value;
- non compromette sicurezza, authority o compliance;
- non impedisce una delivery verificabile;
- può essere testato durante l'MVP;
- dispone di una condizione di verifica esplicita.
```

Esempi possibili:

```text
prezzo esatto
miglior verticale
nome commerciale
branding
canale migliore
feature opzionali
automazione futura
alcune soglie di performance non critiche
```

Comportamento:

```text
NON_BLOCKING UNKNOWN
→ MVP_VALIDATION_HYPOTHESIS
→ passa a SKILL_07 con evidenza e criterio di verifica
```

### Schema concettuale degli UNKNOWN

Ogni `UNKNOWN` rilevante per SKILL_06 dovrebbe dichiarare almeno:

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

Questo schema è concettuale e non definisce ancora formato tecnico, database o API.

### PRODUCT_DEFINITION_GATE

Il gate finale di SKILL_06 può produrre tre stati:

```text
PASS
PARTIAL_PASS
BLOCKED
```

#### PASS

```text
→ nessun BLOCKING UNKNOWN irrisolto
→ prodotto sufficientemente definito
→ SKILL_07 consentita
```

#### PARTIAL_PASS

```text
→ core sufficientemente definito
→ nessun BLOCKING UNKNOWN irrisolto
→ CONDITIONALLY_BLOCKING neutralizzati tramite scope/fallback
→ NON_BLOCKING tracciati come MVP_VALIDATION_HYPOTHESIS
→ SKILL_07 consentita
```

Principio:

```text
PARTIAL_PASS
!=
prodotto incompleto in modo incontrollato
```

Può significare:

```text
core sufficientemente definito
+
ipotesi non bloccanti lasciate intenzionalmente
alla validazione MVP
```

#### BLOCKED

```text
→ almeno un BLOCKING UNKNOWN irrisolto
→ SKILL_07 non consentita
→ ritorno alla skill competente
```

Regola centrale:

```text
MVP
!=
luogo dove nascondere UNKNOWN critici

MVP
=
luogo dove testare ipotesi non bloccanti
su un core già sufficientemente definito
```

Routing concettuale dei gap:

```text
missing company constraint
→ SKILL_01

internal capability / economic uncertainty
→ SKILL_01 o SKILL_02 secondo la fonte del dato

market / buyer / price uncertainty
→ SKILL_03 o SKILL_05 secondo il tipo di evidenza richiesta

opportunity no longer coherent
→ SKILL_04

commercial evidence insufficient
→ SKILL_05

capability gap
→ capability / skill-gap lifecycle

technical implementation question
→ SKILL_07
```

Stato concettuale corrente:

```text
SKILL_06

BEHAVIORAL DEFINITION
→ COMPLETE_FOR_CURRENT_PHASE

UNKNOWN CLASSIFICATION
→ DEFINED

PRODUCT_DEFINITION_GATE
→ DEFINED

SKILL_07 TRANSITION RULE
→ DEFINED

REAL VALIDATION
→ PENDING

IMPLEMENTATION
→ NOT STARTED

FINAL ARCHITECTURE
→ NOT CLOSED
```

### SKILL_07 — Progettazione Soluzione e Piano Delivery / MVP


[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]Trasforma un prodotto/servizio sufficientemente definito in una soluzione realmente costruibile, erogabile, testabile e controllabile.

SKILL_07 non deve ridefinire problema, buyer, valore o perimetro commerciale già fissati da SKILL_06. Se durante la progettazione emerge la necessità di ampliare o modificare il prodotto, deve generare un `PRODUCT_CHANGE_CANDIDATE` e tornare alla skill competente.

Input concettuali:

```text
PRIMARY_CONTEXT
+
PRODUCT_SERVICE_DEFINITION
+
PRODUCT_DEFINITION_GATE RESULT
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

Regole di ingresso:

```text
SKILL_06 = BLOCKED
→ SKILL_07 non parte

SKILL_06 = PASS
→ SKILL_07 può partire

SKILL_06 = PARTIAL_PASS
→ SKILL_07 può partire solo se:
  - nessun BLOCKING UNKNOWN resta irrisolto;
  - i CONDITIONALLY_BLOCKING sono stati neutralizzati;
  - i NON_BLOCKING sono tracciati come MVP_VALIDATION_HYPOTHESES.
```

Output concettuale principale:

```text
SOLUTION_DELIVERY_PLAN
```

che dovrebbe includere almeno:

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

Il flusso concettuale è:

```text
VALIDATE INPUT
↓
FREEZE VALUE TO DELIVER
↓
DEFINE MVP SCOPE
↓
DEFINE END-TO-END FLOW
↓
DERIVE REQUIREMENTS
↓
MAP CAPABILITIES
↓
IDENTIFY CAPABILITY GAPS
↓
MAKE / BUY / INTEGRATE ANALYSIS
↓
DEFINE SOLUTION COMPONENTS
↓
MAP DEPENDENCIES
↓
RESOURCE / CAPACITY CHECK
↓
COST / TIME BOUNDS
↓
RISK / OBLIGATION CHECK
↓
DEFINE TEST PLAN
↓
DEFINE ACCEPTANCE CRITERIA
↓
DEFINE FALLBACK / ROLLBACK
↓
CLASSIFY REMAINING UNKNOWN
↓
DELIVERY_PLAN_GATE
```

### Freeze del valore

SKILL_07 non deve ampliare automaticamente il prodotto.

```text
TARGET
PROBLEM
DELIVERABLE
CORE VALUE
SCOPE
```

rimangono congelati rispetto all'output di SKILL_06, salvo ritorno esplicito alla skill competente.

Se durante la progettazione emerge:

```text
"per funzionare dobbiamo vendere anche X"
```

comportamento:

```text
PRODUCT_CHANGE_CANDIDATE
→ ritorno SKILL_06
```

### MVP scope

Principio:

```text
MVP
=
minimo necessario per erogare
il valore già validato
+
minimo necessario per testare
le MVP_VALIDATION_HYPOTHESES
```

Una capability, feature o componente entra nell'MVP solo se è:

```text
CORE_VALUE_REQUIRED
oppure
VALIDATION_REQUIRED
oppure
DELIVERY_REQUIRED
oppure
COMPLIANCE_REQUIRED
```

Il resto rimane `OUT_OF_MVP`.

Principio:

```text
MVP
!=
software obbligatorio
```

L'MVP può essere:

```text
MANUAL
ASSISTED
AUTOMATED
HYBRID
```

La forma dipende da evidenze, economics, capability, rischio e vincoli.

### User / Delivery Flow

SKILL_07 deve descrivere il percorso end-to-end del valore, per esempio:

```text
REQUEST
↓
INTAKE
↓
VALIDATION
↓
PROCESSING
↓
QUALITY CONTROL
↓
DELIVERY
↓
ACCEPTANCE
↓
OUTCOME
```

Il flow deve essere verificabile anche quando la delivery non è software.

### Requirements

SKILL_07 distingue:

```text
FUNCTIONAL_REQUIREMENTS
→ cosa deve fare la soluzione

NON_FUNCTIONAL_REQUIREMENTS
→ qualità, privacy, sicurezza, tracciabilità,
  performance, disponibilità, recoverability,
  usability e altri requisiti pertinenti
```

Non devono essere introdotti SLA o soglie arbitrarie prive di fonte, contesto o requisito.

### Capability mapping

Ogni step del delivery flow deve essere mappato sulle capability necessarie.

```text
CAPABILITY_REQUIRED
↓
AVAILABLE
PARTIAL
MISSING
```

Se emerge una capability mancante:

```text
CAPABILITY_GAP
→ applicare il capability / skill-gap lifecycle
```

Una capability in stato `TESTING` può essere utilizzata in un MVP controllato solo entro i limiti validati e con supervisione/authority adeguate.

### Capability e componenti

Principio:

```text
CAPABILITY
!=
COMPONENT
```

```text
CAPABILITY
→ ciò che il sistema sa fare

COMPONENT
→ ciò che materialmente realizza
  o supporta quella capability
```

La stessa capability può essere erogata da componenti differenti.

### Make / Buy / Integrate / Reuse / Manual

Per ogni capability o componente necessario, SKILL_07 può valutare:

```text
BUILD
BUY
INTEGRATE
REUSE
MANUAL
```

La valutazione considera almeno, quando pertinenti:

```text
time
cost
risk
quality
vendor dependency
data / privacy
available capability
maintenance burden
```

Principio corrente:

```text
REUSE / INTEGRATE
prima di
BUILD
```

quando strumenti o componenti esistenti soddisfano requisiti, policy e vincoli.

SKILL_07 non deve costruire automaticamente software custom solo perché tecnicamente possibile.

### Dependencies

Ogni dipendenza critica dovrebbe dichiarare almeno:

```text
DEPENDENCY
REQUIRED_FOR
INTERNAL / EXTERNAL
BLOCKING?
FALLBACK_AVAILABLE?
```

Una dipendenza senza fallback che blocca il valore deve essere trattata come `CRITICAL_DEPENDENCY`.

### Resources e capacity

SKILL_07 verifica almeno:

```text
PEOPLE
TIME
TOOLS
INFRASTRUCTURE
BUDGET
CAPACITY
```

Stati possibili:

```text
AVAILABLE
INSUFFICIENT
UNKNOWN
```

Una risorsa essenziale `INSUFFICIENT` può bloccare il piano oppure richiedere scope reduction, sourcing o ritorno alla skill competente.

### Cost / Time Bounds

SKILL_07 non deve produrre precisione fittizia.

Quando i dati non permettono una stima puntuale può distinguere:

```text
KNOWN
BOUND
UNKNOWN
```

Se il dato necessario non è disponibile:

```text
ESTIMATION_GAP
```

[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]
Le stime devono rimanere compatibili con vincoli di budget, capacità e authority.

### Test plan

Ogni elemento critico del piano dovrebbe poter dichiarare:

```text
WHAT_TO_TEST
INPUT
EXPECTED_OUTPUT
PASS_CONDITION
FAIL_CONDITION
EVIDENCE_TO_CAPTURE
```

I test possono includere, quando pertinenti:

```text
TECHNICAL TEST
OPERATIONAL TEST
MVP VALIDATION TEST
```

SKILL_07 non sostituisce SKILL_05 nella validazione commerciale, ma deve rendere il piano di delivery misurabile e capace di produrre le evidenze richieste.

### Acceptance criteria

I criteri di accettazione derivano dalla definizione di prodotto di SKILL_06.

SKILL_07 può tradurli in condizioni verificabili, ma non modificarne arbitrariamente il significato.

```text
PRODUCT ACCEPTANCE CRITERIA
↓
IMPLEMENTABLE TEST CONDITIONS
```

Se non è possibile tradurre un criterio essenziale in una verifica:

```text
ACCEPTANCE_NOT_TESTABLE
→ ritorno SKILL_06
```

### Fallback e rollback

Principio:

```text
FALLBACK
→ come continuiamo a erogare valore
  se il percorso principale fallisce

ROLLBACK
→ come torniamo a uno stato precedente sicuro
```

Fallback e rollback devono essere proporzionati al rischio, compatibili con authority ed economics e non devono introdurre scope non validato.

### Remaining UNKNOWN

SKILL_07 eredita gli `MVP_VALIDATION_HYPOTHESES` da SKILL_06 e può individuare nuovi UNKNOWN relativi a costruibilità e delivery.

La classificazione resta:

```text
BLOCKING
CONDITIONALLY_BLOCKING
NON_BLOCKING
```

ma il criterio specifico di SKILL_07 è:

```text
possiamo costruire, erogare e testare
la soluzione in modo sicuro e verificabile?
```

Un `BLOCKING UNKNOWN` irrisolto impedisce il passaggio oltre il `DELIVERY_PLAN_GATE`.

### DELIVERY_PLAN_GATE

Il gate finale di SKILL_07 può produrre:

```text
PASS
PARTIAL_PASS
BLOCKED
```

#### PASS

```text
→ MVP scope definito
→ flow definito
→ requirements testabili
→ capability sufficienti
→ risorse sufficienti
→ rischi critici controllati
→ test plan definito
→ acceptance criteria eseguibili
→ fallback / rollback adeguati
→ nessun BLOCKING UNKNOWN
```

#### PARTIAL_PASS

```text
→ core delivery plan eseguibile
→ nessun BLOCKING UNKNOWN irrisolto
→ remaining unknowns non bloccanti
→ validation plan esplicito
→ implementazione / test controllato consentito
```

#### BLOCKED

```text
→ capability critica mancante
oppure
→ risorse insufficienti
oppure
→ dipendenza critica irrisolta
oppure
→ problema di rischio / authority
oppure
→ acceptance non verificabile
oppure
→ BLOCKING UNKNOWN irrisolto
```

Routing concettuale:

```text
product definition issue
→ SKILL_06

market / commercial evidence issue
→ SKILL_05

opportunity issue
→ SKILL_04

context issue
→ SKILL_01

capability gap
→ capability / skill-gap lifecycle

implementation issue inside valid design
→ specialist technical skill
```

### Esito del test concettuale su OPP-01

Nel test di progettazione corrente, restringendo l'MVP a:

```text
documenti strutturati / tabellari
+
dati non sensibili
+
controlled human-supervised service
```

SKILL_07 ha prodotto concettualmente:

```text
SOLUTION_DELIVERY_PLAN_v1

CUSTOM SOFTWARE REQUIRED
→ NO

CORE FLOW
→ DEFINED

CORE CAPABILITY
→ Structured Record Extraction / TESTING

TOOLS
→ REUSE EXISTING TOOLS initially

HITL
→ REQUIRED

TEST PLAN
→ DEFINED

ACCEPTANCE
→ DEFINED

FALLBACK
→ DEFINED

ROLLBACK
→ DEFINED

MVP VALIDATION HYPOTHESES
→ TRACKED

DELIVERY_PLAN_GATE
→ PARTIAL_PASS_ELIGIBLE_FOR_CONTROLLED_MVP
```

Questo risultato è relativo alla simulazione e non costituisce validazione reale dell'MVP.

Stato concettuale corrente:

```text
SKILL_07

BEHAVIORAL DEFINITION
→ COMPLETE_FOR_CURRENT_PHASE

INPUT / OUTPUT
→ DEFINED

MVP SCOPE RULE
→ DEFINED

FLOW
→ DEFINED

REQUIREMENTS MODEL
→ DEFINED

CAPABILITY MAPPING
→ DEFINED

MAKE / BUY / INTEGRATE
→ DEFINED CONCEPTUALLY

DEPENDENCIES
→ DEFINED

RESOURCE CHECK
→ DEFINED

TEST / ACCEPTANCE
→ DEFINED

FALLBACK / ROLLBACK
→ DEFINED

DELIVERY_PLAN_GATE
→ DEFINED

REAL MVP EXECUTION
→ PENDING

IMPLEMENTATION
→ NOT STARTED

FINAL ARCHITECTURE
→ NOT CLOSED
```

Dopo `DELIVERY_PLAN_READY` non viene ancora fissata una singola skill universale di esecuzione.

Da questo punto il framework può richiedere la composizione di più competenze specialistiche.

---


[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]