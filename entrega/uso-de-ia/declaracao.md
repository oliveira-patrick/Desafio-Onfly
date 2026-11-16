# Declaração de uso de IA

Usei assistente de IA neste desafio. Abaixo estão a ferramenta, o modelo e a divisão do trabalho
entre mim e a IA.

## Ferramenta e modelo

| Item | Valor |
|---|---|
| Ferramenta | Claude Code (Anthropic), aplicativo desktop |
| Modelo | Claude Opus 5 |
| Sessão registrada | Auditoria independente e testes adicionais — 15 de novembro de 2026 |
| Exportação | `sessao.jsonl` nesta pasta (formato nativo do Claude Code) |

### Sobre a exportação

`sessao.jsonl` é a exportação nativa da sessão, com o conteúdo integral da conversa. Antes de
incluí-la aqui, substituí cinco categorias de dado sem relação com o desafio, que não devem ir para
um repositório público: meu endereço de e-mail (`<email-removido>`), o nome de usuário do Windows
nos caminhos de arquivo (`<usuario>`), os nomes de diretório de outros projetos meus, que
apareceram em uma listagem de pastas durante a sessão (`<outro-projeto>`), a variável `PATH` da
minha máquina, que lista o software instalado e apareceu na saída de uma verificação de versão do
Python (`<path-removido>`), e o identificador da minha organização na ferramenta
(`<org-uuid-removido>`). Nenhuma mensagem, decisão técnica ou saída de comando relacionada ao
desafio foi alterada ou removida.

## O que eu fiz

1. **Investiguei e diagnostiquei os 5 defeitos do CLI**, partindo das falhas dos testes fornecidos e
   confrontando cada módulo de `src/` com a regra correspondente do `README.md`.
2. **Implementei todas as correções de código de produção.** As cinco mudanças em `src/`
   (truncamento da leitura, política de status, cálculo de noites, conversão de câmbio e ordenação
   do ranking) são minhas, incluindo as docstrings que registram causa e justificativa de cada uma.
3. **Escrevi o teste `tests/test_all_rows.py`**, que cobre a leitura integral do arquivo — o defeito
   do truncamento não era alcançado por nenhum teste fornecido.
4. **Defini o escopo e a especificação da segunda varredura:** quais grupos de requisitos auditar,
   quais seis testes adicionais implementar e, para cada um deles, os dados de entrada, os valores
   esperados e o comportamento a proteger.
5. **Revisei e decidi** o que entrava na entrega: aceitei a remoção dos meus lembretes de
   desenvolvimento nas docstrings e dispensei as melhorias opcionais apontadas pela auditoria, por
   serem validações não exigidas pelo enunciado.

## O que a IA fez

Nesta sessão, sob a especificação descrita acima:

1. **Auditoria independente da implementação**, sem partir das minhas conclusões: leitura do
   `README.md`, de todos os módulos de `src/`, dos testes e dos CSVs; execução da suíte original;
   verificação dos códigos de saída em 10 cenários de argumento e de entrada inválida; e comparação
   byte a byte da árvore entregue com o pacote original do desafio, para isolar exatamente o que foi
   alterado.
2. **Conferência por reimplementação independente:** escreveu, fora do projeto, uma implementação
   própria das regras do enunciado e comparou o resultado com o do CLI na amostra de validação e no
   dataset de 300 reservas. Os relatórios coincidem em todos os campos.
3. **Implementou os seis testes adicionais** em `tests/test_extra_*.py`, conforme a especificação de
   dados e valores esperados que eu defini.
4. **Provou a efetividade dos testes por mutação:** quebrou a implementação de propósito sete vezes
   (desempate invertido, noites no mês do check-out, multiplicador de quartos removido,
   arredondamento half-even, não faturáveis nas agregações, câmbio dividindo em `float` e corte em
   200 linhas reinstalado), confirmou que o teste correspondente falha em cada caso e restaurou o
   código, conferindo o MD5 dos arquivos a cada ciclo.
5. **Redigiu o `entrega/README-ENTREGA.md` e esta declaração**, a partir das evidências coletadas.
6. **Removeu, a meu pedido, os lembretes `(Revisitar na entrega)`** que eu havia deixado nas
   docstrings durante o desenvolvimento.

## Limites do uso de IA nesta entrega

- **A IA não alterou a lógica de produção.** A única alteração que fez em `src/` nesta sessão foi
  textual: a remoção do lembrete em uma linha de docstring. Os cinco arquivos corrigidos continuam
  byte a byte como eu os entreguei, exceto essa linha.
- **A IA não modificou os testes fornecidos** nem os arquivos de `data/`. Isso foi verificado por
  comparação byte a byte com o pacote original.
- **A auditoria concluiu sem divergências em relação ao enunciado**, portanto nenhuma correção
  adicional foi necessária e nenhuma foi feita pela IA.
- **Escopo da verificação de ambiente:** a execução em Python 3.11 foi conferida por mim antes desta
  sessão; o ambiente usado aqui tem Python 3.13.5, então a suíte e o CLI desta auditoria rodaram na
  3.13. O código não usa recursos posteriores à 3.11.
- Todo o resultado produzido pela IA foi revisado por mim antes de entrar na entrega.
