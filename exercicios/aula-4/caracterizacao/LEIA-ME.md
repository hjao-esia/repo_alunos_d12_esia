# Caracterização mínima — AV1.4

Gravada **antes de qualquer mudança** no legado, em 23/10/2026, com a branch `aula-4` no commit 753c616 (merge de `upstream/bloco4_legado`). Python 3.12.10, Windows 11, Git Bash, sem rede.

## Comandos (a partir de `caso/legado/`, banco vazio)

```
CIENTO_OFFLINE=1 python -B -m cienciometria.jobs ingest       # 120 trabalhos
CIENTO_OFFLINE=1 python -B -m cienciometria.jobs enriquecer   # 30 autores
CIENTO_OFFLINE=1 PYTHONIOENCODING=utf-8 python -B -m cienciometria.jobs relatorio top_instituicoes
CIENTO_OFFLINE=1 PYTHONIOENCODING=utf-8 python -B -m cienciometria.jobs relatorio evolucao_anual
```

Saídas: [preparo.txt](preparo.txt), [top_instituicoes.txt](top_instituicoes.txt), [evolucao_anual.txt](evolucao_anual.txt).

- `PYTHONIOENCODING=utf-8`: sem ele, no Windows, a saída redirecionada sai em cp1252 e os acentos quebram ao comparar. Só a codificação muda; o conteúdo é o mesmo.
- Escolhi relatórios **só de leitura**: `exporta_parceiro` também escreve em `trabalhos` (`cienciometria/exporta_parceiro.py:11`).
- **Fragilidade:** `top_instituicoes` tem empate (64 × 64) e o SQL ordena só pela contagem (`cienciometria/relatorios.py:11`). A ordem das duas primeiras linhas não é garantida, então a comparação deve aceitar troca entre linhas empatadas ou ordenar também pelo nome.
- `evolucao_anual` mostra `ano = 0` (2 trabalhos: W9000007 e W9000077). No cron, `scripts/corrigir_anos.sql` os anula **antes** dos relatórios, então a saída do cron não teria essa linha.

## Experimentos que mudam dados (cópia descartável no scratchpad, não no repositório)

| Experimento | Resultado observado |
| --- | --- |
| `CIENTO_AMBIENT=prod` (nome usado em `scripts/rodar_tudo.sh:3`) | `ambiente()` = `dev`, `parceiro_pasta` = `saida_parceiro`, `limite_paginas` = 50 |
| `CIENTO_AMBIENTE=prod` (nome lido em `cienciometria/config.py:11`) | `prod`, `/mnt/compartilhado/parceiro`, 500 |
| `relatorio exporta_parceiro` | CSV gerado; `exportado = 1` em 120/120 trabalhos |
| `refresh` sem rede, logo depois | funciona com o cache (41 trabalhos); `exportado = 1` cai para 79: 2022–2023 e os de ano 0 voltam a 0 (`INSERT OR REPLACE`, `cienciometria/ingest.py:17`) |
| `sql scripts/corrigir_anos.sql` | W9000007 e W9000077 passam a `ano = NULL` |
| `relatorio` sem nome | `TypeError` (concatena `None` em `cienciometria/relatorios.py:43`), não o `ValueError` previsto |
| `relatorio conceitos` | `ValueError: relatório desabilitado: conceitos` |
