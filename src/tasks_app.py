import argparse
import json
import re
from datetime import date
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task

RUTA_ARREL = Path(__file__).resolve().parent.parent
RUTA_DADES = RUTA_ARREL / "data" / "tasks.json"
MISSATGE_DATA_INVALIDA = "Error: data límit no vàlida. Format esperat: YYYY-MM-DD."
MISSATGE_ESTAT_INVALID = "Error: estat no vàlid. Valors permesos: pendent, completada."
ESTAT_COMPLETADA = "completada"
ESTATS = ("pendent", ESTAT_COMPLETADA)


def es_data_valida(cadena):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cadena) is None:
        return False
    try:
        date.fromisoformat(cadena)
    except ValueError:
        return False
    return True


def carregar_tasques():
    if not RUTA_DADES.exists():
        RUTA_DADES.parent.mkdir(parents=True, exist_ok=True)
        RUTA_DADES.write_text("[]", encoding="utf-8")
        return []
    with RUTA_DADES.open(encoding="utf-8") as fitxer:
        return [Task.from_dict(dada) for dada in json.load(fitxer)]


def desar_tasques(tasques):
    RUTA_DADES.parent.mkdir(parents=True, exist_ok=True)
    with RUTA_DADES.open("w", encoding="utf-8") as fitxer:
        json.dump(
            [tasca.to_dict() for tasca in tasques],
            fitxer,
            ensure_ascii=False,
            indent=2,
        )
        fitxer.write("\n")


def afegir_tasca(títol, assignatura, data_límit=None):
    if data_límit is not None and not es_data_valida(data_límit):
        print(MISSATGE_DATA_INVALIDA)
        return
    tasques = carregar_tasques()
    identificador = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(
        id=identificador,
        títol=títol,
        assignatura=assignatura,
        data_límit=data_límit,
    )
    tasques.append(tasca)
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] creada amb èxit")


def modificar_tasca(
    identificador,
    títol=None,
    assignatura=None,
    data_límit=None,
    estat=None,
):
    if data_límit is not None and not es_data_valida(data_límit):
        print(MISSATGE_DATA_INVALIDA)
        return
    if estat is not None and estat not in ESTATS:
        print(MISSATGE_ESTAT_INVALID)
        return
    tasques = carregar_tasques()
    tasca = next(
        (element for element in tasques if element.id == identificador),
        None,
    )
    if tasca is None:
        print(f"Error: no existeix la tasca amb ID {identificador}.")
        return
    if títol is not None:
        tasca.títol = títol
    if assignatura is not None:
        tasca.assignatura = assignatura
    if data_límit is not None:
        tasca.data_límit = data_límit
    if estat is not None:
        tasca.estat = estat
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] actualitzada amb èxit")


def completar_tasca(identificador):
    tasques = carregar_tasques()
    tasca = next(
        (element for element in tasques if element.id == identificador),
        None,
    )
    if tasca is None:
        print(f"Error: no existeix la tasca amb ID {identificador}.")
        return
    tasca.estat = ESTAT_COMPLETADA
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] completada amb èxit")


def llistar_tasques():
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(
            f"[{tasca.id}] {tasca.títol} ({tasca.assignatura}) "
            f"- estat: {tasca.estat}"
        )


def construir_parser():
    parser = argparse.ArgumentParser(
        prog="tasks_app",
        description="Gestor de tasques acadèmiques.",
    )
    comandaments = parser.add_subparsers(
        dest="comandament",
        required=True,
    )
    afegir = comandaments.add_parser(
        "add",
        help="Crea una nova tasca.",
    )
    afegir.add_argument(
        "--title",
        required=True,
        help="Títol de la tasca.",
    )
    afegir.add_argument(
        "--subject",
        required=True,
        help="Assignatura de la tasca.",
    )
    afegir.add_argument(
        "--due",
        help="Data límit amb format YYYY-MM-DD.",
    )
    editar = comandaments.add_parser(
        "edit",
        help="Modifica una tasca existent.",
    )
    editar.add_argument(
        "--id",
        required=True,
        type=int,
        help="Identificador de la tasca.",
    )
    editar.add_argument(
        "--title",
        help="Nou títol de la tasca.",
    )
    editar.add_argument(
        "--subject",
        help="Nova assignatura de la tasca.",
    )
    editar.add_argument(
        "--due",
        help="Nova data límit amb format YYYY-MM-DD.",
    )
    editar.add_argument(
        "--status",
        help="Nou estat: pendent o completada.",
    )
    finalitzar = comandaments.add_parser(
        "complete",
        help="Marca una tasca com a completada.",
    )
    finalitzar.add_argument(
        "--id",
        required=True,
        type=int,
        help="Identificador de la tasca.",
    )
    comandaments.add_parser(
        "list",
        help="Mostra totes les tasques registrades.",
    )
    return parser


def main():
    arguments = construir_parser().parse_args()
    if arguments.comandament == "add":
        afegir_tasca(arguments.title, arguments.subject, arguments.due)
    elif arguments.comandament == "edit":
        modificar_tasca(
            arguments.id,
            arguments.title,
            arguments.subject,
            arguments.due,
            arguments.status,
        )
    elif arguments.comandament == "complete":
        completar_tasca(arguments.id)
    elif arguments.comandament == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()
