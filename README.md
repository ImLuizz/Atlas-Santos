# Atlas Santos

Aplicação web de cartografia colaborativa do estudo do meio em Santos, realizado de **5 a 11 de outubro de 2026** pelo IFSP Campus Araraquara. O projeto reúne as fotografias e reflexões de 83 estudantes e 12 servidores em um atlas por equipe. A entrega está prevista para 4 de dezembro de 2026.

## O que existe no repositório

Esta versão é a fundação do sistema. Há um frontend React/Vite, uma API FastAPI com verificações de saúde em `/health` e `/api/v1/health`, persistência de tarefas com SQLAlchemy/Alembic, um worker e testes. Os fluxos de negócio abaixo estão no [plano de implementação](TODO.md). A [matriz de requisitos](docs/requirements/requirements-summary.md) identifica o comportamento a homologar e as evidências já disponíveis.

## Fluxo previsto

1. A administração concilia os cadastros do IF-Arbitra e mantém equipes, capitães, acessos e cotas. O sistema envia as credenciais por e-mail e oferece recuperação de senha na tela de login.
2. Estudantes e servidores enviam uma foto por formulário, até a cota individual do atlas (padrão de 20). Podem corrigir data e localização e incluir tema e reflexão em **Olhares sobre Santos**.
3. O capitão revisa os registros de sua equipe. A aprovação os disponibiliza no atlas conforme as permissões. Fotos enviadas pelo próprio capitão recebem aprovação automática no envio inicial. Uma edição de registro retorna à aprovação.
4. O mapa e a galeria permitem explorar equipe e dia. O backend estima automaticamente percursos a pé entre fotos aprovadas e localizadas, em ordem cronológica. A equipe selecionada tem visualização 3D e o mapa geral permite comparar todas as equipes.
5. A IA sugere descrições a partir da imagem e, quando disponível, da reflexão aprovada. O usuário pode escolher, editar ou descartar o texto antes da revisão do capitão. Em outro fluxo, a IA reúne reflexões aprovadas e propõe uma conclusão da viagem em diálogo com *Sonho Manifesto*, de Sidarta Ribeiro. A administração revisa a síntese antes de publicá-la.
6. As exportações respeitam as autorizações do acervo. PDF e PNG têm prioridade, seguidos por HTML e GeoJSON.

## Tecnologias

| Camada | Tecnologia e responsabilidade |
| --- | --- |
| Interface | React, Vite e JavaScript/JSX, com Tailwind CSS. |
| Cartografia | Mapbox para o mapa e deck.gl para pontos e percursos. O cálculo do percurso usa um serviço pedestre a partir do backend. |
| API e tarefas | Python, FastAPI e worker para operações demoradas. |
| Dados | PostgreSQL, SQLAlchemy e migrações Alembic. |
| Hospedagem e arquivos | Railway e Railway Buckets compatível com S3 para originais, derivados e exportações. |

## Desenvolvimento local

Use Python 3.11 ou superior e Node.js 22. Para começar com um clone existente, entre em `backend/` e siga a partir da criação do ambiente virtual. No Windows, use `.\.venv\Scripts\Activate.ps1` no PowerShell para ativar o ambiente e `Copy-Item` para copiar os exemplos.

```bash
git clone https://github.com/ImLuizz/Atlas-Santos.git
cd Atlas-Santos/backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
# Configure DATABASE_URL para um PostgreSQL de desenvolvimento disponível.
alembic upgrade head
uvicorn app.main:app --reload
```

No diretório `backend/`, com o mesmo ambiente configurado, o worker pode ser iniciado separadamente com `python -m app.worker.main`. Os contratos HTTP disponíveis em desenvolvimento podem ser consultados em `http://localhost:8000/docs` com a documentação habilitada.

Em outro terminal, na raiz do repositório:

```bash
cd frontend
cp .env.example .env
npm ci
npm run dev
```

## Verificações e documentação

O [relatório da revisão de 23 de novembro](docs/requirements/auditoria-2026-11-23.md) registra as divergências encontradas e indica onde acompanhar as pendências.

- No diretório `backend/`: `ruff check .`, `ruff format --check .` e `pytest`.
- No diretório `frontend/`: `npm run lint`, `npm run test:run` e `npm run build`.
- [Arquitetura](docs/architecture/overview.md), [decisões técnicas](docs/decisions/README.md) e [contratos de API](docs/api/README.md).
- [Implantação Railway](docs/operations/deployment-railway.md), [backup e restauração](docs/operations/backup-and-retention.md) e [guia de contribuição](CONTRIBUTING.md).
