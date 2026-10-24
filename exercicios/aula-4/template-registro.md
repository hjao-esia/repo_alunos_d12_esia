# Registro individual — AV1.4

**Limite: uma página, incluindo evidências essenciais.** Estudante: Heitor José Andrade de Oliveira — Data: 23/10/2026
Origem: Caminhos relativos a `caso/legado/`.

| # | Afirmação | Trecho (arquivo:linha) | Contraevidência buscada | Status |
| --- | --- | --- | --- | --- |
| 1 | A ingestão começa em `ingest.run`, disparada pelos comandos `ingest` **e** `refresh` (o cron chama os dois). | `cienciometria/ingest.py:43`; `cienciometria/jobs.py:22-23`, `:10`, `:28-29`; `scripts/rodar_tudo.sh:6`, `:11` | grep `ingest.run`: só `jobs.py:10` e `:23`. "Só o comando `ingest` ingere" fica refutada. | confirmada |
| 2 | Quatro pontos escrevem em `trabalhos`: a ingestão, o refresh, **um relatório** e um SQL do cron. | `cienciometria/ingest.py:17`; `cienciometria/jobs.py:12`; `cienciometria/exporta_parceiro.py:11`; `scripts/corrigir_anos.sql:2` via `cienciometria/jobs.py:30-32` | grep `trabalhos` em `.py` e `.sql`. Executado: o refresh volta `exportado` a 0 (120→79) por causa do `INSERT OR REPLACE`. O comando `sql` aceita qualquer script, então a lista só vale para o repositório. | confirmada (lista mínima) |
| 3 | A área vem de **Concepts**: trabalhos por filtro `concepts.id` e `concepts[0]`; autores por `x_concepts` nível 0 de maior score; instituição atual por `last_known_institution`. | `cienciometria/ingest.py:7`, `:15`, `:36-39`; `cienciometria/instituicoes.py:10`, `:21-26`; `cienciometria/conceitos.py:20-26` | Documentação do OpenAlex (23/10/2026): Concepts congelados (trocar por Topics), `x_concepts` a ser removido, `last_known_institution` trocado por `last_known_institutions[0]`. | confirmada no código; efeito na API real **incerto** (cache fictício) |
| 4 | Há 5 relatórios `rel_*`, chamados por `getattr` e filtrados por `[relatorios] habilitados`; o cron dispara só `top_instituicoes` e `exporta_parceiro`. | `cienciometria/relatorios.py:7-45` (despacho em `:44`); `config.ini:21`; `scripts/rodar_tudo.sh:9-10` | grep `rel_conceitos` só acha a definição ("nunca chamado"?), mas o despacho é dinâmico. Executado: `relatorio conceitos` dá "desabilitado"; existe, mas está fora da config. | confirmada |
| 5 | `prod` sobrescreve 3 chaves via `CIENTO_AMBIENTE`, mas **o cron roda como dev**: exporta `CIENTO_AMBIENT` (sem o E). `por_pagina` nunca é lido. | `cienciometria/config.py:10-17`; `config.ini:15-18`; `scripts/rodar_tudo.sh:3`; `config.ini:6` × `cienciometria/ingest.py:8` | Executado com a variável do cron: `dev`, `saida_parceiro`, 50 páginas. Com `CIENTO_AMBIENTE`: `prod`, `/mnt/compartilhado/parceiro`, 500. | confirmada |

**Resposta do assistente que parecia certa e estava errada:** "`relatorio` sem nome levanta `ValueError: relatório desabilitado`" (`None not in habilitados` é verdadeiro). **Como refutei:** executei o comando, que deu `TypeError`: a mensagem concatena `None` em `cienciometria/relatorios.py:43` antes do `raise`.

**Caracterização antes de mudar (comando e saída gravada):** `CIENTO_OFFLINE=1 python -B -m cienciometria.jobs ingest|enriquecer` (120 trabalhos, 30 autores), depois `... relatorio top_instituicoes` e `... relatorio evolucao_anual`, com saídas em `exercicios/aula-4/caracterizacao/`. Ressalvas: empate 64×64 sem desempate no SQL; linha de ano 0 que o cron anularia.

| Fatia do plano | Mudança | Mecânica (codemod) ou decisão humana? | Verificação da fatia |
| --- | --- | --- | --- |
| 1 | Chave de API (o `mailto` é ignorado desde 02/2026; o cursor sem chave dá 401 após a 1ª página), enviada no header `Authorization` para não mudar a URL nem o hash do cache | Mecânica; **decisão** sobre onde guardar a chave | Saídas gravadas idênticas, offline |
| 2 | `per-page: 200` passa a `per_page` lido de `por_pagina` (máx. 100) | Codemod; **decisão** sobre `limite_paginas` (o dobro de páginas) | Mesmo total de trabalhos, com cache novo |
| 3 | `last_known_institution` passa a `last_known_institutions[0]` | Codemod; **decisão** quando há várias instituições | `top_instituicoes` e `areas_autores` iguais |
| 4 | Concepts passam a Topics: filtro `topics.id`, `primary_topic` no lugar de `concepts[0]`, ID `conceito_padrao` (C→T), `nivel_minimo` (6 níveis → 4) | **Decisão humana**: taxonomias sem mapeamento 1:1 | Contagens antes/depois, cada diferença explicada |
| 5 | Área do autor: `x_concepts` nível 0 passa a domain/field via Topics | **Decisão humana** | `areas_autores` comparado e justificado |

Invariante de todas as fatias: colunas do CSV do parceiro (`cienciometria/exporta_parceiro.py:7`). As fatias 2–5 mudam URLs e exigem cache novo (rede + chave). O erro do `CIENTO_AMBIENT` fica fora do escopo: corrigir passa a gravar em `/mnt/compartilhado`, decisão de quem mantém o sistema.

**Limite da leitura e condição para reabrir uma resposta:** os dados e o cache são fictícios. Não vi o crontab real nem consumidores externos do banco ou do CSV, e o comando `sql` e o `getattr` permitem caminhos que o grep não enxerga. Reabro a 2 se surgir outro `.sql` ou acesso direto ao SQLite; a 4 se `habilitados` mudar; a 5 se o cron real definir `CIENTO_AMBIENTE`. O `UPDATE` de citações negativas (`cienciometria/jobs.py:12`) não pôde ser observado (não há casos nos dados). O `README.md` (de 2023), lido só depois das respostas, está desatualizado: diz que a API "não precisa de chave" e recomenda o "polite pool" (`README.md:10-11`), o que a documentação atual refuta, e manda instalar `requests`, que o código não importa.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Opus 5.5 (`claude-opus-5-5`); tarefa delegada e contexto: ler o legado (sem o README), responder com trecho, rodar a caracterização e os experimentos numa cópia descartável, consultar a documentação do OpenAlex e redigir este registro; trecho aproveitado: tabelas e plano; minha verificação/intervenção: pedi a IA um varredura do repo legado e analise de cada item, aprovei cada etapa. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] cinco respostas com trecho; [x] uma refutação; [x] caracterização; [x] plano em fatias; [X] até uma página.
