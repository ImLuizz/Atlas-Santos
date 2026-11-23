# Backend do Atlas Santos

A API FastAPI e o processo assíncrono compartilham modelos SQLAlchemy e configuração. O esquema inicial do Alembic cria a tabela de tarefas. As únicas rotas disponíveis são `GET /health` e `GET /api/v1/health`. Ambas consultam o banco, retornam 200 quando ele responde e 503 quando está indisponível.

Os [módulos](app/modules/README.md) descrevem funcionalidades previstas; seus diretórios ainda não expõem serviços de negócio. Os [adaptadores](app/integrations/README.md) definem contratos Python. O worker não registra processadores para fotos, IA, roteamento ou exportação nesta versão.

Consulte as [instruções de execução](../README.md), a [arquitetura](../docs/architecture/overview.md) e o [backlog](../TODO.md).
