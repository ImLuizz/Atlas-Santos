# ADR-0002: Escolha da Stack Tecnológica Oficial

- **Status**: Aprovado
- **Data**: 12 de novembro de 2026
- **Decisores**: Principal Software Architect & Atlas Santos Engineering Team
- **Contexto Técnico**: Restrições Tecnológicas Confirmadas (Seção 8.1 dos Requisitos)

---

## 1. Contexto

A especificação do Atlas Santos estabeleceu a necessidade de migrar a API de protótipo (Express/Node.js) para uma base tecnológica robusta em Python para viabilizar processamento científico de dados cartográficos, integração de modelos de IA e manipulação de mídia em segundo plano, mantendo o frontend em React.

As escolhas precisam atender aos seguintes requisitos não funcionais:
- RNF-01: Controle de sessão e segurança de cookies.
- RNF-04: Interface responsiva e acessível para dispositivos móveis (360px).
- RNF-09: Cartografia com tiles OSM e dados geográficos precisos.
- RNF-10: Implantação reproduzível e versionada.

---

## 2. Decisão

A equipe adota oficialmente as seguintes tecnologias e ferramentas:

### 2.1 Backend
- **Linguagem**: Python (versão base `>= 3.11`, compatível com Python 3.12/3.14).
- **Framework Web**: `FastAPI` (versão fixada `0.115.x`). Fornece alto desempenho assíncrono e geração automática de documentação OpenAPI/Swagger (RNF-12).
- **Validação e Tipagem**: `Pydantic v2` e `pydantic-settings`. Garante parsing seguro de payloads e variáveis de ambiente.
- **ORM e Migrações**: `SQLAlchemy 2.0` (estilo declarativo assíncrono) com `Alembic 1.14.x` para versionamento estrito de esquema.
- **Driver de Banco**: `psycopg` (versão 3 com binários otimizados) para PostgreSQL e `aiosqlite` para suíte de testes rápida in-memory.
- **Servidor ASGI**: `uvicorn` com event loop uvloop.
- **Qualidade de Código**: `Ruff` como linter e formatador unificado (substitui Flake8, Black e isort com alta velocidade de execução).
- **Testes**: `Pytest` com `pytest-asyncio` e `httpx`.

### 2.2 Frontend
- **Biblioteca de Interface**: `React 18.3.x` com JSX moderno.
- **Bundler & Dev Server**: `Vite 6.x` com ESM nativo e Hot Module Replacement ultrarrápido.
- **Estilização**: `Tailwind CSS 3.4.x` com `postcss` e `autoprefixer`.
- **Cartografia Interativa**: `Leaflet 1.9.x` com `React Leaflet 4.2.x`, consumindo tiles comunitários do OpenStreetMap respeitando as diretrizes de atribuição (RNF-09).
- **Qualidade de Código**: `ESLint 9` (Flat Config) e `Prettier 3.x`.
- **Testes**: `Vitest` com `@testing-library/react` e `jsdom`.

### 2.3 Infraestrutura
- **PaaS**: `Railway` (com projetos e segredos segregados para Desenvolvimento, Homologação e Produção).
- **Banco de Dados**: Instância gerenciada de `PostgreSQL 16+` no Railway.
- **Armazenamento de Objetos**: `Railway Buckets` privados (API compatível com AWS S3).

---

## 3. Consequências

- **Compatibilidade e Estabilidade**: Todas as versões foram selecionadas com base em compatibilidade mútua e maturidade no ecossistema open-source.
- **Sem Dependência de Serviços Externos no CI**: Testes de backend executam com SQLite assíncrono in-memory e mocks de adaptadores, permitindo validação ágil no GitHub Actions sem provisionar PostgreSQL ou contas S3 reais.

