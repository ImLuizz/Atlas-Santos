# Módulo: Media (Armazenamento, Uploads e Processamento de Mídia)

## Responsabilidades
- Emissão de URLs temporárias pré-assinadas para upload direto ao Railway Buckets / S3 (RF-08, RN-03).
- Reserva e liberação de cotas com expiração (RN-04, proposta: 30 minutos).
- Finalização de upload: verificação de integridade (tamanho, checksum SHA-256) e criação de tarefa assíncrona para o Worker.
- Processamento assíncrono de imagem via Worker: rotação EXIF, geração de miniatura (até 480px), versão de exibição (até 2048px), e expurgo de metadados EXIF/GPS dos arquivos derivados públicos (RF-10, RNF-02).
- Reconciliação periódica entre banco e bucket para expurgar arquivos órfãos (RNF-16).

## Invariantes
- Nenhum arquivo é gravado permanentemente no filesystem local da aplicação.
- A chave final da mídia no bucket não pode ser sobrescrita por reuso de URL temporária (RF-09, RNF-07).
- Arquivos derivados divulgáveis jamais contêm metadados sensíveis ou GPS no cabeçalho EXIF (RNF-02).

