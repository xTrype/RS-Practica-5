import argparse
import json
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task

RUTA_ARREL = Path(__file__).resolve().parent.parent
RUTA_DADES = RUTA_ARREL / "data" / "tasks.json"


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


def afegir_tasca(títol, assignatura):
    tasques = carregar_tasques()
    identificador = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(
        id=identificador,
        títol=títol,
        assignatura=assignatura,
    )
    tasques.append(tasca)
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] creada amb èxit")


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
    comandaments.add_parser(
        "list",
        help="Mostra totes les tasques registrades.",
    )
    return parser


def main():
    arguments = construir_parser().parse_args()
    if arguments.comandament == "add":
        afegir_tasca(arguments.title, arguments.subject)
    elif arguments.comandament == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()
