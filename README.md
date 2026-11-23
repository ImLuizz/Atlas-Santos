<p align="center">
  <img src="docs/assets/atlas-santos.png" width="320" alt="Logotipo do Atlas Santos">
</p>

# Atlas Santos

De 5 a 11 de outubro de 2026, **83 estudantes e 12 servidores do IFSP Campus Araraquara** participaram de um estudo do meio em Santos. O Atlas Santos nasceu para reunir as fotografias e reflexões dessa viagem. Cada equipe terá seu próprio atlas para contar o que observou e revisitar, dia a dia, os lugares por onde passou.

**[Abrir o Atlas Santos](https://atlas-santos.vercel.app/) · [Consultar os requisitos](docs/requirements/requirements-summary.md)**

## O projeto

A proposta é que estudantes e servidores escolham suas fotos e possam escrever sobre elas no **Olhares sobre Santos**. Os capitães revisam os registros de suas equipes. No mapa, cada fotografia com localização ajuda a reconstruir um trecho provável do percurso a pé.

Hoje, a página inicial já consulta a API e confirma a conexão com o banco. A galeria, o envio de fotos, a curadoria e os mapas são as próximas funcionalidades previstas.

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

## Onde está publicado

A **Vercel** hospeda a interface. O **Railway** executa a API e o PostgreSQL. Para conferir a conexão do serviço publicado com o banco, consulte a [rota de saúde da API](https://atlas-santos-production.up.railway.app/health).
