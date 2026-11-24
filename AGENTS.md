# AGENTS.md — Directives per a OpenCode

## Entorn i Stack Tècnic
- Llenguatge: Python 3.11+
- Interfície: Línia de comandes (CLI) amb mòdul `argparse` o `cmd`  
- Manteniment de Dades: Fitxer JSON local (`data/tasks.json`)

## Comandes de Desenvolupament
- Executar aplicació: `python3 src/tasks_app.py`
- Executar tots els tests: `python3 -m pytest test`
- Executar test únic: `python3 -m pytest test/test_task.py`

## Convencions de Codi
- Estil: PEP8.
- Idioma del codi i comentaris: Català (mantenir consistència en noms de variables).

## Regles de Gestió de Tasques (`TASKS.md`)
1. Llegeix `TASKS.md` i identifica la següent tasca amb estat `[ ]`.
2. Canvia l'estat de la tasca actual a `[/]` abans d'iniciar la codificació.
3. Executa ÚNICAMENT una sola tasca per torn.
4. Verifica que el codi compleixi els requisits i escenaris Gherkin de `SPECIFICATIONS.md`.
5. Quan estigui completada i verificada, canvia l'estat a `[x]`.
6. Atura't i demana confirmació a l'usuari abans de passar a la següent tasca.

## Restriccions de Desenvolupament
- No instal·lis llibreries externes no autoritzades.
- No modifiquis fitxers de configuració fora de `src/` i `test/`

