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

Trasforma un'opportunità validata in un'offerta concreta, costruibile, erogabile, misurabile e vendibile.

Deve definire almeno:

```text
COSA VENDIAMO
A CHI
QUALE PROBLEMA RISOLVIAMO
COSA RICEVE IL CLIENTE
COME VIENE EROGATO
QUANTO COSTA
QUANTO COSTA A NOI
QUANTO MARGINA
QUALI RISORSE SERVONO
COSA È INCLUSO
COSA È ESCLUSO
COME SI TESTA
COME SI MISURA
```

Regola:

```text
una feature entra nel perimetro solo se deriva da:
- problema validato;
- requisito necessario alla delivery;
- vincolo tecnico o normativo.
```

Il resto rimane fuori scope o future feature.

### SKILL_07 — Progettazione Soluzione e Piano Delivery / MVP

Trasforma il prodotto/servizio definito in una soluzione realmente costruibile ed erogabile.

Deve affrontare:

- requisiti;
- MVP;
- architettura;
- componenti;
- make / buy / integrate;
- risorse;
- dipendenze;
- costi;
- tempi;
- milestone;
- test;
- criteri di accettazione;
- rischi;
- fallback;
- rollback;
- piano di rilascio.

Principio:

```text
MVP
=
minimo necessario per erogare
il valore già validato
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
