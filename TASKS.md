# TASKS.md - Tasks_app



## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.



### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02)

- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.

- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)

- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03.

- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).



## Increment 2: Data límit, edició, finalització i priorització

Objectiu: Ampliar la CLI amb data límit, edició per ID, finalització i etiquetes d'urgència i caducitat, mantenint la compatibilitat amb el sprint 1 i amb proves deterministes.

Dependències: model/persistència → dates → edició → finalització → etiquetes → tests → validació.



### Tasques d'Execució:

- [x] Tasca 2.1: Adaptació del model de dades i persistència: afegir el camp opcional `data_límit` a `src/models.py`, serialitzar-lo a `data/tasks.json` i preservar les tasques del sprint 1 sense aquest camp. (Requisits RF-01, RF-05, RF-08 i RF-09; escenaris GS-04 i GS-05)

- [ ] Tasca 2.2: Incorporació i validació de dates límit: acceptar `--due YYYY-MM-DD` a `add`, conservar el missatge de confirmació i rebutjar formats incorrectes o dates inexistents sense desar res. (Requisits RF-06, RF-07, RF-10 i RF-11; escenaris GS-04, GS-06, GS-07 i GS-20)

- [ ] Tasca 2.3: Implementació de la modificació de tasques: afegir `edit --id ID` per a `--title`, `--subject`, `--due` i `--status`, mantenir l'ID i els camps no indicats, i gestionar identificadors inexistents. (Requisits RF-12, RF-13, RF-14, RF-15, RF-18 i RF-19; escenaris GS-08, GS-09, GS-10 i GS-20)

- [ ] Tasca 2.4: Implementació de la finalització de tasques: afegir `complete --id ID` per a establir l'estat `completada` i gestionar identificadors inexistents sense modificar les dades. (Requisits RF-16, RF-17, RF-18 i RF-19; escenaris GS-11 i GS-12)

- [ ] Tasca 2.5: Identificació de tasques urgents i caducades: calcular les etiquetes `[CADUCADA]` i `[URGENT]` a `list` amb la data de referència controlada, excloent tasques sense data, completades i del dia +7. (Requisits RF-20, RF-21, RF-22, RF-23, RF-24 i RF-25; escenaris GS-13, GS-14, GS-15, GS-16, GS-17, GS-18, GS-19, GS-21 i GS-22)

- [ ] Tasca 2.6: Tests d'integració dels nous escenaris Gherkin: estendre `test/test_tasks_app.py` amb GS-04 a GS-22, fixant `TASKS_TODAY=2026-06-15` llevat de GS-22, que no el defineix i no altera el rellotge, i treballant sobre còpies aïllades de `data/tasks.json`. (Requisits RF-05 a RF-25; escenaris GS-04 a GS-22; directives de proves de dates d'`AGENTS.md`)

- [ ] Tasca 2.7: Validació final i proves de regressió: executar `python3 -m pytest test`, verificar RF-01 a RF-25 i GS-01 a GS-22, i comprovar que les dades originals resten intactes. (Requisits RF-01 a RF-25; escenaris GS-01 a GS-22)
