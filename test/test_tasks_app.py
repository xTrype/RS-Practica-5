import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ARREL_PROJECTE = Path(__file__).resolve().parent.parent
APP_ORIGINAL = ARREL_PROJECTE / "src" / "tasks_app.py"
MODEL_ORIGINAL = ARREL_PROJECTE / "src" / "models.py"


@pytest.fixture
def projecte_aillat(tmp_path):
    directori_src = tmp_path / "src"
    directori_src.mkdir()
    shutil.copy(APP_ORIGINAL, directori_src / "tasks_app.py")
    shutil.copy(MODEL_ORIGINAL, directori_src / "models.py")
    return tmp_path, tmp_path / "data" / "tasks.json"


def executar_cli(directori, *arguments):
    resultat = subprocess.run(
        [sys.executable, "src/tasks_app.py", *arguments],
        cwd=directori,
        capture_output=True,
        text=True,
        check=True,
    )
    return resultat.stdout.strip()


def llegir_dades(ruta_dades):
    return json.loads(ruta_dades.read_text(encoding="utf-8"))


def test_gs01_creacio_correcta_duna_tasca(projecte_aillat):
    directori, ruta_dades = projecte_aillat

    sortida = executar_cli(
        directori,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
    )

    assert sortida == "Tasca [ID: 1] creada amb èxit"
    assert llegir_dades(ruta_dades) == [
        {
            "id": 1,
            "títol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_gs02_llistat_buit(projecte_aillat):
    directori, ruta_dades = projecte_aillat

    sortida = executar_cli(directori, "list")

    assert sortida == "Registre de tasques buit."
    assert llegir_dades(ruta_dades) == []


def test_gs03_llistat_amb_registres(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    ruta_dades.parent.mkdir(parents=True, exist_ok=True)
    ruta_dades.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "títol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "títol": "Examen parcial",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    sortida = executar_cli(directori, "list")

    assert sortida.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Examen parcial (SO) - estat: pendent",
    ]
