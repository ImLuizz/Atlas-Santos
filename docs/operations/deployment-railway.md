# Guia de Implantação e Operação no Railway — Atlas Santos

Este documento descreve a topologia de implantação, segregação de ambientes e configurações da infraestrutura do **Atlas Santos** na plataforma **Railway**.

---

## 1. Topologia de Serviços

Para atender à arquitetura de **Monólito Modular com Worker Independente** (ADR-0001) e segregação de persistência, a infraestrutura é composta por 5 recursos no Railway:

```text
[Railway Project: Atlas Santos]
├── 1. Service: atlas-santos-frontend (Node / Static Web Server)
├── 2. Service: atlas-santos-api (Python / FastAPI / Uvicorn)
├── 3. Service: atlas-santos-worker (Python Background Worker)
├── 4. Plugin: Railway PostgreSQL (Instância Postgres 16+)
└── 5. Plugin: Railway Storage Bucket (Armazenamento S3-compatível)
```

---

## 2. Segregação de Ambientes

O projeto opera com três ambientes lógicos totalmente isolados:

1. **Desenvolvimento (Local / Preview Branches)**:
   - Utilizado pela equipe de desenvolvimento.
   - Banco SQLite in-memory para testes unitários ou Postgres local via Docker.
   - Mock de S3 e provedores externos.
2. **Homologação (Staging Railway)**:
   - Espelho fiel do ambiente produtivo, acionado automaticamente em merges na branch `develop`.
   - Utilizado para validação com os cenários de homologação T-01 a T-12 com dados sintéticos dos 95 participantes.
3. **Produção (Railway Production)**:
   - Acionado via releases tagueadas na branch `main`.
   - Banco PostgreSQL com backups automáticos habilitados.
   - Balde S3 com criptografia em repouso e permissões privadas estritas.

---

## 3. Comandos de Inicialização no Railway

### API (FastAPI)
- **Root Directory**: `backend`
- **Build Command**: `pip install --upgrade pip && pip install .`
- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### Worker (Processo Assíncrono)
- **Root Directory**: `backend`
- **Build Command**: `pip install --upgrade pip && pip install .`
- **Start Command**:
  ```bash
  python -m app.worker.main --poll-interval 2.0
  ```

### Frontend (React / Vite)
- **Root Directory**: `frontend`
- **Build Command**: `npm ci && npm run build`
- **Start Command**: `npx serve -s dist -l $PORT`

---

## 4. Gestão de Segredos e Variáveis de Ambiente

Todas as variáveis sensíveis são injetadas exclusivamente pelo painel do Railway, nunca versionadas no Git:

| Variável | Descrição | Onde Configurar |
| :--- | :--- | :--- |
| `SECRET_KEY` | Chave de 32+ caracteres criptográficos para assinar sessões | API, Worker |
| `DATABASE_URL` | String de conexão segura gerada automaticamente pelo Railway Postgres | API, Worker |
| `STORAGE_ENDPOINT_URL` | URL do endpoint S3 do Railway Bucket | API, Worker |
| `STORAGE_ACCESS_KEY_ID` | Chave de acesso do bucket privado | API, Worker |
| `STORAGE_SECRET_ACCESS_KEY`| Chave secreta do bucket privado | API, Worker |
| `STORAGE_BUCKET_NAME` | Nome do balde no Railway Storage | API, Worker |
| `CORS_ORIGINS` | Lista JSON com URLs autorizadas (ex: `["https://atlas-santos.up.railway.app"]`) | API |
| `VITE_API_BASE_URL` | URL pública da API do backend | Frontend |

