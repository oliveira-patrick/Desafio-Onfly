"""Teste adicional: leitura integral do arquivo, sem o corte em 200 linhas """

from helpers import run_cli


def test_reads_all_rows_beyond_200(tmp_path):
    rows = [{"reservation_id": f"R-{i}"} for i in range(201)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 201

"""Teste adicional: leitura de arquivo com exatamente 200 linhas"""

def test_reads_exactly_200_rows(tmp_path):
    """Fronteira exata do antigo corte: nenhuma linha perdida em arquivo de 200 reservas."""
    rows = [{"reservation_id": f"R-{i}"} for i in range(200)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 200
    assert report["summary"]["confirmed_reservations"] == 200