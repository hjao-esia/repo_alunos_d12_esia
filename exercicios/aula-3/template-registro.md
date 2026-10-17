# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.** Estudante: Heitor José Andrade de Oliveira — Data: 17/10/2026
Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: **execução própria**.

| Teste suspeito | Tipo de tautologia | Sabotagem que apliquei (ou raciocínio) | Continuou verde? |
| --- | --- | --- | --- |
| `test_calculo::test_cupom_natal_com_flag` | sem asserção real (`assertIsNotNone`) | mutante `total * 0.8` → `0.79` (NATAL 21%) | **Sim**: sobreviveu |
| `test_calculo::test_cenarios_gravados` | snapshot do próprio código | grava `limite_200` = 223,55; pela R1.3, 100 × 2 em PE tem frete grátis: 200 × 1,05 = **210,00**. O mutante `> 200` → `>= 200` (que aproxima o código do contrato) é morto por ele | **Não**, mas pelo motivo errado: falhou com o código corrigido segundo a R1.3, porque espera 223,55 (o valor com o bug) |
| `test_pedidos::test_criar_pedido` | super-mockado / afirma o mock | repositório, estoque e gateway são `MagicMock`; o teste só confere `repo.salvar.called`. Mutante `"total_fmt": moeda(total)` → `moeda(0)` | **Sim**: sobreviveu |

| Mutante sobrevivente | Por que sobreviveu | Teste que o mataria (ou "equivalente", com justificativa) |
| --- | --- | --- |
| frete RJ `21.5` → `22.5` | nenhum teste calcula total no RJ abaixo de R$ 200 (o do RJ usa `FRETEGRATIS`) | `test_frete_rj_abaixo_de_200`: 40 × 1, RJ → (40 + 21,50) × 1,06 = **65,19**. Mutante daria 66,25. **Morto** |
| estoque `disponivel < qtd` → `<=` | falta o teste de borda (pedir exatamente o saldo) | `test_reservar_exatamente_o_saldo`: saldo 3, reservar 3 → não levanta e o saldo fica **0** (R2.2). **Morto** |
| `desconto_aplicado = True` → `False` | **equivalente**: a variável só é lida em `if desconto_aplicado: pass`, sem efeito observável | nenhum teste pode matá-lo; remover o código morto é a saída, fora do escopo deste bloco |

Também acrescentei testes para NATAL (106,89), VIP15 em `descontos.py` (170,00), `total_fmt` ("R$ 31,99") e o arredondamento do relatório ("R$ 11,11"): os 6 sobreviventes não equivalentes morreram.

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão) | Observado no código | Decisão |
| --- | --- | --- | --- |
| 100 × 2, sem cupom, PE (fronteira do frete) | subtotal 200 ≥ 200 → frete 0; 200 × 1,05 = **210,00** | 223,55 | **bug: código diverge** de R1.3: usa `> 200`; R1.3 diz "maior ou igual" |
| 2,00 × 1, sem cupom, PE (arredondamento) | (2 + 12,90) × 1,05 = 15,645 → meio para cima **15,65** (exemplo da R1.5) | 15,64 | **bug: código diverge** de R1.5: `round()` sobre `float` não arredonda meio para cima |
| 220 × 1, `PROMO10`, SP (desconto abaixo do limite) | 198 < 200 → paga frete; (198 + 19,90) × 1,07 = 233,153 → **233,15** | 233,15 | concordam: o limite é aplicado sobre o subtotal com desconto |

**ADR curto:** contexto: R1.3 exige frete grátis com subtotal com desconto ≥ R$ 200, o código usa `> 200`, e `test_cenarios_gravados` e o golden master da AV1.2 gravaram 223,55; decisão: o contrato prevalece (a regra não é ambígua), a correção de R1.3 e R1.5 será feita numa mudança de comportamento separada, testes primeiro; consequências: regravar o golden master e as chaves `limite_200` (210,00) e `vazio` (13,55) de `test_cenarios_gravados`, e 3 mutantes de `testes/mutacao_manual.py` (`if total > 200:` ×2 e `round(total, 2)`) deixam de se aplicar; alternativa descartada: manter `> 200` e ler o contrato como errado, o que não cabe porque `regras.md` vale mais que o código.

**Trecho essencial de evidência:** `python -B testes/mutacao_manual.py calculo.py descontos.py estoque.py formatacao.py pedidos.py relatorios.py handlers.py` (30 de 31 mutantes: o de `cadastro.py` procura um trecho que não existe desde a AV1.1) antes → `Mutantes: 30 | mortos: 23 | sobreviventes: 7 | escore: 77%`; depois dos 6 testes → `Mutantes: 30 | mortos: 29 | sobreviventes: 1 | escore: 97%` (sobra o equivalente); `--existentes` → `Ran 32 tests ... OK`; verificações → `Ran 11 tests ... OK`; `caso/miniloja/` não foi alterado. **Limite do que a suíte garante e condição para rever a decisão:** a suíte continua sem cobrir a fronteira de R$ 200 e os valores de meio centavo (806 entradas simples divergem do contrato no arredondamento), porque esses testes ficariam vermelhos contra o código atual; os novos testes usam entradas fora dessas fronteiras. Escore de mutação mede só os 30 operadores escolhidos, não a correção. O formato "R$ 0,00" de `total_fmt` não está no contrato (veio de `formatar_moeda`). Revejo o ADR se uma nova versão do contrato mudar R1.3/R1.5.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Claude Opus 5.5 (`claude-opus-5-5`); tarefa delegada e contexto: rodar a mutação e diagnosticar as falhas, propor plano, calcular os casos do contrato e escrever os 6 testes com escopo declarado (só acrescentar em `caso/testes_existentes/`); trecho aproveitado: os 6 testes integrais; minha verificação/intervenção: decidi manter 30 mutantes em vez de alterar `cadastro.py` para a ferramenta, dispensei a cópia de trabalho, pedi os testes na suíte (e não só descritos) e adiei a correção de R1.3/R1.5 para mudança separada. O raciocínio e a decisão registrados são meus.

**Revisão:** [X] três testes; [X] dois mutantes; [X] três casos do contrato; [X] ADR; [X] até uma página.
