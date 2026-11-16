"""Teste adicional: multiplicador de quartos nas diárias."""

from helpers import run_cli


def test_room_nights_multiply_by_rooms(tmp_path):
    """3 noites x 2 quartos = 6 diárias, no resumo e nas duas agregações."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-01-10",
                "checkout_date": "2025-01-13",
                "rooms": "2",
                "status": "CONFIRMED",
                "amount": "100.00",
                "currency": "BRL",
            }
        ],
    )

    assert report["summary"]["total_room_nights"] == 6
    assert report["by_month"] == [
        {"month": "2025-01", "reservations": 1, "room_nights": 6, "total_brl": "100.00"}
    ]
    assert [(hotel["hotel_id"], hotel["room_nights"]) for hotel in report["top_hotels"]] == [("H01", 6)]
