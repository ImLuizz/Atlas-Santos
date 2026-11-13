## Descrição da Modificação

<!-- Descreva de forma concisa o que foi implementado, corrigido ou refatorado neste Pull Request. -->

## Rastreabilidade

- **Issue vinculada**: Fixes #<!-- número da issue -->
- **Requisitos contemplados**: <!-- Ex: RF-01, RN-03, RNF-01 -->
- **Módulo(s) afetado(s)**: <!-- Ex: identity, media, curation, frontend -->

## Tipo de Alteração

- [ ] `feat`: Nova funcionalidade
- [ ] `fix`: Correção de bug
- [ ] `docs`: Documentação
- [ ] `refactor`: Refatoração sem alteração de comportamento
- [ ] `test`: Adição ou ajuste de testes
- [ ] `chore`: Configuração, dependências ou automação

## Checklist de Qualidade e Segurança

- [ ] **Conventional Commits**: As mensagens de commit seguem o padrão obrigatório.
- [ ] **Fronteiras de Domínio**: Nenhum router contém lógica de negócio pesada; o isolamento entre módulos foi respeitado.
- [ ] **Segurança e Privacidade**:
  - [ ] Nenhuma credencial, token ou chave privada está exposta.
  - [ ] Nenhum dado real de estudantes ou servidores foi incluído em fixtures/código.
  - [ ] Variáveis privadas do backend não vazam para o frontend.
- [ ] **Persistência e Migrações**:
  - [ ] Não há alteração destrutiva em banco sem migração Alembic correspondente.
  - [ ] Operações críticas mantêm integridade atômica e idempotência.
- [ ] **Testes**:
  - [ ] Testes automatizados cobrindo a alteração foram adicionados ou atualizados.
  - [ ] A suíte de testes passa localmente (`pytest` / `npm test`).
- [ ] **Linters e Formatação**:
  - [ ] Backend validado com `ruff check` e `ruff format --check`.
  - [ ] Frontend validado com `npm run lint` e `npm run format:check`.

## Revisão Obrigatória (Peer Review)

- [ ] PR atribuído a pelo menos um colega da equipe de 5 desenvolvedores para revisão cruzada.
- [ ] Bloqueios ou pendências de decisão (D-01 a D-10) sinalizados nos comentários.

