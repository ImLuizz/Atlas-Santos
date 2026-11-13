# Guia de Contribuição e Convenções da Equipe — Atlas Santos

Bem-vindo ao repositório do **Atlas Santos**. Este guia estabelece os padrões e convenções de desenvolvimento obrigatórios para os cinco integrantes da equipe, garantindo que o trabalho progrida de forma organizada, segura e sustentável até a entrega final em **04 de dezembro de 2026**.

---

## 1. Convenções de Código e Nomenclatura

- **Idioma de Código e Commits**: Todo o código (nomes de variáveis, funções, classes, métodos, arquivos de código e mensagens de commit) deve ser escrito em **Inglês**.
- **Idioma da Documentação**: Toda a documentação técnica voltada à equipe e ao cliente deve ser redigida em **Português Brasileiro (pt-BR)** com precisão técnica.
- **Python (Backend e Worker)**:
  - Estilo: `snake_case` para variáveis, funções, atributos e módulos (`photo_record_service.py`).
  - Classes: `PascalCase` (`PhotoRecord`, `JobDispatcher`).
  - Constantes: `UPPER_SNAKE_CASE` (`DEFAULT_PHOTO_QUOTA`).
  - Linters e Formatação: `ruff check` e `ruff format` (configurados no `pyproject.toml`).
- **JavaScript e React (Frontend)**:
  - Arquivos e Componentes React: `PascalCase` (`Header.jsx`, `MapViewer.jsx`).
  - Variáveis, funções e hooks: `camelCase` (`useAuth.js`, `formatCaptureDate.js`).
  - Constantes: `UPPER_SNAKE_CASE` ou `camelCase` agrupado.
  - Linters e Formatação: `eslint` e `prettier` (configurados no `package.json`).

---

## 2. Convenção de Branches

Nenhum desenvolvedor realiza commits diretamente na branch `main`. Todo trabalho deve ser isolado em branches temporárias derivadas da `main` atualizada:

- `feat/<issue-id>-<short-description>`: Novas funcionalidades (ex: `feat/08-atomic-upload-reservation`).
- `fix/<issue-id>-<short-description>`: Correção de bugs (ex: `fix/19-route-segment-gap`).
- `docs/<short-description>`: Documentação, ADRs e especificações (ex: `docs/adr-0004-ai-limits`).
- `refactor/<short-description>`: Refatorações sem alteração funcional externa (ex: `refactor/extract-storage-adapter`).
- `test/<short-description>`: Adição ou melhoria de suítes de testes (ex: `test/concurrency-quota`).
- `chore/<short-description>`: Automações, scripts ou atualização de dependências fixadas (ex: `chore/ci-caching`).

---

## 3. Mensagens de Commit (Conventional Commits)

Seguimos a especificação [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) em inglês:

```text
<type>(<scope>): <short imperative description>

[optional body explaining rationale]

[optional footer referencing issue and requirement ID]
```

**Tipos aceitos**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.

**Exemplos válidos**:
- `feat(organization): add atomic quota check before issuing upload ticket (RF-09, RN-03)`
- `fix(routes): handle disconnected route segments for split groups (RF-19, RN-12)`
- `docs(team): add working agreements for peer review and dod`

---

## 4. Processo de Pull Request e Revisão Obrigatória (Peer Review)

1. **Abrir PR com Template**: Todo PR deve ser preenchido utilizando o `.github/PULL_REQUEST_TEMPLATE.md`, citando a Issue correspondente e os identificadores de requisitos (RF/RN/RNF).
2. **Revisão Obrigatória por Colega**: Nenhum PR é mesclado sem aprovação explícita de **pelo menos um outro desenvolvedor da equipe**.
3. **Pipeline Verde**: A suíte de testes e linters do GitHub Actions (`ci.yml`) deve passar com 100% de sucesso.
4. **Resolução de Conflitos**: O autor do PR é responsável por manter a branch atualizada com `git pull --rebase origin main`.

---

## 5. Regras de Migração de Banco de Dados (Alembic)

1. **Toda alteração estrutural no modelo relacional exige migração versionada**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "create_initial_schema"
   ```
2. **Reversibilidade**: Toda migração criada deve implementar adequadamente tanto a função `upgrade()` quanto a função `downgrade()`.
3. **Sem Migrações Destrutivas sem Aprovação Coletiva**: Renomear ou remover colunas existentes deve ser acordado previamente com o time para evitar perda de dados em homologação ou produção.

---

## 6. Convenções e Boas Práticas de Testes

1. **Isolamento de Infraestrutura Externa**: Os testes automatizados da fundação e unitários não devem depender de instâncias externas ativas de PostgreSQL, S3 real ou chaves de provedores de IA. Usamos SQLite in-memory assíncrono (`sqlite+aiosqlite:///:memory:`) e adaptadores em mock.
2. **Sem Dados Reais de Participantes**: Fixtures de teste devem utilizar dados sintéticos e fictícios. **Nunca utilize nomes, e-mails ou fotografias reais dos 83 estudantes ou 12 servidores nos testes**.
3. **Cobertura de Casos Críticos**:
   - Concorrência de cotas (tentativa de 21 reservas simultâneas para cota 20 — T-03).
   - Rejeição de mídias inválidas ou corrompidas (RF-08).
   - Isolamento de dados entre atlas de equipes distintas (RN-01).

---

## 7. Fronteiras Arquiteturais e Encapsulamento de Módulos

Para permitir desenvolvimento paralelo por 5 pessoas sem conflitos de merge ou acoplamento espaguete:
- **Routers Magros**: Endpoints em `app/api/` e nos módulos apenas validam entrada HTTP, verificam autenticação e chamam métodos do `service.py` do domínio correspondente.
- **Proibido Importar Models de Outros Domínios**: Se o módulo `curation` precisa saber se uma foto existe, ele chama um serviço público de `contributions`, nunca faz `db.query(PhotoRecord)` diretamente se `PhotoRecord` não pertence ao seu domínio.
- **Transactional Outbox para Ações Pesadas**: Operações demoradas (análise de imagem, IA, roteamento de percurso, geração de PDF/PNG) devem registrar um `JobRecord` no PostgreSQL para execução assíncrona pelo Worker.

---

## 8. Segurança e Privacidade (LGPD)

- **Sem Segredos em Código**: Segredos (`SECRET_KEY`, chaves de S3, tokens) devem residir exclusivamente em variáveis de ambiente `.env` locais (ignoradas no Git) ou no painel seguro do Railway.
- **Purga de Metadados Privados**: Arquivos derivados de exibição pública jamais devem conter tags EXIF ou coordenadas de GPS embutidas (RNF-02).
- **Sem Armazenamento Permanente no Disco Local**: Nenhum upload de foto ou arquivo de exportação pode ser armazenado permanentemente no sistema de arquivos local do contêiner. Todo armazenamento físico ocorre no Railway Buckets (compatível com S3).

---

## 9. Critérios de Conclusão de Tarefa (Definition of Done — DoD)

Uma tarefa só pode ser marcada como concluída se:
1. Atender integralmente aos critérios de aceite do requisito (RF/RN/RNF).
2. Estiver coberta por testes automatizados (unitários ou integração).
3. Respeitar as convenções de lint e formatação (`ruff` e `eslint`/`prettier` sem avisos).
4. Possuir migração de banco correspondente (se alterou entidades).
5. For revisada e aprovada por outro membro da equipe via Pull Request.
6. Não introduzir dependências ou serviços externos não documentados.

