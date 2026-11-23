# Implantação no Railway

A especificação exige configurações próprias para desenvolvimento, homologação e produção no Railway (RNF015, RNF022), HTTPS em produção (RNF004), PostgreSQL (RNF020) e Railway Buckets (RNF021). Este guia descreve a implantação prevista. O workflow do repositório executa verificações de código. A publicação e o provisionamento dos ambientes dependem de configuração no Railway. [Workflow de CI](../../.github/workflows/ci.yml)

## Componentes

| Componente | Como preparar |
| --- | --- |
| API | Diretório `backend`. Instalar com `pip install .`. Aplicar as migrações com `alembic upgrade head` antes de utilizar o esquema. Iniciar `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. |
| Worker | Usar o mesmo pacote e banco da API. Iniciar `python -m app.worker.main`. Verificar cada tipo de trabalho efetivamente implementado antes de usá-lo com dados reais. |
| Frontend | Diretório `frontend`. Executar `npm ci` e `npm run build`. Publicar o conteúdo de `dist/` em um servidor de arquivos estáticos com suporte à navegação da aplicação. |
| PostgreSQL | Configurar a conexão do ambiente para a API, a migração e o worker, usando o driver declarado em [pyproject.toml](../../backend/pyproject.toml). |
| Railway Buckets | Reservar armazenamento privado do ambiente para originais, derivados e arquivos exportados. Configurar os acessos de homologação antes de usar a integração. |

## Configuração do ambiente

Os exemplos versionados descrevem os nomes das variáveis locais. Os valores de desenvolvimento devem ser substituídos pelos específicos de cada ambiente. [Backend](../../backend/.env.example) · [Frontend](../../frontend/.env.example)

- A API e o worker precisam das configurações apropriadas para o banco. As chaves privadas de armazenamento, e-mail, roteamento e IA devem permanecer no backend quando essas integrações forem habilitadas. Configurar origens CORS permitidas e cookies de sessão compatíveis com HTTPS.
- O frontend recebe a URL pública da API e a configuração pública do Mapbox. As variáveis `VITE_*` ficam disponíveis no navegador. O frontend deve enviar e receber apenas dados autorizados, inclusive ao mostrar várias equipes.
- Em homologação, conferir que o mapa e os arquivos exportados preservam os créditos cartográficos. O backend deve realizar o roteamento a pé e as chamadas de IA nos limites de divulgação dos registros (RNF008, RNF014, RNF023–RNF025).

## Conferência da entrega

Consultar `/health` para verificar o estado do banco e da API. Conferir a execução das migrações e a inicialização do worker separadamente. Para aceitar o produto, exercitar também as funcionalidades implementadas com uma equipe de teste, incluindo uma retirada e a falha de um provedor externo. O procedimento de [recuperação dos dados](backup-and-retention.md) abrange os arquivos e seus vínculos.

