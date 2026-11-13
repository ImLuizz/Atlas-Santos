# Backlog Inicial e Rastreabilidade de Requisitos — Atlas Santos

Este documento gerencia o backlog do **Atlas Santos**, baseado na Especificação de Requisitos v1.2. O planejamento é dimensionado para uma equipe de 5 desenvolvedores com prazo final improrrogável em **04 de dezembro de 2026**.

> [!IMPORTANT]
> **Convenção de Marcação de Status**:
> - `[x]` Concluído com evidência comprovada e validada.
> - `[ ]` Não iniciado ou em planejamento.
> - **NÃO marcar funcionalidades como concluídas sem código funcional, migração e testes aprovados**.

---

## 1. Fase 0: Fundação da Arquitetura e Engenharia (12–14/11/2026)

- [x] **Configuração Base do Repositório**: Monorepo com diretórios estruturados para backend, frontend, worker e docs.
- [x] **Políticas de Governança e CI**:
  - [x] `.editorconfig` e `.gitignore` com proteção contra vazamento de credenciais e arquivos temporários.
  - [x] GitHub Actions CI (`ci.yml`) validando lint, formatação e testes unitários/contratuais de backend e frontend.
  - [x] Templates de Issues (`[BUG]`, `[FEAT]`) e Pull Request (`PULL_REQUEST_TEMPLATE.md`).
- [x] **Fundação do Backend (FastAPI + SQLAlchemy + Alembic)**:
  - [x] Configuração centralizada tipada via Pydantic Settings (`app/core/config.py`).
  - [x] Engine e sessão assíncrona SQLAlchemy (`app/db/session.py`).
  - [x] Tabela de controle de tarefas assíncronas `jobs` (Transactional Outbox — RNF-06, ADR-0003).
  - [x] Inicialização do Alembic (`alembic.ini`, `alembic/env.py`).
  - [x] Endpoints de health check operacional (`/health` e `/api/v1/health`).
  - [x] Suíte de testes automatizados com Pytest (`unit/`, `integration/`, `contract/`).
- [x] **Fundação do Worker Python**:
  - [x] Processo assíncrono independente (`app/worker/main.py`) com dispatcher concorrente e suporte a modo single-pass.
- [x] **Fundação do Frontend (React + Vite + Tailwind CSS)**:
  - [x] Configuração do bundler Vite, ESLint e Prettier.
  - [x] Configuração de Tailwind CSS com esquema de cores institucional.
  - [x] Biblioteca de cartografia `react-leaflet` e `leaflet` configurada com coordenadas de Santos/SP.
  - [x] Suíte de testes com Vitest e Testing Library.
- [x] **Documentação Arquitetural e Acordos**:
  - [x] Visão Geral da Arquitetura (`docs/architecture/overview.md`).
  - [x] Máquina de Estados e Dimensões Independentes (`docs/architecture/state-machine.md`).
  - [x] Fronteiras de Domínio e Modelo Conceitual (`docs/architecture/domain-boundaries.md`).
  - [x] ADR-0001 (Monólito Modular com Worker Assíncrono).
  - [x] ADR-0002 (Stack Tecnológica Oficial).
  - [x] ADR-0003 (Estratégia de Dados, Outbox e Armazenamento).
  - [x] Acordos de Trabalho da Equipe (`docs/team/working-agreements.md`).

---

## 2. Fase 1: Identidade, Domínio Central e Conciliação (15–18/11/2026) — Prioridade P1

### 2.1 Acesso e Identidade (Módulo `identity`)
- [ ] Implementar modelo de dados de participante (`Participant`) e conta (`UserAccount`).
- [ ] Implementar fluxo de provisionamento por convite com token seguro de uso único (RF-01, D-03).
- [ ] Implementar autenticação baseada em sessão com cookies HTTP-only seguros, expiração e logout (RF-02, RNF-01).
- [ ] Teste de isolamento de sessão e revogação administrativa (Cenário T-01).

### 2.2 Organização, Equipes e Vínculos (Módulo `organization`)
- [ ] Implementar entidades `Team`, `Atlas` (relação 1:1, RN-01) e vínculos `Membership` (RF-03).
- [ ] Implementar regras de papel: participante, capitão do atlas e administração (RF-03).
- [ ] Implementar bloqueio de acesso cruzado: troca de ID na requisição não permite visualizar outro atlas não autorizado (RF-03, RN-01).

### 2.3 Administração e Integração IF-Arbitra (Módulo `administration`)
- [ ] Implementar ingestão e validação de schema JSON administrativo versionado do IF-Arbitra (RF-04, RNF-13).
- [ ] Implementar prévia administrativa exibindo inclusões, atualizações, conflitos e pessoas sem vínculo (RF-04).
- [ ] Implementar confirmação idempotente de lote de importação preservando IDs internos e autoria (RF-05, RNF-14).
- [ ] Implementar relatório de conciliação formal demonstrando a inclusão dos 83 estudantes e 12 servidores (RF-06, RN-02, Cenário T-02).
- [ ] Trilha de auditoria operacional para ações críticas administrativas (RF-29).

---

## 3. Fase 2: Mídia, Upload Direto e Cotas Atômicas (19–21/11/2026) — Prioridade P1

### 3.1 Gestão de Cotas e Uploads (Módulos `organization` e `media`)
- [ ] Implementar reserva de cota com lock pessimista no PostgreSQL garantindo atomicidade sob concorrência (RF-09, RN-03, RN-05).
- [ ] Implementar teste de estresse de concorrência: 21 reservas simultâneas para cota 20 aceitam estritamente 20 (Cenário T-03).
- [ ] Implementar endpoint de emissão de URLs pré-assinadas para envio direto ao Railway Buckets/S3 com TTL de 10 minutos (RF-08, RN-03).
- [ ] Implementar finalização de upload com validação de tamanho (máx 15 MB), integridade e formato (JPEG, PNG, WebP) (RF-08, RNF-07).
- [ ] Implementar política de expiração de reservas vencidas (30 minutos) e estorno atômico de cota (RN-04).

### 3.2 Processamento de Imagens e Metadados no Worker (Módulo `media` & Worker)
- [ ] Implementar handler de processamento de imagem com Pillow limitando consumo de memória (RF-10, ADR-02).
- [ ] Correção automática de rotação/orientação com base no EXIF (RF-10).
- [ ] Geração assíncrona de miniatura (até 480px) e derivado de exibição (até 2048px) (RF-10, Seção 9).
- [ ] Remoção estrita de coordenadas GPS e metadados privados dos derivados públicos (RF-10, RNF-02, Cenário T-04).
- [ ] Preservação de arquivo original em área privada com acesso restrito (RNF-02).
- [ ] Rotina periódica de reconciliação de arquivos órfãos entre banco e bucket (RNF-16).

### 3.3 Contribuições e Metadados (Módulo `contributions`)
- [ ] Implementar painel do participante com visualização de cota disponível, uso e fotos enviadas (RF-07).
- [ ] Implementar captura e correção manual de localização para fotos sem GPS (RF-11, RN-10).
- [ ] Implementar correção de fuso horário e dia da atividade (05 a 11/10/2026) (RF-11, RN-09).

---

## 4. Fase 3: Curadoria, Exploração Cartográfica e Exportações Visuais (22–25/11/2026) — Marco P1

### 4.1 Mesa de Curadoria Editorial do Capitão (Módulo `curation`)
- [ ] Fila de análise do atlas atribuído com filtros por pendência e dia (RF-12).
- [ ] Ações editoriais: aprovação, solicitação de ajuste e rejeição com justificativa obrigatória (RF-12).
- [ ] Autoaprovação do capitão permitida mediante registro auditado (RF-12, RN-06, Cenário T-05).
- [ ] Ciclo de revisão independente entre mídia e textos: aprovação da foto não exige reflexão e vice-versa (RF-13, RN-08).
- [ ] Fluxo de correção e reenvio pelo participante sem perder autoria nem consumir cota duplicada (RF-14).
- [ ] Fluxo de retirada, suspensão e exclusão por privacidade com invalidação em cascata (RF-15, RN-16, Cenário T-11).

### 4.2 Exploração do Atlas: Mapa e Galeria (Módulo `contributions` e Frontend)
- [ ] Interface com mapa interativo (React-Leaflet) e galeria sincronizada (RF-16, Cenário T-06).
- [ ] Filtros combinados por equipe, dia (05 a 11/10/2026) e tema pedagógico (RF-16).
- [ ] Fotos sem localização acessíveis exclusivamente na galeria (RF-16, RN-10).
- [ ] Detalhe do registro: visualização de foto, autoria autorizada e reflexão aprovada sem campos privados vazados (RF-17).
- [ ] Responsividade mobile e acessibilidade por teclado testadas em 360px (RNF-04).

### 4.3 Exportações Visuais P1: PDF e PNG (Módulo `exports` & Worker)
- [ ] Handler do worker para geração de caderno em PDF (formato A4) com fotos, mapa, créditos OSM e legendas (RF-26).
- [ ] Handler do worker para geração de painel resumo em PNG (2400x1600px) (RF-26).
- [ ] Inclusão explícita de aviso de "percurso reconstruído pelas fotos" e atribuição completa do OpenStreetMap (RF-26, RNF-09).
- [ ] Controle assíncrono de status e expiração da exportação hospedada (7 dias) (RF-28).

---

## 5. Fase 4: Inteligência, Reconstrução e Exportações P2 (26–27/11/2026) — Marco P2

### 5.1 Reconstrução Pedestre de Percursos (Módulo `routes` & Worker)
- [ ] Adaptador desacoplado para serviço de roteamento pedestre (RF-18, RN-11, ADR-06).
- [ ] Reconstrução retrospectiva por dia conectando pontos fotográficos elegíveis (RF-18).
- [ ] Interface de ajuste do capitão: ordenar fotos, separar trechos e adicionar pontos intermediários (RF-19, RN-12).
- [ ] Tratamento defensivo de percursos: 0 pontos, 1 ponto, lacunas temporais (>2h) ou espaciais (>3km) e falha externa do roteador (RF-20, Cenário T-07).

### 5.2 Descrições por IA e Módulo Olhares sobre Santos (Módulo `ai`)
- [ ] Adaptador para modelo multimodal de IA enviando derivado sem EXIF e reflexão aprovada (RF-21, RNF-02, ADR-06).
- [ ] Geração de até 3 sugestões curtas de descrição (até 600 caracteres) com registro de consumo de tokens (RF-22, RNF-08, Cenário T-08).
- [ ] Interface para o participante/capitão escolher, editar ou descartar sugestão de IA com aprovação humana obrigatória (RF-23, RN-14).
- [ ] Módulo Olhares sobre Santos: catálogo de temas inspirados em *Sonho Manifesto* e reflexões opcionais (RF-24, RF-25, Cenário T-09).

### 5.3 Exportações Estendidas P2: HTML e GeoJSON (Módulo `exports`)
- [ ] Geração de arquivo HTML autocontido e portátil com fotos e metadados autorizados (RF-27).
- [ ] Geração de arquivo GeoJSON padronizado (longitude antes de latitude) com geometria do percurso e pontos (RF-27, Cenário T-10).
- [ ] Validação estrita de não vazamento de identidade privada, dados EXIF ou chaves internas de storage (RF-27).

---

## 6. Fase 5: Homologação e Estabilização (28/11 a 02/12/2026)

- [ ] Execução e coleta formal de evidências dos 12 cenários de homologação (T-01 a T-12).
- [ ] Ensaio de carga simulando 25 sessões, 10 uploads simultâneos e 2 exportações (meta: p95 < 1s, erros < 1% — RNF-05).
- [ ] Teste de desastre e recuperação: restauração de banco e reaplicação automática de ordens de retirada de privacidade (RF-15, RNF-11).
- [ ] Validação de auditoria completa e segurança em navegadores mobile (RNF-04, RF-29).

---

## 7. Fase 6: Implantação Final e Entrega (03–04/12/2026)

- [ ] Execução de migrações finais do banco PostgreSQL de produção no Railway.
- [ ] Publicação das versões finais da API, Worker e Frontend estático.
- [ ] Repasse de credenciais administrativas, documentação e roteiro operacional à coordenação.
- [ ] Assinatura do termo de aceite da aplicação.

---

## 8. Decisões Institucionais e Técnicas Pendentes (D-01 a D-10)

Estas decisões estão sob análise das partes interessadas e devem ser resolvidas nas datas recomendadas:

| ID | Descrição da Pendência | Responsável Sugerido | Prazo Recomendado | Impacto Técnico / Hipótese Adotada na Fundação |
| :--- | :--- | :--- | :--- | :--- |
| **D-01** | Confirmar lista final dos 95, composição das equipes, capitães e versão do IF-Arbitra | Coordenação e responsável pelos dados | 14/11/2026 | Arquitetura preparada para receber JSON administrativo pontual com conciliação formal. |
| **D-02** | Confirmar política de consumo de cota por fotos rejeitadas, exclusão e redução de cota | Produto e equipe técnica | 14/11/2026 | Proposta adotada: fotos rejeitadas ocupam cota até exclusão; exclusão libera vaga uma vez; valores parametrizáveis. |
| **D-03** | Definir procedimento exato de provisionamento e recuperação de acessos | Coordenação e responsável técnico | 14/11/2026 | Proposta adotada: convites com tokens aleatórios criptográficos de uso único, sem cópia de senhas do IF-Arbitra. |
| **D-04** | Definir regras de audiência, autoria pública, precisão geográfica e envio de dados a terceiros (LGPD/menores) | Coordenação e responsáveis institucionais | Antes dos dados reais | Por padrão na fundação, audiência é restrita à equipe autenticada e derivados de imagem expurgam EXIF/GPS. |
| **D-05** | Definir se disponibilização requer comando manual após aprovação e ações delegadas ao capitão | Produto e coordenação | 18/11/2026 | Máquina de estados separa estritamente aprovação editorial e condições de disponibilização. |
| **D-06** | Validar quantidade, extensão das descrições por IA, perguntas pedagógicas e catálogo de temas | Coordenação pedagógica e capitães | 24/11/2026 | Parâmetros configuráveis: até 3 alternativas com até 600 caracteres; temas inspirados em *Sonho Manifesto*. |
| **D-07** | Escolher provedores de IA, tiles cartográficos e roteamento, fixando tetos de orçamento | Equipe técnica e operação | 18/11/2026 | Camada de adaptadores desacoplada (`integrations/`) permite plugar ou trocar fornecedores sem alterar o domínio. |
| **D-08** | Aprovar metas de ensaio de carga, lista de navegadores/dispositivos e dataset de homologação | Equipe técnica e revisor | 24/11/2026 | Ambiente e suíte de testes preparados para mock e dados sintéticos dos 95 participantes. |
| **D-09** | Definir prazos de retenção de dados, política de exclusão definitiva e metas de RPO/RTO de backup | Coordenação e operação | 24/11/2026 | Metas propostas documentadas: backup diário (RPO 24h, RTO 8h); reaplicação obrigatória de retiradas. |
| **D-10** | Confirmar responsável institucional pelo aceite, disponibilidade para piloto e gestão de mudanças | Coordenação e equipe | 24/11/2026 | Processo formal de homologação estruturado em torno dos 12 cenários de conclusão (T-01 a T-12). |

