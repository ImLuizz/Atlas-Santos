# Política de Backup, Retenção e Reconciliação — Atlas Santos

Este documento detalha os procedimentos e salvaguardas para proteção do banco de dados, arquivos de mídia e tratamento de dados dos 95 participantes do Atlas Santos (RNF-11, RNF-16).

---

## 1. Estratégia de Backup Independente (RNF-11)

A proteção do acervo opera em duas trilhas independentes:

1. **Backup Relacional do PostgreSQL**:
   - Snapshots diários automatizados gerenciados pelo Railway com retenção de 7 dias.
   - Dump lógico periódico (`pg_dump`) antes de migrações estruturais do Alembic.
   - **Meta proposta (D-09)**: RPO (perda máxima de dados) de até 24 horas; RTO (tempo de recuperação) de até 8 horas.
2. **Proteção do Armazenamento de Objetos (Railway Buckets)**:
   - Os arquivos originais e derivados residem em balde privado com versionamento de objetos ativado na nuvem.
   - Fotos originais são marcadas como privadas com acesso restrito à aplicação.

---

## 2. Reconciliação Periódica Banco-Bucket (RNF-16)

Para evitar vazamento de armazenamento ou custos desnecessários com arquivos órfãos decorrentes de uploads interrompidos pelo navegador:

1. Uma tarefa periódica assíncrona executada pelo Worker compara:
   - Objetos presentes no Railway Bucket.
   - Registros com status ativo na tabela `media_assets` do PostgreSQL.
2. **Critério de Limpeza**:
   - Arquivos temporários sem confirmação no banco há mais de 24 horas são expurgados do bucket.
   - Reservas de cotas expiradas sem arquivo correspondente são estornadas automaticamente para o participante.

---

## 3. Preservação de Retiradas de Privacidade em Restaurações

Conforme exigido no critério de aceite do **RF-15**:
> *"Uma restauração de backup reaplica as retiradas registradas."*

Para garantir conformidade com a LGPD e privacidade de eventuais menores de idade:
- A tabela de log de retiradas (`content_takedowns`) mantém um registro imutável com hash da mídia e ID do recurso.
- Ao restaurar um dump antigo do banco de dados em caso de desastre, o script de pós-restauração lê a trilha de auditoria externa de retiradas e reaplica o status `excluido` ou `suspenso` em qualquer recurso restaurado que tenha sido objeto de solicitação de privacidade confirmada.

