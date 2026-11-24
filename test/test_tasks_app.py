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
MISSATGE_DATA_INVALIDA = (
    "Error: data límit no vàlida. Format esperat: YYYY-MM-DD."
)
MISSATGE_ID_INVALID = "Error: no existeix la tasca amb ID 99."
MISSATGE_SENSE_COINCIDENCIES = (
    "No s'han trobat tasques que compleixin els filtres."
)
MISSATGE_RESUM_FILTRES = (
    "Error: --summary no es pot combinar amb --subject ni --keyword."
)


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


def resum(total, pendents, completades, caducades, urgents):
    return "\n".join(
        [
            "Resum de tasques:",
            f"- Total: {total}",
            f"- Pendents: {pendents}",
            f"- Completades: {completades}",
            f"- Caducades: {caducades}",
            f"- Urgents: {urgents}",
        ]
    )


def comprovar_consulta(
    directori,
    ruta_dades,
    tasques,
    arguments,
    esperat,
    entorn=ENTORN_REFERENCIA,
):
    escriure_dades(ruta_dades, tasques)
    original = ruta_dades.read_bytes()
    sortida = executar_cli(directori, "list", *arguments, entorn=entorn)
    assert sortida == esperat
    assert ruta_dades.read_bytes() == original


def comprovar_inicialitzacio(directori, ruta_dades, arguments, esperat):
    if ruta_dades.exists():
        ruta_dades.unlink()
    sortida = executar_cli(
        directori,
        "list",
        *arguments,
        entorn=ENTORN_REFERENCIA,
    )
    assert sortida == esperat
    assert ruta_dades.read_text(encoding="utf-8") == "[]"


def comprovar_rebuig_abans_json(directori, ruta_dades, arguments):
    if ruta_dades.exists():
        ruta_dades.unlink()
    sortida = executar_cli(
        directori,
        "list",
        *arguments,
        entorn=ENTORN_REFERENCIA,
    )
    assert sortida == MISSATGE_RESUM_FILTRES
    assert not ruta_dades.exists()


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


def test_gs23_resum_estadistic(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [
            tasca(1, "Pràctica 1", "RS", "pendent", "2026-06-14"),
            tasca(2, "Pràctica 2", "RS", "pendent", "2026-06-16"),
            tasca(3, "Apunts", "SO", "pendent"),
            tasca(4, "Examen", "RS", "completada", "2026-06-10"),
        ],
        ("--summary",),
        resum(4, 3, 1, 1, 1),
    )


def test_gs24_resum_registre_buit(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [],
        ("--summary",),
        resum(0, 0, 0, 0, 0),
    )


def test_gs25_limits_temporals_al_resum(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [
            tasca(1, "Avui", "RS", "pendent", "2026-06-15"),
            tasca(2, "Sis dies", "RS", "pendent", "2026-06-21"),
            tasca(3, "Set dies", "SO", "pendent", "2026-06-22"),
            tasca(4, "Feta", "SO", "completada", "2026-06-16"),
        ],
        ("--summary",),
        resum(4, 3, 1, 0, 2),
    )


def test_gs26_resum_sense_modificar_dades(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [tasca(1, "Pràctica 1", "RS", "pendent", "2026-06-16")],
        ("--summary",),
        resum(1, 1, 0, 0, 1),
    )


def test_gs27_filtre_assignatura_exacte(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [
            tasca(1, "Pràctica 1", "RS", "pendent", "2026-06-14"),
            tasca(2, "Pràctica 2", "rs", "pendent", "2026-06-20"),
            tasca(3, "Examen", "SO", "pendent"),
            tasca(4, "Pràctica 4", "RST", "pendent"),
        ],
        ("--subject", "rs"),
        (
            "[1] Pràctica 1 (RS) - estat: pendent "
            "- data límit: 2026-06-14 [CADUCADA]\n"
            "[2] Pràctica 2 (rs) - estat: pendent "
            "- data límit: 2026-06-20 [URGENT]"
        ),
    )


def test_gs28_filtre_assignatura_sense_coincidencies(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [tasca(1, "Examen", "SO", "pendent")],
        ("--subject", "RS"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs29_filtre_assignatura_registre_buit(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [],
        ("--subject", "RS"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs30_cerca_paraula_clau_parcial(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [
            tasca(1, "Pràctica de Xarxes", "RS", "pendent", "2026-06-16"),
            tasca(2, "Xarxa avançada", "SO", "pendent", "2026-06-30"),
            tasca(3, "Examen", "RS", "pendent"),
        ],
        ("--keyword", "xar"),
        (
            "[1] Pràctica de Xarxes (RS) - estat: pendent "
            "- data límit: 2026-06-16 [URGENT]\n"
            "[2] Xarxa avançada (SO) - estat: pendent "
            "- data límit: 2026-06-30"
        ),
    )


def test_gs31_cerca_paraula_clau_sense_coincidencies(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [tasca(1, "Pràctica 1", "RS", "pendent")],
        ("--keyword", "examen"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs32_cerca_paraula_clau_registre_buit(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [],
        ("--keyword", "pràctica"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs33_combinacio_filtres_amb_coincidencies(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    tasques = [
        tasca(1, "Pràctica 1", "RS", "pendent", "2026-06-14"),
        tasca(2, "Pràctica 2", "RS", "pendent", "2026-06-20"),
        tasca(3, "Pràctica 3", "SO", "pendent"),
        tasca(4, "Examen", "RS", "pendent"),
    ]
    esperat = (
        "[1] Pràctica 1 (RS) - estat: pendent "
        "- data límit: 2026-06-14 [CADUCADA]\n"
        "[2] Pràctica 2 (RS) - estat: pendent "
        "- data límit: 2026-06-20 [URGENT]"
    )
    comprovar_consulta(
        directori,
        ruta_dades,
        tasques,
        ("--subject", "rs", "--keyword", "pràctica"),
        esperat,
    )
    comprovar_consulta(
        directori,
        ruta_dades,
        tasques,
        ("--keyword", "pràctica", "--subject", "rs"),
        esperat,
    )


def test_gs34_combinacio_filtres_sense_coincidencies(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [
            tasca(1, "Pràctica 1", "RS", "pendent"),
            tasca(2, "Examen", "SO", "pendent"),
        ],
        ("--subject", "so", "--keyword", "pràctica"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs35_resum_amb_filtre_assignatura(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    tasques = [tasca(1, "Pràctica 1", "RS", "pendent")]
    comprovar_consulta(
        directori,
        ruta_dades,
        tasques,
        ("--summary", "--subject", "RS"),
        MISSATGE_RESUM_FILTRES,
    )
    comprovar_consulta(
        directori,
        ruta_dades,
        tasques,
        ("--subject", "RS", "--summary"),
        MISSATGE_RESUM_FILTRES,
    )
    comprovar_rebuig_abans_json(
        directori,
        ruta_dades,
        ("--summary", "--subject", "RS"),
    )


def test_gs36_resum_amb_cerca_paraula_clau(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    tasques = [tasca(1, "Pràctica 1", "RS", "pendent")]
    comprovar_consulta(
        directori,
        ruta_dades,
        tasques,
        ("--summary", "--keyword", "pràctica"),
        MISSATGE_RESUM_FILTRES,
    )
    comprovar_consulta(
        directori,
        ruta_dades,
        tasques,
        ("--keyword", "pràctica", "--summary"),
        MISSATGE_RESUM_FILTRES,
    )
    comprovar_rebuig_abans_json(
        directori,
        ruta_dades,
        ("--summary", "--keyword", "pràctica"),
    )


def test_gs37_resum_amb_ambdos_filtres(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    tasques = [tasca(1, "Pràctica 1", "RS", "pendent")]
    for arguments in (
        ("--summary", "--subject", "RS", "--keyword", "pràctica"),
        ("--subject", "RS", "--keyword", "pràctica", "--summary"),
        ("--keyword", "pràctica", "--summary", "--subject", "RS"),
    ):
        comprovar_consulta(
            directori,
            ruta_dades,
            tasques,
            arguments,
            MISSATGE_RESUM_FILTRES,
        )
    comprovar_rebuig_abans_json(
        directori,
        ruta_dades,
        ("--summary", "--subject", "RS", "--keyword", "pràctica"),
    )


def test_gs38_format_i_etiquetes_en_resultats_filtrats(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [
            tasca(1, "Caducada", "RS", "pendent", "2026-06-14"),
            tasca(2, "Feta", "RS", "completada", "2026-06-10"),
            tasca(3, "Sense data", "RS", "pendent"),
        ],
        ("--subject", "rs"),
        (
            "[1] Caducada (RS) - estat: pendent "
            "- data límit: 2026-06-14 [CADUCADA]\n"
            "[2] Feta (RS) - estat: completada "
            "- data límit: 2026-06-10\n"
            "[3] Sense data (RS) - estat: pendent"
        ),
    )


def test_gs39_filtres_sense_modificar_dades(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_consulta(
        directori,
        ruta_dades,
        [tasca(1, "Pràctica 1", "RS", "pendent")],
        ("--subject", "rs", "--keyword", "pràctica"),
        "[1] Pràctica 1 (RS) - estat: pendent",
    )


def test_gs40_inicialitzacio_amb_resum(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_inicialitzacio(
        directori,
        ruta_dades,
        ("--summary",),
        resum(0, 0, 0, 0, 0),
    )


def test_gs41_inicialitzacio_amb_filtre_assignatura(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_inicialitzacio(
        directori,
        ruta_dades,
        ("--subject", "RS"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs42_inicialitzacio_amb_paraula_clau(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_inicialitzacio(
        directori,
        ruta_dades,
        ("--keyword", "pràctica"),
        MISSATGE_SENSE_COINCIDENCIES,
    )


def test_gs43_inicialitzacio_amb_filtres_combinats(projecte_aillat):
    directori, ruta_dades = projecte_aillat
    comprovar_inicialitzacio(
        directori,
        ruta_dades,
        ("--subject", "RS", "--keyword", "pràctica"),
        MISSATGE_SENSE_COINCIDENCIES,
    )
