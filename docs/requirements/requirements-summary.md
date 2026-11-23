# Atlas Santos · Requisitos do sistema

De 5 a 11 de outubro de 2026, 83 estudantes e 12 servidores do IFSP Campus Araraquara participaram do estudo do meio em Santos. Cada equipe terá seu próprio atlas para reunir as fotografias da viagem, registrar reflexões e revisitar os caminhos que provavelmente percorreu em cada dia.

**Onde o projeto está hoje.** Em 23 de novembro, a página inicial na Vercel já se comunicava com a API e o PostgreSQL no Railway. O código também inclui um worker para processar tarefas em segundo plano. Cadastro, envio de fotos, curadoria, mapas e exportações fazem parte das próximas entregas.

## O que o Atlas precisa fazer

Os códigos e as páginas nas tabelas correspondem à especificação original. Assim, quem desenvolve e quem revisa pode citar a mesma regra.

### Contas e equipes

A administração também acompanha o histórico das alterações no acervo, gerencia as cotas e define quem pode acessar os dados, conforme o perfil administrativo descrito na seção 1.2 da especificação.

| Código | Regra | Pág. |
| --- | --- | --- |
| RF001 | A administração confere os cadastros vindos do IF-Arbitra e mantém os 83 estudantes, os 12 servidores e a composição das equipes. Cada equipe tem um capitão e um atlas. | 6 |
| RF002 | Quando uma conta é criada, seu titular recebe automaticamente por e-mail as credenciais de acesso. | 6 |
| RF003 | Participantes, capitães e administradores entram com suas credenciais e podem encerrar a sessão com segurança. | 6 |
| RF004 | Quem esquecer a senha pode redefini-la pela própria tela de login. | 6 |

### Consulta ao mapa

| Código | Regra | Pág. |
| --- | --- | --- |
| RF005 | O mapa mostra o percurso estimado de cada equipe por dia de atividade. | 6 |
| RF006 | Na visão geral, os percursos das equipes aparecem juntos para permitir a comparação. | 6 |
| RF007 | Pela legenda, é possível mudar o dia e escolher entre uma equipe e todas as equipes. | 6 |
| RF008 | Ao selecionar uma equipe, o mapa aproxima e centraliza seu percurso em 3D. Ao voltar à visão geral, todas as equipes voltam a caber na tela. | 7 |
| RF009 | Cada foto autorizada que tenha localização aparece como um marcador. Ao abri-lo, a pessoa vê a imagem e, quando disponíveis, seus dados, a legenda e a reflexão. | 7 |

### Envio de fotos e galeria

| Código | Regra | Pág. |
| --- | --- | --- |
| RF010 | Participantes e capitães enviam uma foto por formulário. A cota padrão é de 20 fotos por pessoa em cada atlas. Tema e reflexão são opcionais. | 7 |
| RF011 | Se o arquivo contiver metadados EXIF, o formulário aproveita a data, o horário e as coordenadas disponíveis. | 7 |
| RF012 | O autor pode preencher ou corrigir a data, o horário e o local da foto. | 7 |
| RF013 | A galeria abre com as fotos aprovadas da equipe de quem está consultando. Os filtros de equipe e dia podem ser combinados, inclusive para ver todas as equipes. | 7 |
| RF014 | Ao editar um registro, o autor encontra a foto e os dados já preenchidos. Pode alterar os campos sem reenviar a imagem. A versão editada volta à curadoria antes de ser exibida. | 8 |
| RF015 | O autor pode excluir seus registros, e a administração pode retirar conteúdo. A galeria, o mapa e os percursos devem refletir a retirada. | 8 |

### Curadoria dos capitães

| Código | Regra | Pág. |
| --- | --- | --- |
| RF016 | As fotos enviadas por estudantes e servidores vão para a fila de revisão do capitão da respectiva equipe. | 8 |
| RF017 | O capitão revisa a imagem e os dados do registro, incluindo tema e reflexão quando o autor os tiver preenchido. | 8 |
| RF018 | A aprovação torna o registro visível a quem tem acesso ao atlas. A foto enviada pelo próprio capitão recebe aprovação automática no primeiro envio. | 8 |
| RF019 | Ao recusar um registro, o capitão escreve uma justificativa que o autor pode consultar. | 8 |
| RF020 | Depois que o autor corrige o registro, o capitão recebe a nova versão e decide se ela pode entrar no atlas. | 8 |

### Olhares sobre Santos

| Código | Regra | Pág. |
| --- | --- | --- |
| RF021 | No formulário de envio, o autor pode escrever uma reflexão. O texto fica vinculado à fotografia que motivou o relato. | 9 |
| RF022 | A administração cadastra, edita e disponibiliza temas e perguntas para orientar as reflexões. | 9 |
| RF023 | A IA sugere descrições com base no que aparece na foto. Quando há uma reflexão aprovada, ela também serve de referência. | 9 |
| RF024 | Cada sugestão traz a indicação de que foi gerada por IA. O texto distingue detalhes visíveis de interpretações incertas. | 9 |
| RF025 | O usuário pode escolher, editar ou descartar a sugestão. Antes da exibição, o capitão revisa o texto escolhido junto com a foto. | 9 |

### Reconstrução dos percursos

| Código | Regra | Pág. |
| --- | --- | --- |
| RF026 | Para cada equipe e dia, o backend ordena as fotos aprovadas e localizadas pelo horário de captura. A partir desses pontos, calcula automaticamente um caminho provável a pé pelas ruas. | 10 |
| RF027 | Para o dia escolhido, é possível ver o trajeto de uma equipe ou comparar os trajetos de todas no mesmo mapa. | 10 |
| RF028 | Quando há poucos pontos para estimar um caminho, o mapa continua mostrando os marcadores e as fotos disponíveis. | 10 |

### Conclusão coletiva da viagem

| Código | Regra | Pág. |
| --- | --- | --- |
| RF029 | A conclusão coletiva usa exclusivamente reflexões aprovadas de participantes e capitães. | 10 |
| RF030 | A IA relaciona os relatos a ideias que possam ser conferidas em *Sonho Manifesto*, de Sidarta Ribeiro. O texto preserva o sentido dos relatos. Se houver poucas contribuições, deve evitar generalizações sobre o grupo. | 10–11 |
| RF031 | A administração lê a conclusão, pode editar o texto e aprova a versão que será publicada. | 11 |
| RF032 | Participantes e capitães encontram a conclusão aprovada em uma página própria do Atlas. | 11 |

### Exportações

PDF e PNG têm prioridade. Na sequência entram HTML e GeoJSON. O HTML aparece na visão geral da especificação (§1.1, p. 4), e a equipe ainda precisa definir o conteúdo e a navegação desse arquivo.

| Código | Regra | Pág. |
| --- | --- | --- |
| RF033 | O PDF identifica a equipe e o dia e traz mapa, legenda e créditos. Também pode incluir fotos selecionadas e textos aprovados. | 11 |
| RF034 | O PNG reproduz a visualização filtrada do mapa, com marcadores e percursos legíveis na imagem exportada. | 11 |
| RF035 | O GeoJSON identifica os pontos fotográficos e os trechos reconstruídos, deixando claro que o percurso é estimado. Cada coordenada segue a ordem longitude, latitude. | 11 |
| RF036 | O sistema confere as permissões ao gerar e ao disponibilizar a exportação. O arquivo exclui campos privados, EXIF bruto e credenciais, e respeita a precisão de localização autorizada. | 11–12 |

## Requisitos de qualidade e operação

### Capacidade e continuidade

| Código | O que a equipe precisa garantir | Pág. |
| --- | --- | --- |
| RNF001 | O Atlas deve atender aos 95 participantes ao mesmo tempo. O teste de carga precisa combinar consultas e contribuições, como ocorreria durante o uso pela turma. | 12 |
| RNF002 | Com a cota padrão, o acervo pode chegar a cerca de 1.900 fotos. É com esse volume que a equipe deve testar armazenamento, filtros, mapa e galeria. | 12 |
| RNF003 | As pessoas devem conseguir navegar enquanto o sistema processa imagens, executa tarefas de IA, calcula percursos ou gera exportações. A fila já existe. Falta testar essas quatro operações durante a consulta ao atlas. | 12 |
| RNF011 | Edições, exclusões e aprovações devem atualizar o acervo. Resultados que dependem de uma versão antiga precisam ser atualizados ou invalidados. | 13 |
| RNF012 | Se uma operação falhar, deve ser possível tentar novamente sem perder o registro. A indisponibilidade de um provedor deve preservar as consultas que independem dele. | 14 |

### Acesso, privacidade e uso dos dados

| Código | O que a equipe precisa garantir | Pág. |
| --- | --- | --- |
| RNF004 | O acesso em produção usa HTTPS. A proteção da sessão deve ser verificada no ambiente publicado quando o login estiver disponível. | 12 |
| RNF005 | O servidor confere a permissão em cada recurso. Os testes devem cobrir os três perfis, inclusive tentativas de alterar ou retirar conteúdo. | 12 |
| RNF006 | O sistema guarda as credenciais com segurança, mantém os segredos do servidor fora do navegador e invalida a sessão quando o usuário sai ou o acesso é revogado. | 12 |
| RNF007 | O acesso aos originais, aos dados pessoais e às coordenadas precisas é restrito. As cópias exibidas devem ter todos os metadados EXIF removidos. | 13 |
| RNF008 | Os serviços externos recebem apenas os dados necessários e autorizados. As restrições de uso da fonte também valem para percursos e exportações. | 13 |
| RNF013 | O servidor valida formato, tamanho e características do arquivo enviado. Textos e imagens dos participantes são tratados como conteúdo a analisar, inclusive quando chegam à IA. | 14 |
| RNF014 | Mapas e arquivos exportados exibem os créditos exigidos. O uso dos dados e dos serviços segue os termos de cada provedor. | 14 |

### Dispositivos e acessibilidade

| Código | O que a equipe precisa garantir | Pág. |
| --- | --- | --- |
| RNF009 | Os fluxos principais devem funcionar em computador, tablet e celular. Cada fluxo precisa ser testado nos três formatos à medida que for entregue. | 13 |
| RNF010 | Os campos têm rótulos, os erros indicam o campo correspondente e o foco fica visível ao navegar pelo teclado. Há uma alternativa em lista ao mapa. Os estados da interface também podem ser reconhecidos por sinais além da cor. | 13 |

### Tecnologia e manutenção

| Código | O que a equipe precisa garantir | Pág. |
| --- | --- | --- |
| RNF015 | Desenvolvimento, homologação e produção têm configurações próprias no Railway. A equipe precisa verificar a implantação em cada ambiente. | 14 |
| RNF016 | A API publica seu contrato OpenAPI em `/openapi.json`. Cada nova operação deve documentar as respostas e usar mensagens de erro consistentes, que possam ser mostradas sem expor dados internos. | 14–15 |
| RNF017 | A restauração de um backup deve recuperar o PostgreSQL e os arquivos correspondentes, preservar os vínculos entre eles e respeitar as retiradas de conteúdo. A equipe precisa testar essa recuperação conjunta. | 15 |
| RNF018 | O backend usa Python e FastAPI. [Código da API](../../backend/app/main.py) | 15 |
| RNF019 | A interface usa React com JavaScript/JSX, Vite e Tailwind CSS. [Dependências do frontend](../../frontend/package.json) | 15 |
| RNF020 | Os dados ficam no PostgreSQL, com SQLAlchemy e migrações Alembic. A tabela de tarefas já existe. Ainda faltam as tabelas e os testes de participantes, fotos e curadoria. | 15 |
| RNF021 | Fotos e arquivos gerados ficam no Railway Buckets, com interface compatível com S3. O código já define as operações de armazenamento. Falta testá-las em um bucket autorizado. | 15 |
| RNF022 | Na hospedagem no Railway, a equipe verifica se os ambientes estão isolados entre si, inclusive o de homologação previsto em RNF015. | 15 |
| RNF023 | O mapa usa Mapbox GL JS e deck.gl. As dependências e a configuração do token público já existem. Falta exibir os pontos e os percursos e conferir a visualização com as permissões de cada perfil. | 15 |
| RNF024 | O backend consulta um serviço de roteamento a pé para estimar os caminhos. A interface de integração já está definida e ainda precisa ser conectada ao provedor. | 15 |
| RNF025 | O backend integra o serviço de IA usado nas descrições das fotos e na conclusão coletiva. A interface está definida e os dois fluxos ainda precisam ser testados com o provedor. | 16 |

## Decisões em aberto

- **Foto do capitão.** A aprovação automática vale para o primeiro envio (RF018). Quem revisa uma edição posterior da própria foto do capitão, inclusive se ele alterar a descrição sugerida pela IA (RF014 e RF025)?
- **Cota individual.** A administração pode ajustar o padrão de 20 fotos por pessoa em cada atlas. Quando uma recusa ou retirada libera uma vaga? Como aplicar uma mudança de limite a quem já enviou fotos? Dois envios simultâneos precisam respeitar a mesma cota.
- **Visibilidade e precisão.** Quem pode consultar e exportar cada atlas? Até que precisão o mapa e os arquivos podem mostrar a localização para cada público?
- **Operação.** Faltam definir os limites dos arquivos, os provedores de IA e roteamento, os prazos de retenção e o procedimento de recuperação, incluindo quanto tempo e quanta perda de dados são aceitáveis.
- **Revisão pedagógica.** Que critérios a equipe vai usar para avaliar se há relatos suficientes para uma conclusão coletiva e se a relação com o livro é fiel ao texto?
- **Exportação HTML.** Quais elementos do atlas o arquivo deve incluir e como a pessoa vai navegar por eles?

<details>
<summary>Documento de referência</summary>

*Especificação de requisitos — Atlas Santos*, 16 páginas. A equipe recebeu o arquivo `Atlas_Santos_Requisitos_do_Sistema_v1_3.pdf`. A capa indica versão 1.2 e o histórico de revisões termina em 1.1. A numeração e as páginas desta matriz seguem as tabelas desse arquivo.

SHA-256 do PDF: `8d5e0aae732cbdb02432af905007a17528e608a87746bcedf6640eb0b594ecc3`.

</details>
