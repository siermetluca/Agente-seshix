# Agente-seshix

Agente-seshix è un framework agentico open source progettato per inserirsi nel contesto operativo di un'azienda, costruirne una rappresentazione verificabile a partire da dati reali e supportarne l'evoluzione attraverso analisi, automazione, ricerca di opportunità e coordinamento di competenze specialistiche.

Il progetto separa nettamente il **core open source dell'agente** dai **servizi centrali proprietari Seshix**, in particolare il network di opportunità erogato tramite `seshix.eu`.

---

## Visione

Molte aziende dispongono di dati, competenze, clienti, processi e asset ma non riescono a trasformarli in automazioni, nuovi prodotti, servizi scalabili o nuove opportunità.

Agente-seshix nasce per colmare questo divario.

L'agente deve poter:

- comprendere un'azienda reale senza inventare dati;
- costruire un contesto aziendale verificabile;
- individuare criticità e potenzialità;
- proporre miglioramenti ai processi esistenti;
- ricercare nuovi prodotti, servizi e modelli di ricavo;
- privilegiare soluzioni scalabili, automatizzabili e ricorrenti;
- coordinare competenze tecniche, commerciali, amministrative, marketing, social, logistiche, R&D e altre funzioni necessarie;
- operare con autonomia controllata;
- richiedere intervento umano quando autorità, rischio o policy lo impongono.

Il sistema non parte da un settore predefinito: parte dall'azienda reale.

---

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

## Competenze

Il framework utilizza competenze specialistiche attivate solo quando necessarie.

Esempi:

- sviluppo software;
- infrastruttura;
- cybersecurity;
- R&D;
- prodotto;
- marketing;
- social;
- vendite;
- amministrazione;
- finanza;
- logistica;
- supporto clienti;
- acquisti;
- privacy;
- contratti.

Una competenza dovrebbe dichiarare almeno:

```text
TASK TYPES
REQUIRED CONTEXT
OPTIONAL CONTEXT
POLICY REFERENCES
DECISION RULES
CAPABILITY REQUIREMENTS
AUTHORITY REQUIREMENTS
OUTPUT CONTRACT
STOP CONDITIONS
ESCALATION CONDITIONS
```

Un singolo task può attivare più competenze.

---


## Riferimenti metodologici per le skill

Le skill possono utilizzare riferimenti metodologici esterni quando pertinenti al loro scopo.

Questi riferimenti non costituiscono requisiti universali del framework e non devono essere applicati indiscriminatamente a ogni skill.

Principio:

```text
SCOPO DELLA SKILL
        ↓
riferimenti pertinenti
        ↓
selezione motivata
        ↓
regole / verifiche applicabili
```

L'utilizzo di un riferimento metodologico non implica conformità, certificazione o adozione integrale dello standard da parte di Agente-seshix o dell'azienda analizzata.

Le descrizioni pubbliche degli standard servono esclusivamente a identificarne ambito e pertinenza. Quando una skill deve verificare requisiti specifici di uno standard, deve utilizzare il testo ufficiale applicabile e la relativa edizione vigente.

Riferimenti iniziali:

- **ISO 9001:2026 — Quality management systems — Requirements**: riferimento metodologico per gestione dei processi, responsabilità, controlli, qualità e miglioramento continuo. Fonte ufficiale: [ISO 9001](https://www.iso.org/standard/9001).
- **ISO 31000:2018 — Risk management — Guidelines**: riferimento metodologico per identificazione, analisi, valutazione, trattamento, monitoraggio e comunicazione dei rischi. Fonte ufficiale: [ISO 31000:2018](https://www.iso.org/standard/65694.html).
- **ISO 37301:2021 — Compliance management systems — Requirements with guidance for use**: riferimento metodologico per identificazione e gestione degli obblighi applicabili, conformità e relativo sistema di gestione. Fonte ufficiale: [ISO 37301:2021](https://www.iso.org/standard/75080.html).
- **ISO 15489-1:2016 — Information and documentation — Records management — Part 1: Concepts and principles**: riferimento metodologico per gestione delle registrazioni, metadati, responsabilità, controlli, provenienza e tracciabilità documentale. Fonte ufficiale: [ISO 15489-1:2016](https://www.iso.org/standard/62542.html).
- **ISO 21502:2020 — Project, programme and portfolio management — Guidance on project management**: riferimento metodologico per gestione di obiettivi, attività, risorse, dipendenze, avanzamento e risultati dei progetti. Fonte ufficiale: [ISO 21502:2020](https://www.iso.org/standard/74947.html).
- **Principi contabili nazionali OIC**: riferimento per skill contabili e di analisi economica, secondo applicabilità alla specifica impresa e fattispecie. L'OIC è l'istituto nazionale che emana i principi contabili nazionali per la redazione dei bilanci secondo le disposizioni del codice civile. Fonti ufficiali: [OIC — Presentazione](https://www.fondazioneoic.eu/chi-siamo/presentazione/) e [OIC — Archivio principi contabili](https://www.fondazioneoic.eu/principi-contabili/).

Le versioni e lo stato dei riferimenti devono essere verificati quando una skill li utilizza. Un riferimento in revisione, sostituito o non applicabile non deve essere trattato come requisito corrente senza verifica.

### Contratto concettuale comune delle skill — proposta da validare

**IPOTESI**

Come base comune per lo sviluppo futuro delle skill viene proposta la seguente struttura concettuale:

```text
SCOPO
↓
INPUT
↓
FONTI E PROVENIENZA
↓
REGOLE
↓
COMPORTAMENTO
↓
OUTPUT
↓
VERIFICHE
↓
GESTIONE DEGLI ERRORI
↓
CONDIZIONI DI ARRESTO
↓
INTERVENTO UMANO
↓
TRACCIABILITÀ
```

La proposta non definisce ancora formato tecnico, schema dati, API, database o implementazione runtime.

Per ogni skill futura dovranno essere esplicitati almeno:

1. quali riferimenti metodologici sono pertinenti e perché;
2. quali regole sono verificabili deterministicamente;
3. quali valutazioni richiedono interpretazione semantica o supervisione umana;
4. come vengono trattati dati mancanti, contraddittori o non verificati;
5. quali evidenze consentono di verificare il risultato.

Classificazione del comportamento:

```text
[D-CODICE]
→ regole deterministiche
→ calcoli
→ validazioni
→ soglie approvate
→ autorizzazioni
→ transizioni di stato

[D-LLM]
→ interpretazione semantica vincolata
→ output strutturato
→ risultato verificabile e validato

[LLM]
→ esplorazione
→ generazione di ipotesi
→ sintesi
→ nessuna trasformazione automatica in FATTO o AUTHORITY
```

Rimane obbligatoria la distinzione:

```text
FATTO
→ definito nel contesto verificato o supportato da evidenza

IPOTESI
→ proposta o interpretazione da validare

UNKNOWN
→ informazione non disponibile o non verificata
```

Nessuna skill deve colmare automaticamente un `UNKNOWN`, trasformare una `IPOTESI` in `FATTO` senza evidenza o attribuire `AUTHORITY` sulla base della sola capacità tecnica.

Se un riferimento metodologico entra in conflitto con una decisione già registrata nel contesto o nel framework, il conflitto deve essere esplicitato e sottoposto alla fase o all'autorità competente. Non deve essere risolto sovrascrivendo silenziosamente la decisione esistente.

### Collegamento alle skill di processo già definite

I riferimenti vengono selezionati in funzione dello scopo della skill e non applicati come pacchetto universale.

```text
SKILL_01 — Costruzione Contesto Aziendale
→ priorità metodologica:
  provenienza, registrazioni e tracciabilità
→ riferimento potenzialmente pertinente:
  ISO 15489-1

SKILL_02 — Analisi Aziendale
→ priorità metodologica:
  processi, responsabilità, controlli, errori,
  rischi, obblighi applicabili e dati economici
→ riferimenti potenzialmente pertinenti:
  ISO 9001
  ISO 31000
  ISO 37301
  principi OIC, quando applicabili

SKILL_03 — Analisi Esterna e Validazione di Mercato
→ priorità metodologica:
  fonti, provenienza, rischio, normativa e obblighi
→ riferimenti potenzialmente pertinenti:
  ISO 31000
  ISO 37301
  ISO 15489-1

SKILL_04 — Formulazione e Selezione Opportunità
→ priorità metodologica:
  evidenze, rischio, fattibilità e tracciabilità
→ riferimenti potenzialmente pertinenti:
  ISO 31000
  ISO 15489-1

SKILL_05 — Validazione Pratica / Commerciale
→ priorità metodologica:
  obiettivi del test, attività, risorse, risultati,
  rischi ed evidenze
→ riferimenti potenzialmente pertinenti:
  ISO 21502
  ISO 31000
  ISO 15489-1

SKILL_06 — Definizione Prodotto / Servizio
→ priorità metodologica:
  processi, requisiti, responsabilità,
  rischi, obblighi ed economia dell'offerta
→ riferimenti potenzialmente pertinenti:
  ISO 9001
  ISO 31000
  ISO 37301
  principi OIC, quando applicabili

SKILL_07 — Progettazione Soluzione e Piano Delivery / MVP
→ priorità metodologica:
  obiettivi, attività, risorse, dipendenze,
  rischi, controlli, risultati e tracciabilità
→ riferimenti potenzialmente pertinenti:
  ISO 21502
  ISO 9001
  ISO 31000
  ISO 15489-1
  ISO 37301 quando emergono obblighi applicabili
```

Questa mappatura è metodologica e non stabilisce conformità, certificazione, applicazione integrale degli standard o obblighi universali.

Mantiene inoltre la separazione già prevista dal framework:

```text
SKILL_01
→ acquisizione e costruzione del contesto

SKILL_02
→ analisi interna dell'azienda

SKILL_03
→ ricerca esterna e validazione

SKILL_04+
→ trasformazione delle evidenze validate
  in opportunità, test, offerte e delivery
```

La selezione concreta dei riferimenti, delle regole e delle verifiche rimane parte della definizione e validazione della singola skill.


## Classi di comportamento

Il framework distingue tre classi operative.

### [D-CODICE] — deterministico da codice

Da utilizzare quando la regola è computabile.

Esempi:

- soglie;
- calcoli;
- filtri;
- autorizzazioni;
- state machine;
- validazione schema;
- scoring;
- ordinamento;
- deduplicazione;
- controlli formali.

Esempio:

```text
if costo > limite_autorizzato:
    escalation
```

### [D-LLM] — LLM vincolato

Da utilizzare quando serve comprensione semantica ma l'output deve rispettare tassonomie, schema o alternative predefinite.

Esempi:

- classificazione task;
- estrazione strutturata;
- interpretazione di testo;
- assegnazione categorie;
- valutazioni qualitative vincolate;
- produzione JSON strutturato.

Il risultato deve essere validato dal codice.

### [LLM] — LLM aperto

Da utilizzare quando serve esplorazione o generazione non completamente determinabile.

Esempi:

- generazione di ipotesi;
- esplorazione di alternative;
- ricerca;
- formulazione di query;
- sintesi;
- spiegazione;
- proposta di opportunità.

Principio:

```text
se può essere espresso in codice
→ D-CODICE

se richiede semantica ma può essere vincolato
→ D-LLM

se richiede esplorazione aperta
→ LLM
```

---

## Workflow generale

```text
RICHIESTA
    ↓
NORMALIZZAZIONE INPUT
[D-CODICE]
    ↓
CLASSIFICAZIONE TASK
[D-LLM]
    ↓
VALIDAZIONE CLASSIFICAZIONE
[D-CODICE]
    ↓
RISOLUZIONE COMPETENZE
[D-CODICE]
    ↓
DEFINIZIONE FABBISOGNO CONTESTO
[D-CODICE]
    ↓
RECUPERO CONTESTO
[D-CODICE + D-LLM]
    ↓
VALIDAZIONE CONTESTO
[D-CODICE]
    ↓
CONTEXT PACKAGE
[D-CODICE]
    ↓
PIANIFICAZIONE
[D-LLM / LLM]
    ↓
VALIDAZIONE PIANO
[D-CODICE]
    ↓
ESECUZIONE TOOL
[D-CODICE]
    ↓
RACCOLTA EVIDENZE
[D-CODICE + D-LLM]
    ↓
NORMALIZZAZIONE DATI
[D-CODICE]
    ↓
INTERPRETAZIONE SEMANTICA
[D-LLM]
    ↓
APPLICAZIONE VINCOLI HARD
[D-CODICE]
    ↓
VALUTAZIONE / SCORING
[D-CODICE + D-LLM]
    ↓
MOTORE DECISIONALE
[D-CODICE]
    ↓
CONTROLLO AUTORITÀ
[D-CODICE]
    ↓
AZIONE oppure ESCALATION
[D-CODICE]
    ↓
VERIFICA RISULTATO
[D-CODICE]
    ↓
SPIEGAZIONE
[LLM]
    ↓
VALIDAZIONE FINALE
[D-CODICE]
    ↓
AGGIORNAMENTO STATE
[D-CODICE]
```

---

## Modello digitale dell'azienda

Il primo obiettivo dell'agente è costruire una rappresentazione verificabile dell'azienda.

```text
AZIENDA
├─ identità
├─ visura
├─ ATECO
├─ oggetto sociale
├─ prodotti
├─ servizi
├─ clienti
├─ fornitori
├─ progetti
├─ processi
├─ persone
├─ competenze
├─ software
├─ hardware
├─ asset
├─ costi
├─ ricavi
├─ criticità
└─ opportunità
```

Il modello deve distinguere ciò che l'azienda dichiara formalmente da ciò che emerge dall'operatività reale.

---

## Diagnosi ed evoluzione

L'agente opera su due direttrici parallele.

### Ottimizzazione

- riduzione dei costi;
- eliminazione di attività ripetitive;
- automazione;
- integrazione software;
- miglioramento operativo;
- supporto commerciale;
- miglioramento della delivery.

### Evoluzione

- nuovi prodotti;
- nuovi servizi;
- nuovi mercati;
- nuovi canali;
- nuovi modelli di ricavo;
- asset digitali;
- servizi ricorrenti;
- software;
- licenze;
- marketplace;
- automazioni vendibili.

La domanda non è soltanto:

```text
Come automatizziamo ciò che l'azienda fa già?
```

ma anche:

```text
Cosa può diventare questa azienda utilizzando meglio
asset, competenze, dati, tecnologia e mercato?
```

---

## Opportunity Engine

Agente-seshix gestisce tre categorie principali di opportunità:

```text
OPPORTUNITÀ INTERNA
→ deriva dai dati e dalle capacità della singola azienda

OPPORTUNITÀ DI MERCATO
→ deriva da segnali esterni, domanda, trend, bandi,
  competitor, marketplace e altre fonti

OPPORTUNITÀ DI NETWORK
→ deriva dall'incrocio sicuro tra aziende collegate
```

---

## Isolamento multi-tenant

I tenant devono rimanere isolati.

Dati come:

- email;
- documenti;
- clienti;
- progetti;
- fatture;
- dati operativi;
- contesto completo;
- informazioni riservate;

non devono diventare automaticamente accessibili agli altri tenant.

Principio:

```text
RAW DATA TENANT
        ↓
DERIVAZIONE CONTROLLATA
        ↓
PROFILO OPPORTUNITÀ MINIMIZZATO
        ↓
MATCHING ENGINE
        ↓
MATCH RESULT
```

Il motore di matching non deve utilizzare indiscriminatamente i dati grezzi delle aziende.

---

## Seshix Opportunity Network

Il portale centrale delle opportunità è previsto su:

```text
seshix.eu
```

Il backend del network e il motore centrale di matching rimangono separati dal repository pubblico Agente-seshix.

Il servizio può ricevere esclusivamente profili derivati e minimizzati, secondo policy e consenso.

Esempio:

```json
{
  "offre": [
    "installazione",
    "assistenza tecnica"
  ],
  "cerca": [
    "software SaaS",
    "partnership tecnologiche"
  ],
  "territorio": "IT",
  "partnership_enabled": true
}
```

Il network può individuare complementarità tra aziende senza esporre i rispettivi contesti privati.

La disclosure può essere progressiva:

```text
LIVELLO 0
match anonimo

LIVELLO 1
settore + capacità + territorio

LIVELLO 2
identità aziendale

LIVELLO 3
contatti

LIVELLO 4
documentazione condivisa volontariamente
```

---

## Modello open source + servizi proprietari

### Repository pubblica

`Agente-seshix` contiene il core installabile e utilizzabile autonomamente.

Obiettivo:

```text
OPEN SOURCE AGENT
```

L'utente deve poter utilizzare localmente il framework senza dipendere obbligatoriamente dai servizi Seshix.

### Servizi proprietari

Restano esterni al repository pubblico:

- Opportunity Network;
- motore centrale di matching;
- database del network;
- servizi cloud gestiti;
- billing;
- connettori premium;
- eventuali servizi API premium;
- monitoring e gestione centralizzata;
- componenti commerciali proprietari.

Architettura:

```text
AGENTE OPEN SOURCE
        ↓ opzionale
API SESHIX
        ↓
SERVIZI PROPRIETARI
```

---

## Modalità operative

### Locale

```text
PC / SERVER UTENTE
├─ Agente-seshix
├─ database
├─ modelli locali
├─ API LLM esterne opzionali
└─ interfaccia utente
```

Vantaggi:

- autonomia;
- controllo dei dati;
- possibilità di utilizzare hardware proprio.

Limite:

- il sistema lavora solo quando l'infrastruttura locale è disponibile.

### Cloud

```text
CLOUD / VPS
├─ Agente-seshix
├─ database
├─ scheduler
├─ worker
├─ connettori
├─ API LLM
└─ dashboard
```

Obiettivo:

- funzionamento 24/7;
- nessun PC aziendale obbligatoriamente acceso;
- servizio gestito.

### Ibrida

```text
CLOUD
→ orchestrazione
→ scheduler
→ email
→ automazioni
→ Opportunity Network
→ API LLM

LOCALE
→ file selezionati
→ modelli locali
→ capacità hardware
→ task sensibili o pesanti
```

Quando il nodo locale è offline, il cloud continua le attività che non dipendono da esso.

---

## Interfacce previste

L'interfaccia principale prevista è un'applicazione desktop o web collegata al core dell'agente.

Possibili interfacce:

```text
AGENT_SESHIX CORE
        │
        ├─ Desktop App
        ├─ Web App
        ├─ CLI
        └─ VS Code Extension opzionale
```

L'estensione VS Code non costituisce il prodotto principale: è una capability specialistica per attività tecniche e sviluppo software.

---

## Human in the Loop

Il framework deve distinguere autonomia operativa e autorità.

L'intervento umano può essere richiesto per:

- spese oltre soglia;
- contratti;
- decisioni strategiche;
- azioni irreversibili;
- rischio elevato;
- dati sensibili;
- modifiche critiche;
- operazioni non autorizzate;
- cambiamenti significativi del modello di business.

Il resto può essere automatizzato nei limiti delle policy.

---

## Infrastruttura iniziale di sviluppo

Il progetto viene inizialmente sviluppato localmente e successivamente distribuito su ambienti separati.

### Macchina di sviluppo

```text
Acer Aspire A315-59
Intel Core i7-1255U
32 GB RAM
1 TB SSD
Ubuntu 24.04.5 LTS
```

### VPS sviluppo

```text
OVH VPS-1 2027
2 vCore
4 GB RAM
40 GB storage
```

### VPS produzione

```text
OVH VPS-1 2027
2 vCore
4 GB RAM
40 GB storage
```

I modelli LLM pesanti non sono destinati alle VPS iniziali.

Saranno utilizzati:

```text
modelli locali su hardware adeguato
+
modelli di punta tramite API
```

---

## Primo caso reale di validazione

La prima azienda utilizzata per validare il framework sarà una società italiana reale, già operativa.

Il test iniziale deve verificare almeno:

```text
acquisizione dati
→ costruzione contesto
→ distinzione FATTO / IPOTESI / UNKNOWN
→ diagnosi
→ individuazione criticità
→ individuazione opportunità
→ generazione di possibili evoluzioni
→ selezione delle competenze
→ pianificazione
→ HITL
→ aggiornamento dello stato
```

---


## Repository del progetto

Il progetto è separato in due repository con ruoli diversi.

### 1. `siermetluca/Agente-seshix` — repository pubblica

È la repository pubblica del core open source dell'agente.

Contiene o conterrà:

- framework agentico;
- Gestore del Contesto;
- orchestrazione;
- sistema delle skill;
- runtime;
- connettori open source;
- interfacce e componenti pubblici;
- documentazione tecnica e progettuale;
- client per i servizi Seshix.

Gli utenti possono:

- visionare il codice;
- clonare la repository;
- installare il framework;
- utilizzarlo localmente;
- proporre contributi secondo le regole che saranno definite.

Le modifiche dirette al progetto ufficiale richiedono autorizzazione da parte di Seshix e un ruolo di sviluppatore/collaboratore. Il modello definitivo di governance dei contributi sarà definito successivamente.

### 2. `agent-seshix DEV-PRODUCTION` — repository privata Seshix

Questa repository è prevista come sorgente privata del portale e dei servizi centrali `seshix.eu`.

Il nome GitHub definitivo della repository privata sarà fissato in fase di implementazione; il riferimento funzionale corrente è:

```text
agent-seshix DEV-PRODUCTION
```

Conterrà o conterrà progressivamente:

- portale `seshix.eu`;
- punto di ingresso degli utenti;
- servizi cloud gestiti;
- Opportunity Network;
- social/network delle opportunità;
- matching cross-tenant;
- servizi commerciali proprietari;
- backend e componenti non distribuiti nella repository pubblica;
- ambienti DEV e PRODUCTION;
- eventuali servizi di billing, monitoring e gestione centralizzata.

La repository resta privata.

Gli utenti possono utilizzare i servizi esposti dal portale, ma non acquisiscono automaticamente diritti di modifica del codice sorgente privato.

Le modifiche alla repository privata richiedono autorizzazione esplicita da parte di Seshix come sviluppatori/collaboratori.

Questa governance sarà definita in dettaglio successivamente.

Architettura logica:

```text
REPOSITORY PUBBLICA
siermetluca/Agente-seshix
        │
        │ installazione / utilizzo
        ▼
AGENTE LOCALE / CLOUD / IBRIDO
        │
        │ servizi opzionali
        ▼
API SESHIX
        │
        ▼
REPOSITORY PRIVATA DEV-PRODUCTION
        │
        ▼
seshix.eu
        │
        ├─ accesso utenti
        ├─ Opportunity Network
        ├─ social opportunità
        ├─ matching
        └─ servizi proprietari
```

---

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

Trasforma un prodotto/servizio sufficientemente definito in una soluzione realmente costruibile, erogabile, testabile e controllabile.

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

## Skill di processo, dominio e capacità

Il framework distingue concettualmente:

```text
SKILL DI PROCESSO
→ governa una fase del ciclo

SKILL DI DOMINIO
→ porta conoscenza specialistica

SKILL DI CAPACITÀ
→ utilizza tool, API o azioni specifiche
```

Una skill di processo può coordinare più domini, ma non deve sostituire competenze specialistiche che non possiede.

Esempio:

```text
DELIVERY MVP
↓
orchestrazione
↓
sviluppo software
cloud
cybersecurity
UI/UX
marketing
procurement
elettronica
test
documentazione
...
```

Le competenze effettive saranno definite progressivamente durante sviluppo e test.

---

## Skill Registry ed evoluzione runtime

Il runtime deve poter conoscere quali skill sono disponibili e quali versioni sono attive.

È previsto concettualmente uno:

```text
SKILL REGISTRY
```

con informazioni come:

```text
skill_id
versione
dominio
task supportati
input richiesti
output
capabilities richieste
authority richieste
dipendenze
compatibilità
stato
```

Stati possibili:

```text
DRAFT
TESTING
ACTIVE
DEPRECATED
DISABLED
```

Le nuove skill possono essere introdotte:

```text
1. dallo sviluppatore
2. come proposta generata dal runtime quando emerge un capability/skill gap
```

Il runtime può rilevare:

```text
"non possiedo una competenza sufficiente per questo task"
```

e produrre una richiesta di nuova competenza.

Flusso previsto:

```text
OSSERVAZIONE
→ SKILL GAP
→ PROPOSTA
→ DEFINIZIONE
→ TEST
→ VALIDAZIONE
→ REGISTRAZIONE
→ ACTIVE
```

Il runtime non deve rendere automaticamente operativa una skill appena generata senza validazione.

Principi correnti:

```text
AUTO-DISCOVERY
→ previsto

AUTO-UPDATE DI SKILL APPROVATE
→ previsto, secondo policy

AUTO-CREATION + AUTO-ACTIVATION NON VALIDATA
→ non prevista
```

La runtime deve poter rilevare nuove versioni delle skill approvate e mantenersi aggiornata secondo policy di compatibilità, integrità, dipendenze e breaking changes.

Questi meccanismi non sono ancora chiusi: saranno definiti e validati durante sviluppo e test.

---

## Stato del progetto

Il progetto è attualmente nella fase di definizione dell'architettura e dei contratti concettuali.

Non sono ancora definitive:

- struttura del repository;
- schema database;
- stack finale;
- API interne;
- formato delle competenze;
- contratti del Context Manager;
- protocollo Opportunity Network;
- modello di autorizzazione;
- piani commerciali;
- licenza open source.

Questi elementi saranno definiti prima dell'implementazione produttiva.

---

## Principio progettuale

Agente-seshix non deve delegare a un LLM ciò che può essere espresso in modo affidabile come codice, regola, contratto o macchina a stati.

```text
LLM
→ comprende
→ interpreta
→ esplora
→ propone
→ sintetizza

CODICE
→ valida
→ misura
→ confronta
→ applica regole
→ controlla autorizzazioni
→ esegue
→ verifica
```

L'obiettivo è combinare capacità cognitiva e comportamento controllabile, verificabile e riproducibile.
