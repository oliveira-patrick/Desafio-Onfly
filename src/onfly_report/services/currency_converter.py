"""Conversão de valores para BRL."""

from __future__ import annotations

from decimal import Decimal


def convert_to_brl(amount: Decimal, currency: str, rates: dict[str, Decimal]) -> Decimal:
    """
        Converte um valor na moeda informada para BRL usando a taxa da tabela.

        Correção: 
            De --> Decimal(str(float(amount) / float(rate)))  
            Para --> amount * rate
        Justificativa:
            A conversão dividia o valor pela taxa em vez de multiplicar por rate_to_brl e ainda 
            utilizava float na operação, violando a regra de usar Decimal nos cálculos financeiros.
        Referência: Linhas 76 e 93 das instruções no README 
    """
    rate = rates[currency]
    return amount * rate
