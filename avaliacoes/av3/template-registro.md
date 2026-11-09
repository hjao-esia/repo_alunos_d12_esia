# Registro individual — AV3

**Limite: três páginas + até duas de evidências.** Estudante: Heitor José Andrade de Oliveira — Data: 09/11/2026 — Caminho: **B (MiniLoja: B1, R4)**, branch `av3`

**Modo de interação usado e por quê (raio de impacto, oráculo, familiaridade):** ___ **Alternativa comparada:** ___

**Escopo declarado antes (seis campos, commitado antes de qualquer código):** objetivo: cumprir R4 em `get_pedido` (um usuário só vê os próprios pedidos), respondendo **404** com o mesmo corpo de "não encontrado" para pedido de outro usuário, para não revelar que o pedido existe; pode tocar: `caso/miniloja/handlers.py` (só `get_pedido`), criar `caso/testes_existentes/test_acesso.py` e este registro; não pode tocar: `testes/`, `caso/regras.md`, assinaturas públicas de `handlers`, demais módulos, testes existentes e os literais buscados por `testes/mutacao_manual.py` (`return 409,` em `handlers.py`); invariantes: 11/11 verificações, suíte existente verde, golden master 384/384, escore de mutação não cai; pronto quando: o teste negativo falha antes da correção e passa depois, com saída gravada, e a sabotagem (reverter a correção) o faz falhar de novo; pare e pergunte se: a correção exigir mudar assinatura, o repositório ou outro handler, ou aparecer outro acesso sem checagem de dono. **Cumprido? Como verifiquei (comando ou barreira):** ___

**Verificação:** teste que falharia sem a mudança ___; prova (execução antes e depois, sabotagem ou mutação) ___

| O que a IA errou (o quê, onde) | Como detectei | O que corrigi e por quê (causa e impacto) |
| --- | --- | --- |
| ___ |  |  |
| ___ |  |  |
| ___ |  |  |

**Dependências novas (se houver) e checagem:** ___

| Medição do meu time | Meu desenho |
| --- | --- |
| Pergunta e decisão | ___ |
| Métrica primária e guardrail | ___ |
| Baseline, período e método | ___ |
| Risco de manipulação e contramedida | ___ |
| Tarefa recorrente a automatizar e verificação exigida | ___ |

**Limites e condição para rever:** ___

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: ___; tarefa delegada e contexto: ___; trecho aproveitado: ___; minha verificação/intervenção: ___. O raciocínio e a decisão registrados são meus.

**Revisão:** [ ] modo; [ ] escopo; [ ] verificação; [ ] erros da IA; [ ] medição e automação; [ ] procedência.
