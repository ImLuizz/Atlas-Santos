<p align="center">
  <img src="docs/assets/atlas-santos.png" width="320" alt="Logotipo do Atlas Santos">
</p>

# Atlas Santos

De 5 a 11 de outubro de 2026, **83 estudantes e 12 servidores do IFSP Campus Araraquara** participaram de um estudo do meio em Santos. O Atlas Santos nasceu para reunir as fotografias e reflexões dessa viagem. Cada equipe terá seu próprio atlas para contar o que observou e revisitar, dia a dia, os lugares por onde passou.

**[Abrir o Atlas Santos](https://atlas-santos.vercel.app/) · [Consultar os requisitos](docs/requirements/requirements-summary.md)**

## O projeto

A proposta é que estudantes e servidores escolham suas fotos e possam escrever sobre elas no **Olhares sobre Santos**. Os capitães revisam os registros de suas equipes. No mapa, cada fotografia com localização ajuda a reconstruir um trecho provável do percurso a pé.

## Equipe

- Bernardo Marcelino
- Luiz Leli
- Samuel Fernandes
- Yagor Santos

## Como rodar no computador

Você precisa do **Docker com Compose v2.17 ou superior**. No Windows, abra o Docker Desktop em modo de contêineres Linux. Na pasta principal do repositório, execute:

```sh
docker compose up --build
```

Na primeira execução, o Docker baixa as dependências, inicia o PostgreSQL e aplica as migrações. Quando o Vite estiver pronto, abra a [página local](http://localhost:5173). Se aparecer **“Serviço disponível.”**, a página conseguiu consultar a API e a API conseguiu acessar o banco.

Para abrir o mapa 3D, configure `VITE_MAPBOX_ACCESS_TOKEN` com seu token público do Mapbox em `frontend/.env.local`. Com Docker, execute `docker compose --env-file frontend/.env.local up --build`. Se usar o Vite diretamente, ele lê esse arquivo ao iniciar.

O Compose prepara três contas no banco de desenvolvimento. Abra a [tela de acesso local](http://localhost:5173/login) e use a senha `Santos2026!`.

| Conta | Vínculo e função | Equipe |
| --- | --- | --- |
| `ana@atlas.test` | Estudante participante | Centro |
| `marina@atlas.test` | Estudante e capitã | Centro |
| `caio@atlas.test` | Servidor participante | Orla |

Para conferir o fluxo, entre como Marina, abra **Gestão do grupo** e confira os integrantes do Centro. Atualize `/mapa` para verificar a sessão. Depois de sair, abra `/mapa` diretamente. A aplicação deve pedir o login novamente. Com Caio, o título muda para **Atlas da equipe Orla**.

A API verifica a senha e envia um cookie HttpOnly. O banco guarda o hash do token, a validade e a revogação da sessão. A capitania é uma função vinculada à equipe. Estudantes e servidores podem ter a função de participante.

Quem executa o backend diretamente deve aplicar `alembic upgrade head` na pasta `backend`. Com `ENVIRONMENT=development`, rode `python -m app.modules.auth.seed` para preparar as contas. Repetir o comando preserva senhas e vínculos existentes. Para HTTP local, use `COOKIE_SECURE=false`.

| Componente | Onde trabalhar |
| --- | --- |
| Interface · React, Vite e Tailwind CSS | [Código do frontend](frontend/) |
| API · Python e FastAPI | [Código do backend](backend/) · [Documentação interativa local](http://localhost:8000/docs) |
| Banco e tarefas em segundo plano · PostgreSQL e worker | [Migrações](backend/alembic/) · [Código do worker](backend/app/worker/) |

A interface e a API recarregam quando você edita o código. Para conferir a fila, que começa vazia, abra outro terminal na mesma pasta e rode:

```sh
docker compose exec worker python -m app.worker.main --single-pass
```

Para encerrar, pressione `Ctrl+C` no primeiro terminal e execute `docker compose down`. Os dados do PostgreSQL ficam guardados para a próxima execução.

## Organização do repositório

As telas de acesso, mapa e apresentação ficam em `frontend/src/features`. A API concentra o controle de sessão em `backend/app/modules/auth` e a consulta aos integrantes em `backend/app/modules/teams`.

<details>
<summary>Ver a árvore completa da fase 2A</summary>

```text
Atlas-Santos/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   ├── .gitkeep
│   │   │   ├── 2026_11_12_2155-45e99ca9977f_create_jobs_table.py
│   │   │   └── 2026_11_27_access_teams.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   └── health.py
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── metadata.py
│   │   │   └── session.py
│   │   ├── integrations/
│   │   │   ├── ai/
│   │   │   │   └── base.py
│   │   │   ├── routing/
│   │   │   │   └── base.py
│   │   │   └── storage/
│   │   │       └── base.py
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── models.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── seed.py
│   │   │   └── teams/
│   │   │       ├── models.py
│   │   │       └── router.py
│   │   ├── worker/
│   │   │   ├── dispatcher.py
│   │   │   └── main.py
│   │   └── main.py
│   ├── tests/
│   │   ├── contract/
│   │   │   └── test_openapi.py
│   │   ├── integration/
│   │   │   ├── test_access.py
│   │   │   ├── test_health.py
│   │   │   └── test_worker.py
│   │   ├── unit/
│   │   │   └── test_config.py
│   │   └── conftest.py
│   ├── .env.example
│   ├── alembic.ini
│   ├── Dockerfile
│   └── pyproject.toml
├── docs/
│   ├── assets/
│   │   └── atlas-santos.png
│   └── requirements/
│       └── requirements-summary.md
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── App.jsx
│   │   ├── assets/
│   │   │   ├── atlas-santos.png
│   │   │   ├── centro-santos.jpg
│   │   │   └── santos-aerea.jpg
│   │   ├── components/
│   │   │   └── layout/
│   │   │       ├── Footer.jsx
│   │   │       └── Header.jsx
│   │   ├── features/
│   │   │   ├── atlas/
│   │   │   │   ├── atlas.css
│   │   │   │   ├── AtlasFilters.jsx
│   │   │   │   ├── AtlasPage.jsx
│   │   │   │   ├── SantosMap.jsx
│   │   │   │   └── TeamMembers.jsx
│   │   │   ├── auth/
│   │   │   │   ├── login.css
│   │   │   │   └── LoginPage.jsx
│   │   │   └── landing/
│   │   │       ├── landing.css
│   │   │       └── LandingPage.jsx
│   │   ├── lib/
│   │   │   ├── api-client.js
│   │   │   └── config.js
│   │   ├── styles/
│   │   │   └── index.css
│   │   ├── tests/
│   │   │   ├── App.test.jsx
│   │   │   ├── Atlas.test.jsx
│   │   │   ├── Login.test.jsx
│   │   │   └── setup.js
│   │   └── main.jsx
│   ├── .env.example
│   ├── .prettierrc
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── vercel.json
│   └── vite.config.js
├── scripts/
│   ├── dev-backend.sh
│   ├── dev-frontend.sh
│   └── dev-worker.sh
├── .editorconfig
├── .gitignore
├── compose.yaml
└── README.md
```

</details>
