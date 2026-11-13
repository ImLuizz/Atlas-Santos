# Módulo: AI (Descrições Assistidas por Inteligência Artificial)

## Responsabilidades
- Análise multimodal da imagem (derivado sem EXIF) e reflexão aprovada associada para sugerir descrições curtas da fotografia (RF-21, RF-22).
- Geração de alternativas curtas e editáveis (proposta: até 3 alternativas com até 600 caracteres cada, RF-22, D-06).
- Rastreamento das fontes, modelo utilizado, prompt/instruções e consumo de tokens para controle de custos (RF-22, RNF-08).
- Sinalização de divergências entre imagem e texto sem harmonização fictícia.

## Invariantes e Segurança
- O modelo de IA é tratado como fornecedor não confiável; suas saídas jamais aprovam ou publicam conteúdo automaticamente (RN-14).
- O envio ao provedor restringe-se a imagens sem metadados EXIF/GPS e reflexões com autorização de compartilhamento (RNF-02, D-04).
- Proteção contra prompt injection em textos de participantes ou metadados de imagens (RNF-07).
- A ausência ou falha da IA mantém integralmente a edição e descrição manual disponível (RF-22, RNF-06).

