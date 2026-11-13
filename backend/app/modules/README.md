# Arquitetura dos Módulos de Domínio — Atlas Santos

Este diretório contém os **10 domínios de negócio** do Atlas Santos, estruturados de acordo com o padrão **Monólito Modular** (ver [ADR-0001](../../../docs/decisions/ADR-0001-modular-monolith-and-worker.md)).

## Regras de Isolamento e Fronteiras Arquiteturais

Para permitir que a equipe de 5 desenvolvedores trabalhe em paralelo sem acoplamento indevido, os módulos seguem regras estritas:

1. **Encapsulamento de Dados**: Nenhum módulo pode realizar consultas diretas nas tabelas de banco (`models`) de outro módulo.
2. **Interface Pública**: A comunicação entre módulos deve ser realizada por serviços públicos de domínio (`service.py`), schemas de contrato (`schemas.py`) ou publicação/consumo de eventos internos (`events.py`).
3. **Routers Livres de Regras de Negócio**: Arquivos `router.py` (FastAPI) atuam apenas como adaptadores HTTP: realizam validação de payload, autenticação e delegam a execução para o serviço do domínio.
4. **Persistência de Tarefas no Worker**: Ações pesadas (processamento de imagem, chamadas a modelos de IA, roteamento de ruas e geração de PDF/PNG/HTML/GeoJSON) devem registrar uma tarefa na tabela `jobs` (Transactional Outbox) e delegar a execução assíncrona ao Worker.

---

## Estrutura Padronizada por Módulo

Conforme as funcionalidades forem implementadas nas fases subsequentes (Fase 1 a Fase 4), cada módulo adotará a seguinte anatomia:

```text
modules/<domain_name>/
├── __init__.py       # Exporta a interface pública e schemas do módulo
├── models.py         # Entidades SQLAlchemy de persistência exclusivas do domínio
├── schemas.py        # Schemas Pydantic para validação de entrada e saída
├── service.py        # Casos de uso e regras de negócio do domínio
├── router.py         # Endpoints FastAPI vinculados ao prefixo da API
└── README.md         # Documentação de escopo, responsabilidades e invariantes
```

---

## Mapa de Domínios do Sistema

| Módulo | Responsabilidade Principal | Requisitos Principais |
| :--- | :--- | :--- |
| [`identity`](./identity/README.md) | Usuários, autenticação por cookie, sessões e revogação | RF-01, RF-02, RNF-01 |
| [`organization`](./organization/README.md) | Equipes, atlas, vínculos (membros), papéis e gestão de cotas | RF-03, RN-01, RN-02, RN-03 |
| [`contributions`](./contributions/README.md) | Registros fotográficos lógicos, submissões e metadados de captura | RF-07, RF-11, RN-09, RN-10 |
| [`media`](./media/README.md) | URLs temporárias, upload direto S3, processamento EXIF e miniaturas | RF-08, RF-09, RF-10, RNF-07 |
| [`curation`](./curation/README.md) | Fila de curadoria do capitão, revisões e auditoria de decisões | RF-12, RF-13, RF-14, RN-06 |
| [`routes`](./routes/README.md) | Reconstrução de percursos prováveis a pé pelas fotos e ajustes | RF-18, RF-19, RF-20, RN-11, RN-12 |
| [`ai`](./ai/README.md) | Análise multimodal (imagem sem EXIF + reflexão) e sugestões de texto | RF-21, RF-22, RF-23, RN-14 |
| [`publication`](./publication/README.md) | Critérios de elegibilidade, disponibilização por audiência e suspensão | RF-15, RF-30, RN-07, RN-15, RN-16 |
| [`exports`](./exports/README.md) | Geração de arquivos exportáveis: PDF/PNG (P1), HTML/GeoJSON (P2) | RF-26, RF-27, RF-28, RNF-09 |
| [`administration`](./administration/README.md) | Importação e conciliação do IF-Arbitra e trilhas de auditoria | RF-04, RF-05, RF-06, RF-29 |

