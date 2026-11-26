<p align="center">
  <img src="docs/assets/atlas-santos.png" width="320" alt="Logotipo do Atlas Santos">
</p>

# Atlas Santos

De 5 a 11 de outubro de 2026, **83 estudantes e 12 servidores do IFSP Campus Araraquara** participaram de um estudo do meio em Santos. O Atlas Santos nasceu para reunir as fotografias e reflexões dessa viagem. Cada equipe terá seu próprio atlas para contar o que observou e revisitar, dia a dia, os lugares por onde passou.

**[Abrir o Atlas Santos](https://atlas-santos.vercel.app/) · [Consultar os requisitos](docs/requirements/requirements-summary.md)**

## O projeto

A proposta é que estudantes e servidores escolham suas fotos e possam escrever sobre elas no **Olhares sobre Santos**. Os capitães revisam os registros de suas equipes. No mapa, cada fotografia com localização ajuda a reconstruir um trecho provável do percurso a pé.

### Fases do desenvolvimento

| Fase | Entrega | Critério de conclusão |
| --- | --- | --- |
| 1 · Acesso local e mapa 3D | Primeira tela do atlas da equipe | Os três perfis locais conseguem entrar, explorar Santos com edifícios em 3D, restaurar a vista inicial e sair. |
| 2 · Participantes e equipes | Pré-cadastro do IF-Arbitra, vínculo com equipes e autenticação na API | Cada participante acessa os dados autorizados para seu perfil e equipe. |
| 3 · Acervo e curadoria | Envio de fotos, cotas, EXIF, localização e revisão pelo capitão | O participante acompanha a revisão. A galeria exibe os registros aprovados para aquele público. |
| 4 · Fotografias e percursos no mapa | Marcadores e rotas a pé por equipe e dia, renderizados com deck.gl | O mapa apresenta as fotos autorizadas em ordem cronológica e os caminhos estimados. Retirar uma foto atualiza o percurso. |
| 5 · Olhares sobre Santos | Reflexões opcionais por tema, descrições assistidas por IA e síntese da viagem | A equipe revisa as descrições e a síntese antes de incorporá-las ao atlas. |
| 6 · Exportações e publicação | PDF e PNG, seguidos de HTML e GeoJSON, com homologação e deploy | As exportações respeitam os filtros e as permissões. A equipe valida a recuperação de backup e o funcionamento em produção. |

**Etapa atual para revisão local:** fase 1.

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

Na [tela de acesso local](http://localhost:5173/login), use `ana@atlas.test` (estudante), `marina@atlas.test` (capitã) ou `caio@atlas.test` (servidor). A senha dos três perfis é `Santos2026!`. As contas funcionam apenas em desenvolvimento.

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
