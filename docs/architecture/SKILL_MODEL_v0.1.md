# SKILL MODEL v0.1

Status: CANONICAL

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

[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]→ acquisizione e costruzione del contesto

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


[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]