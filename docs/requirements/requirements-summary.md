# Resumo dos Requisitos do Sistema — Atlas Santos

Este documento consolida os requisitos funcionais, regras de negócio e requisitos não funcionais extraídos da **Especificação de Requisitos do Atlas Santos (Versão 1.2)**.

---

## 1. Universo e Parâmetros Confirmados
- **Participantes**: 95 pessoas (83 estudantes e 12 servidores do IFSP Campus Araraquara).
- **Período da Viagem**: 05 a 11 de outubro de 2026 (fuso `America/Sao_Paulo`).
- **Unidade de Organização**: 1 Atlas por Equipe (não existe entidade "projeto").
- **Cota Base**: Padrão de 20 fotografias por participante em cada atlas autorizado (capacidade de referência: 1.900 fotos).
- **Prazo de Entrega**: Aplicação homologada e entregue até **04/12/2026**.

---

## 2. Requisitos Funcionais (RF-01 a RF-30)

| ID | Prioridade | Nome / Descrição | Critério de Aceite Principal |
| :--- | :--- | :--- | :--- |
| **RF-01** | P1 | Provisionar acesso dos participantes | Estudantes e servidores acessam por convite controlado sem copiar senhas do IF-Arbitra; não autorizados são bloqueados. |
| **RF-02** | P1 | Autenticar e encerrar sessões | Login libera apenas atlas autorizados; logout/expiração encerra leitura e escrita privadas imediatamente. |
| **RF-03** | P1 | Administrar equipes e vínculos | Gestão de equipes, atlas 1:1, capitães e cotas; servidor responsável não ganha função editorial automática. |
| **RF-04** | P1 | Validar importação do IF-Arbitra | Recebe JSON administrativo e gera prévia com inclusões, atualizações e conflitos sem alterar o banco definitivo. |
| **RF-05** | P1 | Confirmar e repetir importações | Confirmação idempotente que preserva IDs internos e histórico prévio de fotos mesmo se o IF-Arbitra estiver offline. |
| **RF-06** | P1 | Conciliar as 95 pessoas | Relatório administrativo demonstra formalmente a conciliação dos 83 estudantes e 12 servidores sem descartar ninguém. |
| **RF-07** | P1 | Apresentar painel do participante | Mostra atlas atual, cota, uso, reservas ativas, fotos enviadas, status editoriais e devolutivas. |
| **RF-08** | P1 | Enviar arquivos com recuperação | Upload direto ao bucket com progresso e retentativa isolada de falhas; validação estrita no servidor. |
| **RF-09** | P1 | Aplicar cota de forma atômica | Reserva concorrente e finalização respeitam o limite no PostgreSQL; impossível ultrapassar cota por concorrência. |
| **RF-10** | P1 | Processar imagens e extrair EXIF | Gera miniatura (480px) e exibição (2048px); remove GPS dos derivados públicos; preserva original privado. |
| **RF-11** | P1 | Corrigir localização e tempo | Permite associar coordenadas manuais a fotos sem GPS e ajustar hipóteses de fuso e dia da viagem. |
| **RF-12** | P1 | Revisar fotografias | Capitão acessa fila do atlas e aprova, rejeita ou solicita ajustes com justificativa clara; auditado. |
| **RF-13** | P1 | Revisar textos e temas separadamente | Ciclo de revisão independente: foto pode ser aprovada sem texto; rejeição de reflexão não desfaz foto. |
| **RF-14** | P1 | Corrigir e reenviar após devolutiva | Participante ajusta e ressubmete sem perder autoria nem gastar cota duplicada. |
| **RF-15** | P1 | Retirar e excluir conteúdo | Exclusão pelo autor, suspensão pelo capitão ou moderação administrativa; invalida artefatos dependentes. |
| **RF-16** | P1 | Explorar mapa e galeria | Filtros combinados por equipe, dia e tema; fotos sem GPS aparecem na galeria normalmente. |
| **RF-17** | P1 | Consultar um registro | Modal ou gaveta detalhada com foto, autor permitido, reflexão aprovada e descrição sem expor campos privados. |
| **RF-18** | P1 | Sugerir ruas entre pontos fotográficos | Roteamento pedestre entre fotos conectáveis; resultado identificado como "percurso reconstruído pelas fotos". |
| **RF-19** | P1 | Ajustar e aprovar um percurso | Capitão seleciona fotos-fonte, ajusta ordem, separa trechos e aprova versão vinculada às fotos de origem. |
| **RF-20** | P1 | Tratar percursos incompletos | Trata 0 pontos, 1 ponto, horários empatados e falhas do roteador sem inventar caminhos fictícios. |
| **RF-21** | P1 | Analisar imagem e reflexão | Modelo multimodal recebe imagem sem EXIF e reflexão aprovada para análise de conteúdo visual. |
| **RF-22** | P1 | Sugerir alternativas de descrição | Sugere até 3 opções curtas com controle de tokens e identificação de autoria por IA; lida com ambiguidades. |
| **RF-23** | P1 | Escolher e revisar descrições de IA | Usuário edita/escolhe sugestão; disponibilização final exige aprovação formal do capitão. |
| **RF-24** | P1 | Registrar olhares e administrar temas | Temas pedagógicos (inspiração em *Sonho Manifesto*) e reflexões opcionais independentes. |
| **RF-25** | P1 | Integrar reflexões aos canais autorizados | Apenas reflexões aprovadas entram em exportações ou como insumo de IA para publicação. |
| **RF-26** | P1 | Gerar PDF e PNG | Exportação real de caderno A4 (PDF) e painel resumido (PNG) com mapa, fotos, créditos e aviso de percurso inferido. |
| **RF-27** | P2 | Gerar HTML e GeoJSON | HTML portátil e GeoJSON estrito (longitude antes de latitude) sem expor metadados privados. |
| **RF-28** | P1/P2 | Acompanhar e autorizar exportações | Tarefas persistidas na fila do worker com validação de permissão no pedido e no download. |
| **RF-29** | P1 | Consultar auditoria e operação | Painel administrativo monitora logs de mutação, cotas, jobs em andamento e saúde geral sem expor segredos. |
| **RF-30** | P1 | Gerenciar audiência e privacidade | Configuração de audiência da equipe e atendimento imediato de solicitações de suspensão/retirada de dados. |

---

## 3. Regras de Negócio Fundamentais (RN-01 a RN-16)

- **RN-01 (Atlas por Equipe)**: Cada equipe tem seu atlas exclusivo; não há entidade "projeto".
- **RN-02 (Universo de 95 Participantes)**: 83 estudantes e 12 servidores devem estar conciliados; ausência temporária no IF-Arbitra não remove participante do acervo.
- **RN-03 (Cota do Vínculo)**: 20 fotos por participante em cada atlas autorizado, sem reinício diário, aplicada no PostgreSQL com URLs pré-assinadas.
- **RN-04 (Consumo e Liberação)**: Fotos pendentes, aprovadas e rejeitadas ocupam cota; exclusão pelo autor libera cota; rejeição não libera automaticamente (confirmar em D-02).
- **RN-05 (Concorrência e Repetição)**: Transações atômicas impedem ultrapassar a cota por requisições simultâneas.
- **RN-06 (Curadoria Obrigatória)**: Nenhuma foto é disponibilizada sem aprovação do capitão autorizado; autoaprovação do capitão é auditada.
- **RN-07 (Aprovação e Divulgação Independentes)**: Aprovação editorial é distinta de autorização de divulgação e da política de audiência.
- **RN-08 (Revisões Independentes)**: Mídia, legendas, reflexões e percursos têm ciclos de vida separados. Foto pode ser publicada sem texto.
- **RN-09 (Instante de Captura)**: Ordenação baseada no instante de captura corrigido pelo EXIF/autor, nunca na hora do upload.
- **RN-10 (Ausência de Metadados)**: Fotos sem GPS participam da galeria; para entrar no mapa exigem localização informada e revisada.
- **RN-11 (Ruas Prováveis)**: O percurso conecta referências por perfil pedestre real; rotulado como "reconstruído pelas fotos"; distância é estimativa.
- **RN-12 (Separação da Equipe)**: Capitão pode separar trechos quando subgrupos caminharam por vias distintas.
- **RN-13 (Reflexão Opcional)**: Ausência de reflexão ou tema não penaliza participante nem impede aprovação da foto.
- **RN-14 (Autoria e IA)**: A reflexão humana é estritamente diferenciada das sugestões da IA; a IA é tratada como não confiável.
- **RN-15 (Seleção Comum aos Canais)**: Regras de elegibilidade idênticas entre mapa, galeria, IA e exportações.
- **RN-16 (Retirada e Dependências)**: Suspensão ou exclusão invalida descrições, percursos e exportações geradas dependentes.

---

## 4. Requisitos Não Funcionais (RNF-01 a RNF-16)

- **RNF-01 (Autorização e Sessão)**: Validação centralizada no servidor; HTTPS em produção; cookies seguros HTTP-only.
- **RNF-02 (Privacidade por Padrão)**: Remoção de EXIF/GPS de derivados divulgáveis; originais mantidos em área privada.
- **RNF-03 (Integridade e Rastreabilidade)**: Transações ACID no PostgreSQL; rastreamento de revisões e auditoria.
- **RNF-04 (Celular e Acessibilidade)**: Funcional em 360px de largura sem rolagem horizontal; navegação por teclado e contraste.
- **RNF-05 (Desempenho e Capacidade)**: P95 de leituras < 1s; processamento pesado assíncrono sem bloquear consultas HTTP.
- **RNF-06 (Recuperação de Tarefas)**: Tarefas assíncronas persistidas no PostgreSQL com recuperação automática após reinício do worker.
- **RNF-07 (Segurança de Arquivos e Textos)**: Validação de assinatura MIME e limites (15 MB/40 MP); proteção contra scripts e prompt injection.
- **RNF-08 (Custos e Tetos)**: Tetos configuráveis para IA, roteamento e exportações com bloqueio automático ao atingir o limite.
- **RNF-09 (Cartografia e Atribuição)**: Créditos obrigatórios OpenStreetMap em tela e em impressões PDF.
- **RNF-10 (Implantação Reproduzível)**: Configurações fixadas, migrações versionadas com Alembic e segregação de ambientes no Railway.
- **RNF-11 (Backup e Retenção)**: Proteção separada para banco e bucket S3 com metas operacionais a validar em D-09.
- **RNF-12 (Contratos e Observabilidade)**: OpenAPI padronizado; respostas de erro com correlation ID e sem stack traces vazados.
- **RNF-13 (Versionamento Explícito de Contratos)**: Esquemas de dados e artefatos salvos contêm versão explícita do contrato.
- **RNF-14 (Idempotência para Operações Mutáveis)**: Requisições com chave de idempotência repetidas não duplicam reservas ou cotas.
- **RNF-15 (Rastreabilidade de Dependências)**: Grafo de dependência de revisões para permitir invalidação automática em cascata.
- **RNF-16 (Reconciliação Banco-Bucket)**: Rotina periódica no worker para expurgar arquivos órfãos sem referência no banco há mais de 24h.

