# Atlas Santos

Atlas fotográfico do estudo do meio em Santos do IFSP Campus Araraquara. A base atual tem uma página React que consulta a API FastAPI, um banco PostgreSQL e um worker que lê a fila de tarefas. Os fluxos de fotos, curadoria e mapas estão na [matriz de requisitos](docs/requirements/requirements-summary.md).

## Rodar no computador

Instale o Docker com o Compose v2.17 ou superior. No Windows, inicie o Docker Desktop em modo de contêineres Linux. Na raiz do clone, execute:

```sh
docker compose up --build
```

Na primeira execução, o Docker baixa as dependências, inicia o PostgreSQL e aplica as migrações. Quando o Vite estiver pronto, abra [a página inicial](http://localhost:5173). A mensagem **Serviço disponível** confirma que a página conseguiu consultar a API e que a API alcançou o banco. A documentação interativa fica em [localhost:8000/docs](http://localhost:8000/docs).

A API e o frontend recarregam ao editar o código. Para conferir a fila, abra outro terminal na raiz e execute `docker compose exec worker python -m app.worker.main --single-pass`. A fila começa vazia.

Para encerrar, use `Ctrl+C` e depois `docker compose down`. O volume do PostgreSQL guarda os dados para a próxima execução.
