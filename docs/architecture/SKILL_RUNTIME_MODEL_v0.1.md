# SKILL RUNTIME MODEL v0.1

Status: CANONICAL

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


[executed on device: lucas-Aspire-A315-59 (9ca13855-8d14-42a5-880a-eb86f81c36c0)]