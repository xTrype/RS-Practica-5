import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ARREL_PROJECTE = Path(__file__).resolve().parent.parent
APP_ORIGINAL = ARREL_PROJECTE / "src" / "tasks_app.py"
MODEL_ORIGINAL = ARREL_PROJECTE / "src" / "models.py"
ENTORN_REFERENCIA = {**os.environ, "TASKS_TODAY": "2026-06-15"}
ENTORN_ALTRA_REFERENCIA = {**os.environ, "TASKS_TODAY": "2026-06-10"}
ENTORN_SENSE_REFERENCIA = {
    clau: valor
    for clau, valor in os.environ.items()
    if clau != "TASKS_TODAY"
}
MISSATGE_DATA_INVALIDA = "Error: data límit no vàlida. Format esperat: YYYY-MM-DD."
MISSATGE_ID_INVALID = "Error: no existeix la tasca amb ID 99."


@pytest.fixture
def projecte_aillat(tmp_path):
    directori_src = tmp_path / "src"
    directori_src.mkdir()
    shutil.copy(APP_ORIGINAL, directori_src / "tasks_app.py")
    shutil.copy(MODEL_ORIGINAL, directori_src / "models.py")
    return tmp_path, tmp_path / "data" / "tasks.json"


def executar_cli(directori, *arguments, entorn=None):
    resultat = subprocess.run(
        [sys.executable, "src/tasks_app.py", *arguments],
        cwd=directori,
        capture_output=True,
        text=True,
        check=True,
        env=entorn,
    )
    return resultat.stdout.strip()


def llegir_dades(ruta_dades):
    return json.loads(ruta_dades.read_text(encoding="utf-8"))


def escriure_dades(ruta_dades, tasques):
    ruta_dades.parent.mkdir(parents=True, exist_ok=True)
    ruta_dades.write_text(
        json.dumps(tasques, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def tasca(
    identificador=1,
    títol="Pràctica 1",
    assignatura="RS",
    estat="pendent",
    data_límit=None,
):
    registre = {
        "id": identificador,
        "títol": títol,
        "assignatura": assignatura,
        "estat": estat,
    }
    if data_límit is not None:
        registre["data_límit"] = data_límit
    return registre


def comprovar_llistat(
    directori,
    ruta_dades,
    registre,
    esperat,
    entorn=ENTORN_REFERENCIA,
):
    escriure_dades(ruta_dades, [registre])
    original = ruta_dades.read_bytes()
    sortida = executar_cli(directori, "list", entorn=entorn)
    assert sortida == esperat
    assert ruta_dades.read_bytes() == original


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


def test_gs04_crear_tasca_amb_data_limit(projecte_aillat):
    directori, ruta_dades = projecte_aillat

    sortida = executar_cli(
        directori,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
        "--due",
        "2026-06-20",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == "Tasca [ID: 1] creada amb èxit"
    assert llegir_dades(ruta_dades) == [
        {
            "id": 1,
            "títol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
            "data_límit": "2026-06-20",
        }
    ]


def test_gs05_compatibilitat_tasca_sense_data(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca()])

    sortida = executar_cli(directori, "list", entorn=ENTORN_REFERENCIA)

    assert sortida == "[1] Pràctica 1 (RS) - estat: pendent"


def test_gs06_data_llimit_format_incorrecte(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [])
    original = ruta_dades.read_bytes()

    sortida = executar_cli(
        directori,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
        "--due",
        "15/06/2026",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == MISSATGE_DATA_INVALIDA
    assert ruta_dades.read_bytes() == original


def test_gs07_data_llimit_inexistent(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [])
    original = ruta_dades.read_bytes()

    sortida = executar_cli(
        directori,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
        "--due",
        "2026-02-30",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == MISSATGE_DATA_INVALIDA
    assert ruta_dades.read_bytes() == original


def test_gs08_modificar_tots_els_camps(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca(data_límit="2026-06-20")])

    sortida = executar_cli(
        directori,
        "edit",
        "--id",
        "1",
        "--title",
        "Pràctica 2",
        "--subject",
        "SO",
        "--due",
        "2026-06-21",
        "--status",
        "completada",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == "Tasca [ID: 1] actualitzada amb èxit"
    assert llegir_dades(ruta_dades) == [
        {
            "id": 1,
            "títol": "Pràctica 2",
            "assignatura": "SO",
            "estat": "completada",
            "data_límit": "2026-06-21",
        }
    ]


def test_gs09_modificacio_parcial(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca(data_límit="2026-06-20")])

    sortida = executar_cli(
        directori,
        "edit",
        "--id",
        "1",
        "--title",
        "Pràctica 2",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == "Tasca [ID: 1] actualitzada amb èxit"
    assert llegir_dades(ruta_dades) == [
        tasca(títol="Pràctica 2", data_límit="2026-06-20")
    ]


def test_gs10_identificador_inexistent_en_edit(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca()])
    original = ruta_dades.read_bytes()

    sortida = executar_cli(
        directori,
        "edit",
        "--id",
        "99",
        "--title",
        "Inexistent",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == MISSATGE_ID_INVALID
    assert ruta_dades.read_bytes() == original


def test_gs11_finalitzar_tasca(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca(data_límit="2026-06-20")])

    sortida = executar_cli(
        directori,
        "complete",
        "--id",
        "1",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == "Tasca [ID: 1] completada amb èxit"
    assert llegir_dades(ruta_dades) == [
        tasca(data_límit="2026-06-20", estat="completada")
    ]


def test_gs12_identificador_inexistent_en_complete(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca()])
    original = ruta_dades.read_bytes()

    sortida = executar_cli(
        directori,
        "complete",
        "--id",
        "99",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == MISSATGE_ID_INVALID
    assert ruta_dades.read_bytes() == original


def test_gs13_tasca_pendent_caducada(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="2026-06-14"),
        (
            "[1] Pràctica 1 (RS) - estat: pendent "
            "- data límit: 2026-06-14 [CADUCADA]"
        ),
    )


def test_gs14_tasca_pendent_urgent_avui(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="2026-06-15"),
        (
            "[1] Pràctica 1 (RS) - estat: pendent "
            "- data límit: 2026-06-15 [URGENT]"
        ),
    )


def test_gs15_tasca_pendent_urgent_a_sis_dies(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="2026-06-21"),
        (
            "[1] Pràctica 1 (RS) - estat: pendent "
            "- data límit: 2026-06-21 [URGENT]"
        ),
    )


def test_gs16_tasca_pendent_a_set_dies_sense_etiqueta(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="2026-06-22"),
        "[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-22",
    )


def test_gs17_tasca_pendent_sense_data_llimit(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(),
        "[1] Pràctica 1 (RS) - estat: pendent",
    )


def test_gs18_tasca_completada_amb_data_caducada(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="2026-06-10", estat="completada"),
        (
            "[1] Pràctica 1 (RS) - estat: completada "
            "- data límit: 2026-06-10"
        ),
    )


def test_gs19_data_de_referencia_controlada(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca(data_límit="2026-06-20")])

    amb_referencia = executar_cli(directori, "list", entorn=ENTORN_REFERENCIA)
    assert amb_referencia == (
        "[1] Pràctica 1 (RS) - estat: pendent "
        "- data límit: 2026-06-20 [URGENT]"
    )

    amb_altra_referencia = executar_cli(
        directori,
        "list",
        entorn=ENTORN_ALTRA_REFERENCIA,
    )
    assert amb_altra_referencia == (
        "[1] Pràctica 1 (RS) - estat: pendent "
        "- data límit: 2026-06-20"
    )


def test_gs20_modificacio_amb_data_llimit_invalida(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    escriure_dades(ruta_dades, [tasca(data_límit="2026-06-20")])
    original = ruta_dades.read_bytes()

    sortida = executar_cli(
        directori,
        "edit",
        "--id",
        "1",
        "--due",
        "2026-02-30",
        entorn=ENTORN_REFERENCIA,
    )

    assert sortida == MISSATGE_DATA_INVALIDA
    assert ruta_dades.read_bytes() == original


def test_gs21_tasca_pendent_mes_enllà_de_set_dies(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="2026-06-23"),
        "[1] Pràctica 1 (RS) - estat: pendent - data límit: 2026-06-23",
    )


def test_gs22_sense_tasks_today(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    assert "TASKS_TODAY" not in ENTORN_SENSE_REFERENCIA
    comprovar_llistat(
        directori,
        ruta_dades,
        tasca(data_límit="1970-01-01"),
        (
            "[1] Pràctica 1 (RS) - estat: pendent "
            "- data límit: 1970-01-01 [CADUCADA]"
        ),
        entorn=ENTORN_SENSE_REFERENCIA,
    )
