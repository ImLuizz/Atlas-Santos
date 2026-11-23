# ADR-0003 · Dados, fila e armazenamento

Registro original de 12/11/2026. O código inicial inclui a migração da tabela de tarefas no PostgreSQL e o processo consumidor. Os fluxos abaixo descrevem como as funcionalidades deverão usar essa infraestrutura.

## Banco e arquivos

O PostgreSQL deve guardar o vínculo entre a foto, o autor, a equipe, a revisão do registro e o arquivo correspondente. O Railway Buckets deve guardar as imagens originais privadas, os derivados de exibição sem EXIF e os arquivos exportados (RNF007, RNF017, RNF020–RNF021). As decisões sobre retenção e restauração precisam abranger banco e arquivos em conjunto. [Recuperação dos dados](../operations/backup-and-retention.md)

A integração prevista usa upload direto ao bucket. O backend deverá autorizar a operação, controlar a cota por participante no atlas e conferir formato, tamanho e conteúdo antes de disponibilizar a imagem. Ao repetir uma confirmação ou retomar um envio, o resultado deve continuar consistente (RF010, RNF005, RNF011–RNF013). A equipe pode ajustar limites técnicos e duração de URLs conforme o armazenamento e os testes. O PDF não fixa esses números.

## Fila persistente

A decisão de usar a tabela `jobs` evita introduzir um serviço de fila adicional nesta etapa. Quando um fluxo gravar dados de negócio e solicitar trabalho, a proposta é registrar ambos na mesma transação. O processamento externo exige controles próprios para impedir a publicação de resultados duplicados, revogados ou obsoletos.

Uma foto aprovada com coordenadas pode afetar o percurso de uma equipe em um dia. Se ela for retirada enquanto o serviço calcula o trajeto, o retorno antigo deve ser descartado ou invalidado. O sistema pode recalcular a partir dos registros autorizados restantes. A falha do roteador não deve bloquear a consulta às fotografias (RF015, RF026–RF028, RNF008, RNF011–RNF012).

## O que medir

Testar a consulta simultânea ao acervo de aproximadamente 1.900 fotos, a recuperação após interrupção de uma tarefa e a consistência das cotas quando envios forem repetidos ou concorrentes. Um teste de conectividade com o banco verifica apenas a consulta usada pela sonda. [Contratos implementados](../api/README.md)

