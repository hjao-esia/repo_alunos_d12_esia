# ADR 0001 — Divergências de `calcular_total` com R1.3 e R1.5

**Status:** aceita (21/10/2026). **Origem:** AV1.2 (golden master), AV1.3 (casos do contrato), AV2 (refatoração).

## Contexto
`caso/regras.md` é o contrato e vale mais que o código. Duas regras de R1 divergem do código atual de `caso/miniloja/calculo.py`:

- **R1.3** — frete grátis quando o subtotal com desconto é **maior ou igual** a R$ 200,00. O código usa `if total > 200:`. Ex.: 100 × 2, sem cupom, PE → contrato **210,00**; código 223,55.
- **R1.5** — arredondamento **meio para cima**. O código faz `round(total, 2)` sobre `float`. Ex. do próprio contrato: 2,00 × 1, PE → (2 + 12,90) × 1,05 = 15,645 → contrato **15,65**; código 15,64.

Na AV1.2, aplicar as duas correções e desfazê-las mostrou **46/384** divergências no golden master (24 na fronteira de R$ 200, 22 de meio centavo). `calcular_total` estava, e está na AV2, sob refatoração com igualdade exata ao golden master.

## Decisão
Não corrigir R1.3 nem R1.5 dentro de uma refatoração. A correção será uma **mudança de comportamento própria**, com escopo próprio e testes primeiro. Até lá, as divergências ficam documentadas na docstring de `calcular_total` e como `expectedFailure` em `caso/testes_existentes/test_calculo_contrato.py` (`test_frete_gratis_com_subtotal_exatamente_200` e `test_meio_centavo_arredonda_para_cima`).

## Consequências
- O golden master preserva o comportamento atual, **inclusive os erros**: prova ausência de mudança, não correção.
- Quando a correção vier: os dois `expectedFailure` passam a acusar *unexpected success* e devem virar testes normais; o golden master deve ser regravado de propósito (46 entradas mudam); `test_cenarios_gravados` precisa das chaves `limite_200` (210,00) e `vazio` (13,55) atualizadas; três mutantes de `testes/mutacao_manual.py` (`if total > 200:` ×2 e `return round(total, 2)`) deixam de se aplicar, porque buscam trechos literais.
- Mudar o tipo numérico para `Decimal` (necessário para R1.5) é uma decisão de projeto maior e deve ser revista na mesma mudança.

## Alternativa descartada
Manter `> 200` e ler o contrato como errado: não cabe, porque a regra não é ambígua e o contrato prevalece. Corrigir junto com a refatoração: descartado porque misturaria mudança de comportamento com refatoração e invalidaria o golden master como evidência.

## Rever quando
Uma nova versão do contrato alterar R1.3 ou R1.5, ou for aberta a mudança de comportamento que as corrige.
