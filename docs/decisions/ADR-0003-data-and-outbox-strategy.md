# ADR-0003: Estratégia de Dados, Transactional Outbox e Armazenamento

- **Status**: Aprovado
- **Data**: 12 de novembro de 2026
- **Decisores**: Principal Software Architect & Atlas Santos Engineering Team
- **Contexto Técnico**: RNF-03, RNF-06, RNF-14, RNF-16 e Seções 7 e 8 dos Requisitos

---

## 1. Contexto

O Atlas Santos gerencia acervos fotográficos, metadados espaciais e temporais, percursos e tarefas pesadas assíncronas. Para manter os custos operacionais baixos e a arquitetura simples, precisamos definir:
1. Onde e como enfileirar tarefas de processamento de fotos, IA e exportações.
2. Como lidar com o fluxo de upload de arquivos pesados (até 15 MB por imagem).
3. Por que adiar a introdução de mensagerias dedicadas (Redis, RabbitMQ, Kafka).

---

## 2. Decisão

### 2.1 PostgreSQL como Única Fonte de Verdade
O banco de dados relacional PostgreSQL gerencia todo o estado estruturado da aplicação: participantes, equipes, atlas, cotas, registros lógicos de fotos, revisões editoriais, trilhas de auditoria e a fila de processamento.

### 2.2 Transactional Outbox na Tabela `jobs`
Em vez de configurar um cluster de Redis ou broker RabbitMQ nesta fase, adotamos o padrão **Transactional Outbox** persistindo tarefas na tabela `jobs` do PostgreSQL:
- Ao finalizar um upload ou solicitar uma exportação, o registro de negócio e a tarefa assíncrona são gravados na mesma transação ACID.
- Isso elimina o risco de estados órfãos (ex: foto registrada no banco, mas evento perdido no broker devido a falha de rede).
- O Worker consulta a tabela com `SELECT ... FOR UPDATE SKIP LOCKED`, garantindo concorrência sem bloqueio entre instâncias.

### 2.3 Upload Direto ao Bucket via URLs Pré-assinadas
O fluxo de envio de mídia ocorre diretamente entre o navegador do participante e o armazenamento S3 (Railway Buckets):
1. **Reserva**: O cliente requisita uma URL de upload à API. A API valida atômica e pontualmente a cota de fotos do vínculo no PostgreSQL.
2. **Emissão**: A API gera uma URL pré-assinada com validade de 10 minutos e chave de objeto única.
3. **Upload**: O cliente envia os bytes diretamente ao bucket S3.
4. **Finalização**: O cliente notifica a API, que valida o tamanho e integridade do arquivo e cria o `JobRecord` de processamento de imagem na tabela `jobs`.
5. **Nenhum arquivo de usuário é gravado no disco local do servidor**.

### 2.4 Justificativa para NÃO Adotar Redis / RabbitMQ / Kafka no Momento
- **Escala de Carga**: Com 95 participantes e volume de ~1.900 fotos geradas ao longo de semanas, o throughput máximo esperado é de dezenas de uploads simultâneos, volume que uma tabela PostgreSQL indexada atende com folga (suporta centenas de operações por segundo sem degradação).
- **Simplicidade de Operação**: Evita a necessidade de configurar, monitorar, manter backups e pagar por instâncias extras de Redis/RabbitMQ no Railway.
- **Transacionalidade Garantida**: Elimina a necessidade de protocolos de consenso distribuído (2-phase commit).

---

## 3. Consequências

- **Alta Confiabilidade**: O banco garante consistência mesmo com interrupções abruptas do worker ou deploy da aplicação (RNF-06).
- **Economia Operacional**: Zero custos com servidores adicionais de fila.
- **Evolução Futura**: Se o volume crescer no futuro para dezenas de milhares de usuários em outras edições do Estudo do Meio, a interface do dispatcher está isolada e permitirá plugar Celery com Redis ou RabbitMQ sem alterar os módulos de domínio.

