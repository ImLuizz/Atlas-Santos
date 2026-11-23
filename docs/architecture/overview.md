# Arquitetura do Atlas Santos

O atlas de cada equipe reúne as fotografias e reflexões do estudo do meio em Santos, de 5 a 11 de outubro de 2026. A referência de capacidade é de 95 participantes e aproximadamente 1.900 fotos. A comprovação de desempenho depende de testes com esse volume (RNF001–RNF003).

## O que existe no repositório

O frontend usa React, Vite e Tailwind CSS. A API FastAPI expõe consultas de saúde. O backend contém o modelo SQLAlchemy de tarefas, a migração Alembic correspondente e um processo Python para consumir a fila. Os diretórios dos módulos separam o trabalho futuro. A presença de um diretório, de um adaptador abstrato ou da fila não comprova a entrega do respectivo fluxo. [Contratos HTTP disponíveis](../api/README.md)

## Fluxo que a arquitetura deve atender

1. A administração confere os dados do IF-Arbitra, os vínculos das equipes e seus capitães. O sistema envia automaticamente as credenciais de acesso por e-mail. A tela de login oferece redefinição de senha (RF001–RF004).
2. O participante envia uma foto por formulário e pode acrescentar tema e reflexão. O horário e a localização extraídos do EXIF preenchem o formulário quando disponíveis. O autor pode informar ou corrigir os dados. O limite de referência é 20 fotos por participante no atlas (RF010–RF012, RF021–RF022).
3. O capitão avalia o registro completo da equipe. A aprovação o disponibiliza ao público autorizado. A autoria do capitão tem o tratamento de envio previsto em RF018. Edições, reenvios e retiradas seguem o [fluxo editorial](state-machine.md).
4. O backend reconstrói automaticamente o percurso por equipe e dia, usando os registros aprovados com localização, em ordem cronológica, e um serviço de roteamento a pé. A interface usa a base do Mapbox e camadas deck.gl para pontos e percursos. A legenda alterna equipes e dias. A seleção de uma equipe centraliza e aproxima sua vista em 3D, e a visão geral permite comparar todas. Marcadores autorizados continuam disponíveis quando faltam pontos para traçar um caminho (RF005–RF009, RF026–RF028, RNF023–RNF024).
5. A galeria destaca inicialmente a equipe do usuário e permite combinar dia e equipe, incluindo todas as equipes. Os dados do mapa também devem estar disponíveis em lista (RF013, RNF010).
6. A IA auxilia em duas atividades distintas. Sugere descrições para uma foto com base na imagem e na eventual reflexão aprovada. Também reúne reflexões aprovadas para propor uma conclusão coletiva, que a administração revisa antes de disponibilizá-la em página própria (RF023–RF025, RF029–RF032, RNF025).
7. O PDF organiza o recorte com mapa, legenda, créditos e fotos selecionadas. O PNG preserva a vista filtrada do mapa. O GeoJSON representa pontos e percursos estimados. A visão geral da especificação também cita HTML, ainda sem contrato detalhado. A autorização e o nível de precisão permitido acompanham os dados até a entrega do arquivo (RF033–RF036, RNF008, RNF014).

## Dados e execução

O PostgreSQL deverá manter vínculos, metadados, decisões editoriais e referências aos arquivos. O armazenamento previsto para originais, derivados e exportações é o Railway Buckets. As versões de exibição devem ter o EXIF removido. O backend deve controlar o acesso a dados precisos e limitar o envio a terceiros ao necessário para cada operação (RNF005–RNF008, RNF020–RNF021).

A API e o worker compartilham o código de negócio. A fila permite implementar processamento de mídia, IA, roteamento e exportação fora das consultas interativas. Ao concluir um trabalho, o resultado precisa continuar compatível com a versão autorizada dos dados de origem. A equipe deve verificar os cenários de falha, nova tentativa e retirada (RNF003, RNF011–RNF012). [Decisão sobre persistência e fila](../decisions/ADR-0003-data-and-outbox-strategy.md)

