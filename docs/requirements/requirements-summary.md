# Requisitos do Atlas Santos

Fonte da revisão de 23/11/2026: *Especificação de requisitos — Atlas Santos*, arquivo recebido como `Atlas_Santos_Requisitos_do_Sistema_v1_3.pdf`. A capa informa **versão 1.2** e o histórico termina em **1.1**. Para identificar sem ambiguidade o documento de 16 páginas, seu SHA-256 é `8d5e0aae732cbdb02432af905007a17528e608a87746bcedf6640eb0b594ecc3`. A numeração abaixo segue as tabelas do PDF.

## Situação verificada em 23/11

O repositório contém a tela inicial, [as duas rotas de saúde da API](../../backend/app/api/v1/endpoints/health.py) e a [fila persistida no banco](../../backend/alembic/versions/2026_11_12_2155-45e99ca9977f_create_jobs_table.py).

A matriz funcional descreve o que falta demonstrar de ponta a ponta. A matriz de qualidade registra a infraestrutura disponível e as verificações pendentes.

## Requisitos funcionais

| ID | Página | Comportamento a verificar |
| --- | --- | --- |
| RF001 | 6 | A administração concilia os cadastros do IF-Arbitra e mantém os 83 estudantes, 12 servidores, equipes já formadas, capitães e um atlas por equipe. |
| RF002 | 6 | Ao provisionar cada conta, o sistema envia automaticamente o e-mail com as credenciais de acesso. |
| RF003 | 6 | Os três perfis entram com as credenciais recebidas e podem encerrar a sessão com segurança. |
| RF004 | 6 | A tela de login oferece redefinição de senha. |
| RF005 | 6 | O mapa apresenta os percursos estimados por equipe e dia de atividade. |
| RF006 | 6 | A visão geral mostra simultaneamente os percursos das equipes. |
| RF007 | 6 | A legenda interativa alterna entre dias e entre uma equipe e todas as equipes. |
| RF008 | 7 | Selecionar uma equipe aproxima e centraliza seu percurso em 3D. Voltar à visão geral restaura o enquadramento de todas as equipes. |
| RF009 | 7 | Fotos autorizadas com localização aparecem como marcadores. Selecionar um marcador abre foto, dados, legenda e reflexão disponíveis. |
| RF010 | 7 | Participantes e capitães enviam **uma foto por formulário**, dentro da cota (padrão de 20 por participante por atlas), com tema e reflexão opcionais. |
| RF011 | 7 | O formulário aproveita data, horário e coordenadas EXIF disponíveis para preencher os campos da foto. |
| RF012 | 7 | O autor pode informar ou corrigir data, horário e localização. |
| RF013 | 7 | A galeria mostra fotos aprovadas, destaca de início a equipe do usuário e combina filtros por equipe (inclusive todas) e dia. |
| RF014 | 8 | O autor reabre o registro com a foto e os dados existentes, altera os campos desejados sem reenviar a imagem e a edição volta à aprovação antes da nova exibição. |
| RF015 | 8 | O autor exclui seus registros e a administração pode retirar conteúdo. A retirada repercute na galeria, no mapa e nos percursos. |
| RF016 | 8 | Fotos enviadas por participantes entram na fila do capitão da equipe correspondente. |
| RF017 | 8 | O capitão analisa o registro completo, com imagem, dados, tema e reflexão, quando presentes. |
| RF018 | 8 | A aprovação disponibiliza o registro no atlas conforme as permissões. O envio inicial do próprio capitão recebe aprovação automática. |
| RF019 | 8 | A recusa exige uma justificativa que o participante consegue consultar. |
| RF020 | 8 | O capitão recebe o registro corrigido e decide sobre a nova versão. |
| RF021 | 9 | A reflexão opcional fica vinculada à foto no formulário de envio. |
| RF022 | 9 | A administração cadastra, edita e disponibiliza temas e perguntas orientadoras. |
| RF023 | 9 | A IA analisa o conteúdo visual da foto e usa a reflexão aprovada, quando houver. Na ausência dela, analisa só a imagem. |
| RF024 | 9 | As sugestões são identificadas como geradas por IA e distinguem o que pode ser observado de inferências incertas. |
| RF025 | 9 | O usuário escolhe, edita ou descarta a sugestão. O capitão revisa o texto escolhido com o registro antes da exibição. |
| RF026 | 10 | O backend usa roteamento pedestre para reconstruir automaticamente o percurso da equipe no dia, em ordem de captura, a partir de fotos aprovadas e localizadas. |
| RF027 | 10 | Para o dia selecionado, o mapa exibe o percurso de uma equipe ou os percursos de todas juntas. |
| RF028 | 10 | Com pontos insuficientes para traçar o caminho, os marcadores e fotos disponíveis continuam acessíveis. |
| RF029 | 10 | A síntese da viagem reúne apenas reflexões aprovadas de participantes e capitães. |
| RF030 | 10–11 | A IA relaciona os relatos às ideias verificáveis de *Sonho Manifesto*, de Sidarta Ribeiro, preserva seu sentido e evita conclusões representativas quando faltam contribuições. |
| RF031 | 11 | A administração revisa, pode editar e aprova a conclusão antes da publicação. |
| RF032 | 11 | Participantes e capitães podem consultar a síntese aprovada em uma página própria. |
| RF033 | 11 | PDF por equipe/dia com mapa, legenda, identificação e créditos, podendo incluir fotos selecionadas e textos aprovados. |
| RF034 | 11 | PNG da visualização filtrada com marcadores, percursos e resolução legível. |
| RF035 | 11 | GeoJSON dos pontos e trechos estimados, identificados como reconstruções. Cada posição usa longitude antes de latitude. |
| RF036 | 11–12 | Conferir permissões antes de gerar e disponibilizar cada exportação. Excluir campos privados, EXIF bruto, credenciais e precisão geográfica acima da autorizada. |

A visão geral (§1.1, p. 4) também prevê galeria, exportação HTML e organização por equipe/dia. O perfil administrativo (§1.2) inclui cotas, conciliação, rastreabilidade e privacidade. HTML permanece no planejamento com critérios de apresentação a detalhar. As prioridades acordadas são PDF/PNG primeiro, HTML/GeoJSON em seguida.

## Requisitos não funcionais

| ID | Página | Exigência e evidência necessária |
| --- | --- | --- |
| RNF001 | 12 | Atender ao uso simultâneo dos 95 participantes. Falta ensaio com consultas e contribuições representativas. |
| RNF002 | 12 | Armazenar e consultar cerca de 1.900 fotografias. Falta medir filtros, mapa e galeria com esse volume de teste. |
| RNF003 | 12 | Mídia, IA, rotas e exportações não bloqueiam a consulta. Há [worker e fila](../../backend/app/worker/dispatcher.py); falta exercitar os quatro tipos de operação durante a navegação. |
| RNF004 | 12 | Usar HTTPS em produção. Conferir o domínio publicado e a proteção da sessão no ambiente real. |
| RNF005 | 12 | O servidor verifica permissões por recurso. Testar os três perfis nos endpoints de negócio, inclusive alterações e retiradas. |
| RNF006 | 12 | Armazenar credenciais com segurança, invalidar sessões no logout/revogação e manter os segredos fora do navegador. A configuração é apenas parte da evidência. |
| RNF007 | 13 | Restringir originais, dados pessoais e localização precisa. Verificar remoção de todo EXIF nos derivados exibidos. |
| RNF008 | 13 | Compartilhar o mínimo autorizado com serviços externos. Conferir as restrições da fonte nas rotas e exportações. |
| RNF009 | 13 | Verificar os fluxos principais em computador, tablet e celular. Uma página inicial responsiva não comprova os fluxos futuros. |
| RNF010 | 13 | Testar rótulos, foco, teclado, erros associados, alternativa em lista ao mapa e estados reconhecíveis além da cor. |
| RNF011 | 13 | Edições, exclusões e aprovações atualizam o acervo e atualizam ou invalidam resultados dependentes de registros antigos. |
| RNF012 | 14 | Recuperar falhas e permitir nova tentativa com preservação dos registros. Testar também indisponibilidade de cada provedor sem interromper consultas independentes. |
| RNF013 | 14 | Servidor valida formato, tamanho e características do arquivo. Textos e imagens de participantes são dados, inclusive na entrada da IA. |
| RNF014 | 14 | Mapas e exportações exibem os créditos exigidos e a integração respeita os termos de cada provedor. Conferir na saída efetiva. |
| RNF015 | 14 | Railway com configurações próprias para desenvolvimento, homologação e produção. O guia de implantação precisa ser validado nesses ambientes. |
| RNF016 | 14–15 | A API expõe o esquema OpenAPI em `/openapi.json`. Documentar contratos, erros consistentes e mensagens seguras nos endpoints de negócio à medida que forem entregues. |
| RNF017 | 15 | Testar backup e restauração conjunta do PostgreSQL e dos arquivos, preservando os vínculos e respeitando retiradas. |
| RNF018 | 15 | Python/FastAPI presentes no [ponto de entrada da API](../../backend/app/main.py). |
| RNF019 | 15 | React com JavaScript/JSX, Vite e Tailwind presentes no [frontend](../../frontend/package.json). |
| RNF020 | 15 | PostgreSQL com SQLAlchemy e Alembic configurados. A tabela de tarefas é infraestrutura; as entidades de participantes, fotos e curadoria ainda precisam de persistência e testes próprios. |
| RNF021 | 15 | Armazenar fotos e arquivos gerados em Railway Buckets compatível com S3. Há [contrato de armazenamento](../../backend/app/integrations/storage/base.py); falta exercício com bucket autorizado. |
| RNF022 | 15 | Validar hospedagem Railway e isolamento entre desenvolvimento e produção, incluindo homologação prevista em RNF015. |
| RNF023 | 15 | O frontend já declara Mapbox GL JS e deck.gl e aceita o token público. Falta renderizar o mapa, os pontos e os percursos e validar a consulta com dados autorizados. |
| RNF024 | 15 | O [contrato de roteamento](../../backend/app/integrations/routing/base.py) deve se ligar a um serviço pedestre no backend. Falta a integração operacional. |
| RNF025 | 16 | Integrar o backend a serviço de IA para descrições de fotos e conclusão coletiva. O [contrato](../../backend/app/integrations/ai/base.py) não comprova processamento com provedor. |

## Pontos que exigem decisão da equipe

- **Nova edição de uma foto do capitão.** RF018 dá aprovação automática ao envio de foto própria. RF014 manda qualquer edição voltar à aprovação. Especificar como o capitão revisa a edição da própria foto, mantendo a regra explícita de reavaliação. RF025 exige revisão do texto escolhido antes de exibi-lo.
- **Cota.** RF010 fixa 20 como limite e §1.2 descreve 20 como padrão com gestão administrativa. Manter o padrão por participante/atlas e definir a política de alteração da cota e contagem de retiradas e recusas. A cota deve resistir a envios simultâneos.
- **Divulgação e operação.** Definir o público autorizado, a precisão geográfica por público, os limites de arquivo e o procedimento de recuperação. A especificação exige controle, atribuição e recuperação; os provedores de IA e de roteamento, os prazos de retenção e os objetivos de recuperação ainda precisam de decisão operacional.
- **Conclusão e HTML.** A equipe pedagógica precisa definir como reconhecer contribuições insuficientes e validar a relação com o livro. Para o HTML, falta especificar o conteúdo e o comportamento do arquivo exportado.
