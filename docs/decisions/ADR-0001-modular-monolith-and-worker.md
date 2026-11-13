# ADR-0001: Adoção de Monólito Modular com Worker Assíncrono Separado

- **Status**: Aprovado
- **Data**: 12 de novembro de 2026
- **Decisores**: Principal Software Architect & Atlas Santos Engineering Team
- **Contexto Técnico**: Especificação de Requisitos v1.2 / Análise Arquitetural v1.1

---

## 1. Contexto e Problema

O **Atlas Santos** é uma plataforma colaborativa para documentação cartográfica, fotográfica e reflexiva do Estudo do Meio em Santos (viagem realizada de 05 a 11 de outubro de 2026). O sistema atende **95 participantes** (83 estudantes e 12 servidores do IFSP Campus Araraquara), organizados em equipes com atlas específicos, totalizando uma referência de capacidade de aproximadamente **1.900 fotografias** (cota base de 20 fotos por participante). O prazo final de entrega homologada da aplicação é **04 de dezembro de 2026** (22 dias corridos a partir do início da fundação).

O desafio central do projeto não reside em suportar concorrência de milhões de acessos por segundo, mas sim em assegurar **consistência rigorosa e integridade de dados**:
- Gestão atômica de cotas de upload por participante e equipe.
- Máquina de estados desacoplada (processamento de imagem, revisão editorial pelo capitão, textos de reflexão e autorização de publicação).
- Reconstrução retrospectiva de percursos a pé a partir de fotografias geolocalizadas.
- Integração multimodal com IA para sugestão de descrições sem quebrar autoria humana.
- Geração pesada de artefatos de exportação (PDF, PNG, HTML, GeoJSON).

Precisamos escolher um estilo arquitetural que ofereça a máxima velocidade de desenvolvimento para uma equipe de 5 pessoas, garantindo ao mesmo tempo modularidade, facilidade de teste e estabilidade operacional.

---

## 2. Alternativas Analisadas

### Alternativa A: Microsserviços Distribuídos
Dividir a aplicação em múltiplos serviços autônomos implantados separadamente (ex: Serviço de Autenticação, Serviço de Mídia, Serviço de Curadoria, Serviço Cartográfico, Serviço de Exportação).
- *Desvantagens para o cenário*: Overhead desproporcional para 95 usuários e 1.900 fotos. Criaria problemas críticos de consistência eventual, orquestração de transações distribuídas (Sagas), latência de rede interna, duplicação de infraestrutura no Railway e alta fricção de comunicação para a equipe de 5 desenvolvedores com prazo de 22 dias.

### Alternativa B: Monólito Tradicional Síncrono (Tudo na API)
Executar todas as tarefas dentro do ciclo de vida das requisições HTTP da API.
- *Desvantagens para o cenário*: Operações intensivas em CPU e rede (extração EXIF, redimensionamento de imagens de até 15 MB/40 MP, chamadas de IA e renderização de PDF) bloqueariam o event loop da API e gerariam timeouts HTTP (504 Gateway Timeout), degradando severamente a experiência do usuário e violando o requisito RNF-05.

### Alternativa C: Monólito Modular com Worker Assíncrono Separado (Proposta Adotada)
Organizar o backend em um único monólito estruturado logicamente em domínios de negócio (`modules/`), compartilhando o mesmo repositório e modelos de dados, porém segregando a execução em **dois processos independentes**:
1. **API FastAPI**: Atende chamadas HTTP interativas do cliente React, responde com baixa latência (<1s p95) e valida autorizações.
2. **Worker Python**: Processa tarefas assíncronas em segundo plano consumindo uma fila persistida no PostgreSQL (`jobs`), com reinício resiliente e isolamento de falhas.

---

## 3. Decisão Arquitetural

Adotar a **Alternativa C — Monólito Modular com Worker Assíncrono Separado**.

1. **Separação Lógica em 10 Domínios**:
   - `identity`, `organization`, `contributions`, `media`, `curation`, `routes`, `ai`, `publication`, `exports`, `administration`.
2. **Dois Processos de Execução**:
   - Processo 1: `uvicorn app.main:app` (API Web).
   - Processo 2: `python -m app.worker.main` (Worker de processamento assíncrono).
3. **Padrão Transactional Outbox no PostgreSQL**:
   - Tarefas pesadas são registradas na tabela relacional `jobs` na mesma transação atômica que manipula o estado do domínio. O worker realiza polling com bloqueio de linha concorrente seguro (`FOR UPDATE SKIP LOCKED`).
4. **Armazenamento de Binários Desacoplado**:
   - Arquivos físicos residem exclusivamente no armazenamento de objetos compatível com S3 (Railway Buckets). O banco retém metadados e referências.

---

## 4. Consequências

### Positivas
- **Velocidade de Desenvolvimento**: A equipe de 5 pessoas trabalha em um único repositório, com modelos de dados consistentes e sem a complexidade de gerenciar múltiplos repositórios e deploys distribuídos.
- **Integridade Transacional (ACID)**: Cotas de envio, vínculos e auditoria são garantidos nativamente pelo PostgreSQL.
- **Resiliência Operacional**: Se o worker cair ou reiniciar durante o processamento de uma imagem ou exportação, o estado da tarefa permanece salvo no banco e pode ser retomado sem perda de dados (RNF-06).
- **Escalabilidade Vertical e Horizontal Simples**: A API e o Worker podem ser escalados de forma independente no Railway conforme o perfil de carga.

### Negativas e Riscos Mitigados
- **Risco de Acoplamento Acidental entre Módulos**:
  - *Mitigação*: Estabelecer regras claras de encapsulamento no `CONTRIBUTING.md` e `docs/architecture/domain-boundaries.md`. É expressamente proibido importar modelos de persistência ou tabelas privadas de outro módulo; toda comunicação intermódulo deve ser feita via serviços públicos ou contratos de interface.
- **Concorrência de Workers no Banco**:
  - *Mitigação*: Uso de `SKIP LOCKED` do PostgreSQL no dispatcher do worker, prevenindo condições de corrida e processamento duplicado (RNF-14).

