"""Política de status das reservas."""

from __future__ import annotations


def is_billable(status: str) -> bool:
    """
        Indica se a reserva entra nos totais financeiros e de noites.

        Correção: 
            De --> status != "CANCELLED" 
            Para --> status == "CONFIRMED"
        Justificativa:
            A política de faturamento usava status != "CANCELLED", incluindo indevidamente reservas 
            NO_SHOW em noites e valores, quando só "CONFIRMED" é faturável.
        Referência: Linhas 60 - 62 e linha 83 das instruções no README
    """
    return status == "CONFIRMED"
