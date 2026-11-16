"""Cálculo de noites ocupadas."""

from __future__ import annotations

from datetime import date


def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """
        Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos.

        Correção: 
            De --> (checkout.day - checkin.day) * rooms 
            Para --> (checkout - checkin).days * rooms 
        Justificativa:
            O cálculo subtraía os componentes dia-do-mês (checkout.day - checkin.day) em vez da diferença 
            real de calendário ((checkout - checkin).days), produzindo noites erradas, até negativas, em 
            qualquer estadia que cruza virada de mês ou ano.
        Referência: Linhas 67 - 71 das instruções no README 
    """
    return (checkout - checkin).days * rooms 