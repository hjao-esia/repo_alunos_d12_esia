# Registro individual — AV2

**Limite: duas páginas de análise + anexo técnico curto.** Estudante: Heitor José Andrade de Oliveira — Data: 21/10/2026 — Caminho: **B (MiniLoja)**, branch `av2`

**Escopo (seis campos, escritos antes da mudança):** objetivo: remover o código morto `desconto_aplicado` de `calcular_total` sem mudar comportamento e entregar uma suíte de contrato de R1 com prova de que falharia; pode tocar: `caso/miniloja/calculo.py`, criar `caso/golden_master.py`, `caso/testes_existentes/test_calculo_contrato.py`, `caso/adr/0001-divergencias-r13-r15.md` e este registro; não pode tocar: `testes/`, `caso/regras.md`, assinatura de `calcular_total`, `golden-master.json`, testes existentes, demais módulos e os literais buscados pelos mutantes (`frete = 12.9`, `taxa = 0.05`, `if total > 200:`…); invariantes: 384/384 iguais ao golden master por `==`, 11/11 verificações, suíte existente verde; pronto quando: tudo verde e cada teste novo com sabotagem registrada; pare e pergunte se: a remoção exigir mudar a ordem das operações em `float` ou aparecer divergência nova com o contrato (R1.3 e R1.5 já conhecidas: reportar, não corrigir).
**Plano do agente: o que cortei ou corrigi:** o agente ofereceu três refatorações. **Cortei** trocar os `if/elif` de frete e taxa pelos dicts `FRETE_POR_UF`/`TAXA_POR_UF` (já definidos e não usados): o código ficaria melhor, mas quebraria 8 mutantes de `testes/mutacao_manual.py`, que busca trechos literais e não pode ser alterado. **Cortei** apenas reaproveitar a extração da AV1.2, porque não fecharia a lacuna deixada na AV1.3 (o mutante equivalente). Escolhi remover o código morto, que eu tinha adiado na AV1.2 e na AV1.3 por estar fora do escopo daqueles blocos. Mantive fora do escopo corrigir R1.3/R1.5 (ver ADR).

**Comportamento preservado:** método: golden master de **384** entradas gravado na AV1.2 antes de qualquer refatoração (8 carrinhos × 6 cupons × 4 UFs × flag NATAL), agora com script versionado `caso/golden_master.py`, que compara por `==` sem tolerância, lista os `id` divergentes e sai com 1. Resultado: antes da mudança (commit `18a352a`) → `384/384 iguais`, saída 0; depois (`df7041b`) → `384/384 iguais`, saída 0. Verificações → `Ran 11 tests ... OK`; suíte existente → `Ran 32 tests ... OK`. A mudança: `_aplicar_desconto` devolve só `total`; saíram `desconto_aplicado` e o `if desconto_aplicado: pass`. Literais e ordem das operações em `float` mantidos.

| Teste (derivado de qual regra do contrato) | Como provei que falharia (sabotagem, mutação ou diferencial) | Resultado |
| --- | --- | --- |
| `test_subtotal_soma_preco_vezes_quantidade` (R1.1): 10×3 + 25×2, SP → 106,89 | mutante `preco * qtd` → `preco + qtd` | falha (e mais 12 testes) |
| `test_natal_sem_campanha_nao_desconta` (R1.2, flag desligada) → 128,79 | sabotagem manual: NATAL ignora a flag (a ferramenta não tem esse mutante) | falha **sozinho** |
| `test_cupom_desconhecido_e_ignorado` (R1.2) → 128,79 | sabotagem manual: cupom desconhecido aplica 10% | falha |
| `test_limite_usa_subtotal_com_desconto_abaixo` (R1.3 + R1.6): 220 + PROMO10, SP → 233,15 | sabotagem manual: frete decidido sobre o subtotal **sem** desconto | falha **sozinho** |
| `test_frete_por_uf_abaixo_de_200` (R1.3), 4 UFs | mutantes de frete PE, SP, RJ e UF desconhecida | falha nos 4 |
| `test_taxa_por_uf_sobre_valor_sem_frete` (R1.4): FRETEGRATIS isola a taxa | mutantes de taxa PE/SP/RJ/demais | falha nos 4 |
| `test_frete_gratis_com_subtotal_exatamente_200` (R1.3), `expectedFailure` | mutante `> 200` → `>= 200` (o que corrige o código) | acusa *unexpected success*: o teste avisa quando a divergência for corrigida |

Resumo: **só o arquivo novo** (15 testes, 13 ok + 2 `expectedFailure`) mata **17/17** mutantes aplicáveis de `calculo.py` e **4/4** sabotagens manuais (flag NATAL, cupom desconhecido, frete antes do desconto, taxa antes do frete). Todos os esperados foram calculados a partir de `regras.md` com `Decimal` e meio para cima, sem importar o código. Escolhi entradas sem meio centavo: com PE e subtotal inteiro, (n + 12,90) × 1,05 sempre termina em meio centavo, então usei 37,50.

**Mutantes sobreviventes e tratamento:** antes: `mutacao_manual.py calculo.py` → `Mutantes: 18 | mortos: 17 | sobreviventes: 1 | escore: 94%`; o sobrevivente era o equivalente `desconto_aplicado = True → False`. Tratamento: **removi o código que o gerava**, em vez de só justificá-lo. Depois: 17 mutantes, **17 mortos, 100%**. Como a ferramenta não pula mutante inaplicável, rodei-a numa cópia do repositório com só essa linha retirada da lista (`testes/` do repositório intacto).
**Documentação (contrato e motivo) ou ADR:** docstring de `calcular_total`: R1 com a ordem (R1.6) e **por que** `> 200` e `round()` ficaram (refatoração com igualdade exata ao golden master). ADR `caso/adr/0001-divergencias-r13-r15.md`: contexto com os números da AV1.2 (46/384 divergências), decisão (corrigir numa mudança de comportamento própria), consequências concretas (dois `expectedFailure` viram testes normais, regravar o golden master e `test_cenarios_gravados`, três mutantes deixam de se aplicar, troca para `Decimal`) e alternativa descartada. `AGENTS.md` ganhou o comando do golden master.
**O que a IA errou (o quê, onde, como detectei):** (1) **no plano**, previu que, removido o código morto, a ferramenta de mutação rodaria "17 mutantes"; na verdade `testes/mutacao_manual.py:76` faz `assert velho in original` e **aborta** a execução inteira (`AssertionError: trecho não encontrado em calculo.py: 'desconto_aplicado = True'`). Detectei rodando a ferramenta logo após a refatoração; contornei com a cópia descrita acima. (2) **No escopo**, o plano mandava atualizar `AGENTS.md` no passo 5, mas o campo "pode tocar" não o listava. Detectei ao revisar o diff contra os seis campos; aceitei a mudança de uma linha e registro aqui a inconsistência.
**Limite da verificação e condição para rever:** o golden master cobre só as 384 entradas escolhidas e preserva os erros: prova ausência de mudança, não correção. O escore de mutação mede só os 17 operadores da ferramenta mais as 4 sabotagens que escolhi. A suíte não verifica tipos de entrada inválidos (preço negativo, `qtd` zero), que o contrato não define. A prova por teste depende de scripts que ficaram no meu ambiente; outra pessoa a repete aplicando as mesmas sabotagens à mão (listadas acima). Revejo a decisão se o contrato mudar R1.3/R1.5, ou quando a correção for aberta: aí os `expectedFailure` viram testes normais.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Claude Opus 5.5 (`claude-opus-5-5`); tarefa delegada e contexto: montar o plano da AV2 a partir do enunciado, da rubrica e dos meus registros AV1.2/AV1.3; escrever o script do golden master, a refatoração, os 15 testes, os scripts de sabotagem e o ADR; contexto: `CLAUDE.md`, `AGENTS.md` e `caso/regras.md`; trecho aproveitado: script, refatoração, testes e ADR integrais; minha verificação/intervenção: escolhi o Caminho B e a refatoração (remover o código morto), cortei a troca pelos dicts, conferi os esperados contra o contrato, rodei golden master, verificações, suíte e mutação antes e depois, e revisei o diff contra o escopo. O raciocínio e a decisão registrados são meus.

**Anexo — diff (`git diff --numstat main...av2`):** `caso/miniloja/calculo.py` +26/−30 · `caso/golden_master.py` +49 · `caso/testes_existentes/test_calculo_contrato.py` +104 · `caso/adr/0001-divergencias-r13-r15.md` +25 · `AGENTS.md` +1/−1. Commits: `18a352a` (golden master), `df7041b` (refatoração), `10af2f7` (testes), `52d2805` (ADR).

**Como repetir (da raiz):**
```
python -B caso/golden_master.py                                   # 384/384 iguais
python -B testes/test_miniloja.py --codigo caso                   # Ran 11 tests ... OK
python -B testes/test_miniloja.py --codigo caso --existentes      # Ran 47 tests ... OK (expected failures=2)
```
Sabotagem: em `caso/miniloja/calculo.py`, troque `elif cupom == "NATAL" and flags.promo_natal_ativa():` por `elif cupom == "NATAL":` e rode a suíte existente → `test_natal_sem_campanha_nao_desconta` falha; desfaça com `git checkout caso/miniloja/calculo.py`.

**Trecho dos testes:**
```python
def test_limite_usa_subtotal_com_desconto_abaixo(self):
    # 220 × 0,9 = 198 < 200 → paga frete; (198 + 19,90) × 1,07 = 233,153
    self.assertEqual(calcular_total([item(220.0)], "PROMO10", "SP"), 233.15)

@unittest.expectedFailure
def test_meio_centavo_arredonda_para_cima(self):
    # Exemplo da R1.5: (2 + 12,90) × 1,05 = 15,645 → 15,65. O código dá 15,64 (ADR 0001).
    self.assertEqual(calcular_total([item(2.0)], None, "PE"), 15.65)
```
**Revisão:** [X] escopo; [X] comportamento; [X] testes com prova; [X] documentação; [X] erros da IA; [X] limite.
