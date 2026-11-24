# SPECIFICATIONS.md — Sistema Tasks_app (v2.0)

## 1. Visió General
Tasks_app és una eina CLI lleugera per ajudar als estudiants a gestionar les seves tasques acadèmiques diàries.

La versió 2.0 afegeix la data límit, la modificació i la finalització de tasques i la identificació de tasques urgents i caducades, mantenint la compatibilitat amb les dades generades al sprint 1.

## 2. User Stories (Històries d'Usuari)
- US-01: Com a estudiant, vull afegir una tasca amb títol i assignatura per tal de recordar els meus deures.
- US-02: Com a estudiant, vull veure la llista de tasques pendents per tal d'organitzar el meu temps.
- US-03: Com a estudiant, vull assignar una data límit a una tasca per tal de planificar el meu temps d'estudi.
- US-04: Com a estudiant, vull modificar el títol, l'assignatura, la data límit i l'estat d'una tasca per tal de corregir-la sense perdre'n l'identificador.
- US-05: Com a estudiant, vull marcar una tasca com a completada per tal de seguir el progrés dels meus deures.
- US-06: Com a estudiant, vull veure les etiquetes `[CADUCADA]` i `[URGENT]` per tal de prioritzar les tasques que requereixen atenció immediata.
- US-07: Com a estudiant, vull rebre missatges d'error clars per tal de corregir les dades invàlides sense perdre les tasques desades.
- US-08: Com a estudiant, vull disposar d'una data de referència controlada per tal de comprovar les etiquetes de manera reproducible.

## 3. Model de Dades (Mermaid)
```mermaid
classDiagram
    class Tasca {
        +int id
        +string títol
        +string assignatura
        +string estat
        +string data_límit
    }
```

`data_límit` és un camp opcional que s'emmagatzema amb format `YYYY-MM-DD`. Les tasques del sprint 1 que no contenen aquest camp s'interpreten com a tasques sense data límit (RF-08 i RF-09). L'estat pren els valors `pendent` o `completada`.

## 4. Requisits
Els requisits RF-01 a RF-04 del sprint 1 es conserven sense canvis.
- RF-01 : El sistema tasks_app ha de guardar les tasques en un fitxer JSON de persistència local.
- RF-02 : Si el fitxer `data/tasks.json` no existeix, el sistema tasks_app ha de crear `data/tasks.json`  inicialitzat amb una llista JSON buida ([])
- RF-03 : El sistema tasks_app ha de proveir a l'estudiant la capacitat de crear una nova tasca amb estat 'pendent' mitjançant el comandament add --title <títol> --subject <assignatura>.
- RF-04: El sistema tasks_app ha de proveir a l’estudiant la capacitat de visualitzar totes les tasques registrades (incloent-hi el seu ID, títol, assignatura i estat) mitjançant el comandament list.

## 5. Criteris d’acceptació i proves (Gherkin scenarios)
Els escenaris GS-01 a GS-03 del sprint 1 es conserven sense canvis.
- GS-01: Creació correcta d'una tasca
  Atès que la base de dades JSON no conté encara tasques
  quan l’estudiant executa `python src/tasks_app.py add --title 'Pràctica 1' --subject 'RS'
  aleshores el sistema confirma `Tasca [ID: 1] creada amb èxit`
  i la tasca queda registrada al fitxer `data/tasks.json`.

- GS-02: Llistat de tasques quan `data/tasks.json` no conté registres
  Atès que la base de dades JSON no conté encara tasques
  quan l’estudiant executa `python src/tasks_app.py list`
  aleshores el sistema mostra `Registre de tasques buit.`

- GS-03: Llistat de tasques quan data/tasks.json conté registres
  Atès que el fitxer `data/tasks.json` conté les següents tasques:
    | id | títol          | assignatura | estat   |
    | 1  | Pràctica 1     | RS          | pendent |
    | 2  | Examen parcial | SO          | pendent |
  quan l’estudiant executa `python src/tasks_app.py list`
  aleshores el sistema mostra per pantalla:
    "[1] Pràctica 1 (RS) - estat: pendent"
    "[2] Examen parcial (SO) - estat: pendent"

## 6. Increment 2 — Data límit, edició, finalització i priorització

### 6.1 Històries d'usuari
Les històries US-03 a US-08 de la secció 2 segueixen el patró obligatori «Com a estudiant, vull... per tal de...» i cobreixen les cinc funcionalitats noves, la validació d'errors i la reproducibilitat de les proves.

### 6.2 Convenció de redacció SOPHIST
Els requisits RF-05 a RF-25 segueixen rigorosament la plantilla SOPHIST (FunktionsMASTER):

`[condició] + El sistema tasks_app + HA DE + [(donar a l'estudiant la possibilitat de | ser capaç de)] + verb en infinitiu + objecte + [detalls]`

- Veu activa i oració completa.
- Un sol verb principal per requisit.
- El sistema s'anomena explícitament amb `tasks_app`.
- `donar a l'estudiant la possibilitat de` s'usa per a interacció d'usuari; `ser capaç de` per a dependència d'una font externa (dades del sprint 1); la forma directa per a activitat automàtica del sistema.
- Les condicions s'escriuen al començament amb `Quan ...`.

### 6.3 Requisits funcionals nous (RF-05 a RF-25)
- RF-05: El sistema tasks_app HA DE desar el camp opcional `data_límit` en format `YYYY-MM-DD` dins de cada registre de `data/tasks.json`.
- RF-06: El sistema tasks_app HA DE donar a l'estudiant la possibilitat d'assignar una data límit a una tasca nova mitjançant el paràmetre `--due YYYY-MM-DD` del comandament `add`.
- RF-07: El sistema tasks_app HA DE mostrar el missatge `Tasca [ID: <id>] creada amb èxit` després d'afegir una tasca amb data límit, igual que al sprint 1.
- RF-08: El sistema tasks_app HA DE ser capaç de llegir les tasques del sprint 1 emmagatzemades a `data/tasks.json` sense el camp `data_límit`.
- RF-09: El sistema tasks_app HA DE considerar sense data límit les tasques recuperades que no contenen el camp `data_límit`.
- RF-10: Quan l'estudiant introdueix una data límit amb un format diferent de `YYYY-MM-DD` o una data inexistent, el sistema tasks_app HA DE mostrar el missatge `Error: data límit no vàlida. Format esperat: YYYY-MM-DD.`
- RF-11: Quan una operació `add` o `edit` rep una data límit no vàlida, el sistema tasks_app HA DE mantenir `data/tasks.json` sense cap modificació.
- RF-12: El sistema tasks_app HA DE donar a l'estudiant la possibilitat de modificar el títol, l'assignatura, la data límit o l'estat d'una tasca identificada amb `edit --id ID`.
- RF-13: El sistema tasks_app HA DE mantenir l'identificador d'una tasca després d'executar el comandament `edit --id ID`.
- RF-14: El sistema tasks_app HA DE conservar els camps no indicats d'una tasca quan l'estudiant executa `edit --id ID` amb només alguns paràmetres.
- RF-15: El sistema tasks_app HA DE mostrar el missatge `Tasca [ID: <id>] actualitzada amb èxit` després d'una modificació correcta amb `edit --id ID`.
- RF-16: El sistema tasks_app HA DE donar a l'estudiant la possibilitat de marcar com a completada una tasca identificada amb `complete --id ID`.
- RF-17: El sistema tasks_app HA DE mostrar el missatge `Tasca [ID: <id>] completada amb èxit` després d'una finalització correcta amb `complete --id ID`.
- RF-18: Quan l'estudiant indica amb `edit --id ID` o `complete --id ID` un identificador inexistent, el sistema tasks_app HA DE mostrar el missatge `Error: no existeix la tasca amb ID <id>.`
- RF-19: Quan l'estudiant indica amb `edit --id ID` o `complete --id ID` un identificador inexistent, el sistema tasks_app HA DE mantenir `data/tasks.json` sense cap modificació.
- RF-20: Quan una tasca pendent té una data límit anterior a la data de referència, el sistema tasks_app HA DE mostrar l'etiqueta `[CADUCADA]` a la línia corresponent del comandament `list`.
- RF-21: Quan una tasca pendent té una data límit compresa entre la data de referència i els sis dies següents, ambdós inclosos, el sistema tasks_app HA DE mostrar l'etiqueta `[URGENT]` a la línia corresponent del comandament `list`.
- RF-22: Quan una tasca no té data límit, el sistema tasks_app HA DE mostrar la línia corresponent del comandament `list` sense les etiquetes `[URGENT]` ni `[CADUCADA]`.
- RF-23: Quan una tasca té l'estat `completada`, el sistema tasks_app HA DE mostrar la línia corresponent del comandament `list` sense les etiquetes `[URGENT]` ni `[CADUCADA]`.
- RF-24: Quan una tasca pendent té una data límit exactament set dies posterior a la data de referència, el sistema tasks_app HA DE mostrar la línia corresponent del comandament `list` sense l'etiqueta `[URGENT]`.
- RF-25: El sistema tasks_app HA DE fer servir el valor de la variable d'entorn `TASKS_TODAY`, amb format `YYYY-MM-DD`, com a data de referència per a les comprovacions d'urgència i caducitat.

### 6.4 Format de comandaments i sortides
- `add --title <títol> --subject <assignatura> [--due YYYY-MM-DD]`: confirma amb `Tasca [ID: <id>] creada amb èxit` també quan s'indica data límit.
- `edit --id <id> [--title <títol>] [--subject <assignatura>] [--due YYYY-MM-DD] [--status pendent|completada]`: confirma amb `Tasca [ID: <id>] actualitzada amb èxit`. L'ID no es modifica.
- `complete --id <id>`: confirma amb `Tasca [ID: <id>] completada amb èxit` i estableix l'estat `completada`.
- `list` sense data límit: `[<id>] <títol> (<assignatura>) - estat: <estat>`, idèntic al format del sprint 1.
- `list` amb data límit: `[<id>] <títol> (<assignatura>) - estat: <estat> - data límit: <YYYY-MM-DD>`, seguit d'un espai i de l'etiqueta `[CADUCADA]` o `[URGENT]` només si escau.
- Les tasques sense data límit i les tasques completades no porten cap etiqueta, encara que la data límit hagi passat.

### 6.5 Data de referència controlada
Tots els escenaris temporals fixen la data de referència amb `TASKS_TODAY=2026-06-15`. Això dona els límits següents:

| Concepte            | Data       | Condició                                  |
| ------------------- | ---------- | ----------------------------------------- |
| Data de referència  | 2026-06-15 | Avui simulada                             |
| Caducada            | 2026-06-14 | Anterior a la data de referència          |
| Urgent (inici)      | 2026-06-15 | Igual a la data de referència             |
| Urgent (final)      | 2026-06-21 | Data de referència + 6 dies               |
| No urgent           | 2026-06-22 | Data de referència + 7 dies               |

Les proves s'executen sobre una còpia aïllada de `data/tasks.json` i no alteren les dades originals de l'aplicació.

### 6.6 Criteris d'acceptació (GS-04 a GS-19)

- GS-04: Creació d'una tasca amb data límit
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté `[]`
  Quan l'estudiant executa `python src/tasks_app.py add --title 'Pràctica 1' --subject 'RS' --due 2026-06-20`
  Aleshores el sistema confirma `Tasca [ID: 1] creada amb èxit`
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-20 |

- GS-05: Compatibilitat amb una tasca del sprint 1 sense data límit
  Atès que el fitxer `data/tasks.json` conté una tasca amb `id` 1, `títol` `Pràctica 1`, `assignatura` `RS`, `estat` `pendent` i sense el camp `data_límit`
  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent`
  I la línia no conté les etiquetes `[URGENT]` ni `[CADUCADA]`.

- GS-06: Data límit amb format incorrecte
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté `[]`
  Quan l'estudiant executa `python src/tasks_app.py add --title 'Pràctica 1' --subject 'RS' --due 15/06/2026`
  Aleshores el sistema mostra `Error: data límit no vàlida. Format esperat: YYYY-MM-DD.`
  I el fitxer `data/tasks.json` continua contenint `[]`.

- GS-07: Data límit inexistent
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté `[]`
  Quan l'estudiant executa `python src/tasks_app.py add --title 'Pràctica 1' --subject 'RS' --due 2026-02-30`
  Aleshores el sistema mostra `Error: data límit no vàlida. Format esperat: YYYY-MM-DD.`
  I el fitxer `data/tasks.json` continua contenint `[]`.

- GS-08: Modificació de tots els camps d'una tasca
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-20 |

  Quan l'estudiant executa `python src/tasks_app.py edit --id 1 --title 'Pràctica 2' --subject 'SO' --due 2026-06-21 --status completada`
  Aleshores el sistema mostra `Tasca [ID: 1] actualitzada amb èxit`
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat      | data_límit |
    | 1  | Pràctica 2 | SO          | completada | 2026-06-21 |

- GS-09: Modificació parcial d'una tasca
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-20 |

  Quan l'estudiant executa `python src/tasks_app.py edit --id 1 --title 'Pràctica 2'`
  Aleshores el sistema mostra `Tasca [ID: 1] actualitzada amb èxit`
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 2 | RS          | pendent | 2026-06-20 |

- GS-10: Identificador inexistent en la modificació
  Atès que el fitxer `data/tasks.json` conté una única tasca amb `id` 1
  Quan l'estudiant executa `python src/tasks_app.py edit --id 99 --title 'Inexistent'`
  Aleshores el sistema mostra `Error: no existeix la tasca amb ID 99.`
  I el fitxer `data/tasks.json` roman amb la mateixa única tasca amb `id` 1.

- GS-11: Finalització d'una tasca
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-20 |

  Quan l'estudiant executa `python src/tasks_app.py complete --id 1`
  Aleshores el sistema mostra `Tasca [ID: 1] completada amb èxit`
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat      | data_límit |
    | 1  | Pràctica 1 | RS          | completada | 2026-06-20 |

- GS-12: Identificador inexistent en la finalització
  Atès que el fitxer `data/tasks.json` conté una única tasca amb `id` 1
  Quan l'estudiant executa `python src/tasks_app.py complete --id 99`
  Aleshores el sistema mostra `Error: no existeix la tasca amb ID 99.`
  I el fitxer `data/tasks.json` roman amb la mateixa única tasca amb `id` 1.

- GS-13: Tasca pendent caducada
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-14 |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-14 [CADUCADA]`.

- GS-14: Tasca pendent urgent amb la data límit avui
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-15 |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-15 [URGENT]`.

- GS-15: Tasca pendent urgent amb la data límit a sis dies
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-21 |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-21 [URGENT]`.

- GS-16: Tasca pendent amb la data límit a set dies
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-22 |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-22`
  I la línia no conté l'etiqueta `[URGENT]`.

- GS-17: Tasca pendent sense data límit
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent |            |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent`
  I la línia no conté les etiquetes `[URGENT]` ni `[CADUCADA]`.

- GS-18: Tasca completada amb la data límit caducada
  Atès que la data de referència controlada és `2026-06-15` (`TASKS_TODAY=2026-06-15`)
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat      | data_límit |
    | 1  | Pràctica 1 | RS          | completada | 2026-06-10 |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: completada - data límit: 2026-06-10`
  I la línia no conté les etiquetes `[URGENT]` ni `[CADUCADA]`.

- GS-19: Data de referència controlada davant d'una data real diferent
  Atès que la data real del sistema és `2026-06-01`
  I la variable d'entorn `TASKS_TODAY` és `2026-06-15`
  I el fitxer `data/tasks.json` conté la tasca següent:

    | id | títol      | assignatura | estat   | data_límit |
    | 1  | Pràctica 1 | RS          | pendent | 2026-06-20 |

  Quan l'estudiant executa `python src/tasks_app.py list`
  Aleshores el sistema mostra `[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-20 [URGENT]`
  I el resultat no depèn de la data real del sistema.
