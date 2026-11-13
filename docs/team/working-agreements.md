# Acordos de Trabalho da Equipe (Working Agreements) — Atlas Santos

Este documento formaliza as regras de colaboração adotadas pelos **cinco integrantes da equipe de desenvolvimento do Atlas Santos**, visando garantir previsibilidade, alta qualidade de código e integração contínua sem depender de convenções informais.

---

## 1. Responsabilidade por Issues

1. **Atribuição Clara**: Toda atividade técnica deve estar vinculada a uma Issue aberta no GitHub com template preenchido (`[FEAT]` ou `[BUG]`).
2. **Um Responsável por Vez (Assignee)**: Cada Issue em desenvolvimento deve ter um único desenvolvedor primário responsável pela entrega, evitando dispersão ou sobreposição de esforços.
3. **Limite de Trabalho em Andamento (WIP Limit)**: Cada desenvolvedor deve manter no máximo **1 Issue em desenvolvimento ativo** e **1 em fase de revisão/ajustes**.
4. **Atualização Diária de Status**: O progresso deve ser refletido nas colunas do quadro do GitHub Projects (*Todo*, *In Progress*, *In Review*, *Done*).

---

## 2. Revisão Cruzada Obrigatória (Peer Review)

1. **Nenhum Código Entra Sem Revisão**: Nenhum Pull Request pode ser integrado à branch `main` ou `develop` sem aprovação de **pelo menos um outro colega da equipe**.
2. **Critérios de Revisão**:
   - Respeito às fronteiras de domínio (routers não devem concentrar regras de negócio; módulos não devem importar modelos privados de outros domínios).
   - Ausência de credenciais, tokens ou dados pessoais reais.
   - Presença e sucesso dos testes unitários e de integração correspondentes.
   - Clareza e objetividade das mensagens de commit seguindo *Conventional Commits*.
3. **Tempo de Resposta (SLA de Code Review)**: A equipe prioriza revisar PRs pendentes em no máximo **4 horas úteis** após a solicitação, evitando que colegas fiquem bloqueados.

---

## 3. Comunicação Proativa de Bloqueios

1. **Sinalização Imediata**: Caso um integrante enfrente um bloqueio técnico ou dependência pendente por mais de **1 hora**, deve comunicar imediatamente o time no canal oficial com a etiqueta `[BLOQUEIO]`.
2. **Dependência de Decisões Institucionais (D-01 a D-10)**: Quando a dúvida decorrer de uma das dez decisões pendentes do projeto (ex: política de cotas de fotos rejeitadas em D-02 ou parâmetros pedagógicos em D-06), a equipe técnica deve documentar a hipótese adotada de forma configurável e consultar o responsável indicado no documento de requisitos.
3. **Pair Programming em Casos Críticos**: Diante de problemas complexos de integração (ex: transações atômicas de upload ou renderização de percursos cartográficos), adota-se sessão de programação em pares para resolução rápida.

---

## 4. Decisões Técnicas e Registro Arquitetural

1. **Autonomia com Responsabilidade**: Decisões de escopo pontual (ex: nome de variáveis, estrutura interna de helper) são tomadas pelo autor com validação no code review.
2. **Obrigatoriedade de ADR**: Mudanças que afetem:
   - Contratos entre módulos ou contratos externos de API.
   - Adição ou remoção de dependências estruturais.
   - Estratégia de dados, persistência ou concorrência.
   *Devem ser submetidas como um Architecture Decision Record (ADR) na pasta `docs/decisions/` para validação coletiva da equipe*.
3. **Sem Tecnologias Fictícias ou Prematuras**: É proibido introduzir novas tecnologias (Docker, Kubernetes, Redis, microsserviços) sem aprovação explícita e justificativa documentada.

---

## 5. Integração Frequente (Continuous Integration)

1. **Branches Curtas**: Branches de funcionalidades (`feat/...`) não devem ter vida superior a **48 horas**. Tarefas grandes devem ser decompostas em entregas incrementais.
2. **Rebase com `main` Diário**: Antes de abrir o Pull Request ou solicitar revisão final, o autor deve atualizar sua branch com a base mais recente da `main` (`git pull --rebase origin main`).
3. **Pipeline Verde Obrigatório**: Nenhum PR pode ser mesclado se as validações do GitHub Actions (`ci.yml`) falharem (lint, formatação ou testes).

---

## 6. Definição de Pronto (Definition of Done — DoD)

Uma Issue ou Pull Request só é considerado **Pronto (Done)** quando cumpre integralmente os seguintes requisitos:

- [ ] **Funcionalidade/Fix Implementado**: O código atende com fidelidade aos critérios de aceite especificados no requisito (RF/RN/RNF).
- [ ] **Fronteiras Respeitadas**: Routers agem como adaptadores HTTP finos; lógica de domínio encapsulada em `service.py`.
- [ ] **Testes Automatizados**: Testes unitários ou de integração cobrindo fluxos felizes e exceções relevantes adicionados e passando com sucesso.
- [ ] **Linters & Formatadores Sem Erros**: Execução limpa de `ruff check`, `ruff format` no backend e `eslint`, `prettier` no frontend.
- [ ] **Documentação Atualizada**: Caso contratos ou regras tenham mudado, os documentos correspondentes em `docs/` e os `README.md` dos módulos foram atualizados.
- [ ] **Migrações Aplicadas**: Se houve alteração de banco, a migração do Alembic correspondente foi criada, testada (upgrade e downgrade) e comitada.
- [ ] **Segurança e Privacidade Homologadas**: Nenhuma chave secreta em código; nenhum dado real de participantes nas fixtures; nenhum arquivo no disco permanente.
- [ ] **Revisão e Aprovação**: Revisado e aprovado formalmente por outro desenvolvedor no GitHub.

