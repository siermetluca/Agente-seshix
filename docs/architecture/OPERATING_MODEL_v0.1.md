# OPERATING MODEL v0.1

Status: CANONICAL

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


[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]