"""Teste adicional: arredondamento half-up apenas na serialização."""

from helpers import run_cli


def test_average_rounds_half_up_on_serialization(tmp_path):
    """200.01 em 2 noites dá média exata 100.005, serializada como "100.01".

    O valor exato fica no meio da casa decimal: half-up devolve "100.01",
    enquanto half-even devolveria "100.00" e uma conta em float produziria
    resíduo (100.00499999...), que também arredondaria para baixo.
    """
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-01-10",
                "checkout_date": "2025-01-12",
                "rooms": "1",
                "status": "CONFIRMED",
                "currency": "BRL",
                "amount": "200.01",
            }
        ],
    )

    assert report["summary"]["total_room_nights"] == 2
    assert report["summary"]["total_amount_brl"] == "200.01"
    assert report["summary"]["average_nightly_rate_brl"] == "100.01"
