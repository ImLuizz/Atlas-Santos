# Registros de Decisão Arquitetural (ADRs) — Atlas Santos

Este diretório contém os **Architecture Decision Records (ADRs)** que formalizam escolhas arquiteturais fundamentais do sistema, registrando contexto, alternativas analisadas, decisões adotadas e suas consequências.

## Índice de Decisões

| ID | Título | Status | Data |
| :--- | :--- | :--- | :--- |
| [ADR-0001](./ADR-0001-modular-monolith-and-worker.md) | Adoção de Monólito Modular com Worker Assíncrono Separado | **Aprovado** | 12/11/2026 |
| [ADR-0002](./ADR-0002-technology-stack.md) | Stack Tecnológica Oficial (FastAPI, React, Vite, PostgreSQL) | **Aprovado** | 12/11/2026 |
| [ADR-0003](./ADR-0003-data-and-outbox-strategy.md) | Estratégia de Dados, Transactional Outbox e Armazenamento de Objetos | **Aprovado** | 12/11/2026 |

---

## Formato Padrão para Novos ADRs

Ao propor uma nova decisão técnica significativa, a equipe deve criar um novo arquivo `ADR-XXXX-<titulo>.md` seguindo o modelo:

1. **Título e Metadados** (Status, Data, Decisores)
2. **Contexto e Formulação do Problema**
3. **Alternativas Consideradas**
4. **Decisão Arquitetural**
5. **Consequências** (Positivas e Negativas/Compromissos)

