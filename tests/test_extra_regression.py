"""Teste adicional: regressão ponta a ponta sobre a amostra oficial do README."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from helpers import PROJECT_ROOT, SRC_DIR

INPUT_CSV = PROJECT_ROOT / "data" / "exemplo-validacao.csv"
RATES_CSV = PROJECT_ROOT / "data" / "taxas_cambio.csv"

# Valores da seção "Amostra de validação" do README (bloco AMOSTRA:INICIO/FIM).
EXPECTED_SUMMARY = {
    "total_reservations": 12,
    "confirmed_reservations": 9,
    "cancelled_reservations": 2,
    "no_show_reservations": 1,
    "total_room_nights": 28,
    "total_amount_brl": "7566.00",
    "average_nightly_rate_brl": "270.21",
}

EXPECTED_BY_MONTH = [
    {"month": "2025-01", "reservations": 8, "room_nights": 25, "total_brl": "6684.00"},
    {"month": "2025-02", "reservations": 1, "room_nights": 3, "total_brl": "882.00"},
]

EXPECTED_TOP_HOTELS = [
    {"hotel_id": "H01", "hotel_name": "Hotel Aurora Paulista", "room_nights": 3, "total_brl": "1200.00"},
    {"hotel_id": "H02", "hotel_name": "Hotel Mirante", "room_nights": 2, "total_brl": "1084.00"},
    {"hotel_id": "H12", "hotel_name": "Hotel Miami Beach", "room_nights": 1, "total_brl": "1000.00"},
    {"hotel_id": "H10", "hotel_name": "Hotel Madrid, Gran Vía", "room_nights": 4, "total_brl": "900.00"},
    {"hotel_id": "H09", "hotel_name": "Hotel Lisboa, Centro", "room_nights": 3, "total_brl": "882.00"},
]


def run_cli_on_official_sample(output_path: Path) -> subprocess.CompletedProcess[str]:
    """Executa o CLI sobre os CSVs oficiais, no mesmo padrão de `helpers.run_cli`."""
    environment = os.environ.copy()
    for import_root in (SRC_DIR, PROJECT_ROOT):
        if (import_root / "onfly_report").is_dir():
            environment["PYTHONPATH"] = str(import_root) + os.pathsep + environment.get("PYTHONPATH", "")
            break
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "onfly_report",
            "--input",
            str(INPUT_CSV),
            "--rates",
            str(RATES_CSV),
            "--output",
            str(output_path),
            "--top",
            "5",
        ],
        cwd=str(PROJECT_ROOT),
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_official_validation_sample_matches_expected_report(tmp_path):
    """O relatório da amostra oficial é igual ao do README, exceto `generated_at`."""
    output_path = tmp_path / "exemplo.json"

    process = run_cli_on_official_sample(output_path)

    assert process.returncode == 0, process.stderr
    assert output_path.is_file()

    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert report["report_version"] == "1.0"
    assert report["generated_at"].endswith("-03:00")

    # Comparação integral: o relatório não tem campos além do contrato e
    # `generated_at` é o único valor dinâmico, explicitamente ignorado.
    assert set(report) == {"report_version", "generated_at", "summary", "by_month", "top_hotels"}
    assert report["summary"] == EXPECTED_SUMMARY
    assert report["by_month"] == EXPECTED_BY_MONTH
    assert report["top_hotels"] == EXPECTED_TOP_HOTELS
