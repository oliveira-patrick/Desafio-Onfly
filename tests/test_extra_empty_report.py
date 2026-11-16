"""Teste adicional: relatório zerado quando nenhuma reserva é faturável."""

import json

from helpers import run_cli


def test_report_zeroed_when_no_billable_reservations(tmp_path):
    """CANCELLED e NO_SHOW contam como reservas, mas não geram valores.

    As duas reservas têm datas, hotéis e valores válidos e meses distintos,
    de modo que o único motivo para ficarem fora das agregações é o status.
    """
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "hotel_id": "H77",
                "hotel_name": "Hotel Cancelado",
                "status": "CANCELLED",
                "checkin_date": "2025-01-10",
                "checkout_date": "2025-01-13",
                "rooms": "2",
                "currency": "BRL",
                "amount": "500.00",
            },
            {
                "reservation_id": "R-2",
                "hotel_id": "H88",
                "hotel_name": "Hotel Ausente",
                "status": "NO_SHOW",
                "checkin_date": "2025-02-05",
                "checkout_date": "2025-02-08",
                "rooms": "1",
                "currency": "USD",
                "amount": "300.00",
            },
        ],
    )

    assert report["summary"] == {
        "total_reservations": 2,
        "confirmed_reservations": 0,
        "cancelled_reservations": 1,
        "no_show_reservations": 1,
        "total_room_nights": 0,
        "total_amount_brl": "0.00",
        "average_nightly_rate_brl": "0.00",
    }
    assert report["by_month"] == []
    assert report["top_hotels"] == []

    # Hotéis e meses que só aparecem em reservas não faturáveis não vazam
    # para nenhum campo do relatório.
    serialized = json.dumps(report, ensure_ascii=False)
    for leaked in ("H77", "H88", "Hotel Cancelado", "Hotel Ausente", "2025-01", "2025-02"):
        assert leaked not in serialized
