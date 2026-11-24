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

- [x] Tasca 2.2: Incorporació i validació de dates límit: acceptar `--due YYYY-MM-DD` a `add`, conservar el missatge de confirmació i rebutjar formats incorrectes o dates inexistents sense desar res. (Requisits RF-06, RF-07, RF-10 i RF-11; escenaris GS-04, GS-06, GS-07 i GS-20)

- [x] Tasca 2.3: Implementació de la modificació de tasques: afegir `edit --id ID` per a `--title`, `--subject`, `--due` i `--status`, mantenir l'ID i els camps no indicats, i gestionar identificadors inexistents. (Requisits RF-12, RF-13, RF-14, RF-15, RF-18 i RF-19; escenaris GS-08, GS-09, GS-10 i GS-20)

- [x] Tasca 2.4: Implementació de la finalització de tasques: afegir `complete --id ID` per a establir l'estat `completada` i gestionar identificadors inexistents sense modificar les dades. (Requisits RF-16, RF-17, RF-18 i RF-19; escenaris GS-11 i GS-12)

- [x] Tasca 2.5: Identificació de tasques urgents i caducades: calcular les etiquetes `[CADUCADA]` i `[URGENT]` a `list` amb la data de referència controlada, excloent tasques sense data, completades i del dia +7. (Requisits RF-20, RF-21, RF-22, RF-23, RF-24 i RF-25; escenaris GS-13, GS-14, GS-15, GS-16, GS-17, GS-18, GS-19, GS-21 i GS-22)

- [x] Tasca 2.6: Tests d'integració dels nous escenaris Gherkin: estendre `test/test_tasks_app.py` amb GS-04 a GS-22, fixant `TASKS_TODAY=2026-06-15` llevat de GS-22, que no el defineix i no altera el rellotge, i treballant sobre còpies aïllades de `data/tasks.json`. (Requisits RF-05 a RF-25; escenaris GS-04 a GS-22; directives de proves de dates d'`AGENTS.md`)

- [x] Tasca 2.7: Validació final i proves de regressió: executar `python3 -m pytest test`, verificar RF-01 a RF-25 i GS-01 a GS-22, i comprovar que les dades originals resten intactes. (Requisits RF-01 a RF-25; escenaris GS-01 a GS-22)



## Increment 3: Resum, filtratge i cerca de tasques

Objectiu: afegir consultes agregades i filtres sobre el llistat sense alterar els formats existents ni les dades persistides.

Dependències: resum → filtre per assignatura → cerca per paraula clau i combinació → tests → validació.



### Tasques d'Execució:

- [ ] Tasca 3.1: Implementació del resum estadístic: afegir `list --summary` amb els recomptes de total, pendents, completades, caducades i urgents, excloure les tasques completades del recompte temporal, aplicar el format exacte amb registre buit a zero i rebutjar la combinació amb filtres amb el missatge d'error definit. (Requisits RF-02, RF-26, RF-27, RF-28, RF-29, RF-30, RF-31, RF-32, RF-38, RF-41 i RF-42; escenaris GS-23, GS-24, GS-25, GS-26, GS-35, GS-36, GS-37 i GS-40)

- [ ] Tasca 3.2: Filtratge per assignatura: afegir `list --subject ASSIGNATURA` amb coincidència exacta insensible a majúscules i minúscules, missatge de sense coincidències i conservació del format i les etiquetes del llistat. (Requisits RF-02, RF-33, RF-34, RF-39, RF-40, RF-42 i RF-43; escenaris GS-27, GS-28, GS-29, GS-38, GS-39 i GS-41)

- [ ] Tasca 3.3: Cerca per paraula clau i combinació de filtres: afegir `list --keyword PARAULA` amb coincidència parcial insensible a majúscules i minúscules, i fer que `--subject` i `--keyword` combinats exigeixin ambdues condicions. (Requisits RF-02, RF-35, RF-36, RF-37, RF-39, RF-40 i RF-42; escenaris GS-30, GS-31, GS-32, GS-33, GS-34, GS-38, GS-39, GS-42 i GS-43)

- [ ] Tasca 3.4: Tests d'integració dels nous escenaris Gherkin: estendre `test/test_tasks_app.py` amb GS-23 a GS-43, fixant `TASKS_TODAY=2026-06-15` quan calgui i treballant sobre còpies aïllades de `data/tasks.json`, amb verificació de format, missatges d'error i no modificació de les dades. (Requisits RF-26 a RF-43; escenaris GS-23 a GS-43; directives de proves de dates d'`AGENTS.md`)

- [ ] Tasca 3.5: Validació final i proves de regressió: executar `python3 -m pytest test -v`, verificar RF-01 a RF-43 i GS-01 a GS-43, comprovar la compatibilitat dels formats dels sprints 1 i 2 i confirmar que les dades originals resten intactes. (Requisits RF-01 a RF-43; escenaris GS-01 a GS-43)
