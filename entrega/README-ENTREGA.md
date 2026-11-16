# Entrega — Consolidador de reservas de hotel (Onfly)

CLI corrigido, testes fornecidos passando sem alteração e relatório conferido contra a amostra de
validação do `README.md`.

- **Defeitos encontrados e corrigidos:** 5
- **Testes:** 13 passando (5 fornecidos + 8 adicionais), 0 falhas
- **Amostra oficial:** relatório idêntico à tabela do enunciado, campo a campo
- **Arquivos de dados:** `data/reservas_hoteis.csv` e `data/taxas_cambio.csv` inalterados
- **Contrato do CLI e schema do relatório:** inalterados

## 1. Defeitos corrigidos

| # | Arquivo | De | Para |
|---|---|---|---|
| 1 | `repositories/csv_reservation_repository.py` | `if len(rows) == 200: break` | bloco removido |
| 2 | `services/status_policy.py` | `status != "CANCELLED"` | `status == "CONFIRMED"` |
| 3 | `services/stay_calculator.py` | `(checkout.day - checkin.day) * rooms` | `(checkout - checkin).days * rooms` |
| 4 | `services/currency_converter.py` | `Decimal(str(float(amount) / float(rate)))` | `amount * rate` |
| 5 | `services/report_builder.py` | `key=lambda item: (item[1]["amount"], item[0])` | `key=lambda item: (-item[1]["amount"], item[0])` |

### Causa raiz (uma frase por defeito)

1. **Truncamento da leitura** — a leitura interrompia o laço ao atingir 200 linhas, descartando em
   silêncio 100 das 300 reservas do arquivo.
2. **Política de faturamento** — o filtro excluía apenas `CANCELLED`, deixando `NO_SHOW` entrar em
   noites, valores, `by_month` e `top_hotels`, quando só `CONFIRMED` é faturável.
3. **Cálculo de noites** — subtraía os componentes dia-do-mês (`checkout.day - checkin.day`) em vez
   da diferença real de calendário, produzindo noites erradas (até negativas) em toda estadia que
   cruza virada de mês ou de ano.
4. **Conversão de câmbio** — dividia o valor pela taxa em vez de multiplicar por `rate_to_brl`, e
   ainda fazia a conta em `float`, violando a exigência de `Decimal` no dinheiro.
5. **Ordenação do ranking** — ordenava os hotéis por valor crescente, de modo que o corte dos
   `--top` primeiros devolvia justamente os hotéis de menor gasto.

## 2. Como investiguei

Comecei pelos testes fornecidos: cada falha apontava para uma regra específica do enunciado, então
usei as asserções como mapa (valor em BRL → câmbio, noites → cálculo de estadia, contagens →
política de status, ordem dos ids → ranking). A partir daí li cada módulo de `src/` confrontando-o
com a regra correspondente do `README.md`, em vez de ajustar o código até o teste ficar verde — o
objetivo era corrigir a causa, não compensar o sintoma.

O defeito do truncamento **não** era coberto pelos testes fornecidos: ele só aparece em arquivos com
mais de 200 linhas, e a amostra de validação tem 12. Encontrei-o lendo o repositório de leitura e
confirmei comparando a contagem do relatório (200) com as linhas do arquivo (300).

Depois das correções, fiz uma segunda varredura independente:

- **Reimplementação de conferência:** escrevi, fora do projeto, uma implementação própria das regras
  do enunciado e comparei o resultado com o do CLI nos dois datasets. Os relatórios coincidem em
  todos os campos.
- **Contratos do CLI:** exercitei 10 cenários de argumento e de entrada inválida (seção 5).
- **Testes de mutação:** para cada regra de negócio, quebrei a implementação de propósito e
  confirmei que o teste correspondente falha, restaurando o código em seguida. Serviu para verificar
  que os testes realmente protegem a regra, e não apenas acompanham o código.

### Evidência sobre exatidão monetária

No dataset de 300 reservas, a soma exata dos valores confirmados é `396169.99940000`, que serializa
como `"396170.00"`. Se o arredondamento acontecesse por reserva (antes da soma), o total sairia
`396169.99`. A diferença de um centavo confirma, na prática, que a soma é exata em `Decimal` e que o
arredondamento `ROUND_HALF_UP` só é aplicado na serialização.

## 3. Testes adicionais

Os testes fornecidos permanecem **inalterados**. Os adicionais ficam em arquivos próprios:

| Arquivo | O que protege |
|---|---|
| `tests/test_all_rows.py` | Leitura integral: 200 linhas (fronteira exata do antigo corte) e 201 linhas |
| `tests/test_extra_ranking.py` | Valor decrescente **e** desempate por `hotel_id` crescente |
| `tests/test_extra_dates.py` | Virada de ano: 3 noites atribuídas integralmente ao mês do check-in |
| `tests/test_extra_rooms.py` | Multiplicador de quartos: 3 noites × 2 quartos = 6 diárias |
| `tests/test_extra_regression.py` | Regressão integral sobre `data/exemplo-validacao.csv` |
| `tests/test_extra_rounding.py` | Média 100.005 → `"100.01"` (half-up, não half-even) |
| `tests/test_extra_empty_report.py` | Relatório zerado quando nada é faturável |

O teste de desempate cobre uma lacuna real: sob uma ordenação com `reverse=True` aplicado à chave
composta, o teste fornecido `test_top_hotels` continua passando (não há empates nele) enquanto o
adicional falha.

## 4. Como validar

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

No Windows (PowerShell), a variável de ambiente é definida antes do comando:

```powershell
$env:PYTHONPATH = "src"
python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

### Resultado do `pytest`

```
$ pytest -q
.............                                                            [100%]
13 passed
```

Detalhado:

```
tests/test_all_rows.py::test_reads_all_rows_beyond_200 PASSED
tests/test_all_rows.py::test_reads_exactly_200_rows PASSED
tests/test_currency.py::test_currency_conversion_to_brl PASSED
tests/test_extra_dates.py::test_nights_across_year_credit_to_checkin_month PASSED
tests/test_extra_empty_report.py::test_report_zeroed_when_no_billable_reservations PASSED
tests/test_extra_ranking.py::test_top_hotels_tie_breaks_by_hotel_id_ascending PASSED
tests/test_extra_regression.py::test_official_validation_sample_matches_expected_report PASSED
tests/test_extra_rooms.py::test_room_nights_multiply_by_rooms PASSED
tests/test_extra_rounding.py::test_average_rounds_half_up_on_serialization PASSED
tests/test_nights.py::test_nights_across_month_boundary PASSED
tests/test_regression_report.py::test_regression_report_on_sample PASSED
tests/test_status_rules.py::test_status_rules_exclude_cancelled_and_no_show PASSED
tests/test_top_hotels.py::test_top_hotels_are_ranked_descending PASSED
```

### Amostra de validação

Saída do CLI sobre `data/exemplo-validacao.csv` (`exit 0`):

```
Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00
```

O `output/exemplo.json` reproduz a tabela do enunciado integralmente: as 7 métricas de `summary`, os
2 registros de `by_month` (`2025-01` com 8 reservas, 25 noites e `"6684.00"`; `2025-02` com 1
reserva, 3 noites e `"882.00"`) e os 5 de `top_hotels`, na ordem `H01`, `H02`, `H12`, `H10`, `H09`,
com nomes, noites e valores iguais aos esperados. `generated_at` é dinâmico e, conforme o enunciado,
fica fora da comparação.

Sobre o dataset completo (`exit 0`):

```
Reservas: 300 | Confirmadas: 235 | Noites: 1347 | Total BRL: 396170.00
```

As contagens por status somam o total (235 + 31 + 34 = 300), o que confirma que nenhuma reserva é
perdida no caminho.

## 5. Contrato do CLI verificado

| Cenário | Código esperado | Obtido |
|---|---|---|
| Execução documentada no README | 0 | 0 |
| `--input` ou `--rates` ausente | 2 | 2 |
| Arquivo de entrada ou de câmbio inexistente | 2 | 2 |
| `--top 0`, `--top -1`, `--top abc` | 2 | 2 |
| Colunas obrigatórias ausentes no CSV | 2 | 2 |
| Data ou `amount` inválido | 2 | 2 |
| Tabela de câmbio vazia | 2 | 2 |
| Moeda sem taxa na tabela (fora do contrato de dados) | 1 | 1 |

`--output` omitido grava em `output/report.json`; diretórios inexistentes são criados, inclusive
aninhados. `--top` maior que a quantidade de hotéis devolve todos os hotéis, sem erro.

## 6. Decisões e escopo

- **Correções mínimas e localizadas.** Cada defeito foi corrigido no módulo responsável pela regra;
  não reorganizei a arquitetura, que já separa repositórios, serviços e orquestração de forma
  adequada ao problema.
- **Nenhuma dependência nova.** O CLI continua usando apenas a biblioteca padrão; `pytest` e `ruff`
  seguem sendo dependências só de desenvolvimento.
- **Os defeitos estão documentados no próprio código**, nas docstrings dos módulos corrigidos, com a
  justificativa de cada mudança.
- **Fora de escopo, por decisão consciente:** uma moeda ausente na tabela de câmbio hoje resulta em
  `exit 1` (erro inesperado) em vez de `2`; o enunciado garante que todas as moedas do dataset têm
  taxa, então preferi não adicionar validação não solicitada. Pelo mesmo motivo não validei
  `rooms >= 1` nem `checkout > checkin` — os dados fornecidos são consistentes nesses dois pontos
  (conferido: `rooms` entre 1 e 3, nenhum `checkout <= checkin`, nenhum id duplicado).

## 7. Uso de IA

Usei assistente de IA neste desafio. A ferramenta, o modelo e a divisão do trabalho estão em
`uso-de-ia/declaracao.md`; a exportação da sessão, no formato nativo da ferramenta, está em
`uso-de-ia/sessao.jsonl`.
