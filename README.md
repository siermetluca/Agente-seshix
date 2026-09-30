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
