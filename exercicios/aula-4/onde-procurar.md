# AV1.4 — Passo 0: onde eu procuraria cada resposta

**Procedência:** escrito pelo assistente (Claude Code, Opus 5.5) **depois** de já ter lido o código de `caso/legado/` (exceto o README). Portanto não é uma hipótese "às cegas": registra a estratégia de busca, não uma previsão independente.

| # | Pergunta | Onde procurar primeiro | Busca que derrubaria a resposta |
| --- | --- | --- | --- |
| 1 | Onde começa a ingestão e quais caminhos a disparam? | Ponto de entrada da CLI (`cienciometria/jobs.py`), o agendamento (`scripts/rodar_tudo.sh`) e o módulo `ingest.py` | Chamadas a `ingest.run` fora do comando `ingest` (grep `ingest.run`) |
| 2 | Quem escreve na tabela `trabalhos`? | `INSERT`/`UPDATE`/`DELETE` em `.py` **e** em `.sql`; o comando que executa SQL arbitrário | grep `trabalhos` em todos os arquivos, inclusive `scripts/` e funções de relatório |
| 3 | Como classifica trabalhos e autores por área, e do que depende da API? | `ingest.py` (filtro e campos lidos do JSON), `instituicoes.py`, `conceitos.py`; um JSON do `.cache/` para ver o formato real | Campos da API usados no código × documentação atual do OpenAlex |
| 4 | Que relatórios existem e quem os dispara? | `relatorios.py`, lista de habilitados em `config.ini`, cron | Despacho dinâmico (`getattr`/nome montado em string): grep pelo nome da função não basta |
| 5 | Que configurações mudam por ambiente, e qual vale no agendamento? | `config.py` (como o ambiente é escolhido), seções do `config.ini`, variáveis exportadas no cron | Comparar, letra por letra, o nome da variável lida no código com o nome exportado no script; procurar chaves do `.ini` que nunca são lidas |
