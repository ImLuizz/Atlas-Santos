<p align="center">
  <img src="docs/assets/atlas-santos.png" width="320" alt="Logotipo do Atlas Santos">
</p>

# Atlas Santos

De 5 a 11 de outubro de 2026, **83 estudantes e 12 servidores do IFSP Campus Araraquara** participaram de um estudo do meio em Santos. O Atlas Santos nasceu para reunir as fotografias e reflexões dessa viagem. Cada equipe terá seu próprio atlas para contar o que observou e revisitar, dia a dia, os lugares por onde passou.

**[Abrir o Atlas Santos](https://atlas-santos.vercel.app/) · [Consultar os requisitos](docs/requirements/requirements-summary.md) · [Diagrama do banco de dados](docs/banco-de-dados.md)**

## O projeto

A proposta é que estudantes e servidores escolham suas fotos e possam escrever sobre elas no **Olhares sobre Santos**. Os capitães revisam os registros de suas equipes. No mapa, cada fotografia com localização ajuda a reconstruir um trecho provável do percurso a pé.

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

## Contribuidores

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/Bernardo270408">
        <img src="https://github.com/Bernardo270408.png" width="100" alt="Bernardo Marcelino"/><br />
        <sub><b>Bernardo Marcelino</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ImLuizz">
        <img src="https://github.com/ImLuizz.png" width="100" alt="Luiz Gabriel"/><br />
        <sub><b>Luiz Gabriel</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Samuel-fernandesf">
        <img src="https://github.com/Samuel-fernandesf.png" width="100" alt="Samuel Fernandes"/><br />
        <sub><b>Samuel Fernandes</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/YagorVitor">
        <img src="https://github.com/YagorVitor.png" width="100" alt="Yagor Santos"/><br />
        <sub><b>Yagor Santos</b></sub>
      </a>
    </td>
  </tr>
</table>
