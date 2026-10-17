# AGENTS.md — MiniLoja

- Python 3.11+, só biblioteca padrão; rode tudo da raiz do repositório.
- Verificações: `python -B testes/test_miniloja.py --codigo caso`; suíte existente: acrescente `--existentes`.
- Não altere `testes/` nem `caso/regras.md`; não ajuste valores esperados de testes para "fazer passar".
- O contrato (`caso/regras.md`) vale mais que o código. Em refatoração, divergência com o contrato é reportada, não corrigida.
- Antes de editar: declare o escopo (objetivo, pode tocar, não pode tocar, invariantes, pronto, parada) e apresente o plano.
- Refatorar `calcular_total` exige igualdade exata (`==`, sem tolerância) com `caso/dados/golden-master.json`.
- Não óbvio: `testes/mutacao_manual.py` muta `calculo.py` por trecho literal (ex.: `frete = 12.9`, `taxa = 0.05`); preserve esses literais.
