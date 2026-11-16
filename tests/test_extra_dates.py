"""Teste adicional: virada de ano e mês de referência das diárias."""

from helpers import run_cli


def test_nights_across_year_credit_to_checkin_month(tmp_path):
    """3 noites na virada de ano, todas creditadas ao mês do check-in.

    30/12/2024 -> 02/01/2025 são 3 noites pela diferença não inclusiva de
    calendário, e a reserva inteira pertence a `2024-12` (mês do check-in),
    sem qualquer rateio para `2025-01`.
    """
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2024-12-30",
                "checkout_date": "2025-01-02",
                "rooms": "1",
                "status": "CONFIRMED",
                "amount": "100.00",
                "currency": "BRL",
            }
        ],
    )

    assert report["summary"]["total_room_nights"] == 3
    assert report["summary"]["total_amount_brl"] == "100.00"
    assert [month["month"] for month in report["by_month"]] == ["2024-12"]
    assert report["by_month"] == [
        {"month": "2024-12", "reservations": 1, "room_nights": 3, "total_brl": "100.00"}
    ]
