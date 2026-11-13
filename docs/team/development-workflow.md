# Fluxo Diário de Desenvolvimento (Development Workflow) — Atlas Santos

Este guia orienta o fluxo operacional cotidiano de um desenvolvedor na equipe do Atlas Santos.

---

## 1. Convenções de Branches

Todas as branches devem seguir a nomenclatura padronizada com o tipo e uma descrição concisa em inglês ou identificador da issue:

- `feat/<issue-num>-<short-description>`: Novas funcionalidades (ex: `feat/12-captain-curation-queue`)
- `fix/<issue-num>-<short-description>`: Correção de defeitos (ex: `fix/34-quota-race-condition`)
- `docs/<short-description>`: Documentação e ADRs (ex: `docs/update-api-specs`)
- `refactor/<short-description>`: Melhorias de código sem mudança funcional (ex: `refactor/extract-routing-adapter`)
- `test/<short-description>`: Adição de testes de regressão ou carga (ex: `test/concurrency-quota-suite`)
- `chore/<short-description>`: Ajustes de CI, dependências ou automações (ex: `chore/upgrade-vite-plugin`)

---

## 2. Padrão de Conventional Commits

As mensagens de commit devem ser escritas em **inglês**, utilizando o formato padronizado:

```text
<tipo>(<escopo>): <descrição no imperativo e minúsculo>

[corpo opcional explicando o motivo da mudança]

[rodapé opcional referenciando issues e RF/RN]
```

### Exemplos Válidos:
- `feat(curation): implement captain approval service endpoint for media (RF-12)`
- `fix(media): enforce atomic reservation check to prevent quota overconsumption (RN-05)`
- `test(health): add contract test for openapi schema compliance`
- `docs(adr): register ADR-0001 on modular monolith architecture`

---

## 3. Passo a Passo do Ciclo de Trabalho

1. **Escolha uma Issue no Backlog**: Garanta que você é o `assignee` e mova a issue para *In Progress*.
2. **Crie a Branch a partir da `main` atualizada**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/42-atomic-quota-reservation
   ```
3. **Desenvolva com Testes**:
   - Escreva ou atualize os testes unitários/integração correspondentes.
   - Execute o backend ou frontend localmente:
     ```bash
     # Backend
     ./scripts/dev-backend.sh
     # Frontend
     ./scripts/dev-frontend.sh
     ```
4. **Valide a Qualidade Localmente Antes do Commit**:
   ```bash
   # No diretório backend/
   ruff check .
   ruff format --check .
   pytest

   # No diretório frontend/
   npm run lint
   npm run test:run
   ```
5. **Comite e Abra o Pull Request**:
   - Faça commits atômicos e bem descritos.
   - Submeta o PR utilizando o template `.github/PULL_REQUEST_TEMPLATE.md`.
   - Solicite a revisão de um colega da equipe.
6. **Resolva Feedbacks e Realize o Merge**:
   - Após aprovação e com o pipeline verde no GitHub Actions, realize o *Squash and Merge* ou *Rebase and Merge*.
   - A branch de trabalho é excluída automaticamente após o merge.

