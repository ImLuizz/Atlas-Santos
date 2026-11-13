# Módulo: Exports (Exportações de Acervo e Cartografia)

## Responsabilidades
- Geração assíncrona via Worker de relatórios e painéis visuais:
  - **P1**: PDF (A4 com mapa, créditos, legendas e fotos) e PNG (resumo visual 2400x1600px) (RF-26).
  - **P2**: HTML portátil autocontido e GeoJSON padronizado (longitude antes de latitude) (RF-27).
- Ciclo de vida das tarefas de exportação (na fila, processando, concluída, falhou, expirada, invalidada) (RF-28).
- Aplicação de atribuição de direitos autorais cartográficos do OpenStreetMap em todos os artefatos (RNF-09).

## Invariantes
- A geração utiliza um snapshot imutável das revisões aprovadas das fontes (RF-28).
- Nenhum dado privado, EXIF bruto ou chave interna do bucket pode vazar para os arquivos exportados (RF-27).
- A alteração ou remoção de fotos-fonte invalida as exportações hospedadas dependentes (RN-16, RNF-15).

