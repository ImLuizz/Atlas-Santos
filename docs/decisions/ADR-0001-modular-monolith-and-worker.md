# ADR-0001 · API modular e worker separado

Registro original de 12/11/2026. A organização em módulos e a separação de processos são decisões de implementação presentes no repositório. Os comportamentos a demonstrar são os descritos na especificação de requisitos.

## Contexto

Durante o estudo do meio participaram 83 estudantes e 12 servidores. A especificação trabalha com aproximadamente 1.900 fotos e exige que consultas e navegação continuem disponíveis durante o processamento de imagens, IA, percursos e exportações (RNF001–RNF003). Também exige recuperação de falhas e proteção dos dados já enviados (RNF011–RNF012).

## Decisão

A API FastAPI e o worker Python compartilham o código do backend e podem rodar como processos separados. A API atende consultas e pedidos de alteração. O worker consome a tabela `jobs` para executar tarefas em segundo plano. A estrutura por módulos facilita localizar o trabalho relativo a cada requisito. [Responsabilidades dos módulos](../architecture/domain-boundaries.md)

## Consequências e verificação

O processo separado permite continuar atendendo a galeria enquanto um cálculo de rota ou uma exportação está em execução. Para concretizar esse comportamento, ainda é necessário ligar os fluxos do produto à fila e implementar os trabalhos de mídia, IA, percursos e exportações. A presença do worker, por si só, não comprova desempenho sob carga ou recuperação de resultados.

Na homologação, interromper um trabalho, retomá-lo e conferir se o registro original permanece íntegro. Repetir a operação com uma foto retirada enquanto o trabalho estava em andamento. O resultado só pode voltar ao atlas se ainda for atual e autorizado. [Persistência e retomada](ADR-0003-data-and-outbox-strategy.md)

