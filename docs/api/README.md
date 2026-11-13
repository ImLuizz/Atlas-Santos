# Especificação e Contratos da API — Atlas Santos

A API do Atlas Santos é construída com **FastAPI** e utiliza **Pydantic v2** para validação estrita de esquemas e contratos de dados (RNF-12, RNF-13).

---

## 1. Documentação Interativa e Esquema OpenAPI

Em ambiente de desenvolvimento e homologação (`DEBUG=true`), a documentação interativa pode ser consultada diretamente em:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Esquema OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## 2. Padrão de Versionamento de Rotas

Todas as rotas de domínio de negócio são versionadas sob o prefixo `/api/v1`:

- `/api/v1/health`: Verificação de prontidão e conectividade de banco.
- `/api/v1/auth/*`: Sessões e convites (módulo `identity`).
- `/api/v1/organizations/*`: Equipes, atlas e cotas (módulo `organization`).
- `/api/v1/contributions/*`: Fotografias e submissões (módulo `contributions`).
- `/api/v1/media/*`: Tickets de upload pré-assinados e finalizações (módulo `media`).
- `/api/v1/curation/*`: Fila de trabalho e revisões do capitão (módulo `curation`).
- `/api/v1/routes/*`: Reconstrução e aprovação de percursos (módulo `routes`).
- `/api/v1/ai/*`: Propostas de descrição assistida (módulo `ai`).
- `/api/v1/publication/*`: Filtros e consultas públicas autorizadas (módulo `publication`).
- `/api/v1/exports/*`: Solicitações assíncronas de PDF/PNG/HTML/GeoJSON (módulo `exports`).
- `/api/v1/administration/*`: Importação do IF-Arbitra e conciliação (módulo `administration`).

---

## 3. Formato Padronizado de Respostas de Erro (RNF-12)

Todas as respostas de erro HTTP seguem uma estrutura previsível contendo código de erro e correlation ID:

```json
{
  "detail": "Mensagem compreensível da falha",
  "error_code": "RESOURCE_NOT_FOUND",
  "correlation_id": "c1f7a28e-89a5-4841-9452-47cbb650f924",
  "timestamp": "2026-11-12T21:00:00Z"
}
```

Nenhum *stack trace* interno do servidor ou segredo é exposto nas respostas da API.

