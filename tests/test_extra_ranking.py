"""Teste adicional: ordenação do ranking de hotéis (valor e desempate)."""

from helpers import run_cli


def test_top_hotels_tie_breaks_by_hotel_id_ascending(tmp_path):
    """Valor total decrescente e, no empate, hotel_id crescente.

    As duas regras do README valem ao mesmo tempo, em sentidos opostos:
    `total_brl` desce e `hotel_id` sobe. H10 e H02 empatam em 500.00, então
    uma inversão global do ranking (por exemplo `reverse=True` sobre a chave
    composta) colocaria H10 antes de H02 e este teste falharia.
    """
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H10", "hotel_name": "Hotel J", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "500.00"},
            {"reservation_id": "R-3", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "900.00"},
        ],
    )

    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02", "H10"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["900.00", "500.00", "500.00"]
    assert [hotel["hotel_name"] for hotel in report["top_hotels"]] == ["Hotel A", "Hotel B", "Hotel J"]
